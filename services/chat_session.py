"""
Multi-turn Conversation Session & Memory Manager for IDP IELTS Bot.
Provides isolated per-user conversation memory (up to 100 turns) with a 15-20 minute sliding timeout window.
"""
import time
import logging
import sqlite3
from typing import List, Dict
from config import DATABASE_PATH
from google.genai import types

logger = logging.getLogger(__name__)

# Session timeout: 15 minutes (900 seconds)
SESSION_TIMEOUT_SECONDS = 900
# Max messages in active memory sliding window
MAX_SESSION_MESSAGES = 100

# In-memory fast cache: { user_id: { "last_activity": float, "messages": [ {"role": "user"|"model", "text": str, "time": float} ] } }
_SESSIONS: Dict[int, Dict] = {}

def init_history_table():
    """Creates the persistent chat_history table in SQLite if it does not exist."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                role TEXT,
                message TEXT,
                timestamp REAL
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_user ON chat_history (user_id, timestamp)")
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error initializing history table: {e}")

def get_user_session_messages(user_id: int) -> List[Dict]:
    """
    Returns active conversation messages for user within the 15-minute sliding window.
    Automatically resets expired sessions.
    """
    now = time.time()
    
    if user_id in _SESSIONS:
        session = _SESSIONS[user_id]
        if now - session["last_activity"] > SESSION_TIMEOUT_SECONDS:
            # Session expired after 15 minutes of inactivity - start fresh
            logger.info(f"User {user_id} session expired (>15 mins). Starting fresh session.")
            _SESSIONS[user_id] = {"last_activity": now, "messages": []}
            return []
        session["last_activity"] = now
        return session["messages"]
    
    # Restore from SQLite if recent (< 15 mins)
    recent_messages = []
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cutoff = now - SESSION_TIMEOUT_SECONDS
        cursor.execute("""
            SELECT role, message, timestamp 
            FROM chat_history 
            WHERE user_id = ? AND timestamp >= ? 
            ORDER BY timestamp ASC 
            LIMIT ?
        """, (user_id, cutoff, MAX_SESSION_MESSAGES))
        rows = cursor.fetchall()
        conn.close()
        
        for role, msg, ts in rows:
            recent_messages.append({"role": role, "text": msg, "time": ts})
    except Exception as e:
        logger.debug(f"Could not restore session from DB: {e}")

    _SESSIONS[user_id] = {
        "last_activity": now,
        "messages": recent_messages
    }
    return recent_messages

def add_message_to_session(user_id: int, role: str, text: str):
    """
    Appends a new turn ('user' or 'model') to the user's active session.
    """
    now = time.time()
    if user_id not in _SESSIONS:
        _SESSIONS[user_id] = {"last_activity": now, "messages": []}
        
    session = _SESSIONS[user_id]
    session["last_activity"] = now
    session["messages"].append({"role": role, "text": text, "time": now})
    
    # Keep within max limit
    if len(session["messages"]) > MAX_SESSION_MESSAGES:
        session["messages"] = session["messages"][-MAX_SESSION_MESSAGES:]
        
    # Save to SQLite asynchronously/safely
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (user_id, role, message, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, role, text, now)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.debug(f"Error persisting chat history: {e}")

def clear_user_session(user_id: int):
    """Explicitly clears a user's session memory."""
    if user_id in _SESSIONS:
        _SESSIONS[user_id] = {"last_activity": time.time(), "messages": []}

def build_gemini_history_contents(user_id: int, current_user_prompt: str, current_parts: list = None) -> List[types.Content]:
    """
    Builds the full multi-turn list of types.Content objects including previous conversation history.
    """
    history = get_user_session_messages(user_id)
    contents = []
    
    # 1. Add previous turns
    for turn in history:
        role = "user" if turn["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=turn["text"])]
            )
        )
        
    # 2. Add current turn
    if current_parts:
        parts = current_parts + [types.Part.from_text(text=current_user_prompt)]
    else:
        parts = [types.Part.from_text(text=current_user_prompt)]
        
    contents.append(
        types.Content(
            role="user",
            parts=parts
        )
    )
    
    return contents
