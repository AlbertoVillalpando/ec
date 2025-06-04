from django.test import TestCase, Client
from django.urls import reverse
from conferencia.models import Conferencia
from formulario.models import Pregunta, Respuesta, Evaluacion
from notificaciones.models import Notificacion
from django.contrib.auth import get_user_model

User = get_user_model()

class FormularioViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Crear usuarios de prueba
        self.usuario = User.objects.create_user(
            username='revisorP',
            email='revisorP@revisorP.com',
            password='P123456789'
        )
        self.autor = User.objects.create_user(
            username='autorP',
            email='autorP@autorP.com',
            password='P123456789'
        )

        # Login del revisor
        self.client.force_login(self.usuario)

        # Crear conferencia
        self.conferencia = Conferencia.objects.create(nombre="Conf de prueba", autor=self.autor)

        # URLs
        self.crear_url = reverse('crear_formulario', args=[self.conferencia.id])
        self.ver_url = reverse('ver_formulario', args=[self.conferencia.id])
        self.evaluar_url = reverse('evaluar_conferencia', args=[self.conferencia.id])
        self.ver_eval_url = reverse('ver_evaluacion', args=[self.conferencia.id])

    def test_crear_formulario_get(self):
        response = self.client.get(self.crear_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'formulario/crear_formulario.html')

    def test_crear_formulario_post_valido(self):
        response = self.client.post(self.crear_url, data={'preguntas': ['Pregunta 1', 'Pregunta 2']})
        self.assertEqual(Pregunta.objects.filter(conferencia=self.conferencia).count(), 2)

    def test_crear_formulario_post_vacio(self):
        response = self.client.post(self.crear_url, data={'preguntas': ['   ', '']})
        self.assertEqual(Pregunta.objects.filter(conferencia=self.conferencia).count(), 0)

    def test_ver_formulario_get(self):
        Pregunta.objects.create(conferencia=self.conferencia, texto="¿Cómo evalúas?")
        response = self.client.get(self.ver_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'formulario/ver_formulario.html')
        self.assertContains(response, "¿Cómo evalúas?")

    def test_ver_formulario_post_respuestas_validas(self):
        p1 = Pregunta.objects.create(conferencia=self.conferencia, texto="P1")
        p2 = Pregunta.objects.create(conferencia=self.conferencia, texto="P2")
        data = {f"respuesta_{p1.id}": "4", f"respuesta_{p2.id}": "5"}
        response = self.client.post(self.ver_url, data=data)
        self.assertEqual(Respuesta.objects.count(), 2)
        self.assertRedirects(response, reverse('conferencia'))

    def test_ver_formulario_post_sin_respuestas(self):
        Pregunta.objects.create(conferencia=self.conferencia, texto="P1")
        response = self.client.post(self.ver_url, data={})
        self.assertEqual(Respuesta.objects.count(), 0)

    def test_evaluar_conferencia_get(self):
        Pregunta.objects.create(conferencia=self.conferencia, texto="Pregunta 1")
        response = self.client.get(self.evaluar_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'formulario/evaluar_conferencia.html')

    def test_evaluar_conferencia_post(self):
        p1 = Pregunta.objects.create(conferencia=self.conferencia, texto="Pregunta 1")
        p2 = Pregunta.objects.create(conferencia=self.conferencia, texto="Pregunta 2")

        data = {
            f'respuesta_{p1.id}': '3',
            f'respuesta_{p2.id}': '4',
            'retroalimentacion': 'Buen trabajo'
        }

        response = self.client.post(self.evaluar_url, data=data)
        self.assertRedirects(response, reverse('conferencias_revisor'))

        evaluacion = Evaluacion.objects.get(conferencia=self.conferencia, revisor=self.usuario)
        self.assertEqual(evaluacion.retroalimentacion, 'Buen trabajo')
        self.assertEqual(evaluacion.respuestas.count(), 2)

        notificacion = Notificacion.objects.get(usuario=self.autor)
        self.assertIn("ha sido evaluada", notificacion.mensaje)

    def test_ver_evaluacion_get(self):
        evaluacion = Evaluacion.objects.create(conferencia=self.conferencia, revisor=self.usuario)
        response = self.client.get(self.ver_eval_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'formulario/ver_evaluacion.html')
        self.assertContains(response, self.conferencia.nombre)
