import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('pos_system.db')
cursor = conn.cursor()

# Add a new column 'order_details' to the 'orders' table if it doesn't exist
try:
    cursor.execute("ALTER TABLE orders ADD COLUMN order_details TEXT")
    print("Column 'order_details' added successfully.")
except sqlite3.OperationalError:
    print("Column 'order_details' already exists.")

# Close the connection
conn.commit()
conn.close()
