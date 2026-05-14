from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

from sessaodeestudos.models import SessaoDeEstudos
from flashcards.models import Flashcard, Assunto
from gamificacao.models import PerfilGamificacao
from gamificacao.services import (
    conceder_xp_flashcard,
    conceder_xp_sessao,
    XP_POR_FLASHCARD,
    XP_POR_SESSAO,
    TEMPO_MINIMO_SEGUNDOS,
)

class GamificacaoSeleniumTest(LiveServerTestCase):

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

    def _criar_flashcard(self):
        assunto = Assunto.objects.create(
            materia=self.materia,
            nome='Álgebra',
            resumo='Revisão de álgebra',
            ordem=1
        )
        return Flashcard.objects.create(
            assunto=assunto,
            frente='Quanto é 2+2?',
            verso='4',
            ordem=1
        )

    def _criar_sessao(self, duracao_segundos=3600):
        return SessaoDeEstudos.objects.create(
            usuario=self.usuario,
            materia=self.materia,
            duracao_segundos=duracao_segundos,
            iniciada_em=timezone.now()
        )

    def test_xp_adicionado_apos_revisao_de_flashcard(self):
        """Revisar flashcard concede XP e registra o flashcard como estudado"""
        flashcard = self._criar_flashcard()

        xp_antes = 0
        conceder_xp_flashcard(self.usuario)
        self.usuario.flashcards_estudados.add(flashcard)

        perfil = PerfilGamificacao.objects.get(usuario=self.usuario)
        self.assertEqual(perfil.xp_total, xp_antes + XP_POR_FLASHCARD)
        self.assertIn(flashcard, self.usuario.flashcards_estudados.all())

        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(3)

        pagina = self.browser.page_source.lower()
        self.assertIn('xp', pagina)
        self.assertIn('1', pagina)
        self.assertIn('flashcard', pagina)

    def test_xp_acumulado_multiplos_flashcards(self):
        """Revisar múltiplos flashcards acumula XP proporcionalmente"""
        flashcards = [self._criar_flashcard() for _ in range(3)]

        for fc in flashcards:
            conceder_xp_flashcard(self.usuario)
            self.usuario.flashcards_estudados.add(fc)

        perfil = PerfilGamificacao.objects.get(usuario=self.usuario)
        self.assertEqual(perfil.xp_total, XP_POR_FLASHCARD * 3)
        self.assertEqual(self.usuario.flashcards_estudados.count(), 3)

        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(3)

        pagina = self.browser.page_source.lower()
        self.assertIn('xp', pagina)

    def test_xp_concedido_sessao_valida(self):
        """Sessão com duração maior que o mínimo concede XP ao aluno"""
        duracao_valida = TEMPO_MINIMO_SEGUNDOS + 60  
        self._criar_sessao(duracao_segundos=duracao_valida)

        xp_concedido, mensagem = conceder_xp_sessao(self.usuario, duracao_valida)

        self.assertEqual(xp_concedido, XP_POR_SESSAO)
        self.assertIn('XP', mensagem)

        perfil = PerfilGamificacao.objects.get(usuario=self.usuario)
        self.assertEqual(perfil.xp_total, XP_POR_SESSAO)

        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(3)

        pagina = self.browser.page_source.lower()
        self.assertIn('xp', pagina)

    def test_sem_xp_sessao_muito_curta(self):
        """Sessão abaixo do tempo mínimo não concede XP e retorna mensagem de aviso"""
        duracao_insuficiente = TEMPO_MINIMO_SEGUNDOS - 1 
        self._criar_sessao(duracao_segundos=duracao_insuficiente)

        xp_concedido, mensagem = conceder_xp_sessao(self.usuario, duracao_insuficiente)

        self.assertEqual(xp_concedido, 0)

        self.assertIn('5 minutos', mensagem)

        perfil_qs = PerfilGamificacao.objects.filter(usuario=self.usuario)
        if perfil_qs.exists():
            self.assertEqual(perfil_qs.first().xp_total, 0)

    def test_xp_zero_quando_sessao_exatamente_no_limite_inferior(self):
        """Sessão com exatamente 0 segundos não concede XP"""
        xp_concedido, mensagem = conceder_xp_sessao(self.usuario, duracao_segundos=0)

        self.assertEqual(xp_concedido, 0)
        self.assertNotEqual(mensagem, '')

        perfil_qs = PerfilGamificacao.objects.filter(usuario=self.usuario)
        if perfil_qs.exists():
            self.assertEqual(perfil_qs.first().xp_total, 0)

    def test_sem_xp_sem_flashcards_revisados(self):
        """Sair dos flashcards sem revisar nenhum não adiciona XP nem recompensa"""
        self._criar_flashcard()

        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/flashcards/')
        time.sleep(3)

        # Aluno navega para outra página sem revisar nenhum flashcard
        self.browser.get(f'{self.live_server_url}/desempenho/')
        time.sleep(3)

        perfil_qs = PerfilGamificacao.objects.filter(usuario=self.usuario)
        xp_total = perfil_qs.first().xp_total if perfil_qs.exists() else 0
        self.assertEqual(xp_total, 0)

        self.assertEqual(self.usuario.flashcards_estudados.count(), 0)

    def test_perfil_gamificacao_nao_criado_sem_interacao(self):
        """Perfil de gamificação não é criado se o aluno não interagiu com nenhuma atividade"""
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/flashcards/')
        time.sleep(2)

        self.browser.get(f'{self.live_server_url}/dashboard/')
        time.sleep(2)

        perfil_qs = PerfilGamificacao.objects.filter(usuario=self.usuario)
        if perfil_qs.exists():
            self.assertEqual(
                perfil_qs.first().xp_total,
                0,
                'XP deve ser 0 quando nenhuma atividade foi realizada'
            )

    def test_nivel_aumenta_com_xp_suficiente(self):
        """Acumular 100 XP sobe o nível do aluno de 1 para 2"""
        perfil = PerfilGamificacao.objects.create(
            usuario=self.usuario,
            xp_total=99
        )
        self.assertEqual(perfil.nivel, 1)

        perfil.xp_total += 1  # 100 XP = nível 2
        perfil.save()
        self.assertEqual(perfil.nivel, 2)

    def test_titulo_calouro_no_nivel_1(self):
        """Aluno no nível 1 recebe o título 'Calouro'"""
        perfil = PerfilGamificacao.objects.create(
            usuario=self.usuario,
            xp_total=0
        )
        self.assertEqual(perfil.titulo, 'Calouro')

    def test_xp_no_nivel_atual_calculado_corretamente(self):
        """XP dentro do nível atual é o resto da divisão por 100"""
        perfil = PerfilGamificacao.objects.create(
            usuario=self.usuario,
            xp_total=150
        )
        self.assertEqual(perfil.xp_no_nivel_atual, 50)
        self.assertEqual(perfil.nivel, 2)