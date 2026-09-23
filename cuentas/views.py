from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PerfilForm
from .models import Perfil


def inicio(request):
    if request.user.is_authenticated:
        return redirect("cuentas:despues_login")
    return render(request, "cuentas/inicio.html")


@login_required
def despues_login(request):
    perfil = getattr(request.user, "perfil", None)
    if perfil is None or not perfil.perfil_completo:
        return redirect("cuentas:completar_perfil")
    return redirect("cuentas:mi_perfil")


@login_required
def completar_perfil(request):
    perfil, _creado = Perfil.objects.get_or_create(usuario=request.user)
    form = PerfilForm(request.POST or None, request.FILES or None, instance=perfil)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tu perfil quedó guardado.")
        return redirect("cuentas:mi_perfil")
    return render(request, "cuentas/completar_perfil.html", {"form": form, "perfil": perfil})


@login_required
def mi_perfil(request):
    perfil, _creado = Perfil.objects.get_or_create(usuario=request.user)
    return render(request, "cuentas/mi_perfil.html", {"perfil": perfil})
