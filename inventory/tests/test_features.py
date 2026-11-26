import json
from datetime import timedelta

from django.core.cache import cache
from django.core.management import call_command
from django.test import Client, TestCase
from django.utils import timezone

from inventory import models as m
from inventory.models import Assignment, AuditEvent, Device, Employee, User

PASSWORD = "Correct-Horse-Battery-7"


class Base(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("load_demo_data", password=PASSWORD, verbosity=0, stdout=open("/dev/null", "w"))
        cls.admin = User.objects.get(email="admin@empresa.es")
        cls.tech = User.objects.get(email="it@empresa.es")
        cls.reader = User.objects.get(email="lectura@empresa.es")

    def setUp(self):
        cache.clear()

    def client_for(self, user):
        c = Client()
        c.force_login(user)
        return c

    def send(self, client, method, url, body=None):
        return getattr(client, method)("/api/" + url, data=json.dumps(body or {}), content_type="application/json")


class DeviceHistoryTests(Base):
    def test_history(self):
        device = Device.objects.first()
        AuditEvent.objects.bulk_create([AuditEvent(key="log_edited", args={"tag": device.tag, "parts": ["ram"]}, device=device) for _ in range(130)])
        AuditEvent.objects.create(key="log_edited", args={"tag": "OTHER"}, device=Device.objects.last())
        reader = self.client_for(self.reader)  # everyone who can see the device
        first = reader.get(f"/api/devices/{device.pk}/history").json()
        self.assertEqual((len(first["events"]), first["more"]), (100, True))
        rest = reader.get(f"/api/devices/{device.pk}/history", {"before": first["events"][-1]["id"]}).json()
        total = AuditEvent.objects.filter(device=device).count()
        self.assertEqual(len(first["events"]) + len(rest["events"]), total)
        self.assertNotIn("OTHER", json.dumps(first) + json.dumps(rest))
        self.assertEqual(reader.get("/api/devices/999999/history").status_code, 404)
        self.assertEqual(Client().get(f"/api/devices/{device.pk}/history").status_code, 401)


class ShareLinkTests(Base):
    def make(self, client, device, days=7, note="Taller Pérez"):
        return self.send(client, "post", f"devices/{device.pk}/share", {"days": days, "note": note})

    def test_link_shows_the_device_but_not_people_or_prices(self):
        assignment = Assignment.objects.filter(hasta__isnull=True, employee__isnull=False).first()
        device = assignment.device
        Device.objects.filter(pk=device.pk).update(precio=1234.56, proveedor="Proveedor Secreto SL")
        response = self.make(self.client_for(self.tech), device).json()
        url = response["url"]
        self.assertTrue(url.startswith("http://testserver/s/"))
        page = Client(HTTP_ACCEPT_LANGUAGE="en").get(url[len("http://testserver"):])
        html = page.content.decode()
        self.assertEqual(page.status_code, 200)
        self.assertIn(device.tag, html)
        self.assertIn(device.serial, html)
        self.assertIn("Faults and repairs", html)
        for secret in (assignment.employee.nombre, "1234", "Proveedor Secreto"):
            self.assertNotIn(secret, html)
        self.assertEqual(page["Cache-Control"], "no-store")
        self.assertIn("noindex", page["X-Robots-Tag"])
        link = m.ShareLink.objects.get()
        self.assertEqual((link.views, link.note), (1, "Taller Pérez"))
        self.assertNotIn(url.rsplit("/", 1)[1], link.token_hash, "only a hash of the token is kept")
        self.assertEqual(AuditEvent.objects.filter(key="log_share_created", device=device).count(), 1)
        # revoked: gone at once
        self.assertFalse(self.send(self.client_for(self.tech), "delete", f"share/{link.pk}").json()["link"]["active"])
        self.assertEqual(Client().get(url[len("http://testserver"):]).status_code, 404)

    def test_expiry_and_rules(self):
        device = Device.objects.first()
        url = self.make(self.client_for(self.admin), device, days=1).json()["url"][len("http://testserver"):]
        m.ShareLink.objects.update(expires_at=timezone.now() - timedelta(minutes=1))
        self.assertEqual(Client().get(url).status_code, 404)
        self.assertEqual(Client().get("/s/made-up-token").status_code, 404)
        self.assertEqual(self.make(self.client_for(self.reader), device).status_code, 403)
        self.assertEqual(self.make(self.client_for(self.tech), device, days=365).status_code, 400)
        links = self.client_for(self.tech).get(f"/api/devices/{device.pk}/share").json()["links"]
        self.assertEqual((len(links), links[0]["active"]), (1, False))
        self.assertNotIn("url", links[0], "the address is only shown when made")


class SessionTests(Base):
    def sign_in(self, agent):
        c = Client(HTTP_USER_AGENT=agent, REMOTE_ADDR="10.0.0.9")
        self.assertEqual(self.send(c, "post", "login", {"email": "it@empresa.es", "password": PASSWORD}).status_code, 200)
        return c

    def test_list_and_sign_out_others(self):
        laptop, phone = self.sign_in("Mozilla/5.0 (Macintosh) Safari"), self.sign_in("Mozilla/5.0 (iPhone) Safari")
        sessions = laptop.get("/api/account/sessions").json()["sessions"]
        self.assertEqual(len(sessions), 2)
        self.assertEqual(sum(s["current"] for s in sessions), 1)
        self.assertEqual({s["ip"] for s in sessions}, {"10.0.0.9"})
        other = next(s for s in sessions if not s["current"])
        mine = next(s for s in sessions if s["current"])
        self.assertEqual(self.send(laptop, "delete", f"account/sessions/{mine['id']}").status_code, 409)
        self.assertEqual(self.send(laptop, "delete", f"account/sessions/{other['id']}").json(), {"ok": True})
        self.assertEqual(phone.get("/api/state").status_code, 401, "the other browser is signed out")
        self.assertEqual(laptop.get("/api/state").status_code, 200)
        # someone else's session cannot be touched
        admin = self.client_for(self.admin)
        self.assertEqual(self.send(admin, "delete", f"account/sessions/{mine['id']}").status_code, 404)

    def test_sign_out_everywhere_else(self):
        a, b, c = self.sign_in("A"), self.sign_in("B"), self.sign_in("C")
        left = self.send(a, "delete", "account/sessions").json()["sessions"]
        self.assertEqual(len(left), 1)
        self.assertEqual((b.get("/api/state").status_code, c.get("/api/state").status_code, a.get("/api/state").status_code), (401, 401, 200))
        self.assertEqual(AuditEvent.objects.filter(key="log_sessions_ended").first().args["n"], 2)
        self.send(a, "post", "logout")
        self.assertFalse(m.UserSession.objects.filter(user=self.tech).exists())

    def test_sessions_from_before_are_listed(self):
        """Browsers signed in before sessions were recorded show up once they load anything, not only after
        signing in again."""
        laptop, phone = self.sign_in("Mozilla/5.0 (Macintosh) Safari"), self.sign_in("Mozilla/5.0 (iPhone) Mobile Safari")
        m.UserSession.objects.all().delete()  # as before the feature
        cache.clear()
        self.assertEqual(phone.get("/api/state").status_code, 200)
        sessions = laptop.get("/api/account/sessions").json()["sessions"]
        self.assertEqual(len(sessions), 2)
        self.assertIn("iPhone", next(s for s in sessions if not s["current"])["agent"])


class LeaverChecklistTests(Base):
    def test_ticks(self):
        tech = self.client_for(self.tech)
        e = Employee.objects.filter(estado="activo").first()
        self.assertEqual(self.send(tech, "post", f"employees/{e.pk}/leaver", {"task": "accounts", "done": True}).status_code, 409)
        Employee.objects.filter(pk=e.pk).update(estado="salida", estado_fecha=timezone.localdate())
        r = self.send(tech, "post", f"employees/{e.pk}/leaver", {"task": "accounts", "done": True}).json()
        self.assertEqual(list(r["employee"]["leaverChecks"]), ["accounts"])
        self.assertEqual(AuditEvent.objects.filter(key="log_leaver_done").first().args, {"name": e.nombre, "task": "accounts"})
        self.send(tech, "post", f"employees/{e.pk}/leaver", {"task": "accounts", "done": False})
        self.assertEqual(Employee.objects.get(pk=e.pk).leaver_checks, {})
        for bad in ({"task": "nope", "done": True}, {"task": "mail", "done": "yes"}):
            self.assertEqual(self.send(tech, "post", f"employees/{e.pk}/leaver", bad).status_code, 400)
        self.assertEqual(self.send(self.client_for(self.reader), "post", f"employees/{e.pk}/leaver", {"task": "mail", "done": True}).status_code, 403)


class AutoBackupSettingsTests(Base):
    def test_settings(self):
        admin = self.client_for(self.admin)
        r = admin.get("/api/backups/auto").json()
        self.assertEqual((r["enabled"], r["hour"], r["keep"], r["updater"]), (True, 2, 14, False))
        r = self.send(admin, "put", "backups/auto", {"enabled": True, "hour": 3, "keep": 7}).json()
        self.assertEqual((r["hour"], r["keep"]), (3, 7))
        self.assertEqual(AuditEvent.objects.order_by("-id").first().args["ch"], [["autoBackupHour", 2, 3], ["autoBackupKeep", 14, 7]])
        for bad in ({"enabled": True, "hour": 24, "keep": 7}, {"enabled": True, "hour": 3, "keep": 0}, {"enabled": "yes", "hour": 3, "keep": 7}):
            self.assertEqual(self.send(admin, "put", "backups/auto", bad).status_code, 400, bad)
        self.assertEqual(self.client_for(self.tech).get("/api/backups/auto").status_code, 403)
        # what the updater reports
        m.UpdaterState.objects.create(pk=1, last_seen=timezone.now(), backup_at=timezone.now(), backup_status="ok",
                                      backup_files=json.dumps([{"name": "auto-20261123-0200.sql.gz", "size": 1234, "at": "2026-11-23T02:00:00+01:00"}]))
        r = admin.get("/api/backups/auto").json()
        self.assertEqual((r["updater"], r["last"]["status"], r["files"][0]["name"]), (True, "ok", "auto-20261123-0200.sql.gz"))


class HistoryCorrectionTests(Base):
    """Administrators can correct the dates of a hand-over or a fault, or delete one; nobody else can."""

    def test_assignment_dates_and_delete(self):
        admin, tech = self.client_for(self.admin), self.client_for(self.tech)
        device = Device.objects.create(tag="FIX-1", serial="S-FIX-1", type=m.DeviceType.objects.first(), loc=m.Location.objects.first(), estado="uso")
        people = list(Employee.objects.filter(estado="activo")[:2])
        old = Assignment.objects.create(device=device, employee=people[0], desde="2025-01-10", hasta="2025-06-30")
        cur = Assignment.objects.create(device=device, employee=people[1], desde="2025-07-01")
        url = f"assignments/{old.pk}"
        self.assertEqual(self.send(tech, "put", url, {"desde": "2025-01-05", "hasta": "2025-06-30"}).status_code, 403)
        self.assertEqual(self.send(tech, "delete", url).status_code, 403)
        r = self.send(admin, "put", url, {"desde": "2025-01-05", "hasta": "2025-07-01"})   # may touch the next one
        self.assertEqual(r.json()["assignment"]["desde"], "2025-01-05")
        self.assertEqual(AuditEvent.objects.filter(key="log_asg_edited").first().args["ch"],
                         [["desde", "2025-01-10", "2025-01-05"], ["hasta", "2025-06-30", "2025-07-01"]])
        for bad, code in (({"desde": "2025-01-05", "hasta": "2025-07-02"}, "err_asg_overlap"),
                          ({"desde": "2025-08-01", "hasta": "2025-07-01"}, "err_dates"),
                          ({"desde": "2025-01-05"}, "err_required"), ({"desde": "nope", "hasta": "2025-07-01"}, "err_invalid")):
            self.assertEqual(self.send(admin, "put", url, bad).json()["error"], code, bad)
        # the current one keeps no end date, and cannot start before the last one was given back
        self.assertEqual(self.send(admin, "put", f"assignments/{cur.pk}", {"desde": "2025-06-15"}).json()["error"], "err_asg_overlap")
        self.assertIsNone(self.send(admin, "put", f"assignments/{cur.pk}", {"desde": "2025-07-03", "hasta": "2025-08-01"}).json()["assignment"]["hasta"])
        # deleting the current one: nobody has it, so it is available
        self.assertEqual(self.send(admin, "delete", f"assignments/{cur.pk}").json(), {})
        device.refresh_from_db()
        self.assertEqual(device.estado, "disponible")
        self.assertEqual(AuditEvent.objects.filter(key="log_asg_deleted").first().args, {"tag": "FIX-1", "name": people[1].nombre, "from": "2025-07-03", "to": ""})
        self.send(admin, "delete", url)
        self.assertFalse(device.assignments.exists())
        self.assertEqual(self.send(admin, "delete", url).status_code, 404)

    def test_fault_dates_and_delete(self):
        admin = self.client_for(self.admin)
        device = Device.objects.create(tag="FIX-2", serial="S-FIX-2", type=m.DeviceType.objects.first(), loc=m.Location.objects.first(), estado="reparacion")
        done = m.Incident.objects.create(device=device, fecha="2025-03-01", tipo="fault", descripcion="Pantalla", estado="resuelta", resuelta="2025-03-10")
        a = m.Incident.objects.create(device=device, fecha="2025-09-01", tipo="fault", descripcion="Teclado")
        b = m.Incident.objects.create(device=device, fecha="2025-09-02", tipo="fault", descripcion="Batería")
        self.assertEqual(self.send(self.client_for(self.tech), "delete", f"incidents/{a.pk}").status_code, 403)
        self.assertEqual(self.send(admin, "put", f"incidents/{done.pk}", {"fecha": "2025-03-11", "resuelta": "2025-03-10"}).json()["error"], "err_fix_dates")
        r = self.send(admin, "put", f"incidents/{done.pk}", {"fecha": "2025-02-27", "resuelta": "2025-03-12"}).json()["incident"]
        self.assertEqual((r["fecha"], r["resuelta"]), ("2025-02-27", "2025-03-12"))
        self.assertIsNone(self.send(admin, "put", f"incidents/{a.pk}", {"fecha": "2025-08-30", "resuelta": "2025-09-01"}).json()["incident"]["resuelta"])
        self.send(admin, "delete", f"incidents/{a.pk}")
        device.refresh_from_db()
        self.assertEqual(device.estado, "reparacion", "another fault is still open")
        self.send(admin, "delete", f"incidents/{b.pk}")
        device.refresh_from_db()
        self.assertEqual(device.estado, "disponible")
        self.assertEqual(AuditEvent.objects.filter(key="log_inc_deleted").count(), 2)
        self.assertEqual(list(device.incidents.all()), [done])
