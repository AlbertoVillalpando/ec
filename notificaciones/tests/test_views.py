# notificaciones/tests/test_views.py

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from notificaciones.models import Notificacion
from notificaciones.views import marcar_notificaciones_leidas


User = get_user_model()

class NotificacionesViewsTestCase(TestCase):
    def setUp(self):
        # Crear dos usuarios con emails únicos
        self.emisor = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='alicepass'
        )
        self.receptor = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='bobpass'
        )
        # Login como receptor
        self.client.login(username='bob', password='bobpass')
        # URLs de las vistas actuales (sin namespace)
        self.url_dropdown = reverse('dropdown_notificaciones')
        self.url_mark     = reverse('marcar_notificaciones_leidas')

    def test_dropdown_requires_authentication(self):
        # Logout para probar acceso anónimo
        self.client.logout()
        response = self.client.get(self.url_dropdown)
        self.assertEqual(response.status_code, 302)
        from django.conf import settings
        # Debe redirigir al login personalizado
        self.assertIn(settings.LOGIN_URL, response['Location'])

    def test_dropdown_shows_only_user_notifications(self):
        # Crear notificaciones para ambos usuarios
        n1 = Notificacion.objects.create(usuario=self.receptor, mensaje='Hola Bob')
        n2 = Notificacion.objects.create(usuario=self.emisor,   mensaje='Hola Alice')
        response = self.client.get(self.url_dropdown)
        self.assertEqual(response.status_code, 200)
        # Contexto bajo clave 'notificaciones'
        notis = response.context['notificaciones']
        self.assertIn(n1, notis)
        self.assertNotIn(n2, notis)
        # Comprobar plantilla parcial usada
        self.assertTemplateUsed(response, 'notificaciones/_dropdown.html')

    def test_dropdown_empty(self):
        # Sin notificaciones
        response = self.client.get(self.url_dropdown)
        self.assertEqual(response.status_code, 200)
        notis = response.context['notificaciones']
        self.assertEqual(list(notis), [])
        # Debe mostrar mensaje en HTML
        self.assertContains(response, 'Sin notificaciones nuevas')

    def test_dropdown_limit_to_five_latest(self):
        # Crear 6 notificaciones con fechas diferentes
        for i in range(6):
            Notificacion.objects.create(
                usuario=self.receptor,
                mensaje=f'Notif {i}',
                fecha=timezone.now() + timezone.timedelta(minutes=i)
            )
        response = self.client.get(self.url_dropdown)
        notis = list(response.context['notificaciones'])
        # Debe limitarse a 5
        self.assertEqual(len(notis), 5)
        # Los 5 más recientes (i=1..5)
        mensajes = [n.mensaje for n in notis]
        self.assertNotIn('Notif 0', mensajes)
        self.assertIn('Notif 5', mensajes)

    def test_dropdown_ordering_by_fecha(self):
        times = [timezone.now() + timezone.timedelta(days=d) for d in (2, 1, 0)]
        for d, t in zip(('A','B','C'), times):
            Notificacion.objects.create(
                usuario=self.receptor,
                mensaje=f'Notif {d}',
                fecha=t
            )
        response = self.client.get(self.url_dropdown)
        notis = list(response.context['notificaciones'])
        # Verificar orden ascendente por fecha (más antiguas primero)
        self.assertEqual([n.mensaje for n in notis], ['Notif C', 'Notif B', 'Notif A'])

    def test_mark_as_read_requires_post(self):
        # GET no permitido
        response = self.client.get(self.url_mark)
        self.assertEqual(response.status_code, 405)

    def test_mark_as_read_valid(self):
        # Crear notificaciones no leídas
        Notificacion.objects.create(usuario=self.receptor, mensaje='Tarea1', leida=False)
        Notificacion.objects.create(usuario=self.receptor, mensaje='Tarea2', leida=False)
        initial_unread = Notificacion.objects.filter(usuario=self.receptor, leida=False).count()
        response = self.client.post(self.url_mark)
        # JSON de éxito
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'ok'})
        # En BD deben marcarse todas como leídas
        self.assertEqual(Notificacion.objects.filter(usuario=self.receptor, leida=False).count(), 0)
        # Idempotencia: repetir POST no falla
        response2 = self.client.post(self.url_mark)
        self.assertEqual(response2.status_code, 200)
        self.assertJSONEqual(response2.content, {'status': 'ok'})

    def test_mark_as_read_other_user(self):
        # Crear notificación para otro usuario
        Notificacion.objects.create(usuario=self.emisor, mensaje='Privada', leida=False)
        count_before = Notificacion.objects.filter(usuario=self.emisor, leida=False).count()
        response = self.client.post(self.url_mark)
        self.assertEqual(response.status_code, 200)
        # No toca notificaciones ajenas
        count_after = Notificacion.objects.filter(usuario=self.emisor, leida=False).count()
        self.assertEqual(count_before, count_after)
        self.assertJSONEqual(response.content, {'status': 'ok'})

    def test_dropdown_renders_template_even_without_notifications(self):
        response = self.client.get(self.url_dropdown)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notificaciones/_dropdown.html')
        self.assertIn('notificaciones', response.context)

    def test_mark_as_read_method_not_allowed(self):
        # Usar la URL generada en setUp
        response = self.client.get(self.url_mark)
        self.assertEqual(response.status_code, 405)


    def test_marcar_como_leidas_view(self):
        # Configurar URL para la vista
        url = reverse('marcar_notificaciones_leidas')
        
        # Crear notificaciones no leídas
        Notificacion.objects.create(usuario=self.receptor, mensaje='Notif 1', leida=False)
        Notificacion.objects.create(usuario=self.receptor, mensaje='Notif 2', leida=False)
        
        # Hacer la petición POST
        response = self.client.post(url)
        
        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'ok'})
        
        # Verificar que las notificaciones se marcaron como leídas
        self.assertEqual(Notificacion.objects.filter(usuario=self.receptor, leida=False).count(), 0)

    def test_marcar_como_leidas_view_invalid_method(self):
        # Usar la URL generada en setUp
        response = self.client.get(self.url_mark)
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'Método no permitido'}
        )


    def test_marcar_como_leidas_csrf_exempt(self):
        """Verificar que la vista es realmente CSRF exempt"""
        from django.middleware.csrf import CsrfViewMiddleware
        from django.core.handlers.wsgi import WSGIRequest
        from io import BytesIO
        from django.conf import settings
        
        # Crear una request simulada sin CSRF token
        request = WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': 'application/json',
            'wsgi.input': BytesIO(b'{}'),
        })
        request.user = self.receptor
        
        # Procesar con middleware CSRF
        response = CsrfViewMiddleware(lambda r: JsonResponse({})).process_view(
            request, marcar_notificaciones_leidas, (), {}
        )
        
        # Si no es exempt, debería haber dado 403
        self.assertIsNone(response)