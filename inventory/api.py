"""JSON API. Every rule that matters (roles, validation, audit) is enforced here."""
import base64
import binascii
import datetime as dt
from datetime import timedelta
import contextlib
import json
import re
from decimal import Decimal, InvalidOperation
from functools import wraps

from django.conf import settings as django_settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.crypto import constant_time_compare

from . import backup as backups
from . import maintenance as maint
from . import models as m
from .catalog import load_catalog
from .models import Assignment, AuditEvent, Device, Employee, Incident, User
from .registry import LISTS
from .tags import SCOPES
from .tags import conflict as tag_conflict
from .state import (assignment_json, device_json, employee_json, full_state, incident_json, list_item_json,
                    me_json, password_policy_json, settings_json)

LOGIN_MAX_ATTEMPTS = 10
LOGIN_WINDOW_SECONDS = 15 * 60
PASSWORD_MAX_LENGTH = 128
MAC_RE = re.compile(r"^([0-9A-F]{2}:){5}[0-9A-F]{2}$")
TRI_VALUES = {"", "yes", "no"}
UNIT_VALUES = {"GHz", "MHz", "GB", "MB", "TB", "MT/s", "Mbps", "Gbps"}
INCIDENT_TYPES = {"fault", "repair", "part", "maint", "loss"}
CONDITIONS = {"good", "worn", "damaged"}
DISPOSALS = {"recycle", "sale", "donation", "lease"}
RETIRED = {Device.State.RETIRED, Device.State.LOST}


class ApiError(Exception):
    """`code` is an i18n key the interface shows in the viewer's language."""

    def __init__(self, code, status=400):
        super().__init__(code)
        self.code = code
        self.status = status


def endpoint(*methods, role="any", auth=True, allow_pending=False, form=False, during_maintenance=False, atomic=True):
    """Wraps a view: method check, maintenance, sign-in, role, JSON body, one transaction, errors."""

    def decorate(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return JsonResponse({"error": "err_invalid"}, status=405)
            user = request.user
            if not during_maintenance:
                state = maint.current()
                if state is not None:  # a restore is replacing the data: nobody else may read or change it
                    return JsonResponse({"error": "maintenance", "maintenance": maint.info(state, user)}, status=503)
            if auth and not user.is_authenticated:
                return JsonResponse({"error": "err_auth"}, status=401)
            if auth and user.must_change_password and not allow_pending:
                return JsonResponse({"error": "err_must_change"}, status=403)
            if role == "edit" and user.rol == User.Role.READ or role == "admin" and user.rol != User.Role.ADMIN:
                return JsonResponse({"error": "err_forbidden"}, status=403)
            try:
                body = request.POST if form else json.loads(request.body or b"{}")  # form: file uploads
                if not form and not isinstance(body, dict):
                    raise ValueError
            except ValueError:
                return JsonResponse({"error": "err_invalid"}, status=400)
            try:
                with transaction.atomic() if atomic else contextlib.nullcontext():
                    result = view(request, body, *args, **kwargs)
            except ApiError as e:
                return JsonResponse({"error": e.code}, status=e.status)
            except ProtectedError:
                return JsonResponse({"error": "in_use_cant"}, status=409)
            except (IntegrityError, ValidationError):
                return JsonResponse({"error": "err_invalid"}, status=400)
            if isinstance(result, HttpResponse):  # files, such as backups
                return result
            return JsonResponse(result if result is not None else {})

        return wrapper

    return decorate


# ---- input helpers -----------------------------------------------------------


def text(body, key, max_len=300, required=False, error="err_invalid"):
    value = body.get(key)
    value = "" if value is None else str(value).strip()
    if required and not value:
        raise ApiError(error)
    if len(value) > max_len:
        raise ApiError("err_invalid")
    return value


def choice(body, key, allowed):
    value = body.get(key) or ""
    if value not in allowed:
        raise ApiError("err_invalid")
    return value


def date(body, key, default=None):
    value = body.get(key)
    if not value:
        return default
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        raise ApiError("err_invalid")


def number(body, key, minimum=0, maximum=None):
    value = body.get(key)
    if value in (None, ""):
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ApiError("err_invalid")
    if value != value or value < minimum or (maximum is not None and value > maximum):
        raise ApiError("err_invalid")
    return value


def money(body, key):
    try:
        value = Decimal(str(body.get(key) or 0))
    except InvalidOperation:
        raise ApiError("err_invalid")
    if not value.is_finite() or value < 0 or value >= Decimal("10000000000"):
        raise ApiError("err_invalid")
    return value


def fk(body, key, model):
    """Resolves an id from the JSON; '' or missing means no value."""
    value = body.get(key)
    if value in (None, ""):
        return None
    try:
        return model.objects.get(pk=int(value))
    except (TypeError, ValueError, model.DoesNotExist):
        raise ApiError("err_invalid")


def get_or_404(model, pk):
    try:
        return model.objects.select_for_update().get(pk=pk)
    except model.DoesNotExist:
        raise ApiError("err_not_found", 404)


def audit(request, key, args=None, device=None):
    AuditEvent.objects.create(key=key, args=args or {}, device=device, user=request.user)


def open_assignment(device):
    return device.assignments.filter(hasta__isnull=True).first()


def append_note(existing, note, sep):
    return existing + sep + note if existing else note


# ---- session -----------------------------------------------------------------


def _throttle_key(request, email):
    ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "")).split(",")[0].strip()
    return f"login:{ip}:{email}"


