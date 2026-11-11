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
