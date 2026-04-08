from django.db import models
from django.conf import settings


class Materia(models.Model):

    ICONE_CHOICES = [
        ("📐", "Matemática"),
        ("📖", "Língua Portuguesa"),
        ("✍️", "Redação"),
        ("🌎", "Ciências Humanas"),
        ("🔬", "Ciências da Natureza"),
    ]

    nome = models.CharField(max_length=100)
    icone = models.CharField(max_length=10, choices=ICONE_CHOICES, default="📐")
    classe_css = models.CharField(max_length=50, blank=True)
    ordem = models.PositiveSmallIntegerField(default=0, help_text="Ordem de exibição")

    class Meta:
        ordering = ["ordem"]
        verbose_name = "Matéria"
        verbose_name_plural = "Matérias"

    def __str__(self):
        return self.nome

    @property
    def total_topicos(self):
        return self.topicos.count()

    @property
    def subtitulo(self):
        n = self.total_topicos
        # "5 tópicos principais" / "5 competências" (Redação)
        sufixo = "competências" if self.nome == "Redação" else "tópicos principais"
        return f"{n} {sufixo}"


class Topico(models.Model):

    materia = models.ForeignKey(
        Materia, on_delete=models.CASCADE, related_name="topicos"
    )
    nome = models.CharField(max_length=200)
    ordem = models.PositiveSmallIntegerField(default=0, help_text="Ordem de exibição")

    class Meta:
        ordering = ["ordem"]
        verbose_name = "Tópico"
        verbose_name_plural = "Tópicos"

    def __str__(self):
        return f"{self.materia.nome} › {self.nome}"


class TopicoMarcado(models.Model):


    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="topicos_marcados",
    )
    topico = models.ForeignKey(
        Topico, on_delete=models.CASCADE, related_name="marcacoes"
    )
    marcado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que um usuário só marca um tópico uma vez
        unique_together = ("usuario", "topico")
        verbose_name = "Tópico Marcado"
        verbose_name_plural = "Tópicos Marcados"

    def __str__(self):
        return f"{self.usuario} marcou '{self.topico}'"