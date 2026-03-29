import sqlite3
import os

db_path = 'instance/runs.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE hosted_run ADD COLUMN claimed_items TEXT DEFAULT '[]'")
        conn.commit()
        print("Column 'claimed_items' added successfully to 'hosted_run' table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Column 'claimed_items' already exists.")
        else:
            print(f"Error adding column: {e}")
    conn.close()
else:
    print(f"Database {db_path} not found.")
