import sqlite3

def update_db():
    conn = sqlite3.connect('pos_system.db')
    cursor = conn.cursor()

    # Add 'status' column to 'orders' table if it doesn't exist
    cursor.execute("PRAGMA table_info(orders)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'status' not in columns:
        cursor.execute("ALTER TABLE orders ADD COLUMN status TEXT NOT NULL DEFAULT 'Pending'")
        print("Added 'status' column to 'orders' table.")
    else:
        print("'status' column already exists in 'orders' table.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
