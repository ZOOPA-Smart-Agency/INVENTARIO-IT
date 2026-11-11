"""Inventario updater: installs new releases of the app on this server.

It runs in its own container, next to the database, the app (web) and the web server (caddy). Every few
seconds it:

* tells the app it is alive and which version is running (table inventory_updaterstate);
* checks GitHub for the latest release when asked to, or once an hour, through a GitHub App that can only
  read this repository;
* installs a release an administrator asked for (table inventory_updatejob), or one due by the automatic
  schedule (Settings > General > Updates).

Installing a release: the app goes into maintenance, the database is backed up, the release's source is
downloaded and built into a new image, the app restarts on it (it applies its own database changes), and
the updater checks it answers with the new version. If any step after the restart fails, the previous
version and the backed-up database are put back, so the app is never left half-updated.

Only the latest published release of the configured repository can be installed, whatever the request says.
The web app never gets access to Docker; it can only ask for that release.
"""
import base64
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
PHASES = ["backup", "download", "build", "restart", "check"]
DEPLOY_FILES = ["docker-compose.yml", "Caddyfile", "maintenance.html"]
API = "https://api.github.com"
SEP = "\x1f"


def log(message):
    print(f"{datetime.now().isoformat(timespec='seconds')} {message}", flush=True)


class Failed(Exception):
    """A step that did not work; the message is shown in the update history."""


def version_tuple(value):
    match = TAG.match(value if str(value).startswith("v") else f"v{value}")
    return tuple(int(n) for n in match.groups()) if match else None


# ---- configuration ------------------------------------------------------------------


class Config:
    def __init__(self, env=os.environ):
        self.install_dir = Path(env.get("INSTALL_DIR", "/opt/inventario"))
        self.project = env.get("COMPOSE_PROJECT_NAME", "inventario")
        self.repo = env.get("APP_UPDATE_REPO", "").strip()
        self.app_id = env.get("APP_UPDATE_GITHUB_APP_ID", "").strip()
        self.key_file = Path(env.get("APP_UPDATE_GITHUB_APP_PRIVATE_KEY_FILE", "/run/secrets/github-app.pem"))
        self.db_user = env.get("POSTGRES_USER", "inventario")
        self.db_name = env.get("POSTGRES_DB", "inventario")
        self.health_url = env.get("HEALTH_URL", "http://web:8000/healthz")
        self.timezone = ZoneInfo(env.get("TZ", "Europe/Madrid"))
        self.keep_backups = int(env.get("KEEP_UPDATE_BACKUPS", "5"))
        self.health_timeout = int(env.get("HEALTH_TIMEOUT", "240"))
        self.poll_seconds = int(env.get("POLL_SECONDS", "5"))
        self.api = (env.get("APP_UPDATE_API", "") or API).rstrip("/")  # only changed to test against a stand-in for GitHub

    @property
    def compose(self):
        d = self.install_dir
        return ["docker", "compose", "--project-name", self.project, "--project-directory", str(d),
                "-f", str(d / "docker-compose.yml"), "--env-file", str(d / ".env")]


