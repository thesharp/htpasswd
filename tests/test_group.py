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

    def test_show_groups(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            self.assertEqual(groupdb.show_groups(), ["admins", "managers"])

    def test_is_group_exists(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            self.assertTrue(groupdb.is_group_exists("admins"))
            self.assertFalse(groupdb.is_group_exists("admins1"))

    def test_is_user_in_a_group(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            self.assertTrue(groupdb.is_user_in_a_group("bob", "admins"))
            self.assertFalse(groupdb.is_user_in_a_group("bob", "managers"))

    def test_add_user_to_group(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            groupdb.add_user_to_group("alice", "admins")
            self.assertTrue(groupdb.is_user_in_a_group("alice", "admins"))

    def test_delete_user_from_group(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            groupdb.delete_user_from_group("bob", "admins")
            self.assertFalse(groupdb.is_user_in_a_group("bob", "admins"))


if __name__ == '__main__':
    unittest.main()
