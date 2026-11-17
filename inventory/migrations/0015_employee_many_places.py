"""An employee can belong to several departments and work from several offices. Each employee keeps the department
and office they had, as the first of their new lists.
"""
from django.db import migrations, models


def copy_places(apps, schema_editor):
    Employee = apps.get_model("inventory", "Employee")
    for employee in Employee.objects.all():
        if employee.dept_id:
            employee.depts.add(employee.dept_id)
        if employee.loc_id:
            employee.locs.add(employee.loc_id)


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_employee_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='depts',
            field=models.ManyToManyField(blank=True, related_name='employees', to='inventory.department'),
        ),
        migrations.AddField(
            model_name='employee',
            name='locs',
            field=models.ManyToManyField(blank=True, related_name='employees', to='inventory.location'),
        ),
        migrations.RunPython(copy_places, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='employee',
            name='dept',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='loc',
        ),
    ]
