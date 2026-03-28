from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Materia(models.Model):
    """
    Representa uma matéria/disciplina disponível para estudo.
    """
    ICONE_CHOICES = [
        ('📐', 'Matemática'),
        ('📖', 'Português'),
        ('🔬', 'Ciências'),
        ('🌍', 'Geografia'),
        ('📜', 'História'),
        ('⚗️', 'Química'),
        ('⚡', 'Física'),
        ('🌿', 'Biologia'),
        ('🗣️', 'Inglês'),
        ('🎨', 'Artes'),
        ('📚', 'Outro'),
    ]

    nome = models.CharField(max_length=100, verbose_name='Nome da Matéria')
    icone = models.CharField(
        max_length=10,
        choices=ICONE_CHOICES,
        default='📚',
        verbose_name='Ícone'
    )
    cor = models.CharField(
        max_length=7,
        default='#7f8fdc',
        verbose_name='Cor (hex)',
        help_text='Ex: #7f8fdc'
    )

    class Meta:
        verbose_name = 'Matéria'
        verbose_name_plural = 'Matérias'
        ordering = ['nome']

    def __str__(self):
        return f'{self.icone} {self.nome}'


class SessaoDeEstudos(models.Model):
    """
    Registra cada sessão de estudo realizada pelo usuário,
    armazena a matéria escolhida, o tempo estudado (em segundos)
    e a data/hora de início da sessão.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessoes_estudo',
        verbose_name='Usuário'
    )
    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        related_name='sessoes',
        verbose_name='Matéria'
    )
    duracao_segundos = models.PositiveIntegerField(
        default=0,
        verbose_name='Duração (segundos)'
    )
    iniciada_em = models.DateTimeField(
        default=timezone.now,
        verbose_name='Iniciada em'
    )

    class Meta:
        verbose_name = 'Sessão de Estudos'
        verbose_name_plural = 'Sessões de Estudos'
        ordering = ['-iniciada_em']

    def __str__(self):
        return f'{self.usuario.username} — {self.materia.nome} ({self.duracao_formatada})'

    @property
    def duracao_formatada(self):
        """Retorna a duração da sessão no formato HH:MM:SS."""
        horas = self.duracao_segundos // 3600
        minutos = (self.duracao_segundos % 3600) // 60
        segundos = self.duracao_segundos % 60
        return f'{horas:02d}:{minutos:02d}:{segundos:02d}'
