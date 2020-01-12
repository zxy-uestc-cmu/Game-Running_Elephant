from selenium import webdriver
from runningelephant.models import Player, Score, Thoughts
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
from django.test.utils import override_settings
from django.contrib.auth import get_user_model
import time

User = get_user_model()

@override_settings(DEBUG=True)
class TestLogout(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(
            username = 'admin',
            first_name = 'Admin',
            last_name = 'CMU'
        )
        self.user.set_password('admin')
        self.user.save()
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.close()
    
    def test_logout(self):
        # Login
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_id('id_username').send_keys('admin')
        self.browser.find_element_by_id('id_password').send_keys('admin')
        self.browser.find_element_by_id('login-submit').click()
        time.sleep(1)

        # logout
        self.browser.find_element_by_id('logout').click()
        
        hello_url = self.live_server_url + reverse('hello')
        self.assertEquals(
            hello_url,
            self.browser.current_url,
        )