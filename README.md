# htpasswd

## Description
**htpasswd** is a library for working with htpasswd user (only basic authorization) and group files.

## Dependencies
- Python 2.6 or 2.7
- [orderedmultidict](http://pypi.python.org/pypi/orderedmultidict/0.7) >= 0.7

## Sample usage
    import htpasswd
    
    with htpasswd.Basic("/path/to/user.db") as userdb:
        try:
            userdb.add_user("bob", "password")
        except htpasswd.basic.UserExists, e:
            print e
        try:
            userdb.change_password("alice", "newpassword")
        except htpasswd.basic.UserNotExists, e:
            print e

    with htpasswd.Group("/path/to/group.db") as groupdb:
        try:
            groupdb.add_user_to_group("bob", "admins")
        except htpasswd.group.UserAlreadyInAGroup, e:
            print e
        try:
            groupdb.delete_user_from_group("alice", "managers")
        except htpasswd.group.UserNotInAGroup, e:
            print e

## Provided methods

### Basic
- show_users()
- is\_user\_exists(user)
- add_user(user, password)
- delete_user(user)
- change_password(user, password)
- _crypt_password(password)

### Group
- show_groups()
- is\_group\_exists(group)
- is\_user\_in\_a\_group(user, group)
- add\_user\_to\_group(user, group)
- delete\_user\_from\_group(user,  group)

## Exceptions

### HtException

That's a general exception from which others are inherited.

### UserExists
Raised by ``add_user`` if user already exists.

### UserNotExists
Raised by ``delete_user`` and ``change_password`` if there is no such user.

### GroupNotExists
Raised by ``delete_user_from_group`` if there is no such group.

### UserAlreadyInAGroup
Raised by ``add_user_to_group`` if user is already in a group.

### UserNotInAGroup
Raised by ``delete_user_from_group`` if user isn't in a group.