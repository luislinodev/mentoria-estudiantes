from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def requiere_rol(*, mentor=False, aprendiz=False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("account_login")
            perfil = getattr(request.user, "perfil", None)
            if perfil is None or not perfil.perfil_completo:
                messages.info(request, "Completa tu perfil para continuar.")
                return redirect("cuentas:completar_perfil")
            if mentor and not perfil.es_mentor:
                messages.warning(request, "Esta acción está disponible solo para mentores.")
                return redirect("cuentas:mi_perfil")
            if aprendiz and not perfil.es_aprendiz:
                messages.warning(request, "Esta acción está disponible solo para aprendices.")
                return redirect("cuentas:mi_perfil")
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
