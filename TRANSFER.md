# 📦 Guía Rápida de Transferencia y Despliegue

## Opción 1: Transferir el script desde Windows (Recomendado)

### 1. Desde PowerShell en Windows:

```powershell
# Navega al directorio del proyecto
cd "C:\2ºDAW\Diseño de Interfaces\4-Usabilidad\Bibliandria\Repositorio"

# Transfiere el script al servidor
scp deploy.sh diego@192.168.5.55:~/
scp update.sh diego@192.168.5.55:~/
```

### 2. Conecta al servidor:

```powershell
ssh diego@192.168.5.55
```

### 3. En el servidor Ubuntu, ejecuta:

```bash
chmod +x deploy.sh update.sh
./deploy.sh
```

---

## Opción 2: Usar Git directamente en el servidor

### 1. Conecta al servidor:

```powershell
ssh diego@192.168.5.55
```

### 2. El script automáticamente clonará el repositorio

```bash
# Si no tienes el script, descárgalo primero:
wget https://raw.githubusercontent.com/AlonsoAlmodovar2006/Bibliandria_Interfaces/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

---

## Opción 3: Copia manual del script

### Desde Windows PowerShell:

```powershell
# Conecta y copia el contenido
ssh diego@192.168.5.55

# Una vez conectado, crea el archivo:
nano deploy.sh
# Pega el contenido del script (Ctrl+Shift+V)
# Guarda con Ctrl+O, Enter, y sal con Ctrl+X

# Dale permisos y ejecútalo:
chmod +x deploy.sh
./deploy.sh
```

---

## 🎯 Después del Despliegue

### Crear superusuario:

```bash
cd /home/diego/apps/bibliandria
source venv/bin/activate
python manage.py createsuperuser --settings=bibliandria.settings_prod
```

Datos sugeridos:
- Username: admin
- Email: admin@bibliandria.local
- Password: (elige una segura)

### Acceder a la aplicación:

Abre tu navegador en:
- **http://192.168.5.55**
- **http://192.168.5.55/admin** (panel de administración)

---

## 🔍 Verificar que todo funciona

```bash
# Ver estado de servicios
sudo systemctl status bibliandria
sudo systemctl status nginx

# Ver logs en tiempo real
sudo journalctl -u bibliandria -f
```

---

## ⚙️ Actualizar la aplicación después de hacer cambios

### Desde tu máquina Windows:

```powershell
# 1. Commit y push tus cambios
git add .
git commit -m "Descripción de cambios"
git push origin main
```

### En el servidor Ubuntu:

```bash
# Opción A: Script automático
cd /home/diego/apps/bibliandria
./update.sh

# Opción B: Manual
cd /home/diego/apps/bibliandria
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=bibliandria.settings_prod
python manage.py collectstatic --settings=bibliandria.settings_prod --noinput
sudo systemctl restart bibliandria
```

---

## 🆘 Solución de Problemas Comunes

### Error: "Permission denied"

```bash
# Dale permisos al script
chmod +x deploy.sh
```

### Error: "sudo: command not found" o "Permission denied"

```bash
# Cambia al usuario root temporalmente
su -
# Password: Prieto*2

# Luego ejecuta el script
exit  # Volver a diego
sudo ./deploy.sh
```

### La aplicación no carga

```bash
# Verifica los logs
sudo journalctl -u bibliandria -n 50
sudo tail -f /home/diego/apps/bibliandria/logs/nginx-error.log
```

### Error 502 Bad Gateway

```bash
# Reinicia los servicios
sudo systemctl restart bibliandria
sudo systemctl restart nginx
```

### No puedes acceder desde Windows

```bash
# En el servidor, verifica el firewall
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow from 192.168.5.0/24
```

---

## 📝 Notas Importantes

1. **El script es idempotente**: Puedes ejecutarlo múltiples veces sin problemas
2. **Backups automáticos**: No se realizan backups automáticos, hazlos manualmente antes de actualizaciones importantes
3. **SECRET_KEY**: Se genera automáticamente una nueva en cada ejecución del script
4. **Base de datos**: Usa SQLite por defecto, considera PostgreSQL para producción
5. **HTTPS**: No configurado por defecto, añade Let's Encrypt si necesitas SSL

---

## 🔗 Archivos Importantes

- `deploy.sh` - Script principal de despliegue
- `update.sh` - Script de actualización rápida
- `DEPLOY.md` - Documentación completa de despliegue
- `bibliandria/settings_prod.py.example` - Ejemplo de configuración de producción

---

## 💡 Consejos

- Guarda la SECRET_KEY generada en un lugar seguro
- Haz backups regulares de `db.sqlite3`
- Monitorea los logs regularmente
- Actualiza las dependencias periódicamente
- Considera usar PostgreSQL en producción
