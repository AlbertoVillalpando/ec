from django import forms
from .models import Conferencia
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class ConferenciaForm(forms.ModelForm):
    class Meta:
        model = Conferencia
        fields = ['nombre', 'meses', 'dias', 'horas', 'minutos', 'organizador', 'autor', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'meses': forms.NumberInput(attrs={'class': 'form-control'}),
            'dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'horas': forms.NumberInput(attrs={'class': 'form-control'}),
            'minutos': forms.NumberInput(attrs={'class': 'form-control'}),
            'organizador': forms.Select(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            grupo_organizadores = Group.objects.get(name='Organizador')
            self.fields['organizador'].queryset = grupo_organizadores.user_set.all()
        except Group.DoesNotExist:
            self.fields['organizador'].queryset = User.objects.none()
        
        try:
            self.fields['autor'].queryset = Group.objects.get(name='Autor').user_set.all()
        except Group.DoesNotExist:
            self.fields['autor'].queryset = User.objects.none()

