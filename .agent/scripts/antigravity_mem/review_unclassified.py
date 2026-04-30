"""
Review Unclassified Logs
========================
An interactive script to review and clear unclassified chunks
from the memory.db unclassified_log table.
"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.getcwd(), ".agent", "memory.db")

def review_logs():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database not found at {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='unclassified_log'")
    if cursor.fetchone() is None:
        print("unclassified_log table does not exist.")
        sys.exit(0)

    # Check if reviewed column exists
    cursor.execute("PRAGMA table_info(unclassified_log)")
    if "reviewed" not in [col[1] for col in cursor.fetchall()]:
        print("reviewed column does not exist. Please run migrate_memory_db.py first.")
        sys.exit(1)

    cursor.execute(
        "SELECT id, file_path, reason, raw_diff, timestamp FROM unclassified_log WHERE reviewed = 0"
    )
    unreviewed = cursor.fetchall()

    if not unreviewed:
        print("✅ No unreviewed entries in unclassified_log. You're all caught up!")
        conn.close()
        sys.exit(0)

    print(f"Found {len(unreviewed)} unreviewed entries.")
    
    # In a non-interactive environment, we might just want to list them or auto-mark
    # If not interactive, just print summary and exit
    if not sys.stdout.isatty():
        print("Non-interactive mode: Listing first 5 entries:")
        for idx, row in enumerate(unreviewed[:5]):
            log_id, file_path, reason, raw_diff, timestamp = row
            print(f"[{log_id}] {timestamp} | {file_path}")
            print(f"Reason: {reason}")
            print("-" * 40)
        print("\nRun this script in an interactive terminal to mark them as reviewed.")
        conn.close()
        sys.exit(0)

    marked_count = 0
    for row in unreviewed:
        log_id, file_path, reason, raw_diff, timestamp = row
        print(f"\n--- Entry [{log_id}] ---")
        print(f"Time:   {timestamp}")
        print(f"File:   {file_path}")
        print(f"Reason: {reason}")
        print("Diff Preview:")
        print("\n".join(raw_diff.split("\n")[:10]))  # Show first 10 lines
        if len(raw_diff.split("\n")) > 10:
            print("... (truncated)")
        
        while True:
            choice = input("\nMark as reviewed? [y/N/q(uit)]: ").strip().lower()
            if choice == 'y':
                cursor.execute("UPDATE unclassified_log SET reviewed = 1 WHERE id = ?", (log_id,))
                conn.commit()
                marked_count += 1
                print("Marked as reviewed.")
                break
            elif choice == 'n' or choice == '':
                print("Skipped.")
                break
            elif choice == 'q':
                print(f"Exiting. Marked {marked_count} entries as reviewed.")
                conn.close()
                sys.exit(0)
            else:
                print("Invalid choice.")

    print(f"\nFinished. Marked {marked_count} entries as reviewed.")
    conn.close()

if __name__ == "__main__":
    review_logs()
