from django.db import models
from conferencia.models import Conferencia
from django.conf import settings

class Evaluacion(models.Model):
    conferencia = models.ForeignKey(Conferencia, on_delete=models.CASCADE)
    revisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    retroalimentacion = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('conferencia', 'revisor')

    def __str__(self):
        return f"Evaluación de {self.revisor} para {self.conferencia}"


class Pregunta(models.Model):
    conferencia = models.ForeignKey(Conferencia, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto

class Respuesta(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    puntaje = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f"{self.pregunta} - {self.puntaje}"
