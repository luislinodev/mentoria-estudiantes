from django.shortcuts import redirect


class PerfilCompletoMiddleware:
    """Redirige a completar el perfil tras el primer acceso."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            perfil = getattr(request.user, "perfil", None)
            incompleto = perfil is None or not perfil.perfil_completo
            if incompleto:
                path = request.path
                libre = (
                    path.startswith("/admin/")
                    or path.startswith("/accounts/")
                    or path.startswith("/static/")
                    or path.startswith("/media/")
                    or path in {
                        "/",
                        "/perfil/completar/",
                        "/perfil/completar",
                        "/despues-login/",
                        "/despues-login",
                    }
                )
                if not libre:
                    return redirect("cuentas:completar_perfil")
        return self.get_response(request)
