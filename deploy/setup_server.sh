#!/usr/bin/env bash
# deploy/setup_server.sh
# Run once on a fresh Ubuntu 22.04 / 24.04 server as root (or with sudo).
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── 0. Variables ──────────────────────────────────────────────────────────────
APP_USER="erp"
APP_DIR="/home/$APP_USER/school-erp"
VENV_DIR="$APP_DIR/venv"
REPO_URL="https://github.com/inam0980/School-ERP-System.git"   # update if private
DOMAIN="yourdomain.com"
DB_NAME="school_db"
DB_USER="django_user"
DB_PASS="StrongProductionPassword!"    # change before running!

# ── 1. System packages ────────────────────────────────────────────────────────
apt-get update -y
apt-get install -y \
    python3.12 python3.12-venv python3.12-dev \
    postgresql postgresql-contrib \
    nginx certbot python3-certbot-nginx \
    git build-essential libpq-dev \
    supervisor

# ── 2. Create app user ────────────────────────────────────────────────────────
id "$APP_USER" &>/dev/null || useradd -m -s /bin/bash "$APP_USER"
usermod -aG www-data "$APP_USER"

# ── 3. PostgreSQL setup ───────────────────────────────────────────────────────
systemctl start postgresql
systemctl enable postgresql

sudo -u postgres psql <<PGSQL
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$DB_USER') THEN
        CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS';
    END IF;
END
\$\$;
CREATE DATABASE $DB_NAME OWNER $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
PGSQL

# ── 4. Clone repo ─────────────────────────────────────────────────────────────
sudo -u "$APP_USER" bash -c "
    git clone $REPO_URL $APP_DIR || (cd $APP_DIR && git pull)
"

# ── 5. Python venv & dependencies ─────────────────────────────────────────────
sudo -u "$APP_USER" bash -c "
    python3.12 -m venv $VENV_DIR
    $VENV_DIR/bin/pip install --upgrade pip
    $VENV_DIR/bin/pip install \
        django==6.0.4 \
        psycopg2-binary \
        gunicorn \
        whitenoise \
        python-decouple \
        Pillow \
        openpyxl \
        factory-boy \
        pytest-django
"

# ── 6. Copy .env ──────────────────────────────────────────────────────────────
echo ">>> Copy your .env file to $APP_DIR/.env now, then press Enter to continue."
read -r

# ── 7. Django setup ───────────────────────────────────────────────────────────
sudo -u "$APP_USER" bash -c "
    cd $APP_DIR/ERP
    export DJANGO_SETTINGS_MODULE=ERP.settings_production
    $VENV_DIR/bin/python manage.py migrate --noinput
    $VENV_DIR/bin/python manage.py collectstatic --noinput
"

# ── 8. Gunicorn socket directory ──────────────────────────────────────────────
mkdir -p /run/gunicorn
chown "$APP_USER":www-data /run/gunicorn

# ── 9. Log directories ────────────────────────────────────────────────────────
mkdir -p /var/log/gunicorn
chown "$APP_USER":www-data /var/log/gunicorn

# ── 10. Systemd service ───────────────────────────────────────────────────────
cp "$APP_DIR/deploy/systemd/school_erp.service" /etc/systemd/system/school_erp.service
systemctl daemon-reload
systemctl enable school_erp
systemctl start school_erp

# ── 11. Nginx ─────────────────────────────────────────────────────────────────
cp "$APP_DIR/deploy/nginx/school_erp.conf" /etc/nginx/sites-available/school_erp
ln -sf /etc/nginx/sites-available/school_erp /etc/nginx/sites-enabled/school_erp
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

# ── 12. SSL certificate ───────────────────────────────────────────────────────
certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --non-interactive --agree-tos -m "admin@$DOMAIN"
systemctl reload nginx

echo "✓ Deployment complete. Visit https://$DOMAIN"
