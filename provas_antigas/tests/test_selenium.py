from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


class ProvasAntigasSeleniumTest(LiveServerTestCase):

    def setUp(self):
        """Cria usuário e inicia navegador"""
        self.usuario = User.objects.create_user(
            username='aluno',
            password='senhaSegura@123!'
        )

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')

        if os.environ.get("CI"):
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

        self.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def tearDown(self):
        """Fecha navegador"""
        time.sleep(1)
        self.browser.quit()

    def test_login_e_acessa_provas(self):
        """faz login e acessa a página de provas"""


        self.browser.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(2)

        self.browser.find_element(By.NAME, 'username').send_keys('aluno')
        time.sleep(1)

        self.browser.find_element(By.NAME, 'password').send_keys('senhaSegura@123!')
        time.sleep(1)

        self.browser.find_element(By.NAME, 'password').submit()
        time.sleep(2)


        self.browser.get(f'{self.live_server_url}/provas/')
        time.sleep(2)

        self.assertIn('/provas/', self.browser.current_url)

    def test_sem_login_redireciona_para_login(self):
        """tenta acessar provas sem login"""

        self.browser.get(f'{self.live_server_url}/provas/')
        time.sleep(2)

        self.assertIn('login', self.browser.current_url)