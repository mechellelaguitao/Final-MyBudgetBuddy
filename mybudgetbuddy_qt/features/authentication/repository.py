from database.database import (
    get_users,
    register_user,
    check_login
)


def get_all_users():
    return get_users()


def find_user(username, password):
    return check_login(username, password)


def register(username, password):
    return register_user(username, password)