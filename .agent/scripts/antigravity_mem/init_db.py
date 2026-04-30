"""
Memory DB Initialization Script
=================================
Creates the full memory.db schema from scratch.
Includes all columns from migrations for fresh installs.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), ".agent", "memory.db")


def init_db():
    print(f"Initializing database at: {DB_PATH}")

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        start_time TEXT,
        end_time TEXT,
        summary TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        type TEXT,
        description TEXT,
        affected_files TEXT,
        overwritten_functions TEXT,
        timestamp TEXT,
        confidence REAL DEFAULT 0.5,
        detection_method TEXT DEFAULT 'heuristic',
        change_type TEXT DEFAULT 'unknown',
        FOREIGN KEY (session_id) REFERENCES sessions (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS unclassified_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        observation_id INTEGER,
        file_path TEXT,
        reason TEXT NOT NULL,
        raw_diff TEXT,
        timestamp TEXT NOT NULL,
        reviewed INTEGER DEFAULT 0,
        FOREIGN KEY (observation_id) REFERENCES observations (id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
