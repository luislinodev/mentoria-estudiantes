import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mentorias.models import Sesion

logger = logging.getLogger(__name__)


def _credenciales_google(usuario):
    if not settings.GOOGLE_OAUTH_CONFIGURADO:
        return None
    try:
        from allauth.socialaccount.models import SocialToken
        from google.oauth2.credentials import Credentials
    except ImportError:
        return None

    token = (
        SocialToken.objects.filter(account__user=usuario, account__provider="google")
        .select_related("app", "account")
        .first()
    )
    if not token:
        return None

    refresh = token.token_secret or None
    return Credentials(
        token=token.token,
        refresh_token=refresh,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/calendar.events"],
    )


def crear_evento_calendario(sesion: Sesion) -> bool:
    """Crea un evento en Google Calendar del mentor. Devuelve False si no se pudo."""
    creds = _credenciales_google(sesion.mentor)
    if creds is None:
        logger.info("Sin credenciales de Calendar para %s", sesion.mentor)
        return False
    try:
        from googleapiclient.discovery import build

        service = build("calendar", "v3", credentials=creds, cache_discovery=False)
        especialidad = sesion.solicitud.especialidad.nombre
        evento = {
            "summary": f"Mentoría: {especialidad}",
            "description": (
                f"Sesión de mentoría entre {sesion.mentor.get_full_name()} "
                f"y {sesion.aprendiz.get_full_name()}.\n\n"
                f"{sesion.notas}"
            ),
            "start": {
                "dateTime": sesion.inicio.isoformat(),
                "timeZone": settings.TIME_ZONE,
            },
            "end": {
                "dateTime": sesion.fin.isoformat(),
                "timeZone": settings.TIME_ZONE,
            },
            "attendees": [
                {"email": sesion.mentor.email},
                {"email": sesion.aprendiz.email},
            ],
            "conferenceData": {
                "createRequest": {
                    "requestId": f"mentoria-{sesion.pk}",
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                }
            },
        }
        creado = (
            service.events()
            .insert(
                calendarId="primary",
                body=evento,
                conferenceDataVersion=1,
                sendUpdates="all",
            )
            .execute()
        )
        sesion.google_event_id = creado.get("id", "")
        enlace = creado.get("hangoutLink") or ""
        if not enlace:
            puntos = creado.get("conferenceData", {}).get("entryPoints", [])
            if puntos:
                enlace = puntos[0].get("uri", "")
        sesion.enlace_meet = enlace
        sesion.save(update_fields=["google_event_id", "enlace_meet"])
        return True
    except Exception:
        logger.exception("No se pudo crear el evento de Calendar para la sesión %s", sesion.pk)
        return False


def enviar_recordatorio(sesion: Sesion) -> bool:
    asunto = f"Recordatorio: sesión de mentoría el {timezone.localtime(sesion.inicio):%d/%m/%Y %H:%M}"
    enlace = sesion.enlace_meet or "Se confirmará en la plataforma."
    cuerpo = (
        f"Hola,\n\nTienes una sesión de mentoría programada.\n"
        f"Especialidad: {sesion.solicitud.especialidad.nombre}\n"
        f"Inicio: {timezone.localtime(sesion.inicio):%d/%m/%Y %H:%M}\n"
        f"Enlace: {enlace}\n\n"
        f"Mentoría entre Estudiantes\n"
    )
    destinatarios = [email for email in (sesion.mentor.email, sesion.aprendiz.email) if email]
    if not destinatarios:
        return False
    send_mail(asunto, cuerpo, settings.DEFAULT_FROM_EMAIL, destinatarios)
    sesion.recordatorio_enviado = True
    sesion.save(update_fields=["recordatorio_enviado"])
    return True


def sesiones_por_recordar():
    ahora = timezone.now()
    return Sesion.objects.filter(
        estado=Sesion.Estado.PROGRAMADA,
        recordatorio_enviado=False,
        inicio__gte=ahora,
        inicio__lte=ahora + timedelta(hours=24),
    ).select_related("solicitud__especialidad", "mentor", "aprendiz")
