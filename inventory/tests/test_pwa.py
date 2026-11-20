import io
import json

from django.core.cache import cache
from django.test import Client, TestCase
from PIL import Image

from inventory import models as m


def png(width, height, colour=(228, 87, 46, 255)):
    buffer = io.BytesIO()
    Image.new("RGBA", (width, height), colour).save(buffer, "PNG")
    return buffer.getvalue()


def image(response):
    return Image.open(io.BytesIO(b"".join(response.streaming_content) if response.streaming else response.content))


class InstallableAppTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()

    def test_manifest(self):
        response = self.client.get("/manifest.webmanifest")
        self.assertEqual(response["Content-Type"], "application/manifest+json")
        data = json.loads(response.content)
        self.assertEqual((data["display"], data["start_url"], data["scope"], data["short_name"]), ("standalone", "/#panel", "/", "Inventario"))
        sizes = {(i["purpose"], i["sizes"]) for i in data["icons"]}
        self.assertEqual(sizes, {("any", "192x192"), ("any", "512x512"), ("maskable", "512x512")})
        for icon in data["icons"]:  # every icon it lists really exists, at the size it claims
            got = image(self.client.get(icon["src"]))
            self.assertEqual(f"{got.width}x{got.height}", icon["sizes"])

    def test_page_links_the_manifest_and_icons(self):
        html = self.client.get("/").content.decode()
        for needle in ('rel="manifest" href="/manifest.webmanifest"', 'rel="apple-touch-icon"', 'name="theme-color"', 'id="installBtn"'):
            self.assertIn(needle, html)

    def test_service_worker_only_handles_whole_pages(self):
        response = self.client.get("/sw.js")
        self.assertEqual(response["Content-Type"], "application/javascript")
        self.assertEqual(response["Cache-Control"], "no-cache")
        script = response.content.decode()
        self.assertIn("event.request.mode !== 'navigate'", script)
        self.assertIn("/offline", script)

    def test_offline_page(self):
        self.assertContains(self.client.get("/offline"), "Sin conexión")

    def test_default_icons_without_a_logo(self):
        icon = image(self.client.get("/app-icon/maskable-512.png"))
        self.assertEqual(icon.size, (512, 512))
        self.assertNotEqual(icon.convert("RGB").getpixel((5, 5)), (255, 255, 255))  # the blue tile
        self.assertEqual(self.client.get("/app-icon/any-999.png").status_code, 404)
        self.assertEqual(self.client.get("/app-icon/other-512.png").status_code, 404)

    def test_company_logo_becomes_the_icon(self):
        m.AppSettings.objects.update_or_create(pk=1, defaults={"logo": png(400, 160), "logo_type": "image/png", "logo_version": 4})
        icon = image(self.client.get("/app-icon/maskable-512.png?v=4")).convert("RGB")
        self.assertEqual(icon.size, (512, 512))
        self.assertEqual(icon.getpixel((5, 5)), (255, 255, 255))      # white around it
        self.assertEqual(icon.getpixel((256, 256)), (228, 87, 46))    # the logo in the middle
        self.assertEqual(icon.getpixel((256, 150)), (255, 255, 255))  # wide logo: room above it
        self.assertIn("immutable", self.client.get("/app-icon/any-192.png?v=4")["Cache-Control"])
        self.assertRegex(self.client.get("/manifest.webmanifest").content.decode(), r"\?v=\d+-4\"")  # a new logo, a new icon address

    def test_svg_or_broken_logo_falls_back_to_the_app_icon(self):
        for logo, kind in ((b"<svg xmlns='http://www.w3.org/2000/svg'/>", "image/svg+xml"), (b"\x89PNG\r\n\x1a\nbroken", "image/png")):
            cache.clear()
            m.AppSettings.objects.update_or_create(pk=1, defaults={"logo": logo, "logo_type": kind, "logo_version": 5})
            icon = image(self.client.get("/app-icon/any-192.png")).convert("RGBA")
            self.assertEqual(icon.size, (192, 192), kind)
            self.assertNotEqual(icon.getpixel((96, 20))[:3], (255, 255, 255), kind)

    def test_shaped_logo_icons(self):
        m.AppSettings.objects.update_or_create(pk=1, defaults={"logo": png(400, 160), "logo_type": "image/png", "logo_version": 6})
        for shape in ("app", "circle"):
            cache.clear()
            m.AppSettings.objects.filter(pk=1).update(logo_shape=shape)
            tab = image(self.client.get(f"/app-icon/any-192.png?v=6{shape}")).convert("RGBA")
            self.assertEqual(tab.size, (192, 192))
            self.assertEqual(tab.getpixel((96, 96)), (228, 87, 46, 255), shape)   # cropped to fill: no white bands
            self.assertEqual(tab.getpixel((96, 3))[:3], (228, 87, 46), shape)    # the top edge's middle is logo too
            self.assertEqual(tab.getpixel((1, 1))[3], 0, shape)                   # the corners are cut away
            edge = tab.getpixel((20, 20))[3]
            self.assertEqual(edge, 0 if shape == "circle" else 255, shape)       # a circle cuts deeper than rounded corners
            phone = image(self.client.get(f"/app-icon/maskable-512.png?v=6{shape}"))
            self.assertEqual(phone.mode, "RGB", "home-screen icons are solid squares")
            self.assertEqual(phone.getpixel((5, 5)), (255, 255, 255))
            self.assertEqual(phone.getpixel((256, 256)), (228, 87, 46))
        apple = image(self.client.get("/app-icon/apple-180.png?v=6circle"))
        self.assertEqual((apple.size, apple.getpixel((2, 2))), ((180, 180), (255, 255, 255)))
        self.assertRegex(self.client.get("/manifest.webmanifest").content.decode(), r"\?v=\d+-6circle\"")  # a new shape, new addresses


