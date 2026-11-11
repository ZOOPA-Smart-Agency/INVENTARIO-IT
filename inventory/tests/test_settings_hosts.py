import os
import subprocess
import sys
from pathlib import Path

from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parents[2]


def settings_for(hosts, port="443"):
    """Loads the settings in a separate process with these addresses, as the server would."""
    env = {**os.environ, "DJANGO_DEBUG": "0", "DJANGO_SECRET_KEY": "x", "DATABASE_URL": "postgres://x/y",
           "DJANGO_ALLOWED_HOSTS": "web,localhost", "DJANGO_SITE_HOSTS": hosts, "DJANGO_HTTPS_PORT": port,
           "DJANGO_CSRF_TRUSTED_ORIGINS": ""}
    code = ("import os, json; os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'; from django.conf import settings; "
            "print(json.dumps([settings.ALLOWED_HOSTS, settings.CSRF_TRUSTED_ORIGINS]))")
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True, check=True).stdout
    import json
    return json.loads(out)


class SiteHostsTests(SimpleTestCase):
    def test_several_addresses(self):
        allowed, trusted = settings_for("localhost, 192.168.16.172, mac.local")
        self.assertEqual(allowed, ["web", "localhost", "192.168.16.172", "mac.local"])
        self.assertEqual(trusted, ["https://localhost", "https://192.168.16.172", "https://mac.local"])

    def test_other_https_port_is_part_of_the_trusted_address(self):
        self.assertEqual(settings_for("localhost", "8443")[1], ["https://localhost:8443"])

    def test_single_domain(self):
        self.assertEqual(settings_for("inventario.example.com"), [["web", "localhost", "inventario.example.com"], ["https://inventario.example.com"]])
