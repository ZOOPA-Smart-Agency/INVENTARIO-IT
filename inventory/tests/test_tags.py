import json
from importlib import import_module

from django.apps import apps
from django.core.cache import cache
from django.test import Client, TestCase

from inventory import models as m
from inventory.models import Device, User
from inventory.tags import conflict, next_tag

GOOD = "Correct-Horse-7"


def kind(es, code="", **flags):
    return m.DeviceType.objects.create(nombre={"es": es, "en": es, "ca": es}, code=code, **flags)


class TagTests(TestCase):
    def setUp(self):
        cache.clear()
        m.AppSettings.objects.update_or_create(pk=1, defaults={"tag_prefix": "Z"})
        self.laptop = kind("Portátil", "LAP", has_screen=True, has_battery=True)
        self.macbook = kind("MacBook", "MB", has_screen=True, has_battery=True)
        self.tower = kind("Torre", "PC")
        self.plain = kind("Otro")
        self.store = m.Location.objects.create(nombre={"es": "Almacén", "en": "Storage", "ca": "Magatzem"}, tipo="storage")

    def device(self, tag, dtype):
        return Device.objects.create(tag=tag, serial=tag, type=dtype, loc=self.store)

    def test_each_code_has_its_own_numbering(self):
        self.assertEqual(next_tag(self.laptop), "ZLAP001")
        self.device("ZLAP001", self.laptop)
        self.device("zlap007", self.laptop)  # the highest number counts, whatever its case
        self.device("ZMB002", self.macbook)
        self.device("ZLAPX01", self.laptop)  # not this code: ignored
        self.assertEqual(next_tag(self.laptop), "ZLAP008")
        self.assertEqual(next_tag(self.macbook), "ZMB003")
        self.assertEqual(next_tag(self.tower), "ZPC001")

    def test_types_sharing_a_code_share_the_numbering(self):
        other = kind("Sobremesa", "PC")
        self.device("ZPC004", self.tower)
        self.assertEqual(next_tag(other), "ZPC005")

    def test_without_a_code_the_plain_numbering_stays(self):
        self.device("ZLAP001", self.laptop)
        self.device("Z0004", self.plain)
        self.assertEqual(next_tag(self.plain), "Z0005")
        self.assertEqual(next_tag(None, "INV-"), "INV-0001")

    def test_global_numbering_counts_every_device(self):
        m.AppSettings.objects.filter(pk=1).update(tag_numbering="global")
        self.device("ZLAP001", self.laptop)
        self.device("ZMB007", self.macbook)
        self.device("OLD-99", self.plain)  # not in the scheme: ignored
        self.assertEqual((next_tag(self.laptop), next_tag(self.macbook), next_tag(self.plain)), ("ZLAP008", "ZMB008", "Z0008"))

    def test_an_identifier_cannot_be_used_twice(self):
        self.device("ZLAP001", self.laptop)
        self.device("ZMB002", self.macbook)
        for tag in ("ZLAP001", "zlap001", "ZLAP01", "ZLAP0001"):
            self.assertIsNotNone(conflict(tag), tag)
        self.assertIsNone(conflict("ZMB001"))  # counted by type, MB 1 is free
        self.assertIsNone(conflict("ZLAP002"))
        self.assertIsNone(conflict("SPARE-1"))
        m.AppSettings.objects.filter(pk=1).update(tag_numbering="global")
        self.assertEqual(conflict("ZMB001").tag, "ZLAP001")  # counted globally, 1 is taken
        self.assertEqual(conflict("ZPC2").tag, "ZMB002")
        self.assertIsNone(conflict("ZPC003"))
        self.assertIsNone(conflict("ZLAP001", Device.objects.get(tag="ZLAP001").pk))  # its own tag

    def test_device_form_refuses_a_used_identifier(self):
        m.AppSettings.objects.filter(pk=1).update(tag_numbering="global")
        admin = User.objects.create_user("admin@x.es", GOOD, nombre="Ada", rol="admin")
        client = Client()
        client.force_login(admin)
        mine = self.device("ZLAP001", self.laptop)
        air = m.DeviceModel.objects.create(nombre="MacBook Air", fabricante="Apple", type=self.macbook)
        mini = m.DeviceModel.objects.create(nombre="ThinkCentre", fabricante="Lenovo", type=self.tower)
        body = {"serial": "S1", "typeId": str(self.macbook.pk), "modelId": str(air.pk), "loc": str(self.store.pk), "estado": "disponible"}

        def save(method, url, tag):
            return getattr(client, method)(url, data=json.dumps({**body, "tag": tag}), content_type="application/json")

        response = save("post", "/api/devices", "ZMB001")
        self.assertEqual((response.status_code, response.json()["error"]), (409, "err_dup"))
        self.assertEqual(save("post", "/api/devices", "ZMB002").status_code, 200)
        # an old clash that is left alone does not block other changes; a new one is refused
        clash = self.device("ZPC001", self.tower)
        body.update(typeId=str(self.tower.pk), modelId=str(mini.pk), serial="ZPC001")
        self.assertEqual(save("put", f"/api/devices/{clash.pk}", "ZPC001").status_code, 200)
        self.assertEqual(save("put", f"/api/devices/{clash.pk}", "ZPC002").status_code, 409)
        self.assertEqual(mine.tag, "ZLAP001")

    def test_numbering_setting(self):
        admin = User.objects.create_user("admin@x.es", GOOD, nombre="Ada", rol="admin")
        client = Client()
        client.force_login(admin)
        body = {"orgName": "Zoopa", "tagPrefix": "Z", "dateFmt": "dmy", "currency": "EUR", "warrantyDays": 90}
        response = client.put("/api/settings", data=json.dumps({**body, "tagNumbering": "global"}), content_type="application/json")
        self.assertEqual(response.json()["settings"]["tagNumbering"], "global")
        client.put("/api/settings", data=json.dumps(body), content_type="application/json")  # left out: kept
        self.assertEqual(m.AppSettings.load().tag_numbering, "global")
        response = client.put("/api/settings", data=json.dumps({**body, "tagNumbering": "random"}), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_codes_are_kept_to_capitals_and_digits(self):
        self.assertEqual(kind("Móvil", " mó-v1 ").code, "MV1")

    def test_list_api_saves_the_code(self):
        admin = User.objects.create_user("admin@x.es", GOOD, nombre="Ada", rol="admin")
        client = Client()
        client.force_login(admin)
        response = client.post("/api/lists/types", data=json.dumps({"nombre": {"es": "Tablet"}, "code": "tab"}),
                               content_type="application/json")
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.json()["item"]["code"], "TAB")

    def test_device_app_gets_a_tag_per_type_and_its_type_from_the_model(self):
        User.objects.create_user("tech@x.es", GOOD, nombre="Teo", rol="tech")
        client = Client(enforce_csrf_checks=True)
        token = client.post("/api/agent/login", data=json.dumps({"email": "tech@x.es", "password": GOOD}),
                            content_type="application/json").json()["token"]
        auth = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
        self.device("ZMB001", self.macbook)

        data = client.get("/api/agent/options?chassis=laptop&model=MacBook%20Air%20(M2)", **auth).json()
        self.assertEqual({t["code"]: t["nextTag"] for t in data["types"]}, {"LAP": "ZLAP001", "MB": "ZMB002", "PC": "ZPC001", "": "Z0001"})
        self.assertEqual(data["nextTag"], "ZMB002")
        self.assertEqual(client.get("/api/agent/options?chassis=laptop&model=ThinkPad%20T14", **auth).json()["nextTag"], "ZLAP001")

        facts = {"serial": "C02ABC", "manufacturer": "Apple", "model": "MacBook Pro 14\"", "chassis": "laptop"}
        response = client.post("/api/agent/report", data=json.dumps({"facts": facts}), content_type="application/json", **auth)
        self.assertEqual(response.status_code, 200, response.content)
        d = Device.objects.get(serial="C02ABC")
        self.assertEqual((d.tag, d.type), ("ZMB002", self.macbook))

        facts = {"serial": "PF123", "manufacturer": "Lenovo", "model": "ThinkCentre M70q", "chassis": "desktop"}
        client.post("/api/agent/report", data=json.dumps({"facts": facts, "typeId": str(self.tower.pk)}), content_type="application/json", **auth)
        self.assertEqual(Device.objects.get(serial="PF123").tag, "ZPC001")

    def test_update_fills_codes_for_the_usual_types(self):
        migration = import_module("inventory.migrations.0007_type_code")
        for es, code in (("iMac", ""), ("Móvil", ""), ("Tablet", "")):
            kind(es, code)
        named = kind("Todo en uno")
        custom = kind("Portátil", "NB")
        migration.fill_codes(apps, None)
        codes = dict(m.DeviceType.objects.values_list("nombre__es", "code"))
        self.assertEqual((codes["iMac"], codes["Móvil"], codes["Tablet"]), ("IMC", "MOV", "TAB"))
        named.refresh_from_db(), custom.refresh_from_db()
        self.assertEqual((named.code, custom.code), ("AIO", "NB"))  # a code someone chose is kept
        self.assertEqual(m.DeviceType.objects.get(pk=self.plain.pk).code, "")
