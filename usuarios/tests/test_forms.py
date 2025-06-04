import logging

from django.contrib.auth import get_user_model
from django.test import TestCase

from usuarios.forms import LoginForm, RegistroForm
from usuarios.models import CustomUser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

User = get_user_model()


class LoginFormTest(TestCase):
    def setUp(self):
        logger.info("[LoginFormTest] setUp: creando usuario de prueba")
        self.email = 'user@example.com'
        self.password = 'StrongPass1!'
        self.user = CustomUser.objects.create_user(
            username=self.email,
            email=self.email,
            password=self.password,
            nombre='Test',
            apellidos='User',
            area_conocimiento='Ingenieria'
        )
        logger.info("[LoginFormTest] Usuario creado: %s", self.email)

    def test_clean_username_user_not_found(self):
        logger.info(
            "[LoginFormTest] test_clean_username_user_not_found: iniciando")
        form = LoginForm(
            None, data={'username': 'noexists@example.com', 'password': 'irrelevant'})
        self.assertFalse(form.is_valid())
        logger.info("[LoginFormTest] errores recibidos: %s",
                    form.errors.as_json())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], [
                         'No se encuentra un usuario con ese correo.'])
        logger.info(
            "[LoginFormTest] test_clean_username_user_not_found: completado")

    def test_missing_username(self):
        logger.info("[LoginFormTest] test_missing_username: iniciando")
        form = LoginForm(None, data={'password': self.password})
        self.assertFalse(form.is_valid())
        logger.info("[LoginFormTest] errores recibidos: %s",
                    form.errors.as_json())
        self.assertIn('username', form.errors)
        logger.info("[LoginFormTest] test_missing_username: completado")

    def test_missing_password(self):
        logger.info("[LoginFormTest] test_missing_password: iniciando")
        form = LoginForm(None, data={'username': self.email})
        self.assertFalse(form.is_valid())
        logger.info("[LoginFormTest] errores recibidos: %s",
                    form.errors.as_json())
        self.assertIn('password', form.errors)
        logger.info("[LoginFormTest] test_missing_password: completado")

    def test_valid_credentials(self):
        logger.info("[LoginFormTest] test_valid_credentials: iniciando")
        form = LoginForm(
            None, data={'username': self.email, 'password': self.password})
        self.assertTrue(form.is_valid())
        logger.info(
            "[LoginFormTest] test_valid_credentials: credenciales válidas confirmadas")


class RegistroFormTest(TestCase):
    def setUp(self):
        logger.info("[RegistroFormTest] setUp: preparando datos de registro")
        self.email = 'new@example.com'
        self.data = {
            'nombre': 'Test',
            'apellidos': 'User',
            'email': self.email,
            'password1': 'StrongPass1!',
            'password2': 'StrongPass1!',
            'area_conocimiento': 'Ingenieria'
        }
        logger.info("[RegistroFormTest] datos iniciales: %s", self.data)

    def test_valid_registration(self):
        logger.info("[RegistroFormTest] test_valid_registration: iniciando")
        form = RegistroForm(data=self.data)
        self.assertTrue(form.is_valid())
        logger.info("[RegistroFormTest] form.is_valid OK")
        user = form.save()
        self.assertEqual(user.username, self.email)
        self.assertEqual(user.email, self.email)
        logger.info("[RegistroFormTest] Usuario registrado: %s", user.username)

    def test_duplicate_email_invalidates_form(self):
        logger.info(
            "[RegistroFormTest] test_duplicate_email_invalidates_form: iniciando")
        CustomUser.objects.create_user(
            username=self.email,
            email=self.email,
            password='OtherPass1!',
            nombre='Ex',
            apellidos='Ist',
            area_conocimiento='Medicina'
        )
        form = RegistroForm(data=self.data)
        self.assertFalse(form.is_valid())
        logger.info("[RegistroFormTest] errores recibidos: %s",
                    form.errors.as_json())
        self.assertIn('email', form.errors)
        logger.info(
            "[RegistroFormTest] test_duplicate_email_invalidates_form: completado")

    def test_empty_area_conocimiento(self):
        logger.info(
            "[RegistroFormTest] test_empty_area_conocimiento: iniciando")
        data = self.data.copy()
        data['area_conocimiento'] = ''
        form = RegistroForm(data=data)
        self.assertFalse(form.is_valid())
        logger.info("[RegistroFormTest] errores recibidos: %s",
                    form.errors.as_json())
        self.assertIn('area_conocimiento', form.errors)
        logger.info(
            "[RegistroFormTest] test_empty_area_conocimiento: completado")

    def test_passwords_mismatch(self):
        logger.info("[RegistroFormTest] test_passwords_mismatch: iniciando")
        data = self.data.copy()
        data['password2'] = 'Different1!'
        form = RegistroForm(data=data)
        self.assertFalse(form.is_valid())
        logger.info("[RegistroFormTest] errores recibidos: %s",
                    form.errors.as_json())
        self.assertIn('password2', form.errors)
        logger.info("[RegistroFormTest] test_passwords_mismatch: completado")

    def test_invalid_email_format(self):
        logger.info("[RegistroFormTest] test_invalid_email_format: iniciando")
        data = self.data.copy()
        data['email'] = 'notanemail'
        form = RegistroForm(data=data)
        self.assertFalse(form.is_valid())
        logger.info("[RegistroFormTest] errores recibidos: %s",
                    form.errors.as_json())
        self.assertIn('email', form.errors)
        logger.info("[RegistroFormTest] test_invalid_email_format: completado")
