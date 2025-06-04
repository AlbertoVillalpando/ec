import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

from conferencia.models import InvitacionRevisor, Conferencia

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

User = get_user_model()


class UsuariosViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Usar get_or_create para evitar duplicados
        self.autor_group, _ = Group.objects.get_or_create(name='Autor')
        self.organizador_group, _ = Group.objects.get_or_create(name='Organizador')
        self.revisor_group, _ = Group.objects.get_or_create(name='Revisor')
        self.admin_group, _ = Group.objects.get_or_create(name='Administrador')
        
        self.user = User.objects.create_user(
            username='autor@example.com',
            email='autor@example.com',
            password='TestPass1!',
            nombre='Autor',
            apellidos='Unit',
            area_conocimiento='Ingenieria'
        )
        self.user.groups.add(self.autor_group)
            

    def test_login_get(self):
        #logger.info("[test_login_get] iniciando")
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/login.html')
        #logger.info("[test_login_get] completado")

    def test_login_post_valid(self):
        #logger.info("[test_login_post_valid] iniciando")
        data = {'username': 'autor@example.com', 'password': 'TestPass1!'}
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(response.url, reverse('vistaAutor'))
        #logger.info("[test_login_post_valid] completado")

    def test_login_post_invalid(self):
        #logger.info("[test_login_post_invalid] iniciando")
        data = {'username': 'wrong@example.com', 'password': 'bad'}
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuario o contraseña incorrectos.")
        #logger.info("[test_login_post_invalid] completado")

    def test_logout_redirect(self):
        #logger.info("[test_logout_redirect] iniciando")
        self.client.login(username='autor@example.com', password='TestPass1!')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        #logger.info("[test_logout_redirect] completado")

    def test_registro_get(self):
        #logger.info("[test_registro_get] iniciando")
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/registro.html')
        #logger.info("[test_registro_get] completado")

    def test_registro_post_valid(self):
        #logger.info("[test_registro_post_valid] iniciando")
        data = {
            'nombre': 'New',
            'apellidos': 'User',
            'email': 'new@example.com',
            'password1': 'NewPass1!',
            'password2': 'NewPass1!',
            'area_conocimiento': 'Medicina'
        }
        response = self.client.post(reverse('registro'), data=data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(email='new@example.com').exists())
        #logger.info("[test_registro_post_valid] completado")

    def test_registro_post_duplicate_email(self):
        #logger.info("[test_registro_post_duplicate_email] iniciando")
        User.objects.create_user(
            username='dup@example.com',
            email='dup@example.com',
            password='DupPass1!',
            nombre='Dup', apellidos='User', area_conocimiento='Letras'
        )
        data = {
            'nombre': 'Dup',
            'apellidos': 'User',
            'email': 'dup@example.com',
            'password1': 'DupPass1!',
            'password2': 'DupPass1!',
            'area_conocimiento': 'Letras'
        }
        response = self.client.post(reverse('registro'), data=data)
        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        self.assertIsNotNone(
            form, "El contexto debe contener el form con errores")
        self.assertIn('email', form.errors)
        #logger.info("[test_registro_post_duplicate_email] errores recibidos: %s", form.errors.as_json())
        #logger.info("[test_registro_post_duplicate_email] completado")

    def _login_as_admin(self):
        admin = User.objects.create_user(
            username='admin@example.com',
            email='admin@example.com',
            password='AdminPass1!',
            nombre='Admin', apellidos='User', area_conocimiento='Contabilidad'
        )
        admin.groups.add(Group.objects.get(name='Administrador'))
        self.client.login(username='admin@example.com', password='AdminPass1!')
        return admin

    def test_admin_dashboard(self):
        #logger.info("[test_admin_dashboard] iniciando")
        self._login_as_admin()
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/admin_dashboard.html')
        self.assertIn('users', response.context)
        #logger.info("[test_admin_dashboard] completado")

    def test_actualizar_roles(self):
        #logger.info("[test_actualizar_roles] iniciando")
        admin = self._login_as_admin()
        user2 = User.objects.create_user(
            username='user2@example.com', email='user2@example.com', password='Pass1!',
            nombre='User', apellidos='Two', area_conocimiento='Letras'
        )
        data = {f'roles_{user2.id}_organizador': 'on'}
        response = self.client.post(reverse('actualizar_roles'), data=data)
        self.assertRedirects(response, reverse('admin_dashboard'))
        self.assertTrue(user2.groups.filter(name='Organizador').exists())
        #logger.info("[test_actualizar_roles] completado")

    def test_vistaAutor_requires_login(self):
        #logger.info("[test_vistaAutor_requires_login] iniciando")
        url = reverse('vistaAutor')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        #logger.info("[test_vistaAutor_requires_login] completado")

    def test_vistaAutor_content(self):
        #logger.info("[test_vistaAutor_content] iniciando")
        self.client.login(username='autor@example.com', password='TestPass1!')
        response = self.client.get(reverse('vistaAutor'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_revisor'] in [True, False])
        self.assertTemplateUsed(response, 'usuarios/vistaAutor.html')
        #logger.info("[test_vistaAutor_content] completado")

    def test_invitaciones_autor_view(self):
        #logger.info("[test_invitaciones_autor_view] iniciando")
        self.client.login(username='autor@example.com', password='TestPass1!')
        response = self.client.get(reverse('invitaciones_autor'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/invitaciones.html')
        self.assertIn('invitaciones', response.context)
        #logger.info("[test_invitaciones_autor_view] completado")

    def test_responder_invitacion_accept(self):
        conf = Conferencia.objects.create(nombre='Conf Test')
        inv = InvitacionRevisor.objects.create(
            autor=self.user, conferencia=conf)
        self.client.login(username='autor@example.com', password='TestPass1!')
        self.client.post(reverse('responder_invitacion', args=[
                        inv.id]), data={'respuesta': 'aceptar'})
        inv.refresh_from_db()
        self.assertEqual(inv.estado, 'aceptado')  # Minúscula
        self.assertTrue(self.user.groups.filter(name='Revisor').exists())

    def test_responder_invitacion_reject(self):
        conf = Conferencia.objects.create(nombre='Conf Test')
        inv = InvitacionRevisor.objects.create(
            autor=self.user, conferencia=conf)
        self.client.login(username='autor@example.com', password='TestPass1!')
        self.client.post(reverse('responder_invitacion', args=[
                        inv.id]), data={'respuesta': 'rechazar'})
        inv.refresh_from_db()
        self.assertEqual(inv.estado, 'rechazado')  # Minúscula

    def test_login_view_invalid_credentials(self):
        # Prueba credenciales inválidas
        response = self.client.post(reverse('login'), {
            'username': 'noexiste@test.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuario o contraseña incorrectos.")

    def test_login_view_redirections(self):
        roles = {
            'Autor': 'vistaAutor',
            'Organizador': 'vistaOrganizador',
            'Revisor': 'vistaRevisor',
            'Administrador': 'vistaAdmin'
        }
        
        for role_name, redirect_name in roles.items():
            # Usar get_or_create para evitar duplicados
            group, _ = Group.objects.get_or_create(name=role_name)
            
            # Crear usuario con email único
            user = User.objects.create_user(
                username=f'{role_name.lower()}_test@example.com',
                email=f'{role_name.lower()}_test@example.com',
                password='testpass'
            )
            user.groups.add(group)
            
            # Usar POST para login en lugar de GET
            response = self.client.post(reverse('login'), {
                'username': user.email,
                'password': 'testpass'
            })
            
            # Verificar redirección
            self.assertRedirects(response, reverse(redirect_name),
                            msg_prefix=f"Failed for role {role_name}")
            
            # Limpiar logout para la siguiente iteración
            self.client.logout()

    def test_registro_view_existing_email(self):
        existing_user = User.objects.create_user(
            username='exist@test.com',
            email='exist@test.com',
            password='testpass',
            nombre='Exist',
            apellidos='User',
            area_conocimiento='Letras'
        )
        
        response = self.client.post(reverse('registro'), {
            'nombre': 'Test',
            'apellidos': 'User',
            'email': 'exist@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'area_conocimiento': 'Letras'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe Usuario con este Email.")

    def test_registro_view_success(self):
        response = self.client.post(reverse('registro'), {
            'nombre': 'New',
            'apellidos': 'User',
            'email': 'new@test.com',
            'password1': 'TestPass1!',
            'password2': 'TestPass1!',
            'area_conocimiento': 'Medicina'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email='new@test.com').exists())
        self.assertRedirects(response, reverse('login'))

    def test_actualizar_roles_add_remove(self):
        admin = User.objects.create_superuser(
            username='admin_test_roles',
            email='admin_test_roles@example.com',
            password='adminpass'
        )
        user = User.objects.create_user(
            username='testuser_roles',
            email='testuser_roles@example.com',
            password='testpass'
        )
        self.client.login(username='admin_test_roles', password='adminpass')
        
        # Añadir rol Organizador
        response = self.client.post(reverse('actualizar_roles'), {
            f'roles_{user.id}_organizador': 'on'
        })
        
        user.refresh_from_db()
        self.assertTrue(user.groups.filter(name='Organizador').exists())
        self.assertRedirects(response, reverse('admin_dashboard'))
        
        # Remover rol Organizador
        response = self.client.post(reverse('actualizar_roles'), {})
        user.refresh_from_db()
        self.assertFalse(user.groups.filter(name='Organizador').exists())

    def test_vista_autor_with_roles(self):
        # Usar get_or_create para evitar duplicados
        group, _ = Group.objects.get_or_create(name='Autor')
        
        user = User.objects.create_user(
            username='autor_test@example.com',
            email='autor_test@example.com',
            password='testpass'
        )
        user.groups.add(group)
        
        self.client.login(username='autor_test@example.com', password='testpass')
        
        response = self.client.get(reverse('vistaAutor'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_organizador'])  # Verificar que no es organizador


    def tearDown(self):
        User.objects.all().delete()
        # No borres los grupos aquí si se crean en setUp