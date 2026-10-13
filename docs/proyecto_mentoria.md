# Planificación del Proyecto: Aplicación de Mentoría entre Estudiantes (Caso 3)

## 1. Nombre del Proyecto

Mentoría Estudiantil: Aplicación de Mentoría entre Estudiantes

## 2. Descripción del Proyecto

El proyecto consiste en desarrollar una aplicación web de mentoría entre estudiantes, diseñada para facilitar la comunicación y el acompañamiento académico y profesional dentro de la comunidad educativa. La plataforma permite conectar a estudiantes de ciclos iniciales que necesitan orientación con estudiantes de ciclos avanzados o estudiantes ya graduados que estén dispuestos a compartir sus conocimientos y experiencias como mentores. Un mismo usuario puede tener el rol de mentor, aprendiz, o ambos.

*Nota: el sistema no distingue entre "estudiante de ciclo avanzado" y "graduado"* 
*como campos separados — cualquier persona que se registra como mentor es*
*tratada igual por la plataforma. La distinción es un criterio de quién decide*
*postularse como mentor, no una validación automática del sistema.*

La plataforma permite:
- Registro e inicio de sesión con Google (Gmail).
- Creación y edición de perfiles de mentor y aprendiz.
- Búsqueda de mentores por especialidad o palabra clave.
- Envío, aceptación y rechazo de solicitudes de mentoría.
- Agenda de sesiones sincronizada con Google Calendar, incluyendo enlace de Google Meet cuando está disponible.
- Recordatorios automáticos de sesiones próximas.
- Valoración de 1 a 5 estrellas al finalizar una sesión, con actualización del promedio del mentor.
- Panel de administración para supervisar usuarios, especialidades y sesiones.

## 3. Problemática del Proyecto
Los estudiantes de ciclos iniciales suelen carecer de un canal directo para resolver dudas académicas o de orientación profesional con estudiantes de ciclos más avanzados. Aunque dentro de la institución existe este conocimiento disponible en
estudiantes de ciclos superiores y egresados, no hay una plataforma que centralice la búsqueda, el contacto y la programación de estas mentorías, lo que dificulta que ambas partes se encuentren de forma organizada.

## 4. Solución Planteada
Se desarrolla una aplicación web que conecta a estudiantes aprendices con estudiantes de ciclos avanzados o graduados que actúan como mentores. El sistema cubre el ciclo completo: registro con Google, búsqueda de mentor, solicitud, aceptación, agendamiento con sincronización a Google Calendar, ejecución de la sesión, y valoración posterior.

## 5. Objetivo del Sistema
Conectar a estudiantes de ciclos iniciales con estudiantes de ciclos avanzados o graduados para recibir mentoría en temas académicos y de desarrollo profesional, mediante una plataforma centralizada que gestione la búsqueda, solicitud, agenda y
valoración de las sesiones.

## 6. Usuarios y Roles

Rol | Funciones
--- | ---
Administrador | Supervisa usuarios, especialidades y sesiones desde el panel de administración (/admin/).
Mentor | Estudiante de ciclo avanzado o graduado. Se registra, publica su oferta de mentoría por especialidad, acepta o rechaza solicitudes y agenda sesiones.
Estudiante Aprendiz | Busca mentores, envía solicitudes, gestiona su agenda y califica las sesiones recibidas.

Un mismo usuario puede combinar los roles de mentor y aprendiz.

## 7. Requerimientos Funcionales
- Registro e inicio de sesión mediante cuenta de Google (Gmail).
- Creación y edición de perfiles de mentor y aprendiz.
- Búsqueda de mentores por especialidad.
- Envío, aceptación y rechazo de solicitudes de mentoría.
- Agenda de sesiones con recordatorios automáticos.
- Sistema de feedback y calificación de mentores (1 a 5 estrellas), con una sola valoración por sesión, permitida únicamente al aprendiz y solo tras marcar la sesión como completada.

