import unittest
from datetime import datetime, timedelta
from app import app, db
from app.models import User


class UserModelCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='moebuta')
        u.set_password('1a2b3c')
        self.assertFalse(u.check_password('12345'))
        self.assertTrue(u.check_password('1a2b3c'))


if __name__ == '__main__':
    unittest.main(verbosity=2)