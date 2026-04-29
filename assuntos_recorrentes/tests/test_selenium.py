from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from assuntos_recorrentes.models import Materia, Topico
import time
import os


class AssuntosRecorrentesSeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='aluno',
            password='senhaSegura@123!'
        )

        self.materia = Materia.objects.create(
            nome='Matemática',
            icone='📐',
            ordem=1
        )
        Topico.objects.create(materia=self.materia, nome='Funções', ordem=1)
        Topico.objects.create(materia=self.materia, nome='Geometria', ordem=2)

        self.materia_vazia = Materia.objects.create(
            nome='Redação',
            icone='✍️',
            ordem=2
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

    def test_sem_login_redireciona_para_login(self):
        """Sem login redireciona para tela de login"""
        self.browser.get(f'{self.live_server_url}/assuntos_recorrentes/')
        time.sleep(2)
        self.assertIn('login', self.browser.current_url)

    def test_seleciona_materia_com_topicos_e_exibe(self):
        """Usuário seleciona matéria com tópicos e os vê na tela"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/assuntos_recorrentes/')
        time.sleep(2)

        self.browser.find_element(
            By.XPATH, "//*[contains(text(), 'Matemática')]"
        ).click()
        time.sleep(2)

        aberto = self.browser.find_elements(By.CSS_SELECTOR, '.fluxo-item.aberto')
        self.assertGreater(len(aberto), 0, "Nenhuma matéria foi aberta")

        page = self.browser.page_source
        self.assertIn('Funções', page)
        self.assertIn('Geometria', page)

    def test_seleciona_materia_sem_topicos_nao_exibe_conteudo(self):
        """Matéria sem tópicos não exibe nenhum tópico na seção aberta"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/assuntos_recorrentes/')
        time.sleep(2)

        self.browser.find_element(
            By.XPATH, "//*[contains(text(), 'Redação')]"
        ).click()
        time.sleep(2)

        # Pega apenas o fluxo-item aberto (Redação)
        item_aberto = self.browser.find_element(By.CSS_SELECTOR, '.fluxo-item.aberto')

        # Não deve ter nenhum topico-card dentro do item aberto
        topicos = item_aberto.find_elements(By.CSS_SELECTOR, '.topico-card')
        self.assertEqual(len(topicos), 0, "Tópicos apareceram indevidamente na Redação")

        # Deve exibir a mensagem de sem tópicos
        mensagem = item_aberto.find_element(By.CSS_SELECTOR, '.sem-topicos')
        self.assertIn('nenhum tópico', mensagem.text.lower())