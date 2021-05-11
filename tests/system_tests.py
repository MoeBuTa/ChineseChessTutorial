import unittest, os, time
from app import create_app, db
from tests import data
from selenium import webdriver
from config import TestingConfig
from flask_testing import LiveServerTestCase
from urllib.request import urlopen

basedir = os.path.abspath(os.path.dirname(__file__))


class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=os.path.join(basedir, 'chromedriver.exe'))
        if not self.driver:
            self.skipTest('Web browser not available')
        else:
            self.app = create_app(TestingConfig)
            self.app_context = self.app.app_context()
            self.app_context.push()
            db.create_all()
            data.add_data()
            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')

    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.remove()
            db.drop_all()
            db.session.remove()
            self.app_context.pop()

    # def test_server_is_up_and_running(self):
    #     response = urlopen(self.get_server_url())
    #     self.assertEqual(response.code, 200)

    def test_register_login(self):
        # test register
        self.driver.get('http://localhost:5000/loginAndRegister')
        self.driver.implicitly_wait(5)
        sign_up_button = self.driver.find_element_by_id('sign-up')
        sign_up_button.click()
        register_username_field = self.driver.find_element_by_id('register_username')
        register_username_field.send_keys('RandomGuy')
        email_field = self.driver.find_element_by_id('email')
        email_field.send_keys('123456@gmail.com')
        register_password_field = self.driver.find_element_by_id('register_password')
        register_password_field.send_keys('12345')
        register_password2_field = self.driver.find_element_by_id('register_password2')
        register_password2_field.send_keys('12345')
        time.sleep(1)
        register_submit = self.driver.find_element_by_id('registration_submit')
        register_submit.click()
        # test login
        self.driver.implicitly_wait(5)
        time.sleep(1)
        login_username_field = self.driver.find_element_by_id('login_username')
        login_username_field.send_keys('RandomGuy')
        login_password_field = self.driver.find_element_by_id('login_password')
        login_password_field.send_keys('12345')
        time.sleep(1)
        login_submit = self.driver.find_element_by_id('login_submit')
        login_submit.click()

        # check login success
        self.driver.implicitly_wait(5)
        time.sleep(1)
        logout = self.driver.find_element_by_partial_link_text('Logout')
        self.assertEqual(logout.get_attribute('innerHTML'), 'RandomGuy_Logout', msg='Logged in')


if __name__ == '__main__':
    unittest.main()
