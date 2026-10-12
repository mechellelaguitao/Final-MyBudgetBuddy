from .repository import find_user, register


def login(username, password):
    return find_user(username, password)


def create_account(username, password):
    return register(username, password)