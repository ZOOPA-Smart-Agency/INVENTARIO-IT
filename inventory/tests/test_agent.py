import json
from datetime import timedelta
from unittest import mock

from django.core.cache import cache
from django.test import Client, TestCase
from django.utils import timezone

from inventory import agent
from inventory import models as m
from inventory.models import AuditEvent, Device, Maintenance, User

GOOD = "Correct-Horse-7"

MAC_FACTS = {
    "serial": "C02XYZ123ABC", "hostname": "MacBook-de-Ana", "manufacturer": "Apple", "model": "MacBook Pro 14\"", "chassis": "laptop",
    "cpu": {"name": "Apple M3 Pro", "cores": 11, "maxGhz": 4.05},
    "ram": {"gb": 18, "type": "LPDDR5", "mts": 6400, "replaceable": "no"},
    "disks": [{"gb": 512, "type": "SSD", "connector": "NVMe"}],
    "gpus": [{"name": "Apple M3 Pro GPU", "kind": "integrated"}],
    "screenInches": 14.2, "battery": {"healthPct": 93},
    "os": {"family": "mac", "version": "15 Sequoia"}, "encryption": "yes", "domainJoined": "no",
    "nics": [{"type": "wifi", "model": "Apple (SoC)", "mac": "f0-18-98-aa-bb-cc"}],
}


