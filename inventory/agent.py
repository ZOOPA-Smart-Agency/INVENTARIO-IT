"""API for the device app (the INVENTARIODATA repository): it reads a computer's details and adds or updates it.

The app signs in with an email and password and gets a signed key valid for an hour, sent as
"Authorization: Bearer <key>". No cookies are involved, so these endpoints do not use CSRF protection.
Only active technicians and administrators can use it, and changing the account's password cancels its keys.

    POST /api/agent/login     {"email", "password"}             -> {"token", "expiresIn", "user"}  ("email" may be a username)
    GET  /api/agent/options   ?serial=...&chassis=...&model=...  -> locations, device types (each with its next
                                                                    asset tag), and the device with that serial
                                                                    number, if any
    POST /api/agent/report    {"facts", "tag", "typeId", "loc"}  -> {"created", "device"}

A computer with the same serial number (ignoring case) is updated: its hardware and software details are
refreshed, while its asset tag, status, location, assignment, purchase data and history are kept.
Otherwise it is added, with the given (or next free) asset tag. The shape of "facts" is described in
docs/agent-api.md.
"""
import json
import re
from functools import wraps

from django.contrib.auth import authenticate
from django.core import signing
from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.utils import timezone
from django.utils.crypto import constant_time_compare, salted_hmac
from django.views.decorators.csrf import csrf_exempt

from . import maintenance as maint
from . import models as m
from .api import LOGIN_MAX_ATTEMPTS, LOGIN_WINDOW_SECONDS, MAC_RE, ApiError, _throttle_key, device_parts_changed, login_email
from .models import AuditEvent, Device, User
from .state import device_json
from .tags import conflict as tag_conflict
from .tags import parts
from .tags import next_tag

TOKEN_SALT = "inventario.agent"
TOKEN_SECONDS = 3600
TRI = {"yes", "no", ""}
EDIT_ROLES = {User.Role.ADMIN, User.Role.TECH}


# ---- keys -----------------------------------------------------------------------------


def _password_mark(user):
    """Changes whenever the password does, so a password change cancels every key issued before it."""
    return salted_hmac(TOKEN_SALT, user.password).hexdigest()[:20]


def issue_token(user):
    return signing.dumps({"u": user.pk, "p": _password_mark(user)}, salt=TOKEN_SALT, compress=True)


def user_for_token(token):
    try:
        data = signing.loads(token, salt=TOKEN_SALT, max_age=TOKEN_SECONDS)
    except signing.BadSignature:  # also expired keys
        return None
    user = User.objects.filter(pk=data.get("u"), is_active=True).first()
    if user is None or not constant_time_compare(str(data.get("p", "")), _password_mark(user)):
        return None
    return user


def agent_endpoint(*methods, auth=True):
    """Like the app's own API: method, maintenance, key, role, JSON body, one transaction, errors as i18n keys."""

    def decorate(view):
        @csrf_exempt
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return JsonResponse({"error": "err_invalid"}, status=405)
            if maint.current() is not None:
                return JsonResponse({"error": "maintenance"}, status=503)
            if auth:
                header = request.META.get("HTTP_AUTHORIZATION", "")
                user = user_for_token(header[7:].strip()) if header.startswith("Bearer ") else None
                if user is None:
                    return JsonResponse({"error": "err_auth"}, status=401)
                if user.must_change_password:
                    return JsonResponse({"error": "err_must_change"}, status=403)
                if user.rol not in EDIT_ROLES:
                    return JsonResponse({"error": "err_forbidden"}, status=403)
                request.user = user
            try:
                body = json.loads(request.body or b"{}") if request.method == "POST" else {}
                if not isinstance(body, dict):
                    raise ValueError
            except ValueError:
                return JsonResponse({"error": "err_invalid"}, status=400)
            try:
                with transaction.atomic():
                    result = view(request, body, *args, **kwargs)
            except ApiError as e:
                return JsonResponse({"error": e.code}, status=e.status)
            except IntegrityError:
                return JsonResponse({"error": "err_invalid"}, status=400)
            return JsonResponse(result)

        return wrapper

    return decorate


# ---- reading the app's input ------------------------------------------------------------


