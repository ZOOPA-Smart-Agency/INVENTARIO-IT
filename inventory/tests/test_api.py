import json

from django.core.cache import cache
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import Client, TestCase

from inventory import models as m
from inventory.models import Assignment, AuditEvent, Device, Employee, User

PASSWORD = "Correct-Horse-Battery-7"


class ApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("load_demo_data", password=PASSWORD, verbosity=0, stdout=open("/dev/null", "w"))
        cls.admin = User.objects.get(email="admin@empresa.es")
        cls.tech = User.objects.get(email="it@empresa.es")
        cls.reader = User.objects.get(email="lectura@empresa.es")

    def setUp(self):
        cache.clear()

    def as_user(self, user):
        client = Client()
        client.force_login(user)
        return client

    def send(self, client, method, url, body=None):
        return getattr(client, method)("/api/" + url, data=json.dumps(body or {}), content_type="application/json")

    def available_device(self):
        return Device.objects.filter(estado="disponible").first()

    def active_employee(self):
        return Employee.objects.filter(estado="activo").first()

    def device_body(self, **over):
        client = self.as_user(self.tech)
        state = client.get("/api/state").json()["state"]
        laptop = next(t for t in state["types"] if t["hasBattery"])
        body = {
            "tag": "INV-9000", "serial": "SER-1", "typeId": laptop["id"],
            "modelId": next(x["id"] for x in state["models"] if x["typeId"] == laptop["id"]),
            "loc": state["locations"][0]["id"], "disks": [], "nics": [],
        }
        body.update(over)
        return body


