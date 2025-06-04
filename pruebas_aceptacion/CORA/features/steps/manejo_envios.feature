Característica: Modificación y manejo de envíos

  Escenario: Modificar envío antes del deadline
      Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000"
      Y ingreso como autor
      Y selecciono el listado de conferencias como autor
      Y selecciono la conferencia "Azure´s Conferences" presionando el boton Subir
      Y subo el archivo .zip 
      Cuando presiono el botón Subir
      Entonces el sistema muestra el boton "Archivo" en la conferencia "Azure´s Conferences"
