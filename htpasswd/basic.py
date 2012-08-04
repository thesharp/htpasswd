from crypt import crypt
from string import ascii_letters, digits
from random import choice
from collections import OrderedDict

from exceptions import HtException


class UserExists(HtException):

    def __str__(self):
        return "User already exists"


class UserNotExists(HtException):

    def __str__(self):
        return "User not exists"


class Basic(object):
    """ Basic object deals with Basic HTTP Authorization configuration file.
    It is passed the path to userdb file. """

    def __init__(self, userdb):
        self.userdb = userdb
        self.users = OrderedDict()
        self.new_users = OrderedDict()

    def __enter__(self):
        with open(self.userdb, "r") as users:
            for i in users:
                user, password = i.split(":", 1)
                self.users[user] = password
        self.new_users = self.users.copy()
        return self

    def __exit__(self, type, value, traceback):
        if self.new_users == self.users:
            return
        with open(self.userdb, "w") as userdb:
            for user in self.new_users:
                userdb.write("%s:%s" % (user, self.new_users[user]))

    def show_users(self):
        """ Returns users in a tuple """
        return self.new_users.keys()

    def is_user_exists(self, user):
        """ Returns True if user exists """
        return user in self.show_users()

    def add_user(self, user, password):
        """ Adds a user with password """
        if self.is_user_exists(user):
            raise UserExists
        self.new_users[user] = self._crypt_password(password) + "\n"

    def delete_user(self, user):
        """ Deletes a user """
        if not self.is_user_exists(user):
            raise UserNotExists
        self.new_users.pop(user)

    def change_password(self, user, password):
        """ Changes user password """
        if not self.is_user_exists(user):
            raise UserNotExists
        self.new_users[user] = self._crypt_password(password) + "\n"

    def _crypt_password(self, password):
        """ Crypts password """

        def salt():
            """ Generates some salt """
            symbols = ascii_letters + digits
            return choice(symbols) + choice(symbols)

        return crypt(password, salt())