def _text(value, limit=200):
    return re.sub(r"\s+", " ", str(value or "")).strip()[:limit]


def _os_number(value):
    """The exact system version ("26.2.1"): numbers and dots only, else nothing."""
    value = _text(value, 20)
    return value if re.fullmatch(r"\d+(\.\d+){0,3}", value) else ""


def _number(value, low=0, high=1_000_000):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return value if low <= value <= high and value == value else None


def _tri(value):
    value = str(value or "").lower()
    return value if value in TRI else ""


def _item(model, name, **defaults):
    """The list entry with this name (ignoring case), created if the inventory does not have it yet."""
    name = _text(name)
    if not name:
        return None
    found = model.objects.filter(nombre__iexact=name, **{k: v for k, v in defaults.items() if k in ("distro", "type")}).first()
    return found or model.objects.create(nombre=name, **defaults)


def _generation(model, label):
    """The list entry for "Wi-Fi 6E" or "Bluetooth 5.3", whether it is written like that or with a note after it
    ("Wi-Fi 6 (802.11ax)"); created if the inventory does not have it yet. "Wi-Fi 6" never matches "Wi-Fi 6E"."""
    pattern = re.compile(re.escape(label) + r"(\s*\(.*\))?", re.IGNORECASE)
    found = next((item for item in model.objects.all() if pattern.fullmatch(item.nombre.strip())), None)
    return found or model.objects.create(nombre=label)


def _drive_label(disk):
    """"512 GB SSD": enough to tell a device's drives apart in the history."""
    size = f"{disk.size:g} {disk.unit}" if disk.size is not None else ""
    return " ".join(x for x in (size, disk.type.nombre if disk.type else "") if x)[:60]


def _nic_speed(n, before):
    """An Ethernet port's fastest speed, from speedMbps (device app 0.9.0): 1000 -> 1 Gbps, 2500 -> 2.5 Gbps, 100 Mbps."""
    mbps = _number(n.get("speedMbps"), 10, 400_000) if n.get("type") == "eth" else None
    if mbps:
        return {"speed": round(mbps / 1000, 1), "speed_unit": "Gbps"} if mbps >= 1000 else {"speed": round(mbps), "speed_unit": "Mbps"}
    return {"speed": before.speed if before else None, "speed_unit": before.speed_unit if before else "Gbps"}


def _wifi_gen(value):
    value = _text(value, 3).upper()
    return _generation(m.WifiGeneration, f"Wi-Fi {value}") if value in ("4", "5", "6", "6E", "7") else None


def _bt_ver(value):
    value = _text(value, 4)
    return _generation(m.BluetoothVersion, f"Bluetooth {value}") if re.fullmatch(r"[1-6]\.[0-9]", value) else None


# ---- endpoints ------------------------------------------------------------------------------


@agent_endpoint("POST", auth=False)
def login(request, body):
    email = login_email(body.get("email"))  # an email address or a username
    password = str(body.get("password") or "")
    key = _throttle_key(request, email or _text(body.get("email"), 254).lower())  # the same limit as the website
    if cache.get(key, 0) >= LOGIN_MAX_ATTEMPTS:
        raise ApiError("login_locked", 429)
    user = authenticate(request, username=email, password=password)  # also for unknown names: same timing
    if user is None:
        inactive = User.objects.filter(email=email, is_active=False).first() if email else None
        if inactive and inactive.check_password(password):
            raise ApiError("login_off", 403)
        cache.set(key, cache.get(key, 0) + 1, LOGIN_WINDOW_SECONDS)
        raise ApiError("login_err", 401)
    cache.delete(key)
    if user.must_change_password:
        raise ApiError("err_must_change", 403)  # the password has to be changed on the website first
    if user.rol not in EDIT_ROLES:
        raise ApiError("err_forbidden", 403)
    return {"token": issue_token(user), "expiresIn": TOKEN_SECONDS, "user": {"nombre": user.nombre, "rol": user.rol}}


def _existing(serial):
    serial = _text(serial, 100)
    return Device.objects.filter(serial__iexact=serial).first() if serial else None


