from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from cronograma.models import Cronograma, Disciplina, SessaoEstudo


class DisciplinaModelTest(TestCase):

    def test_criar_disciplina(self):
        """verifica se uma disciplina é criada corretamente no banco de dados """
        disciplina = Disciplina.objects.create(nome='Matemática', area='exatas')
        self.assertEqual(str(disciplina), 'Matemática')


class CronogramaModelTest(TestCase):

    def setUp(self):
        """cria um user falso antes de cada teste """
        self.usuario = User.objects.create_user(username='aluno', password='senha123')

    def test_cronograma_criado_para_usuario(self):
        """verifica se o cronograma criado é salvo atrelado ao usuario correto"""
        cronograma = Cronograma.objects.create(
            aluno=self.usuario,
            titulo='Meu Cronograma',
            data_inicio=date.today(),
            data_fim=date(2026, 12, 7),
            ativo=True
        )
        self.assertEqual(cronograma.aluno, self.usuario)


class SessaoEstudoModelTest(TestCase):

    def setUp(self):
        """Cria usuario disciplina e cronograma falsos antes de cada teste"""
        self.usuario = User.objects.create_user(username='aluno', password='senha123')
        self.disciplina = Disciplina.objects.create(nome='Física', area='exatas')
        self.cronograma = Cronograma.objects.create(
            aluno=self.usuario,
            titulo='Cronograma',
            data_inicio=date.today(),
            data_fim=date(2026, 12, 7),
        )

    def test_criar_sessao(self):
        """Verifica se uma sessão é criada e começa como nao concluida"""
        sessao = SessaoEstudo.objects.create(
            cronograma=self.cronograma,
            disciplina=self.disciplina,
            dia_semana=0,
            slot_horario=0,
            tipo='exercicio'
        )
        self.assertFalse(sessao.concluida)

    def test_sessao_com_prioridade(self):
        """Verifica se a prioridade é salva corretamente quando definida """
        sessao = SessaoEstudo.objects.create(
            cronograma=self.cronograma,
            disciplina=self.disciplina,
            dia_semana=1,
            slot_horario=0,
            tipo='simulado',
            prioridade='alta'
        )
        self.assertEqual(sessao.prioridade, 'alta')

    def test_sessao_sem_prioridade(self):
        """verifica se uma sessao criada sem prioridade fica como vazia """
        sessao = SessaoEstudo.objects.create(
            cronograma=self.cronograma,
            disciplina=self.disciplina,
            dia_semana=2,
            slot_horario=0,
            tipo='revisao',
        )
        self.assertIsNone(sessao.prioridade)