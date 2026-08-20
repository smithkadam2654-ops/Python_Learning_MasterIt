import sqlite3

def setup_database():
    """Demonstrates basic SQLite operations: Create, Insert, Select."""
    # Connect to an in-memory database (disappears when the script ends)
    # Use 'my_database.db' to save to a file instead.
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            age INTEGER
        )
    ''')
    
    # Insert data
    users_to_add = [
        ('alice_wonder', 28),
        ('bob_builder', 34),
        ('charlie_brown', 12)
    ]
    cursor.executemany('INSERT INTO users (username, age) VALUES (?, ?)', users_to_add)
    
    # Commit the transaction
    conn.commit()
    
    # Query data
    print("Users older than 20:")
    cursor.execute('SELECT username, age FROM users WHERE age > 20')
    for row in cursor.fetchall():
        print(f"- {row[0]} (Age: {row[1]})")
        
    # Close connection
    conn.close()

if __name__ == "__main__":
    setup_database()
