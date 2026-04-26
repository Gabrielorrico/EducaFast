from django.test import TestCase
from django.contrib.auth.models import User
from flashcards.models import Assunto, Flashcard
from sessaodeestudos.models import Materia


class AssuntoModelTest(TestCase):

    def setUp(self):
        self.materia = Materia.objects.create(nome='Matemática')

    def test_criar_assunto(self):
        assunto = Assunto.objects.create(
            materia=self.materia,
            nome='Funções',
            resumo='Estudo de funções'
        )
        self.assertEqual(str(assunto), 'Matemática — Funções')

    def test_total_flashcards(self):
        assunto = Assunto.objects.create(
            materia=self.materia,
            nome='Álgebra',
            resumo='Resumo'
        )

        Flashcard.objects.create(
            assunto=assunto,
            frente='Pergunta 1',
            verso='Resposta 1'
        )

        Flashcard.objects.create(
            assunto=assunto,
            frente='Pergunta 2',
            verso='Resposta 2'
        )

        self.assertEqual(assunto.total_flashcards, 2)


class FlashcardModelTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='aluno', password='senhaSegura@123!')

        self.materia = Materia.objects.create(nome='Física')

        self.assunto = Assunto.objects.create(
            materia=self.materia,
            nome='Cinemática',
            resumo='Movimento'
        )

    def test_criar_flashcard(self):
        flashcard = Flashcard.objects.create(
            assunto=self.assunto,
            frente='O que é velocidade?',
            verso='Variação da posição no tempo'
        )

        self.assertEqual(flashcard.assunto, self.assunto)
        self.assertEqual(flashcard.ordem, 0)

    def test_str_flashcard(self):
        flashcard = Flashcard.objects.create(
            assunto=self.assunto,
            frente='Pergunta teste',
            verso='Resposta'
        )

        self.assertIn('Pergunta teste', str(flashcard))

    def test_usuario_estudou_flashcard(self):
        flashcard = Flashcard.objects.create(
            assunto=self.assunto,
            frente='Pergunta',
            verso='Resposta'
        )

        flashcard.usuarios_que_estudaram.add(self.usuario)

        self.assertIn(self.usuario, flashcard.usuarios_que_estudaram.all())

    def test_flashcard_sem_usuario(self):
        flashcard = Flashcard.objects.create(
            assunto=self.assunto,
            frente='Pergunta',
            verso='Resposta'
        )

        self.assertEqual(flashcard.usuarios_que_estudaram.count(), 0)