@agent_endpoint("GET")
def options(request, body):
    s = m.AppSettings.load()
    device = _existing(request.GET.get("serial"))
    types = list(m.DeviceType.objects.all())
    guess = _guess_type(request.GET.get("chassis"), request.GET.get("model"), types, request.GET.get("manufacturer"))
    return {
        "org": s.org_name, "nextTag": next_tag(guess, s.tag_prefix, s.tag_numbering), "hostnameIsTag": s.hostname_is_tag,
        "types": [{"id": str(t.pk), "nombre": t.nombre, "hasScreen": t.has_screen, "hasBattery": t.has_battery, "usesName": t.uses_name,
                   "code": t.code, "match": t.match_words(), "autoChassis": t.auto_chassis, "autoApple": t.auto_apple, "nextTag": next_tag(t, s.tag_prefix, s.tag_numbering)} for t in types],
        "locations": [{"id": str(l.pk), "nombre": l.nombre, "tipo": l.tipo} for l in m.Location.objects.all()],
        "existing": None if device is None else {"id": str(device.pk), "tag": device.tag, "estado": device.estado,
                                                 "typeId": str(device.type_id), "loc": str(device.loc_id)},
        "hostnameTag": _hostname_tag(request.GET.get("hostname"), device, types, s) if request.GET.get("hostname") else None,
    }


def _hostname_tag(hostname, device, types, s):
    """With "the hostname is the asset tag" on: can this computer's name be its tag?

    valid: it follows the tags' pattern (prefix, a device type's code or none, a number), such as ZLAP004;
    tag: that name written as a tag.
    usedBy: the tag of another device that has it, or has the same identifier (see tags.conflict).
    matches: for a computer already in the inventory, whether the name is its tag.
    """
    hostname = _text(hostname, 63)
    found = parts(hostname, s.tag_prefix)
    codes = {t.code for t in types if t.code}
    valid = bool(hostname) and found is not None and (found[0] in codes or found[0] == "")
    other = tag_conflict(hostname, device.pk if device else None) if valid else None
    # written the way tags are: the prefix as set, the code in capitals (zlap004 -> ZLAP004)
    tag = s.tag_prefix + found[0] + hostname[len(s.tag_prefix) + len(found[0]):] if valid else ""
    return {"name": hostname, "tag": tag, "valid": valid, "usedBy": other.tag if other else None,
            "matches": bool(device) and hostname.lower() == device.tag.lower()}


def _type_names(t):
    return [str(n).lower() for n in (t.nombre.values() if isinstance(t.nombre, dict) else [t.nombre]) if n]


def _is_apple(manufacturer, model):
    return "apple" in (manufacturer or "").lower() or bool(re.match(r"\s*(imac|macbook|mac(?![a-z]))", (model or "").lower()))


def _guess_type(chassis, model=None, types=None, manufacturer=None):
    """The type for a new computer, chosen in this order (the device app makes the same choice):

    1. One whose words to match (Settings > Device types) appear in the maker or model, such as "ThinkPad".
    2. One whose name appears there: a "MacBook Air" is a "MacBook".
    3. One set to take every computer of this shape (all laptops, desktops or all-in-ones), then one set to take
       every computer whatever its shape, leaving out those whose rule is only for Apple computers when this is not
       one, or for all but Apple computers when it is.
    4. One that fits the shape: a laptop gets a type with a battery. Otherwise, the first type.
    A longer word wins over a shorter one, so "MacBook Pro" can go apart from "MacBook".
    """
    types = list(m.DeviceType.objects.all()) if types is None else types
    text = f"{manufacturer or ''} {model or ''}".lower()
    apple = _is_apple(manufacturer, model)

    def longest(words):
        return max((len(w) for w in words if re.search(r"(^|[^a-z])" + re.escape(w) + r"($|[^a-z])", text)), default=0)

    for words in (m.DeviceType.match_words, _type_names):
        scored = [(longest(words(t)), t) for t in types]
        best = max(scored, key=lambda x: x[0], default=(0, None))
        if best[0]:
            return best[1]
    allowed = [t for t in types if t.auto_apple != ("except" if apple else "only")]
    ruled = (next((t for t in allowed if chassis and t.auto_chassis == chassis), None)
             or next((t for t in allowed if t.auto_chassis == "any"), None))
    if ruled:
        return ruled
    wanted = {"laptop": lambda t: t.has_battery, "all_in_one": lambda t: t.has_screen and not t.has_battery,
              "desktop": lambda t: not t.has_screen and not t.has_battery and not t.uses_name}.get(chassis)
    return next((t for t in allowed if wanted and wanted(t)), None) or (allowed or types or [None])[0]