class AgentTests(TestCase):
    def setUp(self):
        cache.clear()
        self.tech = User.objects.create_user("tech@x.es", GOOD, nombre="Teo Tech", rol="tech")
        self.laptop = m.DeviceType.objects.create(nombre={"es": "Portátil", "en": "Laptop", "ca": "Portàtil"}, has_screen=True, has_battery=True)
        self.desktop = m.DeviceType.objects.create(nombre={"es": "Sobremesa", "en": "Desktop", "ca": "Sobretaula"})
        self.office = m.Location.objects.create(nombre={"es": "Oficina", "en": "Office", "ca": "Oficina"}, tipo="office")
        self.store = m.Location.objects.create(nombre={"es": "Almacén", "en": "Storage", "ca": "Magatzem"}, tipo="storage")
        m.AppSettings.objects.update_or_create(pk=1, defaults={"tag_prefix": "INV-"})
        self.client = Client(enforce_csrf_checks=True)  # like the device app: no CSRF token, no cookies

    def post(self, url, body, token=None):
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"} if token else {}
        return self.client.post(f"/api/agent/{url}", data=json.dumps(body), content_type="application/json", **headers)

    def token(self, email="tech@x.es"):
        response = self.post("login", {"email": email, "password": GOOD})
        self.assertEqual(response.status_code, 200, response.content)
        return response.json()["token"]

    # ---- signing in

    def test_login_gives_a_key(self):
        data = self.post("login", {"email": "TECH@x.es", "password": GOOD}).json()
        self.assertEqual((data["expiresIn"], data["user"]["rol"]), (3600, "tech"))
        self.assertNotIn("sessionid", self.client.cookies)  # no website session is created

    def test_wrong_password_and_lockout_share_the_website_limit(self):
        self.assertEqual(self.post("login", {"email": "tech@x.es", "password": "nope"}).json()["error"], "login_err")
        for _ in range(10):
            self.post("login", {"email": "tech@x.es", "password": "nope"})
        self.assertEqual(self.post("login", {"email": "tech@x.es", "password": GOOD}).status_code, 429)

    def test_read_only_and_pending_password_change_are_refused(self):
        User.objects.create_user("read@x.es", GOOD, nombre="R", rol="read")
        self.assertEqual(self.post("login", {"email": "read@x.es", "password": GOOD}).json()["error"], "err_forbidden")
        User.objects.create_user("new@x.es", GOOD, nombre="N", rol="tech", must_change_password=True)
        self.assertEqual(self.post("login", {"email": "new@x.es", "password": GOOD}).json()["error"], "err_must_change")

    def test_key_is_required_and_checked(self):
        self.assertEqual(self.client.get("/api/agent/options").status_code, 401)
        self.assertEqual(self.client.get("/api/agent/options", HTTP_AUTHORIZATION="Bearer forged").status_code, 401)
        self.assertEqual(self.post("report", {"facts": MAC_FACTS}).status_code, 401)

    def test_password_change_cancels_keys(self):
        token = self.token()
        self.tech.set_password("Another-Pass-9")
        self.tech.save()
        self.assertEqual(self.client.get("/api/agent/options", HTTP_AUTHORIZATION=f"Bearer {token}").status_code, 401)

    def test_losing_the_role_or_account_cancels_keys(self):
        token = self.token()
        User.objects.filter(pk=self.tech.pk).update(rol="read")
        self.assertEqual(self.client.get("/api/agent/options", HTTP_AUTHORIZATION=f"Bearer {token}").status_code, 403)
        User.objects.filter(pk=self.tech.pk).update(rol="tech", is_active=False)
        self.assertEqual(self.client.get("/api/agent/options", HTTP_AUTHORIZATION=f"Bearer {token}").status_code, 401)

    def test_keys_expire_after_an_hour(self):
        token = self.token()
        later = timezone.now().timestamp() + 3601
        with mock.patch("django.core.signing.time.time", return_value=later):
            self.assertEqual(self.client.get("/api/agent/options", HTTP_AUTHORIZATION=f"Bearer {token}").status_code, 401)

    def test_closed_during_maintenance(self):
        Maintenance.objects.create(pk=1, active=True, kind="restore", updated_at=timezone.now())
        self.assertEqual(self.post("login", {"email": "tech@x.es", "password": GOOD}).status_code, 503)

    # ---- options

    def test_options(self):
        data = self.client.get("/api/agent/options?serial=C02XYZ123ABC", HTTP_AUTHORIZATION=f"Bearer {self.token()}").json()
        self.assertEqual(data["nextTag"], "INV-0001")
        self.assertEqual(len(data["types"]), 2)
        self.assertEqual({l["tipo"] for l in data["locations"]}, {"office", "storage"})
        self.assertIsNone(data["existing"])

    # ---- reporting

    def test_new_computer_is_added_with_everything(self):
        response = self.post("report", {"facts": MAC_FACTS, "loc": str(self.office.pk)}, self.token())
        self.assertEqual(response.status_code, 200, response.content)
        self.assertTrue(response.json()["created"])
        d = Device.objects.get()
        self.assertEqual((d.tag, d.serial, d.nombre, d.type, d.loc, d.estado), ("INV-0001", "C02XYZ123ABC", "MacBook-de-Ana", self.laptop, self.office, "disponible"))
        self.assertEqual((d.model.fabricante, d.model.nombre), ("Apple", "MacBook Pro 14\""))
        self.assertEqual((d.cpu.nombre, d.cpu.cores, d.cpu.speed), ("Apple M3 Pro", 11, 4.05))
        self.assertEqual((d.ram_size, d.ram_gen.nombre, d.ram_speed, d.ram_rep), (18, "LPDDR5", 6400, "no"))
        self.assertEqual([(k.size, k.unit, k.type.nombre, k.conn.nombre) for k in d.disks.all()], [(512, "GB", "SSD", "NVMe")])
        self.assertEqual((d.gpu.nombre, d.gpu.kind), ("Apple M3 Pro GPU", "integrated"))
        self.assertEqual((d.screen, d.bat_health, d.os_family, d.mac_version.nombre, d.enc, d.ad), (14.2, 93, "mac", "15 Sequoia", "yes", "no"))
        self.assertEqual([(n.type, n.mac, n.model.nombre) for n in d.nics.all()], [("wifi", "F0:18:98:AA:BB:CC", "Apple (SoC)")])
        event = AuditEvent.objects.first()
        self.assertEqual((event.key, event.user, event.args["tag"]), ("log_agent_created", self.tech, "INV-0001"))

    def test_existing_computer_is_updated_and_keeps_its_records(self):
        token = self.token()
        self.post("report", {"facts": MAC_FACTS, "tag": "INV-0042"}, token)
        d = Device.objects.get()
        d.estado, d.loc, d.notas, d.precio = "uso", self.office, "Entregado a Ana", 2449
        d.bat_date = timezone.localdate() - timedelta(days=90)
        d.save()
        disk = d.disks.get()
        disk.rep = "no"
        disk.save()
        employee = m.Employee.objects.create(nombre="Ana", email="ana@x.es", alta="2024-01-01")
        m.Assignment.objects.create(device=d, employee=employee, desde="2024-01-01")
        upgraded = dict(MAC_FACTS, serial="c02xyz123abc", ram={"gb": 36, "type": "LPDDR5"}, battery={"healthPct": 88},
                        os={"family": "mac", "version": "26 Tahoe"})
        response = self.post("report", {"facts": upgraded, "tag": "IGNORED", "loc": str(self.store.pk)}, token)
        self.assertFalse(response.json()["created"])
        d.refresh_from_db()
        self.assertEqual(Device.objects.count(), 1)
        self.assertEqual((d.tag, d.estado, d.loc, d.notas, float(d.precio)), ("INV-0042", "uso", self.office, "Entregado a Ana", 2449.0))
        self.assertEqual((d.ram_size, d.mac_version.nombre, d.bat_health), (36, "26 Tahoe", 88))
        self.assertEqual(list(d.battery_readings.values_list("salud", flat=True)), [93])  # the earlier reading is kept
        self.assertEqual(d.disks.get().rep, "no")  # what a person added is kept
        self.assertTrue(d.assignments.filter(hasta__isnull=True).exists())
        self.assertEqual(AuditEvent.objects.first().key, "log_agent_updated")

    def test_known_list_entries_are_reused_not_duplicated(self):
        m.Cpu.objects.create(nombre="Apple M3 Pro", cores=11)
        token = self.token()
        self.post("report", {"facts": MAC_FACTS}, token)
        self.post("report", {"facts": dict(MAC_FACTS, serial="OTHER-1")}, token)
        self.assertEqual(m.Cpu.objects.filter(nombre__iexact="apple m3 pro").count(), 1)
        self.assertEqual(m.DeviceModel.objects.count(), 1)

    def test_wifi_generation_and_bluetooth(self):
        wifi6 = m.WifiGeneration.objects.create(nombre="Wi-Fi 6 (802.11ax)")
        m.WifiGeneration.objects.create(nombre="Wi-Fi 6E")
        bt = m.BluetoothVersion.objects.create(nombre="Bluetooth 5.3")
        token = self.token()
        nics = [{"type": "wifi", "model": "Intel Wi-Fi 6 AX201", "mac": "A4:C3:F0:00:00:01", "wifiGen": "6", "btVer": "5.3"},
                {"type": "eth", "mac": "A4:C3:F0:00:00:02", "wifiGen": "7"}]
        self.post("report", {"facts": dict(MAC_FACTS, nics=nics)}, token)
        wifi, eth = Device.objects.get().nics.all()
        self.assertEqual((wifi.wifi_gen, wifi.bt_ver), (wifi6, bt))  # "6" matches "Wi-Fi 6 (802.11ax)", not "Wi-Fi 6E"
        self.assertIsNone(eth.wifi_gen)  # only Wi-Fi cards have a generation
        # unknown values are ignored and what was there is kept; new generations are added to the list
        self.post("report", {"facts": dict(MAC_FACTS, nics=[dict(nics[0], wifiGen="abc", btVer="")])}, token)
        self.assertEqual(Device.objects.get().nics.get().wifi_gen, wifi6)
        self.post("report", {"facts": dict(MAC_FACTS, nics=[dict(nics[0], wifiGen="7", btVer="5.4")])}, token)
        card = Device.objects.get().nics.get()
        self.assertEqual((card.wifi_gen.nombre, card.bt_ver.nombre), ("Wi-Fi 7", "Bluetooth 5.4"))
        self.assertEqual(m.WifiGeneration.objects.count(), 3)

    def test_windows_and_linux(self):
        token = self.token()
        win = {"serial": "PF4A9Z2B", "manufacturer": "LENOVO", "model": "ThinkPad T14 Gen 4", "chassis": "laptop",
               "os": {"family": "win", "version": "11 23H2", "edition": "Pro"}, "encryption": "no", "domainJoined": "yes",
               "nics": [{"type": "eth", "mac": "98:FA:9B:00:11:22"}, {"type": "wifi", "mac": "00:00:00:00:00:00"}]}
        self.post("report", {"facts": win}, token)
        d = Device.objects.get(serial="PF4A9Z2B")
        self.assertEqual((d.win_version.nombre, d.win_edition.nombre, d.enc, d.ad), ("11 23H2", "Pro", "no", "yes"))
        self.assertEqual(d.nics.count(), 1)  # empty MAC addresses are ignored
        tux = {"serial": "LNX-1", "chassis": "desktop", "os": {"family": "linux", "distro": "Ubuntu", "version": "24.04 LTS"}}
        self.post("report", {"facts": tux}, token)
        d = Device.objects.get(serial="LNX-1")
        self.assertEqual((d.type, d.loc, d.linux_distro.nombre, d.linux_version.nombre, d.linux_version.distro), (self.desktop, self.store, "Ubuntu", "24.04 LTS", d.linux_distro))

    def test_refusals(self):
        token = self.token()
        self.assertEqual(self.post("report", {"facts": {"hostname": "x"}}, token).json()["error"], "err_required")
        self.post("report", {"facts": MAC_FACTS, "tag": "INV-0007"}, token)
        response = self.post("report", {"facts": dict(MAC_FACTS, serial="OTHER"), "tag": "INV-0007"}, token)
        self.assertEqual((response.status_code, response.json()["error"]), (409, "err_dup"))
        self.assertEqual(self.post("report", {"facts": "nope"}, token).status_code, 400)

    def test_values_are_bounded(self):
        token = self.token()
        wild = dict(MAC_FACTS, serial="X" * 500, ram={"gb": -5}, cpu={"name": "A" * 1000, "cores": 10**9}, battery={"healthPct": 999},
                    disks=[{"gb": "lots"}], nics=[{"type": "wifi", "mac": "not-a-mac"}])
        response = self.post("report", {"facts": wild}, token)
        self.assertEqual(response.status_code, 200, response.content)
        d = Device.objects.get()
        self.assertEqual((len(d.serial), d.ram_size, len(d.cpu.nombre), d.cpu.cores, d.bat_health), (100, None, 200, None, None))
        self.assertEqual((d.disks.count(), d.nics.count()), (0, 0))


