from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from cronograma.models import Cronograma, Disciplina, SessaoEstudo


class DisciplinaModelTest(TestCase):

    def test_criar_disciplina(self):
        disciplina = Disciplina.objects.create(nome='Matemática', area='exatas')
        self.assertEqual(str(disciplina), 'Matemática')


class CronogramaModelTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='aluno', password='senha123')

    def test_criar_cronograma(self):
        cronograma = Cronograma.objects.create(
            aluno=self.usuario,
            titulo='Meu Cronograma',
            data_inicio=date.today(),
            data_fim=date(2025, 12, 31),
            ativo=True
        )
        self.assertEqual(str(cronograma), 'Meu Cronograma — aluno')


class SessaoEstudoModelTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='aluno', password='senha123')
        self.disciplina = Disciplina.objects.create(nome='Física', area='exatas')
        self.cronograma = Cronograma.objects.create(
            aluno=self.usuario,
            titulo='Cronograma',
            data_inicio=date.today(),
            data_fim=date(2025, 12, 31),
        )

    def test_criar_sessao(self):
        sessao = SessaoEstudo.objects.create(
            cronograma=self.cronograma,
            disciplina=self.disciplina,
            dia_semana=0,
            slot_horario=0,
            tipo='exercicio'
        )
        self.assertFalse(sessao.concluida)  

    def test_nao_permite_sessao_duplicada(self):
        SessaoEstudo.objects.create(
            cronograma=self.cronograma,
            disciplina=self.disciplina,
            dia_semana=0,
            slot_horario=0,
            tipo='exercicio'
        )
        with self.assertRaises(Exception):  
            SessaoEstudo.objects.create(
                cronograma=self.cronograma,
                disciplina=self.disciplina,
                dia_semana=0,
                slot_horario=0,
                tipo='revisao'
            )