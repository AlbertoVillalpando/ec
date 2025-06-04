Característica: Creación de Conferencia
Como administrador u organizador
quiero crear una conferencia
para gestionar la carga y evaluación de trabajos académicos

Escenario: Creación exitosa de una conferencia
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/admin/conferencias"
Y hago clic en "Crear conferencia"
Y se muestra el formulario de creación de conferencias
Y ingreso el nombre "Conferencia Innovación 2025"
Y selecciono el área de conocimiento correspondiente
Y ingreso el deadline para envíos con fecha válida (mayor o igual a la fecha actual)
Y ingreso el número de revisores por trabajo
Y selecciono la opción "Definir criterios de evaluación"
Y ingreso la cantidad y descripción de cada criterio
Cuando presiono el botón "Crear"
Entonces el sistema valida los datos
Y crea la conferencia
Y redirige al listado actualizado de conferencias donde se visualiza "Conferencia Innovación 2025"

Escenario: Fallo en la creación por nombre duplicado
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/admin/conferencias"
Y hago clic en "Crear conferencia"
Y ingreso un nombre que ya existe "Conferencia Innovación 2025"
Cuando presiono el botón "Crear"
Entonces el sistema muestra una notificación "El nombre de la conferencia ya está registrado"
Y permanezco en la pantalla de creación

Escenario: Error en la creación por deadline inválido
Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/admin/conferencias"
Y hago clic en "Crear conferencia"
Y ingreso un deadline menor a la fecha actual
Cuando presiono el botón "Crear"
Entonces el sistema notifica "La fecha debe ser mayor o igual a la fecha actual"
Y se solicita corregir la fecha