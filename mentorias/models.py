from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.urls import reverse


class Especialidad(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "especialidad"
        verbose_name_plural = "especialidades"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class OfertaMentor(models.Model):
    perfil = models.OneToOneField(
        "cuentas.Perfil",
        on_delete=models.CASCADE,
        related_name="oferta",
    )
    especialidades = models.ManyToManyField(Especialidad, related_name="mentores", blank=True)
    temas = models.TextField(blank=True, help_text="Temas en los que puedes mentorear.")
    disponibilidad = models.CharField(max_length=255, blank=True)
    activo = models.BooleanField(default=True)
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_valoraciones = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "oferta de mentor"
        verbose_name_plural = "ofertas de mentores"

    def __str__(self):
        return f"Mentor: {self.perfil.nombre_completo}"

    def actualizar_promedio(self):
        agregado = Valoracion.objects.filter(mentor=self.perfil.usuario).aggregate(
            promedio=Avg("estrellas")
        )
        promedio = agregado["promedio"] or 0
        self.calificacion_promedio = round(promedio, 2)
        self.total_valoraciones = Valoracion.objects.filter(mentor=self.perfil.usuario).count()
        self.save(update_fields=["calificacion_promedio", "total_valoraciones"])

    def get_absolute_url(self):
        return reverse("mentorias:detalle_mentor", args=[self.pk])


class Solicitud(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        ACEPTADA = "aceptada", "Aceptada"
        RECHAZADA = "rechazada", "Rechazada"

    aprendiz = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="solicitudes_enviadas",
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="solicitudes_recibidas",
    )
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)
    mensaje = models.TextField()
    fecha_propuesta = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha y hora sugeridas para la sesión.",
    )
    estado = models.CharField(max_length=20, choices=Estado, default=Estado.PENDIENTE)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "solicitud"
        verbose_name_plural = "solicitudes"
        ordering = ["-creado"]
        constraints = [
            models.UniqueConstraint(
                fields=["aprendiz", "mentor", "especialidad"],
                condition=models.Q(estado="pendiente"),
                name="solicitud_pendiente_unica",
            )
        ]

    def __str__(self):
        return f"{self.aprendiz} → {self.mentor} ({self.especialidad})"


class Sesion(models.Model):
    class Estado(models.TextChoices):
        PROGRAMADA = "programada", "Programada"
        COMPLETADA = "completada", "Completada"
        CANCELADA = "cancelada", "Cancelada"

    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE, related_name="sesion")
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sesiones_como_mentor",
    )
    aprendiz = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sesiones_como_aprendiz",
    )
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=Estado, default=Estado.PROGRAMADA)
    google_event_id = models.CharField(max_length=255, blank=True)
    google_event_aprendiz_id = models.CharField(max_length=255, blank=True)
    enlace_meet = models.URLField(blank=True)
    recordatorio_enviado = models.BooleanField(default=False)
    notas = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "sesión"
        verbose_name_plural = "sesiones"
        ordering = ["inicio"]

    def __str__(self):
        return f"Sesión {self.inicio:%d/%m/%Y %H:%M}"

    @property
    def puede_valorarse(self):
        return self.estado == self.Estado.COMPLETADA and not hasattr(self, "valoracion")


class Valoracion(models.Model):
    sesion = models.OneToOneField(Sesion, on_delete=models.CASCADE, related_name="valoracion")
    aprendiz = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="valoraciones_hechas",
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="valoraciones_recibidas",
    )
    estrellas = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "valoración"
        verbose_name_plural = "valoraciones"
        ordering = ["-creado"]

    def __str__(self):
        return f"{self.estrellas}★ para {self.mentor}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        oferta = getattr(self.mentor.perfil, "oferta", None)
        if oferta:
            oferta.actualizar_promedio()
