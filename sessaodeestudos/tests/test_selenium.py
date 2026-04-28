from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os


class SessaoDeEstudosSeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='aluno',
            password='senhaSegura@123!'
        )

        from sessaodeestudos.models import Materia
        self.materia = Materia.objects.create(
            nome='Matemática',
            icone='📐',
            cor='#4A90D9'
        )

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')

        if os.environ.get("CI"):
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        time.sleep(1)
        self.browser.quit()

    def _fazer_login(self):
        self.browser.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(2)
        self.browser.find_element(By.NAME, 'username').send_keys('aluno')
        self.browser.find_element(By.NAME, 'password').send_keys('senhaSegura@123!')
        self.browser.find_element(By.NAME, 'password').submit()
        time.sleep(2)

    def test_login_e_acessa_sessao_estudos(self):
        """Usuário logado acessa a página do cronômetro"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/estudos/cronometro/')
        time.sleep(2)
        self.assertIn('/estudos/cronometro/', self.browser.current_url)

    def test_sem_login_redireciona_para_login(self):
        """Sem login redireciona para tela de login"""
        self.browser.get(f'{self.live_server_url}/estudos/cronometro/')
        time.sleep(2)
        self.assertIn('login', self.browser.current_url)

    def test_iniciar_e_finalizar_sessao(self):
        """Usuário seleciona matéria, inicia e finaliza sessão normalmente"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/estudos/cronometro/')
        time.sleep(2)

        self.browser.find_element(
            By.CSS_SELECTOR, '[data-materia-nome="Matemática"]'
        ).click()
        time.sleep(1)

        btn_iniciar = self.browser.find_element(By.ID, 'btn-iniciar')
        self.assertFalse(btn_iniciar.get_attribute('disabled'))
        btn_iniciar.click()
        time.sleep(1)

        status = self.browser.find_element(By.ID, 'status-cronometro')
        self.assertIn('estudando', status.text.lower())

        btn_parar = self.browser.find_element(By.ID, 'btn-parar')
        self.assertFalse(btn_parar.get_attribute('hidden'))
        btn_parar.click()
        time.sleep(2)

        feedback = self.browser.find_element(By.ID, 'feedback-sessao')
        self.assertTrue(feedback.is_displayed())

    def test_iniciar_sem_materia_nao_permite(self):
        """Sem selecionar matéria o botão iniciar permanece desabilitado"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/estudos/cronometro/')
        time.sleep(2)

        btn_iniciar = self.browser.find_element(By.ID, 'btn-iniciar')
        self.assertIsNotNone(btn_iniciar.get_attribute('disabled'))

        status = self.browser.find_element(By.ID, 'status-cronometro')
        self.assertIn('aguardando', status.text.lower())

    def test_sem_sessoes_exibe_aviso(self):
        """Usuário sem sessões registradas vê aviso na lista"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/estudos/cronometro/')
        time.sleep(2)

        aviso = self.browser.find_element(By.ID, 'aviso-sem-sessoes')
        self.assertTrue(aviso.is_displayed())
        self.assertIn('nenhuma sessão registrada', aviso.text.lower())