from .repository import get_users, register


def login(username, password):
    return any(
        u["username"] == username and u["password"] == password
        for u in get_users()
    )


def create_account(username, password):
    return register(username, password)