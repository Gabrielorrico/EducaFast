from django.test import TestCase, Client
from django.contrib.auth.models import User

class DashboardViewTest(TestCase):

    def setUp(self):
        """Cria usuário logado antes"""
        self.client = Client()
        self.usuario = User.objects.create_user(username='aluno', password='senha123')
        self.client.login(username='aluno', password='senha123')

    def test_dashboard_carrega(self):
        """verifica se o dashboard carrega com sucesso para usuario logado"""
        resposta = self.client.get('/dashboard/')
        self.assertEqual(resposta.status_code, 200)


    def test_sem_login_redireciona(self):
        """Verifica se usuário sem login é redirecionado para o login."""
        client_sem_login = Client()
        resposta = client_sem_login.get('/dashboard/')
        self.assertEqual(resposta.status_code, 302)
