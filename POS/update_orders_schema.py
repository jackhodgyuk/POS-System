import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('pos_system.db')
cursor = conn.cursor()

try:
    # Rename the existing table
    cursor.execute("ALTER TABLE orders RENAME TO orders_old")

    # Create a new table with order_details column and without item_name constraint
    cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_details TEXT,
        total_price REAL,
        status TEXT
    )
    """)

    # Copy data from the old table to the new
    cursor.execute("""
    INSERT INTO orders (order_details, total_price, status)
    SELECT order_details, total_price, status FROM orders_old
    """)

    # Drop the old table
    cursor.execute("DROP TABLE orders_old")
    print("Schema updated successfully.")
except sqlite3.Error as e:
    print(f"An error occurred: {e}")

# Close the connection
conn.commit()
conn.close()

