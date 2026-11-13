"""MacBooks and iMacs get device types of their own, with the codes of the labelling scheme (MB and IMC).

The types are added when missing (an existing type with the same name or code is used instead). Models named
"MacBook ..." or "iMac ..." move to them, and so do their devices. Asset tags are not changed: devices already
labelled keep their labels; new ones are numbered with the new codes.
"""
import re

from django.db import migrations

APPLE = [
    # (name, code, has screen, has battery, model names)
    ("MacBook", "MB", True, True, re.compile(r"^(apple\s+)?macbook\b", re.IGNORECASE)),
    ("iMac", "IMC", True, False, re.compile(r"^(apple\s+)?imac\b", re.IGNORECASE)),
]


def _names(dtype):
    return [str(n).strip().lower() for n in (dtype.nombre.values() if isinstance(dtype.nombre, dict) else [dtype.nombre])]


def add_apple_types(apps, schema_editor):
    DeviceType = apps.get_model("inventory", "DeviceType")
    DeviceModel = apps.get_model("inventory", "DeviceModel")
    Device = apps.get_model("inventory", "Device")
    if not DeviceType.objects.exists():
        return  # not installed yet: the first-run wizard loads the catalog, which has both
    types = list(DeviceType.objects.all())
    for name, code, screen, battery, pattern in APPLE:
        dtype = (next((t for t in types if name.lower() in _names(t)), None)
                 or next((t for t in types if t.code == code), None))
        if dtype is None:
            dtype = DeviceType.objects.create(nombre={"es": name, "en": name, "ca": name}, code=code,
                                              has_screen=screen, has_battery=battery)
        elif not dtype.code:
            dtype.code = code
            dtype.save(update_fields=["code"])
        moved = [x.pk for x in DeviceModel.objects.exclude(type=dtype) if pattern.match(x.nombre)]
        DeviceModel.objects.filter(pk__in=moved).update(type=dtype)
        Device.objects.filter(model_id__in=moved).update(type=dtype)


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_type_code'),
    ]

    operations = [
        migrations.RunPython(add_apple_types, migrations.RunPython.noop),
    ]
