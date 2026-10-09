from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from cuentas.models import Perfil
from mentorias.models import Especialidad, OfertaMentor

User = get_user_model()


class Command(BaseCommand):
    help = "Crea usuarios de prueba (mentor y aprendiz) para desarrollo local."

    def handle(self, *args, **options):
        mentor, created_m = User.objects.get_or_create(
            username="mentor.demo",
            defaults={
                "email": "mentor.demo@example.com",
                "first_name": "Lucía",
                "last_name": "Ramírez",
            },
        )
        if created_m or not mentor.has_usable_password():
            mentor.set_password("demo1234")
            mentor.save()

        aprendiz, created_a = User.objects.get_or_create(
            username="aprendiz.demo",
            defaults={
                "email": "aprendiz.demo@example.com",
                "first_name": "Diego",
                "last_name": "Quispe",
            },
        )
        if created_a or not aprendiz.has_usable_password():
            aprendiz.set_password("demo1234")
            aprendiz.save()

        perfil_m, _ = Perfil.objects.get_or_create(usuario=mentor)
        perfil_m.ciclo = 8
        perfil_m.carrera = "Ingeniería de Software"
        perfil_m.biografia = "Estudiante de últimos ciclos. Me gusta explicar algoritmos y bases de datos."
        perfil_m.es_mentor = True
        perfil_m.es_aprendiz = False
        perfil_m.perfil_completo = True
        perfil_m.save()

        perfil_a, _ = Perfil.objects.get_or_create(usuario=aprendiz)
        perfil_a.ciclo = 2
        perfil_a.carrera = "Ingeniería de Software"
        perfil_a.biografia = "Estoy empezando y busco apoyo en programación y hábitos de estudio."
        perfil_a.es_mentor = False
        perfil_a.es_aprendiz = True
        perfil_a.perfil_completo = True
        perfil_a.save()

        oferta, _ = OfertaMentor.objects.get_or_create(perfil=perfil_m)
        oferta.temas = "POO, SQL, Git y preparación de entrevistas."
        oferta.disponibilidad = "Lunes a jueves, 7:00 p. m. a 9:00 p. m."
        oferta.activo = True
        oferta.save()
        especialidades = Especialidad.objects.filter(
            nombre__in=["Programación", "Bases de datos", "Desarrollo profesional"]
        )
        oferta.especialidades.set(especialidades)

        self.stdout.write(
            self.style.SUCCESS(
                "Usuarios demo listos. Mentor: mentor.demo / Aprendiz: aprendiz.demo "
                "(contraseña: demo1234). Solo disponibles con DEBUG=True en el login."
            )
        )
