from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_app')
    nome_social = models.CharField(max_length=100, blank=True)
    biografia = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'

    def get_materia_preferida(self):
        from sessaodeestudos.models import SessaoDeEstudos
        from django.db.models import Sum

        resultado = (
            SessaoDeEstudos.objects
            .filter(usuario=self.usuario)
            .values('materia__nome', 'materia__icone')
            .annotate(total=Sum('duracao_segundos'))
            .order_by('-total')
            .first()
        )
        return resultado if resultado else None