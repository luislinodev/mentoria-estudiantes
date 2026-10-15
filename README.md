# Mentoría Estudiantil

Plataforma web para acompañar a estudiantes de ciclos iniciales con estudiantes de ciclos avanzados o graduados que quieren compartir lo que ya aprendieron. Un mismo usuario puede ser mentor, aprendiz o ambos.

Quien se registra como mentor es tratado igual por la plataforma. No hay un campo que distinga si esa persona sigue estudiando o ya se graduó: esa diferencia la decide quien se postula, no el sistema.

## Enlaces

- [Repositorio](https://github.com/luislinodev/mentoria-estudiantes)
- [Sprints semanales](https://app.notion.com/p/Mentor-a-Estudiantes-3f7f1e0703d880ee8d46d210be837eaf?source=copy_link)
- [Capturas de pantalla](https://www.figma.com/design/mPHcrylz5mt2ievb3s70U2/Sin-t%C3%ADtulo?node-id=0-1&t=CWoHN1dPU5o5yRh4-1)

## El problema

Los estudiantes nuevos suelen no tener un canal directo para resolver dudas académicas o de orientación profesional con quienes van más adelante. Ese conocimiento existe en la institución, en estudiantes de ciclos superiores y en egresados, pero no hay un lugar que reúna la búsqueda, el contacto y la programación de estas mentorías.

## Qué resuelve

La plataforma cubre el ciclo completo de una mentoría voluntaria y gratuita: ingresar, completar el perfil, buscar un mentor, enviar una solicitud, aceptarla, agendar la sesión y valorarla al terminar.

## Objetivo

Conectar a estudiantes de ciclos iniciales con estudiantes de ciclos avanzados o graduados para recibir mentoría en temas académicos y de desarrollo profesional, en un solo lugar donde se busca, se solicita, se agenda y se valora cada sesión.

## Qué permite

- Registrarse e iniciar sesión con Google (Gmail).
- Crear y editar el perfil de mentor y de aprendiz.
- Buscar mentores por especialidad o por una palabra clave.
- Enviar, aceptar y rechazar solicitudes de mentoría.
- Agendar la sesión y, si el mentor tiene Google conectado, añadirla a Google Calendar con un enlace de Google Meet cuando se puede generar.
- Avisar de las sesiones que están por llegar.
- Valorar de 1 a 5 estrellas al terminar. El promedio del mentor se actualiza con esa calificación.
- Un panel de administración para revisar usuarios, especialidades y sesiones.

## Roles

| Rol | Qué hace |
| --- | --- |
| Aprendiz | Busca mentores, envía solicitudes, sigue su agenda y califica las sesiones que recibió. |
| Mentor | Publica su oferta por especialidad, acepta o rechaza solicitudes y agenda las sesiones. |
| Administrador | Supervisa usuarios, especialidades y sesiones desde el panel de administración. |

## Cómo transcurre una mentoría

1. El aprendiz busca mentores por especialidad o por una palabra clave, revisa su perfil y elige a quien mejor se adapte.
2. Envía una solicitud con un mensaje y una fecha propuesta.
3. El mentor acepta o rechaza. Si acepta, define la fecha y la duración definitivas. La sesión queda en la agenda y, si su cuenta de Google está conectada, también en Google Calendar, con enlace de Meet cuando está disponible.
4. Al terminar, la sesión se marca como completada.
5. El aprendiz deja una valoración de 1 a 5 estrellas y un comentario. Solo puede hacerlo una vez, y solo sobre una sesión ya completada. Esa nota actualiza el promedio del mentor.

La comunicación se da en el mensaje de la solicitud, en la respuesta del mentor y en la agenda. No hay un chat dentro de la plataforma.

## Qué se puede esperar al usarla

- La interfaz está en español y las fechas se muestran en el horario de Perú.
- Se puede usar desde una computadora, una tablet o un celular.
- Los correos de los usuarios no aparecen en los listados públicos. Cada persona ve y modifica lo que le corresponde según su rol.
- Si la conexión con Google no está disponible, igual se puede entrar y usar la plataforma. La sesión se guarda; solo no se sincroniza el calendario hasta que esa conexión vuelva.

## Qué no incluye esta versión

- Chat o mensajería en tiempo real.
- Pagos. Las mentorías se asumen voluntarias y gratuitas.
- Una sala de videollamada propia. El enlace de Meet, cuando existe, abre la llamada fuera de la plataforma (Meet, presencial u otro medio que acuerden).
- Una aplicación para celular. El uso en el teléfono es a través del navegador.
- Horarios fijos de disponibilidad del mentor. La fecha y la hora se coordinan al aceptar la solicitud.
- Otros idiomas. Por ahora todo está en español.

## Especialidades iniciales

Programación, Bases de datos, Desarrollo web, Desarrollo profesional, Matemática e Inglés técnico. Se pueden sumar temas nuevos sin cambiar el resto de la plataforma.

## Cómo ejecutarla

Hace falta [Docker](https://docs.docker.com/get-docker/) con Docker Compose. Copia el archivo de ejemplo y levanta la plataforma:

```bash
cp .env.example .env
docker compose up --build
```

La primera vez descarga lo necesario, prepara la base de datos y abre el servidor de desarrollo. Entra en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Para detenerla, usa `Ctrl+C` en esa terminal. La próxima vez basta con:

```bash
docker compose up
```

Sin las claves de Google la plataforma arranca igual. En este entorno de desarrollo también puedes entrar con correo y contraseña desde la pantalla de inicio de sesión. Para crear un usuario así, con la plataforma en marcha y en otra terminal:

```bash
docker compose exec web python manage.py createsuperuser
```

Ese usuario también sirve para el panel de administración en [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

### Inicio de sesión con Google y calendario

Esto es opcional. Sirve para entrar con Gmail y para que, al aceptar una solicitud, la sesión se agregue al calendario del mentor.

1. En [Google Cloud Console](https://console.cloud.google.com/) crea un proyecto y habilita **Google Calendar API**.
2. Crea credenciales de tipo **Aplicación web**.
3. En URI de redirección autorizada indica:

   `http://127.0.0.1:8000/accounts/google/login/callback/`

4. Copia el identificador y el secreto en `.env`:

```
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

5. Vuelve a levantar la plataforma con `docker compose up`.

Al iniciar sesión se piden perfil, correo y permiso para crear eventos en el calendario. Si el mentor no tiene la cuenta conectada, la sesión queda registrada en la plataforma y se muestra un aviso: no se pierde la mentoría, solo la sincronización automática.
