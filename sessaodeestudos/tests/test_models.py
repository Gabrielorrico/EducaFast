from django.test import TestCase
from django.contrib.auth.models import User
from sessaodeestudos.models import Materia, SessaoDeEstudos


class MateriaModelTest(TestCase):

    def test_criar_materia(self):
        """verifica se a materia é criada corretamente"""
        materia = Materia.objects.create(nome='Matemática')
        self.assertEqual(str(materia), '📚 Matemática')

    def test_valores_padrao(self):
        """verifica valores default de icone e cor"""
        materia = Materia.objects.create(nome='História')

        self.assertEqual(materia.icone, '📚')
        self.assertEqual(materia.cor, '#7f8fdc')


class SessaoDeEstudosModelTest(TestCase):

    def setUp(self):
        """cria usuario e materia falsos"""
        self.usuario = User.objects.create_user(username='aluno', password='senha123')
        self.materia = Materia.objects.create(nome='Física')

    def test_criar_sessao(self):
        """verifica se a sessao é criada corretamente"""
        sessao = SessaoDeEstudos.objects.create(
            usuario=self.usuario,
            materia=self.materia,
            duracao_segundos=120
        )

        self.assertEqual(sessao.usuario, self.usuario)
        self.assertEqual(sessao.materia, self.materia)

    def test_duracao_formatada(self):
        """verifica conversao de segundos para HH:MM:SS"""
        sessao = SessaoDeEstudos.objects.create(
            usuario=self.usuario,
            materia=self.materia,
            duracao_segundos=3661
        )

        self.assertEqual(sessao.duracao_formatada, '01:01:01')

    def test_str_sessao(self):
        """verifica representacao em string"""
        sessao = SessaoDeEstudos.objects.create(
            usuario=self.usuario,
            materia=self.materia,
            duracao_segundos=60
        )

        self.assertIn('aluno', str(sessao))
        self.assertIn('Física', str(sessao))