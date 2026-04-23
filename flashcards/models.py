from django.db import models
from django.contrib.auth.models import User


class Assunto(models.Model):
    """
    Representa um assunto/tópico dentro de uma matéria.
    Cada assunto possui um resumo e um conjunto de flashcards.
    """
    # Ajuste o app_label se a sua Materia estiver em outro app (ex: 'core.Materia')
    materia = models.ForeignKey(
        'sessaodeestudos.Materia',
        on_delete=models.CASCADE,
        related_name='assuntos',
        verbose_name='Matéria',
    )
    nome = models.CharField(max_length=200, verbose_name='Nome do assunto')
    resumo = models.TextField(
        verbose_name='Resumo',
        help_text='Resumo do assunto exibido na aba de flashcards.',
    )
    ordem = models.PositiveIntegerField(default=0, verbose_name='Ordem de exibição')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordem', 'nome']
        verbose_name = 'Assunto'
        verbose_name_plural = 'Assuntos'

    def __str__(self):
        return f'{self.materia.nome} — {self.nome}'

    @property
    def total_flashcards(self):
        return self.flashcards.count()


class Flashcard(models.Model):
    """
    Representa um card individual (frente/verso) vinculado a um assunto.
    """
    assunto = models.ForeignKey(
        Assunto,
        on_delete=models.CASCADE,
        related_name='flashcards',
        verbose_name='Assunto',
    )
    frente = models.TextField(
        verbose_name='Frente (pergunta/conceito)',
        help_text='Pergunta, conceito ou termo exibido na frente do card.',
    )
    verso = models.TextField(
        verbose_name='Verso (resposta/explicação)',
        help_text='Resposta ou explicação detalhada exibida no verso.',
    )
    ordem = models.PositiveIntegerField(default=0, verbose_name='Ordem')

    usuarios_que_estudaram = models.ManyToManyField(User, blank=True, related_name='flashcards_estudados')
    class Meta:
        ordering = ['ordem']
        verbose_name = 'Flashcard'
        verbose_name_plural = 'Flashcards'

    def __str__(self):
        return f'[{self.assunto.nome}] Card {self.ordem}: {self.frente[:60]}'

