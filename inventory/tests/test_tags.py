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


class AppleTypesTests(TestCase):
    """The 0008 update gives MacBooks and iMacs their own types, codes and models, keeping their tags."""

    def test_apple_models_and_devices_move_to_their_own_types(self):
        migration = import_module("inventory.migrations.0008_apple_types")
        laptop = kind("Portátil", "LAP", has_screen=True, has_battery=True)
        aio = kind("Todo en uno", "AIO", has_screen=True)
        store = m.Location.objects.create(nombre={"es": "Almacén", "en": "Storage", "ca": "Magatzem"}, tipo="storage")
        air = m.DeviceModel.objects.create(nombre="MacBook Air 13\"", fabricante="Apple", type=laptop)
        imac = m.DeviceModel.objects.create(nombre="Apple iMac 24\"", fabricante="Apple", type=aio)
        dell = m.DeviceModel.objects.create(nombre="Latitude 5440", fabricante="Dell", type=laptop)
        mac_dev = Device.objects.create(tag="INV-0001", serial="A", type=laptop, model=air, loc=store)
        imac_dev = Device.objects.create(tag="INV-0002", serial="B", type=aio, model=imac, loc=store)
        dell_dev = Device.objects.create(tag="INV-0003", serial="C", type=laptop, model=dell, loc=store)

        migration.add_apple_types(apps, None)
        migration.add_apple_types(apps, None)  # running again changes nothing
        macbook, imac_type = m.DeviceType.objects.get(code="MB"), m.DeviceType.objects.get(code="IMC")
        self.assertEqual((macbook.nombre["es"], macbook.has_screen, macbook.has_battery), ("MacBook", True, True))
        self.assertEqual((imac_type.nombre["es"], imac_type.has_screen, imac_type.has_battery), ("iMac", True, False))
        self.assertEqual(m.DeviceType.objects.count(), 4)
        for obj in (air, imac, dell, mac_dev, imac_dev, dell_dev):
            obj.refresh_from_db()
        self.assertEqual((air.type, imac.type, dell.type), (macbook, imac_type, laptop))
        self.assertEqual((mac_dev.type, imac_dev.type, dell_dev.type), (macbook, imac_type, laptop))
        self.assertEqual((mac_dev.tag, imac_dev.tag), ("INV-0001", "INV-0002"))  # labels already on devices stay

    def test_an_existing_type_is_reused(self):
        migration = import_module("inventory.migrations.0008_apple_types")
        mine = kind("macbook", has_screen=True, has_battery=True)
        kind("Ordenadores Apple", "IMC", has_screen=True)
        migration.add_apple_types(apps, None)
        mine.refresh_from_db()
        self.assertEqual(mine.code, "MB")
        self.assertEqual(m.DeviceType.objects.count(), 2)

    def test_nothing_is_added_before_the_first_run(self):
        import_module("inventory.migrations.0008_apple_types").add_apple_types(apps, None)
        self.assertFalse(m.DeviceType.objects.exists())

    def test_new_installs_start_with_both(self):
        from inventory.catalog import load_catalog
        load_catalog()
        self.assertEqual(dict(m.DeviceType.objects.filter(code__in=["MB", "IMC"]).values_list("code", "nombre__es")),
                         {"MB": "MacBook", "IMC": "iMac"})


