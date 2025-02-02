from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detalles_obra/<int:id_obra>/', views.detalles_obra, name='detalles_obra'), 
    
    
    path('perfil/', views.acceso, name='acceso'),  # Perfil propio (requiere login)
    path('perfil/<str:cedula>/', views.acceso, name='perfil_artista'),  # Perfil público del artista

    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    path('editperfil/', views.edit_perfil, name='edit_perfil'),
    path('subir_obras/', views.subir_obras, name='subir_obras'),
    path('cambiar_plan/', views.cambiar_plan, name='cambiar_plan'),
]
