"""JSON API. Every rule that matters (roles, validation, audit) is enforced here."""
import datetime as dt
import json
import re
from decimal import Decimal, InvalidOperation
from functools import wraps

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.utils import timezone

from . import models as m
from .models import Assignment, AuditEvent, Device, Employee, Incident, User
from .registry import LISTS
from .state import (assignment_json, device_json, employee_json, full_state, incident_json, list_item_json,
                    me_json, settings_json)

LOGIN_MAX_ATTEMPTS = 10
LOGIN_WINDOW_SECONDS = 15 * 60
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


def endpoint(*methods, role="any", auth=True):
    """Wraps a view: method check, sign-in, role, JSON body, one transaction, errors."""

    def decorate(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return JsonResponse({"error": "err_invalid"}, status=405)
            user = request.user
            if auth and not user.is_authenticated:
                return JsonResponse({"error": "err_auth"}, status=401)
            if role == "edit" and user.rol == User.Role.READ or role == "admin" and user.rol != User.Role.ADMIN:
                return JsonResponse({"error": "err_forbidden"}, status=403)
            try:
                body = json.loads(request.body or b"{}")
                if not isinstance(body, dict):
                    raise ValueError
            except ValueError:
                return JsonResponse({"error": "err_invalid"}, status=400)
            try:
                with transaction.atomic():
                    result = view(request, body, *args, **kwargs)
            except ApiError as e:
                return JsonResponse({"error": e.code}, status=e.status)
            except ProtectedError:
                return JsonResponse({"error": "in_use_cant"}, status=409)
            except (IntegrityError, ValidationError):
                return JsonResponse({"error": "err_invalid"}, status=400)
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
    return {"me": me_json(user), "state": full_state(user)}


@endpoint("POST")
def session_logout(request, body):
    logout(request)


@endpoint("GET", auth=False)
def bootstrap(request, body):
    """What the page needs at start-up, signed in or not."""
    if request.user.is_authenticated:
        return {"me": me_json(request.user), "state": full_state(request.user)}
    return {"me": None, "settings": settings_json()}


@endpoint("GET")
def state(request, body):
    return {"me": me_json(request.user), "state": full_state(request.user)}


# ---- devices -----------------------------------------------------------------


def _apply_device(device, b):
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

    duplicate = Device.objects.filter(tag=device.tag).exclude(pk=device.pk).exists()
    if duplicate:
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


@endpoint("PUT", role="admin")
def settings_update(request, body):
    s = m.AppSettings.load()
    s.org_name = text(body, "orgName", 200) or s.org_name
    s.tag_prefix = text(body, "tagPrefix", 20)
    s.date_fmt = choice(body, "dateFmt", {"dmy", "mdy", "ymd", "dmydot"})
    s.currency = choice(body, "currency", {"EUR", "USD", "GBP", "CHF", "MXN", "COP", "ARS", "CLP"})
    s.warranty_days = int(number(body, "warrantyDays", 0, 3650) or 0)
    s.hostname_is_tag = bool(body.get("hostnameIsTag"))
    s.save()
    audit(request, "log_setting", {"xKey": "set_region"})
    return {"settings": settings_json(s)}


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
    password = str(b.get("pass") or "")
    if not user.pk and not password:
        raise ApiError("err_pass")
    if password:
        try:
            validate_password(password, user)
        except ValidationError:
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
