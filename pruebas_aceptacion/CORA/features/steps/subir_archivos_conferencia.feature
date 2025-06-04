Característica: Subir archivos a una conferencia
    Como autor o revisor
    quiero subir archivos a una conferencia
    para que puedan ser evaluados

    Escenario: Subida exitosa de archivo ZIP
        Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000"
        Y ingreso como autor
        Y selecciono el listado de conferencias como autor
        Y selecciono la conferencia "Azure´s Conferences" presionando el boton Subir
        Y subo el archivo .zip 
        Cuando presiono el botón Subir
        Entonces el sistema muestra el boton "Archivo" en la conferencia "Azure´s Conferences"

    Escenario: Subida fallida por extensión no válida
        Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000"
        Y ingreso como autor
        Y selecciono el listado de conferencias como autor
        Y selecciono la conferencia "Azure´s Conferences" presionando el boton Subir
        Y subo el archivo .jpeg
        Cuando presiono el botón Subir
        Entonces el sistema permanece en la misma vista
