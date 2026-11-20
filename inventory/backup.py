"""Backups: one .invbackup file (a zip) holding every record, setting and the logo, optionally encrypted.

Layout of the file:
  manifest.json   app, format, date, whether it is encrypted (and, if not, a summary)
  data.json       every record, as {model label: [rows]}         } plain backups only;
  files/logo.*    the company logo, if there is one              } encrypted backups keep
  summary.json    who made it and how many records it holds      } these inside payload.bin
  payload.bin     encrypted backups only: 12-byte nonce + AES-256-GCM ciphertext of a zip with the files above.
                  The key comes from the password with scrypt; the manifest is authenticated with it.

Reading is defensive: at most 10 entries, only the expected names are read, each within its own size limit
(Python stops unpacking an entry at its declared size, so a zip that lies about sizes fails its CRC check),
and only the exact key-derivation settings this app writes are accepted.
"""
import base64
import binascii
import datetime as dt
import hashlib
import io
import json
import os
import zipfile
import zlib
from decimal import Decimal

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.core.management.color import no_style
from django.db import IntegrityError, connection, models as dj
from django.utils import timezone

from . import models as m

APP = "inventario"
FORMAT = 2
EXTENSION = ".invbackup"
MAX_BYTES = 50 * 1024 * 1024
MAX_ENTRIES = 10
# Largest size each file may unpack to; anything bigger is refused before it is unpacked.
LIMITS = {"manifest.json": 64 * 1024, "summary.json": 64 * 1024, "data.json": 100 * 1024 * 1024, "payload.bin": MAX_BYTES}
LOGO_LIMIT = 512 * 1024  # same as a logo uploaded in Settings
MIN_PASSWORD = 10
KDF = {"name": "scrypt", "n": 2**15, "r": 8, "p": 1}
LOGO_EXT = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp", "image/gif": "gif", "image/svg+xml": "svg"}

# Parents before children: restore inserts in this order and deletes in reverse.
MODELS = [
    m.AppSettings, m.User, m.DeviceType, m.Department, m.Location, m.DeviceModel, m.Cpu, m.Gpu,
    m.RamGeneration, m.RamFormFactor, m.DiskType, m.DiskFormFactor, m.DiskConnector, m.WifiGeneration,
    m.BluetoothVersion, m.MacVersion, m.WinVersion, m.WinEdition, m.LinuxDistro, m.LinuxVersion, m.NicModel,
    m.ProfilePhoto,  # accounts' pictures, in data.json as base64
    m.Employee, m.Employee.depts.through, m.Employee.locs.through,  # an employee's departments and offices
    m.Device, m.Disk, m.NetworkCard, m.BatteryReading, m.DiskReading, m.Assignment, m.Incident, m.AuditEvent,
]
SKIP = {(m.AppSettings, "logo")}  # stored as its own file
# Tables deliberately left out (a test checks every other table is in MODELS, so a new one cannot be forgotten):
NOT_BACKED_UP = {
    m.User.groups.through, m.User.user_permissions.through,  # Django's permission groups, which the app does not use
    m.Maintenance, m.UpdaterState, m.UpdateJob,  # the progress of the running restore or update, not inventory data
}


class BackupError(Exception):
    """`code` is an i18n key."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


# ---- export ---------------------------------------------------------------------


def _dump(value):
    if isinstance(value, (bytes, bytearray, memoryview)):  # pictures
        return base64.b64encode(bytes(value)).decode()
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    return value


def _fields(model):
    return [f for f in model._meta.concrete_fields if (model, f.attname) not in SKIP]


def _zip(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        for name, content in files.items():
            z.writestr(name, content)
    return buffer.getvalue()


def _key(password, salt, kdf=KDF):
    return hashlib.scrypt(password.encode("utf-8"), salt=salt, n=kdf["n"], r=kdf["r"], p=kdf["p"], maxmem=2**26, dklen=32)


def build(user, password=None):
    """Returns the .invbackup file's bytes."""
    data = {}
    for model in MODELS:
        fields = _fields(model)
        data[model._meta.label_lower] = [{f.attname: _dump(getattr(o, f.attname)) for f in fields} for o in model.objects.order_by("pk")]
    summary = {
        "createdBy": user.email,
        "counts": {"devices": m.Device.objects.count(), "employees": m.Employee.objects.count(),
                   "users": m.User.objects.count(), "log": m.AuditEvent.objects.count()},
    }
    files = {"data.json": json.dumps(data, ensure_ascii=False), "summary.json": json.dumps(summary)}
    settings = m.AppSettings.objects.filter(pk=1).first()
    if settings and settings.logo_type:
        files["files/logo." + LOGO_EXT.get(settings.logo_type, "bin")] = bytes(settings.logo)

    manifest = {"app": APP, "format": FORMAT, "created": timezone.now().isoformat(), "encrypted": bool(password)}
    if not password:
        manifest.update(summary)
        return _zip({"manifest.json": json.dumps(manifest), **files})
    salt = os.urandom(16)
    manifest["kdf"] = {**KDF, "salt": base64.b64encode(salt).decode()}
    manifest["cipher"] = "AES-256-GCM"
    manifest_bytes = json.dumps(manifest).encode()
    nonce = os.urandom(12)
    sealed = AESGCM(_key(password, salt)).encrypt(nonce, _zip(files), manifest_bytes)
    return _zip({"manifest.json": manifest_bytes, "payload.bin": nonce + sealed})


