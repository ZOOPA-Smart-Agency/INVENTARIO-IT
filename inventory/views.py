import io
from pathlib import Path

from django.core.cache import cache
from django.db import connection
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET

from .models import AppSettings, ProfilePhoto


ASSETS = Path(__file__).resolve().parent / "static" / "inventory"


def asset_version():
    """Changes whenever the interface files change, so browsers never reuse an old copy."""
    try:
        return int(max((ASSETS / name).stat().st_mtime for name in ("app.js", "app.css")))
    except OSError:
        return 0


def _logo_version():
    s = AppSettings.objects.filter(pk=1).only("logo_version").first()
    return s.logo_version if s else 0


@ensure_csrf_cookie
def index(request):
    return render(request, "inventory/index.html", {"v": asset_version(), "logo_v": _logo_version()})


def healthz(request):
    """For the hosting platform's health check: confirms the database answers."""
    from .version import VERSION

    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return JsonResponse({"status": "ok", "version": VERSION})


@require_GET
def logo(request):
    """The company logo. Public, because the sign-in page shows it."""
    s = AppSettings.objects.filter(pk=1).only("logo", "logo_type").first()
    if not s or not s.logo_type:
        raise Http404
    response = HttpResponse(bytes(s.logo), content_type=s.logo_type)
    # the URL changes with every upload (?v=), so it can be cached for good
    response["Cache-Control"] = "public, max-age=31536000, immutable"
    # an SVG opened directly must not run scripts
    response["Content-Security-Policy"] = "default-src 'none'; style-src 'unsafe-inline'; sandbox"
    response["X-Content-Type-Options"] = "nosniff"
    return response


def user_photo(request, pk):
    """An account's profile picture, for anyone signed in (it is shown next to names). Made by the server, always JPEG.
    DELETE: an administrator removes it (api.user_photo_delete)."""
    if request.method == "DELETE":
        from .api import user_photo_delete
        return user_photo_delete(request, pk=pk)
    if request.method != "GET":
        return JsonResponse({"error": "err_invalid"}, status=405)
    if not request.user.is_authenticated or not request.user.is_active:
        return JsonResponse({"error": "err_auth"}, status=401)
    photo = ProfilePhoto.objects.filter(user_id=pk).only("data").first()
    if not photo:
        raise Http404
    response = HttpResponse(bytes(photo.data), content_type="image/jpeg")
    # the address changes with every new picture (?v=), so the browser can keep it; not shared caches
    response["Cache-Control"] = "private, max-age=31536000, immutable"
    response["X-Content-Type-Options"] = "nosniff"
    return response


# ---- installable app (progressive web app) -------------------------------------------------

ICONS = ASSETS / "icons"
ICON_FILES = {("any", 32): "favicon-32.png", ("any", 192): "icon-192.png", ("any", 512): "icon-512.png",
              ("maskable", 512): "icon-maskable-512.png", ("apple", 180): "apple-touch-icon.png"}
# space around a company logo: phones crop "maskable" icons to their own shape, keeping only the middle
LOGO_PADDING = {"any": 0.1, "apple": 0.12, "maskable": 0.22}
RASTER_LOGOS = {"image/png", "image/jpeg", "image/webp", "image/gif"}


def _logo_icon(logo, size, purpose):
    """The company logo centred on a white square, as a PNG; None if it cannot be read."""
    from PIL import Image, ImageOps

    try:
        img = Image.open(io.BytesIO(logo))
        if img.width * img.height > 40_000_000:  # absurd dimensions: do not even try
            return None
        img = ImageOps.exif_transpose(img).convert("RGBA")
    except Exception:
        return None
    inner = round(size * (1 - 2 * LOGO_PADDING[purpose]))
    scale = inner / max(img.width, img.height)
    img = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    canvas.alpha_composite(img, ((size - img.width) // 2, (size - img.height) // 2))
    out = io.BytesIO()
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    return out.getvalue()


@require_GET
def app_icon(request, purpose, size):
    """Home-screen and browser icons: made from the company logo when there is one, else the app's own."""
    name = ICON_FILES.get((purpose, size))
    if name is None:
        raise Http404
    data = None
    s = AppSettings.objects.filter(pk=1).only("logo", "logo_type", "logo_version").first()
    if s and s.logo_type in RASTER_LOGOS and s.logo:
        key = f"app-icon:{s.logo_version}:{purpose}:{size}"
        data = cache.get(key)
        if data is None:
            data = _logo_icon(bytes(s.logo), size, purpose) or b""
            cache.set(key, data, 24 * 3600)
    response = HttpResponse(data or (ICONS / name).read_bytes(), content_type="image/png")
    response["Cache-Control"] = "public, max-age=31536000, immutable"  # its address changes with the logo
    response["X-Content-Type-Options"] = "nosniff"
    return response


@require_GET
def manifest(request):
    """What browsers need to install the app on a phone, tablet or computer."""
    v = f"{asset_version()}-{_logo_version()}"
    icon = lambda purpose, size: {"src": f"/app-icon/{purpose}-{size}.png?v={v}", "sizes": f"{size}x{size}", "type": "image/png", "purpose": purpose}
    data = {
        "id": "/", "name": "Inventario de equipos", "short_name": "Inventario", "lang": "es",
        "description": "Inventario de dispositivos, empleados, averías y garantías.",
        "start_url": "/#panel", "scope": "/", "display": "standalone",
        "background_color": "#0a0c13", "theme_color": "#0a0c13",
        "icons": [icon("any", 192), icon("any", 512), icon("maskable", 512)],
    }
    response = JsonResponse(data, content_type="application/manifest+json", json_dumps_params={"ensure_ascii": False})
    response["Cache-Control"] = "no-cache"
    return response


SERVICE_WORKER = """// Inventario: lets the app be installed, and shows a friendly page when the server cannot be reached.
// It never keeps inventory data: every request goes to the server as usual.
const CACHE = 'inventario-%(v)s';
const OFFLINE = '/offline';
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.add(OFFLINE)));
  self.skipWaiting();
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  if (event.request.mode !== 'navigate') return;   // data and files always come straight from the server
  event.respondWith(fetch(event.request).catch(() => caches.match(OFFLINE)));
});
"""


@require_GET
def service_worker(request):
    response = HttpResponse(SERVICE_WORKER % {"v": asset_version()}, content_type="application/javascript")
    response["Cache-Control"] = "no-cache"  # browsers check for a new version on every visit
    return response


@require_GET
def offline(request):
    return render(request, "inventory/offline.html")
