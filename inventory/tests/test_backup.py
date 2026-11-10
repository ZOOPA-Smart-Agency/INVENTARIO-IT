import base64
import io
import json
import struct
import time
import zipfile
from unittest import mock

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import Client, TestCase

from inventory import backup as backups
from inventory import models as m
from inventory.models import AuditEvent, Device, Employee, User

PASSWORD = "Correct-Horse-Battery-7"
BACKUP_PW = "backup-secret-2026"
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")


def unzip(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        return {name: z.read(name) for name in z.namelist()}


def rezip(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        for name, content in files.items():
            z.writestr(name, content)
    return buffer.getvalue()


class BackupTests(TestCase):
    databases = {"default", "side"}  # restores publish their progress through the second connection

    @classmethod
    def setUpTestData(cls):
        call_command("load_demo_data", password=PASSWORD, verbosity=0, stdout=open("/dev/null", "w"))
        m.AppSettings.objects.filter(pk=1).update(logo=PNG, logo_type="image/png", logo_version=3, pw_min_length=14)

    def setUp(self):
        cache.clear()
        self.client.force_login(User.objects.get(email="admin@empresa.es"))

    def export(self, password="", client=None):
        response = (client or self.client).post("/api/backup/export", data=json.dumps({"password": password}), content_type="application/json")
        self.assertEqual(response.status_code, 200, response.content)
        return response

    def upload(self, url, raw, password=None, client=None):
        data = {"file": SimpleUploadedFile("copia.invbackup", raw, content_type="application/octet-stream")}
        if password:
            data["password"] = password
        return (client or self.client).post("/api/backup/" + url, data=data)

    def snapshot(self):
        return {
            "devices": sorted(Device.objects.values_list("tag", "serial", "estado", "loc_id", "cpu_id", "garantia")),
            "disks": m.Disk.objects.count(), "nics": sorted(m.NetworkCard.objects.values_list("device_id", "mac")),
            "employees": sorted(Employee.objects.values_list("id", "nombre", "estado")),
            "assignments": sorted(m.Assignment.objects.values_list("id", "device_id", "employee_id", "desde", "hasta")),
            "incidents": sorted(m.Incident.objects.values_list("id", "coste", "estado")),
            "users": sorted(User.objects.values_list("email", "rol", "is_active", "password")),
            "types": sorted(m.DeviceType.objects.values_list("id", "nombre")),
            "settings": m.AppSettings.objects.values("org_name", "pw_min_length", "logo_type", "logo_version").get(),
            "logo": bytes(m.AppSettings.load().logo or b""),
        }

    def change_everything(self):
        Device.objects.filter(tag="INV-0001").update(estado="perdido")
        m.Disk.objects.all().delete()
        Employee.objects.create(nombre="Nuevo", email="n@x.es", alta="2026-01-01")
        m.AppSettings.objects.filter(pk=1).update(org_name="Changed", logo=None, logo_type="")

    # ---- access

    def test_only_admins(self):
        tech = Client()
        tech.force_login(User.objects.get(email="it@empresa.es"))
        self.assertEqual(tech.post("/api/backup/export", data="{}", content_type="application/json").status_code, 403)
        self.assertEqual(self.upload("inspect", b"x", client=tech).status_code, 403)
        self.assertEqual(self.upload("restore", b"x", client=tech).status_code, 403)
        self.assertEqual(Client().post("/api/backup/export", data="{}", content_type="application/json").status_code, 401)

    # ---- plain backups

    def test_plain_file_layout(self):
        response = self.export()
        self.assertRegex(response["Content-Disposition"], r'filename="inventario-copia-\d{4}-\d{2}-\d{2}\.invbackup"')
        files = unzip(response.content)
        self.assertEqual(set(files), {"manifest.json", "data.json", "summary.json", "files/logo.png"})
        self.assertEqual(files["files/logo.png"], PNG)
        manifest = json.loads(files["manifest.json"])
        self.assertEqual((manifest["app"], manifest["format"], manifest["encrypted"]), ("inventario", 2, False))
        self.assertEqual(manifest["counts"]["devices"], Device.objects.count())
        data = json.loads(files["data.json"])
        self.assertNotIn("logo", data["inventory.appsettings"][0])  # the logo is a file, not text
        self.assertEqual(AuditEvent.objects.first().key, "log_backup_export")

    def test_plain_round_trip(self):
        before = self.snapshot()
        raw = self.export().content
        logged_at = json.loads(unzip(raw)["data.json"])["inventory.auditevent"][0]["at"]  # oldest entry
        self.change_everything()
        response = self.upload("restore", raw)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(AuditEvent.objects.order_by("id").first().at.isoformat(), logged_at)
        self.assertEqual(AuditEvent.objects.first().key, "log_backup_restore")

    def test_inspect_changes_nothing(self):
        raw = self.export().content
        self.change_everything()
        changed = self.snapshot()
        summary = self.upload("inspect", raw).json()["summary"]
        self.assertEqual((summary["encrypted"], summary["createdBy"]), (False, "admin@empresa.es"))
        self.assertEqual(summary["counts"]["employees"], 10)
        self.assertEqual(self.snapshot(), changed)

    # ---- encrypted backups

    def test_encrypted_file_hides_everything(self):
        raw = self.export(BACKUP_PW).content
        files = unzip(raw)
        self.assertEqual(set(files), {"manifest.json", "payload.bin"})
        manifest = json.loads(files["manifest.json"])
        self.assertTrue(manifest["encrypted"])
        self.assertNotIn("createdBy", manifest)
        self.assertNotIn("counts", manifest)
        self.assertNotIn(b"admin@empresa.es", raw)
        self.assertNotIn(b"pbkdf2", raw)
        self.assertNotIn(b"INV-0001", raw)

    def test_encrypted_round_trip(self):
        before = self.snapshot()
        raw = self.export(BACKUP_PW).content
        self.change_everything()
        summary = self.upload("inspect", raw, BACKUP_PW).json()["summary"]
        self.assertTrue(summary["encrypted"])
        self.assertEqual(summary["createdBy"], "admin@empresa.es")
        self.assertEqual(self.upload("restore", raw, BACKUP_PW).status_code, 200)
        self.assertEqual(self.snapshot(), before)

    def test_encrypted_needs_the_right_password(self):
        raw = self.export(BACKUP_PW).content
        before = self.snapshot()
        self.assertEqual(self.upload("inspect", raw).json()["error"], "err_backup_password_required")
        self.assertEqual(self.upload("restore", raw).json()["error"], "err_backup_password_required")
        self.assertEqual(self.upload("restore", raw, "wrong-password-123").json()["error"], "err_backup_password")
        self.assertEqual(self.snapshot(), before)

    def test_tampered_encrypted_backup_is_refused(self):
        files = unzip(self.export(BACKUP_PW).content)
        manifest = json.loads(files["manifest.json"])
        manifest["created"] = "2020-01-01T00:00:00+00:00"   # the manifest is authenticated with the password
        tampered_manifest = rezip({"manifest.json": json.dumps(manifest), "payload.bin": files["payload.bin"]})
        payload = bytearray(files["payload.bin"]); payload[40] ^= 1
        tampered_payload = rezip({"manifest.json": files["manifest.json"], "payload.bin": bytes(payload)})
        for raw in (tampered_manifest, tampered_payload):
            self.assertEqual(self.upload("restore", raw, BACKUP_PW).json()["error"], "err_backup_password")

    def test_short_backup_password_refused(self):
        response = self.client.post("/api/backup/export", data=json.dumps({"password": "short"}), content_type="application/json")
        self.assertEqual(response.json()["error"], "err_bk_pw_short")

    # ---- safety

    def test_restore_signs_everyone_out_and_passwords_still_work(self):
        other = Client()
        other.force_login(User.objects.get(email="it@empresa.es"))
        self.assertEqual(self.upload("restore", self.export().content).status_code, 200)
        self.assertEqual(self.client.get("/api/state").status_code, 401)
        self.assertEqual(other.get("/api/state").status_code, 401)
        login = Client().post("/api/login", data=json.dumps({"email": "it@empresa.es", "password": PASSWORD}), content_type="application/json")
        self.assertEqual(login.status_code, 200)

    def test_new_records_after_restore_get_fresh_ids(self):
        self.upload("restore", self.export().content)
        employee = Employee.objects.create(nombre="Después", email="d@x.es", alta="2026-01-01")
        self.assertGreater(employee.pk, max(Employee.objects.exclude(pk=employee.pk).values_list("pk", flat=True)))

    def test_bad_files_change_nothing(self):
        before = self.snapshot()
        files = unzip(self.export().content)

        def variant(change):
            copy = dict(files)
            data = json.loads(copy["data.json"]); manifest = json.loads(copy["manifest.json"])
            change(data, manifest)
            copy["data.json"] = json.dumps(data); copy["manifest.json"] = json.dumps(manifest)
            return rezip(copy)

        def no_admin(data, manifest):
            for u in data["inventory.user"]:
                u["rol"] = "read"

        cases = [
            (b"not a zip at all", "err_backup_invalid"),
            (b'{"app": "inventario", "format": 1, "data": {}}', "err_backup_invalid"),  # old .json backups
            (rezip({"readme.txt": "hi"}), "err_backup_invalid"),
            (variant(lambda d, mf: mf.update(format=99)), "err_backup_version"),
            (variant(lambda d, mf: mf.update(app="other")), "err_backup_invalid"),
            (variant(lambda d, mf: d["inventory.device"][0].update(type_id=999999)), "err_backup_invalid"),
            (variant(lambda d, mf: d["inventory.device"][0].update(compra="not a date")), "err_backup_invalid"),
            (variant(no_admin), "err_backup_no_admin"),
        ]
        for raw, error in cases:
            response = self.upload("restore", raw)
            self.assertEqual((response.status_code, response.json().get("error")), (400, error), error)
            self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.client.get("/api/state").status_code, 200)  # still signed in after a refused restore

    # ---- hostile files

    def assert_refused_quickly(self, raw, password=None):
        started = time.monotonic()
        response = self.upload("restore", raw, password)
        self.assertEqual((response.status_code, response.json().get("error")), (400, "err_backup_invalid"))
        self.assertLess(time.monotonic() - started, 5)

    def test_zip_bomb_refused_before_unpacking(self):
        files = unzip(self.export().content)
        manifest = files["manifest.json"]
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            z.writestr("manifest.json", manifest)
            with z.open("data.json", "w", force_zip64=True) as f:   # 200 MB of zeros, about 200 KB packed
                for _ in range(200):
                    f.write(b"0" * 1024 * 1024)
        self.assertLess(len(buffer.getvalue()), 1024 * 1024)
        self.assert_refused_quickly(buffer.getvalue())

    def test_zip_that_lies_about_its_size_is_refused(self):
        real = 5 * 1024 * 1024
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("manifest.json", json.dumps({"app": "inventario", "format": 2, "encrypted": False}))
            z.writestr("summary.json", "{}")
            z.writestr("data.json", b"0" * real)
        raw = bytearray(buffer.getvalue())
        patched = 0
        for sig, size_at, name_len_at, name_at in ((b"PK\x01\x02", 24, 28, 46), (b"PK\x03\x04", 22, 26, 30)):
            i = 0
            while (i := raw.find(sig, i)) != -1:
                n = struct.unpack_from("<H", raw, i + name_len_at)[0]
                if bytes(raw[i + name_at:i + name_at + n]) == b"data.json":
                    struct.pack_into("<I", raw, i + size_at, 1024)   # claims 1 KB
                    patched += 1
                i += 4
        self.assertEqual(patched, 2)
        self.assert_refused_quickly(bytes(raw))

    def test_each_file_has_its_own_limit(self):
        files = unzip(self.export().content)
        too_big_logo = dict(files, **{"files/logo.png": PNG + b"\0" * (512 * 1024)})
        self.assert_refused_quickly(rezip(too_big_logo))
        too_big_summary = dict(files, **{"summary.json": json.dumps({"pad": "x" * 70000})})
        self.assert_refused_quickly(rezip(too_big_summary))
        with mock.patch.dict(backups.LIMITS, {"data.json": 100}):
            self.assert_refused_quickly(self.export().content)

    def test_too_many_entries_refused(self):
        files = unzip(self.export().content)
        crowded = dict(files, **{f"extra{i}.txt": "x" for i in range(10)})
        self.assert_refused_quickly(rezip(crowded))

    def test_unexpected_files_are_never_unpacked(self):
        files = unzip(self.export().content)
        with_junk = dict(files, **{"junk.bin": b"0" * (2 * 1024 * 1024)})   # ignored, so the backup still restores
        self.assertEqual(self.upload("restore", rezip(with_junk)).status_code, 200)

    def test_tampered_key_settings_refused_without_slow_work(self):
        files = unzip(self.export(BACKUP_PW).content)
        for change in ({"p": 1_000_000}, {"n": 2**20}, {"r": 64}, {"name": "pbkdf2"}, {"salt": "AAAA"}):
            manifest = json.loads(files["manifest.json"])
            manifest["kdf"].update(change)
            raw = rezip({"manifest.json": json.dumps(manifest), "payload.bin": files["payload.bin"]})
            self.assert_refused_quickly(raw, BACKUP_PW)

    def test_size_limit(self):
        with mock.patch.object(backups, "MAX_BYTES", 100):
            response = self.upload("restore", b"x" * 101)
        self.assertEqual((response.status_code, response.json()["error"]), (413, "err_backup_size"))