# ---- reading ---------------------------------------------------------------------


def _limit(name):
    return LOGO_LIMIT if name.startswith("files/logo.") else LIMITS.get(name, 0)


def _unzip(raw, allowed):
    """Reads only the expected files, each within its own limit; anything unexpected is never unpacked."""
    try:
        z = zipfile.ZipFile(io.BytesIO(raw))
        infos = z.infolist()
        if len(infos) > MAX_ENTRIES:
            raise BackupError("err_backup_invalid")
        out = {}
        for info in infos:
            if not allowed(info.filename):
                continue
            if info.file_size > _limit(info.filename):
                raise BackupError("err_backup_invalid")
            out[info.filename] = z.read(info)  # stops at the declared size, so the limit holds even if it lies
    except (zipfile.BadZipFile, zipfile.LargeZipFile, OSError, EOFError, ValueError, zlib.error):
        raise BackupError("err_backup_invalid")
    return out


def _json(files, name):
    try:
        return json.loads(files[name])
    except (KeyError, ValueError):
        raise BackupError("err_backup_invalid")


def read(raw, password=None):
    """Opens a backup. Returns (summary, data, logo bytes or None)."""
    outer = _unzip(raw, lambda n: n in ("manifest.json", "payload.bin", "data.json", "summary.json") or n.startswith("files/logo."))
    manifest = _json(outer, "manifest.json")
    if not isinstance(manifest, dict) or manifest.get("app") != APP:
        raise BackupError("err_backup_invalid")
    if manifest.get("format") != FORMAT:
        raise BackupError("err_backup_version")
    files = outer
    if manifest.get("encrypted"):
        if not password:
            raise BackupError("err_backup_password_required")
        try:
            kdf = manifest["kdf"]
            # only the settings this app writes: a tampered file must not make the server work for minutes
            if not isinstance(kdf, dict) or {k: kdf.get(k) for k in KDF} != KDF or manifest.get("cipher") != "AES-256-GCM":
                raise BackupError("err_backup_invalid")
            salt = base64.b64decode(kdf["salt"], validate=True)
            if len(salt) != 16:
                raise BackupError("err_backup_invalid")
            key = _key(password, salt)
            payload = outer["payload.bin"]
            if len(payload) < 28:  # nonce + authentication tag
                raise BackupError("err_backup_invalid")
            inner = AESGCM(key).decrypt(payload[:12], payload[12:], outer["manifest.json"])
        except InvalidTag:
            raise BackupError("err_backup_password")
        except (KeyError, TypeError, ValueError, binascii.Error):
            raise BackupError("err_backup_invalid")
        files = _unzip(inner, lambda n: n in ("data.json", "summary.json") or n.startswith("files/logo."))
    data = _json(files, "data.json")
    info = _json(files, "summary.json")
    if not isinstance(data, dict) or not isinstance(info, dict):
        raise BackupError("err_backup_invalid")
    logo = next((content for name, content in files.items() if name.startswith("files/logo.")), None)
    summary = {"created": manifest.get("created"), "encrypted": bool(manifest.get("encrypted")),
               "createdBy": info.get("createdBy"), "counts": info.get("counts") or {}}
    return summary, data, logo


# ---- backups from older versions ------------------------------------------------------
# A backup holds the data as its version stored it. Restoring one made by an older version fills in what later
# versions added, the same way their database updates did, so nothing is lost on the way.

EMPLOYEE_DEPTS, EMPLOYEE_LOCS = m.Employee.depts.through._meta.label_lower, m.Employee.locs.through._meta.label_lower


def upgrade(data):
    employees = data.get("inventory.employee", [])
    # before 1.10.0: one department and one office per employee
    if EMPLOYEE_DEPTS not in data and any(isinstance(e, dict) and "dept_id" in e for e in employees):
        rows = [e for e in employees if isinstance(e, dict)]
        data[EMPLOYEE_DEPTS] = [{"id": i + 1, "employee_id": e["id"], "department_id": e["dept_id"]}
                                for i, e in enumerate(x for x in rows if x.get("dept_id"))]
        data[EMPLOYEE_LOCS] = [{"id": i + 1, "employee_id": e["id"], "location_id": e["loc_id"]}
                               for i, e in enumerate(x for x in rows if x.get("loc_id"))]
    for e in employees:
        if isinstance(e, dict) and "contrato" not in e:  # before 1.9.0: a "temporary or intern" checkbox
            e["contrato"] = "temporal" if e.get("temporal") else ""
    for t in data.get("inventory.devicetype", []):
        if isinstance(t, dict) and "auto_apple" not in t and t.get("auto_not_mac"):  # 1.5.0: "except Macs"
            t["auto_apple"] = "except"
    users = [u for u in data.get("inventory.user", []) if isinstance(u, dict)]
    taken = {u["username"] for u in users if u.get("username")}
    for u in users:  # before 1.7.0: no usernames
        if not u.get("username"):
            u["username"] = m.suggest_username(u.get("email", ""), taken)
            taken.add(u["username"])
    for card in data.get("inventory.networkcard", []):  # 1.15.0: megabits typed as Gbps
        if isinstance(card, dict) and card.get("type") == "eth" and isinstance(card.get("speed"), (int, float)):
            if (card.get("speed_unit") == "Gbps" and card["speed"] > 100) or (card.get("speed_unit") == "Mbps" and card["speed"] >= 1000):
                card["speed"], card["speed_unit"] = round(card["speed"] / 1000, 1), "Gbps"
    return data


