from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponseForbidden
from .models import Usuario, Libro, Resena, Prestamo, ListaDeseos, SolicitudContacto
from .forms import (
    RegistroForm, LibroForm, ResenaForm, PrestamoForm,
    ListaDeseosForm, SolicitudContactoForm, BusquedaLibroForm
)


# ====== VISTAS PÚBLICAS ======

def landing(request):
    """Página de aterrizaje con información del producto"""
    return render(request, 'biblioteca/landing.html')


def registro(request):
    """Registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a Bibliandria.')
            return redirect('home')
    else:
        form = RegistroForm()
    
    return render(request, 'biblioteca/registro.html', {'form': form})


def login_view(request):
    """Vista de inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.first_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'biblioteca/login.html')


@login_required
def logout_view(request):
    """Cierre de sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('landing')


# ====== VISTAS DE BIBLIOTECAS ======

@login_required
def home(request):
    """Dashboard principal - Inicio Bibliotecas"""
    context = {
        'total_libros': request.user.libros.count(),
        'libros_recientes': request.user.libros.all()[:5],
        'lista_deseos_count': request.user.lista_deseos.count(),
    }
    return render(request, 'biblioteca/home.html', context)


@login_required
def bibliotecas_publicas(request):
    """Lista de bibliotecas públicas de otros usuarios"""
    usuarios_publicos = Usuario.objects.filter(
        biblioteca_publica=True,
        rol='bibliotecario'
    ).annotate(
        num_libros=Count('libros')
    ).exclude(id=request.user.id)
    
    return render(request, 'biblioteca/bibliotecas_publicas.html', {
        'usuarios': usuarios_publicos
    })


@login_required
def ver_biblioteca(request, username):
    """Ver la biblioteca de un usuario específico"""
    usuario = get_object_or_404(Usuario, username=username)
    
    # Verificar que la biblioteca sea pública o sea el propietario
    if not usuario.biblioteca_publica and usuario != request.user:
        messages.error(request, 'Esta biblioteca es privada.')
        return redirect('bibliotecas_publicas')
    
    # Búsqueda y filtrado
    libros = usuario.libros.all()
    form = BusquedaLibroForm(request.GET)
    
    if form.is_valid() and form.cleaned_data.get('query'):
        query = form.cleaned_data['query']
        libros = libros.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(isbn__icontains=query)
        )
    
    context = {
        'usuario_biblioteca': usuario,
        'libros': libros,
        'form': form,
        'es_propietario': usuario == request.user,
    }
    
    return render(request, 'biblioteca/ver_biblioteca.html', context)


@login_required
def mi_biblioteca(request):
    """Biblioteca personal del usuario autenticado"""
    return ver_biblioteca(request, request.user.username)


# ====== VISTAS DE LIBROS ======

@login_required
def libro_detalle(request, pk):
    """Vista detallada de un libro"""
    libro = get_object_or_404(Libro, pk=pk)
    
    # Verificar acceso
    if libro.propietario != request.user and not libro.propietario.biblioteca_publica:
        return HttpResponseForbidden('No tienes permiso para ver este libro.')
    
    # Formulario de solicitud de contacto solo para visitantes
    solicitud_form = None
    if libro.propietario != request.user:
        if request.method == 'POST':
            solicitud_form = SolicitudContactoForm(request.POST)
            if solicitud_form.is_valid():
                solicitud = solicitud_form.save(commit=False)
                solicitud.visitante = request.user
                solicitud.bibliotecario = libro.propietario
                solicitud.libro = libro
                solicitud.save()
                messages.success(request, 'Solicitud de contacto enviada.')
                return redirect('libro_detalle', pk=pk)
        else:
            solicitud_form = SolicitudContactoForm()
    
    context = {
        'libro': libro,
        'es_propietario': libro.propietario == request.user,
        'solicitud_form': solicitud_form,
    }
    
    return render(request, 'biblioteca/libro_detalle.html', context)


@login_required
def libro_crear(request):
    """Crear un nuevo libro"""
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.propietario = request.user
            libro.save()
            messages.success(request, f'Libro "{libro.titulo}" añadido correctamente.')
            return redirect('libro_detalle', pk=libro.pk)
    else:
        form = LibroForm()
    
    return render(request, 'biblioteca/libro_form.html', {
        'form': form,
        'titulo': 'Añadir Nuevo Libro'
    })


@login_required
def libro_editar(request, pk):
    """Editar un libro existente"""
    libro = get_object_or_404(Libro, pk=pk)
    
    if libro.propietario != request.user:
        return HttpResponseForbidden('No tienes permiso para editar este libro.')
    
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro actualizado correctamente.')
            return redirect('libro_detalle', pk=pk)
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'biblioteca/libro_form.html', {
        'form': form,
        'libro': libro,
        'titulo': f'Editar {libro.titulo}'
    })


@login_required
def libro_eliminar(request, pk):
    """Eliminar un libro"""
    libro = get_object_or_404(Libro, pk=pk)
    
    if libro.propietario != request.user:
        return HttpResponseForbidden('No tienes permiso para eliminar este libro.')
    
    if request.method == 'POST':
        titulo = libro.titulo
        libro.delete()
        messages.success(request, f'Libro "{titulo}" eliminado correctamente.')
        return redirect('mi_biblioteca')
    
    return render(request, 'biblioteca/libro_confirmar_eliminar.html', {'libro': libro})


# ====== VISTAS DE RESEÑAS ======

@login_required
def resena_crear(request, libro_pk):
    """Crear o editar reseña de un libro"""
    libro = get_object_or_404(Libro, pk=libro_pk)
    
    if libro.propietario != request.user:
        return HttpResponseForbidden('Solo puedes reseñar tus propios libros.')
    
    try:
        resena = libro.resena
        es_nuevo = False
    except Resena.DoesNotExist:
        resena = None
        es_nuevo = True
    
    if request.method == 'POST':
        form = ResenaForm(request.POST, instance=resena)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.libro = libro
            resena.save()
            messages.success(request, 'Reseña guardada correctamente.')
            return redirect('libro_detalle', pk=libro_pk)
    else:
        form = ResenaForm(instance=resena)
    
    return render(request, 'biblioteca/resena_form.html', {
        'form': form,
        'libro': libro,
        'es_nuevo': es_nuevo
    })


# ====== VISTAS DE PRÉSTAMOS ======

@login_required
def prestamo_crear(request, libro_pk):
    """Registrar un préstamo"""
    libro = get_object_or_404(Libro, pk=libro_pk)
    
    if libro.propietario != request.user:
        return HttpResponseForbidden('Solo puedes registrar préstamos de tus propios libros.')
    
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.libro = libro
            prestamo.save()
            messages.success(request, 'Préstamo registrado correctamente.')
            return redirect('libro_detalle', pk=libro_pk)
    else:
        form = PrestamoForm()
    
    return render(request, 'biblioteca/prestamo_form.html', {
        'form': form,
        'libro': libro
    })


@login_required
def prestamo_devolver(request, pk):
    """Marcar un préstamo como devuelto"""
    prestamo = get_object_or_404(Prestamo, pk=pk)
    
    if prestamo.libro.propietario != request.user:
        return HttpResponseForbidden('No tienes permiso.')
    
    if request.method == 'POST':
        from datetime import date
        prestamo.fecha_devolucion_real = date.today()
        prestamo.save()
        messages.success(request, 'Préstamo marcado como devuelto.')
        return redirect('libro_detalle', pk=prestamo.libro.pk)
    
    return render(request, 'biblioteca/prestamo_devolver.html', {'prestamo': prestamo})


# ====== VISTAS DE LISTA DE DESEOS ======

@login_required
def lista_deseos(request):
    """Ver lista de deseos del usuario"""
    if request.method == 'POST':
        form = ListaDeseosForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.usuario = request.user
            item.save()
            messages.success(request, 'Libro añadido a tu lista de deseos.')
            return redirect('lista_deseos')
    else:
        form = ListaDeseosForm()
    
    items = request.user.lista_deseos.all()
    
    return render(request, 'biblioteca/lista_deseos.html', {
        'items': items,
        'form': form
    })


@login_required
def lista_deseos_eliminar(request, pk):
    """Eliminar un item de la lista de deseos"""
    item = get_object_or_404(ListaDeseos, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item eliminado de tu lista de deseos.')
        return redirect('lista_deseos')
    
    return render(request, 'biblioteca/lista_deseos_eliminar.html', {'item': item})


# ====== VISTAS DE ADMINISTRACIÓN ======

@login_required
def usuarios_lista(request):
    """Lista de usuarios (solo para admins)"""
    if not request.user.es_admin():
        return HttpResponseForbidden('No tienes permiso para acceder a esta página.')
    
    usuarios = Usuario.objects.all().annotate(num_libros=Count('libros'))
    
    return render(request, 'biblioteca/usuarios_lista.html', {
        'usuarios': usuarios
    })


@login_required
def usuario_cambiar_privacidad(request, pk):
    """Cambiar la privacidad de la biblioteca de un usuario (admin)"""
    if not request.user.es_admin():
        return HttpResponseForbidden('No tienes permiso.')
    
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario.biblioteca_publica = not usuario.biblioteca_publica
    usuario.save()
    
    estado = 'pública' if usuario.biblioteca_publica else 'privada'
    messages.success(request, f'Biblioteca de {usuario.username} marcada como {estado}.')
    
    return redirect('usuarios_lista')


@login_required
def configuracion(request):
    """Configuración de la cuenta del usuario"""
    if request.method == 'POST':
        # Cambiar visibilidad de la biblioteca
        if 'cambiar_privacidad' in request.POST:
            request.user.biblioteca_publica = not request.user.biblioteca_publica
            request.user.save()
            estado = 'pública' if request.user.biblioteca_publica else 'privada'
            messages.success(request, f'Tu biblioteca ahora es {estado}.')
    
    return render(request, 'biblioteca/configuracion.html')
