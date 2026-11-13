import unicodedata

from django.db import migrations, models

# Codes for the usual device types, so their asset tags follow the labelling scheme right after updating.
KNOWN = {
    "imac": "IMC", "torre": "PC", "tower": "PC", "portatil": "LAP", "laptop": "LAP", "macbook": "MB",
    "movil": "MOV", "mobil": "MOV", "mobile": "MOV", "mobile phone": "MOV", "tablet": "TAB", "tauleta": "TAB",
    "sobremesa premontado": "PC", "sobremesa a medida": "PC", "todo en uno": "AIO",
}


def _plain(text):
    text = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode()
    return " ".join(text.lower().split())


def fill_codes(apps, schema_editor):
    DeviceType = apps.get_model("inventory", "DeviceType")
    for dtype in DeviceType.objects.filter(code=""):
        names = dtype.nombre.values() if isinstance(dtype.nombre, dict) else [dtype.nombre]
        code = next((KNOWN[_plain(n)] for n in names if _plain(n) in KNOWN), "")
        if code:
            dtype.code = code
            dtype.save(update_fields=["code"])


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_updates'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetype',
            name='code',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='appsettings',
            name='tag_numbering',
            field=models.CharField(default='type', max_length=10),
        ),
        migrations.RunPython(fill_codes, migrations.RunPython.noop),
    ]
