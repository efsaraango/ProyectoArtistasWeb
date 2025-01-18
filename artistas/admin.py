from django.contrib import admin
from .models import Artista

# Definición de la clase personalizada para la administración de Artista
class ArtistaAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'correo', 'categoria', 'categoriaplan', 'is_active')
    search_fields = ('cedula', 'nombre', 'apellido', 'correo')
    list_filter = ('categoria', 'categoriaplan', 'is_active')

# Registrar el modelo Artista con la clase personalizada ArtistaAdmin
admin.site.register(Artista, ArtistaAdmin)