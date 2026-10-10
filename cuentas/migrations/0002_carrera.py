import django.db.models.deletion
from django.db import migrations, models

CARRERAS = [
    (1, "Diseño y Desarrollo de Software"),
    (2, "Arquitectura de Sistemas de Información"),
    (3, "Adm. de Sistemas para la Transformación Digital"),
    (4, "Gestión de Sistemas de Información"),
]


def cargar_carreras(apps, schema_editor):
    Carrera = apps.get_model("cuentas", "Carrera")
    for orden, nombre in CARRERAS:
        Carrera.objects.update_or_create(nombre=nombre, defaults={"orden": orden})


def vaciar_carreras(apps, schema_editor):
    Carrera = apps.get_model("cuentas", "Carrera")
    Carrera.objects.filter(nombre__in=[nombre for _, nombre in CARRERAS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("cuentas", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Carrera",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=120, unique=True)),
                ("orden", models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                "verbose_name": "carrera",
                "verbose_name_plural": "carreras",
                "ordering": ["orden", "nombre"],
            },
        ),
        migrations.RunPython(cargar_carreras, vaciar_carreras),
        migrations.RemoveField(
            model_name="perfil",
            name="carrera",
        ),
        migrations.AddField(
            model_name="perfil",
            name="carrera",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="perfiles",
                to="cuentas.carrera",
            ),
        ),
    ]
