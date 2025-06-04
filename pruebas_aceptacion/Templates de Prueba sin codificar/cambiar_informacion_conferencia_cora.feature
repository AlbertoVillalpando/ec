Característica: Cambiar Información de Conferencia
Como administrador
quiero modificar la información de una conferencia
para actualizar sus datos cuando sea necesario

Escenario: Modificación exitosa de la información de una conferencia
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/admin/conferencias"
Y visualizo el listado de conferencias
Y selecciono una conferencia para editar
Y se muestra el panel de edición
Y modifico el nombre de la conferencia a "Conferencia Innovación 2025 - Edición"
Cuando presiono el botón "Confirmar cambios"
Entonces el sistema realiza las modificaciones
Y redirige al listado actualizado con la nueva información

Escenario: Fallo al guardar cambios en la conferencia
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/admin/conferencias"
Y selecciono una conferencia para editar
Y modifico la información de la conferencia
Cuando presiono el botón "Confirmar cambios"
Y ocurre un fallo en la operación (error al guardar)
Entonces debo ver un mensaje de error "Error al guardar los cambios"
Y la conferencia se mantiene sin modificaciones en el listado