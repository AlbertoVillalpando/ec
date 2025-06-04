from django.test import TestCase
from formulario.models import Pregunta, Respuesta
from conferencia.models import Conferencia

class FormularioFormsTest(TestCase):
    def setUp(self):
        self.conferencia = Conferencia.objects.create(nombre="TestConf")

    def test_crear_pregunta_valida(self):
        pregunta = Pregunta.objects.create(conferencia=self.conferencia, texto="¿Cuál es tu experiencia?")
        self.assertEqual(pregunta.texto, "¿Cuál es tu experiencia?")
        self.assertEqual(pregunta.conferencia, self.conferencia)

    def test_crear_respuesta_valida(self):
        pregunta = Pregunta.objects.create(conferencia=self.conferencia, texto="¿Qué calificación das?")
        respuesta = Respuesta.objects.create(pregunta=pregunta, puntaje=4)
        self.assertEqual(respuesta.pregunta, pregunta)
        self.assertEqual(respuesta.puntaje, 4)

    def test_respuesta_fuera_de_rango(self):
        pregunta = Pregunta.objects.create(conferencia=self.conferencia, texto="¿Qué calificación das?")
        with self.assertRaises(ValueError):
            Respuesta.objects.create(pregunta=pregunta, puntaje=10)
