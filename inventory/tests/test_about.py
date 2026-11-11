import io
import json
import urllib.error
from unittest import mock

from django.core.cache import cache
from django.test import Client, TestCase, override_settings

from inventory import updates
from inventory.models import User
from inventory.version import VERSION

GOOD = "Correct-Horse-7"


def github(status=200, body=None):
    """Simulates GitHub's answer to the latest-release request."""
    def fake(request, timeout):
        fake.request = request
        if status != 200:
            raise urllib.error.HTTPError(request.full_url, status, "error", {}, io.BytesIO(b"{}"))
        return io.BytesIO(json.dumps(body).encode())
    return mock.patch("urllib.request.urlopen", side_effect=fake), fake


@override_settings(UPDATE_REPO="acme/inventario", UPDATE_TOKEN="")
class AboutTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client.force_login(User.objects.create_user("admin@x.es", GOOD, nombre="Admin", rol="admin"))

    def check(self):
        return self.client.post("/api/about/updates", data="{}", content_type="application/json").json()

    def test_about_shows_version_and_environment(self):
        data = self.client.get("/api/about").json()
        self.assertEqual(data["version"], VERSION)
        self.assertIn(data["environment"], ("production", "development"))
        self.assertTrue(data["tech"]["postgres"][0].isdigit())
        self.assertGreater(data["dbSize"], 0)
        self.assertEqual(data["counts"]["users"], 1)
        self.assertEqual(data["updates"]["repo"], "acme/inventario")

    def test_only_admins(self):
        tech = Client()
        tech.force_login(User.objects.create_user("t@x.es", GOOD, nombre="T", rol="tech"))
        self.assertEqual(tech.get("/api/about").status_code, 403)
        self.assertEqual(tech.post("/api/about/updates", data="{}", content_type="application/json").status_code, 403)

    def test_newer_release_is_reported(self):
        patch, _ = github(body={"tag_name": "v99.0.0", "name": "Big release", "body": "Notes", "published_at": "2026-12-01T10:00:00Z",
                                "html_url": "https://github.com/acme/inventario/releases/tag/v99.0.0"})
        with patch:
            result = self.check()
        self.assertEqual((result["status"], result["latest"], result["notes"]), ("update", "v99.0.0", "Notes"))
        self.assertTrue(result["url"].startswith("https://github.com/"))
        self.assertEqual(self.client.get("/api/about").json()["updates"]["last"]["status"], "update")  # remembered

    def test_same_or_older_release_is_current(self):
        for tag in (f"v{VERSION}", "v0.9.9"):
            patch, _ = github(body={"tag_name": tag, "html_url": "https://github.com/acme/inventario"})
            with patch:
                self.assertEqual(self.check()["status"], "current", tag)

    def test_links_outside_github_are_dropped(self):
        patch, _ = github(body={"tag_name": "v99.0.0", "html_url": "https://evil.example/x"})
        with patch:
            self.assertEqual(self.check()["url"], "")

    def test_private_repo_without_token(self):
        patch, fake = github(status=404)
        with patch:
            self.assertEqual(self.check()["status"], "private")
        self.assertNotIn("Authorization", fake.request.headers)

    @override_settings(UPDATE_TOKEN="ghp_secret")
    def test_token_is_sent_and_never_shown(self):
        patch, fake = github(status=404)
        with patch:
            self.assertEqual(self.check()["status"], "none")
        self.assertEqual(fake.request.headers["Authorization"], "Bearer ghp_secret")
        self.assertNotIn("ghp_secret", self.client.get("/api/about").content.decode())

    def test_bad_token_and_network_errors(self):
        patch, _ = github(status=401)
        with patch:
            self.assertEqual(self.check()["status"], "auth")
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("offline")):
            self.assertEqual(self.check()["status"], "error")

    @override_settings(UPDATE_REPO="")
    def test_check_can_be_turned_off(self):
        with mock.patch("urllib.request.urlopen") as never:
            self.assertEqual(self.check()["status"], "off")
        never.assert_not_called()

    def test_version_comparison(self):
        self.assertGreater(updates.parse("v1.10.0"), updates.parse("1.9.9"))
        self.assertEqual(updates.parse("v1.2.3-beta"), (1, 2, 3))
        self.assertEqual(updates.parse("garbage"), (0,))


