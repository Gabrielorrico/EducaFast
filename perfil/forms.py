from django import forms
from .models import Perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome_social', 'biografia']
        widgets = {
            'nome_social': forms.TextInput(attrs={
                'class': 'perfil-input',
                'placeholder': 'Seu nome social',
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'perfil-input',
                'placeholder': 'Conte um pouco sobre você...',
                'rows': 3,
            }),
        }
        labels = {
            'nome_social': 'Nome social',
            'biografia': 'Biografia',
        }