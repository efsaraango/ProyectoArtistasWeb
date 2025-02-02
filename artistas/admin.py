from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType  # Importar ContentType
from .models import Artista, Obra

class ArtistaAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'correo', 'categoria', 'categoriaplan', 'is_active', 'is_approved')
    search_fields = ('cedula', 'nombre', 'apellido', 'correo')
    list_filter = ('categoria', 'categoriaplan', 'is_active', 'is_approved')
    actions = ['aprobar_artistas']

    def aprobar_artistas(self, request, queryset):
        content_type = ContentType.objects.get_for_model(Artista)
        queryset.update(is_approved=True)

        for artista in queryset:
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=content_type.id,
                object_id=artista.cedula,
                object_repr=str(artista),
                action_flag=2,
                change_message="Aprobación de artistas seleccionados"
            )
        self.message_user(request, f"{queryset.count()} artistas aprobados con éxito.")
    aprobar_artistas.short_description = "Aprobar artistas seleccionados"

admin.site.register(Artista, ArtistaAdmin)

@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ('id_obra', 'nombre_obra', 'categoria', 'ubicacion', 'id_artista')
    search_fields = ('nombre_obra', 'categoria', 'id_artista__nombre')
    list_filter = ('categoria',)

    def get_artista_nombre(self, obj):
        return f"{obj.id_artista.nombre} {obj.id_artista.apellido}"
    get_artista_nombre.short_description = 'Artista'