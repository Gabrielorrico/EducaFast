from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


class CronogramaSeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='aluno',
            password='senhaSegura@123!'
        )

        from cronograma.models import Cronograma, Disciplina
        self.disciplina = Disciplina.objects.create(
            nome='Matemática',
            cor_hex='#FF0000',
            area='exatas'
        )
        self.cronograma = Cronograma.objects.create(
            aluno=self.usuario,
            titulo='Cronograma Teste',
            data_inicio='2026-01-01',
            data_fim='2026-12-31',
            ativo=True
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
        time.sleep(1)
        self.browser.quit()

    def _fazer_login(self):
        self.browser.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(2)
        self.browser.find_element(By.NAME, 'username').send_keys('aluno')
        self.browser.find_element(By.NAME, 'password').send_keys('senhaSegura@123!')
        self.browser.find_element(By.NAME, 'password').submit()
        time.sleep(2)

    def test_login_e_acessa_cronograma(self):
        """Usuário logado acessa o cronograma"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/cronograma/')
        time.sleep(2)
        self.assertIn('/cronograma/', self.browser.current_url)

    def test_sem_login_redireciona_para_login(self):
        """Sem login redireciona para tela de login"""
        self.browser.get(f'{self.live_server_url}/cronograma/')
        time.sleep(2)
        self.assertIn('login', self.browser.current_url)

    def test_adicionar_sessao_com_prioridade(self):
        """Usuário adiciona sessão e define prioridade — verifica tag na tela"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/cronograma/')
        time.sleep(2)

        slot_vazio = self.browser.find_element(By.CSS_SELECTOR, '.slot-vazio')
        slot_vazio.click()
        time.sleep(1)

        Select(self.browser.find_element(By.ID, 'selectDisciplina')).select_by_index(0)
        Select(self.browser.find_element(By.ID, 'selectTipo')).select_by_index(0)

        self.browser.find_element(By.ID, 'inputAtividade').send_keys('Simulado ENEM')

        Select(self.browser.find_element(By.ID, 'selectPrioridade')).select_by_value('alta')
        time.sleep(1)

        self.browser.find_element(By.ID, 'btnSalvar').click()
        time.sleep(2)

        tag = self.browser.find_element(By.CSS_SELECTOR, '.tag-prioridade')
        self.assertIn('Alta', tag.text)

    def test_grade_e_slots_visiveis(self):
        """Grade do cronograma e slots estão visíveis e utilizáveis"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/cronograma/')
        time.sleep(2)

        grade = self.browser.find_element(By.CSS_SELECTOR, '.grade-cronograma')
        self.assertTrue(grade.is_displayed())

        slots = self.browser.find_elements(By.CSS_SELECTOR, '.slot-vazio')
        self.assertGreater(len(slots), 0, "Nenhum slot disponível na grade")

    def test_usuario_novo_acessa_cronograma(self):
        """Usuário novo é direcionado para um cronograma gerado automaticamente"""
        User.objects.create_user(username='novo', password='senhaSegura@123!')

        self.browser.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(2)
        self.browser.find_element(By.NAME, 'username').send_keys('novo')
        self.browser.find_element(By.NAME, 'password').send_keys('senhaSegura@123!')
        self.browser.find_element(By.NAME, 'password').submit()
        time.sleep(2)

        self.browser.get(f'{self.live_server_url}/cronograma/')
        time.sleep(2)

        self.assertIn('/cronograma/', self.browser.current_url)

        grade = self.browser.find_element(By.CSS_SELECTOR, '.grade-cronograma')
        self.assertTrue(grade.is_displayed())