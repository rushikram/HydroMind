import os
import sqlite3
from datetime import datetime

# Define path to SQLite DB
DB_PATH = "data/hydration.db"

# Ensure the 'data' directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def init_db():
    """Initializes the hydration database and tables if they do not exist."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # Water intake log table per user
        c.execute("""
            CREATE TABLE IF NOT EXISTS water (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                amount_ml INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        # Metadata table for global reset tracking
        c.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        conn.commit()
        check_and_reset_if_new_day(conn)


def check_and_reset_if_new_day(conn):
    """Checks date and resets water log if a new day has started (global reset)."""
    today = datetime.now().strftime("%Y-%m-%d")
    c = conn.cursor()
    c.execute("SELECT value FROM metadata WHERE key = 'last_date'")
    row = c.fetchone()

    if row is None or row[0] != today:
        print("[⏰ Auto Reset] New day detected — clearing all water logs.")
        c.execute("DELETE FROM water")
        c.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES ('last_date', ?)", (today,))
        conn.commit()


def add_entry(user_id: str, amount_ml: int) -> dict:
    """Adds a water intake entry for the specified user."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO water (user_id, amount_ml, timestamp) VALUES (?, ?, ?)",
            (user_id, amount_ml, now)
        )
        conn.commit()
    return {"status": "success", "user_id": user_id, "amount_ml": amount_ml, "timestamp": now}


def get_history(user_id: str) -> list:
    """Returns full hydration history for a specific user."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT amount_ml, timestamp FROM water WHERE user_id = ? ORDER BY timestamp ASC",
            (user_id,)
        )
        rows = c.fetchall()
    return [{"amount_ml": row[0], "timestamp": row[1]} for row in rows]


def get_today_total(user_id: str) -> int:
    """Returns today's total water intake for the given user."""
    today = datetime.now().strftime("%Y-%m-%d")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT SUM(amount_ml) FROM water WHERE user_id = ? AND DATE(timestamp) = ?",
            (user_id, today)
        )
        result = c.fetchone()[0]
    return result if result is not None else 0


def reset_user_data(user_id: str) -> dict:
    """Manually resets hydration log for a specific user."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM water WHERE user_id = ?", (user_id,))
        conn.commit()
    print(f"✅ Hydration log reset for user: {user_id}")
    return {"status": "success", "message": f"Hydration log cleared for user: {user_id}"}


# Automatically initialize DB when this module is imported
init_db()
