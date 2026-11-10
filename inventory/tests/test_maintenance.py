import io
import json
import zipfile
from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.utils import timezone

from inventory import backup as backups
from inventory import maintenance as maint
from inventory import models as m
from inventory.models import Maintenance, User

GOOD = "Correct-Horse-7"


class MaintenanceTests(TestCase):
    databases = {"default", "side"}

    def setUp(self):
        self.admin = User.objects.create_user("admin@x.es", GOOD, nombre="Ana Admin", rol="admin")
        self.tech = User.objects.create_user("tech@x.es", GOOD, nombre="Teo Tech", rol="tech")
        self.admin_client, self.tech_client = Client(), Client()
        self.admin_client.force_login(self.admin)
        self.tech_client.force_login(self.tech)

    def start(self, **over):
        values = dict(active=True, kind="restore", started_at=timezone.now(), started_by="Ana Admin", phase="replacing",
                      done=40, total=100, updated_at=timezone.now())
        values.update(over)
        Maintenance.objects.update_or_create(pk=1, defaults=values)

    def test_everything_is_closed_during_maintenance(self):
        self.start()
        for client in (self.admin_client, self.tech_client, Client()):
            for method, url in [("get", "/api/state"), ("post", "/api/devices"), ("post", "/api/login"), ("post", "/api/backup/export")]:
                if method == "get":
                    response = client.get(url)
                else:
                    response = client.post(url, data="{}", content_type="application/json")
                self.assertEqual((response.status_code, response.json()["error"]), (503, "maintenance"), url)

    def test_administrators_can_follow_it(self):
        self.start()
        info = self.admin_client.get("/api/state").json()["maintenance"]
        self.assertEqual((info["canWatch"], info["startedBy"], info["done"], info["total"]), (True, "Ana Admin", 40, 100))
        status = self.admin_client.get("/api/maintenance").json()
        self.assertTrue(status["active"] and status["canWatch"])

    def test_everyone_else_only_learns_it_is_maintenance(self):
        self.start()
        for client in (self.tech_client, Client()):
            info = client.get("/api/maintenance").json()
            self.assertEqual(info, {"active": True, "kind": "restore", "canWatch": False})
            boot = client.get("/api/bootstrap").json()
            self.assertNotIn("state", boot)
            self.assertFalse(boot["maintenance"]["canWatch"])
            self.assertNotIn("startedBy", boot["maintenance"])

    def test_bootstrap_and_logout_still_answer(self):
        self.start()
        self.assertEqual(self.admin_client.get("/api/bootstrap").status_code, 200)
        self.assertEqual(self.tech_client.post("/api/logout", data="{}", content_type="application/json").status_code, 200)

    def test_stale_maintenance_opens_the_app_again(self):
        self.start(updated_at=timezone.now() - timedelta(minutes=6))
        self.assertEqual(self.tech_client.get("/api/state").status_code, 200)
        self.assertEqual(Client().get("/api/maintenance").json(), {"active": False})

    def test_off_means_normal(self):
        self.start(active=False)
        self.assertEqual(self.tech_client.get("/api/state").status_code, 200)

    def test_only_one_restore_at_a_time(self):
        self.assertTrue(maint.claim("restore", self.admin))
        self.assertFalse(maint.claim("restore", self.admin))
        maint.release()
        self.assertTrue(maint.claim("restore", self.admin))
        maint.release()


class RestoreProgressTests(TestCase):
    databases = {"default", "side"}

    def setUp(self):
        self.admin = User.objects.create_user("admin@x.es", GOOD, nombre="Ana Admin", rol="admin")
        m.Employee.objects.bulk_create([m.Employee(nombre=f"P{i}", email=f"p{i}@x.es", alta="2026-01-01") for i in range(4500)])
        self.client.force_login(self.admin)

    def test_restore_reports_its_progress(self):
        raw = backups.build(self.admin)
        seen = []
        backups.restore(raw, report=lambda phase, done, total: seen.append((phase, done, total)))
        phases = [p for p, _, _ in seen]
        self.assertEqual(phases[0], "reading")
        self.assertEqual(phases[-1], "finishing")
        replacing = [(d, t) for p, d, t in seen if p == "replacing"]
        self.assertGreater(len(replacing), 3)  # several steps, so the bar moves
        self.assertEqual([d for d, _ in replacing], sorted(d for d, _ in replacing))
        self.assertEqual(replacing[-1][0], replacing[-1][1])

    def test_restore_endpoint_ends_maintenance(self):
        raw = backups.build(self.admin)
        upload = SimpleUploadedFile("c.invbackup", raw)
        self.assertEqual(self.client.post("/api/backup/restore", data={"file": upload}).status_code, 200)
        self.assertFalse(Maintenance.objects.using("side").get(pk=1).active)

    def test_failed_restore_ends_maintenance_too(self):
        upload = SimpleUploadedFile("c.invbackup", b"not a backup")
        self.assertEqual(self.client.post("/api/backup/restore", data={"file": upload}).json()["error"], "err_backup_invalid")
        self.assertFalse(Maintenance.objects.using("side").get(pk=1).active)

    def test_second_restore_is_turned_away(self):
        self.assertTrue(maint.claim("restore", self.admin))
        try:
            upload = SimpleUploadedFile("c.invbackup", backups.build(self.admin))
            response = self.client.post("/api/backup/restore", data={"file": upload})
            self.assertEqual((response.status_code, response.json()["error"]), (409, "err_maintenance_busy"))
        finally:
            maint.release()
