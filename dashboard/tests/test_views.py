from django.test import TestCase, Client, LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


class DashboardViewTest(TestCase):

    def setUp(self):
        """Cria usuário logado antes"""
        self.client = Client()
        self.usuario = User.objects.create_user(username='aluno', password='senha123')
        self.client.login(username='aluno', password='senha123')

    def test_dashboard_carrega(self):
        """verifica se o dashboard carrega com sucesso para usuario logado"""
        resposta = self.client.get('/dashboard/')
        self.assertEqual(resposta.status_code, 200)


    def test_sem_login_redireciona(self):
        """Verifica se usuário sem login é redirecionado para o login."""
        client_sem_login = Client()
        resposta = client_sem_login.get('/dashboard/')
        self.assertEqual(resposta.status_code, 302)


class DashboardSeleniumTest(LiveServerTestCase):
    

    def setUp(self):
        """cria o usuario e abre o chrome antes de cada teste"""
        self.usuario = User.objects.create_user(
            username='aluno',
            password='senha123'
        )

        options = webdriver.ChromeOptions()

        options.add_argument('--start-maximized')

        self.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def tearDown(self):
        """fecha o chrome depois de cada test"""
        time.sleep(2)

        self.browser.quit()

    def test_login_e_acessa_dashboard(self):
        """abre o chrome, faz login e acessa o dashboard"""

        self.browser.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(2)

        campo_usuario = self.browser.find_element(By.NAME, 'username')

        campo_usuario.send_keys('aluno')
        time.sleep(1)

        campo_senha = self.browser.find_element(By.NAME, 'password')

        campo_senha.send_keys('senha123')
        time.sleep(1)

        campo_senha.submit()
        time.sleep(2)

        self.assertIn('/dashboard/', self.browser.current_url)

    def test_sem_login_redireciona_para_login(self):
        """tenta acessar o dashboard sem login e verifica o redirecionamento."""

        self.browser.get(f'{self.live_server_url}/dashboard/')
        time.sleep(2)

        self.assertIn('login', self.browser.current_url)