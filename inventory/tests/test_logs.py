import json
from datetime import timedelta

from django.core.cache import cache
from django.core.management import call_command
from django.test import Client, TestCase
from django.utils import timezone

from inventory.models import AuditEvent, Device, Employee, User

PASSWORD = "Correct-Horse-Battery-7"


class LogsBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("load_demo_data", password=PASSWORD, verbosity=0, stdout=open("/dev/null", "w"))
        cls.admin = User.objects.get(email="admin@empresa.es")
        cls.tech = User.objects.get(email="it@empresa.es")

    def setUp(self):
        cache.clear()

    def client_for(self, user):
        client = Client()
        client.force_login(user)
        return client

    def send(self, client, method, url, body=None):
        return getattr(client, method)("/api/" + url, data=json.dumps(body or {}), content_type="application/json")

    def last(self):
        return AuditEvent.objects.order_by("-id").first()

    def logs(self, client=None, **params):
        response = (client or self.client_for(self.admin)).get("/api/logs", params)
        self.assertEqual(response.status_code, 200, response.content)
        return response.json()


class LogsTests(LogsBase):

    # ---- what is recorded

    def test_sign_ins(self):
        client = Client(REMOTE_ADDR="10.0.0.7")
        self.assertEqual(self.send(client, "post", "login", {"email": "it@empresa.es", "password": "wrong"}).status_code, 401)
        failed = self.last()
        self.assertEqual((failed.key, failed.user_id, failed.args), ("log_login_failed", self.tech.pk, {"who": self.tech.nombre, "ip": "10.0.0.7"}))
        self.send(client, "post", "login", {"email": "nobody@x.es", "password": "x"})
        self.assertEqual((self.last().user_id, self.last().args["who"]), (None, "nobody@x.es"))
        self.assertEqual(self.send(client, "post", "login", {"email": "it@empresa.es", "password": PASSWORD}).status_code, 200)
        self.assertEqual((self.last().key, self.last().user_id, self.last().args["ip"]), ("log_login", self.tech.pk, "10.0.0.7"))
        self.send(client, "post", "logout")
        self.assertEqual((self.last().key, self.last().user_id), ("log_logout", self.tech.pk))
        # they stay out of the Overview feed
        keys = {e["k"] for e in self.client_for(self.admin).get("/api/state").json()["state"]["log"]}
        self.assertFalse(keys & {"log_login", "log_login_failed", "log_logout"})

    def test_accounts_and_employees(self):
        admin = self.client_for(self.admin)
        response = self.send(admin, "post", "users", {"nombre": "Nueva Persona", "email": "nueva@empresa.es", "rol": "read", "pass": "Another-Long-Pass-91!"})
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual((self.last().key, self.last().args), ("log_user_created", {"name": "Nueva Persona", "rol": "read"}))
        new = User.objects.get(email="nueva@empresa.es")
        self.send(admin, "post", f"users/{new.pk}/toggle")
        self.assertEqual(self.last().key, "log_user_off")
        self.send(admin, "post", f"users/{new.pk}/toggle")
        self.assertEqual(self.last().key, "log_user_on")
        self.send(admin, "put", f"users/{new.pk}", {"nombre": "Nueva P.", "email": "nueva@empresa.es", "username": "nueva", "rol": "tech", "pass": "Yet-Another-Pass-77!"})
        self.assertEqual((self.last().key, self.last().args), ("log_user_edited", {
            "name": "Nueva P.", "ch": [["nombre", "Nueva Persona", "Nueva P."], ["rol", "read", "tech"], ["password", None, None]]}))
        self.assertNotIn("Yet-Another", json.dumps(self.last().args))
        before = AuditEvent.objects.count()
        self.send(admin, "put", f"users/{new.pk}", {"nombre": "Nueva P.", "email": "nueva@empresa.es", "username": "nueva", "rol": "tech"})
        self.assertEqual(AuditEvent.objects.count(), before, "saved without changes: nothing to record")
        employee = Employee.objects.first()
        body = next(e for e in admin.get("/api/state").json()["state"]["employees"] if e["id"] == str(employee.pk))
        self.send(admin, "put", f"employees/{employee.pk}", body)
        self.assertEqual(AuditEvent.objects.count(), before)
        self.assertEqual(self.send(admin, "put", f"employees/{employee.pk}", {**body, "contrato": "temporal", "email": "otro@x.es"}).status_code, 200)
        self.assertEqual((self.last().key, self.last().args["parts"]), ("log_emp_edited", ["email", "contrato"]))

    # ---- the Logs page

    def test_only_admins(self):
        self.assertEqual(self.client_for(self.tech).get("/api/logs").status_code, 403)
        self.assertEqual(Client().get("/api/logs").status_code, 401)

    def test_pages(self):
        AuditEvent.objects.bulk_create([AuditEvent(key="log_setting", args={"xKey": "set_region"}) for _ in range(230)])
        total = AuditEvent.objects.count()
        first = self.logs()
        self.assertEqual((len(first["events"]), first["more"]), (100, True))
        ids = [int(e["id"]) for e in first["events"]]
        self.assertEqual(ids, sorted(ids, reverse=True))
        seen = ids
        page = first
        while page["more"]:
            page = self.logs(before=seen[-1])
            seen += [int(e["id"]) for e in page["events"]]
        self.assertEqual(len(seen), total)
        self.assertEqual(len(set(seen)), total)
        self.assertIn("at", first["events"][0])

    def test_filters(self):
        device = Device.objects.first()
        AuditEvent.objects.all().delete()
        old = AuditEvent.objects.create(key="log_edited", args={"tag": device.tag}, device=device, user=self.tech)
        AuditEvent.objects.filter(pk=old.pk).update(at=timezone.now() - timedelta(days=10))
        AuditEvent.objects.create(key="log_login", args={"name": self.admin.nombre, "ip": "192.168.1.50"}, user=self.admin)
        AuditEvent.objects.create(key="log_login_failed", args={"who": "intruso@x.es", "ip": "203.0.113.9"})
        keys = lambda **p: [e["k"] for e in self.logs(**p)["events"]]
        self.assertEqual(keys(kind="devices"), ["log_edited"])
        self.assertEqual(keys(kind="access"), ["log_login_failed", "log_login"])
        self.assertEqual(keys(user=self.tech.pk), ["log_edited"])
        self.assertEqual(keys(user="none"), ["log_login_failed"])
        self.assertEqual(keys(q="203.0.113"), ["log_login_failed"])  # what the entry keeps
        self.assertEqual(keys(q=device.tag.lower()), ["log_edited"])
        self.assertEqual(keys(q=self.admin.nombre.split()[0]), ["log_login"])  # who did it
        today = timezone.localdate().isoformat()
        self.assertEqual(keys(**{"from": today}), ["log_login_failed", "log_login"])
        self.assertEqual(keys(to=(timezone.localdate() - timedelta(days=5)).isoformat()), ["log_edited"])
        admin = self.client_for(self.admin)
        for bad in ({"kind": "x"}, {"user": "abc"}, {"from": "2026-13-45"}, {"before": "x"}):
            self.assertEqual(admin.get("/api/logs", bad).status_code, 400, bad)