@endpoint("POST", auth=False)
def session_login(request, body):
    email = text(body, "email", 254).lower()
    password = body.get("password") or ""
    key = _throttle_key(request, email)
    if cache.get(key, 0) >= LOGIN_MAX_ATTEMPTS:
        raise ApiError("login_locked", 429)
    user = authenticate(request, username=email, password=str(password))
    if user is None:
        inactive = User.objects.filter(email=email, is_active=False).first()
        if inactive and inactive.check_password(str(password)):
            raise ApiError("login_off", 403)
        cache.set(key, cache.get(key, 0) + 1, LOGIN_WINDOW_SECONDS)
        raise ApiError("login_err", 401)
    cache.delete(key)
    login(request, user)
    if user.must_change_password:  # nothing else until a new password is chosen
        return {"me": me_json(user), "settings": settings_json()}
    return {"me": me_json(user), "state": full_state(user)}


@endpoint("POST", allow_pending=True, during_maintenance=True)
def session_logout(request, body):
    logout(request)


@endpoint("GET", auth=False, during_maintenance=True)
def bootstrap(request, body):
    """What the page needs at start-up, signed in or not."""
    state = maint.current()
    if state is not None:
        me = me_json(request.user) if request.user.is_authenticated else None
        return {"me": me, "settings": settings_json(), "maintenance": maint.info(state, request.user)}
    if request.user.is_authenticated:
        if request.user.must_change_password:
            return {"me": me_json(request.user), "settings": settings_json()}
        return {"me": me_json(request.user), "state": full_state(request.user)}
    out = {"me": None, "settings": settings_json()}
    if not User.objects.exists():
        required = _setup_token_required()
        out["setup"] = {"tokenRequired": required, "blocked": required and not django_settings.SETUP_TOKEN}
    return out


@endpoint("GET")
def state(request, body):
    return {"me": me_json(request.user), "state": full_state(request.user)}


# ---- devices -----------------------------------------------------------------


def _apply_device(device, b):
    old_tag = device.tag
    device.tag = text(b, "tag", 50, required=True, error="err_required")
    device.serial = text(b, "serial", 100, required=True, error="err_required")
    device.nombre = text(b, "nombre", 100)
    device.type = fk(b, "typeId", m.DeviceType)
    device.loc = fk(b, "loc", m.Location)
    if device.type is None or device.loc is None:
        raise ApiError("err_required")
    if device.type.uses_name:
        device.model, device.custom_name = None, text(b, "customName", 200)
    else:
        device.model, device.custom_name = fk(b, "modelId", m.DeviceModel), ""
        if device.model is None:
            raise ApiError("err_model_req")

    device.cpu, device.cpu_rep = fk(b, "cpuId", m.Cpu), choice(b, "cpuRep", TRI_VALUES)
    device.ram_size, device.ram_unit = number(b, "ramSize"), choice(b, "ramUnit", UNIT_VALUES | {""}) or "GB"
    device.ram_gen = fk(b, "ramGen", m.RamGeneration)
    device.ram_speed, device.ram_speed_unit = number(b, "ramSpeed"), choice(b, "ramSpeedUnit", UNIT_VALUES | {""}) or "MT/s"
    device.ram_rep = choice(b, "ramRep", TRI_VALUES)
    replaceable = device.ram_rep == "yes"
    device.ram_modules = int(number(b, "ramModules", 1, 64) or 0) or None if replaceable else None
    device.ram_mod_size = number(b, "ramModSize") if replaceable else None
    device.ram_mod_unit = choice(b, "ramModUnit", UNIT_VALUES | {""}) or "GB"
    device.ram_form = fk(b, "ramForm", m.RamFormFactor) if replaceable else None
    device.gpu = fk(b, "gpuId", m.Gpu)

    new_health = number(b, "batHealth", 0, 100) if device.type.has_battery else None
    new_date = date(b, "batDate") if device.type.has_battery else None
    keep_reading = (
        device.pk and device.bat_health and new_health and (device.bat_health != new_health or device.bat_date != new_date)
    )
    previous = (device.bat_date, device.bat_health) if keep_reading else None
    device.bat_health, device.bat_date = new_health, new_date
    device.screen = number(b, "screen") if device.type.has_screen else None
    device.touch = choice(b, "touch", TRI_VALUES) if device.type.has_screen else ""

    family = choice(b, "osFamily", {"", "mac", "win", "linux"})
    device.os_family = family
    device.mac_version = fk(b, "osVerId", m.MacVersion) if family == "mac" else None
    device.win_version = fk(b, "osVerId", m.WinVersion) if family == "win" else None
    device.win_edition = fk(b, "osEditionId", m.WinEdition) if family == "win" else None
    device.linux_distro = fk(b, "osDistroId", m.LinuxDistro) if family == "linux" else None
    device.linux_version = fk(b, "osVerId", m.LinuxVersion) if family == "linux" else None
    if device.linux_version and device.linux_version.distro_id != getattr(device.linux_distro, "pk", None):
        raise ApiError("err_invalid")
    device.oclp = choice(b, "oclp", TRI_VALUES) if family == "mac" else ""
    device.hackintosh = choice(b, "hackintosh", TRI_VALUES) if family == "mac" else ""
    device.enc, device.ad = choice(b, "enc", TRI_VALUES), choice(b, "ad", TRI_VALUES)

    device.compra, device.precio = date(b, "compra"), money(b, "precio")
    device.proveedor, device.factura = text(b, "proveedor", 200), text(b, "factura", 100)
    device.garantia_ended = bool(b.get("garantiaEnded"))
    device.garantia = None if device.garantia_ended else date(b, "garantia")
    device.garantia_ext = choice(b, "garantiaExt", TRI_VALUES)
    device.notas = text(b, "notas", 10000)

    # the same tag, or (for a new or changed tag) the same identifier, as another device
    if (Device.objects.filter(tag=device.tag).exclude(pk=device.pk).exists()
            or (device.tag.lower() != (old_tag or "").lower() and tag_conflict(device.tag, device.pk))):
        raise ApiError("err_dup", 409)
    device.save()
    if previous:
        m.BatteryReading.objects.create(device=device, fecha=previous[0], salud=previous[1])
    _replace_children(device, b)


