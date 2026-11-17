"""The "Temporal o en prácticas" checkbox becomes a choice of contract: not defined, indefinido, temporal or
prácticas. Employees who had the box ticked become "temporal" (the box did not say which of the two); the rest are
not defined, since an unticked box did not say they were permanent.
"""
from django.db import migrations, models


def copy_choice(apps, schema_editor):
    Employee = apps.get_model("inventory", "Employee")
    Employee.objects.filter(temporal=True).update(contrato="temporal")


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_employee_temporal'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='contrato',
            field=models.CharField(blank=True, choices=[('', 'Not defined'), ('indefinido', 'Permanent'), ('temporal', 'Temporary'), ('practicas', 'Internship')], default='', max_length=10),
        ),
        migrations.RunPython(copy_choice, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='employee',
            name='temporal',
        ),
    ]
