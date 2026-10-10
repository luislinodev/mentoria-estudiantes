from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cuentas.models import Carrera
from mentorias.models import Especialidad, OfertaMentor, Sesion, Solicitud, Valoracion

User = get_user_model()


class FlujoMentoriaTests(TestCase):
    def setUp(self):
        self.mentor = User.objects.create_user(
            "mentor", "mentor@example.com", "clave12345", first_name="Ana", last_name="Mentor"
        )
        self.aprendiz = User.objects.create_user(
            "aprendiz", "aprendiz@example.com", "clave12345", first_name="Pablo", last_name="Aprendiz"
        )
        perfil_m = self.mentor.perfil
        perfil_m.es_mentor = True
        perfil_m.perfil_completo = True
        perfil_m.carrera = Carrera.objects.get(nombre="Diseño y Desarrollo de Software")
        perfil_m.ciclo = 8
        perfil_m.save()
        perfil_a = self.aprendiz.perfil
        perfil_a.es_aprendiz = True
        perfil_a.perfil_completo = True
        perfil_a.carrera = Carrera.objects.get(nombre="Diseño y Desarrollo de Software")
        perfil_a.ciclo = 2
        perfil_a.save()
        self.especialidad = Especialidad.objects.create(nombre="Pruebas")
        self.oferta = OfertaMentor.objects.create(perfil=perfil_m, temas="Testing", activo=True)
        self.oferta.especialidades.add(self.especialidad)

    def test_buscar_muestra_mentor(self):
        self.client.force_login(self.aprendiz)
        respuesta = self.client.get(reverse("mentorias:buscar"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Ana Mentor")

    def test_solicitud_sesion_y_valoracion(self):
        self.client.force_login(self.aprendiz)
        inicio = timezone.now() + timedelta(days=1)
        respuesta = self.client.post(
            reverse("mentorias:crear_solicitud", args=[self.oferta.pk]),
            {
                "especialidad": self.especialidad.pk,
                "mensaje": "Ayuda con pruebas.",
                "fecha_propuesta": inicio.strftime("%Y-%m-%dT%H:%M"),
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        solicitud = Solicitud.objects.get()

        self.client.force_login(self.mentor)
        respuesta = self.client.post(
            reverse("mentorias:aceptar_solicitud", args=[solicitud.pk]),
            {
                "inicio": inicio.strftime("%Y-%m-%dT%H:%M"),
                "duracion_minutos": "60",
                "notas": "Ok",
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        sesion = Sesion.objects.get()
        self.client.post(reverse("mentorias:completar_sesion", args=[sesion.pk]))
        sesion.refresh_from_db()
        self.assertEqual(sesion.estado, Sesion.Estado.COMPLETADA)

        self.client.force_login(self.aprendiz)
        respuesta = self.client.post(
            reverse("mentorias:valorar", args=[sesion.pk]),
            {"estrellas": 4, "comentario": "Muy clara la sesión."},
        )
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Valoracion.objects.count(), 1)
        self.oferta.refresh_from_db()
        self.assertEqual(float(self.oferta.calificacion_promedio), 4.0)
