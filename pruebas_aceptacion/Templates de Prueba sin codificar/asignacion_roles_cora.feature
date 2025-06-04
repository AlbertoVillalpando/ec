Característica: Asignación de Roles
Como administrador
quiero asignar o actualizar roles a los usuarios
para gestionar sus permisos dentro del sistema

Escenario: Asignación o actualización de rol exitosa
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/admin/asignacion-roles"
Y visualizo la lista de usuarios registrados
Y selecciono un usuario de la lista
Y visualizo los detalles y roles actuales del usuario
Y selecciono el rol "Revisor"
Cuando presiono el botón "Actualizar rol"
Entonces el sistema valida la selección
Y actualiza el rol del usuario
Y muestra un mensaje de confirmación "El rol se ha actualizado con éxito"
Y vuelvo a la lista de usuarios

Escenario: Fallo en la asignación de roles por error del sistema
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/admin/asignacion-roles"
Y selecciono un usuario
Y intento actualizar el rol del usuario
Cuando presiono el botón "Actualizar rol"
Y ocurre un error del sistema (ej. error en la base de datos)
Entonces debo ver un mensaje "No se pudo completar la acción, intente de nuevo"
Y permanezco en la pantalla de asignación de roles