class OclpAndDrivesTests(TestCase):
    """Macs report whether they start through OpenCore Legacy Patcher, and drives whether they can be replaced."""

    setUp, post, token = AgentTests.setUp, AgentTests.post, AgentTests.token

    def report(self, **facts):
        response = self.post("report", {"facts": {**MAC_FACTS, **facts}, "loc": str(self.office.pk)}, self.token())
        self.assertEqual(response.status_code, 200, response.content)
        return Device.objects.get()

    def test_oclp(self):
        d = self.report(oclp="2.1.0")
        self.assertEqual((d.oclp, d.oclp_version), ("yes", "2.1.0"))
        d = self.report(oclp="yes")  # through OpenCore, version unknown
        self.assertEqual((d.oclp, d.oclp_version), ("yes", ""))
        d = self.report(oclp="")
        self.assertEqual((d.oclp, d.oclp_version), ("no", ""))
        Device.objects.update(oclp="yes", oclp_version="1.0.0")
        facts = dict(MAC_FACTS)  # an older device app sends nothing: what someone set by hand stays
        self.post("report", {"facts": facts}, self.token())
        d = Device.objects.get()
        self.assertEqual((d.oclp, d.oclp_version), ("yes", "1.0.0"))

    def test_exact_macos_version(self):
        d = self.report(os={"family": "mac", "version": "26 Tahoe", "number": "26.2.1"})
        self.assertEqual((str(d.mac_version.nombre), d.os_number), ("26 Tahoe", "26.2.1"))
        d = self.report(os={"family": "mac", "version": "26 Tahoe"})  # an older device app: the number stays
        self.assertEqual(d.os_number, "26.2.1")
        d = self.report(os={"family": "mac", "version": "26 Tahoe", "number": "26.2 beta"})  # not a version number
        self.assertEqual(d.os_number, "")
        self.report(os={"family": "mac", "version": "26 Tahoe", "number": "26.3"})
        d = self.report(os={"family": "win", "version": "11 24H2", "edition": "Pro", "number": "26.3"})
        self.assertEqual(d.os_number, "", "only Macs keep it")

    def test_replaceable_drive(self):
        d = self.report(disks=[{"gb": 1000, "type": "SSD", "connector": "SATA", "replaceable": "yes"}])
        self.assertEqual([k.rep for k in d.disks.all()], ["yes"])


