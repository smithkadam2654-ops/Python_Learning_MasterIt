"""
Hash Table - Implementation of hash table with collision handling.
Features: Separate chaining, dynamic resizing, and common operations.
"""

from typing import Optional, Any, List, Tuple
from dataclasses import dataclass


@dataclass
class HashEntry:
    """Entry for hash table bucket."""
    key: Any
    value: Any
    next: Optional['HashEntry'] = None


class HashTable:
    """Hash table implementation with separate chaining."""
    
    def __init__(self, initial_capacity: int = 16, load_factor: float = 0.75) -> None:
        """
        Initialize hash table.
        
        Args:
            initial_capacity: Starting capacity of the table
            load_factor: Threshold for resizing (0.0 - 1.0)
        """
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets: List[Optional[HashEntry]] = [None] * self.capacity
    
    def _hash(self, key: Any) -> int:
        """
        Compute hash value for a key.
        
        Args:
            key: Key to hash
            
        Returns:
            Hash value (bucket index)
        """
        if isinstance(key, int):
            return abs(key) % self.capacity
        elif isinstance(key, str):
            hash_value = 0
            for char in key:
                hash_value = (hash_value * 31 + ord(char)) % self.capacity
            return hash_value
        else:
            return hash(key) % self.capacity
    
    def put(self, key: Any, value: Any) -> None:
        """
        Insert or update a key-value pair.
        
        Args:
            key: Key to insert
            value: Value to associate with key
        """
        index = self._hash(key)
        entry = self.buckets[index]
        
        # Check if key already exists
        while entry:
            if entry.key == key:
                entry.value = value
                return
            entry = entry.next
        
        # Insert new entry at head of chain
        new_entry = HashEntry(key, value, self.buckets[index])
        self.buckets[index] = new_entry
        self.size += 1
        
        # Resize if load factor exceeded
        if self.size / self.capacity > self.load_factor:
            self._resize()
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Retrieve value for a given key.
        
        Args:
            key: Key to look up
            
        Returns:
            Value associated with key, or None if not found
        """
        index = self._hash(key)
        entry = self.buckets[index]
        
        while entry:
            if entry.key == key:
                return entry.value
            entry = entry.next
        
        return None
    
    def remove(self, key: Any) -> bool:
        """
        Remove a key-value pair from the table.
        
        Args:
            key: Key to remove
            
        Returns:
            True if key was found and removed, False otherwise
        """
        index = self._hash(key)
        entry = self.buckets[index]
        prev = None
        
        while entry:
            if entry.key == key:
                if prev:
                    prev.next = entry.next
                else:
                    self.buckets[index] = entry.next
                self.size -= 1
                return True
            prev = entry
            entry = entry.next
        
        return False
    
    def contains_key(self, key: Any) -> bool:
        """
        Check if a key exists in the table.
        
        Args:
            key: Key to check
            
        Returns:
            True if key exists, False otherwise
        """
        return self.get(key) is not None
    
    def keys(self) -> List[Any]:
        """Return all keys in the table."""
        keys = []
        for entry in self.buckets:
            while entry:
                keys.append(entry.key)
                entry = entry.next
        return keys
    
    def values(self) -> List[Any]:
        """Return all values in the table."""
        values = []
        for entry in self.buckets:
            while entry:
                values.append(entry.value)
                entry = entry.next
        return values
    
    def items(self) -> List[Tuple[Any, Any]]:
        """Return all key-value pairs in the table."""
        items = []
        for entry in self.buckets:
            while entry:
                items.append((entry.key, entry.value))
                entry = entry.next
        return items
    
    def _resize(self) -> None:
        """Resize the hash table to double its capacity."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        
        # Rehash all entries
        for entry in old_buckets:
            while entry:
                self.put(entry.key, entry.value)
                entry = entry.next
    
    def __len__(self) -> int:
        """Return the number of key-value pairs."""
        return self.size
    
    def __str__(self) -> str:
        """String representation of the hash table."""
        items = []
        for entry in self.buckets:
            chain = []
            while entry:
                chain.append(f"{entry.key}: {entry.value}")
                entry = entry.next
            if chain:
                items.append(" -> ".join(chain))
        return "{" + "; ".join(items) + "}"
    
    def get_load_factor(self) -> float:
        """Return current load factor."""
        return self.size / self.capacity if self.capacity > 0 else 0


def main() -> None:
    """Demonstrate hash table operations."""
    
    print("=== Hash Table Operations ===")
    
    # Create hash table
    ht = HashTable(initial_capacity=8)
    
    # Insert key-value pairs
    print("\nInserting key-value pairs:")
    pairs = [
        ("name", "Alice"),
        ("age", 30),
        ("city", "New York"),
        ("country", "USA"),
        ("occupation", "Engineer"),
        ("hobby", "Reading"),
        ("email", "alice@example.com"),
        ("phone", "123-456-7890"),
    ]
    
    for key, value in pairs:
        ht.put(key, value)
        print(f"  put('{key}', '{value}')")
    
    print(f"\nHash table: {ht}")
    print(f"Size: {len(ht)}")
    print(f"Capacity: {ht.capacity}")
    print(f"Load factor: {ht.get_load_factor():.2f}")
    
    # Retrieve values
    print("\nRetrieving values:")
    for key in ["name", "age", "city", "nonexistent"]:
        value = ht.get(key)
        print(f"  get('{key}'): {value}")
    
    # Check key existence
    print("\nChecking key existence:")
    for key in ["name", "age", "nonexistent"]:
        exists = ht.contains_key(key)
        print(f"  contains_key('{key}'): {exists}")
    
    # Update value
    print("\nUpdating value:")
    ht.put("age", 31)
    print(f"  After put('age', 31): get('age') = {ht.get('age')}")
    
    # Remove key
    print("\nRemoving keys:")
    ht.remove("hobby")
    print(f"  After remove('hobby'): {ht}")
    print(f"  Size: {len(ht)}")
    
    # Get all keys, values, items
    print("\nAll data:")
    print(f"  Keys: {ht.keys()}")
    print(f"  Values: {ht.values()}")
    print(f"  Items: {ht.items()}")
    
    # Test collision handling
    print("\n=== Collision Handling Test ===")
    ht2 = HashTable(initial_capacity=4)
    
    # These keys will likely collide in a small table
    for i in range(10):
        ht2.put(f"key{i}", f"value{i}")
    
    print(f"Inserted 10 items with capacity 4")
    print(f"Final capacity: {ht2.capacity}")
    print(f"Load factor: {ht2.get_load_factor():.2f}")
    print(f"Hash table: {ht2}")


if __name__ == "__main__":
    main()
