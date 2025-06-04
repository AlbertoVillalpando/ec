from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from conferencia.forms import ConferenciaForm

User = get_user_model()

class ConferenciaFormTestCase(TestCase):
    def setUp(self):
        self.organizador_user = User.objects.create_user(
            username='org1', password='pass', email='org1@example.com'
        )
        self.autor_user = User.objects.create_user(
            username='autor1', password='pass', email='autor1@example.com'
        )
        # Prepare valid form data
        self.valid_data = {
            'nombre': 'Test Conference',
            'meses': 1,
            'dias': 2,
            'horas': 3,
            'minutos': 30,
        }

    def test_widget_attributes(self):
        form = ConferenciaForm()
        for field_name in ['nombre', 'meses', 'dias', 'horas', 'minutos']:
            widget = form.fields[field_name].widget
            self.assertIn('class', widget.attrs)
            self.assertEqual(widget.attrs['class'], 'form-control')

    def test_init_no_groups(self):
        Group.objects.filter(name='Organizador').delete()
        Group.objects.filter(name='Autor').delete()
        form = ConferenciaForm()
        self.assertQuerySetEqual(form.fields['organizador'].queryset, [], transform=repr)
        self.assertQuerySetEqual(form.fields['autor'].queryset, [], transform=repr)

    def test_init_with_groups_but_no_users(self):
        Group.objects.create(name='Organizador')
        Group.objects.create(name='Autor')
        form = ConferenciaForm()
        self.assertQuerySetEqual(form.fields['organizador'].queryset, [], transform=repr)
        self.assertQuerySetEqual(form.fields['autor'].queryset, [], transform=repr)

    def test_init_with_groups_and_users(self):
        org_group = Group.objects.create(name='Organizador')
        autor_group = Group.objects.create(name='Autor')
        org_group.user_set.add(self.organizador_user)
        autor_group.user_set.add(self.autor_user)
        form = ConferenciaForm()
        self.assertQuerySetEqual(
            form.fields['organizador'].queryset,
            [repr(self.organizador_user)],
            transform=repr
        )
        self.assertQuerySetEqual(
            form.fields['autor'].queryset,
            [repr(self.autor_user)],
            transform=repr
        )

    def test_valid_form_data(self):
        org_group = Group.objects.create(name='Organizador')
        autor_group = Group.objects.create(name='Autor')
        org_group.user_set.add(self.organizador_user)
        autor_group.user_set.add(self.autor_user)
        data = self.valid_data.copy()
        data['organizador'] = self.organizador_user.pk
        data['autor'] = self.autor_user.pk
        form = ConferenciaForm(data=data)
        self.assertTrue(form.is_valid())
        conference = form.save()
        self.assertEqual(conference.nombre, data['nombre'])
        self.assertEqual(conference.meses, data['meses'])
        self.assertEqual(conference.dias, data['dias'])
        self.assertEqual(conference.horas, data['horas'])
        self.assertEqual(conference.minutos, data['minutos'])
        self.assertEqual(conference.organizador, self.organizador_user)
        self.assertEqual(conference.autor, self.autor_user)

    def test_invalid_missing_nombre(self):
        Group.objects.create(name='Organizador').user_set.add(self.organizador_user)
        Group.objects.create(name='Autor').user_set.add(self.autor_user)
        data = self.valid_data.copy()
        data.pop('nombre')  # Explicitly remove 'nombre'
        data['organizador'] = self.organizador_user.pk
        data['autor'] = self.autor_user.pk
        form = ConferenciaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_invalid_non_integer_fields(self):
        Group.objects.create(name='Organizador').user_set.add(self.organizador_user)
        Group.objects.create(name='Autor').user_set.add(self.autor_user)
        data = self.valid_data.copy()
        data.update({
            'organizador': self.organizador_user.pk,
            'autor': self.autor_user.pk,
            'meses': 'not-a-number',
            'dias': 5,
            'horas': 2,
            'minutos': 15
        })
        form = ConferenciaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('meses', form.errors)
