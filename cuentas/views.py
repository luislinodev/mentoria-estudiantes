from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from mentorias.models import Sesion, Solicitud

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
    return redirect("cuentas:panel")


@login_required
def completar_perfil(request):
    perfil, _creado = Perfil.objects.get_or_create(usuario=request.user)
    form = PerfilForm(request.POST or None, request.FILES or None, instance=perfil)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tu perfil quedó guardado.")
        return redirect("cuentas:panel")
    return render(request, "cuentas/completar_perfil.html", {"form": form, "perfil": perfil})


@login_required
def panel(request):
    perfil, _creado = Perfil.objects.get_or_create(usuario=request.user)
    proximas = (
        Sesion.objects.filter(
            Q(mentor=request.user) | Q(aprendiz=request.user),
            estado=Sesion.Estado.PROGRAMADA,
            inicio__gte=timezone.now(),
        )
        .select_related("solicitud__especialidad")
        .order_by("inicio")[:5]
    )
    solicitudes_pendientes = Solicitud.objects.none()
    solicitudes_enviadas = Solicitud.objects.none()
    if perfil.es_mentor:
        solicitudes_pendientes = Solicitud.objects.filter(
            mentor=request.user, estado=Solicitud.Estado.PENDIENTE
        ).select_related("aprendiz", "especialidad")[:5]
    if perfil.es_aprendiz:
        solicitudes_enviadas = Solicitud.objects.filter(aprendiz=request.user).select_related(
            "mentor", "especialidad"
        )[:5]
    return render(
        request,
        "cuentas/panel.html",
        {
            "perfil": perfil,
            "proximas": proximas,
            "solicitudes_pendientes": solicitudes_pendientes,
            "solicitudes_enviadas": solicitudes_enviadas,
        },
    )


@login_required
def mi_perfil(request):
    perfil, _creado = Perfil.objects.get_or_create(usuario=request.user)
    return render(request, "cuentas/mi_perfil.html", {"perfil": perfil})
