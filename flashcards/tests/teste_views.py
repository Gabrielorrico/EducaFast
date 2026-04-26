from django.test import TestCase, Client
from django.contrib.auth.models import User
from flashcards.models import Assunto, Flashcard
from sessaodeestudos.models import Materia


class FlashcardViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(username='aluno', password='senha123')
        self.client.login(username='aluno', password='senha123')

        self.materia = Materia.objects.create(
            nome='Matemática',
            icone='📘',
            cor='#000'
        )

        self.assunto = Assunto.objects.create(
            materia=self.materia,
            nome='Funções',
            resumo='Resumo de funções'
        )

        self.flashcard = Flashcard.objects.create(
            assunto=self.assunto,
            frente='O que é função?',
            verso='Uma relação entre conjuntos'
        )

    def test_pagina_index_carrega(self):
        """verifica se a pagina principal carrega"""
        resposta = self.client.get('/flashcards/')
        self.assertEqual(resposta.status_code, 200)

    def test_api_assuntos(self):
        """verifica se a API de assuntos retorna dados"""
        resposta = self.client.get(f'/flashcards/api/assuntos/{self.materia.id}/')
        self.assertEqual(resposta.status_code, 200)

        dados = resposta.json()
        self.assertEqual(dados['materia']['nome'], 'Matemática')
        self.assertEqual(len(dados['assuntos']), 1)

    def test_api_assuntos_materia_inexistente(self):
        """verifica erro 404 quando materia nao existe"""
        resposta = self.client.get('/flashcards/api/assuntos/999/')
        self.assertEqual(resposta.status_code, 404)

    def test_api_flashcards(self):
        """verifica se retorna os flashcards do assunto"""
        resposta = self.client.get(f'/flashcards/api/flashcards/{self.assunto.id}/')
        self.assertEqual(resposta.status_code, 200)

        dados = resposta.json()
        self.assertEqual(dados['assunto']['nome'], 'Funções')
        self.assertEqual(len(dados['flashcards']), 1)

    def test_api_flashcards_sem_cards(self):
        """verifica erro quando nao ha flashcards"""
        assunto_vazio = Assunto.objects.create(
            materia=self.materia,
            nome='Vazio',
            resumo='Sem cards'
        )

        resposta = self.client.get(f'/flashcards/api/flashcards/{assunto_vazio.id}/')
        self.assertEqual(resposta.status_code, 404)

    def test_marcar_estudado(self):
        """verifica se usuario consegue marcar como estudado"""
        resposta = self.client.get(f'/flashcards/marcar-estudado/{self.flashcard.id}/')
        self.assertEqual(resposta.status_code, 200)

        self.assertIn(self.usuario, self.flashcard.usuarios_que_estudaram.all())

    def test_marcar_estudado_inexistente(self):
        """verifica erro ao marcar card inexistente"""
        resposta = self.client.get('/flashcards/marcar-estudado/999/')
        self.assertEqual(resposta.status_code, 404)

    def test_sem_login_redireciona(self):
        """verifica se sem login redireciona"""
        client = Client()
        resposta = client.get('/flashcards/')
        self.assertEqual(resposta.status_code, 302)