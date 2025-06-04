# CORA



## Herramientas

    Django
    Contenedor Docker
    HTML
    CSS
    JS
    Bootstrap
    Behave
    Selenium
    Coverage

## Correr el sistema en pruebas

docker network create proxy

docker-compose up -d --build

docker-compose exec web bash

python3 manage.py check

python3 manage.py makemigrations

python3 manage.py migrate

#### En algunos casos puede suceder que docker-compose up ya ejecuta runserver, puedes probar entrando a http://localhost:8000/ , si no ejecutar:
python3 manage.py runserver 0.0.0.0:8000

## Correr pruebas de integracion

#### Ejecutar este comando en caso de que el proyecto no este corriendo
docker-compose up -d --build

docker-compose exec web bash

coverage run --branch --source='.' --omit="*/migrations/*,*test*,*__init__*,*settings*,*apps*,*wsgi.py*,*admin.py*,*asgi.py*,*manage.py*,*urls.py*" manage.py test

coverage report -m --fail-under 95

#### Si quieres ver archivo por archivo cual es el porcentaje se tiene que ejecutar:

coverage html

#### Este comando creara la carpeta llamada htmlcov, hay que entrar en esa carpeta y abrir en el navegador el index

## Pruebas BEHAVE

cd .\pruebas_aceptacion\CORA\

behave

## Usuarios de prueba
#### En caso de requerir hacer pruebas para los diferentes tipos de usuario se pueden usar las siguientes credenciales:

- adminP@adminP.com
- organizadorP@organizadorP.com
- revisorP@revisorP.com
- autorP@autorP.com

Para todos la contraseña es: P123456789
