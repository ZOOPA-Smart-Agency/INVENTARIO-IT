# Inventario de equipos

Web app to manage the company's device inventory: laptops, desktops and all-in-ones, the employees who hold them, faults and repairs, warranty, and hardware and software specs. The interface is available in Spanish, Catalan and English.

- **Backend:** Django 5.2 and PostgreSQL. Accounts, roles, validation and the audit log are enforced on the server.
- **Frontend:** the original interface, with no build step, in `inventory/static/inventory/`.
- **Spec:** `docs/documento-planificacion.txt`. Design and working notes are in `docs/HANDOFF.md`, and the original prototype is in `docs/prototype/`.

## Roles

| Role | Can do |
|---|---|
| `admin` | Everything, including Settings and accounts |
| `tech` | Devices, employees and faults; can add list entries from the **+** buttons |
| `read` | View only |

## Local development

Requires Python 3.13 and PostgreSQL.

```bash
python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env          # then set DJANGO_SECRET_KEY
createdb inventario
.venv/bin/python manage.py migrate
.venv/bin/python manage.py load_demo_data --password 'choose-a-password'
.venv/bin/python manage.py runserver
```

Open <http://localhost:8000> and sign in as `admin@empresa.es`, `it@empresa.es` or `lectura@empresa.es`.

To see the first-install wizard, skip `load_demo_data` or point `DATABASE_URL` at a new empty database. In development it does not ask for a code.

Run the tests with `.venv/bin/python manage.py test`.

## Deployment

The app is one container (`Dockerfile`) plus a PostgreSQL database, and suits any host that runs containers. It applies database migrations on start.

| Environment variable | Required | Purpose |
|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `DJANGO_SECRET_KEY` | Yes | Long random value, unique to each environment |
| `DJANGO_ALLOWED_HOSTS` | Yes | Comma-separated host names, such as `inventario.example.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Yes | Comma-separated origins, such as `https://inventario.example.com` |
| `DJANGO_SETUP_TOKEN` | For first install | Code the setup wizard asks for |
| `DJANGO_DEBUG` | No | Leave unset in production |
| `DJANGO_SSL_REDIRECT` | No | Set to `0` only if the host already forces HTTPS and redirects loop |
| `PORT`, `WEB_CONCURRENCY` | No | Listening port (8000) and worker count (3) |
| `GUNICORN_TIMEOUT` | No | Seconds a request may take before it is stopped (180). Large backups and restores need the time; raise it if a restore is cut off. A restore that is stopped changes nothing. |

The app must be served over HTTPS, because its cookies are marked secure. The health check is at `/healthz`; include the host name the check uses in `DJANGO_ALLOWED_HOSTS`.

### First install

Set `DJANGO_SETUP_TOKEN` to a long random value, deploy, and open the site. On an empty database the app shows a three-step wizard: organisation, locations and departments, then the first administrator. It asks for that code, works only once, and also loads the standard device types, components and software lists. Remove the variable afterwards if you like.

Without a code configured, production keeps the wizard closed so nobody else can claim a fresh install. To create the first administrator from the command line instead, run `python manage.py load_demo_data --catalog-only` and then `python manage.py createsuperuser`.

Do not run `load_demo_data` without `--catalog-only` in production: it creates fictional people and devices.

## Backups

Administrators export and restore everything in **Settings > Data > Backups**. A backup is one `.invbackup` file (a zip) holding every record, setting, the activity history, user accounts with their encrypted passwords, and the logo. It can be protected with a password, which encrypts the contents with AES-256-GCM, with the key derived from the password using scrypt. Without that password the backup cannot be restored, and nobody can recover it.

Restoring replaces all data in a single transaction, so a failed restore changes nothing, and it signs everyone out. Backups without an active administrator are refused. The file format is described at the top of `inventory/backup.py`.

While a restore runs, the app is in maintenance mode: every request from anyone else is turned away. Administrators who open the app follow the restore's live progress, and everyone else sees a maintenance page; both clear by themselves when it ends. The state is published through a second connection to the same database (`side` in `config/settings.py`), so all server processes see it immediately. If the process doing the restore dies, maintenance mode lifts itself after 5 minutes.

These backups are for moving or recovering the app's data. The hosting database should still have its own regular backups.

## Password rules

The wizard, and later **Settings > Passwords**, control whether password requirements are enforced and which ones apply: minimum length, an uppercase letter, a number and a symbol. The server enforces them for new and changed passwords made in the app; existing passwords keep working. Passwords set from the command line with `createsuperuser` follow Django's own validators instead.

## Project layout

| Path | Contents |
|---|---|
| `config/settings.py` | All configuration, read from the environment |
| `inventory/models.py` | Database tables |
| `inventory/api.py` | JSON API and business rules |
| `inventory/state.py` | Snapshot of the data sent to the interface |
| `inventory/registry.py` | Definition of each Settings list |
| `inventory/static/inventory/app.js` | Interface, including all translations in `I18N` |
| `inventory/tests/` | Server tests, also run by GitHub Actions |

## Conventions

- Every user-facing text exists in `es`, `ca` and `en`, with identical key sets.
- Errors from the API are translation keys, so people read them in their own language.
- Whether someone was dismissed or resigned is deliberately not recorded. Leaving is one neutral status.
- A form's main button is one short verb. The Classic design stays available alongside Glass.
