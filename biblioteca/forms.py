from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Libro, Resena, Prestamo, ListaDeseos, SolicitudContacto


class RegistroForm(UserCreationForm):
    """Formulario de registro de usuario"""
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellidos')
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: maria_garcia',
                'autocomplete': 'username',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: María',
            'autocomplete': 'given-name',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: García López',
            'autocomplete': 'family-name',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: maria@ejemplo.com',
            'autocomplete': 'email',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repite tu contraseña',
            'autocomplete': 'new-password',
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.rol = 'bibliotecario'  # Por defecto, los usuarios registrados son bibliotecarios
        if commit:
            user.save()
        return user


class LibroForm(forms.ModelForm):
    """Formulario para añadir/editar libros"""
    class Meta:
        model = Libro
        fields = [
            'titulo', 'autor', 'isbn', 'editorial', 'año_publicacion',
            'descripcion', 'portada', 'numero_paginas', 'estado', 'formato'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'año_publicacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'numero_paginas': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'formato': forms.Select(attrs={'class': 'form-control'}),
        }


class ResenaForm(forms.ModelForm):
    """Formulario para añadir/editar reseñas"""
    class Meta:
        model = Resena
        fields = ['puntuacion', 'comentario', 'fecha_lectura']
        widgets = {
            'puntuacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'fecha_lectura': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class PrestamoForm(forms.ModelForm):
    """Formulario para registrar préstamos"""
    class Meta:
        model = Prestamo
        fields = [
            'nombre_prestatario', 'fecha_prestamo',
            'fecha_devolucion_esperada', 'notas'
        ]
        widgets = {
            'nombre_prestatario': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_prestamo': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_devolucion_esperada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ListaDeseosForm(forms.ModelForm):
    """Formulario para la lista de deseos"""
    class Meta:
        model = ListaDeseos
        fields = ['titulo', 'autor', 'isbn', 'notas', 'prioridad']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
        }


class SolicitudContactoForm(forms.ModelForm):
    """Formulario para enviar solicitudes de contacto"""
    class Meta:
        model = SolicitudContacto
        fields = ['mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe tu mensaje al bibliotecario...'
            }),
        }


class BusquedaLibroForm(forms.Form):
    """Formulario para búsqueda de libros"""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título, ISBN o autor...'
        })
    )
