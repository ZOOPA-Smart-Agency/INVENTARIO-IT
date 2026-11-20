"""Checks GitHub for a newer release. Only reads; installing a release is done by deploying it.

GitHub access, for a private repository, is either a read-only token (APP_UPDATE_TOKEN) or a GitHub App
(APP_UPDATE_GITHUB_APP_ID + its private key). With an app, the server signs a short JWT with the key, asks
GitHub for an installation token limited to reading this repository's contents, and uses that for about an hour.
"""
import base64
import json
import re
import time
import urllib.error
import urllib.request

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from .version import VERSION

CACHE_KEY = "update-check"
CACHE_SECONDS = 3600
APP_TOKEN_KEY = "update-app-token"
API = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "inventario-update-check"}


class AccessProblem(Exception):
    """`status` is shown on the Updates page."""

    def __init__(self, status):
        super().__init__(status)
        self.status = status


def _b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def app_jwt(app_id, key_pem, now=None):
    """The short-lived token that proves to GitHub the request comes from the app (RS256, at most 10 minutes)."""
    try:
        key = serialization.load_pem_private_key(key_pem.encode(), password=None)
    except (ValueError, TypeError):
        raise AccessProblem("app_key")
    now = int(now or time.time())
    header = _b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    claims = _b64(json.dumps({"iat": now - 60, "exp": now + 540, "iss": str(app_id)}).encode())
    signature = key.sign(f"{header}.{claims}".encode(), padding.PKCS1v15(), hashes.SHA256())
    return f"{header}.{claims}.{_b64(signature)}"


def _call(url, token, body=None):
    request = urllib.request.Request(url, headers={**HEADERS, "Authorization": f"Bearer {token}"},
                                     data=None if body is None else json.dumps(body).encode(), method="GET" if body is None else "POST")
    with urllib.request.urlopen(request, timeout=8) as response:
        return json.loads(response.read(1_000_000))


def app_token(repo):
    """An installation token that can only read this repository's contents; kept until shortly before it expires."""
    cached_token = cache.get(APP_TOKEN_KEY)
    if cached_token:
        return cached_token
    jwt = app_jwt(settings.UPDATE_APP_ID, settings.UPDATE_APP_KEY)
    try:
        installation = _call(f"{API}/repos/{repo}/installation", jwt)
        granted = _call(f"{API}/app/installations/{int(installation['id'])}/access_tokens", jwt,
                        {"repositories": [repo.split("/", 1)[1]], "permissions": {"contents": "read"}})
    except urllib.error.HTTPError as e:
        raise AccessProblem("app_missing" if e.code == 404 else "auth")
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError, TypeError):
        raise AccessProblem("error")
    token = str(granted.get("token") or "")
    if not token:
        raise AccessProblem("auth")
    cache.set(APP_TOKEN_KEY, token, 50 * 60)  # GitHub gives an hour
    return token


def access():
    """How this server signs in to GitHub: 'app', 'token' or None."""
    if settings.UPDATE_APP_ID or settings.UPDATE_APP_KEY:
        return "app"
    return "token" if settings.UPDATE_TOKEN else None
REPO_PATTERN = re.compile(r"^[\w.-]+/[\w.-]+$")


def parse(version):
    """'v1.10.2' -> (1, 10, 2); anything else sorts lowest."""
    numbers = re.findall(r"\d+", str(version or "").split("-")[0])
    return tuple(int(n) for n in numbers[:3]) or (0,)


def as_installed(result):
    """A check made before an update may still call the now-installed version "new"; it is not."""
    if result and result.get("status") == "update" and parse(result.get("latest")) <= parse(VERSION):
        return {**result, "status": "current"}
    return result


def cached():
    return as_installed(cache.get(CACHE_KEY))


def check():
    repo = settings.UPDATE_REPO
    if not repo or not REPO_PATTERN.match(repo):
        return {"status": "off"}
    headers = dict(HEADERS)
    token = settings.UPDATE_TOKEN
    if access() == "app":
        try:
            if not (settings.UPDATE_APP_ID and settings.UPDATE_APP_KEY):
                raise AccessProblem("app_key")
            token = app_token(repo)
        except AccessProblem as problem:
            result = {"status": problem.status, "checked": timezone.now().isoformat()}
            cache.set(CACHE_KEY, result, CACHE_SECONDS)
            return result
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"{API}/repos/{repo}/releases/latest", headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            data = json.loads(response.read(2_000_000))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # GitHub answers 404 both for "no releases yet" and for a private repo without access
            result = {"status": "none" if token else "private"}
        elif e.code in (401, 403):
            cache.delete(APP_TOKEN_KEY)  # an app token may have been withdrawn: ask for a new one next time
            result = {"status": "auth"}
        else:
            result = {"status": "error"}
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        result = {"status": "error"}
    else:
        latest = str(data.get("tag_name") or "")
        url = str(data.get("html_url") or "")
        result = {
            "status": "update" if parse(latest) > parse(VERSION) else "current",
            "latest": latest,
            "name": str(data.get("name") or latest)[:200],
            "published": data.get("published_at"),
            "notes": str(data.get("body") or "")[:5000],
            "url": url if url.startswith("https://github.com/") else "",
        }
    result["checked"] = timezone.now().isoformat()
    cache.set(CACHE_KEY, result, CACHE_SECONDS)
    return result


# ---- results in the activity log ---------------------------------------------------------------

RESULTS_LOCK = 7_310_412  # any number of this app's own
RESULT_KEYS = {"done": "log_update_done", "failed": "log_update_failed", "rolled_back": "log_update_rolled_back"}


def record_results():
    """Adds each finished installation's result to the activity log, once. The updater service, which installs them,
    only writes the job (and may itself be an older version); the web app notes how it ended, at the time it did."""
    from django.db import connection, transaction

    from .models import AuditEvent, UpdateJob, User

    finished = list(UpdateJob.objects.filter(status__in=RESULT_KEYS, finished_at__isnull=False))
    if not finished:
        return
    with transaction.atomic():
        # one request at a time, or two at once could both add the same results (held until the transaction ends)
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_xact_lock(%s)", [RESULTS_LOCK])
        logged = set(AuditEvent.objects.filter(key__in=RESULT_KEYS.values()).values_list("args__job", flat=True))
        for job in finished:
            if job.id in logged:
                continue
            args = {"job": job.id, "v": job.target, "from": job.from_version, "auto": job.automatic}
            if job.status != "done":
                args["msg"] = job.message[:300]
            by = User.objects.filter(nombre=job.requested_by).first() if job.requested_by else None
            AuditEvent.objects.create(key=RESULT_KEYS[job.status], args=args, user=by, at=job.finished_at)