def _replace_children(device, b):
    disks, nics = [], []
    for k in b.get("disks") or []:
        replaceable = choice(k, "rep", TRI_VALUES)
        disks.append(m.Disk(
            device=device, size=number(k, "size"), unit=choice(k, "unit", UNIT_VALUES | {""}) or "GB",
            type=fk(k, "type", m.DiskType), rep=replaceable,
            form=fk(k, "form", m.DiskFormFactor) if replaceable == "yes" else None,
            conn=fk(k, "conn", m.DiskConnector) if replaceable == "yes" else None,
        ))
    for n in b.get("nics") or []:
        kind = choice(n, "type", {"wifi", "eth"})
        mac = text(n, "mac", 17).upper().replace("-", ":")
        if mac and not MAC_RE.match(mac):
            raise ApiError("err_mac")
        wifi = kind == "wifi"
        nics.append(m.NetworkCard(
            device=device, type=kind, model=fk(n, "modelId", m.NicModel), mac=mac,
            wifi_gen=fk(n, "wifiGen", m.WifiGeneration) if wifi else None,
            bt_ver=fk(n, "btVer", m.BluetoothVersion) if wifi else None,
            speed=None if wifi else number(n, "speed"),
            speed_unit=choice(n, "speedUnit", UNIT_VALUES | {""}) or "Gbps",
        ))
    device.disks.all().delete()
    device.nics.all().delete()
    m.Disk.objects.bulk_create(disks)
    m.NetworkCard.objects.bulk_create(nics)


@endpoint("POST", role="edit")
def device_create(request, body):
    device = Device(estado=Device.State.AVAILABLE)
    _apply_device(device, body)
    audit(request, "log_created", {"tag": device.tag}, device)
    return {"device": device_json(device)}


@endpoint("PUT", role="edit")
def device_update(request, body, pk):
    device = get_or_404(Device, pk)
    _apply_device(device, body)
    audit(request, "log_edited", {"tag": device.tag}, device)
    return {"device": device_json(device)}


@endpoint("POST", role="edit")
def device_assign(request, body, pk):
    device = get_or_404(Device, pk)
    employee = fk(body, "employeeId", Employee)
    if employee is None or employee.estado != Employee.State.ACTIVE:
        raise ApiError("err_invalid")
    if device.estado in RETIRED or open_assignment(device):
        raise ApiError("err_conflict", 409)
    location = fk(body, "loc", m.Location)
    if location is None:
        raise ApiError("err_required")
    assignment = Assignment.objects.create(
        device=device, employee=employee, desde=date(body, "desde", timezone.localdate()), notas=text(body, "notas", 1000)
    )
    if device.estado != Device.State.REPAIR:
        device.estado = Device.State.IN_USE
    device.loc = location
    device.save()
    audit(request, "log_assigned", {"tag": device.tag, "name": employee.nombre}, device)
    return {"assignment": assignment_json(assignment)}


