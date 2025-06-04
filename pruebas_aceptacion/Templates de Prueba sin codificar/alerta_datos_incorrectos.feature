Característica: Alertas de datos incorrectos al iniciar sesión
Como usuario registrado
quiero recibir retroalimentación cuando ingreso credenciales inválidas
para saber que debo corregir los datos ingresados

Escenario: Mostrar mensaje de error por contraseña incorrecta
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/usuarios/login"
Y escribo el correo "usuario@example.com" y la contraseña "incorrecta123"
Cuando presiono el botón "Iniciar sesión"
Entonces debo ver un mensaje "Usuario o contraseña incorrectos."

Escenario: Mostrar error por email no registrado
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/usuarios/login"
Y escribo un correo "noexiste@example.com" y una contraseña cualquiera
Cuando presiono el botón "Iniciar sesión"
Entonces debo ver un mensaje "No se encuentra un usuario con ese correo."
