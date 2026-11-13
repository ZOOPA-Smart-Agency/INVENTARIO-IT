"""Describes every registrable list: how it maps to the JSON the interface uses."""
from dataclasses import dataclass, field

from . import models as m


@dataclass(frozen=True)
class ListSpec:
    model: type
    title: str  # i18n key shown in the activity feed
    fields: dict = field(default_factory=dict)  # JSON key -> model attribute
    fks: dict = field(default_factory=dict)  # JSON key -> (model attribute, target model)
    translated: bool = False


LISTS = {
    "types": ListSpec(m.DeviceType, "set_types", {"hasScreen": "has_screen", "hasBattery": "has_battery", "usesName": "uses_name", "code": "code"}, translated=True),
    "depts": ListSpec(m.Department, "set_depts", translated=True),
    "locations": ListSpec(m.Location, "set_locs", {"tipo": "tipo", "direccion": "direccion"}, translated=True),
    "models": ListSpec(m.DeviceModel, "set_models", {"fabricante": "fabricante"}, {"typeId": ("type", m.DeviceType)}),
    "cpus": ListSpec(m.Cpu, "set_cpus", {"cores": "cores", "speed": "speed", "speedUnit": "speed_unit"}),
    "gpus": ListSpec(m.Gpu, "set_gpus", {"kind": "kind", "vram": "vram", "vramUnit": "vram_unit"}),
    "ramGens": ListSpec(m.RamGeneration, "set_ram"),
    "ramForms": ListSpec(m.RamFormFactor, "set_ramforms"),
    "diskTypes": ListSpec(m.DiskType, "set_disk"),
    "diskForms": ListSpec(m.DiskFormFactor, "set_diskforms"),
    "diskConns": ListSpec(m.DiskConnector, "set_conns"),
    "wifiGens": ListSpec(m.WifiGeneration, "set_wifigens"),
    "btVers": ListSpec(m.BluetoothVersion, "set_bt"),
    "macVersions": ListSpec(m.MacVersion, "set_macver"),
    "winVersions": ListSpec(m.WinVersion, "set_winver"),
    "winEditions": ListSpec(m.WinEdition, "set_wined"),
    "linuxDistros": ListSpec(m.LinuxDistro, "set_distros"),
    "linuxVersions": ListSpec(m.LinuxVersion, "set_linuxver", {}, {"distroId": ("distro", m.LinuxDistro)}),
    "nicModels": ListSpec(m.NicModel, "set_nicmodels", {"type": "type"}),
}
