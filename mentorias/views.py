from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cuentas.decorators import requiere_rol

from .calendario import crear_evento_calendario
from .forms import AceptarSolicitudForm, OfertaMentorForm, SolicitudForm, ValoracionForm
from .models import Especialidad, OfertaMentor, Sesion, Solicitud, Valoracion


@login_required
def buscar_mentores(request):
    especialidades = Especialidad.objects.all()
    q = request.GET.get("q", "").strip()
    especialidad_id = request.GET.get("especialidad", "").strip()
    mentores = (
        OfertaMentor.objects.filter(activo=True, perfil__es_mentor=True, perfil__perfil_completo=True)
        .select_related("perfil__usuario", "perfil__carrera")
        .prefetch_related("especialidades")
        .distinct()
    )
    if q:
        mentores = mentores.filter(
            Q(perfil__usuario__first_name__icontains=q)
            | Q(perfil__usuario__last_name__icontains=q)
            | Q(temas__icontains=q)
            | Q(perfil__carrera__nombre__icontains=q)
            | Q(especialidades__nombre__icontains=q)
        ).distinct()
    if especialidad_id.isdigit():
        mentores = mentores.filter(especialidades__pk=int(especialidad_id))
    return render(
        request,
        "mentorias/buscar.html",
        {
            "mentores": mentores,
            "especialidades": especialidades,
            "q": q,
            "especialidad_id": especialidad_id,
        },
    )


@login_required
def detalle_mentor(request, pk):
    oferta = get_object_or_404(
        OfertaMentor.objects.select_related("perfil__usuario", "perfil__carrera").prefetch_related(
            "especialidades"
        ),
        pk=pk,
        activo=True,
    )
    valoraciones = (
        Valoracion.objects.filter(mentor=oferta.perfil.usuario)
        .select_related("aprendiz")
        .order_by("-creado")[:8]
    )
    return render(
        request,
        "mentorias/detalle_mentor.html",
        {"oferta": oferta, "valoraciones": valoraciones},
    )


@login_required
@requiere_rol(mentor=True)
def editar_oferta(request):
    oferta, _ = OfertaMentor.objects.get_or_create(perfil=request.user.perfil)
    form = OfertaMentorForm(request.POST or None, instance=oferta)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tu oferta de mentoría se actualizó.")
        return redirect("cuentas:mi_perfil")
    return render(request, "mentorias/editar_oferta.html", {"form": form})


@login_required
@requiere_rol(aprendiz=True)
def crear_solicitud(request, mentor_id):
    oferta = get_object_or_404(OfertaMentor, pk=mentor_id, activo=True)
    if oferta.perfil.usuario == request.user:
        messages.error(request, "No puedes solicitarte mentoría a ti mismo.")
        return redirect("mentorias:detalle_mentor", pk=oferta.pk)
    form = SolicitudForm(
        request.POST or None,
        especialidades=oferta.especialidades.all(),
    )
    if request.method == "POST" and form.is_valid():
        existente = Solicitud.objects.filter(
            aprendiz=request.user,
            mentor=oferta.perfil.usuario,
            especialidad=form.cleaned_data["especialidad"],
            estado=Solicitud.Estado.PENDIENTE,
        ).exists()
        if existente:
            messages.warning(request, "Ya tienes una solicitud pendiente con este mentor.")
            return redirect("mentorias:solicitudes")
        solicitud = form.save(commit=False)
        solicitud.aprendiz = request.user
        solicitud.mentor = oferta.perfil.usuario
        solicitud.save()
        messages.success(request, "Solicitud enviada. El mentor te responderá pronto.")
        return redirect("mentorias:solicitudes")
    return render(
        request,
        "mentorias/crear_solicitud.html",
        {"form": form, "oferta": oferta},
    )


@login_required
def solicitudes(request):
    perfil = request.user.perfil
    recibidas = Solicitud.objects.none()
    enviadas = Solicitud.objects.none()
    if perfil.es_mentor:
        recibidas = Solicitud.objects.filter(mentor=request.user).select_related(
            "aprendiz", "especialidad"
        )
    if perfil.es_aprendiz:
        enviadas = Solicitud.objects.filter(aprendiz=request.user).select_related(
            "mentor", "especialidad"
        )
    aceptar_form = AceptarSolicitudForm()
    return render(
        request,
        "mentorias/solicitudes.html",
        {
            "recibidas": recibidas,
            "enviadas": enviadas,
            "aceptar_form": aceptar_form,
        },
    )


