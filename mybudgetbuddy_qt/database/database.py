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

    # Each user has their own budget period and total budget.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_budgets (
            user_id INTEGER PRIMARY KEY,
            month TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Each user has their own category budgets.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_category_budgets (
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            PRIMARY KEY (user_id, category),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Each expense belongs to one user.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Default account described in the README (ignored if it already exists).
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        ("admin", "admin123")
    )

    conn.commit()
    conn.close()


def get_users():
    create_tables()
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, password FROM users")
    rows = cursor.fetchall()

    conn.close()

    return [
        {"id": row[0], "username": row[1], "password": row[2]}
        for row in rows
    ]


def register_user(username, password):
    create_tables()
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def check_login(username, password):
    create_tables()
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    row = cursor.fetchone()

    conn.close()

    if row:
        return {"id": row[0], "username": row[1]}

    return None


def load_user_data(username):
    create_tables()
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()

    budget = {
        "month": "",
        "total": 0,
        "categories": {}
    }
    expenses = []

    if user:
        user_id = user[0]

        cursor.execute(
            "SELECT month, total FROM user_budgets WHERE user_id = ?",
            (user_id,)
        )
        row = cursor.fetchone()

        if row:
            budget["month"] = row[0]
            budget["total"] = row[1]

        cursor.execute(
            """
            SELECT category, amount
            FROM user_category_budgets
            WHERE user_id = ?
            ORDER BY rowid
            """,
            (user_id,)
        )

        for category, amount in cursor.fetchall():
            budget["categories"][category] = amount

        cursor.execute(
            """
            SELECT description, category, amount
            FROM user_expenses
            WHERE user_id = ?
            ORDER BY id
            """,
            (user_id,)
        )

        for description, category, amount in cursor.fetchall():
            expenses.append({
                "description": description,
                "category": category,
                "amount": amount
            })

    conn.close()

    return budget, expenses


def save_user_data(username, budget, expenses):
    create_tables()
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()

        if not user:
            return False

        user_id = user[0]

        # Save only this user's budget.
        cursor.execute(
            """
            INSERT INTO user_budgets (user_id, month, total)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET month = excluded.month,
                          total = excluded.total
            """,
            (user_id, budget["month"], budget["total"])
        )

        # Replace only this user's category budgets.
        cursor.execute(
            "DELETE FROM user_category_budgets WHERE user_id = ?",
            (user_id,)
        )

        for category, amount in budget["categories"].items():
            cursor.execute(
                """
                INSERT INTO user_category_budgets
                    (user_id, category, amount)
                VALUES (?, ?, ?)
                """,
                (user_id, category, amount)
            )

        # Replace only this user's expenses.
        cursor.execute(
            "DELETE FROM user_expenses WHERE user_id = ?",
            (user_id,)
        )

        for expense in expenses:
            cursor.execute(
                """
                INSERT INTO user_expenses
                    (user_id, description, category, amount)
                VALUES (?, ?, ?, ?)
                """,
                (
                    user_id,
                    expense["description"],
                    expense["category"],
                    expense["amount"]
                )
            )

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()