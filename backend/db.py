import os
import sqlite3
from datetime import datetime

# Define path to SQLite DB
DB_PATH = "data/hydration.db"

# Ensure the 'data' directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Initialize the database with the required tables
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # Water intake log table with user_id
        c.execute("""
            CREATE TABLE IF NOT EXISTS water (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                amount_ml INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        # Metadata table to store last reset date
        c.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        conn.commit()
        check_and_reset_if_new_day(conn)

# Resets hydration log if a new calendar day has started
def check_and_reset_if_new_day(conn):
    today = datetime.now().strftime("%Y-%m-%d")
    c = conn.cursor()
    c.execute("SELECT value FROM metadata WHERE key = 'last_date'")
    row = c.fetchone()
    if row is None or row[0] != today:
        print("[⏰ Auto Reset] New day detected — clearing water log.")
        c.execute("DELETE FROM water")
        c.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES ('last_date', ?)", (today,))
        conn.commit()

# Add a new water entry for a specific user
def add_entry(user_id: str, amount_ml: int) -> dict:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO water (user_id, amount_ml, timestamp) VALUES (?, ?, ?)", (user_id, amount_ml, now))
        conn.commit()
    return {"status": "success", "user_id": user_id, "amount_ml": amount_ml, "timestamp": now}

# Get full history for a specific user
def get_history(user_id: str) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT amount_ml, timestamp FROM water WHERE user_id = ? ORDER BY timestamp ASC", (user_id,))
        rows = c.fetchall()
    return [{"amount_ml": row[0], "timestamp": row[1]} for row in rows]

# Get today’s total intake for a user
def get_today_total(user_id: str) -> int:
    today = datetime.now().strftime("%Y-%m-%d")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT SUM(amount_ml) FROM water WHERE user_id = ? AND DATE(timestamp) = ?", (user_id, today))
        result = c.fetchone()[0]
    return result if result is not None else 0

# Manual reset from API/Streamlit
def reset_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM water")
        today = datetime.now().strftime("%Y-%m-%d")
        c.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES ('last_date', ?)", (today,))
        conn.commit()
    print("✅ hydration.db reset — all entries cleared.")
    return {"status": "success", "message": "Hydration log cleared."}

# Always init on module import
init_db()
