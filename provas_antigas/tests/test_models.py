from django.test import TestCase
from provas_antigas.models import Prova

class ProvaModelTest(TestCase):

    def setUp(self):
        """Cria a prova falsa antes de cada teste"""
        self.prova = Prova.objects.create(
            ano=2023,
            edicao='1º Dia',
            tipo='Regular',
            area_conhecimento='Matemática',
            total_questoes=45,
        )

    def test_criar_prova(self):
        """Verifica se a prov criada corretamente no banco"""
        self.assertEqual(self.prova.ano, 2023)

    def test_str_prova(self):
        """Verifica se o retorna o formato correto"""
        self.assertEqual(str(self.prova), 'ENEM 2023 — 1º Dia (Regular)')

    def test_prova_sem_pdf(self):
        """Verifica se uma prova pode ser criada sem PDF"""
        self.assertIsNone(self.prova.pdf_url)