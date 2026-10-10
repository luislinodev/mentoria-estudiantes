from django.db import migrations


def agregar_columnas_calendario(apps, schema_editor):
    Sesion = apps.get_model("mentorias", "Sesion")
    tabla = Sesion._meta.db_table
    conexion = schema_editor.connection
    with conexion.cursor() as cursor:
        existentes = {
            columna.name
            for columna in conexion.introspection.get_table_description(cursor, tabla)
        }
    campos = {campo.column: campo for campo in Sesion._meta.local_fields}
    for columna in ("google_event_id", "enlace_meet", "recordatorio_enviado"):
        if columna not in existentes:
            schema_editor.add_field(Sesion, campos[columna])


class Migration(migrations.Migration):

    dependencies = [
        ("mentorias", "0002_datos_iniciales"),
    ]

    operations = [
        migrations.RunPython(agregar_columnas_calendario, migrations.RunPython.noop),
    ]
