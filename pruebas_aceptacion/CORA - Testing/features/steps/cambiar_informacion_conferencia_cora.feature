Característica: Cambiar Información de Conferencia
    Como administrador
    quiero modificar la información de una conferencia
    para actualizar sus datos cuando sea necesario

    Escenario: Modificación exitosa de la información de una conferencia
        Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000"
        Y ingreso como administrador
        Y selecciono el listado de conferencias
        Y selecciono la conferencia "Prueba template" presionando el boton Editar Conferencia
        Y modifico el nombre de la conferencia a "Conferencia Innovación 2025 - Edición"
        Cuando presiono el botón "Guardar cambios"
        Entonces podre ver la conferencia con nombre "Conferencia Innovación 2025 - Edición"

    Escenario: Cambio exitoso de fecha
        Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000"
        Y ingreso como administrador
        Y selecciono el listado de conferencias
        Y selecciono la conferencia "Conferencia Innovación 2025 - Edición" presionando el boton Editar Conferencia
        Y modifico la duracion a "1" meses, "3" dias, "4" horas y "23" minutos
        Cuando presiono el botón "Guardar cambios"
        Entonces podre ver la conferencia de nombre "Conferencia Innovación 2025 - Edición" con la fecha "1" meses, "3" dias, "4" horas y "23" minutos
