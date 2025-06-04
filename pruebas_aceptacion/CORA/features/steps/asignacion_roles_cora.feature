Característica: Asignación de Roles
Como administrador
quiero asignar o actualizar roles a los usuarios
para gestionar sus permisos dentro del sistema

Escenario: Asignación o actualización de rol exitosa
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000"
Y ingreso como administrador
Y selecciono el apartado Usuarios
Y al usuario con nombre "Pueba" de apellido "8" activo el rol "REVISOR"
Cuando presiono el botón Guardar Cambios
Entonces el sistema valida la selección y muestra en la columna ROL el texto "Revisor" del usuario "Pueba" "8"
