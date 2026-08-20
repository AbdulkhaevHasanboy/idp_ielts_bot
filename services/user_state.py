import sqlite3
import os
from config import DATABASE_PATH

def init_db():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            language TEXT DEFAULT 'uz',
            state TEXT DEFAULT 'NONE',
            calc_mode TEXT,
            last_center_id TEXT,
            calc_listening REAL,
            calc_reading REAL,
            calc_writing REAL,
            calc_speaking REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Ensure last_center_id column exists if table was previously created
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    if "last_center_id" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN last_center_id TEXT")
    
    conn.commit()
    conn.close()

def get_user_language(user_id: int) -> str:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row and row[0]:
        return row[0]
    return "uz"

def set_user_language(user_id: int, lang: str, username: str = "", first_name: str = ""):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, username, first_name, language)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            language = excluded.language,
            username = excluded.username,
            first_name = excluded.first_name
    """, (user_id, username or "", first_name or "", lang))
    conn.commit()
    conn.close()

def set_user_state(user_id: int, state: str, calc_mode: str = None, last_center_id: str = None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, state, calc_mode, last_center_id)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            state = excluded.state,
            calc_mode = COALESCE(excluded.calc_mode, users.calc_mode),
            last_center_id = COALESCE(excluded.last_center_id, users.last_center_id)
    """, (user_id, state, calc_mode, last_center_id))
    conn.commit()
    conn.close()

def get_user_state(user_id: int):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT state, calc_mode, language, last_center_id FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"state": row[0], "calc_mode": row[1], "language": row[2], "last_center_id": row[3]}
    return {"state": "NONE", "calc_mode": None, "language": "uz", "last_center_id": None}