## 8. Requerimientos No Funcionales
- **Seguridad en la gestión de datos personales:** las contraseñas y claves de acceso se guardan de forma protegida y separada del resto del sistema; cada usuario solo puede ver y modificar la información que le corresponde según su rol; los correos electrónicos de los usuarios no se muestran públicamente en ninguna parte de la plataforma.
- **Diseño responsivo y accesible:** la plataforma se puede usar correctamente desde una computadora, una tablet o un celular, adaptándose al tamaño de la pantalla.
- **Idioma y horario local:** toda la interfaz está en español y las fechas de las sesiones se muestran en el horario de Perú.
- **Funcionamiento continuo:** si por algún motivo falla la conexión con Google, el usuario igual puede ingresar y usar la plataforma; solo no se sincroniza automáticamente el calendario hasta que la conexión se restablezca.

## 9. Casos de Uso Principales

1. Un estudiante aprendiz busca y contacta a un mentor por especialidad.
2. Un mentor acepta una solicitud, define fecha y duración, y se agenda la sesión.
3. Un aprendiz deja una valoración sobre la mentoría recibida una vez completada la sesión.

### 9.1 Alcance del Proyecto

El alcance comprende el diseño y desarrollo de una plataforma web funcional que permite realizar el proceso completo de mentoría, desde el registro del usuario hasta la finalización y valoración de una sesión.

El estudiante inicia sesión mediante su cuenta de Google y completa su perfil de acuerdo con su rol. Los aprendices pueden consultar los perfiles de los mentores, conocer sus especialidades y elegir al mentor que mejor se adapte a sus
necesidades.

Una vez elegido un mentor, el aprendiz envía una solicitud con un mensaje y una fecha propuesta. El mentor puede aceptar o rechazar dicha solicitud; en caso de aceptación, define la fecha y duración definitivas de la sesión. La plataforma genera recordatorios automáticos y, si el mentor tiene su cuenta de Google conectada, agrega la sesión a Google Calendar junto con un enlace de Google Meet.

Después de finalizar una mentoría, el estudiante aprendiz puede dejar una calificación y comentario sobre la experiencia, generando una referencia sobre la calidad de las mentorías ofrecidas por cada mentor.El proyecto contempla diseño responsivo y accesible, de manera que la aplicación se pueda usar desde computadora, tablet o celular. Asimismo, incluye medidas de seguridad para proteger los datos personales de los usuarios (ver sección 8).

En esta primera versión, el proyecto está enfocado en las funciones esenciales de conexión, comunicación, programación y evaluación de las mentorías. No se contempla la implementación de pagos, un sistema propio de videollamadas o una aplicación móvil nativa, ya que estas funcionalidades podrían incorporarse en futuras versiones.

### 9.2 ¿Qué NO incluye el proyecto?
- No incluye chat o mensajería instantánea en tiempo real; la comunicación se limita al mensaje de la solicitud, su aceptación y la agenda de la sesión.
- No incluye pasarela de pagos ni monetización de las mentorías (se asume que son voluntarias/gratuitas).
- No incluye una sala de videollamada propia dentro de la plataforma. Sí genera automáticamente un enlace de Google Meet al crear el evento en Calendar, pero la llamada en sí ocurre fuera del sistema (Meet, presencial, u otro medio que acuerden mentor y aprendiz).
- No incluye una aplicación nativa para iOS/Android en esta fase; el enfoque es diseño web responsivo.
- No incluye configuración de horarios de disponibilidad por parte del mentor; la fecha y hora se coordinan al momento de aceptar la solicitud.
- No incluye soporte multi-idioma en esta primera versión (la interfaz está en español).

## 10. Integraciones y Autenticación
- **Inicio de sesión con Google:** los usuarios ingresan a la plataforma usando su cuenta de Gmail, sin necesidad de crear una contraseña nueva.
- **Conexión con Google Calendar:** cuando un mentor acepta una solicitud, la sesión se agrega automáticamente al calendario del mentor, incluyendo un enlace de videollamada cuando es posible generarlo. Si la cuenta de Google no está conectada, la sesión queda registrada igualmente dentro de la plataforma, y solo se pierde la sincronización automática con el calendario.

