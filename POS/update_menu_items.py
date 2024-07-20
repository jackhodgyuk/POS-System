import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('pos_system.db')
cursor = conn.cursor()

# Update item types for drinks
cursor.execute("UPDATE menu_items SET type='drinks' WHERE name='Coke'")
# Add any other drink items as needed
# cursor.execute("UPDATE menu_items SET type='drinks' WHERE name='Other Drink'")

conn.commit()
conn.close()
