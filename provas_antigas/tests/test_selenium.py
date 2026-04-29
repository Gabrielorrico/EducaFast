from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from provas_antigas.models import Prova
import time
import os


class ProvasAntigasSeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='aluno',
            password='senhaSegura@123!'
        )

        # Prova que deve aparecer no filtro
        self.prova_2023 = Prova.objects.create(
            ano=2023,
            edicao='1º Dia',
            tipo='Regular',
            area_conhecimento='Matemática',
            total_questoes=45,
        )

        # Prova de outro ano — não deve aparecer no filtro por 2023
        self.prova_2022 = Prova.objects.create(
            ano=2022,
            edicao='2º Dia',
            tipo='Regular',
            area_conhecimento='Linguagens',
            total_questoes=45,
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

    def test_login_e_acessa_provas(self):
        """Usuário logado acessa a aba de provas antigas"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/provas/')
        time.sleep(2)
        self.assertIn('/provas/', self.browser.current_url)

    def test_sem_login_redireciona_para_login(self):
        """Sem login redireciona para tela de login"""
        self.browser.get(f'{self.live_server_url}/provas/')
        time.sleep(2)
        self.assertIn('login', self.browser.current_url)

    def test_busca_prova_inexistente_exibe_mensagem(self):
        """Filtro por ano inexistente exibe mensagem de nenhuma prova encontrada"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/provas/?ano=1800')
        time.sleep(2)

        mensagem = self.browser.find_element(By.CSS_SELECTOR, '.sem-resultado')
        self.assertIn('Nenhuma prova encontrada', mensagem.text)

    def test_filtro_por_ano_exibe_apenas_prova_correta(self):
        """Filtro por 2023 exibe prova de 2023 e não exibe prova de 2022"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/provas/?ano=2023')
        time.sleep(2)

        # 2023 deve aparecer
        self.assertIn('2023', self.browser.page_source)

        # 2022 não deve aparecer nos resultados
        cards = self.browser.find_elements(By.CSS_SELECTOR, '.card-info')
        textos = [card.text for card in cards]
        self.assertTrue(
            any('2023' in texto for texto in textos),
            "Prova de 2023 não apareceu nos resultados"
        )
        self.assertFalse(
            any('2022' in texto for texto in textos),
            "Prova de 2022 apareceu indevidamente no filtro de 2023"
        )