from cryptography.hazmat.primitives import hashes, serialization  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import padding, rsa  # noqa: E402

KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
PEM = KEY.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()).decode()


def b64decode(part):
    import base64
    return base64.urlsafe_b64decode(part + "=" * (-len(part) % 4))


class FakeGitHub:
    """Answers the three calls a GitHub App makes: find the installation, get a token, read the release."""

    def __init__(self, installation_status=200, release=None):
        self.calls, self.installation_status = [], installation_status
        self.release = release or {"tag_name": "v99.0.0", "html_url": "https://github.com/acme/inventario/releases/tag/v99.0.0"}

    def __call__(self, request, timeout):
        url, auth = request.full_url, request.headers.get("Authorization", "")
        body = json.loads(request.data) if request.data else None
        self.calls.append((request.get_method(), url, auth, body))
        if url.endswith("/repos/acme/inventario/installation"):
            if self.installation_status != 200:
                raise urllib.error.HTTPError(url, self.installation_status, "x", {}, io.BytesIO(b"{}"))
            return io.BytesIO(b'{"id": 4242}')
        if url.endswith("/app/installations/4242/access_tokens"):
            return io.BytesIO(b'{"token": "ghs_installation", "expires_at": "2026-11-11T13:00:00Z"}')
        if url.endswith("/repos/acme/inventario/releases/latest"):
            assert auth == "Bearer ghs_installation"
            return io.BytesIO(json.dumps(self.release).encode())
        raise AssertionError(url)


@override_settings(UPDATE_REPO="acme/inventario", UPDATE_TOKEN="", UPDATE_APP_ID="123456", UPDATE_APP_KEY=PEM)
class GitHubAppTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client.force_login(User.objects.create_user("admin@x.es", GOOD, nombre="Admin", rol="admin"))

    def check(self):
        return self.client.post("/api/about/updates", data="{}", content_type="application/json").json()

    def test_full_app_sign_in(self):
        fake = FakeGitHub()
        with mock.patch("urllib.request.urlopen", side_effect=fake):
            self.assertEqual(self.check()["status"], "update")
        (m1, _, auth1, _), (m2, _, auth2, body2), (m3, _, auth3, _) = fake.calls
        self.assertEqual((m1, m2, m3), ("GET", "POST", "GET"))
        # the app proves itself with a JWT signed by its private key
        jwt = auth1.split(" ", 1)[1]
        header, claims, signature = jwt.split(".")
        KEY.public_key().verify(b64decode(signature), f"{header}.{claims}".encode(), padding.PKCS1v15(), hashes.SHA256())
        claims = json.loads(b64decode(claims))
        self.assertEqual(claims["iss"], "123456")
        self.assertLessEqual(claims["exp"] - claims["iat"], 600)
        self.assertEqual(auth2, auth1)
        # the installation token it asks for can only read this one repository
        self.assertEqual(body2, {"repositories": ["inventario"], "permissions": {"contents": "read"}})
        self.assertEqual(auth3, "Bearer ghs_installation")

    def test_installation_token_is_reused(self):
        fake = FakeGitHub()
        with mock.patch("urllib.request.urlopen", side_effect=fake):
            self.check()
            self.check()
        self.assertEqual([url.rsplit("/", 1)[-1] for _, url, _, _ in fake.calls], ["installation", "access_tokens", "latest", "latest"])

    def test_app_not_installed_on_the_repo(self):
        with mock.patch("urllib.request.urlopen", side_effect=FakeGitHub(installation_status=404)):
            self.assertEqual(self.check()["status"], "app_missing")

    @override_settings(UPDATE_APP_KEY="not a key")
    def test_bad_private_key(self):
        with mock.patch("urllib.request.urlopen") as never:
            self.assertEqual(self.check()["status"], "app_key")
        never.assert_not_called()

    @override_settings(UPDATE_APP_KEY="")
    def test_missing_private_key(self):
        self.assertEqual(self.check()["status"], "app_key")

    def test_key_never_leaves_the_server(self):
        about = self.client.get("/api/about").content.decode()
        self.assertEqual(json.loads(about)["updates"]["access"], "app")
        self.assertNotIn("PRIVATE KEY", about)
