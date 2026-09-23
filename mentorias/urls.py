from django.urls import path

from . import views

app_name = "mentorias"

urlpatterns = [
    path("buscar/", views.buscar_mentores, name="buscar"),
    path("mentores/<int:pk>/", views.detalle_mentor, name="detalle_mentor"),
    path("mentores/<int:mentor_id>/solicitar/", views.crear_solicitud, name="crear_solicitud"),
    path("oferta/", views.editar_oferta, name="editar_oferta"),
    path("solicitudes/", views.solicitudes, name="solicitudes"),
    path("solicitudes/<int:pk>/aceptar/", views.aceptar_solicitud, name="aceptar_solicitud"),
    path("solicitudes/<int:pk>/rechazar/", views.rechazar_solicitud, name="rechazar_solicitud"),
    path("sesiones/", views.sesiones, name="sesiones"),
    path("sesiones/<int:pk>/", views.detalle_sesion, name="detalle_sesion"),
    path("sesiones/<int:pk>/completar/", views.completar_sesion, name="completar_sesion"),
    path("sesiones/<int:pk>/cancelar/", views.cancelar_sesion, name="cancelar_sesion"),
    path("sesiones/<int:pk>/valorar/", views.valorar_sesion, name="valorar"),
]
