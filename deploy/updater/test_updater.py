"""Tests for the updater's decisions, with Docker, GitHub and the database replaced by fakes.

Run with:  python -m unittest discover -s deploy/updater
"""
import gzip
import io
import json
import tarfile
import tempfile
import unittest
import urllib.error
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import updater as u

MADRID = ZoneInfo("Europe/Madrid")


def archive(files, root="acme-inventario-abc1234"):
    """A release's source as GitHub sends it: a .tar.gz with one folder named owner-repo-<commit>."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for name, content in files.items():
            data = content.encode()
            info = tarfile.TarInfo(f"{root}/{name}" if not name.startswith("/") and not name.startswith("..") else name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


RELEASE_FILES = {"Dockerfile": "FROM python", "deploy/docker-compose.yml": "new compose", "deploy/Caddyfile": "new caddy",
                 "deploy/maintenance.html": "new page", "deploy/updater/updater.py": "same updater",
                 "inventory/version.py": '"""The version."""\nimport os\n\nVERSION = "1.1.0"\n'}


class FakeDb:
    def __init__(self):
        self.calls, self.jobs, self.maint = [], {}, []
        self.state_value = {"check_requested": False, "checked_at": 0.0, "latest_tag": ""}
        self.schedule_value, self.auto_today, self.saved = (False, 3), False, []

    def heartbeat(self, running): self.calls.append(("heartbeat", running))
    def state(self): return dict(self.state_value)
    def save_check(self, status, release=None): self.saved.append((status, (release or {}).get("tag")))
    def schedule(self): return self.schedule_value
    def next_job(self): return None
    def automatic_job_since(self, since): self.calls.append(("since", since)); return self.auto_today
    def queue_automatic(self, target, running): self.calls.append(("queue", target, running))
    def job(self, job_id, **changes): self.jobs.setdefault(job_id, []).append({k: v for k, v in changes.items() if v not in (None, False)})
    def maintenance(self, phase, step, by): self.maint.append((phase, step, by))
    def touch_maintenance(self): pass
    def end_maintenance(self): self.maint.append(("end",))

    def final(self, job_id):
        merged = {}
        for change in self.jobs[job_id]:
            merged.update(change)
        return merged


class FakeGitHub:
    def __init__(self, tag="v1.1.0", files=RELEASE_FILES, problem=None):
        self.tag, self.files, self.problem = tag, files, problem

    def latest(self):
        if self.problem:
            raise u.Failed(self.problem)
        return None if self.tag is None else {"tag": self.tag, "name": self.tag, "notes": "", "url": "", "published": ""}

    def source(self, tag):
        return archive(self.files)


class Server:
    """Docker and the app's health check, as the updater sees them."""

    def __init__(self, running="1.0.0", healthy_after_switch=True, fail_on=None):
        self.running, self.healthy_after_switch, self.fail_on, self.commands = running, healthy_after_switch, fail_on, []

    def run(self, args, input=None, timeout=None):
        self.commands.append((args, input))
        text = " ".join(args)
        if self.fail_on and self.fail_on in text:
            raise u.Failed(f"{self.fail_on} failed")
        if "pg_dump" in text:
            return b"-- database dump --"
        if " up -d " in f" {text} " and "web" in args:
            env = dict(line.split("=", 1) for line in self.env_file.read_text().splitlines() if "=" in line)
            self.running = env["APP_VERSION"] if self.healthy_after_switch or env["APP_VERSION"] == self.original else "starting"
        if "image ls" in text:
            return b"1.0.0\n0.9.0\n0.8.0\n1.1.0\n"
        return b""

    def open_url(self, request, timeout=None):
        return io.BytesIO(json.dumps({"status": "ok", "version": self.running}).encode())


class UpdaterTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        (self.dir / ".env").write_text("INSTALL_DIR=x\nAPP_VERSION=1.0.0\nSITE_HOST=inventario.local\n")
        for name in u.DEPLOY_FILES:
            (self.dir / name).write_text(f"old {name}")
        (self.dir / "updater").mkdir()
        (self.dir / "updater" / "updater.py").write_text("same updater")
        self.config = u.Config({"INSTALL_DIR": str(self.dir), "APP_UPDATE_REPO": "acme/inventario", "HEALTH_TIMEOUT": "30"})
        self.db, self.clock = FakeDb(), [datetime(2026, 11, 11, 10, 0, tzinfo=MADRID).timestamp()]
        self.server = Server()
        self.server.env_file, self.server.original = self.dir / ".env", "1.0.0"

    def make(self, github=None):
        def sleep(seconds):
            self.clock[0] += seconds
        return u.Updater(self.config, self.db, github or FakeGitHub(), run=self.server.run, open_url=self.server.open_url,
                         sleep=sleep, now=lambda: self.clock[0])

    def env(self):
        return dict(line.split("=", 1) for line in (self.dir / ".env").read_text().splitlines() if "=" in line)

    def commands(self):
        return [" ".join(args) for args, _ in self.server.commands]


class InstallTests(UpdaterTestCase):
    job = {"id": 7, "target": "v1.1.0", "by": "Ana", "automatic": False}

    def test_successful_update(self):
        self.make().install(self.job, "1.0.0")
        self.assertEqual(self.db.final(7)["status"], "done")
        self.assertEqual(self.db.saved, [("current", "v1.1.0")])  # straight away, not at the next hourly check
        self.assertEqual(self.env()["APP_VERSION"], "1.1.0")
        self.assertEqual(self.env()["SITE_HOST"], "inventario.local")  # the rest of .env is untouched
        self.assertEqual((self.dir / "docker-compose.yml").read_text(), "new compose")
        phases = [m[0] for m in self.db.maint]
        self.assertEqual(phases, ["backup", "backup", "download", "build", "restart", "check", "end"])
        backup = next((self.dir / "backups").glob("before-v1.1.0-from-v1.0.0-*.sql.gz"))
        self.assertEqual(gzip.decompress(backup.read_bytes()), b"-- database dump --")
        build = next(c for c in self.commands() if c.startswith("docker build"))
        self.assertIn("inventario-web:1.1.0", build)
        self.assertIn("APP_COMMIT=abc1234", build)
        self.assertLess(self.commands().index(next(c for c in self.commands() if "pg_dump" in c)), self.commands().index(build))
        removed = [c for c in self.commands() if c.startswith("docker image rm")]
        self.assertEqual(removed, ["docker image rm inventario-web:0.8.0", "docker image rm inventario-web:0.9.0"])  # keeps current and previous
        self.assertFalse((self.dir / "work" / "v1.1.0").exists())

    def test_failure_before_switching_changes_nothing(self):
        self.server.fail_on = "docker build"
        self.make().install(self.job, "1.0.0")
        final = self.db.final(7)
        self.assertEqual(final["status"], "failed")
        self.assertIn("Nothing was changed", final["message"])
        self.assertEqual(self.env()["APP_VERSION"], "1.0.0")
        self.assertEqual((self.dir / "docker-compose.yml").read_text(), "old docker-compose.yml")
        self.assertFalse(any(" up " in c for c in self.commands()))
        self.assertEqual(self.db.maint[-1], ("end",))

    def test_new_version_that_does_not_start_is_rolled_back(self):
        self.server.healthy_after_switch = False
        self.make().install(self.job, "1.0.0")
        final = self.db.final(7)
        self.assertEqual(final["status"], "rolled_back")
        self.assertIn("previous version and its data are back", final["message"])
        self.assertEqual(self.db.saved, [])  # still not installed, so it stays on offer
        self.assertEqual(self.env()["APP_VERSION"], "1.0.0")
        self.assertEqual((self.dir / "docker-compose.yml").read_text(), "old docker-compose.yml")
        commands = self.commands()
        stop = commands.index(next(c for c in commands if c.endswith("stop web")))
        restore = next(i for i, (args, data) in enumerate(self.server.commands) if "psql" in args and data == b"-- database dump --")
        self.assertLess(stop, restore)  # the app is stopped before its data is put back
        self.assertEqual(self.server.running, "1.0.0")
        self.assertEqual(self.db.maint[-2:], [("rollback", 4, "Ana"), ("end",)])  # set again after the database came back
        self.assertEqual(self.db.maint.count(("rollback", 4, "Ana")), 2)
        self.assertIn("docker image rm inventario-web:1.1.0", commands)  # the version that did not work is not kept

    def test_failed_rollback_is_reported_with_the_backup_name(self):
        self.server.healthy_after_switch = False
        original_run = self.server.run

        def run(args, input=None, timeout=None):
            if input == b"-- database dump --":
                raise u.Failed("restore failed")
            return original_run(args, input, timeout)
        self.server.run = run
        self.make().install(self.job, "1.0.0")
        final = self.db.final(7)
        self.assertEqual(final["status"], "failed")
        self.assertIn("rollback also failed", final["message"])
        self.assertIn("before-v1.1.0", final["message"])

    def test_only_the_latest_release_can_be_installed(self):
        self.make(FakeGitHub(tag="v1.2.0")).install(self.job, "1.0.0")
        self.assertEqual(self.db.final(7)["status"], "failed")
        self.assertIn("not the latest", self.db.final(7)["message"])
        self.assertEqual(self.server.commands, [])
        self.assertEqual(self.db.maint, [("end",)])

    def test_same_or_older_version_is_refused(self):
        self.make(FakeGitHub(tag="v1.0.0")).install(dict(self.job, target="v1.0.0"), "1.0.0")
        self.assertIn("already installed", self.db.final(7)["message"])
        self.assertEqual(self.server.commands, [])

    def test_github_unreachable(self):
        self.make(FakeGitHub(problem="error")).install(self.job, "1.0.0")
        self.assertEqual(self.db.final(7)["status"], "failed")
        self.assertEqual(self.server.commands, [])

    def test_archive_that_escapes_its_folder_is_refused(self):
        files = dict(RELEASE_FILES, **{"../../escape.txt": "x"})
        self.make(FakeGitHub(files=files)).install(self.job, "1.0.0")
        self.assertEqual(self.db.final(7)["status"], "failed")
        self.assertFalse((self.dir / "escape.txt").exists())
        self.assertFalse((self.dir.parent / "escape.txt").exists())
        self.assertEqual(self.env()["APP_VERSION"], "1.0.0")

    def test_tag_on_the_wrong_commit_is_refused_at_once(self):
        files = dict(RELEASE_FILES, **{"inventory/version.py": 'VERSION = "1.0.0"\n'})  # tagged v1.1.0 before the bump
        self.make(FakeGitHub(files=files)).install(self.job, "1.0.0")
        final = self.db.final(7)
        self.assertEqual(final["status"], "failed")
        self.assertIn("Nothing was changed", final["message"])
        self.assertIn("contains version 1.0.0", final["message"])
        self.assertFalse(any(c.startswith("docker build") for c in self.commands()), "not built, nothing switched")
        self.assertEqual(self.env()["APP_VERSION"], "1.0.0")
        without = {k: v for k, v in RELEASE_FILES.items() if k != "inventory/version.py"}
        self.make(FakeGitHub(files=without)).install(self.job, "1.0.0")
        self.assertIn("contains version unknown", self.db.final(7)["message"])

    def test_archive_without_the_app_is_refused(self):
        self.make(FakeGitHub(files={"README.md": "hello"})).install(self.job, "1.0.0")
        self.assertIn("does not contain the app", self.db.final(7)["message"])

    def test_changed_updater_restarts_itself_from_outside(self):
        files = dict(RELEASE_FILES, **{"deploy/updater/updater.py": "new updater"})
        self.make(FakeGitHub(files=files)).install(self.job, "1.0.0")
        self.assertEqual((self.dir / "updater" / "updater.py").read_text(), "new updater")
        self.assertTrue(any(c.startswith("docker run --rm -d") and "up -d --no-deps updater" in c for c in self.commands()))


