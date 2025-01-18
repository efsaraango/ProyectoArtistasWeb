from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),           # Ruta para el inicio
    path('login/', views.login_view, name='login'),     # Ruta para el login
    path('registro/', views.registro, name='registro'),  # Ruta para el registro
    path('mostrar/', views.mostrar_artistas, name='mostrar'),
    path('acceso/', views.acceso, name='acceso'),  # Ruta de acceso después de un login exitoso
    path('logout/', views.logout_view, name='logout'),
    path('editperfil/', views.edit_perfil, name='edit_perfil'),
]