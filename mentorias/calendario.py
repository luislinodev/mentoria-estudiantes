import logging
from dataclasses import dataclass
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mentorias.models import Sesion

logger = logging.getLogger(__name__)


@dataclass
class ResultadoCalendario:
    mentor: bool = False
    aprendiz: bool = False


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


def _nombre(usuario):
    return usuario.get_full_name() or usuario.email


def _descripcion(sesion: Sesion, enlace: str = "") -> str:
    texto = (
        f"Sesión de mentoría entre {_nombre(sesion.mentor)} "
        f"y {_nombre(sesion.aprendiz)}."
    )
    if enlace:
        texto += f"\n\nEnlace de Google Meet:\n{enlace}"
    if sesion.notas:
        texto += f"\n\n{sesion.notas}"
    return texto


def _horario(sesion: Sesion) -> dict:
    return {
        "start": {
            "dateTime": sesion.inicio.isoformat(),
            "timeZone": settings.TIME_ZONE,
        },
        "end": {
            "dateTime": sesion.fin.isoformat(),
            "timeZone": settings.TIME_ZONE,
        },
    }


def _insertar_evento(creds, cuerpo: dict, *, con_meet: bool, send_updates: str):
    from googleapiclient.discovery import build

    service = build("calendar", "v3", credentials=creds, cache_discovery=False)
    parametros = {
        "calendarId": "primary",
        "body": cuerpo,
        "sendUpdates": send_updates,
    }
    if con_meet:
        parametros["conferenceDataVersion"] = 1
    return service.events().insert(**parametros).execute()


def _enlace_meet(evento: dict) -> str:
    enlace = evento.get("hangoutLink") or ""
    if enlace:
        return enlace
    puntos = evento.get("conferenceData", {}).get("entryPoints", [])
    for punto in puntos:
        if punto.get("uri"):
            return punto["uri"]
    return ""


def _crear_evento_mentor(sesion: Sesion, *, invitar_por_correo: bool) -> bool:
    creds = _credenciales_google(sesion.mentor)
    if creds is None:
        logger.info("Sin credenciales de Calendar para el mentor %s", sesion.mentor)
        return False
    especialidad = sesion.solicitud.especialidad.nombre
    cuerpo = {
        "summary": f"Mentoría: {especialidad}",
        "description": _descripcion(sesion),
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
        **_horario(sesion),
    }
    try:
        creado = _insertar_evento(
            creds,
            cuerpo,
            con_meet=True,
            send_updates="all" if invitar_por_correo else "none",
        )
    except Exception:
        logger.exception("No se pudo crear el evento del mentor para la sesión %s", sesion.pk)
        return False
    sesion.google_event_id = creado.get("id", "")
    sesion.enlace_meet = _enlace_meet(creado)
    sesion.save(update_fields=["google_event_id", "enlace_meet"])
    return True


def _crear_evento_aprendiz(sesion: Sesion) -> bool:
    """Copia el horario al calendario del aprendiz con el mismo enlace de Meet.

    Listar al aprendiz como invitado no pone el evento en su calendario: Google
    lo deja solo en el del mentor. Hace falta crearlo con la cuenta del aprendiz.
    """
    creds = _credenciales_google(sesion.aprendiz)
    if creds is None:
        logger.info("Sin credenciales de Calendar para el aprendiz %s", sesion.aprendiz)
        return False
    especialidad = sesion.solicitud.especialidad.nombre
    enlace = sesion.enlace_meet
    cuerpo = {
        "summary": f"Mentoría: {especialidad}",
        "description": _descripcion(sesion, enlace),
        **_horario(sesion),
    }
    if enlace:
        cuerpo["location"] = enlace
    try:
        creado = _insertar_evento(creds, cuerpo, con_meet=False, send_updates="none")
    except Exception:
        logger.exception("No se pudo crear el evento del aprendiz para la sesión %s", sesion.pk)
        return False
    sesion.google_event_aprendiz_id = creado.get("id", "")
    sesion.save(update_fields=["google_event_aprendiz_id"])
    return True


def crear_evento_calendario(sesion: Sesion) -> ResultadoCalendario:
    """Crea la reunión en el calendario del mentor y en el del aprendiz."""
    aprendiz_conectado = _credenciales_google(sesion.aprendiz) is not None
    mentor_ok = bool(sesion.google_event_id) or _crear_evento_mentor(
        sesion,
        invitar_por_correo=not aprendiz_conectado,
    )
    aprendiz_ok = bool(sesion.google_event_aprendiz_id) or _crear_evento_aprendiz(sesion)
    return ResultadoCalendario(mentor=mentor_ok, aprendiz=aprendiz_ok)


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
