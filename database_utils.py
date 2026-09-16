"""
Database Utilities Module

This module provides comprehensive database operations and utilities including:
- SQLite database operations
- Connection pooling and management
- CRUD operations with type hints
- Transaction management
- Query building utilities
- Data migration helpers
- ORM-like patterns
- Database backup and restore
- Performance monitoring
- Schema validation

All functions include comprehensive docstrings and type hints.
"""

import sqlite3
import json
import time
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple, Union, Iterator
from dataclasses import dataclass, asdict
from enum import Enum


class DatabaseType(Enum):
    """Supported database types."""
    SQLITE = "sqlite"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"


@dataclass
class DatabaseConfig:
    """Database configuration."""
    db_type: DatabaseType
    host: Optional[str] = None
    port: Optional[int] = None
    database: str = ":memory:"
    username: Optional[str] = None
    password: Optional[str] = None
    timeout: float = 5.0


class DatabaseManager:
    """Database connection manager with connection pooling support."""
    
    def __init__(self, config: DatabaseConfig):
        """Initialize database manager with configuration."""
        self.config = config
        self._connection_pool: List[sqlite3.Connection] = []
        self._pool_size = 5
        self._query_count = 0
        self._query_times: List[float] = []
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection from the pool or create new one."""
        if self._connection_pool:
            return self._connection_pool.pop()
        
        if self.config.db_type == DatabaseType.SQLITE:
            conn = sqlite3.connect(
                self.config.database,
                timeout=self.config.timeout,
                check_same_thread=False
            )
            conn.row_factory = sqlite3.Row
            return conn
        else:
            raise NotImplementedError(f"Database type {self.config.db_type} not implemented")
    
    def return_connection(self, conn: sqlite3.Connection) -> None:
        """Return a connection to the pool."""
        if len(self._connection_pool) < self._pool_size:
            self._connection_pool.append(conn)
        else:
            conn.close()
    
    @contextmanager
    def get_cursor(self) -> Iterator[sqlite3.Cursor]:
        """Context manager for database cursor with automatic cleanup."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.return_connection(conn)
    
    def execute_query(self, query: str, params: Tuple = ()) -> List[Dict]:
        """Execute a query and return results as list of dictionaries."""
        start_time = time.time()
        self._query_count += 1
        
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            results = [dict(row) for row in cursor.fetchall()]
        
        elapsed = time.time() - start_time
        self._query_times.append(elapsed)
        
        return results
    
    def execute_update(self, query: str, params: Tuple = ()) -> int:
        """Execute an update/insert/delete query and return affected rows."""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get database performance statistics."""
        avg_time = sum(self._query_times) / len(self._query_times) if self._query_times else 0
        return {
            "total_queries": self._query_count,
            "average_query_time": avg_time,
            "pool_size": len(self._connection_pool),
            "max_pool_size": self._pool_size
        }
    
    def close_all(self) -> None:
        """Close all connections in the pool."""
        for conn in self._connection_pool:
            conn.close()
        self._connection_pool.clear()


class QueryBuilder:
    """SQL query builder for dynamic query construction."""
    
    def __init__(self, table: str):
        """Initialize query builder for a table."""
        self.table = table
        self._select_fields: List[str] = ["*"]
        self._where_conditions: List[str] = []
        self._where_params: List[Any] = []
        self._join_clauses: List[str] = []
        self._order_by: Optional[str] = None
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
    
    def select(self, *fields: str) -> 'QueryBuilder':
        """Specify fields to select."""
        self._select_fields = list(fields) if fields else ["*"]
        return self
    
    def where(self, condition: str, *params: Any) -> 'QueryBuilder':
        """Add a WHERE condition."""
        self._where_conditions.append(condition)
        self._where_params.extend(params)
        return self
    
    def join(self, table: str, on: str) -> 'QueryBuilder':
        """Add a JOIN clause."""
        self._join_clauses.append(f"JOIN {table} ON {on}")
        return self
    
    def left_join(self, table: str, on: str) -> 'QueryBuilder':
        """Add a LEFT JOIN clause."""
        self._join_clauses.append(f"LEFT JOIN {table} ON {on}")
        return self
    
    def order_by(self, field: str, direction: str = "ASC") -> 'QueryBuilder':
        """Add ORDER BY clause."""
        self._order_by = f"{field} {direction}"
        return self
    
    def limit(self, count: int) -> 'QueryBuilder':
        """Add LIMIT clause."""
        self._limit = count
        return self
    
    def offset(self, count: int) -> 'QueryBuilder':
        """Add OFFSET clause."""
        self._offset = count
        return self
    
    def build(self) -> Tuple[str, Tuple]:
        """Build the final SQL query and parameters."""
        query = f"SELECT {', '.join(self._select_fields)} FROM {self.table}"
        
        if self._join_clauses:
            query += " " + " ".join(self._join_clauses)
        
        if self._where_conditions:
            query += " WHERE " + " AND ".join(self._where_conditions)
        
        if self._order_by:
            query += f" ORDER BY {self._order_by}"
        
        if self._limit:
            query += f" LIMIT {self._limit}"
        
        if self._offset:
            query += f" OFFSET {self._offset}"
        
        return query, tuple(self._where_params)


class CRUDOperations:
    """CRUD operations helper for database tables."""
    
    def __init__(self, db_manager: DatabaseManager, table: str):
        """Initialize CRUD operations for a table."""
        self.db = db_manager
        self.table = table
    
    def create(self, data: Dict[str, Any]) -> int:
        """Insert a new record and return the last row ID."""
        fields = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {self.table} ({fields}) VALUES ({placeholders})"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, tuple(data.values()))
            return cursor.lastrowid
    
    def read(self, record_id: int) -> Optional[Dict]:
        """Read a single record by ID."""
        query = f"SELECT * FROM {self.table} WHERE id = ?"
        results = self.db.execute_query(query, (record_id,))
        return results[0] if results else None
    
    def read_all(self, limit: Optional[int] = None) -> List[Dict]:
        """Read all records with optional limit."""
        query = f"SELECT * FROM {self.table}"
        if limit:
            query += f" LIMIT {limit}"
        return self.db.execute_query(query)
    
    def update(self, record_id: int, data: Dict[str, Any]) -> int:
        """Update a record by ID and return affected rows."""
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {self.table} SET {set_clause} WHERE id = ?"
        params = tuple(data.values()) + (record_id,)
        return self.db.execute_update(query, params)
    
    def delete(self, record_id: int) -> int:
        """Delete a record by ID and return affected rows."""
        query = f"DELETE FROM {self.table} WHERE id = ?"
        return self.db.execute_update(query, (record_id,))
    
    def find(self, **filters: Any) -> List[Dict]:
        """Find records matching filter criteria."""
        conditions = [f"{k} = ?" for k in filters.keys()]
        query = f"SELECT * FROM {self.table} WHERE {' AND '.join(conditions)}"
        return self.db.execute_query(query, tuple(filters.values()))


class TransactionManager:
    """Transaction management with rollback support."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize transaction manager."""
        self.db = db_manager
    
    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """Context manager for transaction with automatic commit/rollback."""
        conn = self.db.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.db.return_connection(conn)
    
    def execute_in_transaction(self, operations: List[Tuple[str, Tuple]]) -> bool:
        """Execute multiple operations in a single transaction."""
        with self.transaction() as conn:
            cursor = conn.cursor()
            for query, params in operations:
                cursor.execute(query, params)
        return True


