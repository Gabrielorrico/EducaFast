from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from assuntos_recorrentes.models import Materia, Topico
import time
import os


class AssuntosRecorrentesSeleniumTest(LiveServerTestCase):

    def setUp(self):
        """Cria usuário, dados no banco e inicia navegador"""
        self.usuario = User.objects.create_user(
            username='aluno',
            password='senhaSegura@123!'
        )

        self.materia = Materia.objects.create(
            nome='Matemática',
            icone='📐',
            classe_css='mat-matematica',
            ordem=1
        )
        self.topico = Topico.objects.create(
            nome='Funções',
            materia=self.materia,
            ordem=1
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

    def _fazer_login(self):
        """Helper: realiza login com o usuário de teste"""
        self.browser.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(2)

        self.browser.find_element(By.NAME, 'username').send_keys('aluno')
        time.sleep(1)

        self.browser.find_element(By.NAME, 'password').send_keys('senhaSegura@123!')
        time.sleep(1)

        self.browser.find_element(By.NAME, 'password').submit()
        time.sleep(2)

    def _acessar_pagina(self):
        """Helper: acessa a página de assuntos recorrentes"""
        self.browser.get(f'{self.live_server_url}/assuntos_recorrentes/')
        time.sleep(2)

    def _expandir_primeira_materia(self):
        """Helper: expande a primeira matéria para exibir os tópicos"""
        primeira_materia = self.browser.find_element(By.CSS_SELECTOR, '.materia-card')
        primeira_materia.click()
        time.sleep(1)

    def test_logado_seleciona_area_ve_temas_com_porcentagem(self):
        """
        Dado que o aluno está logado,
        quando ele seleciona uma área específica e um ano disponível,
        então os temas recorrentes aparecem com a porcentagem de aparição.
        """
        self._fazer_login()
        self._acessar_pagina()

        corpo = self.browser.find_element(By.CSS_SELECTOR, '.fluxo-lista')
        self.assertIn(
            'Matemática',
            corpo.text,
            "A matéria cadastrada deve aparecer na página"
        )

        self._expandir_primeira_materia()

        topico_visivel = self.browser.find_element(
            By.CSS_SELECTOR, f'[data-id="{self.topico.id}"]'
        )
        self.assertTrue(
            topico_visivel.is_displayed(),
            "O tópico cadastrado deve aparecer ao selecionar a área"
        )

        btn_ano = self.browser.find_element(By.CSS_SELECTOR, '[data-ano="2022"]')
        btn_ano.click()
        time.sleep(1)

        badges = self.browser.find_elements(
            By.CSS_SELECTOR, '.pct-badge[style*="inline-block"]'
        )
        self.assertGreater(
            len(badges), 0,
            "Os temas recorrentes devem exibir a porcentagem de aparição no ENEM"
        )

        texto = badges[0].text.strip()
        self.assertTrue(
            texto.endswith('%'),
            f"A porcentagem deve terminar com '%', mas exibiu: '{texto}'"
        )

    def test_edicao_recente_sem_dados_nao_exibe_informacoes(self):
        """
        Dado que o aluno está logado e seleciona o ano mais recente,
        quando os dados ainda não foram processados,
        então o sistema não exibe nenhuma informação de porcentagem.
        """

        self._fazer_login()
        self._acessar_pagina()
        self._expandir_primeira_materia()

        btn_2025 = self.browser.find_element(By.CSS_SELECTOR, '[data-ano="2025"]')
        btn_2025.click()
        time.sleep(1)

        badges = self.browser.find_elements(
            By.CSS_SELECTOR, '.pct-badge[style*="inline-block"]'
        )
        self.assertEqual(
            len(badges), 0,
            "O sistema não deve exibir informações quando os dados não foram processados"
        )

        mensagem = self.browser.find_element(By.ID, 'filtro-erro')
        self.assertTrue(
            mensagem.is_displayed(),
            "O sistema deve informar que os dados ainda não estão disponíveis"
        )
        self.assertIn(
            '2025',
            mensagem.text,
            "A mensagem deve indicar o ano cujos dados não estão disponíveis"
        )

    def test_nao_logado_redireciona_para_login(self):
        """
        Dado que o aluno não está logado,
        quando tenta acessar os assuntos recorrentes,
        então o sistema redireciona para a tela de login.
        """
        self._acessar_pagina()
        self.assertIn(
            'login',
            self.browser.current_url,
            "O sistema deve redirecionar para o login quando o aluno não está autenticado"
        )