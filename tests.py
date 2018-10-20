import unittest
import os
import util.config as config
import util.accounts as accounts

config.use_test_db()  # Use a test database

class TestAccounts(unittest.TestCase):
    def setUp(self):
        accounts.create_table()

    def tearDown(self):
        try:
            os.remove(config.DB_FILE)
        except FileNotFoundError:
            pass

    def test_user_exists(self):
        self.assertFalse(accounts.user_exists('foo'))

    def test_add_user(self):
        self.assertFalse(accounts.user_exists('foo'))
        accounts.add_user('foo', 'bar')
        self.assertTrue(accounts.user_exists('foo'))
        accounts.add_user('new_user', 'bar')
        self.assertTrue(accounts.user_exists('new_user'))

    def test_auth_user(self):
        accounts.add_user('foo', 'bar')
        self.assertTrue(accounts.auth_user('foo', 'bar'))
        self.assertFalse(accounts.auth_user('foo', 'bad_pass'))
        self.assertFalse(accounts.auth_user('not_a_user', 'bar'))
        self.assertFalse(accounts.auth_user('not_a_user', 'not_a_pass'))

    def test_remove_user(self):
        accounts.add_user('foo', 'bar')
        self.assertTrue(accounts.user_exists('foo'))
        accounts.remove_user('foo')
        self.assertFalse(accounts.user_exists('foo'))
        accounts.remove_user('foo')
        self.assertFalse(accounts.user_exists('foo'))

if __name__ == '__main__':
    unittest.main()

