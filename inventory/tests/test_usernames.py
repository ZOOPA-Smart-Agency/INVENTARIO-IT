import json
from importlib import import_module

from django.apps import apps
from django.core.cache import cache
from django.test import Client, TestCase

from inventory.models import User, clean_username, suggest_username

GOOD = "Correct-Horse-7"


class UsernameTests(TestCase):
    def setUp(self):
        cache.clear()
        self.admin = User.objects.create_user("ana.lopez@x.es", GOOD, nombre="Ana", rol="admin")
        self.tech = User.objects.create_user("teo@x.es", GOOD, nombre="Teo", rol="tech", username="Teo.IT")

    def login(self, who, password=GOOD, url="/api/login"):
        return Client().post(url, data=json.dumps({"email": who, "password": password}), content_type="application/json")

    def test_new_accounts_get_one(self):
        self.assertEqual((self.admin.username, self.tech.username), ("ana.lopez", "teo.it"))
        self.assertEqual(User.objects.create_user("ana.lopez@y.es", GOOD, nombre="Otra").username, "ana.lopez2")
        self.assertEqual(suggest_username("a+b@x.es"), "ab")
        self.assertEqual((clean_username(" Ana_1 "), clean_username("ana lopez"), clean_username("a@b"), clean_username("a")), ("ana_1", "", "", ""))

    def test_sign_in_with_email_or_username(self):
        for who in ("ana.lopez@x.es", "ANA.LOPEZ@x.es", "ana.lopez", " Ana.Lopez "):
            response = self.login(who)
            self.assertEqual(response.status_code, 200, who)
            self.assertEqual(response.json()["me"]["username"], "ana.lopez")
        self.assertEqual(self.login("ana.lopez", "wrong").json()["error"], "login_err")
        self.assertEqual(self.login("nobody").json()["error"], "login_err")

    def test_device_app_signs_in_with_a_username(self):
        response = self.login("teo.it", url="/api/agent/login")
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.json()["user"]["nombre"], "Teo")

    def test_deactivated_and_lockout_apply_to_usernames(self):
        User.objects.filter(pk=self.tech.pk).update(is_active=False)
        self.assertEqual(self.login("teo.it").json()["error"], "login_off")
        for _ in range(10):
            self.login("ana.lopez", "wrong")
        self.assertEqual(self.login("ana.lopez@x.es").status_code, 429)  # the same limit, whichever name is typed

    def test_administrators_set_change_and_clear_it(self):
        client = Client()
        client.force_login(self.admin)

        def save(method, url, **extra):
            body = {"nombre": "Teo", "email": "teo@x.es", "rol": "tech", **extra}
            return getattr(client, method)(url, data=json.dumps(body), content_type="application/json")

        url = f"/api/users/{self.tech.pk}"
        self.assertEqual(save("put", url, username="Soporte").status_code, 200)
        self.tech.refresh_from_db()
        self.assertEqual(self.tech.username, "soporte")
        self.assertEqual(save("put", url, username="ana.lopez").json()["error"], "err_username_dup")
        self.assertEqual(save("put", url, username="has space").json()["error"], "err_username")
        self.assertEqual(save("put", url, username="").status_code, 200)
        self.tech.refresh_from_db()
        self.assertIsNone(self.tech.username)  # cleared: email only
        self.assertEqual(self.login("teo@x.es").status_code, 200)
        body = {"pass": GOOD, "email": "nuevo.tecnico@x.es", "nombre": "Nuevo"}
        self.assertEqual(save("post", "/api/users", **body).status_code, 200)
        self.assertEqual(User.objects.get(email="nuevo.tecnico@x.es").username, "nuevo.tecnico")  # made from the email
        users = client.get("/api/state").json()
        self.assertIn("nuevo.tecnico", json.dumps(users))

    def test_update_gives_existing_accounts_one(self):
        User.objects.update(username=None)
        User.objects.create_user("ana.lopez@y.es", GOOD, nombre="Otra")
        User.objects.update(username=None)
        import_module("inventory.migrations.0012_user_username").fill_usernames(apps, None)
        self.assertEqual(sorted(User.objects.values_list("username", flat=True)), ["ana.lopez", "ana.lopez2", "teo"])
