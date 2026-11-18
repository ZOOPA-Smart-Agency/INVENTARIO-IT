"""Intel's built-in "Arc" graphics (Core Ultra processors: "Intel Arc Graphics", "Intel Arc 140V GPU (16GB)") were
saved by the device app as separate cards with 4 GB of memory. They are part of the processor: integrated, with no
memory of their own. The memory class in brackets ("(16GB)") is dropped from the name, as the device app now does.
Intel's separate Arc cards (A380, A770, B580, Pro A60...) are left alone.
"""
import re

from django.db import migrations

CARD = re.compile(r"\barc\s+(pro\s+)?[ab]\d{2,3}", re.IGNORECASE)
BUILT_IN = re.compile(r"\bintel\b.*\barc\b", re.IGNORECASE)


def fix(apps, schema_editor):
    Gpu = apps.get_model("inventory", "Gpu")
    for gpu in Gpu.objects.all():
        if not BUILT_IN.search(gpu.nombre) or CARD.search(gpu.nombre):
            continue
        gpu.kind, gpu.vram = "integrated", None
        name = re.sub(r"\s*\(\d+\s*GB\)\s*$", "", gpu.nombre, flags=re.IGNORECASE).strip()
        if name != gpu.nombre and not Gpu.objects.filter(nombre__iexact=name).exists():
            gpu.nombre = name
        gpu.save()


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_fix_ethernet_speeds'),
    ]

    operations = [
        migrations.RunPython(fix, migrations.RunPython.noop),
    ]