class LogLimitTests(LogsBase):
    """Settings > Logs: a maximum size, past which the oldest entries are deleted."""

    def put_limit(self, value, client=None):
        return self.send(client or self.client_for(self.admin), "put", "logs/limit", {"maxMb": value})

    def test_values(self):
        for bad in (5, -1, 1024 * 1024 + 1, "20", True, 10.5, None):
            self.assertEqual(self.put_limit(bad).json().get("error"), "err_log_limit", bad)
        self.assertEqual(self.put_limit(20, self.client_for(self.tech)).status_code, 403)
        for good in (0, 10, 1024 * 1024):
            self.assertEqual(self.put_limit(good).json()["maxMb"], good)
        from inventory.models import AppSettings
        self.assertEqual(AppSettings.load().log_max_mb, 1024 * 1024)
        first = self.logs()
        self.assertEqual(first["maxMb"], 1024 * 1024)
        self.assertGreater(first["size"], 0)
        self.assertEqual(first["count"], AuditEvent.objects.count())
        self.assertNotIn("size", self.logs(before=first["events"][-1]["id"]))

    def test_oldest_deleted_past_the_limit(self):
        from unittest import mock
        from inventory import logsize
        AuditEvent.objects.bulk_create([AuditEvent(key="log_setting", args={"xKey": "set_region", "i": i}) for i in range(1500)])
        newest = AuditEvent.objects.order_by("-id").first().pk
        # as if each entry took 10 KB: 10 MB holds 1,024 of them
        with mock.patch.object(logsize, "_row_bytes", return_value=10 * 1024):
            response = self.put_limit(10).json()
            self.assertGreater(response["deleted"], 0)
            self.assertEqual(AuditEvent.objects.filter(key="log_pruned").count(), 1)
            self.assertLessEqual(AuditEvent.objects.count(), 1024 * 0.95 + 2)  # trimmed to 95%, the note and the setting change
            self.assertTrue(AuditEvent.objects.filter(pk=newest).exists(), "the newest entries stay")
            self.assertEqual(self.put_limit(10).json()["deleted"], 0)  # within it now
            # later, while things are logged, it is checked again only every few minutes
            cache.clear()
            AuditEvent.objects.bulk_create([AuditEvent(key="log_setting", args={}) for _ in range(300)])
            self.assertGreater(logsize.enforce(), 0)
            AuditEvent.objects.bulk_create([AuditEvent(key="log_setting", args={}) for _ in range(300)])
            self.assertEqual(logsize.enforce(), 0, "checked a moment ago")
        self.put_limit(0)
        self.assertEqual(logsize.enforce(force=True), 0, "no limit: nothing is deleted")


