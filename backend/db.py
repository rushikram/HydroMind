import os
import sqlite3
from datetime import datetime

# Define path to SQLite DB
DB_PATH = "data/hydration.db"

# Ensure the 'data' directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# === Initialize the database ===
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # Table for hydration logs
        c.execute("""
            CREATE TABLE IF NOT EXISTS water (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                amount_ml INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        # Metadata table (global last reset date)
        c.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        conn.commit()
        check_and_reset_if_new_day(conn)

# === Daily reset (global) — optional ===
def check_and_reset_if_new_day(conn):
    today = datetime.now().strftime("%Y-%m-%d")
    c = conn.cursor()
    c.execute("SELECT value FROM metadata WHERE key = 'last_date'")
    row = c.fetchone()
    if row is None or row[0] != today:
        print("[⏰ Auto Reset] New day detected — clearing all water logs.")
        c.execute("DELETE FROM water")  # This clears logs for all users
        c.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES ('last_date', ?)", (today,))
        conn.commit()

# === Add new entry for a specific user ===
def add_entry(user_id: str, amount_ml: int) -> dict:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO water (user_id, amount_ml, timestamp) VALUES (?, ?, ?)",
            (user_id, amount_ml, now)
        )
        conn.commit()
    return {
        "status": "success",
        "user_id": user_id,
        "amount_ml": amount_ml,
        "timestamp": now
    }

# === Get hydration history for a specific user ===
def get_history(user_id: str) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT amount_ml, timestamp FROM water WHERE user_id = ? ORDER BY timestamp ASC",
            (user_id,)
        )
        rows = c.fetchall()
    return [{"amount_ml": row[0], "timestamp": row[1]} for row in rows]

# === Get today's total intake for a user ===
def get_today_total(user_id: str) -> int:
    today = datetime.now().strftime("%Y-%m-%d")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT SUM(amount_ml) FROM water WHERE user_id = ? AND DATE(timestamp) = ?",
            (user_id, today)
        )
        result = c.fetchone()[0]
    return result if result is not None else 0

# === Reset hydration log for a specific user ===
def reset_db(user_id: str) -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM water WHERE user_id = ?", (user_id,))
        today = datetime.now().strftime("%Y-%m-%d")
        # Global last reset metadata — optional to update
        c.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES ('last_date', ?)", (today,))
        conn.commit()
    print(f"✅ hydration.db reset — entries cleared for user: {user_id}")
    return {"status": "success", "message": f"Hydration log cleared for user: {user_id}"}

# === Always initialize DB on import ===
init_db()
