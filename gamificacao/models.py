from django.db import models
from django.contrib.auth.models import User


class PerfilGamificacao(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='gamificacao'
    )
    xp_total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.usuario.username} — {self.xp_total} XP'

    @property
    def nivel(self):
        # Cada 100 XP = 1 nível, começando do nível 1
        return (self.xp_total // 100) + 1

    @property
    def xp_no_nivel_atual(self):
        # Quanto XP dentro do nível atual (0 a 99)
        return self.xp_total % 100

    @property
    def percentual_nivel(self):
        # Para a barra de progresso: 0% a 100%
        return self.xp_no_nivel_atual  # já é 0-99, basta usar como %
    
    @property
    def titulo(self):
        titulos = {
            1:  'Calouro',
            2:  'Estudante',
            3:  'Dedicado',
            4:  'Aplicado',
            5:  'Focado',
            6:  'Persistente',
            7:  'Determinado',
            8:  'Avançado',
            9:  'Expert',
            10: 'Mestre',
        }
        return titulos.get(self.nivel, 'Mestre')