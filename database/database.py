import sqlite3

FILE = "mybudgetbuddy.db"


def connect():
    return sqlite3.connect(FILE)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY,
            month TEXT,
            total REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def load_data():
    create_tables()

    conn = connect()
    cursor = conn.cursor()

    users = []
    expenses = []
    budget = {
        "month": "",
        "total": 0,
        "categories": {}
    }

    cursor.execute("SELECT username, password FROM users")

    for username, password in cursor.fetchall():
        users.append({
            "username": username,
            "password": password
        })

    cursor.execute("SELECT month, total FROM budget WHERE id = 1")
    row = cursor.fetchone()

    if row:
        budget["month"] = row[0]
        budget["total"] = row[1]

    cursor.execute("SELECT category, amount FROM category_budgets")

    for category, amount in cursor.fetchall():
        budget["categories"][category] = amount

    cursor.execute("SELECT description, category, amount FROM expenses")

    for description, category, amount in cursor.fetchall():
        expenses.append({
            "description": description,
            "category": category,
            "amount": amount
        })

    conn.close()

    if not users:
        users.append({
            "username": "admin",
            "password": "admin123"
        })

        save_data(users, budget, expenses)

    return users, budget, expenses


def save_data(users, budget, expenses):
    create_tables()

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM budget")
    cursor.execute("DELETE FROM category_budgets")
    cursor.execute("DELETE FROM expenses")

    for user in users:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user["username"], user["password"])
        )

    cursor.execute(
        "INSERT INTO budget (id, month, total) VALUES (1, ?, ?)",
        (budget["month"], budget["total"])
    )

    for category, amount in budget["categories"].items():
        cursor.execute(
            "INSERT INTO category_budgets (category, amount) VALUES (?, ?)",
            (category, amount)
        )

    for expense in expenses:
        cursor.execute(
            "INSERT INTO expenses (description, category, amount) VALUES (?, ?, ?)",
            (expense["description"], expense["category"], expense["amount"])
        )

    conn.commit()
    conn.close()