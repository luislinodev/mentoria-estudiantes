from django.conf import settings
from django.db import models
from django.urls import reverse


class Carrera(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "carrera"
        verbose_name_plural = "carreras"
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    ciclo = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Ciclo académico actual (1 a 12).",
    )
    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="perfiles",
    )
    biografia = models.TextField(blank=True)
    foto = models.ImageField(upload_to="perfiles/", blank=True, null=True)
    es_mentor = models.BooleanField(default=False)
    es_aprendiz = models.BooleanField(default=False)
    perfil_completo = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"
        ordering = ["usuario__first_name", "usuario__last_name"]

    def __str__(self):
        return self.nombre_completo

    @property
    def nombre_completo(self):
        nombre = self.usuario.get_full_name().strip()
        return nombre or self.usuario.email or self.usuario.username

    def get_absolute_url(self):
        return reverse("cuentas:mi_perfil")

    def avatar_url(self):
        if self.foto:
            return self.foto.url
        extra = getattr(self.usuario, "socialaccount_set", None)
        if extra:
            cuenta = self.usuario.socialaccount_set.filter(provider="google").first()
            if cuenta:
                picture = cuenta.extra_data.get("picture")
                if picture:
                    return picture
        return ""
