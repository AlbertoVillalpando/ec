Característica: Subir archivos a una conferencia
Como autor o revisor
quiero subir archivos a una conferencia
para que puedan ser evaluados

Escenario: Subida exitosa de archivo ZIP
Dado que ingreso a la URL "http://127.0.0.1:8000/conferencias/participar/1"
Y selecciono el archivo válido "trabajo.zip"
Cuando presiono el botón "Entregar"
Entonces el sistema muestra el mensaje "Archivo enviado correctamente"

Escenario: Subida fallida por extensión no válida
Dado que ingreso a la URL "http://127.0.0.1:8000/conferencias/participar/1"
Y selecciono el archivo "trabajo.pdf"
Cuando presiono el botón "Entregar"
Entonces debo ver el mensaje de error "Solo se permiten archivos ZIP"
Y permanezco en la misma pantalla
