import sqlite3
import os

db_path = "instance/runs.db"

if not os.path.exists(db_path):
    print(f"Error: {db_path} not found.")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Adding 'is_private' column to 'character' table...")
    cursor.execute("ALTER TABLE character ADD COLUMN is_private BOOLEAN DEFAULT 0")
    
    conn.commit()
    conn.close()
    print("Migration successful: 'is_private' column added.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("Column 'is_private' already exists. Skipping.")
    else:
        print(f"Operational Error: {e}")
except Exception as e:
    print(f"Error during migration: {e}")