@agent_endpoint("POST")
def report(request, body):
    facts = body.get("facts")
    if not isinstance(facts, dict):
        raise ApiError("err_invalid")
    serial = _text(facts.get("serial"), 100)
    if not serial:
        raise ApiError("err_required")
    device = _existing(serial)
    created = device is None
    if created:
        dtype = (m.DeviceType.objects.filter(pk=_int(body.get("typeId"))).first()
                 or _guess_type(facts.get("chassis"), facts.get("model"), manufacturer=facts.get("manufacturer")))
        tag = _text(body.get("tag"), 50)
        if not tag and m.AppSettings.load().hostname_is_tag:  # the computer's name, when it is a valid, free tag
            check = _hostname_tag(facts.get("hostname"), None, list(m.DeviceType.objects.all()), m.AppSettings.load())
            tag = check["tag"] if check["valid"] and not check["usedBy"] else ""
        tag = tag or next_tag(dtype)
        if tag_conflict(tag):  # the same tag, or the same identifier, as another device
            raise ApiError("err_dup", 409)
        loc = (m.Location.objects.filter(pk=_int(body.get("loc"))).first()
               or m.Location.objects.filter(tipo="storage").first() or m.Location.objects.first())
        if dtype is None or loc is None:
            raise ApiError("err_required")  # the inventory needs device types and a location first
        device = Device(tag=tag, serial=serial, type=dtype, loc=loc, estado=Device.State.AVAILABLE)
    else:
        device = Device.objects.select_for_update().get(pk=device.pk)
    before = None if created else device_json(device)
    _apply_facts(device, facts)
    device.save()
    _apply_parts(device, facts)
    args = {"tag": device.tag}
    if before is not None:
        args["parts"] = device_parts_changed(before, device_json(device))  # empty: read again, nothing changed
    AuditEvent.objects.create(key="log_agent_created" if created else "log_agent_updated", args=args,
                              device=device, user=request.user)
    return {"created": created, "device": device_json(device)}