@endpoint("POST", role="edit")
def device_return(request, body, pk):
    device = get_or_404(Device, pk)
    assignment = open_assignment(device)
    if assignment is None:
        raise ApiError("err_conflict", 409)
    next_state = choice(body, "next", {Device.State.AVAILABLE, Device.State.REPAIR, Device.State.RETIRED})
    if not next_state:
        raise ApiError("err_invalid")
    assignment.hasta = date(body, "hasta", timezone.localdate())
    if assignment.hasta < assignment.desde:
        raise ApiError("err_dates")
    assignment.condicion = choice(body, "condicion", CONDITIONS)
    note = text(body, "notas", 1000)
    if note:
        assignment.notas = append_note(assignment.notas, note, ". ")
    assignment.save()
    device.estado = next_state
    storage = m.Location.objects.filter(tipo="storage").first()
    if storage:
        device.loc = storage
    device.save()
    audit(request, "log_returned",
          {"name": assignment.employee.nombre, "tag": device.tag, "cond": assignment.condicion}, device)


@endpoint("POST", role="edit")
def device_incident(request, body, pk):
    device = get_or_404(Device, pk)
    description = text(body, "descripcion", 5000, required=True, error="err_desc")
    tipo = choice(body, "tipo", INCIDENT_TYPES)
    if not tipo:
        raise ApiError("err_invalid")
    incident = Incident.objects.create(
        device=device, fecha=date(body, "fecha", timezone.localdate()), tipo=tipo, descripcion=description,
        piezas=text(body, "piezas"), coste=money(body, "coste"), proveedor=text(body, "proveedor", 200),
    )
    to_repair = bool(body.get("rep"))
    if to_repair:
        device.estado = Device.State.REPAIR
        device.save()
    audit(request, "log_repair" if to_repair else "log_incident", {"tag": device.tag, "desc": description}, device)
    return {"incident": incident_json(incident)}


@endpoint("POST", role="edit")
def incident_resolve(request, body, pk):
    incident = get_or_404(Incident, pk)
    if incident.estado != "abierta":
        raise ApiError("err_conflict", 409)
    incident.estado = "resuelta"
    incident.resuelta = date(body, "resuelta", timezone.localdate())
    incident.coste = money(body, "coste")
    incident.piezas = text(body, "piezas")
    incident.save()
    device = Device.objects.select_for_update().get(pk=incident.device_id)
    still_open = device.incidents.filter(estado="abierta").exists()
    if device.estado == Device.State.REPAIR and not still_open:
        device.estado = Device.State.IN_USE if open_assignment(device) else Device.State.AVAILABLE
        device.save()
    audit(request, "log_resolved", {"tag": device.tag}, device)


@endpoint("POST", role="edit")
def device_status(request, body, pk):
    device = get_or_404(Device, pk)
    new_state = body.get("estado")
    if new_state not in Device.State.values or new_state == device.estado:
        raise ApiError("err_invalid")
    assignment = open_assignment(device)
    if new_state == Device.State.IN_USE and assignment is None:
        raise ApiError("err_conflict", 409)
    if assignment and new_state in {Device.State.AVAILABLE, Device.State.RETIRED, Device.State.LOST}:
        assignment.hasta = timezone.localdate()
        assignment.save()
    device.estado = new_state
    if new_state == Device.State.RETIRED:
        device.destino = choice(body, "metodo", DISPOSALS)
        device.wipe_cert = text(body, "cert", 100)
    reason = text(body, "motivo", 2000)
    note = " ".join(x for x in (text(body, "note", 500), reason) if x)
    if note:
        device.notas = append_note(device.notas, note, "\n")
    device.save()
    audit(request, "log_status", {"tag": device.tag, "st": new_state, "reason": reason}, device)


# ---- employees ---------------------------------------------------------------


def _apply_employee(employee, b):
    employee.nombre = text(b, "nombre", 200, required=True, error="err_person")
    employee.email = text(b, "email", 254, required=True, error="err_person")
    try:
        validate_email(employee.email)
    except ValidationError:
        raise ApiError("err_person")
    employee.dept, employee.loc = fk(b, "dept", m.Department), fk(b, "loc", m.Location)
    employee.alta = date(b, "alta", timezone.localdate())
    employee.save()


@endpoint("POST", role="edit")
def employee_create(request, body):
    employee = Employee()
    _apply_employee(employee, body)
    return {"employee": employee_json(employee)}


@endpoint("PUT", role="edit")
def employee_update(request, body, pk):
    employee = get_or_404(Employee, pk)
    _apply_employee(employee, body)
    return {"employee": employee_json(employee)}


