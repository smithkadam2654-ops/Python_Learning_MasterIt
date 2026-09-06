"""
LRU Cache - Least Recently Used cache implementation.
Features: Fixed capacity, O(1) operations, and eviction policy.
"""

from typing import Optional, TypeVar, Generic, Dict

T = TypeVar('T')
V = TypeVar('V')


class LRUCacheNode(Generic[T, V]):
    """Node in LRU cache doubly linked list."""
    
    def __init__(self, key: T, value: V) -> None:
        """
        Initialize node.
        
        Args:
            key: Node key
            value: Node value
        """
        self.key = key
        self.value = value
        self.prev: Optional['LRUCacheNode[T, V]'] = None
        self.next: Optional['LRUCacheNode[T, V]'] = None


class LRUCache(Generic[T, V]):
    """LRU cache implementation."""
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize LRU cache.
        
        Args:
            capacity: Maximum number of items
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.capacity = capacity
        self.cache: Dict[T, LRUCacheNode[T, V]] = {}
        self.head: Optional[LRUCacheNode[T, V]] = None
        self.tail: Optional[LRUCacheNode[T, V]] = None
        self._size = 0
    
    def get(self, key: T) -> Optional[V]:
        """
        Get value by key.
        
        Args:
            key: Key to get
            
        Returns:
            Value or None if not found
        """
        if key not in self.cache:
            return None
        
        node = self.cache[key]
        self._move_to_front(node)
        return node.value
    
    def put(self, key: T, value: V) -> None:
        """
        Put key-value pair into cache.
        
        Args:
            key: Key
            value: Value
        """
        if key in self.cache:
            # Update existing
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
        else:
            # Add new
            if self._size >= self.capacity:
                self._evict_lru()
            
            new_node = LRUCacheNode(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)
            self._size += 1
    
    def delete(self, key: T) -> bool:
        """
        Delete key from cache.
        
        Args:
            key: Key to delete
            
        Returns:
            True if deleted
        """
        if key not in self.cache:
            return False
        
        node = self.cache[key]
        self._remove_node(node)
        del self.cache[key]
        self._size -= 1
        return True
    
    def contains(self, key: T) -> bool:
        """
        Check if key exists in cache.
        
        Args:
            key: Key to check
            
        Returns:
            True if exists
        """
        return key in self.cache
    
    def size(self) -> int:
        """Get current size."""
        return self._size
    
    def capacity(self) -> int:
        """Get capacity."""
        return self.capacity
    
    def is_empty(self) -> bool:
        """Check if cache is empty."""
        return self._size == 0
    
    def is_full(self) -> bool:
        """Check if cache is full."""
        return self._size >= self.capacity
    
    def clear(self) -> None:
        """Clear cache."""
        self.cache.clear()
        self.head = None
        self.tail = None
        self._size = 0
    
    def keys(self) -> list:
        """Get all keys in LRU order."""
        keys = []
        current = self.head
        while current:
            keys.append(current.key)
            current = current.next
        return keys
    
    def values(self) -> list:
        """Get all values in LRU order."""
        values = []
        current = self.head
        while current:
            values.append(current.value)
            current = current.next
        return values
    
    def items(self) -> list:
        """Get all key-value pairs in LRU order."""
        items = []
        current = self.head
        while current:
            items.append((current.key, current.value))
            current = current.next
        return items
    
    def _add_to_front(self, node: LRUCacheNode[T, V]) -> None:
        """Add node to front of list (most recently used)."""
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
    
    def _move_to_front(self, node: LRUCacheNode[T, V]) -> None:
        """Move node to front of list."""
        if node == self.head:
            return
        
        self._remove_node(node)
        self._add_to_front(node)
    
    def _remove_node(self, node: LRUCacheNode[T, V]) -> None:
        """Remove node from list."""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        
        node.prev = None
        node.next = None
    
    def _evict_lru(self) -> None:
        """Evict least recently used item."""
        if self.tail:
            lru_key = self.tail.key
            self._remove_node(self.tail)
            del self.cache[lru_key]
            self._size -= 1
    
    def __len__(self) -> int:
        """Get length."""
        return self._size
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return f"LRUCache(empty, capacity={self.capacity})"
        
        items_str = ", ".join(f"{k}: {v}" for k, v in self.items())
        return f"LRUCache([{items_str}], capacity={self.capacity})"


def main() -> None:
    """Demonstrate LRU cache."""
    
    print("=== LRU Cache Demo ===")
    
    cache = LRUCache[str, int](3)
    
    print(f"Empty: {cache.is_empty()}")
    print(f"Full: {cache.is_full()}")
    
    # Put items
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    print(f"\nAfter put(a,1), put(b,2), put(c,3):")
    print(f"  Cache: {cache}")
    print(f"  Keys (LRU order): {cache.keys()}")
    
    # Get item
    print(f"\nGet 'b': {cache.get('b')}")
    print(f"  Keys after get (b moved to front): {cache.keys()}")
    
    # Put with eviction
    print(f"\nPut 'd' (should evict 'a'):")
    cache.put("d", 4)
    print(f"  Cache: {cache}")
    print(f"  Keys: {cache.keys()}")
    print(f"  Contains 'a': {cache.contains('a')}")
    
    # Update existing
    print(f"\nPut 'b' with new value:")
    cache.put("b", 20)
    print(f"  Cache: {cache}")
    print(f"  Keys: {cache.keys()}")
    
    # Delete
    print(f"\nDelete 'c':")
    cache.delete("c")
    print(f"  Cache: {cache}")
    print(f"  Keys: {cache.keys()}")
    
    # Size and capacity
    print(f"\nSize: {cache.size()}")
    print(f"Capacity: {cache.capacity()}")
    
    # Items and values
    print(f"\nItems: {cache.items()}")
    print(f"Values: {cache.values()}")
    
    # Clear
    cache.clear()
    print(f"\nAfter clear: {cache}")
    print(f"Is empty: {cache.is_empty()}")
    
    # Integer key cache
    print("\n=== Integer Key Cache ===")
    int_cache = LRUCache[int, str](2)
    
    int_cache.put(1, "one")
    int_cache.put(2, "two")
    int_cache.put(3, "three")
    
    print(f"Cache: {int_cache}")
    print(f"Get 1: {int_cache.get(1)}")
    print(f"Get 2: {int_cache.get(2)}")
    print(f"Get 3: {int_cache.get(3)}")


if __name__ == "__main__":
    main()
