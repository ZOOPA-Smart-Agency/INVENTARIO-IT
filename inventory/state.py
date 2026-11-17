"""Builds the JSON snapshot the interface renders from."""
from .models import AppSettings, Assignment, AuditEvent, Device, Employee, Incident, User
from .registry import LISTS


def sid(value):
    """Ids are strings in the JSON; empty foreign keys are ''."""
    return "" if value is None else str(value)


def iso(value, empty=""):
    return value.isoformat() if value else empty


def settings_json(s=None):
    s = s or AppSettings.objects.defer("logo").filter(pk=1).first() or AppSettings.load()
    return {
        "logo": s.logo_version if s.logo_type else 0,
        "orgName": s.org_name,
        "tagPrefix": s.tag_prefix,
        "tagNumbering": s.tag_numbering,
        "dateFmt": s.date_fmt,
        "currency": s.currency,
        "warrantyDays": s.warranty_days,
        "hostnameIsTag": s.hostname_is_tag,
    }


def password_policy_json(s=None):
    s = s or AppSettings.load()
    return {
        "enforce": s.pw_enforce, "minOn": s.pw_min_enabled, "minLen": s.pw_min_length,
        "upper": s.pw_upper, "number": s.pw_number, "symbol": s.pw_symbol,
    }


def list_item_json(spec, obj):
    out = {"id": str(obj.pk), "nombre": obj.nombre}
    for key, attr in spec.fields.items():
        out[key] = getattr(obj, attr)
    for key, (attr, _) in spec.fks.items():
        out[key] = sid(getattr(obj, attr + "_id"))
    return out


def user_json(u, full):
    out = {"id": str(u.pk), "nombre": u.nombre, "rol": u.rol, "activo": u.is_active}
    if full:  # addresses and sign-in dates are only for administrators
        out.update(email=u.email, username=u.username or "", last=iso(u.last_login.date() if u.last_login else None, None), mustChange=u.must_change_password)
    return out


def me_json(u):
    out = {"id": str(u.pk), "nombre": u.nombre, "rol": u.rol, "email": u.email, "username": u.username or "", "activo": u.is_active,
           "mustChange": u.must_change_password}
    if u.must_change_password:  # the change-password screen shows the rules
        out["pwPolicy"] = password_policy_json()
    return out


def employee_json(e):
    return {
        "id": str(e.pk),
        "nombre": e.nombre,
        "email": e.email,
        "depts": sorted((str(x.pk) for x in e.depts.all()), key=int),
        "locs": sorted((str(x.pk) for x in e.locs.all()), key=int),
        "alta": iso(e.alta),
        "estado": e.estado,
        "estadoFecha": iso(e.estado_fecha, None),
        "contrato": e.contrato,
    }


def device_json(d):
    os_version = {"mac": d.mac_version_id, "win": d.win_version_id, "linux": d.linux_version_id}.get(d.os_family)
    return {
        "id": str(d.pk), "tag": d.tag, "nombre": d.nombre, "serial": d.serial,
        "typeId": sid(d.type_id), "modelId": sid(d.model_id), "customName": d.custom_name,
        "estado": d.estado, "loc": sid(d.loc_id),
        "compra": iso(d.compra), "precio": float(d.precio), "proveedor": d.proveedor, "factura": d.factura,
        "garantia": iso(d.garantia), "garantiaExt": d.garantia_ext, "garantiaEnded": d.garantia_ended,
        "destino": d.destino, "wipeCert": d.wipe_cert, "notas": d.notas,
        "cpuId": sid(d.cpu_id), "cpuRep": d.cpu_rep,
        "ramSize": d.ram_size, "ramUnit": d.ram_unit, "ramGen": sid(d.ram_gen_id),
        "ramSpeed": d.ram_speed, "ramSpeedUnit": d.ram_speed_unit, "ramRep": d.ram_rep,
        "ramModules": d.ram_modules, "ramModSize": d.ram_mod_size, "ramModUnit": d.ram_mod_unit,
        "ramForm": sid(d.ram_form_id), "gpuId": sid(d.gpu_id),
        "screen": d.screen, "touch": d.touch, "batHealth": d.bat_health, "batDate": iso(d.bat_date),
        "batLog": [{"fecha": iso(r.fecha), "salud": r.salud} for r in d.battery_readings.all()],
        "osFamily": d.os_family, "osVerId": sid(os_version), "osVersion": "",
        "osEditionId": sid(d.win_edition_id), "osDistroId": sid(d.linux_distro_id),
        "oclp": d.oclp, "oclpVersion": d.oclp_version, "hackintosh": d.hackintosh, "enc": d.enc, "ad": d.ad,
        "disks": [
            {"size": k.size, "unit": k.unit, "type": sid(k.type_id), "rep": k.rep, "form": sid(k.form_id), "conn": sid(k.conn_id)}
            for k in d.disks.all()
        ],
        "nics": [
            {"type": n.type, "modelId": sid(n.model_id), "mac": n.mac, "wifiGen": sid(n.wifi_gen_id),
             "btVer": sid(n.bt_ver_id), "speed": n.speed, "speedUnit": n.speed_unit}
            for n in d.nics.all()
        ],
    }


def assignment_json(a):
    return {
        "id": str(a.pk), "deviceId": str(a.device_id), "employeeId": str(a.employee_id),
        "desde": iso(a.desde), "hasta": iso(a.hasta, None), "notas": a.notas, "condicion": a.condicion,
    }


def incident_json(i):
    return {
        "id": str(i.pk), "deviceId": str(i.device_id), "fecha": iso(i.fecha), "tipo": i.tipo,
        "descripcion": i.descripcion, "estado": i.estado, "resuelta": iso(i.resuelta, None),
        "piezas": i.piezas, "coste": float(i.coste), "proveedor": i.proveedor,
    }


def log_json(e):
    return {
        "fecha": e.at.date().isoformat(), "k": e.key, "a": e.args,
        "deviceId": sid(e.device_id) or None, "by": sid(e.user_id) or None,
    }


def full_state(user):
    state = {"settings": settings_json()}
    for coll, spec in LISTS.items():
        state[coll] = [list_item_json(spec, o) for o in spec.model.objects.all()]
    is_admin = user.rol == User.Role.ADMIN
    if is_admin:  # only administrators set passwords
        state["settings"]["pwPolicy"] = password_policy_json()
    state["users"] = [user_json(u, is_admin) for u in User.objects.order_by("id")]
    state["employees"] = [employee_json(e) for e in Employee.objects.prefetch_related("depts", "locs")]
    devices = Device.objects.prefetch_related("disks", "nics", "battery_readings")
    state["devices"] = [device_json(d) for d in devices]
    state["assignments"] = [assignment_json(a) for a in Assignment.objects.all()]
    state["incidents"] = [incident_json(i) for i in Incident.objects.all()]
    state["log"] = [log_json(e) for e in AuditEvent.objects.all()[:500]]
    return state
