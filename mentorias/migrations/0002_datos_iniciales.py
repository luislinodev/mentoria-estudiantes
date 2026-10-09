from django.db import migrations


ESPECIALIDADES = [
    ("Programación", "Algoritmos, estructuras de datos y fundamentos de código."),
    ("Bases de datos", "Modelado, SQL y diseño de consultas."),
    ("Desarrollo web", "HTML, CSS, JavaScript y frameworks web."),
    ("Desarrollo profesional", "CV, entrevistas, LinkedIn y habilidades blandas."),
    ("Matemática", "Cálculo, estadística y raciocinio cuantitativo."),
    ("Inglés técnico", "Vocabulario y comunicación en contextos académicos."),
]


def cargar(apps, schema_editor):
    Especialidad = apps.get_model("mentorias", "Especialidad")
    Site = apps.get_model("sites", "Site")
    for nombre, descripcion in ESPECIALIDADES:
        Especialidad.objects.get_or_create(
            nombre=nombre, defaults={"descripcion": descripcion}
        )
    Site.objects.update_or_create(
        pk=1,
        defaults={"domain": "127.0.0.1:8000", "name": "Mentoría Estudiantes"},
    )


def vaciar(apps, schema_editor):
    Especialidad = apps.get_model("mentorias", "Especialidad")
    Especialidad.objects.filter(nombre__in=[n for n, _ in ESPECIALIDADES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("mentorias", "0001_initial"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(cargar, vaciar),
    ]