def _int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _apply_facts(device, f):
    """Hardware and software details. Asset tag, status, location, purchase data and notes are never touched."""
    if not m.AppSettings.load().hostname_is_tag and _text(f.get("hostname"), 100):
        device.nombre = _text(f.get("hostname"), 100)
    manufacturer, model_name = _text(f.get("manufacturer"), 100), _text(f.get("model"))
    if device.type.uses_name:
        if manufacturer or model_name:
            device.custom_name = device.custom_name or " ".join(x for x in (manufacturer, model_name) if x)[:200]
    elif model_name:
        device.model = (m.DeviceModel.objects.filter(nombre__iexact=model_name, fabricante__iexact=manufacturer, type=device.type).first()
                        or m.DeviceModel.objects.create(nombre=model_name, fabricante=manufacturer, type=device.type))

    cpu = f.get("cpu") if isinstance(f.get("cpu"), dict) else {}
    if _text(cpu.get("name")):
        found = m.Cpu.objects.filter(nombre__iexact=_text(cpu.get("name"))).first()
        cores, ghz = _number(cpu.get("cores"), 1, 1024), _number(cpu.get("maxGhz"), 0.1, 20)
        if found is None:
            found = m.Cpu.objects.create(nombre=_text(cpu.get("name")), cores=int(cores) if cores else None, speed=ghz, speed_unit="GHz")
        elif (found.cores is None and cores) or (found.speed is None and ghz):  # fill in what the entry lacks; never overwrite
            found.cores = found.cores or (int(cores) if cores else None)
            if found.speed is None and ghz:
                found.speed, found.speed_unit = ghz, "GHz"
            found.save()
        device.cpu = found

    ram = f.get("ram") if isinstance(f.get("ram"), dict) else {}
    if _number(ram.get("gb"), 0.1, 65536):
        device.ram_size, device.ram_unit = round(_number(ram.get("gb"), 0.1, 65536), 1), "GB"
    if _text(ram.get("type")):
        device.ram_gen = _item(m.RamGeneration, ram.get("type"))
    if _number(ram.get("mts"), 100, 20000):
        device.ram_speed, device.ram_speed_unit = _number(ram.get("mts"), 100, 20000), "MT/s"
    if _tri(ram.get("replaceable")):
        device.ram_rep = _tri(ram.get("replaceable"))
    if device.ram_rep == "no":  # soldered: no modules to describe (older reports may have left some)
        device.ram_modules, device.ram_mod_size, device.ram_form = None, None, None
    if device.ram_rep == "yes":
        modules, module_gb = _number(ram.get("modules"), 1, 64), _number(ram.get("moduleGb"), 0.1, 4096)
        device.ram_modules = int(modules) if modules else device.ram_modules
        if module_gb:
            device.ram_mod_size, device.ram_mod_unit = module_gb, "GB"
        if _text(ram.get("formFactor")):
            device.ram_form = _item(m.RamFormFactor, ram.get("formFactor"))

    gpus = [g for g in (f.get("gpus") or []) if isinstance(g, dict) and _text(g.get("name"))][:8]
    if gpus:
        main = next((g for g in gpus if g.get("kind") == "dedicated"), gpus[0])
        found = m.Gpu.objects.filter(nombre__iexact=_text(main.get("name"))).first()
        kind = main.get("kind") if main.get("kind") in ("integrated", "dedicated") else ""
        vram = _number(main.get("vramGb"), 0.1, 1024) if kind == "dedicated" else None
        if found is None:
            found = m.Gpu.objects.create(nombre=_text(main.get("name")), kind=kind, vram=vram, vram_unit="GB")
        elif (not found.kind and kind) or (found.vram is None and vram):  # fill in what the entry lacks; never overwrite
            found.kind = found.kind or kind
            if found.vram is None and vram:
                found.vram, found.vram_unit = vram, "GB"
            found.save()
        device.gpu = found

    if device.type.has_screen:
        if _number(f.get("screenInches"), 5, 100):
            device.screen = round(_number(f.get("screenInches"), 5, 100), 1)
        if _tri(f.get("touch")):
            device.touch = _tri(f.get("touch"))
    battery = f.get("battery") if isinstance(f.get("battery"), dict) else {}
    health = _number(battery.get("healthPct"), 1, 150)
    cycles = _number(f.get("batteryCycles"), 1, 100_000)  # device app 0.10.0
    if device.type.has_battery and health:
        health = min(100.0, round(health))
        today = timezone.localdate()
        if device.pk and device.bat_health and (device.bat_health != health or device.bat_date != today):
            # kept in the battery history, with the cycles it had then
            device._previous_battery = (device.bat_date, device.bat_health, device.bat_cycles)
        device.bat_health, device.bat_date = health, today
    if device.type.has_battery and cycles:
        device.bat_cycles = int(cycles)

    os_info = f.get("os") if isinstance(f.get("os"), dict) else {}
    family = os_info.get("family") if os_info.get("family") in ("mac", "win", "linux") else ""
    if family:
        device.os_family = family
        device.mac_version = _item(m.MacVersion, os_info.get("version")) if family == "mac" else None
        if family != "mac":
            device.os_number = ""
        elif isinstance(os_info.get("number"), str):  # sent by the device app from 0.12.0; older ones leave it alone
            device.os_number = _os_number(os_info["number"])
        device.win_version = _item(m.WinVersion, os_info.get("version")) if family == "win" else None
        device.win_edition = _item(m.WinEdition, os_info.get("edition")) if family == "win" else None
        distro = _item(m.LinuxDistro, os_info.get("distro")) if family == "linux" else None
        device.linux_distro = distro
        device.linux_version = _item(m.LinuxVersion, os_info.get("version"), distro=distro) if distro else None
        if family != "mac":
            device.oclp = device.hackintosh = ""
            device.oclp_version = ""
        elif isinstance(f.get("oclp"), str):  # the device app reads it on Macs from 0.8.0; older ones leave it alone
            found = _text(f["oclp"], 20)
            device.oclp = "yes" if found else "no"
            device.oclp_version = "" if found in ("", "yes") else found.lstrip("vV")
    if _tri(f.get("encryption")):
        device.enc = _tri(f.get("encryption"))
    if _tri(f.get("domainJoined")):
        device.ad = _tri(f.get("domainJoined"))


