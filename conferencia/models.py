from django.conf import settings  # para usar AUTH_USER_MODEL
from django.db import models
from django.core.validators import FileExtensionValidator

AREAS_CONOCIMIENTO = [
    ('Ingenieria', 'Ingeniería'),
    ('Medicina', 'Medicina'),
    ('Letras', 'Letras'),
    ('Contabilidad', 'Contabilidad'),
]

class Conferencia(models.Model):
    nombre = models.CharField(max_length=255)
    meses = models.IntegerField(default=0)
    dias = models.IntegerField(default=0)
    horas = models.IntegerField(default=0)
    minutos = models.IntegerField(default=0)
    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conferencias_organizadas'
    )
    categoria = models.CharField(max_length=50, choices=AREAS_CONOCIMIENTO)
    
    estado_revision = models.CharField(max_length=20, choices=[("aceptado", "Aceptado"), ("rechazado", "Rechazado")], blank=True, null=True)
    trabajo_reportado = models.BooleanField(default=False)

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conferencias_autorias'
    )
    archivo_zip = models.FileField(upload_to='conferencias_zips/', null=True, blank=True, validators=[FileExtensionValidator(['zip'])])

    def __str__(self):
        return self.nombre
    
    @property
    def invitaciones(self):
        return InvitacionRevisor.objects.filter(conferencia=self)

class InvitacionRevisor(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]

    conferencia = models.ForeignKey(
        Conferencia,
        on_delete=models.CASCADE,
        related_name='invitaciones_revisor'  # <--- ESTA LÍNEA ES NUEVA
    )
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.nombre} - {self.conferencia.nombre} ({self.estado})"
    


