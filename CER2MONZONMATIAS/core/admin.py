from django.contrib import admin
from .models import Material, Solicitud

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'descripcion')

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('ciudadano', 'material', 'cantidad', 'fecha_estimada', 'estado', 'operario_asignado')
    list_filter = ('estado', 'material')
    search_fields = ('ciudadano__username', 'material__nombre')