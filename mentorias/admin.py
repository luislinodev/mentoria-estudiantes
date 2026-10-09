from django.contrib import admin

from .models import Especialidad, OfertaMentor, Sesion, Solicitud, Valoracion


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(OfertaMentor)
class OfertaMentorAdmin(admin.ModelAdmin):
    list_display = ("perfil", "activo", "calificacion_promedio", "total_valoraciones")
    list_filter = ("activo", "especialidades")
    search_fields = ("perfil__usuario__first_name", "perfil__usuario__email")
    filter_horizontal = ("especialidades",)


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ("aprendiz", "mentor", "especialidad", "estado", "fecha_propuesta", "creado")
    list_filter = ("estado", "especialidad")
    search_fields = ("aprendiz__email", "mentor__email")


@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ("mentor", "aprendiz", "inicio", "estado", "recordatorio_enviado")
    list_filter = ("estado",)
    search_fields = ("mentor__email", "aprendiz__email")


@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ("mentor", "aprendiz", "estrellas", "creado")
    list_filter = ("estrellas",)