class ScheduleTests(UpdaterTestCase):
    def schedule(self, hour=10, enabled=True, latest="v1.1.0", running="1.0.0", already=False):
        self.db.schedule_value, self.db.auto_today = (enabled, hour), already
        self.make().maybe_schedule(running, latest)
        return [c for c in self.db.calls if c[0] == "queue"]

    def test_queues_at_the_chosen_hour(self):
        self.assertEqual(self.schedule(), [("queue", "v1.1.0", "1.0.0")])

    def test_counts_the_day_from_local_midnight(self):
        self.schedule()
        since = next(c[1] for c in self.db.calls if c[0] == "since")
        self.assertEqual(datetime.fromtimestamp(since, MADRID).strftime("%Y-%m-%d %H:%M"), "2026-11-11 00:00")

    def test_does_nothing_otherwise(self):
        self.assertEqual(self.schedule(hour=3), [])
        self.assertEqual(self.schedule(enabled=False), [])
        self.assertEqual(self.schedule(latest="v1.0.0"), [])
        self.assertEqual(self.schedule(already=True), [])
        self.assertEqual(self.schedule(latest=""), [])


class CheckTests(UpdaterTestCase):
    def test_statuses(self):
        self.make(FakeGitHub(tag="v1.1.0")).check("1.0.0")
        self.make(FakeGitHub(tag="v1.0.0")).check("1.0.0")
        self.make(FakeGitHub(tag=None)).check("1.0.0")
        self.make(FakeGitHub(problem="app_missing")).check("1.0.0")
        self.make(FakeGitHub(problem="error")).check("1.0.0")
        self.assertEqual(self.db.saved, [("update", "v1.1.0"), ("current", "v1.0.0"), ("private", None), ("app_missing", None), ("error", None)])

    def test_tick_checks_when_asked_and_reports_running_version(self):
        self.db.state_value["check_requested"] = True
        self.clock[0] = 10_000_000_000  # long after the last check anyway
        self.make().tick()
        self.assertEqual(self.db.calls[0], ("heartbeat", "1.0.0"))
        self.assertEqual(self.db.saved, [("update", "v1.1.0")])


