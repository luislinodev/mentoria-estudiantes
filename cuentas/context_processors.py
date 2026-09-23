from django.conf import settings


def plataforma(request):
    perfil = None
    if request.user.is_authenticated:
        perfil = getattr(request.user, "perfil", None)
    return {
        "perfil_actual": perfil,
        "google_oauth_configurado": settings.GOOGLE_OAUTH_CONFIGURADO,
        "debug_mode": settings.DEBUG,
    }
