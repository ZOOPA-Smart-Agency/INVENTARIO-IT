"""Accounts get a username that signs in like the email address. Existing accounts get one made from the start of
their email (ana.lopez@empresa.es -> ana.lopez; ana.lopez2 if that is taken), which administrators can change.
"""
import re

from django.db import migrations, models


def fill_usernames(apps, schema_editor):
    User = apps.get_model("inventory", "User")
    taken = set()
    for user in User.objects.order_by("pk"):
        base = re.sub(r"[^a-z0-9._-]", "", user.email.split("@")[0].lower())[:140] or "user"
        base = base if len(base) >= 2 else base + "0"
        name, n = base, 1
        while name in taken:
            n += 1
            name = f"{base}{n}"
        taken.add(name)
        user.username = name
        user.save(update_fields=["username"])


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_type_auto_apple'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
        migrations.RunPython(fill_usernames, migrations.RunPython.noop),
    ]
