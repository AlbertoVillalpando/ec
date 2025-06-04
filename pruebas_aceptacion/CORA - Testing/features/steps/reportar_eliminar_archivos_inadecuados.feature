Característica: Reportar y eliminar archivos inadecuados

  Escenario: Reportar archivo subido como inadecuado
    Dado El revisor ha iniciado sesión como revisor
    Y Un revisor ha accedido a un archivo subido
    Cuando El revisor encuentra que el archivo no contiene la información adecuada
    Entonces El revisor puede reportar el archivo como inadecuado

  Escenario: Eliminar archivo subido reportado como inadecuado
    Dado El administrador ha iniciado sesión como administrador
    Y Un archivo ha sido reportado como inadecuado
    Cuando El administrador verifica que el archivo no contiene la información adecuada
    Entonces El administrador puede eliminar el archivo del sistema
