
import sqlite3

FILE = "mybudgetbuddy.db"


def connect():
    return sqlite3.connect(FILE)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS user_budgets (
        user_id INTEGER PRIMARY KEY,
        month TEXT NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS user_category_budgets (
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        PRIMARY KEY (user_id, category),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS user_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        ("admin", "admin123")
    )

    conn.commit()
    conn.close()


def get_users():
    create_tables()
    conn = connect()
    rows = conn.execute("SELECT id, username, password FROM users").fetchall()
    conn.close()
    return [{"id": r[0], "username": r[1], "password": r[2]} for r in rows]


def register_user(username, password):
    create_tables()
    conn = connect()
    try:
        conn.execute(
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
    row = conn.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()
    conn.close()
    return {"id": row[0], "username": row[1]} if row else None


def load_user_data(username):
    create_tables()
    conn = connect()
    cursor = conn.cursor()
    user = cursor.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone()

    budget = {"month": "", "total": 0, "categories": {}}
    expenses = []

    if user:
        user_id = user[0]
        row = cursor.execute(
            "SELECT month, total FROM user_budgets WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if row:
            budget["month"], budget["total"] = row

        budget["categories"] = dict(cursor.execute(
            """SELECT category, amount FROM user_category_budgets
            WHERE user_id = ? ORDER BY rowid""", (user_id,)
        ).fetchall())

        expenses = [
            {"description": d, "category": c, "amount": a}
            for d, c, a in cursor.execute(
                """SELECT description, category, amount FROM user_expenses
                WHERE user_id = ? ORDER BY id""", (user_id,)
            ).fetchall()
        ]

    conn.close()
    return budget, expenses


def save_user_data(username, budget, expenses):
    create_tables()
    conn = connect()
    cursor = conn.cursor()

    try:
        user = cursor.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()

        if not user:
            return False

        user_id = user[0]

        cursor.execute("""
            INSERT INTO user_budgets (user_id, month, total) VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
            month = excluded.month, total = excluded.total
        """, (user_id, budget["month"], budget["total"]))

        cursor.execute(
            "DELETE FROM user_category_budgets WHERE user_id = ?", (user_id,)
        )
        cursor.executemany(
            """INSERT INTO user_category_budgets (user_id, category, amount)
            VALUES (?, ?, ?)""",
            [(user_id, c, a) for c, a in budget["categories"].items()]
        )

        cursor.execute(
            "DELETE FROM user_expenses WHERE user_id = ?", (user_id,)
        )
        cursor.executemany(
            """INSERT INTO user_expenses
            (user_id, description, category, amount) VALUES (?, ?, ?, ?)""",
            [(user_id, e["description"], e["category"], e["amount"])
             for e in expenses]
        )

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
