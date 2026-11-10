import base64
import json

from django.core.cache import cache
from django.test import Client, TestCase

from inventory import models as m
from inventory.models import AuditEvent, User

GOOD = "Correct-Horse-7"
NEW = "Brand-New-Pass-9"
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")


def send(client, method, url, body=None):
    return getattr(client, method)("/api/" + url, data=json.dumps(body if body is not None else {}), content_type="application/json")


class RequiredPasswordChangeTests(TestCase):
    def setUp(self):
        cache.clear()
        self.admin = User.objects.create_user("admin@x.es", GOOD, nombre="Admin", rol="admin")
        self.admin_client = Client()
        self.admin_client.force_login(self.admin)

    def create_user(self, must_change=True):
        body = {"nombre": "Nuevo", "email": "nuevo@x.es", "rol": "tech", "pass": GOOD, "mustChange": must_change}
        self.assertEqual(send(self.admin_client, "post", "users", body).status_code, 200)
        return User.objects.get(email="nuevo@x.es")

    def sign_in(self):
        client = Client()
        response = send(client, "post", "login", {"email": "nuevo@x.es", "password": GOOD})
        return client, response.json()

    def test_flag_is_stored_and_shown_to_admins(self):
        self.assertTrue(self.create_user().must_change_password)
        users = self.admin_client.get("/api/state").json()["state"]["users"]
        self.assertTrue(next(u for u in users if u["email"] == "nuevo@x.es")["mustChange"])

    def test_option_can_be_left_off(self):
        self.assertFalse(self.create_user(must_change=False).must_change_password)
        _, data = self.sign_in()
        self.assertIn("state", data)

    def test_sign_in_gives_no_data_until_changed(self):
        self.create_user()
        client, data = self.sign_in()
        self.assertTrue(data["me"]["mustChange"])
        self.assertNotIn("state", data)
        self.assertIn("pwPolicy", data["me"])
        self.assertEqual(client.get("/api/state").json()["error"], "err_must_change")
        self.assertNotIn("state", client.get("/api/bootstrap").json())
        self.assertEqual(send(client, "post", "devices").status_code, 403)

    def test_change_checks_current_password_rules_and_reuse(self):
        self.create_user()
        client, _ = self.sign_in()
        self.assertEqual(send(client, "post", "account/password", {"current": "wrong", "new": NEW}).json()["error"], "err_pw_current")
        self.assertEqual(send(client, "post", "account/password", {"current": GOOD, "new": GOOD}).json()["error"], "err_pw_same")
        self.assertEqual(send(client, "post", "account/password", {"current": GOOD, "new": "weak"}).json()["error"], "err_pass_weak")

    def test_successful_change_unlocks_the_app(self):
        user = self.create_user()
        client, _ = self.sign_in()
        response = send(client, "post", "account/password", {"current": GOOD, "new": NEW})
        self.assertEqual(response.status_code, 200, response.content)
        self.assertFalse(response.json()["me"]["mustChange"])
        self.assertEqual(client.get("/api/state").status_code, 200)  # still signed in
        user.refresh_from_db()
        self.assertFalse(user.must_change_password)
        self.assertTrue(user.check_password(NEW))
        self.assertEqual(AuditEvent.objects.first().key, "log_pwchanged")

    def test_can_sign_out_while_change_is_pending(self):
        self.create_user()
        client, _ = self.sign_in()
        self.assertEqual(send(client, "post", "logout").status_code, 200)

    def test_admin_cannot_force_it_on_themselves(self):
        body = {"nombre": "Admin", "email": "admin@x.es", "rol": "admin", "mustChange": True}
        send(self.admin_client, "put", f"users/{self.admin.pk}", body)
        self.admin.refresh_from_db()
        self.assertFalse(self.admin.must_change_password)

    def test_guessing_current_password_gets_locked(self):
        self.create_user()
        client, _ = self.sign_in()
        for _ in range(10):
            send(client, "post", "account/password", {"current": "wrong", "new": NEW})
        self.assertEqual(send(client, "post", "account/password", {"current": GOOD, "new": NEW}).status_code, 429)


class LogoTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin@x.es", GOOD, nombre="Admin", rol="admin")
        self.client.force_login(self.admin)

    def upload(self, data, kind="image/png", client=None):
        url = f"data:{kind};base64," + base64.b64encode(data).decode()
        return send(client or self.client, "put", "settings/logo", {"data": url})

    def test_upload_serve_and_remove(self):
        self.assertEqual(Client().get("/api/logo").status_code, 404)
        response = self.upload(PNG)
        self.assertEqual(response.status_code, 200, response.content)
        version = response.json()["logo"]
        self.assertEqual(Client().get("/api/bootstrap").json()["settings"]["logo"], version)
        served = Client().get(f"/api/logo?v={version}")
        self.assertEqual((served.status_code, served["Content-Type"], served.content), (200, "image/png", PNG))
        self.assertIn("sandbox", served["Content-Security-Policy"])
        self.assertIn("immutable", served["Cache-Control"])
        self.assertEqual(send(self.client, "delete", "settings/logo").json()["logo"], 0)
        self.assertEqual(Client().get("/api/logo").status_code, 404)

    def test_new_upload_changes_the_version(self):
        first = self.upload(PNG).json()["logo"]
        self.assertGreater(self.upload(PNG).json()["logo"], first)

    def test_file_must_match_its_type(self):
        self.assertEqual(self.upload(b"<html>not an image</html>").json()["error"], "err_logo_type")
        self.assertEqual(self.upload(PNG, kind="image/jpeg").json()["error"], "err_logo_type")
        self.assertEqual(send(self.client, "put", "settings/logo", {"data": "data:text/html;base64,PGI+"}).json()["error"], "err_logo_type")

    def test_svg_is_accepted_but_sandboxed(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><script>alert(1)</script></svg>'
        self.assertEqual(self.upload(svg, kind="image/svg+xml").status_code, 200)
        served = Client().get("/api/logo")
        self.assertEqual(served["Content-Type"], "image/svg+xml")
        self.assertIn("sandbox", served["Content-Security-Policy"])
        self.assertIn("default-src 'none'", served["Content-Security-Policy"])

    def test_size_limit(self):
        self.assertEqual(self.upload(PNG + b"\0" * (512 * 1024)).json()["error"], "err_logo_size")

    def test_only_admins_change_it(self):
        tech = Client()
        tech.force_login(User.objects.create_user("t@x.es", GOOD, nombre="T", rol="tech"))
        self.assertEqual(self.upload(PNG, client=tech).status_code, 403)

    def test_state_does_not_carry_the_image(self):
        self.upload(PNG)
        self.assertNotIn(base64.b64encode(PNG).decode()[:20], self.client.get("/api/state").content.decode())


class PageTests(TestCase):
    def test_interface_files_carry_a_version(self):
        html = self.client.get("/").content.decode()
        self.assertRegex(html, r"inventory/app\.js\?v=\d+")
        self.assertRegex(html, r"inventory/app\.css\?v=\d+")
