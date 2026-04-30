"""
Memory DB Migration Script
===========================
Adds change_type column and unclassified_log table to memory.db.
Idempotent — safe to run multiple times.
"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.getcwd(), ".agent", "memory.db")


def migrate():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database not found at {DB_PATH}")
        print("Run init_db.py first.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    migrations_applied = []

    # Migration 1: Add change_type column to observations
    cursor.execute("PRAGMA table_info(observations)")
    columns = [col[1] for col in cursor.fetchall()]

    if "change_type" not in columns:
        cursor.execute(
            "ALTER TABLE observations ADD COLUMN change_type TEXT DEFAULT 'unknown'"
        )
        migrations_applied.append("Added column: observations.change_type")

    if "confidence" not in columns:
        cursor.execute(
            "ALTER TABLE observations ADD COLUMN confidence REAL DEFAULT 0.5"
        )
        migrations_applied.append("Added column: observations.confidence")

    if "detection_method" not in columns:
        cursor.execute(
            "ALTER TABLE observations ADD COLUMN detection_method TEXT DEFAULT 'heuristic'"
        )
        migrations_applied.append("Added column: observations.detection_method")

    # Migration 2: Create unclassified_log table
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='unclassified_log'"
    )
    if cursor.fetchone() is None:
        cursor.execute("""
        CREATE TABLE unclassified_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            observation_id INTEGER,
            file_path TEXT,
            reason TEXT NOT NULL,
            raw_diff TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (observation_id) REFERENCES observations (id)
        )
        """)
        migrations_applied.append("Created table: unclassified_log")

    # Migration 3: Add reviewed column to unclassified_log
    cursor.execute("PRAGMA table_info(unclassified_log)")
    unclassified_columns = [col[1] for col in cursor.fetchall()]

    if "reviewed" not in unclassified_columns:
        cursor.execute(
            "ALTER TABLE unclassified_log ADD COLUMN reviewed INTEGER DEFAULT 0"
        )
        migrations_applied.append("Added column: unclassified_log.reviewed")

    conn.commit()
    conn.close()

    if migrations_applied:
        print(f"Migration complete. {len(migrations_applied)} change(s) applied:")
        for m in migrations_applied:
            print(f"  + {m}")
    else:
        print("No migrations needed — schema is up to date.")


if __name__ == "__main__":
    migrate()
