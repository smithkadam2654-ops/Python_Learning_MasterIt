"""
Simple Database - In-memory database with SQL-like operations.
Features: Tables, indexes, queries, and transactions.
"""

import json
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ComparisonOperator(Enum):
    """Comparison operators."""
    EQ = "=="
    NE = "!="
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="
    LIKE = "LIKE"
    IN = "IN"


@dataclass
class Record:
    """Database record."""
    data: Dict[str, Any]
    id: int = 0
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value by key."""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set value by key."""
        self.data[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {"id": self.id, **self.data}


@dataclass
class Table:
    """Database table."""
    name: str
    columns: Dict[str, type] = field(default_factory=dict)
    records: List[Record] = field(default_factory=list)
    indexes: Dict[str, Dict[Any, List[int]]] = field(default_factory=dict)
    auto_increment: int = 1
    
    def insert(self, data: Dict[str, Any]) -> Record:
        """
        Insert record into table.
        
        Args:
            data: Record data
            
        Returns:
            Inserted record
        """
        record = Record(data.copy(), self.auto_increment)
        self.records.append(record)
        self.auto_increment += 1
        
        # Update indexes
        for column in self.indexes:
            if column in data:
                value = data[column]
                if value not in self.indexes[column]:
                    self.indexes[column][value] = []
                self.indexes[column][value].append(record.id)
        
        return record
    
    def select(self, where: Optional[Callable[[Record], bool]] = None) -> List[Record]:
        """
        Select records from table.
        
        Args:
            where: Optional filter function
            
        Returns:
            List of matching records
        """
        if where is None:
            return self.records.copy()
        
        return [record for record in self.records if where(record)]
    
    def update(self, where: Callable[[Record], bool], data: Dict[str, Any]) -> int:
        """
        Update records in table.
        
        Args:
            where: Filter function
            data: Data to update
            
        Returns:
            Number of updated records
        """
        count = 0
        for record in self.records:
            if where(record):
                for key, value in data.items():
                    record.set(key, value)
                count += 1
        return count
    
    def delete(self, where: Callable[[Record], bool]) -> int:
        """
        Delete records from table.
        
        Args:
            where: Filter function
            
        Returns:
            Number of deleted records
        """
        to_delete = [record for record in self.records if where(record)]
        for record in to_delete:
            self.records.remove(record)
            # Update indexes
            for column in self.indexes:
                for value, ids in self.indexes[column].items():
                    if record.id in ids:
                        ids.remove(record.id)
        return len(to_delete)
    
    def create_index(self, column: str) -> None:
        """
        Create index on column.
        
        Args:
            column: Column to index
        """
        self.indexes[column] = {}
        for record in self.records:
            value = record.get(column)
            if value not in self.indexes[column]:
                self.indexes[column][value] = []
            self.indexes[column][value].append(record.id)
    
    def count(self) -> int:
        """Get record count."""
        return len(self.records)
    
    def find_by_id(self, record_id: int) -> Optional[Record]:
        """
        Find record by ID.
        
        Args:
            record_id: Record ID
            
        Returns:
            Record or None
        """
        for record in self.records:
            if record.id == record_id:
                return record
        return None


class SimpleDatabase:
    """Simple in-memory database."""
    
    def __init__(self) -> None:
        """Initialize database."""
        self.tables: Dict[str, Table] = {}
        self._transactions: List[Dict] = []
        self._in_transaction = False
    
    def create_table(self, name: str, columns: Dict[str, type]) -> Table:
        """
        Create table.
        
        Args:
            name: Table name
            columns: Column definitions
            
        Returns:
            Created table
        """
        table = Table(name, columns)
        self.tables[name] = table
        return table
    
    def drop_table(self, name: str) -> bool:
        """
        Drop table.
        
        Args:
            name: Table name
            
        Returns:
            True if dropped
        """
        if name in self.tables:
            del self.tables[name]
            return True
        return False
    
    def get_table(self, name: str) -> Optional[Table]:
        """
        Get table by name.
        
        Args:
            name: Table name
            
        Returns:
            Table or None
        """
        return self.tables.get(name)
    
    def table_exists(self, name: str) -> bool:
        """Check if table exists."""
        return name in self.tables
    
    def begin_transaction(self) -> None:
        """Begin transaction."""
        if self._in_transaction:
            raise Exception("Transaction already in progress")
        
        self._in_transaction = True
        self._transactions.append({
            "tables": {name: self._serialize_table(table) for name, table in self.tables.items()}
        })
    
    def commit(self) -> None:
        """Commit transaction."""
        if not self._in_transaction:
            raise Exception("No transaction in progress")
        
        self._transactions.pop()
        self._in_transaction = False
    
    def rollback(self) -> None:
        """Rollback transaction."""
        if not self._in_transaction:
            raise Exception("No transaction in progress")
        
        state = self._transactions.pop()
        self._in_transaction = False
        
        # Restore tables
        for name, table_data in state["tables"].items():
            self.tables[name] = self._deserialize_table(table_data)
    
    def _serialize_table(self, table: Table) -> Dict:
        """Serialize table for transaction."""
        return {
            "name": table.name,
            "columns": table.columns,
            "records": [record.to_dict() for record in table.records],
            "auto_increment": table.auto_increment
        }
    
    def _deserialize_table(self, data: Dict) -> Table:
        """Deserialize table from transaction."""
        table = Table(data["name"], data["columns"])
        table.auto_increment = data["auto_increment"]
        
        for record_data in data["records"]:
            record_id = record_data.pop("id")
            record = Record(record_data, record_id)
            table.records.append(record)
        
        return table
    
    def join(self, table1: str, table2: str, 
             on: Callable[[Record, Record], bool]) -> List[Dict[str, Any]]:
        """
        Join two tables.
        
        Args:
            table1: First table name
            table2: Second table name
            on: Join condition function
            
        Returns:
            List of joined records
        """
        t1 = self.get_table(table1)
        t2 = self.get_table(table2)
        
        if not t1 or not t2:
            return []
        
        results = []
        for r1 in t1.records:
            for r2 in t2.records:
                if on(r1, r2):
                    results.append({**r1.to_dict(), **r2.to_dict()})
        
        return results
    
    def export_to_json(self) -> Dict:
        """
        Export database to JSON.
        
        Returns:
            Dictionary representation
        """
        return {
            "tables": {
                name: self._serialize_table(table)
                for name, table in self.tables.items()
            }
        }
    
    def import_from_json(self, data: Dict) -> None:
        """
        Import database from JSON.
        
        Args:
            data: Dictionary representation
        """
        self.tables.clear()
        
        for name, table_data in data.get("tables", {}).items():
            table = self._deserialize_table(table_data)
            self.tables[name] = table
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            "table_count": len(self.tables),
            "tables": {
                name: {
                    "record_count": table.count(),
                    "column_count": len(table.columns),
                    "index_count": len(table.indexes)
                }
                for name, table in self.tables.items()
            }
        }


