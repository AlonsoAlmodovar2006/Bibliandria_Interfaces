from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Libro, Resena, Prestamo, ListaDeseos, SolicitudContacto


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Administración personalizada de usuarios"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol', 'biblioteca_publica', 'is_active']
    list_filter = ['rol', 'biblioteca_publica', 'is_active', 'fecha_registro']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Bibliandria', {'fields': ('rol', 'biblioteca_publica')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de Bibliandria', {'fields': ('rol', 'biblioteca_publica')}),
    )


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    """Administración de libros"""
    list_display = ['titulo', 'autor', 'isbn', 'propietario', 'estado', 'formato', 'fecha_agregado']
    list_filter = ['estado', 'formato', 'fecha_agregado', 'propietario']
    search_fields = ['titulo', 'autor', 'isbn', 'editorial']
    date_hierarchy = 'fecha_agregado'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'autor', 'isbn', 'editorial', 'año_publicacion')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'portada', 'numero_paginas')
        }),
        ('Estado y Formato', {
            'fields': ('propietario', 'estado', 'formato')
        }),
    )


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    """Administración de reseñas"""
    list_display = ['libro', 'puntuacion', 'fecha_lectura', 'fecha_creacion']
    list_filter = ['puntuacion', 'fecha_lectura', 'fecha_creacion']
    search_fields = ['libro__titulo', 'comentario']


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    """Administración de préstamos"""
    list_display = [
        'libro', 'nombre_prestatario', 'fecha_prestamo',
        'fecha_devolucion_esperada', 'fecha_devolucion_real', 'esta_prestado'
    ]
    list_filter = ['fecha_prestamo', 'fecha_devolucion_real']
    search_fields = ['libro__titulo', 'nombre_prestatario']
    date_hierarchy = 'fecha_prestamo'


@admin.register(ListaDeseos)
class ListaDeseosAdmin(admin.ModelAdmin):
    """Administración de listas de deseos"""
    list_display = ['titulo', 'autor', 'usuario', 'prioridad', 'fecha_agregado']
    list_filter = ['prioridad', 'fecha_agregado', 'usuario']
    search_fields = ['titulo', 'autor', 'isbn']


@admin.register(SolicitudContacto)
class SolicitudContactoAdmin(admin.ModelAdmin):
    """Administración de solicitudes de contacto"""
    list_display = ['visitante', 'bibliotecario', 'libro', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['visitante__username', 'bibliotecario__username', 'mensaje']
    date_hierarchy = 'fecha_creacion'
