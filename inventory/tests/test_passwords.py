import json

from django.test import Client, TestCase, override_settings

from inventory import models as m
from inventory.models import User

GOOD = "Correct-Horse-7"


class PasswordPolicyTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin@x.es", GOOD, nombre="Admin", rol="admin")
        self.tech = User.objects.create_user("tech@x.es", GOOD, nombre="Tech", rol="tech")
        self.client.force_login(self.admin)

    def set_policy(self, **over):
        body = {"enforce": True, "minOn": True, "minLen": 10, "upper": True, "number": True, "symbol": True}
        body.update(over)
        return self.client.put("/api/settings/password-policy", data=json.dumps(body), content_type="application/json")

    def create(self, password, email="new@x.es"):
        body = {"nombre": "N", "email": email, "rol": "read", "pass": password}
        return self.client.post("/api/users", data=json.dumps(body), content_type="application/json")

    def assert_refused(self, password):
        self.assertEqual(self.create(password).json().get("error"), "err_pass_weak", password)

    def assert_accepted(self, password):
        response = self.create(password)
        self.assertEqual(response.status_code, 200, (password, response.content))
        User.objects.filter(email="new@x.es").delete()

    def test_defaults_require_everything(self):
        for bad in ("Short-7", "correct-horse-7", "Correct-Horse-x", "CorrectHorse77"):
            self.assert_refused(bad)
        self.assert_accepted(GOOD)

    def test_each_rule_can_be_turned_off_separately(self):
        self.set_policy(upper=False)
        self.assert_accepted("correct-horse-7")
        self.set_policy(number=False)
        self.assert_accepted("Correct-Horse-x")
        self.set_policy(symbol=False)
        self.assert_accepted("CorrectHorse77")
        self.set_policy(minOn=False)
        self.assert_accepted("Ab-7")

    def test_minimum_length_is_configurable(self):
        self.set_policy(minLen=20)
        self.assert_refused(GOOD)
        self.assert_accepted("Correct-Horse-Battery-7")

    def test_turning_enforcement_off_ignores_the_rules(self):
        self.set_policy(enforce=False)
        self.assert_accepted("abc")

    def test_an_empty_new_password_is_never_accepted(self):
        self.set_policy(enforce=False)
        self.assertEqual(self.create("").json()["error"], "err_pass")

    def test_accented_uppercase_and_symbols_count(self):
        self.set_policy(number=False, minLen=4)
        self.assert_accepted("Ñandú_x")

    def test_invalid_minimum_refused(self):
        for value in (0, 500, "x", 2.5):
            self.assertEqual(self.set_policy(minLen=value).status_code, 400, value)

    def test_policy_is_for_administrators_only(self):
        tech = Client()
        tech.force_login(self.tech)
        response = tech.put("/api/settings/password-policy", data="{}", content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertNotIn("pwPolicy", tech.get("/api/state").json()["state"]["settings"])
        self.assertIn("pwPolicy", self.client.get("/api/state").json()["state"]["settings"])
        self.assertNotIn("pwPolicy", Client().get("/api/bootstrap").json()["settings"])

    def test_existing_passwords_keep_working_when_rules_tighten(self):
        self.set_policy(minLen=40)
        response = Client().post("/api/login", data=json.dumps({"email": "tech@x.es", "password": GOOD}), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_changing_a_password_follows_the_policy(self):
        body = {"nombre": "Tech", "email": "tech@x.es", "rol": "tech", "pass": "weak"}
        url = f"/api/users/{self.tech.pk}"
        self.assertEqual(self.client.put(url, data=json.dumps(body), content_type="application/json").json()["error"], "err_pass_weak")
        body.pop("pass")
        self.assertEqual(self.client.put(url, data=json.dumps(body), content_type="application/json").status_code, 200)


@override_settings(DEBUG=True, SETUP_TOKEN="")
class SetupPolicyTests(TestCase):
    def payload(self, password, policy):
        return json.dumps({
            "orgName": "Acme", "dateFmt": "dmy", "currency": "EUR", "locations": [{"nombre": "Madrid", "tipo": "office"}],
            "pwPolicy": policy, "admin": {"nombre": "Ada", "email": "ada@x.es", "pass": password},
        })

    def test_wizard_applies_and_stores_chosen_rules(self):
        policy = {"enforce": True, "minOn": True, "minLen": 6, "upper": False, "number": True, "symbol": False}
        response = self.client.post("/api/setup", data=self.payload("abcde1", policy), content_type="application/json")
        self.assertEqual(response.status_code, 200, response.content)
        s = m.AppSettings.load()
        self.assertEqual((s.pw_min_length, s.pw_upper, s.pw_number), (6, False, True))

    def test_wizard_refuses_password_breaking_chosen_rules(self):
        policy = {"enforce": True, "minOn": True, "minLen": 12, "upper": False, "number": False, "symbol": False}
        response = self.client.post("/api/setup", data=self.payload("short", policy), content_type="application/json")
        self.assertEqual(response.json()["error"], "err_pass_weak")
        self.assertFalse(User.objects.exists())
