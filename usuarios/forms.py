from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser  # Asegúrate de importar CustomUser

class LoginForm(AuthenticationForm):
    username = forms.EmailField() # Usamos 'username' pero representará el correo
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser  # Usamos CustomUser en lugar de User
        fields = ['username', 'password']

    def clean_username(self):
        # Validamos que el correo ingresado sea único y válido
        email = self.cleaned_data.get('username')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("No se encuentra un usuario con ese correo.")
        return email


AREAS = [
    ('Ingenieria', 'Ingenieria'),
    ('Medicina', 'Medicina'),
    ('Letras', 'Letras'),
    ('Contabilidad', 'Contabilidad'),
]

class RegistroForm(UserCreationForm):
    email = forms.EmailField()
    
    area_conocimiento = forms.ChoiceField(
        choices=[('', 'Seleccionar área')] + AREAS
    )

    class Meta:
        model = CustomUser
        fields = ['nombre', 'apellidos', 'email', 'password1', 'password2', 'area_conocimiento']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Usamos el correo como username
        user.email = self.cleaned_data['email']

        # Validación para asegurarnos de que no haya duplicados de correo
        if CustomUser.objects.filter(email=user.email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electrónico.")
        
        if commit:
            user.save()
        return user
