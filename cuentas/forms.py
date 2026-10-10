from django import forms
from django.core.exceptions import ValidationError

from .models import Carrera, Perfil


class PerfilForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellidos", max_length=150)

    class Meta:
        model = Perfil
        fields = [
            "ciclo",
            "carrera",
            "biografia",
            "foto",
            "es_mentor",
            "es_aprendiz",
        ]
        labels = {
            "ciclo": "Ciclo académico",
            "carrera": "Carrera",
            "biografia": "Biografía",
            "foto": "Foto de perfil",
            "es_mentor": "Quiero ser mentor",
            "es_aprendiz": "Quiero ser aprendiz",
        }
        widgets = {
            "biografia": forms.Textarea(attrs={"rows": 4}),
            "ciclo": forms.NumberInput(attrs={"min": 1, "max": 12}),
        }

    field_order = [
        "first_name",
        "last_name",
        "ciclo",
        "carrera",
        "biografia",
        "foto",
        "es_mentor",
        "es_aprendiz",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usuario = self.instance.usuario
        self.fields["first_name"].initial = usuario.first_name
        self.fields["last_name"].initial = usuario.last_name
        self.fields["carrera"].queryset = Carrera.objects.all()
        self.fields["carrera"].empty_label = "Selecciona tu carrera"
        self.fields["carrera"].required = True

    def clean_ciclo(self):
        ciclo = self.cleaned_data.get("ciclo")
        if ciclo is not None and not 1 <= ciclo <= 12:
            raise ValidationError("El ciclo debe estar entre 1 y 12.")
        return ciclo

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("es_mentor") and not cleaned.get("es_aprendiz"):
            raise ValidationError("Elige al menos un rol: mentor o aprendiz.")
        return cleaned

    def save(self, commit=True):
        perfil = super().save(commit=False)
        usuario = perfil.usuario
        usuario.first_name = self.cleaned_data["first_name"]
        usuario.last_name = self.cleaned_data["last_name"]
        perfil.perfil_completo = True
        if commit:
            usuario.save()
            perfil.save()
        return perfil
