from database.database import load_data, save_data


def get_users():
    return load_data()[0]


def register(username, password):
    users, budget, expenses = load_data()

    if any(u["username"] == username for u in users):
        return False

    users.append({
        "username": username,
        "password": password
    })

    save_data(users, budget, expenses)
    return True