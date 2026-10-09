from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import OfertaMentor, Sesion, Solicitud, Valoracion


class OfertaMentorForm(forms.ModelForm):
    class Meta:
        model = OfertaMentor
        fields = ["especialidades", "temas", "disponibilidad", "activo"]
        labels = {
            "especialidades": "Especialidades",
            "temas": "Temas que ofreces",
            "disponibilidad": "Disponibilidad",
            "activo": "Perfil visible para aprendices",
        }
        widgets = {
            "especialidades": forms.CheckboxSelectMultiple(),
            "temas": forms.Textarea(attrs={"rows": 4}),
        }


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ["especialidad", "mensaje", "fecha_propuesta"]
        labels = {
            "especialidad": "Especialidad",
            "mensaje": "¿En qué necesitas ayuda?",
            "fecha_propuesta": "Fecha y hora propuestas",
        }
        widgets = {
            "mensaje": forms.Textarea(attrs={"rows": 4}),
            "fecha_propuesta": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, especialidades=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha_propuesta"].input_formats = ["%Y-%m-%dT%H:%M"]
        if especialidades is not None:
            self.fields["especialidad"].queryset = especialidades

    def clean_fecha_propuesta(self):
        fecha = self.cleaned_data.get("fecha_propuesta")
        if fecha and fecha < timezone.now():
            raise ValidationError("La fecha propuesta debe ser futura.")
        return fecha


class AceptarSolicitudForm(forms.Form):
    inicio = forms.DateTimeField(
        label="Inicio de la sesión",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"],
    )
    duracion_minutos = forms.ChoiceField(
        label="Duración",
        choices=[(30, "30 minutos"), (45, "45 minutos"), (60, "60 minutos"), (90, "90 minutos")],
        initial=60,
    )
    notas = forms.CharField(
        label="Notas para el aprendiz (opcional)",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def clean_inicio(self):
        inicio = self.cleaned_data["inicio"]
        if inicio < timezone.now():
            raise ValidationError("La sesión debe agendarse en el futuro.")
        return inicio


class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ["estrellas", "comentario"]
        labels = {
            "estrellas": "Calificación",
            "comentario": "Comentario",
        }
        widgets = {
            "estrellas": forms.RadioSelect(choices=[(i, f"{i} estrella{'s' if i > 1 else ''}") for i in range(1, 6)]),
            "comentario": forms.Textarea(attrs={"rows": 4}),
        }