class DriveAndEthernetDetailsTests(TestCase):
    """Device app 0.9.0 sends the drive's connection generation and form factor, and the Ethernet port's speed."""

    setUp, post, token = AgentTests.setUp, AgentTests.post, AgentTests.token

    def report(self, **facts):
        response = self.post("report", {"facts": {**MAC_FACTS, **facts}, "loc": str(self.office.pk)}, self.token())
        self.assertEqual(response.status_code, 200, response.content)
        return Device.objects.get()

    def test_drive_details(self):
        m.DiskConnector.objects.create(nombre="SATA III")
        m.DiskFormFactor.objects.create(nombre='2.5"')
        d = self.report(disks=[{"gb": 1000, "type": "SSD", "connector": "SATA III", "replaceable": "yes", "formFactor": '2.5"'}])
        disk = d.disks.get()
        self.assertEqual((disk.conn.nombre, disk.form.nombre), ("SATA III", '2.5"'))
        self.assertEqual(m.DiskConnector.objects.count(), 1)  # the existing entry, not a copy
        d = self.report(disks=[{"gb": 1000, "type": "SSD", "connector": "SATA III"}])  # not known this time: kept
        self.assertEqual(d.disks.get().form.nombre, '2.5"')

    def test_ethernet_speed(self):
        eth = {"type": "eth", "model": "Broadcom BCM16B4", "mac": "10:dd:b1:f1:15:d0"}
        d = self.report(nics=[{**eth, "speedMbps": 1000}])
        card = d.nics.get()
        self.assertEqual((card.model.nombre, card.speed, card.speed_unit), ("Broadcom BCM16B4", 1.0, "Gbps"))
        d = self.report(nics=[{**eth, "speedMbps": 2500}])
        self.assertEqual((d.nics.get().speed, d.nics.get().speed_unit), (2.5, "Gbps"))
        d = self.report(nics=[{**eth, "speedMbps": 100}])
        self.assertEqual((d.nics.get().speed, d.nics.get().speed_unit), (100, "Mbps"))
        d = self.report(nics=[eth])  # an older app sends no speed: the one saved stays
        self.assertEqual((d.nics.get().speed, d.nics.get().speed_unit), (100, "Mbps"))


