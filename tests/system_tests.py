import unittest, os
from app import create_app, db
from tests import data
from selenium import webdriver
from config import TestingConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=os.path.join(basedir, 'geckodriver'))

        if not self.driver:
            self.skipTest('Web browser not available')

        else:
            self.app = create_app(TestingConfig)
            self.app_context = self.app.app_context()
            self.app_context.push()
            db.create_all()
            data.add_question()
            data.add_tutorial_data()

    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.remove()
            db.drop_all()
            db.session.remove()
            self.app_context.pop()


if __name__ == '__main__':
    unittest.main(verbosity=2)
