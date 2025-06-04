Característica: Login de usuarios
Como usuario registrado
quiero iniciar sesión ingresando mi correo y contraseña
para acceder al sistema

Escenario: Login con credenciales válidas
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/"
Y ingreso mi correo "autorP@autorP.com" y una contraseña incorrecta "P123456789"
Cuando presiono el botón "Iniciar sesión"
Entonces el sistema valida las credenciales y accede al menu donde se muestra "Bienvenido, Autor"

Escenario: Login con credenciales inválidas
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/"
Y ingreso mi correo "usuario@example.com" y una contraseña incorrecta "errorpass"
Cuando presiono el botón "Iniciar sesión"
Entonces el sistema valida las credenciales y muestra un mensaje "Usuario o contraseña incorrectos."
