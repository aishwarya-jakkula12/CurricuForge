import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "curriculum.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # FORCE fresh table
    cur.execute("DROP TABLE IF EXISTS curriculum")

    cur.execute("""
    CREATE TABLE curriculum (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT,
        level TEXT,
        duration TEXT,
        syllabus TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_curriculum(course, level, duration, syllabus):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO curriculum (course, level, duration, syllabus)
    VALUES (?, ?, ?, ?)
    """, (course, level, duration, syllabus))

    conn.commit()
    conn.close()


