from django.test import TestCase, Client, LiveServerTestCase
from django.contrib.auth.models import User
from provas_antigas.models import Prova
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class ProvasAntigasViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(username='aluno', password='senha123')
        self.client.login(username='aluno', password='senha123')
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


class ProvasAntigasSeleniumTest(LiveServerTestCase):
    """Testes com navegador real — abrem o Chrome e simulam o usuário."""

    def setUp(self):
        """Cria usuário, prova e abre o Chrome antes de cada teste."""
        self.usuario = User.objects.create_user(
            username='aluno',
            password='senha123'
        )
        self.prova = Prova.objects.create(
            ano=2023,
            edicao="2° DIA",
            tipo="Regular",
            area_conhecimento="Linguagens e Humanas",
            total_questoes=90,
        )

        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        time.sleep(2)
        self.browser.quit()

    def _fazer_login(self):
        self.browser.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(2)

        self.browser.find_element(By.NAME, 'username').send_keys('aluno')
        time.sleep(1)

        self.browser.find_element(By.NAME, 'password').send_keys('senha123')
        time.sleep(1)

        self.browser.find_element(By.NAME, 'password').submit()
        time.sleep(2)

    def test_lista_provas_carrega(self):
        self._fazer_login()

        self.browser.get(f'{self.live_server_url}/provas/')
        time.sleep(2)

        self.assertIn('/provas/', self.browser.current_url)

    def test_filtro_por_ano(self):
        self._fazer_login()

        self.browser.get(f'{self.live_server_url}/provas/?ano=2023')
        time.sleep(2)

        self.assertIn('2023', self.browser.page_source)

    def test_detalhe_prova(self):
        self._fazer_login()

        self.browser.get(f'{self.live_server_url}/provas/{self.prova.pk}/')
        time.sleep(2)

        self.assertIn('/provas/', self.browser.current_url)

    def test_sem_login_redireciona(self):
        self.browser.get(f'{self.live_server_url}/provas/')
        time.sleep(2)

        self.assertIn('login', self.browser.current_url)