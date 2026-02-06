#!/bin/bash

# ============================================
# Script de Actualización - Bibliandria
# ============================================

set -e

APP_NAME="bibliandria"
APP_DIR="/home/diego/apps/$APP_NAME"
VENV_PATH="$APP_DIR/venv"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Actualizando Bibliandria...${NC}\n"

cd $APP_DIR

# 1. Actualizar código
echo -e "${YELLOW}[1/5] Actualizando código desde Git...${NC}"
git pull

# 2. Activar entorno virtual
source $VENV_PATH/bin/activate

# 3. Actualizar dependencias
echo -e "${YELLOW}[2/5] Actualizando dependencias...${NC}"
pip install -r requirements.txt

# 4. Aplicar migraciones
echo -e "${YELLOW}[3/5] Aplicando migraciones...${NC}"
python manage.py migrate --settings=bibliandria.settings_prod --noinput

# 5. Recopilar archivos estáticos
echo -e "${YELLOW}[4/5] Recopilando archivos estáticos...${NC}"
python manage.py collectstatic --settings=bibliandria.settings_prod --noinput

deactivate

# 6. Reiniciar servicio
echo -e "${YELLOW}[5/5] Reiniciando servicio...${NC}"
sudo systemctl restart $APP_NAME

echo -e "\n${GREEN}✓ Actualización completada${NC}"
echo -e "Ver logs: sudo journalctl -u $APP_NAME -f\n"
