import sqlite3

def initialize_db():
    conn = sqlite3.connect('pos_system.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL
    )
    ''')

    # Insert some sample menu items
    cursor.executemany('''
    INSERT INTO menu_items (name, price) VALUES (?, ?)
    ''', [
        ('Big Mac', 5.99),
        ('McChicken', 1.99),
        ('French Fries', 2.49),
        ('Coke', 1.29),
        ('Nuggets', 3.49),
        ('Filet-O-Fish', 3.79),
        ('Cheeseburger', 1.49),
        ('Apple Pie', 0.99)
    ])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    print("Database initialized and sample menu items added.")
