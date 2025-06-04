Característica: Reasignar documentos entre conferencias
Como administrador
quiero mover documentos entre conferencias activas
para reorganizar el contenido

Escenario: Reasignación exitosa de documento
Dado que ingreso al panel de usuarios
Y selecciono un usuario con documentos cargados
Y selecciono el documento "Trabajo A"
Y selecciono la conferencia "Evento Ciencia 2025"
Cuando presiono el botón "Reasignar"
Entonces el sistema muestra "El documento ha sido reasignado exitosamente"

Escenario: No hay conferencias activas
Dado que ingreso al panel de usuarios
Y selecciono un documento
Y no hay conferencias activas disponibles
Entonces el sistema muestra "No hay conferencias activas para reasignar"
