"""Device types can also take every computer of one shape (Settings > Device types): `auto_chassis` is "laptop",
"desktop" or "all_in_one", and `auto_not_mac` leaves Macs out of it, so "all laptops except Macs" can go to Portátil
while MacBooks get their own type.

The starting types get sensible words and rules, unless someone already set their own.
"""
from django.db import migrations, models

# By type code, as set in 0007 and 0008: (words, chassis, except Macs).
RULES = {
    "LAP": ("ThinkPad, Latitude, EliteBook, ProBook, IdeaPad, Zenbook, Vivobook, Surface Laptop", "laptop", True),
    "MB": ("MacBook", "", False),
    "AIO": ("EliteOne, ProOne, All-in-One", "all_in_one", True),
    "IMC": ("iMac", "", False),
}
PREBUILT = ("EliteDesk, ProDesk, Mac mini, Mac Studio, Mac Pro", "desktop", False)
CUSTOM = ("To Be Filled By O.E.M., System Product Name, Default string", "", False)  # what home-built PCs report


def fill_rules(apps, schema_editor):
    DeviceType = apps.get_model("inventory", "DeviceType")
    for dtype in DeviceType.objects.all():
        rule = RULES.get(dtype.code) or ((CUSTOM if dtype.uses_name else PREBUILT) if dtype.code == "PC" else None)
        if rule is None:
            continue
        words, chassis, not_mac = rule
        if not dtype.match:
            dtype.match = words
        if chassis:  # a new setting: nobody has chosen it yet
            dtype.auto_chassis, dtype.auto_not_mac = chassis, not_mac
        dtype.save(update_fields=["match", "auto_chassis", "auto_not_mac"])


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_type_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetype',
            name='auto_chassis',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AddField(
            model_name='devicetype',
            name='auto_not_mac',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(fill_rules, migrations.RunPython.noop),
    ]
