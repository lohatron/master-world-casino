import sqlite3
import json


DB_NAME = "data.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name VARCHAR(255),
                coins INTEGER DEFAULT 100,
                data TEXT DEFAULT '[]'
            )
        """)


def new_user(user_id, username):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO users (id, name) VALUES (?, ?)",
            (user_id, username)
        )


def add_toy(toy_name, user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT data FROM users WHERE id = ?",
            (user_id,)
        )
        row = cur.fetchone()

        if row is None:
            return False

        items = json.loads(row[0] or "[]")
        items.append(toy_name)

        cur.execute(
            "UPDATE users SET data = ? WHERE id = ?",
            (json.dumps(items, ensure_ascii=False), user_id)
        )

        return True


def find_user(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM users WHERE id = ?",
            (user_id,)
        )
        return cur.fetchone() is not None


def trade_items(user1_id, item1, user2_id, item2):
    if user1_id == user2_id:
        return False

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, data FROM users WHERE id IN (?, ?)",
            (user1_id, user2_id)
        )

        rows = cur.fetchall()
        users = {
            row[0]: json.loads(row[1] or "[]")
            for row in rows
        }

        if user1_id not in users or user2_id not in users:
            return False

        items1 = users[user1_id]
        items2 = users[user2_id]

        if item1 not in items1 or item2 not in items2:
            return False

        items1.remove(item1)
        items2.remove(item2)

        items1.append(item2)
        items2.append(item1)

        cur.execute(
            "UPDATE users SET data = ? WHERE id = ?",
            (json.dumps(items1, ensure_ascii=False), user1_id)
        )
        cur.execute(
            "UPDATE users SET data = ? WHERE id = ?",
            (json.dumps(items2, ensure_ascii=False), user2_id)
        )

        return True


def delete_account(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )
        return cur.rowcount > 0


def remove_item(user_id, item):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT data FROM users WHERE id = ?",
            (user_id,)
        )
        row = cur.fetchone()

        if row is None:
            return False

        items = json.loads(row[0] or "[]")

        if item not in items:
            return False

        items.remove(item)

        cur.execute(
            "UPDATE users SET data = ? WHERE id = ?",
            (json.dumps(items, ensure_ascii=False), user_id)
        )

        return True


def show_items(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT data FROM users WHERE id = ?",
            (user_id,)
        )
        row = cur.fetchone()

        if row is None:
            return None

        return json.loads(row[0] or "[]")


def update_coins(user_id, how_much):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET coins = coins + ? WHERE id = ?",
            (how_much, user_id)
        )
        return cur.rowcount > 0


def show_coins(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        # Fixed query syntax and tuple parameters
        cur.execute("SELECT coins FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        
        if row is None:
            return None
            
        return row[0]