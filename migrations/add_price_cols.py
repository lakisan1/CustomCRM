import sqlite3
import os
import sys

# Ensure we can import 'shared' from parent dir
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from shared.db import get_db

def migrate():
    print("Migrating prices table...")
    conn = get_db()
    cur = conn.cursor()

    columns_to_add = [
        ("warranty_percent", "REAL DEFAULT 0"),
        ("service_percent", "REAL DEFAULT 0"),
        ("instalation", "REAL DEFAULT 0"),
        ("traning", "REAL DEFAULT 0"),
        ("other", "REAL DEFAULT 0"),
    ]

    for col_name, col_type in columns_to_add:
        try:
            cur.execute(f"ALTER TABLE prices ADD COLUMN {col_name} {col_type};")
            print(f"Added column: {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"Column {col_name} already exists, skipping.")
            else:
                print(f"Error adding {col_name}: {e}")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
