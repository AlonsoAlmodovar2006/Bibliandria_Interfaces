# 📚 Bibliandria - Gestor de Bibliotecas Personales

![Django](https://img.shields.io/badge/Django-5.0-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-Academic-yellow)

**Bibliandria** es una aplicación web de gestión digital de bibliotecas personales desarrollada con Django. Permite a los usuarios organizar su colección de libros, llevar un registro de sus lecturas, gestionar préstamos y compartir su biblioteca con otros usuarios.

---

## 📋 Índice

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Características](#-características)
- [Roles de Usuario](#-roles-de-usuario)
- [Historias de Usuario](#-historias-de-usuario)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Información Académica](#-información-académica)
- [Autor](#-autor)

---

## 📖 Descripción del Proyecto

Bibliandria es un software de gestión digital de bibliotecas personales que permite:

- **Gestionar colecciones de libros** con información detallada (título, autor, ISBN, editorial, etc.)
- **Añadir reseñas y puntuaciones personales** para cada libro
- **Registrar préstamos** para llevar un control de qué libros están prestados
- **Crear listas de deseos** para planificar futuras compras
- **Compartir bibliotecas** con otros usuarios o mantenerlas privadas
- **Explorar bibliotecas públicas** de otros usuarios

Este proyecto ha sido desarrollado como práctica para la asignatura **Diseño de Interfaces** del ciclo de **Desarrollo de Aplicaciones Web (DAW)**.

---

## ✨ Características

### Gestión de Libros
- ✅ Añadir, editar y eliminar libros
- ✅ Subir portadas de libros
- ✅ Información completa: título, autor, ISBN, editorial, año, páginas
- ✅ Estados del libro: nuevo, como nuevo, usado, deteriorado
- ✅ Formatos: tapa dura, tapa blanda, bolsillo, ebook, audiolibro
- ✅ Búsqueda por título, autor o ISBN

### Reseñas y Valoraciones
- ✅ Puntuación de 1 a 5 estrellas
- ✅ Comentarios personales
- ✅ Fecha de lectura

### Gestión de Préstamos
- ✅ Registro de préstamos con nombre del prestatario
- ✅ Fechas de préstamo y devolución esperada
- ✅ Control de libros prestados actualmente
- ✅ Historial completo de préstamos

### Lista de Deseos
- ✅ Añadir libros deseados con prioridad
- ✅ Notas sobre dónde encontrarlos o por qué adquirirlos
- ✅ Organización por prioridad

### Control de Privacidad
- ✅ Bibliotecas públicas o privadas
- ✅ Explorar bibliotecas de otros usuarios
- ✅ Solicitar contacto con otros bibliotecarios

### Panel de Administración
- ✅ Gestión de usuarios
- ✅ Control de privacidad de bibliotecas
- ✅ Acceso completo al sistema

---

## 👥 Roles de Usuario

### 🔴 Admin
- Gestiona todos los usuarios del sistema
- Accede y modifica todas las bibliotecas
- Cambia la privacidad de las bibliotecas
- Mantiene la base de datos limpia y organizada

### 🔵 Bibliotecario
- Registra y gestiona sus libros
- Añade reseñas y puntuaciones
- Controla préstamos
- Decide si su biblioteca es pública o privada
- Gestiona su lista de deseos

### ⚪ Visitante
- Explora bibliotecas públicas
- Envía solicitudes de contacto a bibliotecarios
- Puede convertirse en bibliotecario registrándose

---

## 📝 Historias de Usuario

### Admin
- ✅ Como admin, quiero ver los usuarios y sus bibliotecas para poder gestionarlos
- ✅ Como admin, quiero mantener la base de datos limpia y organizada

### Bibliotecario
- ✅ Como bibliotecario, quiero registrar mis libros para poder gestionarlos
- ✅ Como bibliotecario, quiero marcar mi biblioteca como privada o pública
- ✅ Como bibliotecario, quiero añadir reseñas y puntuaciones personales
- ✅ Como bibliotecario, quiero registrar préstamos de libros
- ✅ Como bibliotecario, quiero crear una lista de "Libros deseados"

### Visitante
- ✅ Como visitante, quiero ver las bibliotecas de otros usuarios
- ✅ Como visitante, quiero enviar solicitudes de contacto a bibliotecarios

---

## 🛠️ Tecnologías

- **Backend**: Django 5.0
- **Base de Datos**: SQLite (desarrollo)
- **Frontend**: HTML5, CSS3, Bootstrap 5.3
- **Iconos**: Bootstrap Icons
- **Lenguaje**: Python 3.10+

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd Repositorio
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar el entorno virtual**
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Aplicar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario (admin)**
```bash
python manage.py createsuperuser
```

7. **Ejecutar el servidor de desarrollo**
```bash
python manage.py runserver
```

### 🌐 Despliegue en Producción

Para desplegar la aplicación en un servidor Ubuntu sin contenedores:

- 📖 **Guía completa**: Ver [DEPLOY.md](DEPLOY.md)
- 🚀 **Script automático**: Usar [deploy.sh](deploy.sh)
- 📦 **Transferencia**: Ver [TRANSFER.md](TRANSFER.md)

```bash
# Ejemplo rápido
scp deploy.sh usuario@servidor:~/
ssh usuario@servidor
chmod +x deploy.sh && ./deploy.sh
```

8. **Acceder a la aplicación**
- Aplicación: http://localhost:8000
- Panel de administración: http://localhost:8000/admin

---

## 📱 Uso

### Primera Vez

1. **Accede a la landing page** en http://localhost:8000
2. **Regístrate** como nuevo usuario (automáticamente serás bibliotecario)
3. **Añade tu primer libro** desde el botón "Nuevo Libro"
4. **Configura la privacidad** de tu biblioteca desde Configuración

### Como Bibliotecario

- **Añadir libros**: Navega a "Nuevo Libro" y completa el formulario
- **Gestionar biblioteca**: Accede a "Mi Biblioteca" para ver todos tus libros
- **Añadir reseñas**: Desde el detalle de cada libro, añade tu puntuación
- **Registrar préstamos**: Marca cuando prestas un libro y a quién
- **Lista de deseos**: Añade libros que quieras comprar en el futuro

### Como Admin

1. Accede al panel de administración en `/admin`
2. Gestiona usuarios, cambia roles y privacidad
3. Accede a "Usuarios" desde el menú principal para gestión rápida

### Explorar Bibliotecas

- Navega a "Bibliotecas" para ver usuarios con bibliotecas públicas
- Explora sus colecciones
- Envía solicitudes de contacto sobre libros específicos

---

## 📁 Estructura del Proyecto

```
Repositorio/
├── bibliandria/              # Configuración del proyecto Django
│   ├── settings.py           # Configuración principal
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # WSGI para producción
├── biblioteca/               # Aplicación principal
│   ├── models.py             # Modelos de datos
│   ├── views.py              # Vistas
│   ├── urls.py               # URLs de la app
│   ├── forms.py              # Formularios
│   └── admin.py              # Configuración del admin
├── templates/                # Templates HTML
│   ├── base.html             # Template base
│   └── biblioteca/           # Templates de la app
├── static/                   # Archivos estáticos (CSS, JS)
├── media/                    # Archivos subidos (portadas)
├── Wiki/                     # Documentación del proyecto
│   └── Home.md               # Historias de usuario
├── wireframes.excalidraw     # Diseños de interfaz
├── manage.py                 # Utilidad de Django
├── requirements.txt          # Dependencias
└── README.md                 # Este archivo
```

---

## 🖼️ Capturas de Pantalla

### Landing Page
Página principal con información del producto y funcionalidades destacadas.

### Mi Biblioteca
Vista de todos los libros del usuario con opciones de búsqueda y filtrado.

### Detalle de Libro
Información completa del libro, reseña personal y gestión de préstamos.

### Bibliotecas Públicas
Exploración de bibliotecas de otros usuarios.

### Panel de Administración
Gestión completa de usuarios y permisos.

---

## 🎓 Información Académica

**Asignatura**: Diseño de Interfaces  
**Ciclo**: 2º Desarrollo de Aplicaciones Web (DAW)  
**Curso**: 2025-2026  
**Tipo**: Proyecto de práctica educativo

### Objetivos de Aprendizaje

- ✅ Diseño de interfaces web usables y accesibles
- ✅ Implementación de wireframes en aplicaciones reales
- ✅ Desarrollo con framework Django
- ✅ Gestión de roles y permisos de usuario
- ✅ Sistema CRUD completo
- ✅ Diseño responsive con Bootstrap
- ✅ Historias de usuario y casos de uso

---

## 👨‍💻 Autor

Proyecto desarrollado para la asignatura de Diseño de Interfaces.

---

## 📄 Licencia

Este proyecto es de carácter académico y educativo. Desarrollado como práctica para 2º DAW.

---

## 🤝 Contribuciones

Este es un proyecto educativo. Las sugerencias y mejoras son bienvenidas para fines de aprendizaje.

---

## 📧 Contacto

Para cualquier consulta sobre el proyecto académico, contacta a través de tu profesor de Diseño de Interfaces.

---

## 🔮 Futuras Mejoras

- [ ] Integración con API de Google Books para autocompletar información
- [ ] Sistema de etiquetas y categorías
- [ ] Gráficos de estadísticas de lectura
- [ ] Exportación de biblioteca a PDF
- [ ] Sistema de mensajería entre usuarios
- [ ] Aplicación móvil

---

**¡Gracias por revisar Bibliandria!** 📚✨

