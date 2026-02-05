from django.urls import path
from . import views

urlpatterns = [
    # Públicas
    path('', views.landing, name='landing'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard y bibliotecas
    path('home/', views.home, name='home'),
    path('bibliotecas/', views.bibliotecas_publicas, name='bibliotecas_publicas'),
    path('biblioteca/<str:username>/', views.ver_biblioteca, name='ver_biblioteca'),
    path('mi-biblioteca/', views.mi_biblioteca, name='mi_biblioteca'),
    
    # Libros
    path('libro/<int:pk>/', views.libro_detalle, name='libro_detalle'),
    path('libro/nuevo/', views.libro_crear, name='libro_crear'),
    path('libro/<int:pk>/editar/', views.libro_editar, name='libro_editar'),
    path('libro/<int:pk>/eliminar/', views.libro_eliminar, name='libro_eliminar'),
    
    # Reseñas
    path('libro/<int:libro_pk>/resena/', views.resena_crear, name='resena_crear'),
    
    # Préstamos
    path('libro/<int:libro_pk>/prestamo/', views.prestamo_crear, name='prestamo_crear'),
    path('prestamo/<int:pk>/devolver/', views.prestamo_devolver, name='prestamo_devolver'),
    
    # Lista de deseos
    path('lista-deseos/', views.lista_deseos, name='lista_deseos'),
    path('lista-deseos/<int:pk>/eliminar/', views.lista_deseos_eliminar, name='lista_deseos_eliminar'),
    
    # Administración
    path('usuarios/', views.usuarios_lista, name='usuarios_lista'),
    path('usuarios/<int:pk>/privacidad/', views.usuario_cambiar_privacidad, name='usuario_cambiar_privacidad'),
    
    # Configuración
    path('configuracion/', views.configuracion, name='configuracion'),
]
