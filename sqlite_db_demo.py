import sqlite3
import os

def demonstrate_sqlite():
    """Demonstrate basic SQLite database operations."""
    db_name = "example.db"
    
    # 1. Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 2. Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    
    # 3. Insert data
    try:
        cursor.execute("INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com')")
        cursor.execute("INSERT INTO users (username, email) VALUES ('bob', 'bob@example.com')")
        conn.commit()
    except sqlite3.IntegrityError:
        print("Users already exist in the database.")
        
    # 4. Query data
    print("Users in the database:")
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(row)
        
    # 5. Clean up
    conn.close()
    
    # Optional: Delete the db file to keep the workspace clean
    os.remove(db_name)
    print("\nDatabase file deleted.")

if __name__ == "__main__":
    demonstrate_sqlite()
