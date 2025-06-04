Característica: Invitar revisores manualmente
    Como organizador
    quiero asignar revisores a documentos manualmente
    para controlar el proceso de revisión

    Escenario: Asignación manual de revisor a documento
        Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000/organizador/documentos-pendientes"
        Y selecciono el documento "Trabajo A"
        Y selecciono el revisor "revisor@example.com"
        Cuando presiono el botón "Asignar"
        Entonces el sistema muestra "Se ha enviado una invitación al revisor seleccionado"
        Y el documento queda marcado como "En espera de aceptación"
