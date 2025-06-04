from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class HomeViewTestCase(TestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # URL para la vista
        self.url = reverse('home')  # Asume que la URL se llama 'home'

    def test_home_view_renders_correct_template(self):
        """Prueba que la vista renderiza el template correcto"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_accessible_when_logged_in(self):
        """Prueba que la vista es accesible cuando el usuario está autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)