from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Carrera, Perfil


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = [PerfilInline]


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "carrera", "ciclo", "es_mentor", "es_aprendiz", "perfil_completo")
    list_filter = ("es_mentor", "es_aprendiz", "perfil_completo", "carrera")
    search_fields = ("usuario__first_name", "usuario__last_name", "usuario__email", "carrera__nombre")


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ("nombre", "orden")
    ordering = ("orden", "nombre")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
