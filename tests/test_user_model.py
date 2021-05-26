import unittest
from app.models import Admin

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        a = Admin(password = 'cat')
        self.assertTrue(a.password_hash is not None)

    def test_no_password_getter(self):
        a = Admin(password = 'cat')
        with self.assertRaises(AttributeError):
            a.password

    def test_password_verification(self):
        a = Admin(password='cat')
        self.assertTrue(a.verify_password('cat'))
        self.assertFalse(a.verify_password('dog'))

    def test_password_salts_are_random(self):
        a = Admin(password='cat')
        a2 = Admin(password='cat')
        self.assertTrue(a.password_hash != a2.password_hash)