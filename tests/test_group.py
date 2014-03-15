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
            self.assertRaises(htpasswd.UserAlreadyInAGroup, lambda: groupdb.add_user("alice", "admins"))

    def test_delete_user(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            groupdb.delete_user("bob", "admins")
            self.assertFalse(groupdb.is_user_in("bob", "admins"))
            self.assertRaises(htpasswd.GroupNotExists, lambda: groupdb.delete_user("bob", "nogroup"))
            groupdb.add_user("alice", "admins")
            self.assertRaises(htpasswd.UserNotInAGroup, lambda: groupdb.delete_user("bob", "admins"))

    def test_user_not_in_a_group(self):
        with htpasswd.Group(t_groupdb) as groupdb:
            result = False
            try:
                groupdb.delete_user("alice", "admins")
            except htpasswd.UserNotInAGroup:
                result = True
            self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
