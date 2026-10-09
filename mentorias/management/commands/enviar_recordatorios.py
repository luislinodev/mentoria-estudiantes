from django.core.management.base import BaseCommand

from mentorias.calendario import enviar_recordatorio, sesiones_por_recordar


class Command(BaseCommand):
    help = "Envía recordatorios por correo para sesiones de las próximas 24 horas."

    def handle(self, *args, **options):
        enviados = 0
        for sesion in sesiones_por_recordar():
            if enviar_recordatorio(sesion):
                enviados += 1
                self.stdout.write(f"Recordatorio enviado para sesión {sesion.pk}")
        self.stdout.write(self.style.SUCCESS(f"Listo. Recordatorios enviados: {enviados}"))
