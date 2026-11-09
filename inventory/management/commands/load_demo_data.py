"""Loads example data, or only the standard catalogue lists with --catalog-only."""
import datetime as dt
import json
from pathlib import Path

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from inventory import models as m
from inventory.registry import LISTS

SEED = Path(__file__).resolve().parents[2] / "demo" / "seed.json"
CATALOG_ONLY_SKIP = {"depts", "locations", "models"}


def plain(value):
    """Example free text comes as {es, en, ca}; real records hold plain text."""
    return value.get("es", "") if isinstance(value, dict) else (value or "")


def day(value):
    return dt.date.fromisoformat(value) if value else None


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument("--password", help="Password for the example accounts (required unless --catalog-only).")
        parser.add_argument("--catalog-only", action="store_true", help="Only device types, components and software lists.")

    @transaction.atomic
    def handle(self, *args, **opts):
        data = json.loads(SEED.read_text(encoding="utf8"))
        ids = {}
        for coll, spec in LISTS.items():
            if opts["catalog_only"] and coll in CATALOG_ONLY_SKIP:
                continue
            if spec.model.objects.exists():
                raise CommandError(f"{coll} already has data; this command only fills an empty database.")
            ids[coll] = {}
            for row in data[coll]:
                item = spec.model(nombre=row["nombre"])
                for key, attr in spec.fields.items():
                    if key in row and row[key] is not None:
                        value = row[key]
                        setattr(item, attr, plain(value) if isinstance(value, dict) else value)
                for key, (attr, target) in spec.fks.items():
                    parent = next(c for c, s in LISTS.items() if s.model is target)
                    setattr(item, attr + "_id", ids[parent][row[key]])
                item.save()
                ids[coll][row["id"]] = item.pk
        if opts["catalog_only"]:
            self.stdout.write(self.style.SUCCESS("Catalogue lists loaded."))
            return

        password = opts["password"]
        if not password:
            raise CommandError("--password is required for example accounts.")
        try:
            validate_password(password)
        except ValidationError as e:
            raise CommandError(" ".join(e.messages))
        if m.User.objects.exists() or m.Device.objects.exists():
            raise CommandError("The database already has users or devices.")

        s = data["settings"]
        m.AppSettings.objects.update_or_create(pk=1, defaults={
            "org_name": s["orgName"], "tag_prefix": s["tagPrefix"], "date_fmt": s["dateFmt"], "currency": s["currency"],
            "warranty_days": s["warrantyDays"], "hostname_is_tag": bool(s.get("hostnameIsTag")),
        })
        users = {}
        for u in data["users"]:
            users[u["id"]] = m.User.objects.create_user(
                u["email"], password, nombre=u["nombre"], rol=u["rol"], is_active=u["activo"]
            ).pk
        employees = {}
        for e in data["employees"]:
            employees[e["id"]] = m.Employee.objects.create(
                nombre=e["nombre"], email=e["email"], dept_id=ids["depts"][e["dept"]], loc_id=ids["locations"][e["loc"]],
                alta=day(e["alta"]), estado=e["estado"], estado_fecha=day(e["estadoFecha"]),
            ).pk

        def ref(coll, value):
            return ids[coll][value] if value else None

        devices = {}
        for d in data["devices"]:
            family = d.get("osFamily", "")
            ver = d.get("osVerId")
            device = m.Device.objects.create(
                tag=d["tag"], nombre=d["nombre"], serial=d["serial"], type_id=ref("types", d["typeId"]),
                model_id=ref("models", d.get("modelId")), custom_name=d.get("customName", ""), estado=d["estado"],
                loc_id=ref("locations", d["loc"]), compra=day(d.get("compra")), precio=d.get("precio") or 0,
                proveedor=plain(d.get("proveedor")), factura=d.get("factura", ""), garantia=day(d.get("garantia")),
                garantia_ext=d.get("garantiaExt", ""), garantia_ended=bool(d.get("garantiaEnded")),
                destino=d.get("destino", ""), wipe_cert=d.get("wipeCert", ""), notas=plain(d.get("notas")),
                cpu_id=ref("cpus", d.get("cpuId")), cpu_rep=d.get("cpuRep", ""), ram_size=d.get("ramSize"),
                ram_unit=d.get("ramUnit") or "GB", ram_gen_id=ref("ramGens", d.get("ramGen")), ram_speed=d.get("ramSpeed"),
                ram_speed_unit=d.get("ramSpeedUnit") or "MT/s", ram_rep=d.get("ramRep", ""), ram_modules=d.get("ramModules"),
                ram_mod_size=d.get("ramModSize"), ram_mod_unit=d.get("ramModUnit") or "GB",
                ram_form_id=ref("ramForms", d.get("ramForm")), gpu_id=ref("gpus", d.get("gpuId")), screen=d.get("screen"),
                touch=d.get("touch", ""), bat_health=d.get("batHealth"), bat_date=day(d.get("batDate")), os_family=family,
                mac_version_id=ref("macVersions", ver) if family == "mac" else None,
                win_version_id=ref("winVersions", ver) if family == "win" else None,
                linux_version_id=ref("linuxVersions", ver) if family == "linux" else None,
                win_edition_id=ref("winEditions", d.get("osEditionId")), linux_distro_id=ref("linuxDistros", d.get("osDistroId")),
                oclp=d.get("oclp", ""), hackintosh=d.get("hackintosh", ""), enc=d.get("enc", ""), ad=d.get("ad", ""),
            )
            devices[d["id"]] = device.pk
            for k in d.get("disks", []):
                m.Disk.objects.create(device=device, size=k.get("size"), unit=k.get("unit") or "GB", type_id=ref("diskTypes", k.get("type")),
                                      rep=k.get("rep", ""), form_id=ref("diskForms", k.get("form")), conn_id=ref("diskConns", k.get("conn")))
            for n in d.get("nics", []):
                m.NetworkCard.objects.create(device=device, type=n["type"], model_id=ref("nicModels", n.get("modelId")), mac=n.get("mac", ""),
                                             wifi_gen_id=ref("wifiGens", n.get("wifiGen")), bt_ver_id=ref("btVers", n.get("btVer")),
                                             speed=n.get("speed"), speed_unit=n.get("speedUnit") or "Gbps")
            for r in reversed(d.get("batLog") or []):
                m.BatteryReading.objects.create(device=device, fecha=day(r["fecha"]), salud=r["salud"])
        for a in data["assignments"]:
            m.Assignment.objects.create(device_id=devices[a["deviceId"]], employee_id=employees[a["employeeId"]], desde=day(a["desde"]),
                                        hasta=day(a["hasta"]), notas=plain(a["notas"]), condicion=a["condicion"])
        for i in data["incidents"]:
            m.Incident.objects.create(device_id=devices[i["deviceId"]], fecha=day(i["fecha"]), tipo=i["tipo"], descripcion=plain(i["descripcion"]),
                                      estado=i["estado"], resuelta=day(i["resuelta"]), piezas=plain(i["piezas"]), coste=i["coste"], proveedor=plain(i["proveedor"]))
        for e in reversed(data["log"]):
            event = m.AuditEvent.objects.create(key=e["k"], args=e["a"], device_id=devices.get(e.get("deviceId")), user_id=users.get(e.get("by")))
            m.AuditEvent.objects.filter(pk=event.pk).update(at=dt.datetime.combine(day(e["fecha"]), dt.time(12), dt.timezone.utc))
        self.stdout.write(self.style.SUCCESS(f"Example data loaded: {len(devices)} devices, {len(employees)} employees."))