class LogoShapeTests(TestCase):
    def setUp(self):
        cache.clear()
        from django.core.management import call_command
        call_command("load_demo_data", password="Correct-Horse-Battery-7", verbosity=0, stdout=open("/dev/null", "w"))
        self.admin = Client()
        self.admin.force_login(m.User.objects.get(email="admin@empresa.es"))

    def put(self, client, shape):
        return client.put("/api/settings/logo-shape", data=json.dumps({"shape": shape}), content_type="application/json")

    def test_choose_a_shape(self):
        response = self.put(self.admin, "circle")
        self.assertEqual(response.json()["settings"]["logoShape"], "circle")
        event = m.AuditEvent.objects.order_by("-id").first()
        self.assertEqual(event.args, {"xKey": "set_brand", "ch": [["logoShape", "", "circle"]]})
        count = m.AuditEvent.objects.count()
        self.put(self.admin, "circle")
        self.assertEqual(m.AuditEvent.objects.count(), count, "the same shape again: nothing to record")
        self.assertEqual(self.put(self.admin, "star").status_code, 400)
        tech = Client()
        tech.force_login(m.User.objects.get(email="it@empresa.es"))
        self.assertEqual(self.put(tech, "app").status_code, 403)
        self.assertEqual(self.put(self.admin, "").json()["settings"]["logoShape"], "")


class IconFallbackTests(TestCase):
    """Where iPhones and browsers look for icons without being told, and when phones must trust the certificate."""

    def test_root_icons(self):
        for url, size in (("/apple-touch-icon.png", 180), ("/apple-touch-icon-precomposed.png", 180), ("/favicon.ico", 32)):
            response = self.client.get(url)
            self.assertEqual((response.status_code, response["Content-Type"]), (200, "image/png"), url)
            self.assertEqual(image(response).size, (size, size), url)

    def test_own_certificate_flag(self):
        from django.test import override_settings
        with override_settings(OWN_CERTIFICATE=True):
            self.assertTrue(json.loads(self.client.get("/api/bootstrap").content)["settings"]["ownCert"])
        with override_settings(OWN_CERTIFICATE=False):
            self.assertFalse(json.loads(self.client.get("/api/bootstrap").content)["settings"]["ownCert"])
        compose = open("deploy/docker-compose.yml").read()
        self.assertIn("DJANGO_TLS_MODE: ${TLS_MODE:-internal}", compose)  # the web app is told how the server's certificate is made
