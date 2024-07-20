import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('pos_system.db')
cursor = conn.cursor()

# Add the `type` column to `menu_items` table
try:
    cursor.execute("ALTER TABLE menu_items ADD COLUMN type TEXT DEFAULT 'food'")
    print("Added `type` column successfully.")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")

conn.commit()
conn.close()