def _upgrade_types(data):
    """Device type codes, words and rules (1.3.0 to 1.6.0), and Intel's built-in Arc (1.15.0), for older backups.
    Runs on the restored records, with the same steps as those versions' database updates."""
    from importlib import import_module

    from django.apps import apps

    types = [t for t in data.get("inventory.devicetype", []) if isinstance(t, dict)]
    if types and "code" not in types[0]:
        import_module("inventory.migrations.0007_type_code").fill_codes(apps, None)
        import_module("inventory.migrations.0008_apple_types").add_apple_types(apps, None)
    if types and "match" not in types[0]:
        import_module("inventory.migrations.0009_type_match").fill_apple(apps, None)
    if types and "auto_chassis" not in types[0]:
        rules = import_module("inventory.migrations.0010_type_auto_rules")
        for dtype in m.DeviceType.objects.all():
            rule = rules.RULES.get(dtype.code) or ((rules.CUSTOM if dtype.uses_name else rules.PREBUILT) if dtype.code == "PC" else None)
            if rule:
                words, chassis, not_mac = rule
                dtype.match = dtype.match or words
                dtype.auto_chassis, dtype.auto_apple = chassis, "except" if not_mac else ""
                dtype.save()
    import_module("inventory.migrations.0019_fix_integrated_arc").fix(apps, None)


# ---- restore ---------------------------------------------------------------------


def _load(value, field):
    if value is None or isinstance(field, dj.JSONField):
        return value
    if isinstance(field, dj.BinaryField):
        if not isinstance(value, str):
            raise ValueError("not base64")
        try:
            return base64.b64decode(value, validate=True)
        except binascii.Error:
            raise ValueError("not base64")
    return field.to_python(value)


def _objects(data, logo):
    out = []
    for model in MODELS:
        rows = data.get(model._meta.label_lower, [])
        if not isinstance(rows, list):
            raise BackupError("err_backup_invalid")
        fields = {f.attname: f for f in _fields(model)}
        objects = []
        for row in rows:
            if not isinstance(row, dict) or row.get(model._meta.pk.attname) is None:  # "id", or a picture's "user_id"
                raise BackupError("err_backup_invalid")
            try:  # unknown keys are ignored; only real columns are written
                objects.append(model(**{k: _load(v, fields[k]) for k, v in row.items() if k in fields}))
            except (ValidationError, ValueError, TypeError):
                raise BackupError("err_backup_invalid")
        out.append((model, objects))
    plan = dict(out)
    for settings in plan[m.AppSettings]:
        settings.logo = logo if settings.logo_type and logo else None
        if not settings.logo:
            settings.logo_type = ""
    if not any(u.is_active and u.rol == m.User.Role.ADMIN for u in plan[m.User]):
        raise BackupError("err_backup_no_admin")
    return out


BATCH = 2000


def restore(raw, password=None, report=None):
    """Replaces everything. Call inside a transaction: any failure leaves the data as it was.

    `report(phase, done, total)` is told how far it has got, for the progress bar.
    """
    report = report or (lambda phase, done, total: None)
    report("reading", 0, 0)
    _, data, logo = read(raw, password)
    data = upgrade(data)
    plan = _objects(data, logo)
    total, done = sum(len(objects) for _, objects in plan), 0
    report("replacing", 0, total)
    for model in reversed(MODELS):
        model.objects.all().delete()
    try:
        for model, objects in plan:
            for start in range(0, len(objects), BATCH):
                batch = objects[start:start + BATCH]
                model.objects.bulk_create(batch)
                done += len(batch)
                report("replacing", done, total)
        report("finishing", total, total)
        connection.check_constraints()  # every reference must point at a restored record
    except (IntegrityError, ValueError):
        raise BackupError("err_backup_invalid")
    with connection.cursor() as cursor:  # new records continue after the restored ids
        for sql in connection.ops.sequence_reset_sql(no_style(), MODELS):
            cursor.execute(sql)
    _upgrade_types(data)
    Session.objects.all().delete()  # everyone signs in again against the restored accounts
