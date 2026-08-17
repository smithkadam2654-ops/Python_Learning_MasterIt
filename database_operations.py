"""
Database Operations - SQLite database operations and ORM patterns.
Features: CRUD operations, query building, and data management.
"""

import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from contextlib import contextmanager


@dataclass
class User:
    """User model for database operations."""
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    age: int = 0


class DatabaseManager:
    """SQLite database manager with connection pooling."""
    
    def __init__(self, db_path: str = ":memory:") -> None:
        """
        Initialize database manager.
        
        Args:
            db_path: Path to database file (":memory:" for in-memory)
        """
        self.db_path = db_path
        self._init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_database(self) -> None:
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    age INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER DEFAULT 0
                )
            """)
    
    def execute_query(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """
        Execute a SELECT query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of result rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: Tuple = ()) -> int:
        """
        Execute an INSERT/UPDATE/DELETE query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    
    def insert_user(self, user: User) -> int:
        """
        Insert a new user into the database.
        
        Args:
            user: User object to insert
            
        Returns:
            ID of inserted user
        """
        query = "INSERT INTO users (name, email, age) VALUES (?, ?, ?)"
        params = (user.name, user.email, user.age)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve user by ID.
        
        Args:
            user_id: User ID to retrieve
            
        Returns:
            User object or None if not found
        """
        query = "SELECT id, name, email, age FROM users WHERE id = ?"
        rows = self.execute_query(query, (user_id,))
        
        if rows:
            row = rows[0]
            return User(row["id"], row["name"], row["email"], row["age"])
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve user by email.
        
        Args:
            email: User email to retrieve
            
        Returns:
            User object or None if not found
        """
        query = "SELECT id, name, email, age FROM users WHERE email = ?"
        rows = self.execute_query(query, (email,))
        
        if rows:
            row = rows[0]
            return User(row["id"], row["name"], row["email"], row["age"])
        return None
    
    def get_all_users(self) -> List[User]:
        """
        Retrieve all users from database.
        
        Returns:
            List of User objects
        """
        query = "SELECT id, name, email, age FROM users"
        rows = self.execute_query(query)
        
        return [User(row["id"], row["name"], row["email"], row["age"]) for row in rows]
    
    def update_user(self, user: User) -> bool:
        """
        Update an existing user.
        
        Args:
            user: User object with updated data
            
        Returns:
            True if update successful, False otherwise
        """
        if user.id is None:
            return False
        
        query = "UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?"
        params = (user.name, user.email, user.age, user.id)
        
        affected = self.execute_update(query, params)
        return affected > 0
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by ID.
        
        Args:
            user_id: User ID to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        query = "DELETE FROM users WHERE id = ?"
        affected = self.execute_update(query, (user_id,))
        return affected > 0
    
    def search_users(self, name_pattern: str) -> List[User]:
        """
        Search users by name pattern.
        
        Args:
            name_pattern: Pattern to search for (LIKE syntax)
            
        Returns:
            List of matching User objects
        """
        query = "SELECT id, name, email, age FROM users WHERE name LIKE ?"
        rows = self.execute_query(query, (f"%{name_pattern}%",))
        
        return [User(row["id"], row["name"], row["email"], row["age"]) for row in rows]
    
    def get_user_count(self) -> int:
        """
        Get total number of users.
        
        Returns:
            Number of users in database
        """
        query = "SELECT COUNT(*) as count FROM users"
        rows = self.execute_query(query)
        return rows[0]["count"] if rows else 0
    
    def get_average_age(self) -> float:
        """
        Get average age of all users.
        
        Returns:
            Average age
        """
        query = "SELECT AVG(age) as avg_age FROM users"
        rows = self.execute_query(query)
        return rows[0]["avg_age"] if rows and rows[0]["avg_age"] else 0.0


class QueryBuilder:
    """SQL query builder for dynamic queries."""
    
    def __init__(self, table: str) -> None:
        """
        Initialize query builder.
        
        Args:
            table: Table name to query
        """
        self.table = table
        self._select_columns = ["*"]
        self._where_conditions = []
        self._order_by = None
        self._limit = None
        self._offset = None
    
    def select(self, *columns: str) -> 'QueryBuilder':
        """Specify columns to select."""
        self._select_columns = list(columns) if columns else ["*"]
        return self
    
    def where(self, condition: str, params: Tuple = ()) -> 'QueryBuilder':
        """Add WHERE condition."""
        self._where_conditions.append((condition, params))
        return self
    
    def order_by(self, column: str, ascending: bool = True) -> 'QueryBuilder':
        """Add ORDER BY clause."""
        direction = "ASC" if ascending else "DESC"
        self._order_by = f"{column} {direction}"
        return self
    
    def limit(self, limit: int) -> 'QueryBuilder':
        """Add LIMIT clause."""
        self._limit = limit
        return self
    
    def offset(self, offset: int) -> 'QueryBuilder':
        """Add OFFSET clause."""
        self._offset = offset
        return self
    
    def build(self) -> Tuple[str, Tuple]:
        """Build the final query and parameters."""
        query = f"SELECT {', '.join(self._select_columns)} FROM {self.table}"
        params = []
        
        if self._where_conditions:
            conditions = []
            for condition, cond_params in self._where_conditions:
                conditions.append(condition)
                params.extend(cond_params)
            query += " WHERE " + " AND ".join(conditions)
        
        if self._order_by:
            query += f" ORDER BY {self._order_by}"
        
        if self._limit:
            query += f" LIMIT {self._limit}"
        
        if self._offset:
            query += f" OFFSET {self._offset}"
        
        return query, tuple(params)


class TransactionManager:
    """Manager for database transactions."""
    
    def __init__(self, db_manager: DatabaseManager) -> None:
        """
        Initialize transaction manager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager
    
    def execute_in_transaction(self, operations: List[Tuple[str, Tuple]]) -> bool:
        """
        Execute multiple operations in a single transaction.
        
        Args:
            operations: List of (query, params) tuples
            
        Returns:
            True if all operations succeeded, False otherwise
        """
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                for query, params in operations:
                    cursor.execute(query, params)
            return True
        except Exception:
            return False


