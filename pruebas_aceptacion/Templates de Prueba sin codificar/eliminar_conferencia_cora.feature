Característica: Eliminar Conferencia
Como administrador
quiero eliminar una conferencia
para actualizar el listado y remover eventos que ya no se requieran

Escenario: Eliminación exitosa de una conferencia
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/admin/conferencias"
Y visualizo el listado de conferencias
Y selecciono la opción "Eliminar" para la conferencia "Conferencia Innovación 2025"
Cuando confirmo la eliminación
Entonces el sistema elimina la conferencia
Y redirige al listado actualizado sin "Conferencia Innovación 2025"

Escenario: Error en la eliminación de una conferencia
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/admin/conferencias"
Y selecciono la opción "Eliminar" para una conferencia
Cuando confirmo la eliminación
Y ocurre un error en la operación (por ejemplo, fallo en la base de datos)
Entonces debo ver un mensaje "Error al eliminar la conferencia"
Y el listado continúa mostrando la conferencia que se intentó eliminar