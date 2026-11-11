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

## Installing on a server

The recommended setup is one Linux server with Docker, installed by `deploy/install.sh`. It runs four containers: the database, the app, a web server (Caddy) that provides HTTPS, and the **updater**, which installs new versions from **Settings > General > Updates**.

**Requirements:** any Linux server (for example Ubuntu 24.04 or Debian 12) with [Docker Engine and the Compose plugin](https://docs.docker.com/engine/install/), 2 GB of memory, 20 GB of disk, and ports 80 and 443 open to the people who will use it.

1. Create the GitHub App described under [Access to the private repository](#access-to-the-private-repository), and copy its private key (`.pem`) to the server.
2. Download the latest release's source code from the repository's **Releases** page on GitHub, copy it to the server, and unpack it.
3. From the unpacked folder, run `sudo ./deploy/install.sh`. It asks for the address people will use (or several, separated by commas, such as a domain and the server's IP address), whether it is a public domain (then a free certificate is issued automatically; otherwise the server uses its own certificate and browsers warn the first time), and the GitHub App's ID and key.
4. Open the address it prints and complete the first-run wizard with the setup code it shows.

To change the addresses later, edit `SITE_HOST` in `/opt/inventario/.env` (for example `SITE_HOST=inventario.yourcompany.com, 192.168.1.20`) and run `docker compose up -d` there. If the list includes an IP address, also set `DEFAULT_SNI` to that IP: browsers opening the app by IP do not name the address they want, and this tells the web server which certificate to give them. A free public certificate is only possible when every address is a public domain; otherwise use `TLS_MODE=internal`.

Everything lives in `/opt/inventario`: `.env` (settings and secrets: keep it private), `keys/` (the GitHub App key), `backups/` (the database backups taken before each update) and the container definitions. Useful commands, run in that folder: `docker compose ps`, `docker compose logs -f updater`, `docker compose restart web`.

### Installing new versions

**Settings > General > Updates** shows the installed version and the latest release on GitHub (the updater checks every hour, or on **Check for updates**). When there is a new one, **Install** does the rest, while administrators watch the progress and everyone else sees a maintenance page:

1. A full backup of the database, kept in `backups/`.
2. The release is downloaded through the GitHub App and built on the server.
3. The app restarts on the new version, which applies its own database changes.
4. The updater checks that the new version answers. If it does not, it stops it, puts back the previous version and the backed-up database, and records what happened in the update history.

Updates can also install by themselves: turn on **Automatic updates** and choose the hour (server time). Only published releases are installed, never pre-releases, and a failed automatic update is not retried until the next day.

Only the latest release of the configured repository can be installed. The app never has access to Docker: it can only ask the updater for that release. The updater keeps the last 5 pre-update backups and the current and previous app images.

### Installing it on phones, tablets and computers

The app can be installed like a native one, with its own icon and window: from the account menu, **Install the app** (Chrome, Edge and Android show the browser's install prompt; iPhone, iPad and Safari on the Mac show the steps). The icon is made from the company logo when one is uploaded in **Settings > General > Logo** (PNG, JPG, WebP or GIF; an SVG logo keeps the app's own icon). Without a connection to the server, the installed app shows a "no connection" page; it never keeps inventory data on the device.

Browsers only allow installing from an address with a certificate they trust. That works out of the box with a public domain (`TLS_MODE` set to an email address). With the server's own certificate (`TLS_MODE=internal`, for local addresses and IPs), each device must first be set to trust it: copy it with `docker compose cp caddy:/data/caddy/pki/authorities/local/root.crt inventario-ca.crt` and install it as a trusted certificate on the device. Only do this on company devices: whoever controls the server could then create certificates those devices trust for any website. For anything beyond testing, a domain with a public certificate (or the company's own certificate authority) is the better choice.

### Adding computers with the device app

The device app (repository `INVENTARIODATA`) reads a computer's details (serial number, model, processor, memory, drives, graphics, network cards, operating system, encryption, domain membership, battery health) and adds it to the inventory, or updates it if its serial number is already there. It signs in with a technician's or administrator's email and password. The API it uses is described in [docs/agent-api.md](docs/agent-api.md).

With the server's own certificate (`TLS_MODE=internal`), the device app asks the first time whether to trust the server's certificate authority, which the web server publishes at `/ca.crt`. It trusts it only for that address. The installer prints the fingerprint to compare it with; to see it again, run this in the install folder:

```bash
docker compose exec -T caddy cat /data/caddy/pki/authorities/local/root.crt | openssl x509 -noout -fingerprint -sha256
```

## Other hosting

The app is one container (`Dockerfile`) plus a PostgreSQL database, and also runs on any host that runs containers. It applies database migrations on start. Without the updater, **Settings > General > Updates** can only check for new versions; installing them is done by deploying the new version.

| Environment variable | Required | Purpose |
|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `DJANGO_SECRET_KEY` | Yes | Long random value, unique to each environment |
| `DJANGO_ALLOWED_HOSTS` | Yes | Comma-separated host names, such as `inventario.example.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Yes | Comma-separated origins, such as `https://inventario.example.com` |
| `DJANGO_SETUP_TOKEN` | For first install | Code the setup wizard asks for |
| `APP_UPDATE_REPO` | No | GitHub repository checked for new releases (`ZOOPA-Smart-Agency/INVENTARIO-IT`); empty turns the check off |
| `APP_UPDATE_TOKEN` | For a private repo | Read-only GitHub token for the update check (or use a GitHub App instead) |
| `APP_UPDATE_GITHUB_APP_ID`, `APP_UPDATE_GITHUB_APP_PRIVATE_KEY_FILE` | For a private repo, instead of a token | GitHub App used by the update check, and the path to its private key; the key's contents can go in `APP_UPDATE_GITHUB_APP_PRIVATE_KEY` instead |
| `APP_COMMIT` | No | Exact build shown in Settings > About; set at build time with `--build-arg APP_COMMIT=$(git rev-parse HEAD)` |
| `DJANGO_DEBUG` | No | Leave unset in production |
| `DJANGO_SSL_REDIRECT` | No | Set to `0` only if the host already forces HTTPS and redirects loop |
| `PORT`, `WEB_CONCURRENCY` | No | Listening port (8000) and worker count (3) |
| `GUNICORN_TIMEOUT` | No | Seconds a request may take before it is stopped (180). Large backups and restores need the time; raise it if a restore is cut off. A restore that is stopped changes nothing. |

The app must be served over HTTPS, because its cookies are marked secure. The health check is at `/healthz`; include the host name the check uses in `DJANGO_ALLOWED_HOSTS`.

### First install on other hosting

Set `DJANGO_SETUP_TOKEN` to a long random value, deploy, and open the site. On an empty database the app shows a three-step wizard: organisation, locations and departments, then the first administrator. It asks for that code, works only once, and also loads the standard device types, components and software lists. Remove the variable afterwards if you like.

Without a code configured, production keeps the wizard closed so nobody else can claim a fresh install. To create the first administrator from the command line instead, run `python manage.py load_demo_data --catalog-only` and then `python manage.py createsuperuser`.

Do not run `load_demo_data` without `--catalog-only` in production: it creates fictional people and devices.

## Backups

Administrators export and restore everything in **Settings > Data > Backups**. A backup is one `.invbackup` file (a zip) holding every record, setting, the activity history, user accounts with their encrypted passwords, and the logo. It can be protected with a password, which encrypts the contents with AES-256-GCM, with the key derived from the password using scrypt. Without that password the backup cannot be restored, and nobody can recover it.

Restoring replaces all data in a single transaction, so a failed restore changes nothing, and it signs everyone out. Backups without an active administrator are refused. The file format is described at the top of `inventory/backup.py`.

While a restore runs, the app is in maintenance mode: every request from anyone else is turned away. Administrators who open the app follow the restore's live progress, and everyone else sees a maintenance page; both clear by themselves when it ends. The state is published through a second connection to the same database (`side` in `config/settings.py`), so all server processes see it immediately. If the process doing the restore dies, maintenance mode lifts itself after 5 minutes.

These backups are for moving or recovering the app's data. The hosting database should still have its own regular backups.

## Versions and updates

**Settings > General > About** shows the version, the exact build, the environment, how much data there is, and the Python, Django and PostgreSQL versions. **Settings > General > Updates** compares the running version with the latest release published on GitHub, shows that release's notes and link, and, on a server installed with `deploy/install.sh`, installs it (see [Installing new versions](#installing-new-versions)).

To publish a release:

1. Raise `VERSION` in `inventory/version.py` (for example `1.1.0`) and commit.
2. On GitHub, create a release with the tag `v1.1.0` and write what changed in its notes. Mark it as a pre-release if it is not ready for everyone.
3. The **Release** workflow (`.github/workflows/release.yml`) runs the tests, checks that the tag matches `VERSION`, and publishes the app image to GitHub's container registry as `ghcr.io/zoopa-smart-agency/inventario-it:1.1.0`, plus `:latest` for normal releases. If the tag and `VERSION` differ, it stops without publishing.
4. On a server installed with `deploy/install.sh`, install it from **Settings > General > Updates**, or let it install itself at night. On other hosting, make a backup and deploy that image.

### Access to the private repository

The updater (or, on other hosting, the update check) needs read access to the repository's releases and source code. Where the organisation does not allow personal tokens, use a GitHub App:

1. In the organisation's settings on GitHub, open **Developer settings > GitHub Apps > New GitHub App**. If you cannot create one there, an organisation owner can, or you can create it under your own account and ask an owner to approve its installation.
2. Name it, for example *Inventario update check*. Use the repository's address as the homepage URL, and untick **Webhook > Active**.
3. Under **Repository permissions**, set **Contents** to **Read-only**. GitHub adds **Metadata: Read-only** automatically. Leave every other permission off.
4. Under **Where can this GitHub App be installed?**, choose **Only on this account**, and create it.
5. Note the **App ID** at the top of the app's **General** page. Then, in the app's left sidebar, open **Credentials** and, under **Key pairs**, choose **New key**: a `.pem` file downloads. GitHub keeps only its public half, so this is the only copy: keep it secret, and never commit it.
6. Choose **Install App**, pick the organisation, choose **Only select repositories**, and select this repository.
7. With `deploy/install.sh`, give the App ID and the `.pem` file when it asks, or later put the key in `/opt/inventario/keys/github-app.pem`, set `APP_UPDATE_GITHUB_APP_ID` in `/opt/inventario/.env`, and run `docker compose up -d updater` there. On other hosting, set `APP_UPDATE_GITHUB_APP_ID` and `APP_UPDATE_GITHUB_APP_PRIVATE_KEY_FILE` (the path of the `.pem` file), or put the key's contents in `APP_UPDATE_GITHUB_APP_PRIVATE_KEY`, writing each line break as `\n`.

**Settings > General > Updates** then shows *GitHub access: GitHub App*. The server signs in with the key, and GitHub gives it a token, valid for an hour, that can only read this repository's contents. The key never leaves the server. If a personal token is allowed instead, set `APP_UPDATE_TOKEN` to a fine-grained token with **Contents: read-only** on this repository.

### Getting the image onto other hosting

A server installed with `deploy/install.sh` builds each release itself and does not need this. The release workflow also publishes the image to GitHub's container registry, which is private like the repository. Outside GitHub, that registry only accepts classic personal access tokens: GitHub App tokens cannot download from it. Where tokens are not allowed, choose one of these instead:

- **A host that builds from the repository.** Many hosts connect to GitHub through their own GitHub App and build the `Dockerfile` themselves for each release or push. No registry login is needed.
- **The host's own registry.** The release workflow can push the image there as well, using credentials stored as a GitHub Actions secret, and the server pulls from it.
- **A personal access token (classic) with only `read:packages`,** if an organisation owner creates one for a dedicated account.

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
| `deploy/` | Server installation: `install.sh`, the containers (`docker-compose.yml`), the web server (`Caddyfile`) and the updater (`updater/`, with its own tests) |

## Conventions

- Every user-facing text exists in `es`, `ca` and `en`, with identical key sets.
- Errors from the API are translation keys, so people read them in their own language.
- Whether someone was dismissed or resigned is deliberately not recorded. Leaving is one neutral status.
- A form's main button is one short verb. The Classic design stays available alongside Glass.
