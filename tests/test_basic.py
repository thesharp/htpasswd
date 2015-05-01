#!/usr/bin/env

import htpasswd
from htpasswd import UserExists, UserNotExists
import unittest
import shutil
from crypt import crypt

t_userdb = "tests/test.userdb"

class BasicMD5Tests(unittest.TestCase):
    def setUp(self):
        shutil.copy(t_userdb, "tests/test.userdb_backup")

    def tearDown(self):
        shutil.move("tests/test.userdb_backup", t_userdb)

    def test_users(self):
        with htpasswd.Basic(t_userdb, mode='md5') as userdb:
            self.assertEqual(userdb.users, ["bob", "alice"])

    def test___contains__(self):
        with htpasswd.Basic(t_userdb) as userdb:
            self.assertTrue(userdb.__contains__("bob"))
            self.assertFalse(userdb.__contains__("bob1"))

    def test_not_exists(self):
        with htpasswd.Basic(t_userdb, mode='md5') as userdb:
            def not_exists():
                userdb.__contains__("nobody")
            self.assertRaises(UserNotExists, not_exists())

    def test_exists(self):
        with htpasswd.Basic(t_userdb, mode='md5') as userdb:
            self.assertRaises(UserExists, lambda: userdb.add("bob", "password"))

    def test_add(self):
        with htpasswd.Basic(t_userdb, mode='md5') as userdb:
            userdb.add("henry", "password")
            self.assertTrue(userdb.__contains__("henry"))

    def test_pop(self):
        with htpasswd.Basic(t_userdb, mode='md5') as userdb:
            userdb.pop("alice")
            self.assertFalse(userdb.__contains__("alice"))

    def test_pop_exception(self):
        with htpasswd.Basic(t_userdb, mode='md5') as userdb:
            self.assertRaises(htpasswd.UserNotExists, lambda: userdb.pop("nobody"))

    def test_change_password(self):
        with htpasswd.Basic(t_userdb, mode='md5') as userdb:
            userdb.change_password("alice", "password")
        with open(t_userdb, "r") as users:
            for user in users.readlines():
                if user.startswith("alice:"):
                    test = user
        self.assertRegexpMatches(test, "alice:\$apr1\$")

    def test_change_password_exception(self):
        with htpasswd.Basic(t_userdb, mode='md5') as userdb:
            self.assertRaises(htpasswd.UserNotExists, lambda: userdb.change_password("nobody",
                                                                                     "password"))
    def test_invalid_mode_exception(self):
        with htpasswd.Basic(t_userdb, mode='blah') as userdb:
            self.assertRaises(htpasswd.UnknownEncryptionMode, lambda: userdb.change_password("bob",
                                                                                     "password"))
    def test_no_newline(self):
        with htpasswd.Basic(t_userdb, mode='md5') as userdb:
            self.assertNotIn('\n', userdb._encrypt_password('password'), msg="no newline characters allowed in pwd")
            self.assertNotIn('\r', userdb._encrypt_password('password'), msg="no newline characters allowed in pwd")
    def test__crypt_password(self):
        with htpasswd.Basic(t_userdb, mode='md5') as userdb:
            password = userdb._crypt_password("password")
            salt = password[:2]
            test = crypt("password", salt)
            self.assertEqual(password, test)

class BasicTests(unittest.TestCase):
    def setUp(self):
        shutil.copy(t_userdb, "tests/test.userdb_backup")

    def tearDown(self):
        shutil.move("tests/test.userdb_backup", t_userdb)

    def test_users(self):
        with htpasswd.Basic(t_userdb) as userdb:
            self.assertEqual(userdb.users, ["bob", "alice"])

    def test___contains__(self):
        with htpasswd.Basic(t_userdb) as userdb:
            self.assertTrue(userdb.__contains__("bob"))
            self.assertFalse(userdb.__contains__("bob1"))

    def test_not_exists(self):
        with htpasswd.Basic(t_userdb) as userdb:
            def not_exists():
                userdb.__contains__("nobody")
            self.assertRaises(UserNotExists, not_exists())

    def test_exists(self):
        with htpasswd.Basic(t_userdb) as userdb:
            self.assertRaises(UserExists, lambda: userdb.add("bob", "password"))

    def test_add(self):
        with htpasswd.Basic(t_userdb) as userdb:
            userdb.add("henry", "password")
            self.assertTrue(userdb.__contains__("henry"))

    def test_pop(self):
        with htpasswd.Basic(t_userdb) as userdb:
            userdb.pop("alice")
            self.assertFalse(userdb.__contains__("alice"))

    def test_pop_exception(self):
        with htpasswd.Basic(t_userdb) as userdb:
            self.assertRaises(htpasswd.UserNotExists, lambda: userdb.pop("nobody"))

    def test_change_password(self):
        with htpasswd.Basic(t_userdb) as userdb:
            userdb.change_password("alice", "password")
        with open(t_userdb, "r") as users:
            for user in users.readlines():
                if user.startswith("alice:"):
                    test = user
        self.assertNotEqual(test, "alice:2EtHk7FyD0THc\n")

    def test_change_password_exception(self):
        with htpasswd.Basic(t_userdb) as userdb:
            self.assertRaises(htpasswd.UserNotExists, lambda: userdb.change_password("nobody",
                                                                                     "password"))

    def test__crypt_password(self):
        with htpasswd.Basic(t_userdb) as userdb:
            password = userdb._crypt_password("password")
            salt = password[:2]
            test = crypt("password", salt)
            self.assertEqual(password, test)

if __name__ == '__main__':
    unittest.main()
