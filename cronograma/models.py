from django.db import models
from django.contrib.auth.models import User


class Disciplina(models.Model):
    AREA_CHOICES = [
        ('exatas', 'Ciências da Natureza e Matemática'),
        ('humanas', 'Ciências Humanas'),
        ('linguagens', 'Linguagens e Códigos'),
        ('redacao', 'Redação'),
    ]

    nome = models.CharField(max_length=100)
    cor_hex = models.CharField(max_length=7, default='#888888') 
    area = models.CharField(max_length=20, choices=AREA_CHOICES)

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Cronograma(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cronogramas')
    titulo = models.CharField(max_length=150, default='Meu Cronograma')
    data_inicio = models.DateField()
    data_fim = models.DateField()
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cronograma'
        verbose_name_plural = 'Cronogramas'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.titulo} — {self.aluno.username}'


class SessaoEstudo(models.Model):

    TIPO_CHOICES = [
        ('exercicio', 'Exercício'),
        ('revisao', 'Revisão'),
        ('simulado', 'Simulado'),
        ('pratica', 'Prática'),
        ('leitura', 'Leitura'),
    ]   
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='exercicio')

    DIA_SEMANA_CHOICES = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    cronograma = models.ForeignKey(
        Cronograma, on_delete=models.CASCADE, related_name='sessoes'
    )
    disciplina = models.ForeignKey(
        Disciplina, on_delete=models.SET_NULL, null=True, blank=True
    )
    dia_semana = models.IntegerField(choices=DIA_SEMANA_CHOICES)
    slot_horario = models.PositiveSmallIntegerField(
        help_text='Posição do bloco na grade (0 = primeiro slot do dia)'
    )
    descricao_atividade = models.CharField(
        max_length=200,
        blank=True,
        help_text='Ex: Lista de Exercícios 04 - P.A e P.G'
    )
    concluida = models.BooleanField(default=False)
    prioritaria = models.BooleanField(default=False) 
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sessão de Estudo'
        verbose_name_plural = 'Sessões de Estudo'
        unique_together = ('cronograma', 'dia_semana', 'slot_horario')
        ordering = ['dia_semana', 'slot_horario']

    def __str__(self):
        dia = self.get_dia_semana_display()
        disciplina = self.disciplina.nome if self.disciplina else 'Vazio'
        return f'{dia} | Slot {self.slot_horario} | {disciplina}'