## 11. Herramientas Utilizadas
El sistema se construyó con herramientas gratuitas y ampliamente usadas en el desarrollo de aplicaciones web: un lenguaje de programación estable y confiable, una base de datos incluida en el propio sistema (sin necesidad de contratar un servidor de base de datos externo), y un diseño visual basado en componentes reutilizables que facilita que la plataforma se vea bien en cualquier dispositivo.

## 12. Flujo Principal del Sistema
1. El aprendiz busca mentores por especialidad o palabra clave.
2. Envía una solicitud con un mensaje y una fecha propuesta.
3. El mentor acepta, define fecha y duración; se crea la sesión y, si hay credenciales configuradas, el evento en Google Calendar.
4. Al finalizar, la sesión se marca como completada.
5. El aprendiz deja una valoración de 1 a 5 estrellas, que actualiza el promedio del mentor.

## 13. Organización del Proyecto
El proyecto está organizado en módulos independientes para facilitar su mantenimiento:
- Cuentas: maneja el registro, los perfiles y los roles de los usuarios.
- Mentorías: maneja las especialidades, solicitudes, sesiones y valoraciones.
- Interfaz: contiene las pantallas que ve el usuario, en español.
- Configuración general: contiene los ajustes internos del sistema.

## 14. Especialidades Iniciales
Programación, Bases de datos, Desarrollo web, Desarrollo profesional, Matemática e Inglés técnico.

## 15. Roles del Equipo
El proyecto es desarrollado por dos integrantes:

Integrante | Responsabilidades
--- | ---
Luis | Lógica del sistema (registro, roles, solicitudes, sesiones, valoraciones), conexión con Google y Google Calendar, y documentación del proyecto.
Lei | Diseño de pantallas en Figma, interfaz visual del sistema, y pruebas de funcionamiento.

## 16. Cronograma del Proyecto (8 semanas)
Semana | Fechas | Etapa | Actividades
--- | --- | --- | ---
1 | 24–30 ago | Identificación de la problemática | Se identifica la dificultad de los estudiantes nuevos para encontrar orientación académica dentro de la institución, y se analiza el contexto del problema.
2 | 31 ago–6 sep | Propuesta de solución | Se define la idea de una plataforma de mentoría entre estudiantes como solución, y se delimita qué funciones tendrá.
3 | 7–13 sep | Planificación del proyecto | Se elabora el documento de planificación: objetivos, alcance, roles del equipo, cronograma y primeras maquetas de pantallas en Figma.
4 | 14–20 sep | Planificación y diseño | Se terminan las maquetas en Figma y se organiza la estructura del proyecto. Se crea el repositorio en GitHub con la base inicial del sistema.
5 | 21–27 sep | Desarrollo (parte 1) | Se construye el ingreso con cuenta de Google y la creación de perfiles de mentor y aprendiz.
6 | 28 sep–4 oct | Desarrollo (parte 2) | Se construye la búsqueda de mentores, el envío y aceptación de solicitudes, y la conexión con Google Calendar para agendar sesiones.
7 | 5–11 oct | Desarrollo (parte 3) y pruebas | Se agregan los recordatorios de sesiones, el sistema de valoraciones y el panel de administración. Se prueba que todo funcione correctamente.
8 | 12–18 oct | Viabilidad, sostenibilidad y entrega | Se revisa que el sistema pueda mantenerse en el tiempo (facilidad de agregar nuevas especialidades, bajo costo de mantenimiento al usar herramientas gratuitas), se corrigen detalles finales y se entrega el proyecto completo con su repositorio en GitHub.

## 17. Viabilidad y Sostenibilidad
El proyecto utiliza herramientas gratuitas o de bajo costo (base de datos incluida en el sistema, cuenta de Google para el inicio de sesión y el calendario), por lo que no requiere de un presupuesto elevado para mantenerse en funcionamiento. Al estarorganizado por especialidades, el sistema puede crecer fácilmente agregando nuevos temas de mentoría sin necesidad de rediseñar la plataforma. El principal riesgo identificado es la dependencia de la cuenta de Google para el inicio de sesión y el calendario: si un usuario no la  configura, puede seguir usando la plataforma con menos funciones (sin sincronización automática de sus sesiones).