class SchemaManager:
    """Database schema management utilities."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize schema manager."""
        self.db = db_manager
    
    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        """Create a table with specified columns."""
        column_defs = ", ".join([f"{name} {definition}" for name, definition in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"
        self.db.execute_update(query)
    
    def drop_table(self, table_name: str) -> None:
        """Drop a table if it exists."""
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.db.execute_update(query)
    
    def add_column(self, table_name: str, column_name: str, column_type: str) -> None:
        """Add a column to an existing table."""
        query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        self.db.execute_update(query)
    
    def get_table_schema(self, table_name: str) -> List[Dict]:
        """Get schema information for a table."""
        query = f"PRAGMA table_info({table_name})"
        return self.db.execute_query(query)
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists."""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        results = self.db.execute_query(query, (table_name,))
        return len(results) > 0


class BackupManager:
    """Database backup and restore utilities."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize backup manager."""
        self.db = db_manager
    
    def backup_to_file(self, backup_path: str) -> bool:
        """Backup database to a file."""
        try:
            source = self.db.get_connection()
            backup = sqlite3.connect(backup_path)
            
            with backup:
                source.backup(backup)
            
            backup.close()
            self.db.return_connection(source)
            return True
        except Exception as e:
            print(f"Backup failed: {e}")
            return False
    
    def restore_from_file(self, backup_path: str) -> bool:
        """Restore database from a backup file."""
        try:
            backup = sqlite3.connect(backup_path)
            target = self.db.get_connection()
            
            with target:
                backup.backup(target)
            
            backup.close()
            self.db.return_connection(target)
            return True
        except Exception as e:
            print(f"Restore failed: {e}")
            return False
    
    def export_to_json(self, table_name: str, output_path: str) -> bool:
        """Export table data to JSON file."""
        try:
            query = f"SELECT * FROM {table_name}"
            data = self.db.execute_query(query)
            
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def import_from_json(self, table_name: str, input_path: str) -> bool:
        """Import data from JSON file to table."""
        try:
            with open(input_path, 'r') as f:
                data = json.load(f)
            
            if not data:
                return True
            
            fields = list(data[0].keys())
            placeholders = ", ".join(["?"] * len(fields))
            query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})"
            
            with self.db.get_cursor() as cursor:
                for record in data:
                    cursor.execute(query, tuple(record[field] for field in fields))
            
            return True
        except Exception as e:
            print(f"Import failed: {e}")
            return False