class AccessTests(ApiTestCase):
    def test_state_requires_sign_in(self):
        self.assertEqual(Client().get("/api/state").status_code, 401)

    def test_bootstrap_leaks_nothing_when_signed_out(self):
        data = Client().get("/api/bootstrap").json()
        self.assertIsNone(data["me"])
        self.assertEqual(set(data), {"me", "settings"})

    def test_login_and_wrong_password(self):
        ok = self.send(Client(), "post", "login", {"email": "ADMIN@empresa.es", "password": PASSWORD})
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(ok.json()["me"]["rol"], "admin")
        bad = self.send(Client(), "post", "login", {"email": "admin@empresa.es", "password": "nope"})
        self.assertEqual((bad.status_code, bad.json()["error"]), (401, "login_err"))

    def test_deactivated_user_cannot_sign_in(self):
        response = self.send(Client(), "post", "login", {"email": "raul.iglesias@empresa.es", "password": PASSWORD})
        self.assertEqual((response.status_code, response.json()["error"]), (403, "login_off"))

    def test_repeated_failures_lock_the_login(self):
        for _ in range(10):
            self.send(Client(), "post", "login", {"email": "admin@empresa.es", "password": "nope"})
        locked = self.send(Client(), "post", "login", {"email": "admin@empresa.es", "password": PASSWORD})
        self.assertEqual((locked.status_code, locked.json()["error"]), (429, "login_locked"))

    def test_csrf_is_enforced(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.tech)
        response = client.post("/api/devices", data="{}", content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_read_only_cannot_change_anything(self):
        client = self.as_user(self.reader)
        device = self.available_device()
        for method, url in [("post", "devices"), ("put", f"devices/{device.pk}"), ("post", f"devices/{device.pk}/status"),
                            ("post", "employees"), ("post", "lists/cpus")]:
            self.assertEqual(self.send(client, method, url).status_code, 403, url)

    def test_technician_cannot_reach_administration(self):
        client = self.as_user(self.tech)
        cpu = m.Cpu.objects.first()
        for method, url in [("put", "settings"), ("post", "users"), ("delete", f"lists/cpus/{cpu.pk}"),
                            ("post", f"users/{self.reader.pk}/toggle")]:
            self.assertEqual(self.send(client, method, url).status_code, 403, url)

    def test_emails_of_accounts_are_only_for_admins(self):
        tech_users = self.as_user(self.tech).get("/api/state").json()["state"]["users"]
        self.assertNotIn("email", tech_users[0])
        admin_users = self.as_user(self.admin).get("/api/state").json()["state"]["users"]
        self.assertIn("email", admin_users[0])

    def test_state_never_contains_password_hashes(self):
        self.assertNotIn("pbkdf2", self.as_user(self.admin).get("/api/state").content.decode())


class DeviceTests(ApiTestCase):
    def test_create_records_audit_with_author(self):
        client = self.as_user(self.tech)
        response = self.send(client, "post", "devices", self.device_body())
        self.assertEqual(response.status_code, 200, response.content)
        event = AuditEvent.objects.first()
        self.assertEqual((event.key, event.user, event.args["tag"]), ("log_created", self.tech, "INV-9000"))

    def test_duplicate_tag_rejected(self):
        client = self.as_user(self.tech)
        existing = Device.objects.first().tag
        response = self.send(client, "post", "devices", self.device_body(tag=existing))
        self.assertEqual((response.status_code, response.json()["error"]), (409, "err_dup"))

    def test_invalid_mac_rejected_and_nothing_saved(self):
        client = self.as_user(self.tech)
        body = self.device_body(nics=[{"type": "wifi", "mac": "not-a-mac"}])
        self.assertEqual(self.send(client, "post", "devices", body).json()["error"], "err_mac")
        self.assertFalse(Device.objects.filter(tag="INV-9000").exists())

    def test_mac_is_normalised(self):
        client = self.as_user(self.tech)
        body = self.device_body(nics=[{"type": "eth", "mac": "aa-bb-cc-dd-ee-ff"}])
        response = self.send(client, "post", "devices", body)
        self.assertEqual(response.json()["device"]["nics"][0]["mac"], "AA:BB:CC:DD:EE:FF")

    def test_model_required_unless_type_uses_a_name(self):
        client = self.as_user(self.tech)
        self.assertEqual(self.send(client, "post", "devices", self.device_body(modelId="")).json()["error"], "err_model_req")
        custom = m.DeviceType.objects.get(uses_name=True)
        response = self.send(client, "post", "devices", self.device_body(typeId=str(custom.pk), modelId="", customName="Render"))
        self.assertEqual(response.json()["device"]["customName"], "Render")

    def test_new_battery_reading_keeps_previous_in_history(self):
        client = self.as_user(self.tech)
        created = self.send(client, "post", "devices", self.device_body(batHealth=90, batDate="2026-01-01")).json()["device"]
        updated = self.send(client, "put", f"devices/{created['id']}", self.device_body(batHealth=80, batDate="2026-06-01")).json()["device"]
        self.assertEqual(updated["batLog"], [{"fecha": "2026-01-01", "salud": 90.0}])
        self.assertEqual(updated["batHealth"], 80.0)

    def test_assign_then_return(self):
        client = self.as_user(self.tech)
        device, employee = self.available_device(), self.active_employee()
        response = self.send(client, "post", f"devices/{device.pk}/assign", {"employeeId": str(employee.pk), "loc": str(device.loc_id)})
        self.assertEqual(response.status_code, 200, response.content)
        device.refresh_from_db()
        self.assertEqual(device.estado, "uso")
        again = self.send(client, "post", f"devices/{device.pk}/assign", {"employeeId": str(employee.pk), "loc": str(device.loc_id)})
        self.assertEqual(again.status_code, 409)
        back = self.send(client, "post", f"devices/{device.pk}/return", {"condicion": "good", "next": "disponible"})
        self.assertEqual(back.status_code, 200, back.content)
        device.refresh_from_db()
        self.assertEqual(device.estado, "disponible")
        self.assertFalse(device.assignments.filter(hasta__isnull=True).exists())

    def test_cannot_assign_to_someone_who_left(self):
        client = self.as_user(self.tech)
        device = self.available_device()
        gone = Employee.objects.get(estado="salida")
        response = self.send(client, "post", f"devices/{device.pk}/assign", {"employeeId": str(gone.pk), "loc": str(device.loc_id)})
        self.assertEqual(response.status_code, 400)

    def test_database_refuses_two_open_assignments(self):
        device, employee = self.available_device(), self.active_employee()
        Assignment.objects.create(device=device, employee=employee, desde="2026-01-01")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Assignment.objects.create(device=device, employee=employee, desde="2026-02-01")

    def test_resolving_last_fault_ends_repair(self):
        client = self.as_user(self.tech)
        device = self.available_device()
        created = self.send(client, "post", f"devices/{device.pk}/incidents", {"tipo": "fault", "descripcion": "x", "rep": True}).json()["incident"]
        device.refresh_from_db()
        self.assertEqual(device.estado, "reparacion")
        self.send(client, "post", f"incidents/{created['id']}/resolve", {"coste": 10})
        device.refresh_from_db()
        self.assertEqual(device.estado, "disponible")

    def test_retiring_closes_assignment_and_stores_disposal(self):
        client = self.as_user(self.tech)
        assignment = Assignment.objects.filter(hasta__isnull=True, device__estado="uso").first()
        response = self.send(client, "post", f"devices/{assignment.device_id}/status",
                             {"estado": "descartado", "metodo": "recycle", "cert": "BR-1"})
        self.assertEqual(response.status_code, 200, response.content)
        assignment.refresh_from_db()
        self.assertIsNotNone(assignment.hasta)
        self.assertEqual(Device.objects.get(pk=assignment.device_id).destino, "recycle")


class EmployeeTests(ApiTestCase):
    def test_leaving_is_neutral_and_lists_pending_devices(self):
        client = self.as_user(self.tech)
        assignment = Assignment.objects.filter(hasta__isnull=True, employee__estado="activo").first()
        response = self.send(client, "post", f"employees/{assignment.employee_id}/status", {"estado": "salida", "fecha": "2026-11-01"})
        self.assertEqual(response.status_code, 200, response.content)
        event = AuditEvent.objects.first()
        self.assertEqual(event.key, "log_left")
        self.assertIn(assignment.device.tag, event.args["tags"])
        self.assertFalse({"motivo", "reason"} & set(event.args))


class SettingsTests(ApiTestCase):
    def test_list_entry_in_use_cannot_be_deleted(self):
        client = self.as_user(self.admin)
        cpu = Device.objects.exclude(cpu=None).first().cpu
        response = self.send(client, "delete", f"lists/cpus/{cpu.pk}")
        self.assertEqual((response.status_code, response.json()["error"]), (409, "in_use_cant"))

    def test_unknown_list_is_404(self):
        self.assertEqual(self.send(self.as_user(self.admin), "post", "lists/nope", {"nombre": "x"}).status_code, 404)

    def test_technician_can_quick_add_list_entry(self):
        response = self.send(self.as_user(self.tech), "post", "lists/cpus", {"nombre": "New CPU", "cores": 8, "speed": 3.2, "speedUnit": "GHz"})
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.json()["item"]["cores"], 8)

    def test_translated_list_needs_spanish_name(self):
        response = self.send(self.as_user(self.admin), "post", "lists/depts", {"nombre": {"es": "", "en": "X"}})
        self.assertEqual(response.json()["error"], "err_name")

    def test_cannot_deactivate_yourself(self):
        response = self.send(self.as_user(self.admin), "post", f"users/{self.admin.pk}/toggle")
        self.assertEqual(response.json()["error"], "err_self")

    def test_cannot_demote_last_admin(self):
        body = {"nombre": "A", "email": self.admin.email, "rol": "tech"}
        response = self.send(self.as_user(self.admin), "put", f"users/{self.admin.pk}", body)
        self.assertEqual(response.json()["error"], "err_last_admin")

    def test_weak_password_rejected(self):
        body = {"nombre": "N", "email": "new@empresa.es", "rol": "read", "pass": "1234"}
        self.assertEqual(self.send(self.as_user(self.admin), "post", "users", body).json()["error"], "err_pass_weak")

    def test_new_user_can_sign_in(self):
        body = {"nombre": "N", "email": "new@empresa.es", "rol": "read", "pass": PASSWORD}
        self.assertEqual(self.send(self.as_user(self.admin), "post", "users", body).status_code, 200)
        self.assertEqual(self.send(Client(), "post", "login", {"email": "new@empresa.es", "password": PASSWORD}).status_code, 200)


class HealthTests(TestCase):
    def test_healthz(self):
        from inventory.version import VERSION
        self.assertEqual(self.client.get("/healthz").json(), {"status": "ok", "version": VERSION})
