#!/usr/bin/env bash
set -euo pipefail

KEY_PATH=""
SERVER_IP=""
SERVER_USER="ubuntu"
LOCAL_DIR=""
REMOTE_DIR=""
SECRET_KEY=""
ENABLE_HTTPS="0"
SSH_PORT="22"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --key)
      KEY_PATH="$2"
      shift 2
      ;;
    --ip)
      SERVER_IP="$2"
      shift 2
      ;;
    --user)
      SERVER_USER="$2"
      shift 2
      ;;
    --local-dir)
      LOCAL_DIR="$2"
      shift 2
      ;;
    --remote-dir)
      REMOTE_DIR="$2"
      shift 2
      ;;
    --secret-key)
      SECRET_KEY="$2"
      shift 2
      ;;
    --enable-https)
      ENABLE_HTTPS="$2"
      shift 2
      ;;
    --port)
      SSH_PORT="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$KEY_PATH" || -z "$SERVER_IP" || -z "$LOCAL_DIR" || -z "$SECRET_KEY" ]]; then
  echo "Usage:"
  echo "bash scripts/deploy_with_ip.sh --key ~/.ssh/key.pem --ip 1.2.3.4 --local-dir '/absolute/path/to/IT' --secret-key 'your-secret' [--user ubuntu] [--remote-dir /home/ubuntu/uniclub] [--enable-https 0|1] [--port 22]"
  exit 1
fi

if [[ -z "$REMOTE_DIR" ]]; then
  REMOTE_DIR="/home/${SERVER_USER}/uniclub"
fi

if [[ ! -f "$KEY_PATH" ]]; then
  echo "SSH key not found: $KEY_PATH"
  exit 1
fi

if [[ ! -d "$LOCAL_DIR" ]]; then
  echo "Local project directory not found: $LOCAL_DIR"
  exit 1
fi

ssh -p "$SSH_PORT" -i "$KEY_PATH" -o StrictHostKeyChecking=accept-new "${SERVER_USER}@${SERVER_IP}" "mkdir -p '$REMOTE_DIR'"

rsync -avz --delete \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude 'db.sqlite3' \
  -e "ssh -p $SSH_PORT -i \"$KEY_PATH\" -o StrictHostKeyChecking=accept-new" \
  "$LOCAL_DIR/" "${SERVER_USER}@${SERVER_IP}:$REMOTE_DIR/"

ssh -p "$SSH_PORT" -i "$KEY_PATH" "${SERVER_USER}@${SERVER_IP}" \
"set -euo pipefail
if command -v sudo >/dev/null 2>&1; then
  SUDO='sudo'
else
  SUDO=''
fi

if command -v apt >/dev/null 2>&1; then
  \$SUDO apt update
  \$SUDO apt install -y python3 python3-venv python3-pip nginx
elif command -v dnf >/dev/null 2>&1; then
  \$SUDO dnf install -y python3 python3-pip nginx
elif command -v yum >/dev/null 2>&1; then
  \$SUDO yum install -y python3 python3-pip nginx
elif command -v apk >/dev/null 2>&1; then
  \$SUDO apk add --no-cache python3 py3-pip nginx
else
  echo 'No supported package manager found'
  exit 1
fi

cd '$REMOTE_DIR'
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
\$SUDO tee /etc/uniclub.env > /dev/null <<EOF
DJANGO_DEBUG=0
DJANGO_ENABLE_HTTPS=$ENABLE_HTTPS
DJANGO_SECRET_KEY=$SECRET_KEY
DJANGO_ALLOWED_HOSTS=$SERVER_IP
DJANGO_CSRF_TRUSTED_ORIGINS=
EOF
DJANGO_DEBUG=0 DJANGO_ENABLE_HTTPS=$ENABLE_HTTPS DJANGO_SECRET_KEY=\"$SECRET_KEY\" DJANGO_ALLOWED_HOSTS=\"$SERVER_IP\" python3 manage.py migrate
DJANGO_DEBUG=0 DJANGO_ENABLE_HTTPS=$ENABLE_HTTPS DJANGO_SECRET_KEY=\"$SECRET_KEY\" DJANGO_ALLOWED_HOSTS=\"$SERVER_IP\" python3 manage.py collectstatic --noinput
if getent group www-data >/dev/null 2>&1; then
  SERVICE_GROUP='www-data'
elif getent group nginx >/dev/null 2>&1; then
  SERVICE_GROUP='nginx'
else
  SERVICE_GROUP='$SERVER_USER'
fi
\$SUDO tee /etc/systemd/system/uniclub.service > /dev/null <<EOF
[Unit]
Description=UniClub Django Service
After=network.target

[Service]
User=$SERVER_USER
Group=\$SERVICE_GROUP
WorkingDirectory=$REMOTE_DIR
EnvironmentFile=/etc/uniclub.env
ExecStart=$REMOTE_DIR/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 it_site.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF
\$SUDO systemctl daemon-reload
\$SUDO systemctl enable --now uniclub
if [ -d /etc/nginx/sites-available ] && [ -d /etc/nginx/sites-enabled ]; then
  NGINX_CONF_TARGET='/etc/nginx/sites-available/uniclub'
else
  NGINX_CONF_TARGET='/etc/nginx/conf.d/uniclub.conf'
fi
\$SUDO tee \"\$NGINX_CONF_TARGET\" > /dev/null <<EOF
server {
    listen 80;
    server_name $SERVER_IP;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $SERVER_IP;
    }
}
EOF
if [ -d /etc/nginx/sites-available ] && [ -d /etc/nginx/sites-enabled ]; then
  \$SUDO ln -sf /etc/nginx/sites-available/uniclub /etc/nginx/sites-enabled/uniclub
fi
\$SUDO nginx -t
\$SUDO systemctl reload nginx
\$SUDO systemctl status uniclub --no-pager
\$SUDO systemctl status nginx --no-pager
"

echo "Deployment completed: http://$SERVER_IP"
