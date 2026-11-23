import io
from pathlib import Path

from django.core.cache import cache
from django.db import connection
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from django.utils import timezone

from .models import AppSettings, ProfilePhoto


ASSETS = Path(__file__).resolve().parent / "static" / "inventory"


def asset_version():
    """Changes whenever the interface files change, so browsers never reuse an old copy."""
    try:
        return int(max((ASSETS / name).stat().st_mtime for name in ("app.js", "app.css")))
    except OSError:
        return 0


def _logo_version():
    """What the logo's addresses change with: a new logo, or a new shape for it."""
    s = AppSettings.objects.filter(pk=1).only("logo_version", "logo_shape").first()
    return f"{s.logo_version}{s.logo_shape}" if s else "0"


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


# ---- read-only share link for one device (/s/<token>) ------------------------------------------

SHARE_TEXT = {
    "es": {"title": "Ficha del equipo", "shared": "Compartido en modo solo lectura. Este enlace caduca el {d}.", "gone": "Este enlace ha caducado o ya no existe.",
           "tag": "Etiqueta", "type": "Tipo", "model": "Modelo", "serial": "Número de serie", "cpu": "Procesador", "ram": "Memoria", "disks": "Almacenamiento",
           "gpu": "Gráficos", "screen": "Pantalla", "os": "Sistema operativo", "battery": "Salud de la batería", "bought": "Fecha de compra",
           "warranty": "Garantía hasta", "faults": "Averías y reparaciones", "none": "Ninguna", "open": "Abierta", "done": "Resuelta", "parts": "Piezas"},
    "en": {"title": "Device details", "shared": "Shared read-only. This link expires on {d}.", "gone": "This link has expired or no longer exists.",
           "tag": "Tag", "type": "Type", "model": "Model", "serial": "Serial number", "cpu": "Processor", "ram": "Memory", "disks": "Storage",
           "gpu": "Graphics", "screen": "Screen", "os": "Operating system", "battery": "Battery health", "bought": "Purchase date",
           "warranty": "Warranty until", "faults": "Faults and repairs", "none": "None", "open": "Open", "done": "Resolved", "parts": "Parts"},
    "ca": {"title": "Fitxa de l’equip", "shared": "Compartit en mode només lectura. Aquest enllaç caduca el {d}.", "gone": "Aquest enllaç ha caducat o ja no existeix.",
           "tag": "Etiqueta", "type": "Tipus", "model": "Model", "serial": "Número de sèrie", "cpu": "Processador", "ram": "Memòria", "disks": "Emmagatzematge",
           "gpu": "Gràfics", "screen": "Pantalla", "os": "Sistema operatiu", "battery": "Salut de la bateria", "bought": "Data de compra",
           "warranty": "Garantia fins a", "faults": "Avaries i reparacions", "none": "Cap", "open": "Oberta", "done": "Resolta", "parts": "Peces"},
}


def _share_lang(request):
    for part in request.META.get("HTTP_ACCEPT_LANGUAGE", "").lower().split(","):
        code = part.split(";")[0].strip()[:2]
        if code in SHARE_TEXT:
            return code
    return "es"


def _name(value, lang):
    """A catalogue name, which may be kept in several languages."""
    if value is None:
        return ""
    value = getattr(value, "nombre", value)
    if isinstance(value, dict):
        return str(value.get(lang) or value.get("es") or value.get("en") or "")
    return str(value or "")


def _num(value):
    return "" if value is None else (f"{value:g}" if isinstance(value, float) else str(value))


def _shared_rows(d, lang, tx):
    """What the link shows: the hardware, its warranty and faults. Never who has it, where, or what it cost."""
    model = f"{d.model.fabricante} {d.model.nombre}".strip() if d.model else d.custom_name
    os_name = {"mac": "macOS", "win": "Windows", "linux": _name(d.linux_distro, lang) or "Linux"}.get(d.os_family, "")
    os_ver = _name(d.mac_version or d.win_version or d.linux_version, lang)
    ram = " ".join(x for x in (f"{_num(d.ram_size)} {d.ram_unit}" if d.ram_size else "", _name(d.ram_gen, lang)) if x)
    disks = ", ".join(" ".join(x for x in (f"{_num(k.size)} {k.unit}" if k.size else "", _name(k.type, lang), _name(k.conn, lang)) if x) for k in d.disks.all())
    rows = [("tag", d.tag), ("type", _name(d.type, lang)), ("model", model), ("serial", d.serial), ("cpu", _name(d.cpu, lang)),
            ("ram", ram), ("disks", disks), ("gpu", _name(d.gpu, lang)), ("screen", f'{_num(d.screen)}"' if d.screen else ""),
            ("os", " ".join(x for x in (os_name, d.os_number or os_ver) if x)),
            ("battery", f"{_num(d.bat_health)} %" if d.bat_health is not None else ""),
            ("bought", d.compra.strftime("%d/%m/%Y") if d.compra else ""), ("warranty", d.garantia.strftime("%d/%m/%Y") if d.garantia else "")]
    return [(tx[k], v) for k, v in rows if v]


