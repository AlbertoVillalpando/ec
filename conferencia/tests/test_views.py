from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from conferencia.models import Conferencia
from conferencia.models import InvitacionRevisor
import json


User = get_user_model()

class ConferenciaViewTestCase(TestCase):
    def setUp(self):
        self.org_group = Group.objects.create(name='Organizador')
        self.autor_group = Group.objects.create(name='Autor')
        self.admin_group = Group.objects.create(name='Administrador')

        self.organizador = User.objects.create_user(username='org', password='pass', email='org@example.com')
        self.autor = User.objects.create_user(username='aut', password='pass', email='aut@example.com')
        self.admin = User.objects.create_user(username='admin', password='pass', email='admin@example.com', is_staff=True)
        self.revisor = User.objects.create_user(username='revisor', password='1234', email='revisor@example.com')

        self.org_group.user_set.add(self.organizador)
        self.autor_group.user_set.add(self.autor)
        self.admin_group.user_set.add(self.admin)

        self.conferencia = Conferencia.objects.create(
            nombre='Conf Inicial', meses=1, dias=1, horas=1, minutos=0,
            organizador=self.organizador, autor=self.autor
        )
        # Autenticar usuario organizador
        self.client.force_login(self.organizador)

    def test_conferencias_list_view_authenticated(self):
        url = reverse('conferencias_autor')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/conferencias_autor.html')
        self.assertIn('conferencias', response.context)

    def test_conferencia_create_view_get(self):
        url = reverse('crear_conferencia')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/crear_conferencia.html')


    def test_conferencia_create_view_post_valid(self):
        url = reverse('crear_conferencia')
        data = {
            'nombre': 'Nueva Conf',
            'meses': 0,
            'dias': 2,
            'horas': 3,
            'minutos': 30,
            'categoria': 'Ingenieria',  # Valor válido de AREAS_CONOCIMIENTO
            'organizador': self.organizador.id,
            'autor': self.autor.id,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('conferencias_administrador'))
        self.assertTrue(Conferencia.objects.filter(nombre='Nueva Conf').exists())




    def test_conferencia_create_view_post_invalid(self):
        url = reverse('crear_conferencia')
        data = {'nombre': '', 'meses': 'x'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/crear_conferencia.html')
        form = response.context.get('form')
        self.assertIsNotNone(form)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_conferencia_update_view_get(self):
        url = reverse('editar_conferencia', args=[self.conferencia.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/editar.html')
        self.assertIn('form', response.context)

    def test_conferencia_update_view_post_valid(self):
        url = reverse('editar_conferencia', args=[self.conferencia.pk])
        data = {
            'nombre': 'Updated',
            'meses': 2,
            'dias': 3,
            'horas': 0,
            'minutos': 15,
            'organizador': self.organizador.id,
            'autor': self.autor.id,
            'categoria': 'Ingenieria'  # <-- campo obligatorio agregado
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('conferencias_administrador'))
        self.conferencia.refresh_from_db()
        self.assertEqual(self.conferencia.nombre, 'Updated')


    def test_conferencia_update_view_post_invalid(self):
        url = reverse('editar_conferencia', args=[self.conferencia.pk])
        data = {'nombre': '', 'meses': -1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/editar.html')
        form = response.context.get('form')
        self.assertIsNotNone(form)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_subir_documentos_view_get(self):
        url = reverse('subir_documentos', args=[self.conferencia.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/subir_documentos.html')
        self.assertIn('conferencia', response.context)

    def test_subir_documento_zip_valido(self):
        url = reverse('subir_documentos', args=[self.conferencia.pk])
        archivo = SimpleUploadedFile('doc.zip', b'data', content_type='application/zip')
        response = self.client.post(url, {'archivo': archivo})
        self.assertRedirects(response, reverse('conferencias_autor'))
        self.conferencia.refresh_from_db()
        self.assertTrue(self.conferencia.archivo_zip.name)
        self.assertIn('.zip', self.conferencia.archivo_zip.name)

    def test_subir_documento_invalido_no_file(self):
        url = reverse('subir_documentos', args=[self.conferencia.pk])
        response = self.client.post(url, {})
        self.assertRedirects(response, url)

    def test_subir_documento_invalido_wrong_type(self):
        url = reverse('subir_documentos', args=[self.conferencia.pk])
        archivo = SimpleUploadedFile('doc.txt', b'data', content_type='text/plain')
        response = self.client.post(url, {'archivo': archivo})
        self.assertRedirects(response, url)

    def test_subir_documento_falta_archivo(self):
        url = reverse('subir_documentos', args=[self.conferencia.pk])
        response = self.client.post(url)  # sin archivo
        self.assertEqual(response.status_code, 302)  # redirige a sí mismo

    def test_subir_documento_extension_invalida(self):
        url = reverse('subir_documentos', args=[self.conferencia.pk])
        archivo = SimpleUploadedFile('archivo.txt', b'data', content_type='text/plain')
        response = self.client.post(url, {'archivo': archivo})
        self.assertEqual(response.status_code, 302)  # redirige a sí mismo

    def test_editar_conferencia_post_invalido(self):
        url = reverse('editar_conferencia', args=[self.conferencia.pk])
        data = {'nombre': '', 'meses': '', 'dias': '', 'horas': '', 'minutos': '', 'organizador': '', 'autor': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/editar.html')

    '''def test_invitar_autor_get(self):
        url = reverse('invitar_autor', args=[self.conferencia.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/invitar_autor.html')
    '''
    def test_ver_invitaciones_conferencia(self):
        url = reverse('invitaciones_conferencia', args=[self.conferencia.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/invitaciones_conferencia.html')

    def test_responder_invitacion_aceptar(self):
        invitacion = InvitacionRevisor.objects.create(conferencia=self.conferencia, autor=self.autor)
        url = reverse('responder_invitacion', args=[invitacion.pk, 'aceptar'])
        self.client.force_login(self.autor)
        response = self.client.get(url)
        invitacion.refresh_from_db()
        self.assertEqual(invitacion.estado, 'aceptado')

    def test_responder_invitacion_rechazar(self):
        invitacion = InvitacionRevisor.objects.create(conferencia=self.conferencia, autor=self.autor)
        url = reverse('responder_invitacion', args=[invitacion.pk, 'rechazar'])
        self.client.force_login(self.autor)
        response = self.client.get(url)
        invitacion.refresh_from_db()
        self.assertEqual(invitacion.estado, 'rechazado')

    def test_enviar_revision_post(self):
        self.client.force_login(self.revisor)
        data = {
            "conferencia_id": self.conferencia.pk,
            "decision": "aceptada"
        }
        url = reverse('enviar_revision_conferencia')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.conferencia.refresh_from_db()
        self.assertEqual(self.conferencia.estado_revision, 'aceptada')

    def test_enviar_revision_get(self):
        self.client.force_login(self.revisor)
        url = reverse('enviar_revision_conferencia')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)


    def test_reportar_trabajo_post(self):
        data = {"conferencia_id": self.conferencia.pk}
        url = reverse('reportar_trabajo')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.conferencia.refresh_from_db()
        self.assertTrue(self.conferencia.trabajo_reportado)

    def test_reportar_trabajo_get(self):
        url = reverse('reportar_trabajo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')

    def test_conferencias_administrador_view(self):
        self.client.force_login(self.admin)
        url = reverse('conferencias_administrador')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/conferencias_administrador.html')
        self.assertIn('conferencias', response.context)
        self.assertFalse(response.context['es_autor'])
        self.assertFalse(response.context['es_revisor'])

    def test_conferencias_revisor_view(self):
        # Crear una invitación para el revisor
        InvitacionRevisor.objects.create(
            conferencia=self.conferencia,
            autor=self.revisor,
            estado='aceptado'
        )
        
        self.client.force_login(self.revisor)
        url = reverse('conferencias_revisor')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/conferencias_revisor.html')
        self.assertEqual(len(response.context['conferencias']), 1)

    '''def test_evaluar_conferencia_view(self):
        self.client.force_login(self.revisor)
        url = reverse('evaluar_conferencia', args=[self.conferencia.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'formulario/evaluar_conferencia.html')
        self.assertEqual(response.context['conferencia'], self.conferencia)
        self.assertIn('preguntas', response.context)'''

    def test_autores_disponibles_view(self):
        # Crear un autor adicional que no esté invitado
        otro_autor = User.objects.create_user(username='otro', password='pass', email='otro@example.com')
        self.autor_group.user_set.add(otro_autor)
        
        # Crear una invitación para el autor existente
        InvitacionRevisor.objects.create(conferencia=self.conferencia, autor=self.autor)
        
        self.client.force_login(self.organizador)
        url = reverse('autores_disponibles', args=[self.conferencia.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # Debería devolver solo el autor no invitado
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['email'], 'otro@example.com')

    def test_invitar_autor_post(self):
        otro_autor = User.objects.create_user(username='otro', password='pass', email='otro@example.com')
        self.autor_group.user_set.add(otro_autor)
        
        self.client.force_login(self.organizador)
        url = reverse('invitar_autor', args=[self.conferencia.pk])
        response = self.client.post(url, {'autor': otro_autor.pk})
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(InvitacionRevisor.objects.filter(
            conferencia=self.conferencia, autor=otro_autor
        ).exists())

    '''def test_invitar_autor_get(self):
        # Asegurar que el autor está en el grupo correcto
        self.autor.groups.add(self.autor_group)
        
        # Crear una invitación existente para probar el contexto
        InvitacionRevisor.objects.create(
            conferencia=self.conferencia,
            autor=self.autor,
            estado='pendiente'
        )
        
        self.client.force_login(self.organizador)
        url = reverse('invitar_autor', args=[self.conferencia.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conferencia/invitar_autor.html')  # Asegúrate que este template existe
        self.assertIn('conferencia', response.context)
        self.assertIn('autores_disponibles', response.context)
        self.assertIn('invitaciones', response.context)
        
        # Verificar que los autores disponibles son correctos
        autores_disponibles = response.context['autores_disponibles']
        self.assertTrue(autores_disponibles.exists())  # Verifica que hay autores disponibles'''


    def test_eliminar_trabajo(self):
        # Primero necesitamos subir un archivo y marcarlo como reportado
        archivo = SimpleUploadedFile('doc.zip', b'data', content_type='application/zip')
        self.conferencia.archivo_zip = archivo
        self.conferencia.trabajo_reportado = True
        self.conferencia.save()
        
        self.client.force_login(self.admin)
        url = reverse('eliminar_trabajo', args=[self.conferencia.pk])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.conferencia.refresh_from_db()
        self.assertFalse(self.conferencia.trabajo_reportado)
        self.assertFalse(self.conferencia.archivo_zip)