def shell(args, input=None, timeout=1800):
    """Runs a command; returns its output as bytes. Raises Failed with the command's last error lines."""
    try:
        done = subprocess.run(args, input=input, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Failed(f"{args[0]}: {e}")
    if done.returncode != 0:
        tail = done.stderr.decode(errors="replace").strip().splitlines()[-6:]
        raise Failed(f"{' '.join(args[:4])}…: " + " / ".join(tail))
    return done.stdout


# ---- the app's database -----------------------------------------------------------------


class Db:
    """Talks to the app's database with psql inside the database container. Values are passed as psql
    variables (-v), never pasted into the SQL."""

    def __init__(self, psql_prefix, run=shell):
        self.prefix = psql_prefix
        self.run = run

    def sql(self, statement, **values):
        args = [*self.prefix, "-X", "-q", "-A", "-t", "-F", SEP, "-v", "ON_ERROR_STOP=1"]
        for name, value in values.items():
            args += ["-v", f"{name}={'' if value is None else value}"]
        out = self.run(args, input=statement.encode()).decode()
        return [line.split(SEP) for line in out.splitlines() if line.strip()]

    def heartbeat(self, running):
        self.sql("""INSERT INTO inventory_updaterstate (id, last_seen, running_version, latest_tag, latest_name, latest_notes,
                      latest_url, latest_published, check_status, checked_at, check_requested)
                    VALUES (1, now(), :'v', '', '', '', '', NULL, '', NULL, false)
                    ON CONFLICT (id) DO UPDATE SET last_seen = now(), running_version = :'v';""", v=running)

    def state(self):
        rows = self.sql("SELECT check_requested, COALESCE(extract(epoch FROM checked_at), 0), latest_tag "
                        "FROM inventory_updaterstate WHERE id = 1;")
        if not rows:
            return {"check_requested": False, "checked_at": 0.0, "latest_tag": ""}
        requested, checked, tag = rows[0]
        return {"check_requested": requested == "t", "checked_at": float(checked), "latest_tag": tag}

    def save_check(self, status, release=None):
        r = release or {}
        self.sql("""UPDATE inventory_updaterstate SET check_status = :'status', checked_at = now(), check_requested = false,
                      latest_tag = :'tag', latest_name = :'name', latest_notes = :'notes', latest_url = :'url',
                      latest_published = NULLIF(:'published', '')::timestamptz
                    WHERE id = 1;""",
                 status=status, tag=r.get("tag", ""), name=r.get("name", ""), notes=r.get("notes", ""),
                 url=r.get("url", ""), published=r.get("published", "") or "")

    def schedule(self):
        rows = self.sql("SELECT auto_update, auto_update_hour FROM inventory_appsettings WHERE id = 1;")
        return (rows[0][0] == "t", int(rows[0][1])) if rows else (False, 3)

    def next_job(self):
        rows = self.sql("SELECT id, target, requested_by, automatic FROM inventory_updatejob "
                        "WHERE status = 'queued' ORDER BY id LIMIT 1;")
        return {"id": int(rows[0][0]), "target": rows[0][1], "by": rows[0][2], "automatic": rows[0][3] == "t"} if rows else None

    def automatic_job_since(self, since_epoch):
        rows = self.sql("SELECT count(*) FROM inventory_updatejob WHERE automatic AND created_at >= to_timestamp(:'since');",
                        since=since_epoch)
        return int(rows[0][0]) > 0

    def queue_automatic(self, target, running):
        self.sql("""INSERT INTO inventory_updatejob (created_at, requested_by, automatic, from_version, target, status, phase, message)
                    VALUES (now(), '', true, :'from', :'target', 'queued', '', '');""", target=target, **{"from": running})

    def job(self, job_id, status=None, phase=None, message=None, from_version=None, finished=False):
        self.sql("""UPDATE inventory_updatejob SET
                      status = COALESCE(NULLIF(:'status', ''), status), phase = COALESCE(NULLIF(:'phase', ''), phase),
                      message = CASE WHEN :'setmsg' = 'yes' THEN :'message' ELSE message END,
                      from_version = COALESCE(NULLIF(:'from', ''), from_version),
                      finished_at = CASE WHEN :'finished' = 'yes' THEN now() ELSE finished_at END
                    WHERE id = :'id'::int;""",
                 id=job_id, status=status or "", phase=phase or "", message=message or "", setmsg="no" if message is None else "yes",
                 finished="yes" if finished else "no", **{"from": from_version or ""})

    def maintenance(self, phase, step, by):
        self.sql("""INSERT INTO inventory_maintenance (id, active, kind, started_at, started_by, phase, done, total, updated_at)
                    VALUES (1, true, 'update', now(), :'by', :'phase', :'done'::int, :'total'::int, now())
                    ON CONFLICT (id) DO UPDATE SET active = true, kind = 'update', phase = :'phase', done = :'done'::int,
                      total = :'total'::int, updated_at = now(),
                      started_by = CASE WHEN inventory_maintenance.active AND inventory_maintenance.kind = 'update'
                                   THEN inventory_maintenance.started_by ELSE :'by' END,
                      started_at = CASE WHEN inventory_maintenance.active AND inventory_maintenance.kind = 'update'
                                   THEN inventory_maintenance.started_at ELSE now() END;""",
                 phase=phase, done=step, total=len(PHASES), by=by)

    def touch_maintenance(self):
        self.sql("UPDATE inventory_maintenance SET updated_at = now() WHERE id = 1 AND active;")

    def end_maintenance(self):
        self.sql("UPDATE inventory_maintenance SET active = false, phase = '', done = 0, total = 0, updated_at = now() WHERE id = 1;")


# ---- GitHub, through a GitHub App that can only read this repository ---------------------


def _b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


class GitHub:
    def __init__(self, config, open_url=urllib.request.urlopen, now=time.time):
        self.config, self.open_url, self.now = config, open_url, now
        self.token, self.token_expires = None, 0.0

    def _request(self, url, token=None, body=None, limit=1_000_000):
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "inventario-updater"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        data = None if body is None else json.dumps(body).encode()
        request = urllib.request.Request(url, headers=headers, data=data, method="GET" if body is None else "POST")
        with self.open_url(request, timeout=60) as response:
            content = response.read(limit + 1)
        if len(content) > limit:
            raise Failed("GitHub sent more data than expected")
        return content

    def _jwt(self):
        try:
            key = serialization.load_pem_private_key(self.config.key_file.read_bytes(), password=None)
        except (OSError, ValueError, TypeError):
            raise Failed("app_key")
        now = int(self.now())
        header = _b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
        claims = _b64(json.dumps({"iat": now - 60, "exp": now + 540, "iss": str(self.config.app_id)}).encode())
        return f"{header}.{claims}.{_b64(key.sign(f'{header}.{claims}'.encode(), padding.PKCS1v15(), hashes.SHA256()))}"

    def _token(self):
        if self.token and self.now() < self.token_expires:
            return self.token
        if not self.config.app_id:
            return None  # a public repository needs no sign-in
        jwt, repo = self._jwt(), self.config.repo
        try:
            installation = json.loads(self._request(f"{self.config.api}/repos/{repo}/installation", jwt))
            granted = json.loads(self._request(f"{self.config.api}/app/installations/{int(installation['id'])}/access_tokens", jwt,
                                               {"repositories": [repo.split('/', 1)[1]], "permissions": {"contents": "read"}}))
        except urllib.error.HTTPError as e:
            raise Failed("app_missing" if e.code == 404 else "auth")
        self.token, self.token_expires = granted["token"], self.now() + 50 * 60
        return self.token

    def latest(self):
        """The latest published release (pre-releases and drafts are never offered), or None."""
        try:
            data = json.loads(self._request(f"{self.config.api}/repos/{self.config.repo}/releases/latest", self._token()))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code in (401, 403):
                self.token = None
                raise Failed("auth")
            raise Failed("error")
        url = str(data.get("html_url") or "")
        return {"tag": str(data.get("tag_name") or ""), "name": str(data.get("name") or "")[:200],
                "notes": str(data.get("body") or "")[:5000], "url": url if url.startswith("https://github.com/") else "",
                "published": str(data.get("published_at") or "")}

    def source(self, tag):
        """The release's source code as a .tar.gz (up to 200 MB)."""
        try:
            return self._request(f"{self.config.api}/repos/{self.config.repo}/tarball/{tag}", self._token(), limit=200 * 1024 * 1024)
        except urllib.error.HTTPError as e:
            raise Failed(f"GitHub refused the download ({e.code})")


# ---- the updater -------------------------------------------------------------------------


class Updater:
    def __init__(self, config, db, github, run=shell, open_url=urllib.request.urlopen, sleep=time.sleep, now=time.time):
        self.config, self.db, self.github = config, db, github
        self.run, self.open_url, self.sleep, self.now = run, open_url, sleep, now

    # -- what is running

    def running_version(self):
        try:
            with self.open_url(urllib.request.Request(self.config.health_url), timeout=5) as r:
                return str(json.loads(r.read(10_000)).get("version") or "")
        except (urllib.error.URLError, OSError, ValueError):
            return ""

    # -- one round of the loop

    def tick(self):
        running = self.running_version()
        self.db.heartbeat(running)
        state = self.db.state()
        latest_tag = state["latest_tag"]
        if state["check_requested"] or self.now() - state["checked_at"] > 3600:
            latest_tag = self.check(running)
        job = self.db.next_job()
        if job:
            self.install(job, running)
            return
        self.maybe_schedule(running, latest_tag)

    def check(self, running):
        if not self.config.repo:
            self.db.save_check("off")
            return ""
        try:
            release = self.github.latest()
        except Failed as e:
            self.db.save_check(str(e) if str(e) in ("app_key", "app_missing", "auth") else "error")
            return ""
        if release is None:  # without a GitHub App, a private repository looks like one with no releases
            self.db.save_check("none" if self.config.app_id else "private")
            return ""
        newer = version_tuple(release["tag"]) and version_tuple(running) and version_tuple(release["tag"]) > version_tuple(running)
        self.db.save_check("update" if newer else "current", release)
        return release["tag"]

    def maybe_schedule(self, running, latest_tag):
        enabled, hour = self.db.schedule()
        local = datetime.fromtimestamp(self.now(), self.config.timezone)
        if not enabled or local.hour != hour or not version_tuple(latest_tag) or not version_tuple(running):
            return
        if version_tuple(latest_tag) <= version_tuple(running):
            return
        midnight = local.replace(hour=0, minute=0, second=0, microsecond=0)
        if self.db.automatic_job_since(midnight.timestamp()):
            return  # one automatic attempt a day, even if it failed
        log(f"automatic update to {latest_tag} queued")
        self.db.queue_automatic(latest_tag, running)

    # -- installing a release

    def install(self, job, running):
        target, job_id = job["target"], job["id"]
        log(f"installing {target} (job {job_id}, running {running or 'unknown'})")
        self.db.job(job_id, status="running", from_version=running)
        try:
            release = self.github.latest()
        except Failed as e:
            return self._finish(job_id, "failed", f"Could not reach GitHub: {e}")
        if release is None or release["tag"] != target or not version_tuple(target):
            return self._finish(job_id, "failed", f"{target} is not the latest published release")
        if version_tuple(running) and version_tuple(target) <= version_tuple(running):
            return self._finish(job_id, "failed", f"{running} is already installed")

        by = job["by"]  # empty for automatic updates
        work = self.config.install_dir / "work" / target
        beat = _Heartbeat(self.db, self.sleep)
        self.db.maintenance("backup", 0, by)
        beat.start()
        try:
            try:
                backup = self._step(job_id, "backup", 0, by, lambda: self.backup(running, target))
                source = self._step(job_id, "download", 1, by, lambda: self.download(target, work))
                self._step(job_id, "build", 2, by, lambda: self.build(target, source))
            except Failed as e:
                return self._finish(job_id, "failed", f"Nothing was changed. {e}")
            previous = self.snapshot()
            try:
                self._step(job_id, "restart", 3, by, lambda: self.switch(target, source))
                self._step(job_id, "check", 4, by, lambda: self.wait_for(target.lstrip("v")))
            except Failed as e:
                log(f"{target} failed ({e}); rolling back")
                self.db.maintenance("rollback", 4, by)
                try:
                    self.rollback(previous, backup, running, by)
                except Failed as again:
                    return self._finish(job_id, "failed", f"{e} The rollback also failed: {again}. The backup is {backup.name}.")
                self.discard_image(target)
                return self._finish(job_id, "rolled_back", f"{e} The previous version and its data are back.")
            self._finish(job_id, "done", "")
            self.prune()
            if self._updater_changed(source):
                self.restart_updater()
        finally:
            beat.stop()
            shutil.rmtree(work, ignore_errors=True)

    def _step(self, job_id, phase, number, by, action):
        self.db.job(job_id, phase=phase)
        self.db.maintenance(phase, number, by)
        log(f"  {phase}")
        return action()

    def _finish(self, job_id, status, message):
        log(f"  {status}{': ' + message if message else ''}")
        self.db.job(job_id, status=status, message=message, finished=True)
        self.db.end_maintenance()

    def backup(self, running, target):
        folder = self.config.install_dir / "backups"
        folder.mkdir(parents=True, exist_ok=True)
        stamp = datetime.fromtimestamp(self.now(), self.config.timezone).strftime("%Y%m%d-%H%M%S")
        path = folder / f"before-{target}-from-v{running or 'unknown'}-{stamp}.sql.gz"
        dump = self.run([*self.config.compose, "exec", "-T", "db", "pg_dump", "-U", self.config.db_user, "-d", self.config.db_name,
                         "--clean", "--if-exists", "--no-owner"], timeout=3600)
        if not dump.strip():
            raise Failed("the database backup came out empty")
        path.write_bytes(gzip.compress(dump))
        return path

    def download(self, target, work):
        archive = self.github.source(target)
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        try:
            with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
                tar.extractall(work, filter="data")  # refuses paths outside the folder, links out of it, devices
        except (tarfile.TarError, OSError, ValueError) as e:
            raise Failed(f"the release's archive could not be unpacked: {e}")
        roots = [p for p in work.iterdir() if p.is_dir()]
        if len(roots) != 1 or not (roots[0] / "Dockerfile").exists():
            raise Failed("the release does not contain the app")
        return roots[0]

    def build(self, target, source):
        commit = source.name.rsplit("-", 1)[-1]  # GitHub names the folder owner-repo-<commit>
        self.run(["docker", "build", "--pull", "-t", f"inventario-web:{target.lstrip('v')}", "--build-arg", f"APP_COMMIT={commit}",
                  str(source)], timeout=3600)

    def snapshot(self):
        d = self.config.install_dir
        return {name: (d / name).read_bytes() for name in [*DEPLOY_FILES, ".env"] if (d / name).exists()}

    def switch(self, target, source):
        d = self.config.install_dir
        for name in DEPLOY_FILES:  # the release may bring changes to how the app is run
            if (source / "deploy" / name).exists():
                shutil.copyfile(source / "deploy" / name, d / name)
        set_env(d / ".env", "APP_VERSION", target.lstrip("v"))
        self.run([*self.config.compose, "up", "-d", "--no-deps", "web", "caddy"], timeout=600)
        self.run([*self.config.compose, "exec", "-T", "caddy", "caddy", "reload", "--config", "/etc/caddy/Caddyfile"], timeout=60)

    def wait_for(self, version):
        deadline = self.now() + self.config.health_timeout
        while self.now() < deadline:
            if self.running_version() == version:
                return
            self.sleep(3)
        raise Failed(f"the new version did not start within {self.config.health_timeout} seconds.")

    def rollback(self, previous, backup, running, by=""):
        d = self.config.install_dir
        self.run([*self.config.compose, "stop", "web"], timeout=300)
        for name, content in previous.items():
            (d / name).write_bytes(content)
        self.run([*self.config.compose, "exec", "-T", "db", "psql", "-X", "-q", "-v", "ON_ERROR_STOP=1",
                  "-U", self.config.db_user, "-d", self.config.db_name], input=gzip.decompress(backup.read_bytes()), timeout=3600)
        self.db.maintenance("rollback", 4, by)  # the restored database brought back the progress as it was at the backup
        self.run([*self.config.compose, "up", "-d", "--no-deps", "web", "caddy"], timeout=600)
        if running:
            self.wait_for(running)

    def discard_image(self, target):
        try:
            self.run(["docker", "image", "rm", f"inventario-web:{target.lstrip('v')}"])
        except Failed:
            pass

    def prune(self):
        """Keeps the last few pre-update backups and the current and previous app images."""
        backups = sorted((self.config.install_dir / "backups").glob("before-*.sql.gz"))
        for old in backups[:-self.config.keep_backups]:
            old.unlink(missing_ok=True)
        try:
            tags = self.run(["docker", "image", "ls", "inventario-web", "--format", "{{.Tag}}"]).decode().split()
        except Failed:
            return
        ordered = sorted((t for t in tags if version_tuple(t)), key=version_tuple)
        for tag in ordered[:-2]:
            try:
                self.run(["docker", "image", "rm", f"inventario-web:{tag}"])
            except Failed:
                pass

    def _updater_changed(self, source):
        def digest(folder):
            h = hashlib.sha256()
            for f in sorted(folder.glob("*")) if folder.exists() else []:
                if f.is_file():
                    h.update(f.name.encode() + f.read_bytes())
            return h.hexdigest()
        new, current = source / "deploy" / "updater", self.config.install_dir / "updater"
        if digest(new) == digest(current):
            return False
        shutil.rmtree(current, ignore_errors=True)
        shutil.copytree(new, current)
        return True

    def restart_updater(self):
        """Rebuilds this updater from the release and restarts it from a separate, short-lived container,
        because a container cannot finish replacing itself."""
        log("updating the updater itself")
        self.run([*self.config.compose, "build", "updater"], timeout=1800)
        d = str(self.config.install_dir)
        command = " ".join([*self.config.compose, "up", "-d", "--no-deps", "updater"])
        self.run(["docker", "run", "--rm", "-d", "-v", "/var/run/docker.sock:/var/run/docker.sock", "-v", f"{d}:{d}",
                  "--entrypoint", "sh", "inventario-updater", "-c", f"sleep 5 && {command}"])


class _Heartbeat:
    """Keeps maintenance mode fresh while a long step (such as building) runs; it lifts by itself after
    5 minutes without this, which is what makes a crashed updater harmless."""

    def __init__(self, db, sleep):
        self.db, self.sleep, self.running = db, sleep, False

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self.running:
            self.sleep(20)
            if self.running:
                try:
                    self.db.touch_maintenance()
                except Failed:
                    pass

    def stop(self):
        self.running = False


def set_env(path, key, value):
    """Changes one line of the .env file, keeping the rest exactly as it was."""
    lines = path.read_text().splitlines() if path.exists() else []
    found = False
    for i, line in enumerate(lines):
        if line.split("=", 1)[0].strip() == key:
            lines[i], found = f"{key}={value}", True
    if not found:
        lines.append(f"{key}={value}")
    path.write_text("\n".join(lines) + "\n")


def main():
    config = Config()
    db = Db([*config.compose, "exec", "-T", "db", "psql", "-U", config.db_user, "-d", config.db_name])
    updater = Updater(config, db, GitHub(config))
    log(f"updater started for {config.repo or '(no repository)'} in {config.install_dir}")
    while True:
        try:
            updater.tick()
        except Failed as e:
            log(f"problem: {e}")
        except Exception as e:  # keep running whatever happens; the next round tries again
            log(f"unexpected problem: {e!r}")
        time.sleep(config.poll_seconds)


if __name__ == "__main__":
    sys.exit(main())
