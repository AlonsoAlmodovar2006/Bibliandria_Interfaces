# 🚀 Guía Rápida de Inicio - Bibliandria

## Instalación Rápida

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear base de datos
python manage.py makemigrations
python manage.py migrate

# 4. Crear superusuario
python manage.py createsuperuser

# 5. Ejecutar servidor
python manage.py runserver
```

## Acceso

- **Aplicación**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

## Usuarios de Prueba (después de crear superusuario)

Para crear usuarios de prueba desde el shell de Django:

```bash
python manage.py shell
```

```python
from biblioteca.models import Usuario

# Crear bibliotecario
biblio = Usuario.objects.create_user(
    username='bibliotecario1',
    email='biblio@test.com',
    password='test1234',
    first_name='Juan',
    last_name='Pérez',
    rol='bibliotecario',
    biblioteca_publica=True
)

# Crear visitante
visitante = Usuario.objects.create_user(
    username='visitante1',
    email='visitante@test.com',
    password='test1234',
    first_name='María',
    last_name='García',
    rol='visitante'
)
```

## Comandos Útiles

```bash
# Crear nuevas migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell interactivo
python manage.py shell

# Recopilar archivos estáticos
python manage.py collectstatic
```

## Estructura de URLs

- `/` - Landing page
- `/home/` - Dashboard (requiere login)
- `/mi-biblioteca/` - Mi biblioteca
- `/bibliotecas/` - Bibliotecas públicas
- `/biblioteca/<username>/` - Ver biblioteca de usuario
- `/libro/nuevo/` - Añadir libro
- `/libro/<id>/` - Detalle de libro
- `/usuarios/` - Gestión de usuarios (admin)
- `/admin/` - Panel de administración Django

## Roles y Permisos

### Admin
- Acceso completo al sistema
- Gestión de usuarios
- Cambiar privacidad de bibliotecas

### Bibliotecario
- Gestionar su biblioteca
- Añadir/editar/eliminar libros
- Crear reseñas y préstamos
- Control de privacidad

### Visitante
- Ver bibliotecas públicas
- Enviar solicitudes de contacto

## Problemas Comunes

### Error de migraciones
```bash
python manage.py migrate --run-syncdb
```

### Puerto en uso
```bash
python manage.py runserver 8080
```

### Reiniciar base de datos
```bash
# CUIDADO: Esto borrará todos los datos
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Desarrollo

### Añadir nuevos modelos
1. Editar `biblioteca/models.py`
2. `python manage.py makemigrations`
3. `python manage.py migrate`

### Añadir nuevas vistas
1. Editar `biblioteca/views.py`
2. Añadir URL en `biblioteca/urls.py`
3. Crear template en `templates/biblioteca/`

## Contacto de Soporte

Para dudas sobre el proyecto, consulta con tu profesor de Diseño de Interfaces.