def main() -> None:
    """Demonstrate database operations."""
    
    print("=== Database Initialization ===")
    db = DatabaseManager(":memory:")
    print("Database initialized")
    
    print("\n=== Insert Users ===")
    users = [
        User(name="Alice", email="alice@example.com", age=25),
        User(name="Bob", email="bob@example.com", age=30),
        User(name="Charlie", email="charlie@example.com", age=35),
    ]
    
    for user in users:
        user_id = db.insert_user(user)
        print(f"Inserted {user.name} with ID: {user_id}")
    
    print("\n=== Retrieve Users ===")
    user = db.get_user_by_id(1)
    if user:
        print(f"User by ID 1: {user.name}, {user.email}, {user.age}")
    
    user = db.get_user_by_email("bob@example.com")
    if user:
        print(f"User by email: {user.name}, {user.email}, {user.age}")
    
    print("\n=== Get All Users ===")
    all_users = db.get_all_users()
    for user in all_users:
        print(f"  {user.id}: {user.name} ({user.email}) - Age: {user.age}")
    
    print("\n=== Update User ===")
    user = db.get_user_by_id(1)
    if user:
        user.age = 26
        success = db.update_user(user)
        print(f"Update successful: {success}")
        print(f"Updated user: {db.get_user_by_id(1)}")
    
    print("\n=== Search Users ===")
    results = db.search_users("a")
    print(f"Users matching 'a': {[u.name for u in results]}")
    
    print("\n=== Statistics ===")
    print(f"Total users: {db.get_user_count()}")
    print(f"Average age: {db.get_average_age():.1f}")
    
    print("\n=== Query Builder ===")
    builder = QueryBuilder("users")
    query, params = builder.select("name", "age").where("age > ?", (25,)).order_by("age").build()
    print(f"Built query: {query}")
    print(f"Parameters: {params}")
    
    print("\n=== Transaction ===")
    tx_manager = TransactionManager(db)
    operations = [
        ("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ("David", "david@example.com", 40)),
        ("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ("Eve", "eve@example.com", 28)),
    ]
    success = tx_manager.execute_in_transaction(operations)
    print(f"Transaction successful: {success}")
    print(f"Total users after transaction: {db.get_user_count()}")
    
    print("\n=== Delete User ===")
    success = db.delete_user(1)
    print(f"Delete successful: {success}")
    print(f"Total users after deletion: {db.get_user_count()}")


if __name__ == "__main__":
    main()
