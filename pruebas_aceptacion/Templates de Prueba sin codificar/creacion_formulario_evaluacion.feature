Característica: Creación de formulario para evaluación
Como administrador
quiero definir criterios de evaluación en una conferencia
para evaluar los trabajos cargados

Escenario: Creación exitosa del formulario
Dado que ingreso al módulo de conferencias
Y selecciono la opción "Definir formulario"
Y elijo el tipo de calificación "Cuantitativa"
Y confirmo mi elección
Entonces el sistema muestra "Formulario de evaluación creado exitosamente"

Escenario: No se selecciona tipo de calificación
Dado que ingreso al módulo de conferencias
Y selecciono la opción "Definir formulario"
Y no elijo ningún tipo de calificación
Cuando presiono el botón "Confirmar"
Entonces debo ver un mensaje "Debe seleccionar un tipo de calificación"
