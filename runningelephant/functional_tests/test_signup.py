from selenium import webdriver
from runningelephant.models import Player, Score, Thoughts
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
from django.test.utils import override_settings
from django.contrib.auth import get_user_model
import time

User = get_user_model()

@override_settings(DEBUG=True)
class TestRegister(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.close()
    
    def test_signup(self):
        # Sign up
        self.browser.get(self.live_server_url + reverse('register'))
        self.browser.find_element_by_id('id_username').send_keys('admin')
        self.browser.find_element_by_id('id_password').send_keys('admin')
        self.browser.find_element_by_id('id_first_name').send_keys('Web')
        self.browser.find_element_by_id('id_last_name').send_keys('Cat')
        self.browser.find_element_by_id('login-submit').click()
        
        begin_url = self.live_server_url + reverse('begin')
        self.assertEquals(
            begin_url,
            self.browser.current_url,
        )