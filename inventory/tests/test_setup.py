import json

from django.core.cache import cache
from django.test import Client, TestCase, override_settings

from inventory import models as m
from inventory.models import AuditEvent, User

PASSWORD = "Correct-Horse-Battery-7"


def payload(**over):
    body = {
        "orgName": "Acme", "tagPrefix": "ACM-", "dateFmt": "ymd", "currency": "EUR", "warrantyDays": 90,
        "locations": [{"nombre": {"es": "Oficina", "en": "Office", "ca": "Oficina"}, "tipo": "office"},
                      {"nombre": "Almacén", "tipo": "storage"}],
        "depts": ["IT"],
        "admin": {"nombre": "Ada", "email": "Ada@Acme.es", "pass": PASSWORD},
    }
    body.update(over)
    return body


@override_settings(DEBUG=True, SETUP_TOKEN="")
class SetupTests(TestCase):
    def setUp(self):
        cache.clear()

    def post(self, body, client=None):
        return (client or self.client).post("/api/setup", data=json.dumps(body), content_type="application/json")

    def test_bootstrap_announces_setup_on_empty_install(self):
        self.assertEqual(self.client.get("/api/bootstrap").json()["setup"], {"tokenRequired": False, "blocked": False})

    def test_setup_creates_everything_and_signs_in(self):
        response = self.post(payload())
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.json()["me"]["rol"], "admin")
        admin = User.objects.get()
        self.assertEqual(admin.email, "ada@acme.es")
        self.assertEqual(m.AppSettings.load().org_name, "Acme")
        self.assertEqual(m.Location.objects.count(), 2)
        self.assertEqual(m.Location.objects.get(tipo="storage").nombre["en"], "Almacén")
        self.assertTrue(m.DeviceType.objects.exists())
        self.assertTrue(m.LinuxVersion.objects.exists())
        self.assertEqual(AuditEvent.objects.get().key, "log_setup")
        self.assertEqual(self.client.get("/api/state").status_code, 200)

    def test_setup_only_works_once(self):
        self.post(payload())
        again = self.post(payload(admin={"nombre": "Eve", "email": "eve@x.es", "pass": PASSWORD}), Client())
        self.assertEqual((again.status_code, again.json()["error"]), (409, "err_setup_done"))
        self.assertFalse(User.objects.filter(email="eve@x.es").exists())

    def test_bootstrap_stops_offering_setup_afterwards(self):
        self.post(payload())
        self.assertNotIn("setup", Client().get("/api/bootstrap").json())

    def test_failure_leaves_nothing_behind(self):
        response = self.post(payload(admin={"nombre": "Ada", "email": "ada@acme.es", "pass": "1234"}))
        self.assertEqual(response.json()["error"], "err_pass_weak")
        self.assertFalse(m.Location.objects.exists())
        self.assertFalse(m.DeviceType.objects.exists())
        self.assertEqual(m.AppSettings.load().org_name, "Empresa")

    def test_requires_a_location_and_org_name(self):
        self.assertEqual(self.post(payload(locations=[])).json()["error"], "err_su_loc")
        self.assertEqual(self.post(payload(orgName=" ")).json()["error"], "err_su_org")

    @override_settings(DEBUG=False, SETUP_TOKEN="s3cret-code")
    def test_production_needs_the_code(self):
        self.assertEqual(self.client.get("/api/bootstrap").json()["setup"], {"tokenRequired": True, "blocked": False})
        wrong = self.post(payload(token="nope"))
        self.assertEqual((wrong.status_code, wrong.json()["error"]), (403, "err_setup_token"))
        self.assertFalse(User.objects.exists())
        self.assertEqual(self.post(payload(token="s3cret-code")).status_code, 200)

    @override_settings(DEBUG=False, SETUP_TOKEN="")
    def test_production_without_a_configured_code_is_closed(self):
        self.assertTrue(self.client.get("/api/bootstrap").json()["setup"]["blocked"])
        self.assertEqual(self.post(payload(token="")).status_code, 403)
        self.assertFalse(User.objects.exists())

    @override_settings(DEBUG=False, SETUP_TOKEN="s3cret-code")
    def test_guessing_the_code_gets_locked_out(self):
        for _ in range(10):
            self.post(payload(token="nope"))
        locked = self.post(payload(token="s3cret-code"))
        self.assertEqual((locked.status_code, locked.json()["error"]), (429, "login_locked"))
