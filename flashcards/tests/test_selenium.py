from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os


class FlashcardSeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='aluno',
            password='senha123'
        )

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')

        if os.environ.get("CI"):
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

        self.browser = webdriver.Chrome(options=options)

    def tearDown(self):
        self.browser.quit()

    def test_login_e_acessa_flashcards(self):
        self.browser.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(2)

        self.browser.find_element(By.NAME, 'username').send_keys('aluno')
        self.browser.find_element(By.NAME, 'password').send_keys('senha123')
        self.browser.find_element(By.NAME, 'password').submit()
        time.sleep(2)

        self.browser.get(f'{self.live_server_url}/flashcards/')
        time.sleep(2)

        self.assertIn('/flashcards/', self.browser.current_url)