def _apply_parts(device, f):
    """Drives and network cards. Details only a person can know (form factor, replaceable, Wi-Fi generation...)
    are kept from the previous record when the same drive or card is found again."""
    previous_battery = getattr(device, "_previous_battery", None)
    if previous_battery and previous_battery[1]:
        m.BatteryReading.objects.create(device=device, fecha=previous_battery[0], salud=previous_battery[1], ciclos=previous_battery[2])

    disks = [d for d in (f.get("disks") or []) if isinstance(d, dict) and _number(d.get("gb"), 0.1, 1_000_000)][:16]
    if disks:
        old = list(device.disks.all())
        device.disks.all().delete()
        unused = list(old)
        for i, d in enumerate(disks):
            gb = _number(d.get("gb"), 0.1, 1_000_000)
            size, unit = (round(gb / 1000, 2), "TB") if gb >= 1000 else (round(gb), "GB")
            # the same drive as before: one of the same size, else the one in the same place
            before = (next((o for o in unused if o.size == size and o.unit == unit), None)
                      or (old[i] if i < len(old) and old[i] in unused else None))
            if before is not None:
                unused.remove(before)
            # its own health data (device app 0.10.0); an older app sends none, and the last reading stays
            health = d.get("health") if d.get("health") in ("ok", "warning", "failing") else ""
            wear, hours = _number(d.get("wearPct"), 0, 1000), _number(d.get("hours"), 0, 10_000_000)
            reported = bool(health or wear is not None or hours)
            disk = m.Disk.objects.create(
                device=device, size=size, unit=unit,
                type=_item(m.DiskType, d.get("type")) or (before.type if before else None),
                conn=_item(m.DiskConnector, d.get("connector")) or (before.conn if before else None),
                rep=_tri(d.get("replaceable")) or (before.rep if before else ""),
                form=_item(m.DiskFormFactor, d.get("formFactor")) or (before.form if before else None),
                health=health if reported else (before.health if before else ""),
                wear=wear if reported else (before.wear if before else None),
                hours=int(hours) if reported and hours else (before.hours if before and not reported else None),
                checked=timezone.localdate() if reported else (before.checked if before else None),
            )
            # the previous reading goes to the history when the drive's health or wear changed
            if reported and before is not None and (before.health or before.wear is not None) and (before.health != disk.health or before.wear != disk.wear):
                m.DiskReading.objects.create(device=device, fecha=before.checked, drive=_drive_label(disk),
                                             health=before.health, wear=before.wear, hours=before.hours)

    nics = []
    for n in (f.get("nics") or [])[:16]:
        if not isinstance(n, dict) or n.get("type") not in ("wifi", "eth"):
            continue
        mac = _text(n.get("mac"), 17).upper().replace("-", ":")
        if not MAC_RE.match(mac) or mac == "00:00:00:00:00:00":
            continue
        nics.append((n, mac))
    if nics:
        old = {card.mac: card for card in device.nics.all()}
        device.nics.all().delete()
        for n, mac in nics:
            before = old.get(mac)
            model = (m.NicModel.objects.filter(nombre__iexact=_text(n.get("model")), type=n["type"]).first()
                     or (m.NicModel.objects.create(nombre=_text(n.get("model")), type=n["type"]) if _text(n.get("model")) else None))
            m.NetworkCard.objects.create(
                device=device, type=n["type"], mac=mac, model=model or (before.model if before else None),
                wifi_gen=(_wifi_gen(n.get("wifiGen")) if n["type"] == "wifi" else None) or (before.wifi_gen if before else None),
                bt_ver=(_bt_ver(n.get("btVer")) if n["type"] == "wifi" else None) or (before.bt_ver if before else None),
                **_nic_speed(n, before),
            )
