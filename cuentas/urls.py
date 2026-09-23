from django.urls import path

from . import views

app_name = "cuentas"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("perfil/", views.mi_perfil, name="mi_perfil"),
    path("perfil/completar/", views.completar_perfil, name="completar_perfil"),
    path("despues-login/", views.despues_login, name="despues_login"),
]
