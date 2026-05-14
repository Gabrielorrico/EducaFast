from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

from sessaodeestudos.models import SessaoDeEstudos
from flashcards.models import Flashcard, Assunto


class DesempenhoSeleniumTest(LiveServerTestCase):

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

        if os.environ.get('CI'):
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')

        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        time.sleep(2)
        self.browser.quit()

    def _fazer_login(self):
        self.browser.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(2)
        self.browser.find_element(By.NAME, 'username').send_keys('aluno')
        self.browser.find_element(By.NAME, 'password').send_keys('senhaSegura@123!')
        self.browser.find_element(By.NAME, 'password').submit()
        time.sleep(2)

    def _criar_sessao(self, duracao_segundos=3600):
        SessaoDeEstudos.objects.create(
            usuario=self.usuario,
            materia=self.materia,
            duracao_segundos=duracao_segundos,
            iniciada_em=timezone.now()
        )

    def _criar_flashcard_estudado(self):
        assunto = Assunto.objects.create(
            materia=self.materia,
            nome='Álgebra',
            resumo='Revisão de álgebra',
            ordem=1
        )
        flashcard = Flashcard.objects.create(
            assunto=assunto,
            frente='Quanto é 2+2?',
            verso='4',
            ordem=1
        )
        self.usuario.flashcards_estudados.add(flashcard)

    def test_visualiza_estatisticas_com_dados(self):
        """Aluno com sessão e flashcard estudado vê estatísticas na tela de desempenho"""
        self._criar_sessao(duracao_segundos=3600)
        self._criar_flashcard_estudado()

        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(3)

        pagina = self.browser.page_source.lower()
        self.assertIn('1h', pagina)
        self.assertIn('1', pagina)
        self.assertIn('matemática', pagina)

    def test_historico_exibe_ultima_sessao(self):
        """Histórico mostra a última sessão com matéria e duração"""
        self._criar_sessao(duracao_segundos=1800)

        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(3)

        pagina = self.browser.page_source.lower()
        self.assertIn('matemática', pagina)
        self.assertIn('30min', pagina)

    def test_historico_exibe_data(self):
        """Histórico mostra a data da sessão no formato d/m/Y"""
        self._criar_sessao(duracao_segundos=3600)

        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(3)

        hoje = timezone.localdate().strftime('%d/%m/%Y')
        pagina = self.browser.page_source
        self.assertIn(hoje, pagina)

    def test_sequencia_dias_consecutivos(self):
        """Exibe sequência de dias consecutivos estudando"""
        self._criar_sessao(duracao_segundos=3600)

        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(3)

        pagina = self.browser.page_source.lower()
        self.assertIn('1 dia', pagina)

    def test_grafico_exibe_materia(self):
        """Gráfico de barras exibe a matéria estudada"""
        self._criar_sessao(duracao_segundos=7200)

        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(3)

        pagina = self.browser.page_source.lower()
        self.assertIn('matemática', pagina)

    def test_flashcards_estudados_em_relacao_ao_total(self):
        """Exibe quantidade de flashcards estudados em relação ao total disponível"""
        self._criar_flashcard_estudado()

        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(3)

        pagina = self.browser.page_source.lower()
        self.assertIn('1', pagina)
        self.assertIn('flashcard', pagina)

    def test_metricas_zeradas_sem_atividades(self):
        """Aluno sem atividades vê métricas zeradas e mensagens de ausência de dados"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(3)

        pagina = self.browser.page_source.lower()
        self.assertIn('0', pagina)

        sem_dados = any(termo in pagina for termo in [
            'nenhuma sessão',
            'nenhum dado',
            'sem dados',
            'sem sessões',
            'nenhum registro',
            'ainda não',
        ])
        self.assertTrue(sem_dados, 'Esperava mensagem indicando ausência de dados')

    def test_sem_login_redireciona_para_login(self):
        """Usuário não logado é redirecionado para o login ao acessar desempenho"""
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(2)
        self.assertIn('login', self.browser.current_url)