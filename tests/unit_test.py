import unittest
from app import create_app, db
from app.models import User
from config import TestingConfig


class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='moebuta')
        u.set_password('1a2b3c')
        self.assertFalse(u.check_password('12345'))
        self.assertTrue(u.check_password('1a2b3c'))


if __name__ == '__main__':
    unittest.main(verbosity=2)