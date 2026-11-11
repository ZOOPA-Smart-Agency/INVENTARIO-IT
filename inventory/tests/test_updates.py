import importlib.util
import json
import os
import shutil
import sys
from datetime import timedelta
from pathlib import Path
from unittest import mock

from django.db import connection
from django.test import Client, TestCase, TransactionTestCase
from django.utils import timezone

from inventory import models as m
from inventory.models import AuditEvent, UpdateJob, UpdaterState, User
from inventory.version import VERSION

GOOD = "Correct-Horse-7"
NEWER = "v99.0.0"


def alive(**over):
    values = dict(last_seen=timezone.now(), running_version=VERSION, latest_tag=NEWER, latest_name=NEWER, latest_notes="Notes",
                  latest_url="https://github.com/acme/inventario/releases/tag/v99.0.0", check_status="update", checked_at=timezone.now())
    values.update(over)
    UpdaterState.objects.update_or_create(pk=1, defaults=values)


class UpdatesApiTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin@x.es", GOOD, nombre="Ana Admin", rol="admin")
        self.client.force_login(self.admin)

    def post(self, url, body=None):
        return self.client.post("/api/updates/" + url, data=json.dumps(body or {}), content_type="application/json")

    def test_status_without_updater(self):
        data = self.client.get("/api/updates").json()
        self.assertEqual((data["installed"], data["updater"]), (VERSION, None))

    def test_status_with_updater(self):
        alive()
        data = self.client.get("/api/updates").json()
        self.assertEqual((data["updater"]["latest"], data["updater"]["status"]), (NEWER, "update"))

    def test_silent_updater_counts_as_absent(self):
        alive(last_seen=timezone.now() - timedelta(minutes=5))
        self.assertIsNone(self.client.get("/api/updates").json()["updater"])
        self.assertEqual(self.post("install", {"tag": NEWER}).json()["error"], "err_no_updater")

    def test_install_queues_the_latest_release(self):
        alive()
        response = self.post("install", {"tag": NEWER})
        self.assertEqual(response.status_code, 200, response.content)
        job = UpdateJob.objects.get()
        self.assertEqual((job.target, job.status, job.requested_by, job.from_version), (NEWER, "queued", "Ana Admin", VERSION))
        self.assertEqual(AuditEvent.objects.first().key, "log_update_requested")

    def test_only_the_release_the_updater_found(self):
        alive()
        for tag in ("v100.0.0", "v0.0.1", f"v{VERSION}", "", "latest; rm -rf /"):
            self.assertEqual(self.post("install", {"tag": tag}).json()["error"], "err_update_stale", tag)
        self.assertFalse(UpdateJob.objects.exists())

    def test_one_at_a_time(self):
        alive()
        self.post("install", {"tag": NEWER})
        self.assertEqual(self.post("install", {"tag": NEWER}).json()["error"], "err_update_busy")

    def test_check_asks_the_updater(self):
        alive(check_requested=False)
        self.assertEqual(self.post("check").json(), {"requested": True})
        self.assertTrue(UpdaterState.objects.get().check_requested)

    def test_check_without_updater_checks_directly(self):
        with mock.patch("inventory.updates.check", return_value={"status": "current"}) as check:
            self.assertEqual(self.post("check").json(), {"result": {"status": "current"}})
        check.assert_called_once()

    def test_automatic_schedule(self):
        response = self.client.put("/api/updates/auto", data=json.dumps({"enabled": True, "hour": 4}), content_type="application/json")
        self.assertEqual(response.json()["auto"], {"enabled": True, "hour": 4})
        s = m.AppSettings.load()
        self.assertEqual((s.auto_update, s.auto_update_hour), (True, 4))
        for bad in (24, -1, 2.5, "x"):
            response = self.client.put("/api/updates/auto", data=json.dumps({"enabled": True, "hour": bad}), content_type="application/json")
            self.assertEqual(response.status_code, 400, bad)

    def test_only_admins(self):
        tech = Client()
        tech.force_login(User.objects.create_user("t@x.es", GOOD, nombre="T", rol="tech"))
        self.assertEqual(tech.get("/api/updates").status_code, 403)
        self.assertEqual(tech.post("/api/updates/install", data="{}", content_type="application/json").status_code, 403)

    def test_health_reports_version_for_the_updater(self):
        self.assertEqual(Client().get("/healthz").json()["version"], VERSION)


def load_updater():
    path = Path(__file__).resolve().parents[2] / "deploy" / "updater" / "updater.py"
    spec = importlib.util.spec_from_file_location("inventario_updater", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UpdaterSqlTests(TransactionTestCase):
    """The updater's SQL, run with psql against the real tables (catches a renamed column before a server does)."""

    def setUp(self):
        if not shutil.which("psql"):
            self.skipTest("psql is not installed")
        self.u = load_updater()
        s = connection.settings_dict
        prefix = ["psql", "-d", s["NAME"]]
        if s.get("HOST"):
            prefix += ["-h", s["HOST"]]
        if s.get("PORT"):
            prefix += ["-p", str(s["PORT"])]
        if s.get("USER"):
            prefix += ["-U", s["USER"]]
        if s.get("PASSWORD"):
            os.environ["PGPASSWORD"] = s["PASSWORD"]
        self.db = self.u.Db(prefix)
        m.AppSettings.load()

    def test_heartbeat_check_and_schedule(self):
        self.db.heartbeat("1.0.0")
        self.db.heartbeat("1.0.1")
        state = UpdaterState.objects.get()
        self.assertEqual(state.running_version, "1.0.1")
        self.assertEqual(self.db.state()["check_requested"], False)
        self.db.save_check("update", {"tag": "v2.0.0", "name": "Two", "notes": "It's got 'quotes'; DROP TABLE x;\nand lines",
                                      "url": "https://github.com/a/b", "published": "2026-11-01T10:00:00Z"})
        state.refresh_from_db()
        self.assertEqual((state.latest_tag, state.check_status), ("v2.0.0", "update"))
        self.assertEqual(state.latest_notes, "It's got 'quotes'; DROP TABLE x;\nand lines")  # values never become SQL
        self.assertEqual(state.latest_published.year, 2026)
        self.assertEqual(self.db.schedule(), (False, 3))

    def test_jobs_and_maintenance(self):
        self.db.queue_automatic("v2.0.0", "1.0.0")
        job = self.db.next_job()
        self.assertEqual((job["target"], job["automatic"]), ("v2.0.0", True))
        self.assertTrue(self.db.automatic_job_since((timezone.now() - timedelta(hours=1)).timestamp()))
        self.assertFalse(self.db.automatic_job_since((timezone.now() + timedelta(hours=1)).timestamp()))
        self.db.job(job["id"], status="running", from_version="1.0.0")
        self.db.maintenance("build", 2, "Ana")
        state = m.Maintenance.objects.get()
        self.assertEqual((state.active, state.kind, state.phase, state.done, state.total, state.started_by), (True, "update", "build", 2, 5, "Ana"))
        self.db.maintenance("check", 4, "someone else")
        self.assertEqual(m.Maintenance.objects.get().started_by, "Ana")  # the same update keeps who started it
        self.db.job(job["id"], status="done", message="", finished=True)
        self.db.end_maintenance()
        saved = UpdateJob.objects.get()
        self.assertEqual((saved.status, saved.message), ("done", ""))
        self.assertIsNotNone(saved.finished_at)
        self.assertFalse(m.Maintenance.objects.get().active)
        self.assertIsNone(self.db.next_job())
