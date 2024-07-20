import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('pos_system.db')
cursor = conn.cursor()

# Create the `drink_orders` table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS drink_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_details TEXT,
    total_price REAL,
    status TEXT
)
""")

conn.commit()
conn.close()
