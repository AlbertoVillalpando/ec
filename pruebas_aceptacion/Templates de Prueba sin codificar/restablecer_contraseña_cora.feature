Característica: Restablecimiento de Contraseña
Como usuario que olvidó su contraseña
quiero recuperar mi acceso mediante un enlace enviado a mi correo
para poder restablecer mi contraseña y volver a iniciar sesión

Escenario: Proceso exitoso de restablecimiento de contraseña
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/login"
Y hago clic en "¿Olvidaste tu contraseña?"
Y se muestra la pantalla de restablecimiento de contraseña
Y ingreso mi correo "usuario@example.com"
Cuando presiono el botón "Enviar"
Entonces el sistema valida que el correo exista
Y envía un enlace de restablecimiento al correo
Y muestro un mensaje "Se ha enviado un enlace para restablecer tu contraseña"

Escenario: Correo no registrado para restablecimiento
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/login"
Y hago clic en "¿Olvidaste tu contraseña?"
Y se muestra la pantalla de restablecimiento de contraseña
Y ingreso un correo "noexiste@example.com"
Cuando presiono el botón "Enviar"
Entonces debo ver un mensaje de error "El correo no está registrado"
Y se solicita volver a ingresar un correo válido