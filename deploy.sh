#!/bin/bash

# ============================================
# Script de Despliegue - Bibliandria
# Ubuntu Server 25.10
# ============================================

set -e  # Salir si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración
APP_NAME="bibliandria"
APP_DIR="/home/diego/apps/$APP_NAME"
REPO_URL="https://github.com/AlonsoAlmodovar2006/Bibliandria_Interfaces.git"
DOMAIN_OR_IP="192.168.5.55"
USER="alonso"
VENV_PATH="$APP_DIR/venv"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Despliegue de Bibliandria${NC}"
echo -e "${GREEN}========================================${NC}\n"

# 1. Actualizar sistema
echo -e "${YELLOW}[1/12] Actualizando sistema...${NC}"
sudo apt update
sudo apt upgrade -y

# 2. Instalar dependencias del sistema
echo -e "${YELLOW}[2/12] Instalando dependencias del sistema...${NC}"
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    nginx \
    git \
    libjpeg-dev \
    zlib1g-dev \
    build-essential \
    curl

# 3. Crear directorio de la aplicación
echo -e "${YELLOW}[3/12] Creando directorio de aplicación...${NC}"
mkdir -p /home/diego/apps
mkdir -p $APP_DIR

# 4. Clonar o actualizar repositorio
echo -e "${YELLOW}[4/12] Clonando/actualizando repositorio...${NC}"
if [ -d "$APP_DIR/.git" ]; then
    echo "Repositorio existe, actualizando..."
    cd $APP_DIR
    git pull
else
    echo "Clonando repositorio..."
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

# 5. Crear y activar entorno virtual
echo -e "${YELLOW}[5/12] Creando entorno virtual...${NC}"
python3 -m venv $VENV_PATH
source $VENV_PATH/bin/activate

# 6. Instalar dependencias de Python
echo -e "${YELLOW}[6/12] Instalando dependencias de Python...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# 7. Generar SECRET_KEY aleatoria
echo -e "${YELLOW}[7/12] Generando configuración de producción...${NC}"
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Crear archivo de configuración de producción si no existe
if [ ! -f "$APP_DIR/bibliandria/settings_prod.py" ]; then
    cat > "$APP_DIR/bibliandria/settings_prod.py" << EOF
from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['$DOMAIN_OR_IP', 'alonsoServer', 'localhost', '127.0.0.1']

SECRET_KEY = '$SECRET_KEY'

# Archivos estáticos
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Seguridad
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
EOF
    echo -e "${GREEN}✓ Archivo settings_prod.py creado${NC}"
fi

# Crear directorio de logs
mkdir -p $APP_DIR/logs

# 8. Recopilar archivos estáticos
echo -e "${YELLOW}[8/12] Recopilando archivos estáticos...${NC}"
python manage.py collectstatic --settings=bibliandria.settings_prod --noinput

# 9. Aplicar migraciones
echo -e "${YELLOW}[9/12] Aplicando migraciones de base de datos...${NC}"
python manage.py migrate --settings=bibliandria.settings_prod --noinput

# Desactivar entorno virtual
deactivate

# 10. Configurar servicio systemd para Gunicorn
echo -e "${YELLOW}[10/12] Configurando servicio Gunicorn...${NC}"
sudo tee /etc/systemd/system/$APP_NAME.service > /dev/null << EOF
[Unit]
Description=Bibliandria Gunicorn daemon
After=network.target

[Service]
Type=notify
User=$USER
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_PATH/bin"
Environment="DJANGO_SETTINGS_MODULE=bibliandria.settings_prod"
ExecStart=$VENV_PATH/bin/gunicorn \\
    --workers 3 \\
    --bind unix:/run/$APP_NAME.sock \\
    --access-logfile $APP_DIR/logs/gunicorn-access.log \\
    --error-logfile $APP_DIR/logs/gunicorn-error.log \\
    bibliandria.wsgi:application

ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# 11. Configurar Nginx
echo -e "${YELLOW}[11/12] Configurando Nginx...${NC}"
sudo tee /etc/nginx/sites-available/$APP_NAME > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN_OR_IP alonsoServer;

    client_max_body_size 20M;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        alias $APP_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias $APP_DIR/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    location /videos/ {
        alias $APP_DIR/videos/;
        expires 30d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/$APP_NAME.sock;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_redirect off;
    }

    # Logs
    access_log $APP_DIR/logs/nginx-access.log;
    error_log $APP_DIR/logs/nginx-error.log;
}
EOF

# Habilitar sitio de Nginx
sudo ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Verificar configuración de Nginx
sudo nginx -t

# 12. Configurar permisos
echo -e "${YELLOW}[12/12] Configurando permisos...${NC}"
sudo chown -R $USER:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo chmod -R 775 $APP_DIR/media
sudo chmod -R 775 $APP_DIR/logs
sudo chmod 664 $APP_DIR/db.sqlite3

# Iniciar y habilitar servicios
echo -e "${YELLOW}Iniciando servicios...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME
sudo systemctl restart $APP_NAME
sudo systemctl restart nginx

# Verificar estado de servicios
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  Estado de Servicios${NC}"
echo -e "${GREEN}========================================${NC}"

if sudo systemctl is-active --quiet $APP_NAME; then
    echo -e "${GREEN}✓ Gunicorn: ACTIVO${NC}"
else
    echo -e "${RED}✗ Gunicorn: INACTIVO${NC}"
    echo "Ver logs: sudo journalctl -u $APP_NAME -n 50"
fi

if sudo systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx: ACTIVO${NC}"
else
    echo -e "${RED}✗ Nginx: INACTIVO${NC}"
    echo "Ver logs: sudo tail -f /var/log/nginx/error.log"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  ¡Despliegue Completado!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}Accede a tu aplicación en:${NC}"
echo -e "  → http://$DOMAIN_OR_IP"
echo -e "  → http://alonsoServer"
echo -e "\n${YELLOW}Comandos útiles:${NC}"
echo -e "  Ver logs Gunicorn:  sudo journalctl -u $APP_NAME -f"
echo -e "  Ver logs Nginx:     sudo tail -f $APP_DIR/logs/nginx-error.log"
echo -e "  Reiniciar app:      sudo systemctl restart $APP_NAME"
echo -e "  Reiniciar Nginx:    sudo systemctl restart nginx"
echo -e "\n${YELLOW}Siguiente paso:${NC}"
echo -e "  Crear superusuario: cd $APP_DIR && source venv/bin/activate && python manage.py createsuperuser --settings=bibliandria.settings_prod"
echo -e "\n"