@login_required
@requiere_rol(mentor=True)
def aceptar_solicitud(request, pk):
    solicitud = get_object_or_404(
        Solicitud, pk=pk, mentor=request.user, estado=Solicitud.Estado.PENDIENTE
    )
    form = AceptarSolicitudForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        inicio = form.cleaned_data["inicio"]
        minutos = int(form.cleaned_data["duracion_minutos"])
        sesion = Sesion.objects.create(
            solicitud=solicitud,
            mentor=solicitud.mentor,
            aprendiz=solicitud.aprendiz,
            inicio=inicio,
            fin=inicio + timedelta(minutes=minutos),
            notas=form.cleaned_data.get("notas", ""),
        )
        solicitud.estado = Solicitud.Estado.ACEPTADA
        solicitud.save(update_fields=["estado"])
        creado = crear_evento_calendario(sesion)
        if creado:
            messages.success(request, "Sesión agendada y añadida a Google Calendar.")
        else:
            messages.success(
                request,
                "Sesión agendada. No se pudo sincronizar con Google Calendar "
                "(configura las credenciales o vuelve a iniciar sesión con Google).",
            )
        return redirect("mentorias:sesiones")
    return render(
        request,
        "mentorias/aceptar_solicitud.html",
        {"form": form, "solicitud": solicitud},
    )


@login_required
@requiere_rol(mentor=True)
@require_POST
def rechazar_solicitud(request, pk):
    solicitud = get_object_or_404(
        Solicitud, pk=pk, mentor=request.user, estado=Solicitud.Estado.PENDIENTE
    )
    solicitud.estado = Solicitud.Estado.RECHAZADA
    solicitud.save(update_fields=["estado"])
    messages.info(request, "Solicitud rechazada.")
    return redirect("mentorias:solicitudes")


@login_required
def sesiones(request):
    lista = (
        Sesion.objects.filter(Q(mentor=request.user) | Q(aprendiz=request.user))
        .select_related("solicitud__especialidad", "mentor", "aprendiz")
        .order_by("-inicio")
    )
    return render(request, "mentorias/sesiones.html", {"sesiones": lista})


@login_required
def detalle_sesion(request, pk):
    sesion = get_object_or_404(
        Sesion.objects.select_related("solicitud__especialidad", "mentor", "aprendiz"),
        Q(mentor=request.user) | Q(aprendiz=request.user),
        pk=pk,
    )
    return render(request, "mentorias/detalle_sesion.html", {"sesion": sesion})


@login_required
@require_POST
def completar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk=pk, estado=Sesion.Estado.PROGRAMADA)
    if request.user not in (sesion.mentor, sesion.aprendiz):
        messages.error(request, "No puedes modificar esta sesión.")
        return redirect("mentorias:sesiones")
    sesion.estado = Sesion.Estado.COMPLETADA
    sesion.save(update_fields=["estado"])
    messages.success(request, "Sesión marcada como completada.")
    return redirect("mentorias:detalle_sesion", pk=sesion.pk)


@login_required
@require_POST
def cancelar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk=pk, estado=Sesion.Estado.PROGRAMADA)
    if request.user not in (sesion.mentor, sesion.aprendiz):
        messages.error(request, "No puedes cancelar esta sesión.")
        return redirect("mentorias:sesiones")
    sesion.estado = Sesion.Estado.CANCELADA
    sesion.save(update_fields=["estado"])
    messages.info(request, "Sesión cancelada.")
    return redirect("mentorias:sesiones")


@login_required
@requiere_rol(aprendiz=True)
def valorar_sesion(request, pk):
    sesion = get_object_or_404(
        Sesion,
        pk=pk,
        aprendiz=request.user,
        estado=Sesion.Estado.COMPLETADA,
    )
    if hasattr(sesion, "valoracion"):
        messages.info(request, "Esta sesión ya tiene una valoración.")
        return redirect("mentorias:detalle_sesion", pk=sesion.pk)
    form = ValoracionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        valoracion = form.save(commit=False)
        valoracion.sesion = sesion
        valoracion.aprendiz = request.user
        valoracion.mentor = sesion.mentor
        valoracion.save()
        messages.success(request, "Gracias por tu valoración.")
        return redirect("mentorias:detalle_sesion", pk=sesion.pk)
    return render(request, "mentorias/valorar.html", {"form": form, "sesion": sesion})
