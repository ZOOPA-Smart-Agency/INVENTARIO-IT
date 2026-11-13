"""The "except Macs" checkbox of a device type's rule becomes a choice of makers: all, only Apple computers, or all but
Apple computers. Types that left out Macs now leave out Apple computers, which is the same thing.
"""
from django.db import migrations, models


def copy_choice(apps, schema_editor):
    DeviceType = apps.get_model("inventory", "DeviceType")
    DeviceType.objects.filter(auto_not_mac=True).update(auto_apple="except")


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_type_auto_rules'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetype',
            name='auto_apple',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.RunPython(copy_choice, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='devicetype',
            name='auto_not_mac',
        ),
    ]
