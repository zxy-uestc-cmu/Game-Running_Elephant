from selenium import webdriver
from runningelephant.models import Player, Score, Thoughts
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
from django.test.utils import override_settings
from django.contrib.auth import get_user_model
from friendship.models import Friend, Follow, Block, FriendshipRequest
import time

User = get_user_model()

@override_settings(DEBUG=True)
class TestAddFriend(LiveServerTestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username = 'changhay',
            first_name = 'Changhao',
            last_name = 'Yang'
        )
        self.user1.set_password('changhay')
        self.user1.save()
        self.player1 = Player.objects.create(
            user = self.user1
        )

        self.user2 = User.objects.create(
            username = 'zhaoxinyan',
            first_name = 'Xinyan',
            last_name = 'Zhao'
        )
        self.user2.set_password('zhaoxinyan')
        self.user2.save()
        self.player2 = Player.objects.create(
            user = self.user2
        )

        FriendshipRequest.objects.create(
            from_user = self.user2,
            to_user = self.user1
        )

        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.close()
    
    def test_add_friend(self):
        # Login
        self.browser.get(self.live_server_url + reverse('profile'))
        self.browser.find_element_by_id('id_username').send_keys('changhay')
        self.browser.find_element_by_id('id_password').send_keys('changhay')
        self.browser.find_element_by_id('login-submit').click()
        time.sleep(2)
        
        # Accept
        self.browser.find_element_by_id('zhaoxinyan-message-tab').click()
        time.sleep(2)
        
        self.browser.find_element_by_class_name('accept').click()

        name = self.browser.find_elements_by_id('friend-name')[0].text
        
        self.assertEquals(name, self.user2.username)