from crypt import crypt
from string import ascii_letters, digits
from random import choice
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class UserExists(Exception):

    def __str__(self):
        return "User already exists"


class UserNotExists(Exception):

    def __str__(self):
        return "User not exists"


class Basic(object):
    """ Basic object deals with Basic HTTP Authorization configuration file.
    It is passed the path to userdb file. """

    def __init__(self, userdb):
        self.userdb = userdb
        self.initial_users = OrderedDict()
        self.new_users = OrderedDict()

    def __enter__(self):
        with open(self.userdb, "r") as users:
            for i in users:
                user, password = i.split(":", 1)
                self.initial_users[user] = password
        self.new_users = self.initial_users.copy()
        return self

    def __exit__(self, type, value, traceback):
        if self.new_users == self.initial_users:
            return
        with open(self.userdb, "w") as userdb:
            for user in self.new_users:
                userdb.write("%s:%s" % (user, self.new_users[user]))

    def __contains__(self, user):
        return user in self.users

    @property
    def users(self):
        """ Returns users in a tuple """
        return list(self.new_users.keys())

    def add(self, user, password):
        """ Adds a user with password """
        if self.__contains__(user):
            raise UserExists
        self.new_users[user] = self._crypt_password(password) + "\n"

    def pop(self, user):
        """ Deletes a user """
        if not self.__contains__(user):
            raise UserNotExists
        self.new_users.pop(user)

    def change_password(self, user, password):
        """ Changes user password """
        if not self.__contains__(user):
            raise UserNotExists
        self.new_users[user] = self._crypt_password(password) + "\n"

    def _crypt_password(self, password):
        """ Crypts password """

        def salt():
            """ Generates some salt """
            symbols = ascii_letters + digits
            return choice(symbols) + choice(symbols)

        return crypt(password, salt())