@endpoint("POST", role="edit")
def employee_status(request, body, pk):
    employee = get_or_404(Employee, pk)
    new_state = body.get("estado")
    if new_state not in Employee.State.values:
        raise ApiError("err_invalid")
    before = employee.estado
    employee.estado = new_state
    active = new_state == Employee.State.ACTIVE
    employee.estado_fecha = None if active else date(body, "fecha", timezone.localdate())
    employee.save()
    if before != new_state:
        held = list(employee.assignments.filter(hasta__isnull=True).select_related("device"))
        left = new_state == Employee.State.LEFT
        key = "log_left" if left else "log_onleave" if new_state == Employee.State.LEAVE else "log_back"
        args = {"name": employee.nombre, "tags": ", ".join(a.device.tag for a in held) if left else ""}
        audit(request, key, args, held[0].device if held else None)


# ---- settings (administrators) -------------------------------------------------


def _apply_settings(s, body):
    s.org_name = text(body, "orgName", 200) or s.org_name
    s.tag_prefix = text(body, "tagPrefix", 20)
    s.tag_numbering = body.get("tagNumbering") or s.tag_numbering or "type"
    if s.tag_numbering not in SCOPES:
        raise ApiError("err_invalid")
    s.date_fmt = choice(body, "dateFmt", {"dmy", "mdy", "ymd", "dmydot"})
    s.currency = choice(body, "currency", {"EUR", "USD", "GBP", "CHF", "MXN", "COP", "ARS", "CLP"})
    s.warranty_days = int(number(body, "warrantyDays", 0, 3650) or 0)
    s.hostname_is_tag = bool(body.get("hostnameIsTag"))
    s.save()


@endpoint("PUT", role="admin")
def settings_update(request, body):
    s = m.AppSettings.load()
    _apply_settings(s, body)
    audit(request, "log_setting", {"xKey": "set_region"})
    return {"settings": settings_json(s)}


def _apply_password_policy(s, p):
    if not isinstance(p, dict):
        raise ApiError("err_invalid")
    s.pw_enforce, s.pw_min_enabled = bool(p.get("enforce")), bool(p.get("minOn"))
    s.pw_upper, s.pw_number, s.pw_symbol = bool(p.get("upper")), bool(p.get("number")), bool(p.get("symbol"))
    if s.pw_min_enabled:
        length = number(p, "minLen", 1, PASSWORD_MAX_LENGTH)
        if length is None or length != int(length):
            raise ApiError("err_pw_minlen")
        s.pw_min_length = int(length)
    s.save()


def _password_allowed(password, s):
    if not password or len(password) > PASSWORD_MAX_LENGTH:
        return False
    if not s.pw_enforce:
        return True
    return not (
        (s.pw_min_enabled and len(password) < s.pw_min_length)
        or (s.pw_upper and not any(c.isupper() for c in password))
        or (s.pw_number and not any(c.isdecimal() for c in password))
        or (s.pw_symbol and not any(not c.isalnum() and not c.isspace() for c in password))
    )


@endpoint("PUT", role="admin")
def password_policy_update(request, body):
    s = m.AppSettings.load()
    _apply_password_policy(s, body)
    audit(request, "log_setting", {"xKey": "set_pwpolicy"})
    return {"pwPolicy": password_policy_json(s)}


def _spec(coll):
    if coll not in LISTS:
        raise ApiError("err_not_found", 404)
    return LISTS[coll]


def _apply_item(spec, item, b):
    if spec.translated:
        name = b.get("nombre")
        if not isinstance(name, dict) or not str(name.get("es") or "").strip():
            raise ApiError("err_name")
        item.nombre = {lang: str(name.get(lang) or "").strip()[:200] for lang in ("es", "en", "ca")}
    else:
        item.nombre = text(b, "nombre", 200, required=True, error="err_name")
    for key, attr in spec.fields.items():
        field = spec.model._meta.get_field(attr)
        if field.get_internal_type() == "BooleanField":
            setattr(item, attr, bool(b.get(key)))
        elif field.get_internal_type() in ("FloatField", "PositiveIntegerField"):
            value = number(b, key)
            setattr(item, attr, int(value) if value is not None and field.get_internal_type() != "FloatField" else value)
        else:
            value = text(b, key, field.max_length)
            setattr(item, attr, value or field.get_default())
    for key, (attr, target) in spec.fks.items():
        related = fk(b, key, target)
        if related is None:
            raise ApiError("err_name")
        setattr(item, attr, related)
    item.save()


@endpoint("POST", role="edit")  # technicians add entries from the + buttons in forms
def list_create(request, body, coll):
    spec = _spec(coll)
    item = spec.model()
    _apply_item(spec, item, body)
    audit(request, "log_setting", {"xKey": spec.title})
    return {"item": list_item_json(spec, item)}


@endpoint("PUT", "DELETE", role="admin")
def list_item(request, body, coll, pk):
    spec = _spec(coll)
    item = get_or_404(spec.model, pk)
    if request.method == "DELETE":
        item.delete()
        audit(request, "log_setting", {"xKey": spec.title})
        return None
    _apply_item(spec, item, body)
    audit(request, "log_setting", {"xKey": spec.title})
    return {"item": list_item_json(spec, item)}


