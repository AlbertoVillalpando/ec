Característica: Registro de Usuarios
Como nuevo usuario
quiero registrarme proporcionando mis datos (correo, contraseña, unidad académica y área de conocimiento)
para obtener una cuenta en el sistema

Escenario: Registro exitoso con datos correctos
Dado que ingreso a la plataforma en la URL "http://localhost:8000/usuarios/registro/"
Y ingreso mi nombre "jose emmanuel", apellido "sandoval sanchez", correo "usuario3@example.com" y una contraseña "ContrasenaSegura123"
Y confirmo la contraseña "ContrasenaSegura123"
Y selecciono el área de conocimiento "Medicina"
Cuando presiono el botón "Registrarse"
Entonces el sistema valida las credenciales y muestra un mensaje "¡Registro exitoso! Ya puedes iniciar sesión."


Escenario: Registro fallido por correo ya registrado
Dado que ingreso a la plataforma en la URL "http://localhost:8000/usuarios/registro/"
Y ingreso mi nombre "jose emmanuel", apellido "sandoval sanchez", correo "usuario3@example.com" y una contraseña "ContrasenaSegura123"
Y confirmo la contraseña "ContrasenaSegura123"
Y selecciono el área de conocimiento "Medicina"
Cuando presiono el botón "Registrarse"
Entonces debo ver un mensaje de error "User with this Email already exists."
