from django.contrib.auth.models import AbstractUser
from django.db import models

# Áreas de conocimiento
AREAS_CONOCIMIENTO = [
    ('Ingenieria', 'Ingeniería'),
    ('Medicina', 'Medicina'),
    ('Letras', 'Letras'),
    ('Contabilidad', 'Contabilidad'),
]

class CustomUser(AbstractUser):
    area_conocimiento = models.CharField(max_length=50, choices=AREAS_CONOCIMIENTO)
    
    # Utilizamos los campos heredados de AbstractUser para nombre y apellidos
    # Si prefieres mantener los campos explícitos para nombre y apellidos, déjalos tal como están
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    def __str__(self):
        # Retorna el nombre completo si están definidos, de lo contrario, usa el username
        return f"{self.nombre} {self.apellidos} ({self.username})"
    
    # Aseguramos que el campo de correo sea único y utilizado como username
    email = models.EmailField(unique=True)
    username = models.EmailField(unique=True)  # Usamos el correo como username

    @property
    def conferencias_como_revisor(self):
        from conferencia.models import Conferencia
        return Conferencia.objects.filter(
            invitaciones_revisor__autor=self,
            invitaciones_revisor__estado='aceptado'
        )
