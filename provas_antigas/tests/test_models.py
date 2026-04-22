from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from provas_antigas.models import Prova
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class ProvaModelTest(TestCase):

    def setUp(self):
        """Cria a prova falsa antes de cada teste."""
        self.prova = Prova.objects.create(
            ano=2023,
            edicao='1º Dia',
            tipo='Regular',
            area_conhecimento='Matemática',
            total_questoes=45,
        )

    def test_criar_prova(self):
        """verifica se a prova foi criada corretamente no banc"""
        self.assertEqual(self.prova.ano, 2023)

    def test_str_prova(self):
        """verifica se o __str__ retorna o formato correto"""
        self.assertEqual(str(self.prova), 'ENEM 2023 — 1º Dia (Regular)')

    def test_prova_sem_pdf(self):
        """verifica se uma prova pode ser criada sem PDF"""
        self.assertIsNone(self.prova.pdf_url)


class ProvasAntigasSeleniumTest(LiveServerTestCase):

    def setUp(self):
        """cria usario, prova e abre o chrome antes de cada teste"""
        self.usuario = User.objects.create_user(
            username='aluno',
            password='senha123'
        )
        self.prova = Prova.objects.create(
            ano=2022,
            edicao='2º Dia',
            tipo='Regular',
            area_conhecimento='Linguagens',
            total_questoes=45,
        )

        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')

        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        """fecha o Chrome depois de cada teste."""
        time.sleep(2)
        self.browser.quit()

    def _fazer_login(self):
        """metodo auxiliar que faz login reutilizado nos testes."""
        self.browser.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(2)

        self.browser.find_element(By.NAME, 'username').send_keys('aluno')
        time.sleep(1)

        self.browser.find_element(By.NAME, 'password').send_keys('senha123')
        time.sleep(1)

        self.browser.find_element(By.NAME, 'password').submit()
        time.sleep(2)

    def test_lista_provas_carrega(self):
        """faz login e verifica se a pag de provas carrega"""
        self._fazer_login()

        self.browser.get(f'{self.live_server_url}/provas/')
        
        time.sleep(2)

        self.assertIn('/provas/', self.browser.current_url)
        

    def test_filtro_por_ano(self):
        """faz login e filtra por ano de provba"""
        self._fazer_login()

        self.browser.get(f'{self.live_server_url}/provas/?ano=2022')
       
        time.sleep(2)

        self.assertIn('2022', self.browser.page_source)        

    def test_sem_login_redireciona(self):
        """tenta acessar provas sem login e verifica redirecionamento."""
        self.browser.get(f'{self.live_server_url}/provas/')
        
        time.sleep(2)

        self.assertIn('login', self.browser.current_url)
   