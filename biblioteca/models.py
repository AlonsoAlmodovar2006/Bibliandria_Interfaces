from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Usuario(AbstractUser):
    """
    Modelo de usuario extendido con roles para Bibliandria.
    Roles: Admin, Bibliotecario, Visitante
    """
    ROLES = [
        ('admin', 'Admin'),
        ('bibliotecario', 'Bibliotecario'),
        ('visitante', 'Visitante'),
    ]
    
    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='visitante',
        verbose_name='Rol'
    )
    
    biblioteca_publica = models.BooleanField(
        default=False,
        verbose_name='Biblioteca Pública',
        help_text='Si está marcado, otros usuarios podrán ver tu biblioteca'
    )
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_full_name()} (@{self.username})"
    
    def es_admin(self):
        return self.rol == 'admin'
    
    def es_bibliotecario(self):
        return self.rol == 'bibliotecario'


class Libro(models.Model):
    """
    Modelo para representar un libro en la biblioteca personal
    """
    ESTADOS = [
        ('nuevo', 'Nuevo'),
        ('como_nuevo', 'Como Nuevo'),
        ('usado_bueno', 'Usado - Buen Estado'),
        ('usado_aceptable', 'Usado - Aceptable'),
        ('deteriorado', 'Deteriorado'),
    ]
    
    FORMATOS = [
        ('tapa_dura', 'Tapa Dura'),
        ('tapa_blanda', 'Tapa Blanda'),
        ('bolsillo', 'Bolsillo'),
        ('ebook', 'eBook'),
        ('audiolibro', 'Audiolibro'),
    ]
    
    # Información básica del libro
    titulo = models.CharField(max_length=300, verbose_name='Título')
    autor = models.CharField(max_length=200, verbose_name='Autor')
    isbn = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        verbose_name='ISBN',
        help_text='Código ISBN de 10 o 13 dígitos'
    )
    editorial = models.CharField(max_length=200, blank=True, verbose_name='Editorial')
    año_publicacion = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Año de Publicación',
        validators=[MinValueValidator(1000), MaxValueValidator(2100)]
    )
    
    # Detalles adicionales
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    portada = models.ImageField(
        upload_to='portadas/',
        blank=True,
        null=True,
        verbose_name='Portada'
    )
    numero_paginas = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Número de Páginas'
    )
    
    # Propietario y estado
    propietario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='libros',
        verbose_name='Propietario'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='usado_bueno',
        verbose_name='Estado'
    )
    formato = models.CharField(
        max_length=20,
        choices=FORMATOS,
        default='tapa_blanda',
        verbose_name='Formato'
    )
    
    # Metadata
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['-fecha_agregado']
    
    def __str__(self):
        return f"{self.titulo} - {self.autor}"


class Resena(models.Model):
    """
    Reseñas personales de libros
    """
    libro = models.OneToOneField(
        Libro,
        on_delete=models.CASCADE,
        related_name='resena',
        verbose_name='Libro'
    )
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Puntuación',
        help_text='Puntuación del 1 al 5'
    )
    comentario = models.TextField(verbose_name='Comentario')
    fecha_lectura = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de Lectura'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
    
    def __str__(self):
        return f"Reseña de {self.libro.titulo} - {self.puntuacion}★"


class Prestamo(models.Model):
    """
    Registro de préstamos de libros
    """
    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='prestamos',
        verbose_name='Libro'
    )
    nombre_prestatario = models.CharField(
        max_length=200,
        verbose_name='Nombre del Prestatario'
    )
    fecha_prestamo = models.DateField(verbose_name='Fecha de Préstamo')
    fecha_devolucion_esperada = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de Devolución Esperada'
    )
    fecha_devolucion_real = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de Devolución Real'
    )
    notas = models.TextField(blank=True, verbose_name='Notas')
    
    class Meta:
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        ordering = ['-fecha_prestamo']
    
    def __str__(self):
        return f"{self.libro.titulo} prestado a {self.nombre_prestatario}"
    
    @property
    def esta_prestado(self):
        """Devuelve True si el libro está actualmente prestado"""
        return self.fecha_devolucion_real is None


class ListaDeseos(models.Model):
    """
    Lista de libros deseados para futuras compras
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='lista_deseos',
        verbose_name='Usuario'
    )
    titulo = models.CharField(max_length=300, verbose_name='Título')
    autor = models.CharField(max_length=200, verbose_name='Autor')
    isbn = models.CharField(max_length=13, blank=True, verbose_name='ISBN')
    notas = models.TextField(
        blank=True,
        verbose_name='Notas',
        help_text='Razones para adquirir este libro, dónde encontrarlo, etc.'
    )
    prioridad = models.IntegerField(
        choices=[(1, 'Baja'), (2, 'Media'), (3, 'Alta')],
        default=2,
        verbose_name='Prioridad'
    )
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Lista de Deseos'
        verbose_name_plural = 'Listas de Deseos'
        ordering = ['-prioridad', '-fecha_agregado']
    
    def __str__(self):
        return f"{self.titulo} - {self.autor}"


class SolicitudContacto(models.Model):
    """
    Solicitudes de contacto de visitantes a bibliotecarios
    """
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('respondida', 'Respondida'),
        ('cerrada', 'Cerrada'),
    ]
    
    visitante = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='solicitudes_enviadas',
        verbose_name='Visitante'
    )
    bibliotecario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='solicitudes_recibidas',
        verbose_name='Bibliotecario'
    )
    libro = models.ForeignKey(
        Libro,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Libro de Interés'
    )
    mensaje = models.TextField(verbose_name='Mensaje')
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente',
        verbose_name='Estado'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Solicitud de Contacto'
        verbose_name_plural = 'Solicitudes de Contacto'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Solicitud de {self.visitante.username} a {self.bibliotecario.username}"
