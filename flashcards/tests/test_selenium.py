from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


class FlashcardSeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='aluno',
            password='senhaSegura@123!'
        )

        from sessaodeestudos.models import Materia
        from flashcards.models import Assunto, Flashcard

        self.materia = Materia.objects.create(
            nome='Matemática',
            icone='📐',
            cor='#4A90D9'
        )
        self.assunto = Assunto.objects.create(
            materia=self.materia,
            nome='Equações do 2º grau',
            resumo='Revisão de equações',
            ordem=1
        )
        self.flashcard = Flashcard.objects.create(
            assunto=self.assunto,
            frente='O que é Bhaskara?',
            verso='Fórmula para resolver equações do 2º grau: x = (-b ± √Δ) / 2a',
            ordem=1
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

    def test_login_e_acessa_flashcards(self):
        """Usuário logado acessa a página de flashcards"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/flashcards/')
        time.sleep(2)
        self.assertIn('/flashcards/', self.browser.current_url)

    def test_seleciona_materia_e_exibe_flashcard(self):
        """Usuário clica na matéria, seleciona assunto — flashcard com resumo aparece"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/flashcards/')
        time.sleep(2)

        self.browser.find_element(
            By.CSS_SELECTOR, '[data-materia-nome="Matemática"]'
        ).click()
        time.sleep(2)

        self.browser.find_element(By.CSS_SELECTOR, '.card-assunto').click()
        time.sleep(2)

        secao = self.browser.find_element(By.ID, 'secao-flashcards')
        self.assertTrue(secao.is_displayed())

        frente = self.browser.find_element(By.ID, 'texto-frente')
        self.assertTrue(frente.is_displayed())

        resumo = self.browser.find_element(By.CSS_SELECTOR, '.resumo-texto')
        self.assertIn('Revisão de equações', resumo.text)

    def test_sem_materia_exibe_aviso(self):
        """Sem selecionar matéria, flashcard não aparece e aviso é exibido"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/flashcards/')
        time.sleep(2)

        aviso = self.browser.find_element(By.ID, 'aviso-selecione-materia')
        self.assertTrue(aviso.is_displayed())
        self.assertIn('selecione uma matéria', aviso.text.lower())

        flashcards = self.browser.find_elements(By.CSS_SELECTOR, '.flashcard')
        self.assertEqual(len(flashcards), 0)

    def test_assunto_inexistente_exibe_mensagem(self):
        """Matéria sem assuntos cadastrados exibe mensagem de não encontrado"""
        from sessaodeestudos.models import Materia
        Materia.objects.create(
            nome='Filosofia',
            icone='🧠',
            cor='#999999'
        )

        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/flashcards/')
        time.sleep(2)

        btn_materia = self.browser.find_element(
            By.CSS_SELECTOR, '[data-materia-nome="Filosofia"]'
        )
        btn_materia.click()
        time.sleep(2)

        mensagem = self.browser.find_element(By.CSS_SELECTOR, '.aviso-estado')
        self.assertIn('ainda não há assuntos cadastrados', mensagem.text.lower())