def _active_admins():
    return User.objects.filter(is_active=True, rol=User.Role.ADMIN).count()


def _apply_user(request, user, b):
    was_active_admin = bool(user.pk) and user.is_active and user.rol == User.Role.ADMIN
    user.nombre = text(b, "nombre", 200, required=True, error="err_user")
    user.email = text(b, "email", 254, required=True, error="err_user").lower()
    try:
        validate_email(user.email)
    except ValidationError:
        raise ApiError("err_user")
    if User.objects.filter(email=user.email).exclude(pk=user.pk).exists():
        raise ApiError("err_email_dup", 409)
    if b.get("rol") not in User.Role.values:
        raise ApiError("err_invalid")
    if was_active_admin and b["rol"] != User.Role.ADMIN and _active_admins() == 1:
        raise ApiError("err_last_admin", 409)
    user.rol = b["rol"]
    if user.pk != request.user.pk:  # you cannot lock yourself into a password change
        user.must_change_password = bool(b.get("mustChange"))
    password = str(b.get("pass") or "")
    if not user.pk and not password:
        raise ApiError("err_pass")
    if password:
        if not _password_allowed(password, m.AppSettings.load()):
            raise ApiError("err_pass_weak")
        user.set_password(password)
    user.save()
    if password and user.pk == request.user.pk:
        update_session_auth_hash(request, user)  # changing your own password keeps you signed in
    audit(request, "log_setting", {"xKey": "set_users"})


@endpoint("POST", role="admin")
def user_create(request, body):
    _apply_user(request, User(), body)


@endpoint("PUT", role="admin")
def user_update(request, body, pk):
    _apply_user(request, get_or_404(User, pk), body)


@endpoint("POST", role="admin")
def user_toggle(request, body, pk):
    user = get_or_404(User, pk)
    if user.pk == request.user.pk:
        raise ApiError("err_self", 409)
    if user.is_active and user.rol == User.Role.ADMIN and _active_admins() == 1:
        raise ApiError("err_last_admin", 409)
    user.is_active = not user.is_active
    user.save()
    audit(request, "log_setting", {"xKey": "set_users"})
    return {"activo": user.is_active}


# ---- first-run setup ----------------------------------------------------------


def _setup_token_required():
    return not django_settings.DEBUG or bool(django_settings.SETUP_TOKEN)


def _translated_name(value, error):
    """Accepts one name for every language, or {es, en, ca}."""
    if isinstance(value, dict):
        spanish = str(value.get("es") or "").strip()
        names = {lang: str(value.get(lang) or spanish).strip()[:200] for lang in ("es", "en", "ca")}
    else:
        spanish = str(value or "").strip()
        names = {lang: spanish[:200] for lang in ("es", "en", "ca")}
    if not spanish:
        raise ApiError(error)
    return names


@endpoint("POST", auth=False)
def setup(request, body):
    """Creates the organisation and first administrator. Works once, on an empty install."""
    m.AppSettings.load()
    settings_row = m.AppSettings.objects.select_for_update().get(pk=1)  # two people cannot finish at once
    if User.objects.exists():
        raise ApiError("err_setup_done", 409)

    if _setup_token_required():
        key = _throttle_key(request, "setup")
        if cache.get(key, 0) >= LOGIN_MAX_ATTEMPTS:
            raise ApiError("login_locked", 429)
        expected = django_settings.SETUP_TOKEN
        if not expected or not constant_time_compare(str(body.get("token") or ""), expected):
            cache.set(key, cache.get(key, 0) + 1, LOGIN_WINDOW_SECONDS)
            raise ApiError("err_setup_token", 403)

    if not text(body, "orgName", 200):
        raise ApiError("err_su_org")
    _apply_settings(settings_row, body)
    if "pwPolicy" in body:
        _apply_password_policy(settings_row, body["pwPolicy"])

    locations = body.get("locations") or []
    if not isinstance(locations, list) or not locations:
        raise ApiError("err_su_loc")
    for row in locations:
        tipo = row.get("tipo") if isinstance(row, dict) else None
        if tipo not in {"office", "remote", "storage"}:
            raise ApiError("err_invalid")
        m.Location.objects.create(nombre=_translated_name(row.get("nombre"), "err_su_loc"), tipo=tipo)
    for name in body.get("depts") or []:
        m.Department.objects.create(nombre=_translated_name(name, "err_name"))
    load_catalog()

    admin = body.get("admin")
    if not isinstance(admin, dict):
        raise ApiError("err_su_admin")
    nombre = text(admin, "nombre", 200, required=True, error="err_su_admin")
    email = text(admin, "email", 254, required=True, error="err_su_admin").lower()
    password = str(admin.get("pass") or "")
    try:
        validate_email(email)
    except ValidationError:
        raise ApiError("err_su_admin")
    if not password:
        raise ApiError("err_pass")
    if not _password_allowed(password, settings_row):
        raise ApiError("err_pass_weak")
    user = User.objects.create_user(email, password, nombre=nombre, rol=User.Role.ADMIN)
    AuditEvent.objects.create(key="log_setup", args={}, user=user)
    login(request, user)
    return {"me": me_json(user), "state": full_state(user)}


