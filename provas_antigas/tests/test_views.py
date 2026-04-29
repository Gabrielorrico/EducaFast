from django.test import TestCase, Client
from django.contrib.auth.models import User
from provas_antigas.models import Prova

class ProvasAntigasViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(username='aluno', password='senhaSegura@123!')
        self.client.login(username='aluno', password='senhaSegura@123!')
        self.prova = Prova.objects.create(
            ano=2023,
            edicao="2° DIA",
            tipo="Regular",
            area_conhecimento="Linguagens e Humanas",
            total_questoes=90,
        )

    def test_pagina_carrega(self):
        resposta = self.client.get('/provas/')
        self.assertEqual(resposta.status_code, 200)

    def test_filtro_ano(self):
        resposta = self.client.get('/provas/?ano=2023')
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(all(p.ano == 2023 for p in resposta.context['provas']))

    def test_sem_login_redireciona(self):
        client_sem_login = Client()
        resposta = client_sem_login.get('/provas/')
        self.assertEqual(resposta.status_code, 302)
