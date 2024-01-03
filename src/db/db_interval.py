import sqlite3
from sqlite3 import Error

DB_FILE = "user_states.db"

def create_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Error as e:
        print(e)
    return None

def create_table():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_states (
            user_id INTEGER PRIMARY KEY,
            time_interval TEXT
        )
        """)
        conn.commit()
        conn.close()

def delay_post_table():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS delay_post (
            user_id INTEGER PRIMARY KEY,
            time_post INTEGER
        )
        """)
        conn.commit()
        conn.close()

def get_time_interval(user_id):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT time_interval FROM user_states WHERE user_id=?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
    return None

def set_time_interval(user_id, time_interval):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO user_states (user_id, time_interval) VALUES (?, ?)", (user_id, time_interval))
        conn.commit()
        conn.close()
