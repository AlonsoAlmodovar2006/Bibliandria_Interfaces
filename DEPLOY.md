# 🚀 Guía de Despliegue en Ubuntu Server 25.10

## 📋 Información del Servidor

- **IP**: 192.168.5.55
- **Hostname**: alonsoServer
- **Usuario**: diego
- **SO**: Ubuntu Server 25.10

## 🔧 Instalación Automática

### 1. Conectar al servidor

```bash
ssh diego@192.168.5.55
```

### 2. Descargar el script de despliegue

```bash
# Opción A: Si ya tienes el repositorio clonado localmente
# Copia el archivo deploy.sh al servidor usando scp desde tu máquina Windows:
# scp deploy.sh diego@192.168.5.55:~/

# Opción B: Descargar directamente del repositorio
curl -O https://raw.githubusercontent.com/AlonsoAlmodovar2006/Bibliandria_Interfaces/main/deploy.sh
```

### 3. Dar permisos de ejecución y ejecutar

```bash
chmod +x deploy.sh
```

### 4. Ejecutar el script

```bash
./deploy.sh
```

El script hará automáticamente:
- ✅ Actualizar el sistema
- ✅ Instalar todas las dependencias
- ✅ Clonar el repositorio en `/home/diego/apps/bibliandria`
- ✅ Crear entorno virtual e instalar paquetes Python
- ✅ Generar configuración de producción
- ✅ Recopilar archivos estáticos
- ✅ Aplicar migraciones
- ✅ Configurar Gunicorn como servicio
- ✅ Configurar Nginx
- ✅ Iniciar todos los servicios

### 5. Crear superusuario

```bash
cd /home/diego/apps/bibliandria
source venv/bin/activate
python manage.py createsuperuser --settings=bibliandria.settings_prod
```

### 6. Acceder a la aplicación

Abre tu navegador en:
- http://192.168.5.55
- http://alonsoServer (si está configurado en tu DNS/hosts)

## 🔄 Actualizar la Aplicación

Cuando hagas cambios en el código:

```bash
cd /home/diego/apps/bibliandria
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=bibliandria.settings_prod
python manage.py collectstatic --settings=bibliandria.settings_prod --noinput
sudo systemctl restart bibliandria
```

O usa el script de actualización:

```bash
./update.sh
```

## 📊 Comandos Útiles

### Ver logs en tiempo real

```bash
# Logs de Gunicorn
sudo journalctl -u bibliandria -f

# Logs de Nginx
sudo tail -f /home/diego/apps/bibliandria/logs/nginx-error.log

# Logs de Django
tail -f /home/diego/apps/bibliandria/logs/django.log
```

### Gestión de servicios

```bash
# Reiniciar aplicación
sudo systemctl restart bibliandria

# Ver estado
sudo systemctl status bibliandria

# Reiniciar Nginx
sudo systemctl restart nginx

# Ver estado de Nginx
sudo systemctl status nginx
```

### Backup de base de datos

```bash
# Backup
cp /home/diego/apps/bibliandria/db.sqlite3 /home/diego/apps/bibliandria/db.sqlite3.backup_$(date +%Y%m%d_%H%M%S)

# Restaurar
cp /home/diego/apps/bibliandria/db.sqlite3.backup_XXXXXX /home/diego/apps/bibliandria/db.sqlite3
sudo systemctl restart bibliandria
```

## 🔒 Configuración Adicional (Opcional)

### Firewall

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS (si usas SSL)
sudo ufw enable
sudo ufw status
```

### Configurar hostname en tu máquina local

En Windows, edita el archivo: `C:\Windows\System32\drivers\etc\hosts`

Añade:
```
192.168.5.55    alonsoServer
```

### Acceso desde otras máquinas en la red

Asegúrate de que el servidor Ubuntu permite conexiones en el puerto 80:
```bash
sudo ufw allow from 192.168.5.0/24 to any port 80
```

## ⚠️ Solución de Problemas

### Error "Bad Gateway 502"

```bash
# Ver logs
sudo journalctl -u bibliandria -n 50

# Reiniciar servicio
sudo systemctl restart bibliandria
```

### Error de permisos en archivos

```bash
cd /home/diego/apps/bibliandria
sudo chown -R diego:www-data .
sudo chmod -R 755 .
sudo chmod -R 775 media/ logs/
sudo chmod 664 db.sqlite3
```

### Nginx no inicia

```bash
# Verificar configuración
sudo nginx -t

# Ver logs
sudo tail -f /var/log/nginx/error.log
```

### La aplicación no sirve archivos estáticos

```bash
cd /home/diego/apps/bibliandria
source venv/bin/activate
python manage.py collectstatic --settings=bibliandria.settings_prod --noinput
sudo systemctl restart bibliandria
```

## 📁 Estructura en el Servidor

```
/home/diego/apps/bibliandria/
├── bibliandria/           # Configuración Django
│   ├── settings.py
│   ├── settings_prod.py   # Configuración de producción (generada)
│   ├── urls.py
│   └── wsgi.py
├── biblioteca/            # App principal
├── templates/
├── static/
├── staticfiles/           # Archivos estáticos recopilados
├── media/                 # Archivos subidos por usuarios
├── logs/                  # Logs de la aplicación
│   ├── django.log
│   ├── gunicorn-access.log
│   ├── gunicorn-error.log
│   ├── nginx-access.log
│   └── nginx-error.log
├── venv/                  # Entorno virtual
├── db.sqlite3            # Base de datos
├── manage.py
└── requirements.txt
```

## 🔐 Seguridad

- ✅ DEBUG desactivado en producción
- ✅ SECRET_KEY única generada automáticamente
- ✅ ALLOWED_HOSTS configurado
- ✅ Archivos de logs separados
- ✅ Permisos de archivos correctos
- ⚠️ Considera usar HTTPS con Let's Encrypt en producción real
- ⚠️ Cambia las contraseñas por defecto

## 📞 Contacto

Si tienes problemas, revisa los logs primero:
```bash
sudo journalctl -u bibliandria -n 100
```
