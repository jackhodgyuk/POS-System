import sqlite3

def setup_db():
    conn = sqlite3.connect('pos_system.db')
    cursor = conn.cursor()
    
    # Create menu_items table
    cursor.execute('''CREATE TABLE IF NOT EXISTS menu_items (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        price REAL NOT NULL
                      )''')
    
    # Create orders table with status field
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        total_price REAL NOT NULL,
                        status TEXT NOT NULL DEFAULT 'Pending'
                      )''')
    
    # Insert sample menu items if the table is empty
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO menu_items (name, price) VALUES (?, ?)", [
            ('Big Mac', 5.99),
            ('McChicken', 3.99),
            ('Fries', 2.49),
            ('Coke', 1.49)
        ])
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_db()