def main() -> None:
    """Demonstrate simple database."""
    
    print("=== Simple Database Demo ===")
    
    db = SimpleDatabase()
    
    # Create tables
    users = db.create_table("users", {
        "name": str,
        "email": str,
        "age": int
    })
    
    orders = db.create_table("orders", {
        "user_id": int,
        "product": str,
        "amount": float
    })
    
    # Insert data
    users.insert({"name": "Alice", "email": "alice@example.com", "age": 30})
    users.insert({"name": "Bob", "email": "bob@example.com", "age": 25})
    users.insert({"name": "Charlie", "email": "charlie@example.com", "age": 35})
    
    orders.insert({"user_id": 1, "product": "Laptop", "amount": 999.99})
    orders.insert({"user_id": 1, "product": "Mouse", "amount": 29.99})
    orders.insert({"user_id": 2, "product": "Keyboard", "amount": 79.99})
    
    print(f"Users: {users.count()}")
    print(f"Orders: {orders.count()}")
    
    # Select with filter
    print("\n--- Users over 30 ---")
    old_users = users.select(lambda r: r.get("age") > 30)
    for user in old_users:
        print(f"  {user.to_dict()}")
    
    # Update
    print("\n--- Update Bob's age ---")
    count = users.update(lambda r: r.get("name") == "Bob", {"age": 26})
    print(f"Updated {count} records")
    
    # Delete
    print("\n--- Delete Charlie ---")
    count = users.delete(lambda r: r.get("name") == "Charlie")
    print(f"Deleted {count} records")
    
    # Join
    print("\n--- Join users and orders ---")
    joined = db.join("users", "orders", 
                    lambda u, o: u.id == o.get("user_id"))
    for record in joined:
        print(f"  {record}")
    
    # Create index
    print("\n--- Create index on email ---")
    users.create_index("email")
    print(f"Indexes: {list(users.indexes.keys())}")
    
    # Transaction
    print("\n--- Transaction Demo ---")
    db.begin_transaction()
    
    users.insert({"name": "David", "email": "david@example.com", "age": 40})
    print(f"Users in transaction: {users.count()}")
    
    db.rollback()
    print(f"Users after rollback: {users.count()}")
    
    db.begin_transaction()
    
    users.insert({"name": "Eve", "email": "eve@example.com", "age": 28})
    print(f"Users in transaction: {users.count()}")
    
    db.commit()
    print(f"Users after commit: {users.count()}")
    
    # Statistics
    print("\n--- Database Statistics ---")
    stats = db.get_statistics()
    print(f"Table count: {stats['table_count']}")
    for name, table_stats in stats['tables'].items():
        print(f"  {name}:")
        print(f"    Records: {table_stats['record_count']}")
        print(f"    Columns: {table_stats['column_count']}")
        print(f"    Indexes: {table_stats['index_count']}")
    
    # Export/Import
    print("\n--- Export/Import ---")
    exported = db.export_to_json()
    print(f"Exported data: {list(exported['tables'].keys())}")
    
    new_db = SimpleDatabase()
    new_db.import_from_json(exported)
    print(f"Imported tables: {list(new_db.tables.keys())}")


if __name__ == "__main__":
    main()
