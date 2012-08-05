#!/usr/bin/env

import htpasswd
import unittest
import shutil

t_groupdb = "tests/test.groupdb"


class BasicTests(unittest.TestCase):
    def setUp(self):
        shutil.copy(t_groupdb, "tests/test.groupdb_backup")

    def tearDown(self):
        shutil.move("tests/test.groupdb_backup", t_groupdb)

    def test_groups(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            self.assertEqual(groupdb.groups, ["admins", "managers"])

    def test___contains__(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            self.assertTrue(groupdb.__contains__("admins"))
            self.assertFalse(groupdb.__contains__("admins1"))

    def test_is_user_in(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            self.assertTrue(groupdb.is_user_in("bob", "admins"))
            self.assertFalse(groupdb.is_user_in("bob", "managers"))

    def test_add_user(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            groupdb.add_user("alice", "admins")
            self.assertTrue(groupdb.is_user_in("alice", "admins"))

    def test_delete_user(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            groupdb.delete_user("bob", "admins")
            self.assertFalse(groupdb.is_user_in("bob", "admins"))


if __name__ == '__main__':
    unittest.main()
