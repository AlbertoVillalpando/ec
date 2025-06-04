Característica: Notificaciones

  Escenario: Notificación cuando el rol de un usuario cambia
    Dado El usuario ha iniciado sesión con su rol actual
    Cuando El rol del usuario cambia
    Entonces El usuario recibe una notificación sobre el cambio de rol

  Escenario: Notificación al autor de que su trabajo fue revisado
    Dado El autor ha iniciado sesión como autor
    Y Un autor ha enviado un trabajo para revisión
    Cuando El trabajo es revisado por un revisor
    Entonces El autor recibe una notificación indicando que su trabajo ha sido revisado

  Scenario: Notificación al autor de que su trabajo fue aceptado o rechazado
    Dado El autor ha iniciado sesión como autor
    Y Un autor ha enviado un trabajo para revisión
    Cuando El revisor acepta o rechaza el trabajo
    Entonces El autor recibe una notificación indicando si su trabajo fue aceptado o rechazado