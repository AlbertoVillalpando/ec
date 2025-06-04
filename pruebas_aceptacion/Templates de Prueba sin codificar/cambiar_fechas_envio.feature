Característica: Cambiar fechas de envío
Como administrador
quiero actualizar las fechas límite de envío de trabajos
para extender o limitar el periodo de recepción

Escenario: Cambio exitoso de fecha
Dado que ingreso al módulo de edición de conferencias
Y selecciono una conferencia existente
Y modifico la fecha de envío a una posterior
Cuando presiono "Guardar cambios"
Entonces el sistema muestra "Fecha de envío actualizada correctamente"

Escenario: Fecha menor a la actual
Dado que ingreso al módulo de edición de conferencias
Y modifico la fecha de envío a una anterior a la fecha actual
Cuando presiono "Guardar cambios"
Entonces el sistema muestra "La fecha debe ser mayor o igual a la actual"
