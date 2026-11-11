#!/usr/bin/env bash
# Installs Inventario on this server, or repairs an existing installation.
#
#   sudo ./deploy/install.sh [install directory]        (default: /opt/inventario)
#
# Needs Docker with the Compose plugin. Run it from the app's source folder (the release you downloaded).
# It asks a few questions the first time; the answers can also be given as environment variables
# (SITE_HOST, TLS_MODE, APP_UPDATE_GITHUB_APP_ID, GITHUB_APP_KEY_FILE) together with NONINTERACTIVE=1.
# Afterwards, new versions are installed from Settings > General > Updates.
set -euo pipefail

SOURCE="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-${INSTALL_DIR:-/opt/inventario}}"
REPO="${APP_UPDATE_REPO:-ZOOPA-Smart-Agency/INVENTARIO-IT}"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }
fail() { printf '\n\033[31m%s\033[0m\n' "$*" >&2; exit 1; }
ask() { # ask VARIABLE "question" [default]
  local value="${!1:-}"
  if [ -z "$value" ] && [ -z "${NONINTERACTIVE:-}" ]; then
    read -r -p "$2${3:+ [$3]}: " value
  fi
  printf -v "$1" '%s' "${value:-${3:-}}"
}
random() { head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n'; }

command -v docker >/dev/null || fail "Docker is not installed. See https://docs.docker.com/engine/install/"
docker compose version >/dev/null 2>&1 || fail "The Docker Compose plugin is missing. See https://docs.docker.com/compose/install/linux/"
[ -f "$SOURCE/Dockerfile" ] && [ -f "$SOURCE/inventory/version.py" ] || fail "Run this from the app's source folder."
VERSION="$(sed -n 's/^VERSION = "\(.*\)"$/\1/p' "$SOURCE/inventory/version.py")"
[ -n "$VERSION" ] || fail "Could not read the version from inventory/version.py."

say "Installing Inventario $VERSION in $TARGET"
mkdir -p "$TARGET/backups" "$TARGET/keys" "$TARGET/work"
chmod 700 "$TARGET/keys"
cp "$SOURCE/deploy/docker-compose.yml" "$SOURCE/deploy/Caddyfile" "$SOURCE/deploy/maintenance.html" "$TARGET/"
rm -rf "$TARGET/updater" && cp -R "$SOURCE/deploy/updater" "$TARGET/updater"

if [ ! -f "$TARGET/.env" ]; then
  say "A few questions (Enter accepts the suggestion in brackets)"
  echo "The address people will type to open the app. It must already lead to this server: a domain such as"
  echo "inventario.yourcompany.com set up in your DNS, a name your network knows, or this server's IP address."
  echo "Give several separated by commas if needed (for example: localhost, 192.168.1.20). To try it on this computer, use localhost."
  ask SITE_HOST "Address" "localhost"
  SITE_HOST="$(printf '%s' "$SITE_HOST" | tr -s ' ' | sed 's/ *, */, /g; s/^ *//; s/ *$//')"
  [[ "$SITE_HOST" =~ ^[A-Za-z0-9.-]+(,\ [A-Za-z0-9.-]+)*$ ]] || fail "That address is not valid: use only letters, numbers, dots and dashes, and commas between addresses."
  if [ -z "${TLS_MODE:-}" ]; then
    ask PUBLIC "Is it a public domain pointing at this server, so a free HTTPS certificate can be issued? (y/n)" "n"
    if [[ "$PUBLIC" =~ ^[YySs] ]]; then
      if [[ "$SITE_HOST" =~ (^|\ )(localhost|[0-9.]+|[A-Za-z0-9-]+|[A-Za-z0-9.-]+\.local)(,|$) ]]; then
        fail "Free public certificates are only for public domains. Give only public domains, or answer n to use the server's own certificate."
      fi
      ask TLS_MODE "Email for certificate notices"
    else
      TLS_MODE="internal"
    fi
  fi
  ask APP_UPDATE_GITHUB_APP_ID "GitHub App ID for updates (Enter to set up later)" ""
  ask GITHUB_APP_KEY_FILE "Path to that GitHub App's private key, a .pem file (Enter to set up later)" ""
  [[ -z "$APP_UPDATE_GITHUB_APP_ID" || "$APP_UPDATE_GITHUB_APP_ID" =~ ^[0-9]+$ ]] || fail "The GitHub App ID is a number."
  SETUP_TOKEN="$(random)"
  umask 077
  cat > "$TARGET/.env" <<ENV
# Inventario settings. Keep this file private: it holds the database password and secret key.
INSTALL_DIR=$TARGET
APP_VERSION=$VERSION
SITE_HOST=$SITE_HOST
TLS_MODE=$TLS_MODE
TZ=${TZ:-Europe/Madrid}
POSTGRES_PASSWORD=$(random)
DJANGO_SECRET_KEY=$(random)$(random)
DJANGO_SETUP_TOKEN=$SETUP_TOKEN
DEFAULT_SNI=$(printf '%s' "$SITE_HOST" | tr ',' '\n' | tr -d ' ' | grep -E '^[0-9.]+$' | head -1)
APP_UPDATE_REPO=$REPO
APP_UPDATE_GITHUB_APP_ID=$APP_UPDATE_GITHUB_APP_ID
${HTTP_PORT:+HTTP_PORT=$HTTP_PORT}
${HTTPS_PORT:+HTTPS_PORT=$HTTPS_PORT}
ENV
  umask 022
  if [ -n "${GITHUB_APP_KEY_FILE:-}" ]; then
    install -m 600 "$GITHUB_APP_KEY_FILE" "$TARGET/keys/github-app.pem"
  fi
fi
[ -f "$TARGET/keys/github-app.pem" ] || { : > "$TARGET/keys/github-app.pem"; chmod 600 "$TARGET/keys/github-app.pem"; }

say "Building the app (this takes a few minutes the first time)"
docker build -t "inventario-web:$VERSION" --build-arg "APP_COMMIT=${APP_COMMIT:-}" "$SOURCE"
CURRENT="$(sed -n 's/^APP_VERSION=//p' "$TARGET/.env")"
if [ "$CURRENT" != "$VERSION" ]; then
  sed -i.bak "s/^APP_VERSION=.*/APP_VERSION=$VERSION/" "$TARGET/.env" && rm -f "$TARGET/.env.bak"
fi

say "Starting"
cd "$TARGET"
docker compose build updater
docker compose up -d

for _ in $(seq 1 60); do
  if docker compose exec -T web python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz', timeout=3)" >/dev/null 2>&1; then
    HOSTS="$(sed -n 's/^SITE_HOST=//p' .env)"
    TOKEN="$(sed -n 's/^DJANGO_SETUP_TOKEN=//p' .env)"
    PORT="$(sed -n 's/^HTTPS_PORT=//p' .env)"
    say "Inventario is running."
    IFS=',' read -r -a ADDRESSES <<< "$HOSTS"
    for HOST in "${ADDRESSES[@]}"; do
      HOST="${HOST// /}"
      echo "  https://$HOST${PORT:+:$PORT}"
      if [ "$HOST" != "localhost" ] && ! python3 -c "import socket,sys; socket.gethostbyname(sys.argv[1])" "$HOST" >/dev/null 2>&1; then
        echo "    (this computer cannot find \"$HOST\" yet: add it to your DNS, or to each computer's hosts file, pointing at this server)"
      fi
    done
    echo "Open one of these to finish setting it up. To change the addresses later, edit SITE_HOST in $TARGET/.env and run: docker compose up -d"
    echo "The first-run wizard asks for this setup code: $TOKEN"
    if [ "$(sed -n 's/^TLS_MODE=//p' .env)" = "internal" ]; then
      echo "The certificate is the server's own, so browsers warn the first time; that is expected for in-house addresses."
    fi
    if [ ! -s keys/github-app.pem ]; then
      echo "Updates: add the GitHub App's private key as $TARGET/keys/github-app.pem and its ID to .env, then run: docker compose up -d updater"
    fi
    exit 0
  fi
  sleep 3
done
fail "The app did not start. See what happened with: cd $TARGET && docker compose logs web"
