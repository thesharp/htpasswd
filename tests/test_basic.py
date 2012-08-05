#!/usr/bin/env

import htpasswd
import unittest
import shutil
from crypt import crypt

t_userdb = "tests/test.userdb"


class BasicTests(unittest.TestCase):
    def setUp(self):
        shutil.copy(t_userdb, "tests/test.userdb_backup")

    def tearDown(self):
        shutil.move("tests/test.userdb_backup", t_userdb)

    def test_show_users(self):
        with htpasswd.Basic(t_userdb) as userdb:
            self.assertEqual(userdb.show_users(), ["bob", "alice"])

    def test_is_user_exists(self):
        with htpasswd.Basic(t_userdb) as userdb:
            self.assertTrue(userdb.is_user_exists("bob"))
            self.assertFalse(userdb.is_user_exists("bob1"))

    def test_add_user(self):
        with htpasswd.Basic(t_userdb) as userdb:
            userdb.add_user("henry", "password")
            self.assertTrue(userdb.is_user_exists("henry"))

    def test_delete_user(self):
        with htpasswd.Basic(t_userdb) as userdb:
            userdb.delete_user("alice")
            self.assertFalse(userdb.is_user_exists("alice"))

    def test_change_password(self):
        with htpasswd.Basic(t_userdb) as userdb:
            userdb.change_password("alice", "password")
        with open(t_userdb, "r") as users:
            for user in users.readlines():
                if user.startswith("alice:"):
                    test = user
        self.assertNotEqual(test, "alice:2EtHk7FyD0THc\n")

    def test__crypt_password(self):
        with htpasswd.Basic(t_userdb) as userdb:
            password = userdb._crypt_password("password")
            salt = password[:2]
            test = crypt("password", salt)
            self.assertEqual(password, test)

if __name__ == '__main__':
    unittest.main()
