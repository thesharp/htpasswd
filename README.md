# htpasswd

## Description
**htpasswd** is a library for working with htpasswd user (only basic authorization) and group files.

[![Build Status](https://secure.travis-ci.org/thesharp/htpasswd.png)](http://travis-ci.org/thesharp/htpasswd)

## Dependencies
- Python 2.6 or 2.7
- [orderedmultidict](http://pypi.python.org/pypi/orderedmultidict/0.7) >= 0.7
- [nose](http://pypi.python.org/pypi/nose/) >= 1.1.2 (for tests)

## Sample usage
    import htpasswd

    with htpasswd.Basic("/path/to/user.db") as userdb:
        try:
            userdb.add("bob", "password")
        except htpasswd.basic.UserExists, e:
            print e
        try:
            userdb.change_password("alice", "newpassword")
        except htpasswd.basic.UserNotExists, e:
            print e

    with htpasswd.Group("/path/to/group.db") as groupdb:
        try:
            groupdb.add_user("bob", "admins")
        except htpasswd.group.UserAlreadyInAGroup, e:
            print e
        try:
            groupdb.delete_user("alice", "managers")
        except htpasswd.group.UserNotInAGroup, e:
            print e

## Provided methods

### Basic
- ``__contains__(user)``
- ``users``
- ``add(user, password)``
- ``delete(user)``
- ``change_password(user, password)``
- ``_crypt_password(password)``

### Group
- ``__contains__(group)``
- ``groups``
- ``is_user_in(user, group)``
- ``add_user(user, group)``
- ``delete_user(user,  group)``

## Exceptions

### HtException

That's a general exception from which others are inherited.

### UserExists
Raised by ``Basic.add`` if user already exists.

### UserNotExists
Raised by ``Basic.delete`` and ``Basic.change_password`` if there is no such user.

### GroupNotExists
Raised by ``Group.delete_user`` if there is no such group.

### UserAlreadyInAGroup
Raised by ``Group.add_user`` if user is already in a group.

### UserNotInAGroup
Raised by ``Group.delete_user`` if user isn't in a group.