@require_GET
def shared_device(request, token):
    """A device's details for someone without an account, through a link someone made for them. Read-only."""
    import hashlib

    from django.db.models import F

    from .models import ShareLink

    lang = _share_lang(request)
    tx = SHARE_TEXT[lang]
    link = ShareLink.objects.select_related("device").filter(token_hash=hashlib.sha256(token.encode()).hexdigest()[:64]).first()
    now = timezone.now()
    if link is None or link.revoked_at is not None or link.expires_at <= now:
        response = render(request, "inventory/shared.html", {"tx": tx, "lang": lang, "gone": True}, status=404)
    else:
        ShareLink.objects.filter(pk=link.pk).update(views=F("views") + 1, last_view_at=now)
        d = link.device
        faults = [{"date": i.fecha.strftime("%d/%m/%Y"), "text": _name(i.descripcion, lang), "parts": i.piezas,
                   "status": tx["done"] if i.estado == "resuelta" else tx["open"]} for i in d.incidents.order_by("-fecha")]
        title = (f"{d.model.fabricante} {d.model.nombre}".strip() if d.model else d.custom_name) or d.tag
        response = render(request, "inventory/shared.html", {
            "tx": tx, "lang": lang, "title": title, "tag": d.tag, "rows": _shared_rows(d, lang, tx), "faults": faults,
            "shared": tx["shared"].replace("{d}", timezone.localtime(link.expires_at).strftime("%d/%m/%Y %H:%M"))})
    response["Cache-Control"] = "no-store"
    response["X-Robots-Tag"] = "noindex, nofollow"
    response["Referrer-Policy"] = "no-referrer"
    response["Content-Security-Policy"] = "default-src 'none'; style-src 'unsafe-inline'; img-src 'self'; frame-ancestors 'none'"
    return response


# ---- installable app (progressive web app) -------------------------------------------------

ICONS = ASSETS / "icons"
ICON_FILES = {("any", 32): "favicon-32.png", ("any", 192): "icon-192.png", ("any", 512): "icon-512.png",
              ("maskable", 512): "icon-maskable-512.png", ("apple", 180): "apple-touch-icon.png"}
# space around a company logo: phones crop "maskable" icons to their own shape, keeping only the middle
LOGO_PADDING = {"any": 0.1, "apple": 0.12, "maskable": 0.22}
RASTER_LOGOS = {"image/png", "image/jpeg", "image/webp", "image/gif"}


APP_RADIUS = 0.225  # the app icon's rounded corners, as a share of its side


def _shape_mask(size, shape):
    """White where the shaped logo shows: a rounded square like the app icon, or a circle."""
    from PIL import Image, ImageDraw

    big = size * 4  # drawn larger and reduced, for smooth edges
    mask = Image.new("L", (big, big), 0)
    draw = ImageDraw.Draw(mask)
    if shape == "circle":
        draw.ellipse((0, 0, big - 1, big - 1), fill=255)
    else:
        draw.rounded_rectangle((0, 0, big - 1, big - 1), radius=round(big * APP_RADIUS), fill=255)
    return mask.resize((size, size), Image.LANCZOS)


def _shaped_icon(img, size, purpose, shape):
    """The logo cropped from its centre to fill the shape. Browser icons keep transparent corners; home-screen
    icons need a solid square (phones round them themselves), so the shape sits on white there."""
    from PIL import Image, ImageOps

    if purpose == "apple" and shape == "app":
        inner = size  # iPhone rounds the square to the same shape
    elif purpose == "any":
        inner = size
    else:
        inner = round(size * (1 - 2 * LOGO_PADDING[purpose]))  # inside the part phones always show
    face = ImageOps.fit(img, (inner, inner), Image.LANCZOS)
    if not (purpose == "apple" and shape == "app"):
        face.putalpha(Image.composite(face.getchannel("A"), Image.new("L", face.size, 0), _shape_mask(inner, shape)))
    background = (0, 0, 0, 0) if purpose == "any" else (255, 255, 255, 255)
    canvas = Image.new("RGBA", (size, size), background)
    canvas.alpha_composite(face, ((size - inner) // 2, (size - inner) // 2))
    out = io.BytesIO()
    (canvas if purpose == "any" else canvas.convert("RGB")).save(out, "PNG", optimize=True)
    return out.getvalue()


def _logo_icon(logo, size, purpose, shape=""):
    """The company logo as an icon PNG: centred on a white square, or cropped to `shape`; None if it cannot be read."""
    from PIL import Image, ImageOps

    try:
        img = Image.open(io.BytesIO(logo))
        if img.width * img.height > 40_000_000:  # absurd dimensions: do not even try
            return None
        img = ImageOps.exif_transpose(img).convert("RGBA")
    except Exception:
        return None
    if shape in ("app", "circle"):
        return _shaped_icon(img, size, purpose, shape)
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
    s = AppSettings.objects.filter(pk=1).only("logo", "logo_type", "logo_version", "logo_shape").first()
    if s and s.logo_type in RASTER_LOGOS and s.logo:
        key = f"app-icon:{s.logo_version}:{s.logo_shape}:{purpose}:{size}"
        data = cache.get(key)
        if data is None:
            data = _logo_icon(bytes(s.logo), size, purpose, s.logo_shape) or b""
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
