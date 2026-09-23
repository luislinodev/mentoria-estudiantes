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
    for nombre, descripcion in ESPECIALIDADES:
        Especialidad.objects.get_or_create(nombre=nombre, defaults={"descripcion": descripcion})


def vaciar(apps, schema_editor):
    Especialidad = apps.get_model("mentorias", "Especialidad")
    Especialidad.objects.filter(nombre__in=[nombre for nombre, _descripcion in ESPECIALIDADES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("mentorias", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(cargar, vaciar),
    ]