# ---- own account ---------------------------------------------------------------


@endpoint("POST", allow_pending=True)
def account_password(request, body):
    """Changes your own password; also how a required change is completed."""
    user = request.user
    key = _throttle_key(request, "pw:" + user.email)
    if cache.get(key, 0) >= LOGIN_MAX_ATTEMPTS:
        raise ApiError("login_locked", 429)
    current, new = str(body.get("current") or ""), str(body.get("new") or "")
    if not user.check_password(current):
        cache.set(key, cache.get(key, 0) + 1, LOGIN_WINDOW_SECONDS)
        raise ApiError("err_pw_current", 403)
    if not new:
        raise ApiError("err_pass")
    if new == current:
        raise ApiError("err_pw_same")
    if not _password_allowed(new, m.AppSettings.load()):
        raise ApiError("err_pass_weak")
    user.set_password(new)
    user.must_change_password = False
    user.save()
    update_session_auth_hash(request, user)
    cache.delete(key)
    audit(request, "log_pwchanged", {"name": user.nombre})
    return {"me": me_json(user), "state": full_state(user)}


# ---- company logo ----------------------------------------------------------------

LOGO_MAX_BYTES = 512 * 1024
LOGO_DATA_URL = re.compile(r"^data:(image/(?:png|jpeg|webp|gif|svg\+xml));base64,([A-Za-z0-9+/=\s]+)$")


def _logo_matches(kind, data):
    """Checks the file really is the image type it claims to be."""
    if kind == "image/png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    if kind == "image/jpeg":
        return data.startswith(b"\xff\xd8\xff")
    if kind == "image/gif":
        return data[:6] in (b"GIF87a", b"GIF89a")
    if kind == "image/webp":
        return data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    try:
        return "<svg" in data.decode("utf-8")
    except UnicodeDecodeError:
        return False


@endpoint("PUT", "DELETE", role="admin")
def logo_update(request, body):
    s = m.AppSettings.load()
    if request.method == "DELETE":
        s.logo, s.logo_type = None, ""
    else:
        match = LOGO_DATA_URL.match(str(body.get("data") or ""))
        if not match:
            raise ApiError("err_logo_type")
        try:
            data = base64.b64decode("".join(match.group(2).split()), validate=True)
        except (binascii.Error, ValueError):
            raise ApiError("err_logo_type")
        if len(data) > LOGO_MAX_BYTES:
            raise ApiError("err_logo_size")
        if not _logo_matches(match.group(1), data):
            raise ApiError("err_logo_type")
        s.logo, s.logo_type = data, match.group(1)
    s.logo_version += 1
    s.save()
    audit(request, "log_setting", {"xKey": "set_brand"})
    return {"logo": s.logo_version if s.logo_type else 0}


# ---- backups ----------------------------------------------------------------------


@endpoint("POST", role="admin")
def backup_export(request, body):
    password = str(body.get("password") or "")
    if password and len(password) < backups.MIN_PASSWORD:
        raise ApiError("err_bk_pw_short")
    audit(request, "log_backup_export")
    content = backups.build(request.user, password or None)
    response = HttpResponse(content, content_type="application/octet-stream")
    name = f"inventario-copia-{timezone.localdate().isoformat()}{backups.EXTENSION}"
    response["Content-Disposition"] = f'attachment; filename="{name}"'
    return response


def _uploaded_backup(request):
    upload = request.FILES.get("file")
    if upload is None:
        raise ApiError("err_backup_invalid")
    if upload.size > backups.MAX_BYTES:
        raise ApiError("err_backup_size", 413)
    return upload.read(), str(request.POST.get("password") or "") or None


@endpoint("POST", role="admin", form=True)
def backup_inspect(request, body):
    """Opens a backup without changing anything, so the person can see what it holds first."""
    raw, password = _uploaded_backup(request)
    try:
        summary, _, _ = backups.read(raw, password)
    except backups.BackupError as e:
        raise ApiError(e.code)
    return {"summary": summary}


@endpoint("POST", role="admin", form=True, atomic=False)
def backup_restore(request, body):
    """Replaces all data with the backup's and signs everyone out, including you.

    While it runs the app is in maintenance: other administrators follow the progress, everyone else waits.
    """
    raw, password = _uploaded_backup(request)
    email = request.user.email
    if not maint.claim("restore", request.user):
        raise ApiError("err_maintenance_busy", 409)
    try:
        with transaction.atomic():
            backups.restore(raw, password, report=maint.Reporter())
            AuditEvent.objects.create(key="log_backup_restore", args={}, user=User.objects.filter(email=email).first())
    except backups.BackupError as e:
        raise ApiError(e.code)
    finally:
        maint.release()  # only after the new data is committed, so nobody sees it half-done
    logout(request)


