Característica: Responder invitación a revisar un trabajo
    Como revisor
    quiero aceptar o rechazar una invitación a revisar
    para confirmar mi participación

    Escenario: Aceptar una invitación de revisión
        Dado que recibí una invitación por correo para revisar un archivo
        Y accedo a la URL "http://127.0.0.1:8000/usuarios/invitaciones"
        Y selecciono "Aceptar" en la invitación
        Cuando confirmo la acción
        Entonces el sistema muestra "Has aceptado revisar este trabajo"
        Y el estado del documento se actualiza como "Aceptado"

    Escenario: Rechazar una invitación de revisión
        Dado que accedo a la URL "http://127.0.0.1:8000/usuarios/invitaciones"
        Y selecciono "Rechazar" en la invitación
        Cuando confirmo la acción
        Entonces el sistema muestra "Has rechazado revisar este trabajo"
        Y el documento puede ser reasignado
