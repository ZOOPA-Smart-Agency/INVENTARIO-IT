from pathlib import Path

from django.db import connection
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET

from .models import AppSettings


ASSETS = Path(__file__).resolve().parent / "static" / "inventory"


def asset_version():
    """Changes whenever the interface files change, so browsers never reuse an old copy."""
    try:
        return int(max((ASSETS / name).stat().st_mtime for name in ("app.js", "app.css")))
    except OSError:
        return 0


@ensure_csrf_cookie
def index(request):
    return render(request, "inventory/index.html", {"v": asset_version()})


def healthz(request):
    """For the hosting platform's health check: confirms the database answers."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return JsonResponse({"status": "ok"})


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
