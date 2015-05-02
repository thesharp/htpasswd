from builtins import object
import re
from orderedmultidict import omdict


class GroupNotExists(Exception):

    def __str__(self):
        return "Group not exists"


class UserAlreadyInAGroup(Exception):

    def __str__(self):
        return "User already in a group"


class UserNotInAGroup(Exception):

    def __str__(self):
        return "User not in a group"


class Group(object):

    """ Group object deals with group authorization files.  It is passed the
    path to groupdb file. """

    def __init__(self, groupdb):
        self.groupdb = groupdb
        self.initial_groups = omdict()
        self.new_groups = omdict()

    def __enter__(self):
        with open(self.groupdb, "r") as groupdb:
            groupdb = re.sub("\\\\\n", "", groupdb.read())
            for group in groupdb.splitlines():
                groupname, users = group.split(": ", 1)
                for user in users.split():
                    self.initial_groups.add(groupname, user)
            self.new_groups = self.initial_groups.copy()
            return self

    def __exit__(self, type, value, traceback):
        if self.new_groups == self.initial_groups:
            return
        with open(self.groupdb, "w") as userdb:
            for group in self.new_groups:
                userdb.write("%s: %s\n" % (group, " ".join(self.new_groups.getlist(group))))

    def __contains__(self, group):
        return group in self.groups

    @property
    def groups(self):
        """ Returns groups in a tuple """
        return list(self.new_groups.keys())

    def is_user_in(self, user, group):
        """ Returns True if user is in a group """
        return user in self.new_groups.getlist(group)

    def add_user(self, user, group):
        """ Adds user to a group """
        if self.is_user_in(user, group):
            raise UserAlreadyInAGroup
        self.new_groups.add(group, user)

    def delete_user(self, user, group):
        """ Deletes user from group """
        if not self.__contains__(group):
            raise GroupNotExists
        if not self.is_user_in(user, group):
            raise UserNotInAGroup
        self.new_groups.popvalue(group, user)
