import base64
import io
import json

from django.core.cache import cache
from django.core.management import call_command
from django.test import Client, TestCase
from PIL import Image

from inventory import models as m
from inventory import photos
from inventory.models import User

PASSWORD = "Demo-pass-123!"


def image(fmt="PNG", size=(400, 300), mode="RGB", exif=None):
    out = io.BytesIO()
    img = Image.new(mode, size, (200, 40, 40, 128) if mode == "RGBA" else (200, 40, 40))
    if exif is not None:
        img.save(out, fmt, exif=exif)
    else:
        img.save(out, fmt)
    return out.getvalue()


def data_url(raw, kind="image/png"):
    return f"data:{kind};base64," + base64.b64encode(raw).decode()


class MakePictureTests(TestCase):
    def test_square_jpeg_from_each_format(self):
        for fmt, mode in (("PNG", "RGBA"), ("JPEG", "RGB"), ("WEBP", "RGB"), ("GIF", "P")):
            out = photos.make(image(fmt, mode=mode))
            img = Image.open(io.BytesIO(out))
            self.assertEqual((img.format, img.size), ("JPEG", (256, 256)), fmt)

    def test_photo_details_are_dropped(self):
        exif = Image.Exif()
        exif[0x0112] = 6  # taken turned: 400x300 is really 300x400
        exif[0x010F] = "Camera maker"
        raw = image("JPEG", exif=exif.tobytes())
        out = photos.make(raw)
        self.assertNotIn(b"Camera maker", out)
        self.assertFalse(dict(Image.open(io.BytesIO(out)).getexif()))

    def test_refused(self):
        for raw in (b"<svg xmlns='http://www.w3.org/2000/svg'><script>alert(1)</script></svg>", b"not an image", b"",
                    image("BMP")):
            with self.assertRaises(photos.PhotoError):
                photos.make(raw)
        with self.assertRaises(photos.PhotoError) as e:
            photos.make(image("PNG", size=(8000, 6000)))  # 48 megapixels
        self.assertEqual(e.exception.code, "err_photo_size")
        for value in ("", "data:image/svg+xml;base64,PHN2Zz4=", "data:image/png;base64,***", None, 5):
            with self.assertRaises(photos.PhotoError):
                photos.from_data_url(value)


class PhotoApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("load_demo_data", password=PASSWORD, verbosity=0, stdout=open("/dev/null", "w"))
        cls.reader = User.objects.get(email="lectura@empresa.es")
        cls.admin = User.objects.get(email="admin@empresa.es")

    def setUp(self):
        cache.clear()

    def client_for(self, user):
        client = Client()
        client.force_login(user)
        return client

    def put(self, client, body):
        return client.put("/api/account/photo", data=json.dumps(body), content_type="application/json")

    def test_upload_show_and_remove(self):
        me = self.client_for(self.reader)  # any role sets its own picture
        response = self.put(me, {"data": data_url(image())})
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.json()["me"]["photo"], 1)
        others = self.client_for(self.admin)
        users = {u["id"]: u for u in others.get("/api/state").json()["state"]["users"]}
        self.assertEqual(users[str(self.reader.pk)]["photo"], 1)
        self.assertEqual(users[str(self.admin.pk)]["photo"], 0)
        picture = others.get(f"/api/users/{self.reader.pk}/photo?v=1")
        self.assertEqual((picture.status_code, picture["Content-Type"]), (200, "image/jpeg"))
        self.assertIn("private", picture["Cache-Control"])
        self.assertEqual(Client().get(f"/api/users/{self.reader.pk}/photo").status_code, 401)  # signed out
        self.assertEqual(others.get(f"/api/users/{self.admin.pk}/photo").status_code, 404)

        self.assertEqual(me.delete("/api/account/photo").json()["me"]["photo"], 0)
        self.assertFalse(m.ProfilePhoto.objects.exists())
        self.assertEqual(others.get(f"/api/users/{self.reader.pk}/photo").status_code, 404)
        # a new picture never reuses an old address, which browsers may have kept
        self.assertEqual(self.put(me, {"data": data_url(image())}).json()["me"]["photo"], 2)

    def test_bad_files(self):
        me = self.client_for(self.reader)
        self.assertEqual(self.put(me, {"data": data_url(b"<svg/>", "image/svg+xml")}).json()["error"], "err_photo_type")
        self.assertEqual(self.put(me, {"data": data_url(b"not a png")}).json()["error"], "err_photo_type")
        self.assertEqual(Client().put("/api/account/photo", data="{}", content_type="application/json").status_code, 401)
        self.assertFalse(m.ProfilePhoto.objects.exists())

    def test_deleting_the_account_deletes_the_picture(self):
        self.put(self.client_for(self.reader), {"data": data_url(image())})
        self.reader.delete()
        self.assertFalse(m.ProfilePhoto.objects.exists())


class AdminRemovesPhotoTests(PhotoApiTests):
    """An administrator can remove someone's picture; nobody else can, and it is logged."""

    def test_admin_removes(self):
        self.put(self.client_for(self.reader), {"data": data_url(image())})
        tech = self.client_for(User.objects.get(email="it@empresa.es"))
        self.assertEqual(tech.delete(f"/api/users/{self.reader.pk}/photo").status_code, 403)
        self.assertEqual(self.client_for(self.reader).delete(f"/api/users/{self.reader.pk}/photo").status_code, 403)
        self.assertEqual(Client().delete(f"/api/users/{self.reader.pk}/photo").status_code, 401)
        self.assertTrue(m.ProfilePhoto.objects.exists())
        admin = self.client_for(self.admin)
        self.assertEqual(admin.delete(f"/api/users/{self.reader.pk}/photo").status_code, 200)
        self.assertFalse(m.ProfilePhoto.objects.exists())
        event = m.AuditEvent.objects.order_by("-id").first()
        self.assertEqual((event.key, event.args["name"]), ("log_photo_removed", self.reader.nombre))
        self.assertEqual(admin.delete(f"/api/users/{self.reader.pk}/photo").status_code, 200)  # nothing left: not logged again
        self.assertEqual(m.AuditEvent.objects.filter(key="log_photo_removed").count(), 1)
        self.assertEqual(admin.delete("/api/users/999999/photo").status_code, 404)
        self.assertEqual(admin.post(f"/api/users/{self.reader.pk}/photo").status_code, 405)