class TypeMatchTests(TestCase):
    """Settings > Device types: words that make the device app choose a type."""

    def setUp(self):
        cache.clear()
        User.objects.create_user("tech@x.es", GOOD, nombre="Teo", rol="tech")
        m.AppSettings.objects.update_or_create(pk=1, defaults={"tag_prefix": "Z"})
        m.Location.objects.create(nombre={"es": "Almacén", "en": "Storage", "ca": "Magatzem"}, tipo="storage")
        self.laptop = kind("Portátil", "LAP", has_screen=True, has_battery=True)
        self.macbook = kind("MacBook", "MB", has_screen=True, has_battery=True)
        self.pro = kind("Portátil de diseño", "DIS", has_screen=True, has_battery=True)
        self.phone = kind("Móvil", "MOV", has_screen=True, has_battery=True)
        self.pro.match = "MacBook Pro, Surface"
        self.pro.save()
        self.phone.match = " iphone ,Pixel,\nGalaxy "
        self.phone.save()
        self.client = Client(enforce_csrf_checks=True)
        token = self.client.post("/api/agent/login", data=json.dumps({"email": "tech@x.es", "password": GOOD}),
                                 content_type="application/json").json()["token"]
        self.auth = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    def guess(self, model, manufacturer="", chassis="laptop"):
        from urllib.parse import urlencode
        query = urlencode({"model": model, "manufacturer": manufacturer, "chassis": chassis})
        return self.client.get(f"/api/agent/options?{query}", **self.auth).json()["nextTag"]

    def test_words_choose_the_type(self):
        self.assertEqual(self.phone.match_words(), ["iphone", "pixel", "galaxy"])
        self.assertEqual(self.guess("MacBook Pro 14\"", "Apple"), "ZDIS001")  # a word beats a type name
        self.assertEqual(self.guess("MacBook Air (M2)", "Apple"), "ZMB001")  # the type's name still works
        self.assertEqual(self.guess("Surface Laptop 5", "Microsoft"), "ZDIS001")
        self.assertEqual(self.guess("Galaxy Tab", "Samsung"), "ZMOV001")
        self.assertEqual(self.guess("ThinkPad T14", "Lenovo"), "ZLAP001")  # nothing matches: by chassis
        self.assertEqual(self.guess("Pixelbook", "Google"), "ZLAP001")  # whole words only

    def test_the_maker_counts_too(self):
        self.phone.match = "Apple"
        self.phone.save()
        self.assertEqual(self.guess("Mac17,5", "Apple"), "ZMOV001")

    def test_report_uses_the_words(self):
        facts = {"serial": "SF1", "manufacturer": "Microsoft", "model": "Surface Laptop 5", "chassis": "laptop"}
        response = self.client.post("/api/agent/report", data=json.dumps({"facts": facts}), content_type="application/json", **self.auth)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(Device.objects.get(serial="SF1").type, self.pro)

    def test_options_list_the_words(self):
        types = self.client.get("/api/agent/options", **self.auth).json()["types"]
        self.assertEqual(next(t for t in types if t["code"] == "DIS")["match"], ["macbook pro", "surface"])

    def test_settings_save_the_words(self):
        admin = User.objects.create_user("admin@x.es", GOOD, nombre="Ada", rol="admin")
        client = Client()
        client.force_login(admin)
        response = client.put(f"/api/lists/types/{self.laptop.pk}", content_type="application/json",
                              data=json.dumps({"nombre": {"es": "Portátil"}, "code": "LAP", "hasScreen": True, "hasBattery": True, "match": "ThinkPad, Latitude"}))
        self.assertEqual(response.json()["item"]["match"], "ThinkPad, Latitude")
        self.assertEqual(self.guess("Latitude 5440", "Dell"), "ZLAP001")

    def test_all_of_a_shape_except_macs(self):
        self.laptop.auto_chassis, self.laptop.auto_not_mac = "laptop", True
        self.laptop.save()
        self.macbook.has_battery = True
        aio = kind("Todo en uno", "AIO", has_screen=True, auto_chassis="all_in_one", auto_not_mac=True)
        imac = kind("iMac", "IMC", has_screen=True)
        self.assertEqual(self.guess("Inspiron 15", "Dell"), "ZLAP001")
        self.assertEqual(self.guess("Mac17,9", "Apple"), "ZMB001")  # a Mac laptop no word catches: not Portátil
        self.assertEqual(self.guess("Vostro 5410", "Dell", "all_in_one"), "ZAIO001")
        self.assertEqual(self.guess("iMac (24-inch)", "Apple", "all_in_one"), "ZIMC001")
        self.assertEqual(self.guess("Mac15,4", "Apple", "all_in_one"), "ZIMC001")  # the next type that fits
        aio.auto_chassis = "bogus"
        aio.save()
        self.assertEqual(aio.auto_chassis, "")
        self.assertIsNotNone(imac)

    def test_rules_beat_the_old_guess(self):
        self.phone.auto_chassis = "laptop"
        self.phone.save()
        self.assertEqual(self.guess("Inspiron 15", "Dell"), "ZMOV001")  # not the first type with a battery

    def test_update_fills_the_starting_types(self):
        migration = import_module("inventory.migrations.0010_type_auto_rules")
        aio = kind("Todo en uno", "AIO", has_screen=True)
        custom = kind("Sobremesa a medida", "PC", uses_name=True)
        prebuilt = kind("Sobremesa premontado", "PC")
        self.macbook.match = ""
        self.macbook.save()
        migration.fill_rules(apps, None)
        for t in (self.laptop, self.macbook, aio, custom, prebuilt, self.pro):
            t.refresh_from_db()
        self.assertEqual((self.laptop.auto_chassis, self.laptop.auto_not_mac), ("laptop", True))
        self.assertIn("ThinkPad", self.laptop.match)
        self.assertEqual(self.macbook.match, "MacBook")
        self.assertEqual((aio.auto_chassis, aio.auto_not_mac), ("all_in_one", True))
        self.assertEqual((prebuilt.auto_chassis, custom.auto_chassis), ("desktop", ""))
        self.assertIn("To Be Filled By O.E.M.", custom.match)
        self.assertEqual(self.pro.match, "MacBook Pro, Surface")  # set by someone: kept

    def test_new_installs_start_with_rules(self):
        m.DeviceType.objects.all().delete()
        from inventory.catalog import load_catalog
        load_catalog()
        rules = {t.code + ("+" if t.uses_name else ""): (t.auto_chassis, t.auto_not_mac, bool(t.match)) for t in m.DeviceType.objects.all()}
        self.assertEqual(rules, {"LAP": ("laptop", True, True), "MB": ("", False, True), "PC": ("desktop", False, True),
                                 "PC+": ("", False, True), "AIO": ("all_in_one", True, True), "IMC": ("", False, True)})
        self.assertEqual(self.guess("To Be Filled By O.E.M.", "To Be Filled By O.E.M.", "desktop"), "ZPC001")

    def test_1_4_0_still_gives_the_apple_types_their_words(self):
        migration = import_module("inventory.migrations.0009_type_match")
        self.macbook.match = ""
        self.macbook.save()
        migration.fill_apple(apps, None)
        self.macbook.refresh_from_db()
        self.assertEqual(self.macbook.match, "MacBook")
