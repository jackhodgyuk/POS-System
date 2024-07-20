import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('pos_system.db')
cursor = conn.cursor()

# Fetch the schema of the 'orders' table
cursor.execute("PRAGMA table_info(orders)")
columns = cursor.fetchall()

print("Updated Orders table schema:")
for column in columns:
    print(column)

# Close the connection
conn.close()