class GitHubAppTests(unittest.TestCase):
    def test_signs_in_and_asks_only_to_read_this_repository(self):
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        folder = Path(tempfile.mkdtemp())
        (folder / "app.pem").write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
        config = u.Config({"APP_UPDATE_REPO": "acme/inventario", "APP_UPDATE_GITHUB_APP_ID": "99", "APP_UPDATE_GITHUB_APP_PRIVATE_KEY_FILE": str(folder / "app.pem")})
        calls = []

        def open_url(request, timeout=None):
            calls.append((request.full_url, request.headers.get("Authorization"), request.data))
            if request.full_url.endswith("/installation"):
                return io.BytesIO(b'{"id": 5}')
            if request.full_url.endswith("/access_tokens"):
                return io.BytesIO(b'{"token": "ghs_x"}')
            if request.full_url.endswith("/releases/latest"):
                return io.BytesIO(b'{"tag_name": "v2.0.0", "html_url": "https://github.com/acme/inventario/releases/v2.0.0"}')
            raise urllib.error.HTTPError(request.full_url, 404, "x", {}, io.BytesIO(b""))
        github = u.GitHub(config, open_url=open_url)
        self.assertEqual(github.latest()["tag"], "v2.0.0")
        self.assertEqual(json.loads(calls[1][2]), {"repositories": ["inventario"], "permissions": {"contents": "read"}})
        self.assertEqual(calls[2][1], "Bearer ghs_x")
        github.latest()
        self.assertEqual(len(calls), 4)  # the installation token is reused

    def test_missing_key(self):
        config = u.Config({"APP_UPDATE_REPO": "acme/inventario", "APP_UPDATE_GITHUB_APP_ID": "99", "APP_UPDATE_GITHUB_APP_PRIVATE_KEY_FILE": "/nonexistent.pem"})
        with self.assertRaisesRegex(u.Failed, "app_key"):
            u.GitHub(config).latest()


class EnvFileTests(unittest.TestCase):
    def test_changes_one_line_only(self):
        path = Path(tempfile.mkdtemp()) / ".env"
        path.write_text("# comment\nA=1\nAPP_VERSION=1.0.0\nB=two=2\n")
        u.set_env(path, "APP_VERSION", "1.1.0")
        self.assertEqual(path.read_text(), "# comment\nA=1\nAPP_VERSION=1.1.0\nB=two=2\n")
        u.set_env(path, "NEW", "x")
        self.assertTrue(path.read_text().endswith("NEW=x\n"))


if __name__ == "__main__":
    unittest.main()
