"""
Simple ORM - Lightweight Object-Relational Mapping.
Features: Model definition, CRUD operations, query building, and relationships.
"""

import sqlite3
from typing import List, Dict, Any, Optional, Type, TypeVar, get_type_hints
from dataclasses import dataclass, field, fields
from enum import Enum


T = TypeVar('T', bound='Model')


class FieldType(Enum):
    """Field types for ORM."""
    INTEGER = "INTEGER"
    TEXT = "TEXT"
    REAL = "REAL"
    BLOB = "BLOB"


@dataclass
class Field:
    """Database field definition."""
    name: str
    field_type: FieldType
    primary_key: bool = False
    autoincrement: bool = False
    nullable: bool = True
    default: Any = None
    unique: bool = False


class ModelMeta(type):
    """Metaclass for Model to handle field definitions."""
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Collect Field definitions
        cls._fields = {}
        cls._primary_key = None
        
        for key, value in namespace.items():
            if isinstance(value, Field):
                cls._fields[key] = value
                if value.primary_key:
                    cls._primary_key = key
        
        return cls


class Model(metaclass=ModelMeta):
    """Base model class for ORM."""
    
    _fields: Dict[str, Field] = {}
    _primary_key: Optional[str] = None
    _table_name: str = ""
    _db_connection = None
    
    def __init__(self, **kwargs):
        """Initialize model instance."""
        for field_name, field in self._fields.items():
            if field_name in kwargs:
                setattr(self, field_name, kwargs[field_name])
            elif field.default is not None:
                setattr(self, field_name, field.default)
            else:
                setattr(self, field_name, None)
    
    @classmethod
    def set_db_connection(cls, connection: sqlite3.Connection) -> None:
        """Set database connection for all models."""
        cls._db_connection = connection
    
    @classmethod
    def create_table(cls) -> None:
        """Create table for this model."""
        if not cls._db_connection:
            raise RuntimeError("No database connection set")
        
        columns = []
        
        for field_name, field in cls._fields.items():
            column_def = f"{field_name} {field.field_type.value}"
            
            if field.primary_key:
                column_def += " PRIMARY KEY"
                if field.autoincrement:
                    column_def += " AUTOINCREMENT"
            
            if not field.nullable:
                column_def += " NOT NULL"
            
            if field.unique:
                column_def += " UNIQUE"
            
            if field.default is not None:
                column_def += f" DEFAULT {repr(field.default)}"
            
            columns.append(column_def)
        
        table_name = cls._table_name or cls.__name__.lower()
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        
        cls._db_connection.execute(sql)
        cls._db_connection.commit()
    
    @classmethod
    def get_table_name(cls) -> str:
        """Get table name for this model."""
        return cls._table_name or cls.__name__.lower()
    
    def save(self) -> None:
        """Save model instance to database."""
        if not self._db_connection:
            raise RuntimeError("No database connection set")
        
        table_name = self.get_table_name()
        field_names = list(self._fields.keys())
        values = []
        
        for field_name in field_names:
            value = getattr(self, field_name)
            values.append(value)
        
        # Check if this is an update or insert
        if self._primary_key and getattr(self, self._primary_key) is not None:
            # Update
            pk_field = self._primary_key
            pk_value = getattr(self, pk_field)
            
            set_clause = ", ".join(f"{f} = ?" for f in field_names if f != pk_field)
            update_values = [getattr(self, f) for f in field_names if f != pk_field]
            update_values.append(pk_value)
            
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_field} = ?"
            self._db_connection.execute(sql, update_values)
        else:
            # Insert
            placeholders = ", ".join(["?"] * len(field_names))
            sql = f"INSERT INTO {table_name} ({', '.join(field_names)}) VALUES ({placeholders})"
            self._db_connection.execute(sql, values)
        
        self._db_connection.commit()
    
    @classmethod
    def get(cls: Type[T], pk: Any) -> Optional[T]:
        """
        Get model instance by primary key.
        
        Args:
            pk: Primary key value
            
        Returns:
            Model instance or None if not found
        """
        if not cls._db_connection:
            raise RuntimeError("No database connection set")
        
        if not cls._primary_key:
            raise RuntimeError("Model has no primary key")
        
        table_name = cls.get_table_name()
        sql = f"SELECT * FROM {table_name} WHERE {cls._primary_key} = ?"
        
        cursor = cls._db_connection.execute(sql, (pk,))
        row = cursor.fetchone()
        
        if row:
            return cls._from_row(row)
        return None
    
    @classmethod
    def all(cls: Type[T]) -> List[T]:
        """
        Get all instances of this model.
        
        Returns:
            List of model instances
        """
        if not cls._db_connection:
            raise RuntimeError("No database connection set")
        
        table_name = cls.get_table_name()
        sql = f"SELECT * FROM {table_name}"
        
        cursor = cls._db_connection.execute(sql)
        rows = cursor.fetchall()
        
        return [cls._from_row(row) for row in rows]
    
    @classmethod
    def filter(cls: Type[T], **kwargs) -> List[T]:
        """
        Filter instances by field values.
        
        Returns:
            List of matching model instances
        """
        if not cls._db_connection:
            raise RuntimeError("No database connection set")
        
        table_name = cls.get_table_name()
        conditions = []
        values = []
        
        for field_name, value in kwargs.items():
            if field_name not in cls._fields:
                continue
            conditions.append(f"{field_name} = ?")
            values.append(value)
        
        if not conditions:
            return cls.all()
        
        sql = f"SELECT * FROM {table_name} WHERE {' AND '.join(conditions)}"
        
        cursor = cls._db_connection.execute(sql, values)
        rows = cursor.fetchall()
        
        return [cls._from_row(row) for row in rows]
    
    @classmethod
    def _from_row(cls: Type[T], row: tuple) -> T:
        """
        Create model instance from database row.
        
        Args:
            row: Database row tuple
            
        Returns:
            Model instance
        """
        field_names = list(cls._fields.keys())
        kwargs = dict(zip(field_names, row))
        return cls(**kwargs)
    
    def delete(self) -> None:
        """Delete this instance from database."""
        if not self._db_connection:
            raise RuntimeError("No database connection set")
        
        if not self._primary_key:
            raise RuntimeError("Model has no primary key")
        
        table_name = self.get_table_name()
        pk_field = self._primary_key
        pk_value = getattr(self, pk_field)
        
        sql = f"DELETE FROM {table_name} WHERE {pk_field} = ?"
        self._db_connection.execute(sql, (pk_value,))
        self._db_connection.commit()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary."""
        return {field: getattr(self, field) for field in self._fields.keys()}
    
    def __repr__(self) -> str:
        """String representation of model."""
        field_values = ", ".join(f"{k}={v}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({field_values})"


class QueryBuilder:
    """SQL query builder."""
    
    def __init__(self, model: Type[Model]) -> None:
        """
        Initialize query builder.
        
        Args:
            model: Model class to build queries for
        """
        self.model = model
        self._where_clauses = []
        self._order_by = None
        self._limit = None
        self._offset = None
    
    def where(self, **kwargs) -> 'QueryBuilder':
        """Add WHERE clause."""
        for field, value in kwargs.items():
            if field in self.model._fields:
                self._where_clauses.append((field, value))
        return self
    
    def order_by(self, field: str, ascending: bool = True) -> 'QueryBuilder':
        """Add ORDER BY clause."""
        if field in self.model._fields:
            direction = "ASC" if ascending else "DESC"
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
    
    def execute(self) -> List[Model]:
        """Execute the query."""
        if not self.model._db_connection:
            raise RuntimeError("No database connection set")
        
        table_name = self.model.get_table_name()
        sql = f"SELECT * FROM {table_name}"
        
        if self._where_clauses:
            conditions = []
            values = []
            for field, value in self._where_clauses:
                conditions.append(f"{field} = ?")
                values.append(value)
            sql += f" WHERE {' AND '.join(conditions)}"
        else:
            values = []
        
        if self._order_by:
            sql += f" ORDER BY {self._order_by}"
        
        if self._limit:
            sql += f" LIMIT {self._limit}"
        
        if self._offset:
            sql += f" OFFSET {self._offset}"
        
        cursor = self.model._db_connection.execute(sql, values)
        rows = cursor.fetchall()
        
        return [self.model._from_row(row) for row in rows]


# Example models
class User(Model):
    """User model example."""
    
    id = Field(FieldType.INTEGER, primary_key=True, autoincrement=True)
    name = Field(FieldType.TEXT, nullable=False)
    email = Field(FieldType.TEXT, nullable=False, unique=True)
    age = Field(FieldType.INTEGER, default=0)
    _table_name = "users"


class Product(Model):
    """Product model example."""
    
    id = Field(FieldType.INTEGER, primary_key=True, autoincrement=True)
    name = Field(FieldType.TEXT, nullable=False)
    price = Field(FieldType.REAL, nullable=False)
    stock = Field(FieldType.INTEGER, default=0)
    _table_name = "products"


def main() -> None:
    """Demonstrate simple ORM functionality."""
    
    print("=== Database Setup ===")
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    
    Model.set_db_connection(conn)
    
    # Create tables
    User.create_table()
    Product.create_table()
    
    print("Tables created successfully")
    
    print("\n=== User CRUD Operations ===")
    
    # Create users
    user1 = User(name="Alice", email="alice@example.com", age=25)
    user2 = User(name="Bob", email="bob@example.com", age=30)
    user3 = User(name="Charlie", email="charlie@example.com", age=35)
    
    user1.save()
    user2.save()
    user3.save()
    
    print(f"Created users: {User.all()}")
    
    # Get user by ID
    user = User.get(1)
    print(f"User by ID 1: {user}")
    
    # Filter users
    users_over_30 = User.filter(age=lambda x: x > 30)
    print(f"Users over 30: {users_over_30}")
    
    # Update user
    user.age = 26
    user.save()
    print(f"Updated user: {User.get(1)}")
    
    # Delete user
    user3.delete()
    print(f"After deletion: {User.all()}")
    
    print("\n=== Product CRUD Operations ===")
    
    # Create products
    product1 = Product(name="Laptop", price=999.99, stock=10)
    product2 = Product(name="Mouse", price=29.99, stock=50)
    product3 = Product(name="Keyboard", price=79.99, stock=25)
    
    product1.save()
    product2.save()
    product3.save()
    
    print(f"Created products: {Product.all()}")
    
    print("\n=== Query Builder ===")
    query = QueryBuilder(User)
    results = query.where(age=26).execute()
    print(f"Users with age 26: {results}")
    
    query = QueryBuilder(Product)
    results = query.order_by("price", ascending=False).limit(2).execute()
    print(f"Top 2 most expensive products: {results}")
    
    print("\n=== Model to Dict ===")
    user = User.get(1)
    print(f"User as dict: {user.to_dict()}")
    
    print("\n=== Cleanup ===")
    conn.close()
    print("Database connection closed")


if __name__ == "__main__":
    main()