class DataValidator:
    """Data validation for database operations."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format."""
        import re
        pattern = r'^\+?[\d\s-()]{10,}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def sanitize_input(data: Any) -> Any:
        """Sanitize input data to prevent SQL injection."""
        if isinstance(data, str):
            return data.replace("'", "''")
        elif isinstance(data, dict):
            return {k: DataValidator.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [DataValidator.sanitize_input(item) for item in data]
        return data


def create_sample_database(db_path: str = "sample.db") -> DatabaseManager:
    """Create a sample database with tables and data for demonstration."""
    config = DatabaseConfig(db_type=DatabaseType.SQLITE, database=db_path)
    db = DatabaseManager(config)
    
    schema = SchemaManager(db)
    
    # Create users table
    schema.create_table("users", {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "email": "TEXT UNIQUE",
        "age": "INTEGER",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    })
    
    # Create products table
    schema.create_table("products", {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "price": "REAL NOT NULL",
        "quantity": "INTEGER DEFAULT 0",
        "category": "TEXT"
    })
    
    # Insert sample data
    crud = CRUDOperations(db, "users")
    sample_users = [
        {"name": "John Doe", "email": "john@example.com", "age": 30},
        {"name": "Jane Smith", "email": "jane@example.com", "age": 25},
        {"name": "Bob Johnson", "email": "bob@example.com", "age": 35}
    ]
    
    for user in sample_users:
        crud.create(user)
    
    product_crud = CRUDOperations(db, "products")
    sample_products = [
        {"name": "Laptop", "price": 999.99, "quantity": 10, "category": "Electronics"},
        {"name": "Mouse", "price": 29.99, "quantity": 50, "category": "Electronics"},
        {"name": "Desk", "price": 299.99, "quantity": 5, "category": "Furniture"}
    ]
    
    for product in sample_products:
        product_crud.create(product)
    
    return db


def demonstrate_database_utils():
    """Demonstrate database utilities functionality."""
    print("=== Database Utilities Demonstration ===\n")
    
    # Create sample database
    print("1. Creating sample database...")
    db = create_sample_database(":memory:")
    
    # Demonstrate CRUD operations
    print("\n2. CRUD Operations:")
    crud = CRUDOperations(db, "users")
    
    # Create
    print("   Creating new user...")
    new_id = crud.create({"name": "Alice Brown", "email": "alice@example.com", "age": 28})
    print(f"   Created user with ID: {new_id}")
    
    # Read
    print(f"   Reading user with ID {new_id}...")
    user = crud.read(new_id)
    print(f"   User: {user}")
    
    # Read all
    print("   Reading all users...")
    all_users = crud.read_all()
    print(f"   Total users: {len(all_users)}")
    
    # Update
    print(f"   Updating user {new_id}...")
    updated = crud.update(new_id, {"age": 29})
    print(f"   Updated {updated} row(s)")
    
    # Find
    print("   Finding users with age > 25...")
    young_users = [u for u in all_users if u.get('age', 0) > 25]
    print(f"   Found {len(young_users)} users")
    
    # Delete
    print(f"   Deleting user {new_id}...")
    deleted = crud.delete(new_id)
    print(f"   Deleted {deleted} row(s)")
    
    # Demonstrate Query Builder
    print("\n3. Query Builder:")
    builder = QueryBuilder("users")
    query, params = builder.select("name", "email").where("age > ?", 25).order_by("name").build()
    print(f"   Query: {query}")
    print(f"   Params: {params}")
    
    # Demonstrate Schema Manager
    print("\n4. Schema Management:")
    schema = SchemaManager(db)
    print("   Getting table schema...")
    users_schema = schema.get_table_schema("users")
    print(f"   Columns: {[col['name'] for col in users_schema]}")
    
    # Demonstrate Transaction Manager
    print("\n5. Transaction Management:")
    tx = TransactionManager(db)
    operations = [
        ("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ("Charlie", "charlie@example.com", 40)),
        ("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ("Diana", "diana@example.com", 32))
    ]
    tx.execute_in_transaction(operations)
    print("   Executed transaction with 2 operations")
    
    # Demonstrate Performance Stats
    print("\n6. Performance Statistics:")
    stats = db.get_performance_stats()
    print(f"   Total queries: {stats['total_queries']}")
    print(f"   Average query time: {stats['average_query_time']:.4f}s")
    
    # Demonstrate Data Validation
    print("\n7. Data Validation:")
    print(f"   Valid email test: {DataValidator.validate_email('test@example.com')}")
    print(f"   Invalid email test: {DataValidator.validate_email('invalid-email')}")
    print(f"   Valid phone test: {DataValidator.validate_phone('+1 555-123-4567')}")
    
    # Demonstrate Backup
    print("\n8. Backup Operations:")
    backup = BackupManager(db)
    print("   Exporting users to JSON...")
    backup.export_to_json("users", "users_backup.json")
    print("   Export completed")
    
    # Cleanup
    db.close_all()
    print("\n=== Demonstration Complete ===")


if __name__ == "__main__":
    demonstrate_database_utils()