@endpoint("GET", auth=False, during_maintenance=True)
def maintenance_status(request, body):
    state = maint.current()
    return {"active": False} if state is None else {"active": True, **maint.info(state, request.user)}


# ---- about and updates ---------------------------------------------------------------


@endpoint("GET", role="admin")
def about(request, body):
    import platform

    import django
    from django.conf import settings
    from django.db import connection

    from . import updates
    from .version import VERSION, commit

    with connection.cursor() as cursor:
        cursor.execute("SELECT current_setting('server_version'), pg_database_size(current_database())")
        postgres, size = cursor.fetchone()
    first = AuditEvent.objects.order_by("at").values_list("at", flat=True).first()
    return {
        "version": VERSION, "commit": commit()[:12], "environment": "development" if settings.DEBUG else "production",
        "since": first.date().isoformat() if first else None, "timeZone": settings.TIME_ZONE,
        "counts": {"devices": m.Device.objects.count(), "employees": m.Employee.objects.count(),
                   "users": User.objects.count(), "log": AuditEvent.objects.count()},
        "dbSize": size,
        "tech": {"python": platform.python_version(), "django": django.get_version(), "postgres": postgres.split(" ")[0]},
        "updates": {"repo": settings.UPDATE_REPO, "access": updates.access(), "last": updates.cached()},
    }


@endpoint("POST", role="admin")
def check_updates(request, body):
    from . import updates

    return updates.check()


# ---- installing updates (with the updater service, see deploy/updater) -------------------

UPDATER_ALIVE = timedelta(seconds=60)


def _updater():
    """The updater's state, if it has reported in the last minute; otherwise None (not installed or stopped)."""
    state = m.UpdaterState.objects.filter(pk=1).first()
    if state is None or state.last_seen is None or timezone.now() - state.last_seen > UPDATER_ALIVE:
        return None
    return state


def _job_json(job):
    return {"id": job.id, "createdAt": job.created_at.isoformat(), "by": job.requested_by, "automatic": job.automatic,
            "from": job.from_version, "target": job.target, "status": job.status, "phase": job.phase, "message": job.message,
            "finishedAt": job.finished_at.isoformat() if job.finished_at else None}


@endpoint("GET", role="admin")
def updates_status(request, body):
    from .version import VERSION, commit

    s = m.AppSettings.load()
    state = _updater()
    out = {"installed": VERSION, "commit": commit()[:12], "auto": {"enabled": s.auto_update, "hour": s.auto_update_hour},
           "jobs": [_job_json(j) for j in m.UpdateJob.objects.all()[:10]], "updater": None}
    if state is not None:
        from .updates import as_installed

        out["updater"] = as_installed({
            "status": state.check_status, "checkedAt": state.checked_at.isoformat() if state.checked_at else None,
            "checkRequested": state.check_requested, "latest": state.latest_tag, "name": state.latest_name,
            "notes": state.latest_notes, "url": state.latest_url,
            "published": state.latest_published.isoformat() if state.latest_published else None,
        })
    return out


@endpoint("POST", role="admin")
def updates_check(request, body):
    """Asks the updater to check GitHub now; without an updater, the app checks by itself."""
    from . import updates

    if _updater() is None:
        return {"result": updates.check()}
    m.UpdaterState.objects.filter(pk=1).update(check_requested=True)
    return {"requested": True}


@endpoint("POST", role="admin")
def updates_install(request, body):
    """Queues the latest release for the updater. Only the release the updater found on GitHub can be chosen."""
    from .updates import parse
    from .version import VERSION

    state = _updater()
    if state is None:
        raise ApiError("err_no_updater", 409)
    tag = text(body, "tag", 40)
    if not tag or tag != state.latest_tag or parse(tag) <= parse(VERSION):
        raise ApiError("err_update_stale", 409)
    if m.UpdateJob.objects.filter(status__in=["queued", "running"]).exists() or maint.current() is not None:
        raise ApiError("err_update_busy", 409)
    job = m.UpdateJob.objects.create(requested_by=request.user.nombre, from_version=VERSION, target=tag)
    audit(request, "log_update_requested", {"v": tag})
    return {"job": _job_json(job)}


@endpoint("PUT", role="admin")
def updates_auto(request, body):
    s = m.AppSettings.load()
    hour = number(body, "hour", 0, 23)
    if hour is None or hour != int(hour):
        raise ApiError("err_invalid")
    s.auto_update, s.auto_update_hour = bool(body.get("enabled")), int(hour)
    s.save()
    audit(request, "log_setting", {"xKey": "set_updates"})
    return {"auto": {"enabled": s.auto_update, "hour": s.auto_update_hour}}
