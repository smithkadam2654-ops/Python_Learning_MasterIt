import sqlite3

def database_operations():
    db_name = "example_database.db"
    
    print(f"--- Connecting to SQLite Database: {db_name} ---")
    # Connect to the SQLite database (this creates the file if it doesn't exist)
    conn = sqlite3.connect(db_name)
    
    # A cursor is used to execute SQL commands
    cursor = conn.cursor()
    
    # 1. Create a Table
    print("Creating a 'users' table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT
        )
    ''')
    
    # Clear the table in case the script is run multiple times
    cursor.execute('DELETE FROM users')
    
    # 2. Insert Data
    print("Inserting data into the table...")
    users_to_insert = [
        ('Alice', 28, 'alice@example.com'),
        ('Bob', 35, 'bob@example.com'),
        ('Charlie', 22, 'charlie@example.com')
    ]
    
    # Use executemany for inserting multiple rows efficiently
    # The '?' placeholders protect against SQL injection attacks!
    cursor.executemany('''
        INSERT INTO users (name, age, email)
        VALUES (?, ?, ?)
    ''', users_to_insert)
    
    # Commit (save) the changes to the database
    conn.commit()
    
    # 3. Query Data
    print("\n--- Querying the Database ---")
    print("Fetching all users older than 25:")
    
    # Execute a SELECT query
    cursor.execute('SELECT name, age, email FROM users WHERE age > 25')
    
    # Fetch all the results matching the query
    results = cursor.fetchall()
    
    for row in results:
        # row is a tuple containing the selected columns: (name, age, email)
        print(f"Name: {row[0]}, Age: {row[1]}, Email: {row[2]}")
        
    # Close the connection when done to free up resources
    conn.close()
    print("\nDatabase connection closed.")

if __name__ == "__main__":
    database_operations()