class ClearerEntriesTests(LogsBase):
    """Entries say what changed: settings, lists, devices, backups and how updates ended."""

    def test_settings(self):
        admin = self.client_for(self.admin)
        from inventory.models import AppSettings
        from inventory.state import settings_json
        body = {**settings_json(AppSettings.load()), "dateFmt": "ymd", "currency": "USD"}
        self.assertEqual(self.send(admin, "put", "settings", body).status_code, 200)
        self.assertEqual(self.last().args, {"xKey": "set_region", "ch": [["dateFmt", "dmy", "ymd"], ["currency", "EUR", "USD"]]})
        count = AuditEvent.objects.count()
        self.send(admin, "put", "settings", body)
        self.assertEqual(AuditEvent.objects.count(), count, "nothing changed")
        self.send(admin, "put", "logs/limit", {"maxMb": 100})
        self.assertEqual(self.last().args, {"xKey": "set_logs", "ch": [["logMax", 0, 100]]})
        self.send(admin, "put", "updates/auto", {"enabled": True, "hour": 4})
        self.assertEqual(self.last().args["ch"][0][0], "autoUpdate")

    def test_lists(self):
        admin = self.client_for(self.admin)
        created = self.send(admin, "post", "lists/cpus", {"nombre": "Intel Core i9-14900K", "cores": 24}).json()["item"]
        self.assertEqual((self.last().key, self.last().args), ("log_item_added", {"xKey": "set_cpus", "name": "Intel Core i9-14900K"}))
        self.send(admin, "put", f"lists/cpus/{created['id']}", {"nombre": "Intel Core i9-14900KF", "cores": 24})
        self.assertEqual((self.last().key, self.last().args["ch"]), ("log_item_edited", [["nombre", "Intel Core i9-14900K", "Intel Core i9-14900KF"]]))
        self.send(admin, "delete", f"lists/cpus/{created['id']}")
        self.assertEqual((self.last().key, self.last().args["name"]), ("log_item_deleted", "Intel Core i9-14900KF"))

    def test_device_parts(self):
        from inventory.api import device_parts_changed
        before = {"estado": "uso", "ramSize": 8, "disks": [{"size": 512, "checked": "2026-01-01"}], "batHealth": 90}
        after = {"estado": "uso", "ramSize": 16, "disks": [{"size": 512, "checked": "2026-02-01"}], "batHealth": 90}
        self.assertEqual(device_parts_changed(before, after), ["ram"])  # a new reading date alone is no change
        self.assertEqual(device_parts_changed(after, after), [])

    def test_backups_and_checks(self):
        admin = self.client_for(self.admin)
        admin.post("/api/backup/export", data=json.dumps({"password": "Long-enough-password-1"}), content_type="application/json")
        self.assertEqual((self.last().key, self.last().args), ("log_backup_export", {"enc": True}))

    def test_update_results(self):
        from inventory import models as m
        from inventory.updates import record_results
        finished = timezone.now() - timedelta(hours=3)
        ok = m.UpdateJob.objects.create(requested_by=self.admin.nombre, from_version="1.18.1", target="v1.19.0", status="done", finished_at=finished)
        bad = m.UpdateJob.objects.create(automatic=True, from_version="1.19.0", target="v1.20.0", status="rolled_back",
                                         message="The new version did not answer.", finished_at=finished)
        m.UpdateJob.objects.create(target="v1.21.0", status="running")  # not finished: nothing yet
        record_results()
        record_results()  # once each
        done = AuditEvent.objects.get(key="log_update_done")
        self.assertEqual((done.args, done.user_id, done.at), ({"job": ok.id, "v": "v1.19.0", "from": "1.18.1", "auto": False}, self.admin.pk, finished))
        back = AuditEvent.objects.get(key="log_update_rolled_back")
        self.assertEqual((back.args["msg"], back.user_id, back.args["auto"]), ("The new version did not answer.", None, True))
        self.assertEqual(AuditEvent.objects.filter(key__startswith="log_update_").exclude(key="log_update_requested").count(), 2)
        self.assertIn("log_update_done", [e["k"] for e in self.logs(kind="system")["events"]])
