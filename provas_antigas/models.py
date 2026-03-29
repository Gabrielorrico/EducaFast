from django.db import models


class Prova(models.Model):
    ano = models.PositiveIntegerField()
    edicao = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20)
    area_conhecimento = models.CharField(max_length=50)
    total_questoes = models.PositiveIntegerField()
    pdf_url = models.URLField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ano', 'edicao']
        verbose_name = 'Prova'
        verbose_name_plural = 'Provas'

    def __str__(self):
        return f"ENEM {self.ano} — {self.edicao} ({self.tipo})"