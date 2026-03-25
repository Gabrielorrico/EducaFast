from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    meta_horas_estudo = models.PositiveIntegerField(default=2)  
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'