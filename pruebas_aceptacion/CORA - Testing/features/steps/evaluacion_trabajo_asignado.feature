Característica: Evaluación de trabajos asignados
    Como revisor
    quiero evaluar trabajos asignados
    para completar el proceso de revisión

    Escenario: Evaluación completa y válida
        Dado que ingreso al módulo "Trabajos asignados"
        Y selecciono el trabajo "Trabajo A"
        Y completo todos los criterios con puntajes válidos
        Y agrego un comentario general
        Cuando presiono el botón "Enviar revisión"
        Entonces el sistema muestra "Evaluación registrada correctamente"

    Escenario: Evaluación incompleta
        Dado que ingreso al módulo "Trabajos asignados"
        Y selecciono el trabajo "Trabajo B"
        Y dejo un criterio sin contestar
        Cuando presiono el botón "Enviar revisión"
        Entonces debo ver un mensaje "Todos los campos son obligatorios"
        Y permanezco en el formulario de evaluación
