"""Ethernet speeds typed in megabits while the form's unit said Gbps ("1000 Gbps", which no port reaches) become
what was meant: 1000 -> 1 Gbps. Speeds of 1000 Mbps or more are written in Gbps, as the form now saves them.
"""
from django.db import migrations


def fix(apps, schema_editor):
    NetworkCard = apps.get_model("inventory", "NetworkCard")
    for card in NetworkCard.objects.filter(type="eth", speed__isnull=False):
        if (card.speed_unit == "Gbps" and card.speed > 100) or (card.speed_unit == "Mbps" and card.speed >= 1000):
            card.speed, card.speed_unit = round(card.speed / 1000, 1), "Gbps"
            card.save(update_fields=["speed", "speed_unit"])


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_assignment_to_department'),
    ]

    operations = [
        migrations.RunPython(fix, migrations.RunPython.noop),
    ]
