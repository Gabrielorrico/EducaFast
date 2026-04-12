from django.test import TestCase, Client
from django.contrib.auth.models import User
from datetime import date
from cronograma.models import Cronograma, Disciplina, SessaoEstudo
import json


class CronogramaViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(username='aluno', password='senha123')
        self.client.login(username='aluno', password='senha123')
        self.disciplina = Disciplina.objects.create(nome='Química', area='exatas')
        self.cronograma = Cronograma.objects.create(
            aluno=self.usuario,
            titulo='Cronograma',
            data_inicio=date.today(),
            data_fim=date(2025, 12, 31),
            ativo=True
        )

    def test_pagina_carrega(self):
        resposta = self.client.get(f'/cronograma/{self.cronograma.id}/')
        self.assertEqual(resposta.status_code, 200)

    def test_criar_sessao(self):
        resposta = self.client.post(
            f'/cronograma/{self.cronograma.id}/sessao/criar/',
            data=json.dumps({
                'dia_semana': 0,
                'slot_horario': 0,
                'disciplina_id': self.disciplina.id,
                'tipo': 'exercicio',
                'descricao_atividade': 'Lista 01'
            }),
            content_type='application/json'
        )
        self.assertEqual(resposta.status_code, 201)

    def test_nao_cria_sessao_duplicada(self):
        SessaoEstudo.objects.create(
            cronograma=self.cronograma,
            disciplina=self.disciplina,
            dia_semana=0,
            slot_horario=0,
            tipo='exercicio'
        )
        resposta = self.client.post(
            f'/cronograma/{self.cronograma.id}/sessao/criar/',
            data=json.dumps({
                'dia_semana': 0,
                'slot_horario': 0,
                'disciplina_id': self.disciplina.id,
                'tipo': 'revisao',
            }),
            content_type='application/json'
        )
        self.assertEqual(resposta.status_code, 409)

    def test_deletar_sessao(self):
        sessao = SessaoEstudo.objects.create(
            cronograma=self.cronograma,
            disciplina=self.disciplina,
            dia_semana=1,
            slot_horario=1,
            tipo='revisao'
        )
        resposta = self.client.delete(f'/cronograma/sessao/{sessao.id}/deletar/')
        self.assertEqual(resposta.status_code, 200)

    def test_sem_login_redireciona(self):
        client_sem_login = Client()
        resposta = client_sem_login.get(f'/cronograma/{self.cronograma.id}/')
        self.assertEqual(resposta.status_code, 302)