class AccuracyTests(TestCase):
    """Fixes from the accuracy review: entries are completed, soldered memory has no modules, old mistakes corrected."""

    setUp, post, token = AgentTests.setUp, AgentTests.post, AgentTests.token

    def report(self, **facts):
        response = self.post("report", {"facts": {**MAC_FACTS, **facts}, "loc": str(self.office.pk)}, self.token())
        self.assertEqual(response.status_code, 200, response.content)
        return Device.objects.get()

    def test_entries_are_filled_in_but_never_overwritten(self):
        m.Gpu.objects.create(nombre="NVIDIA GeForce GTX 775M", kind="", vram=None)
        m.Cpu.objects.create(nombre="Intel Core i5-4670", cores=None, speed=None)
        d = self.report(gpus=[{"name": "NVIDIA GeForce GTX 775M", "kind": "dedicated", "vramGb": 2}],
                        cpu={"name": "Intel Core i5-4670", "cores": 4, "maxGhz": 3.4})
        self.assertEqual((d.gpu.kind, d.gpu.vram, d.cpu.cores, d.cpu.speed), ("dedicated", 2, 4, 3.4))
        m.Gpu.objects.filter(pk=d.gpu.pk).update(vram=4)  # someone corrected it by hand
        d = self.report(gpus=[{"name": "NVIDIA GeForce GTX 775M", "kind": "dedicated", "vramGb": 2}])
        self.assertEqual(d.gpu.vram, 4)

    def test_soldered_memory_has_no_modules(self):
        d = self.report(ram={"gb": 16, "type": "DDR4", "replaceable": "yes", "modules": 2, "moduleGb": 8, "formFactor": "SO-DIMM"})
        self.assertEqual((d.ram_modules, d.ram_mod_size, d.ram_form.nombre), (2, 8, "SO-DIMM"))
        d = self.report(ram={"gb": 16, "type": "LPDDR5", "replaceable": "no"})
        self.assertEqual((d.ram_modules, d.ram_mod_size, d.ram_form), (None, None, None))

    def test_integrated_arc_entries_are_corrected(self):
        from importlib import import_module

        from django.apps import apps
        wrong = m.Gpu.objects.create(nombre="Intel Arc 140V GPU (16GB)", kind="dedicated", vram=4)
        card = m.Gpu.objects.create(nombre="Intel Arc A770 Graphics", kind="dedicated", vram=16)
        import_module("inventory.migrations.0019_fix_integrated_arc").fix(apps, None)
        wrong.refresh_from_db(), card.refresh_from_db()
        self.assertEqual((wrong.nombre, wrong.kind, wrong.vram), ("Intel Arc 140V GPU", "integrated", None))
        self.assertEqual((card.kind, card.vram), ("dedicated", 16))


class DriveOrderTests(TestCase):
    setUp, post, token = AgentTests.setUp, AgentTests.post, AgentTests.token

    def test_details_follow_the_drive_not_its_place(self):
        hdd = {"gb": 2000, "type": "HDD", "connector": "SATA III"}
        ssd = {"gb": 512, "type": "SSD", "connector": "NVMe"}
        self.post("report", {"facts": {**MAC_FACTS, "disks": [ssd, hdd]}, "loc": str(self.office.pk)}, self.token())
        device = Device.objects.get()
        form = m.DiskFormFactor.objects.create(nombre='3.5"')
        device.disks.filter(size=2.0, unit="TB").update(form=form)  # set by hand
        self.post("report", {"facts": {**MAC_FACTS, "disks": [hdd, ssd]}}, self.token())  # listed the other way round
        forms = {(d.size, d.unit): d.form for d in device.disks.all()}
        self.assertEqual((forms[(2.0, "TB")], forms[(512, "GB")]), (form, None))
