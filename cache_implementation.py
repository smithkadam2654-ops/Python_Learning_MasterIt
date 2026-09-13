"""
Cache Implementation - LRU and LFU cache implementations.
Features: LRU cache with O(1) operations, LFU cache, and cache utilities.
"""

from typing import Optional, TypeVar, Generic
from collections import OrderedDict, defaultdict

T = TypeVar('T')
V = TypeVar('V')


class LRUCache:
    """LRU (Least Recently Used) cache implementation."""
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize LRU cache.
        
        Args:
            capacity: Maximum number of items
        """
        self.capacity = capacity
        self.cache: OrderedDict[T, V] = OrderedDict()
    
    def get(self, key: T) -> Optional[V]:
        """
        Get value for key.
        
        Args:
            key: Key to retrieve
            
        Returns:
            Value or None if not found
        """
        if key not in self.cache:
            return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: T, value: V) -> None:
        """
        Put key-value pair into cache.
        
        Args:
            key: Key
            value: Value
        """
        if key in self.cache:
            # Update and move to end
            self.cache.move_to_end(key)
        else:
            # Remove least recently used if at capacity
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        
        self.cache[key] = value
    
    def remove(self, key: T) -> bool:
        """
        Remove key from cache.
        
        Args:
            key: Key to remove
            
        Returns:
            True if removed, False if not found
        """
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all items from cache."""
        self.cache.clear()
    
    def __len__(self) -> int:
        """Get cache size."""
        return len(self.cache)
    
    def __contains__(self, key: T) -> bool:
        """Check if key in cache."""
        return key in self.cache
    
    def __repr__(self) -> str:
        return f"LRUCache(capacity={self.capacity}, size={len(self)})"


class LFUCache:
    """LFU (Least Frequently Used) cache implementation."""
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize LFU cache.
        
        Args:
            capacity: Maximum number of items
        """
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val_freq: dict = {}  # key -> (value, freq)
        self.freq_to_keys: defaultdict = defaultdict(OrderedDict)  # freq -> OrderedDict of keys
    
    def get(self, key: T) -> Optional[V]:
        """
        Get value for key.
        
        Args:
            key: Key to retrieve
            
        Returns:
            Value or None if not found
        """
        if key not in self.key_to_val_freq:
            return None
        
        val, freq = self.key_to_val_freq[key]
        
        # Update frequency
        del self.freq_to_keys[freq][key]
        
        if not self.freq_to_keys[freq]:
            if self.min_freq == freq:
                self.min_freq += 1
            del self.freq_to_keys[freq]
        
        self.key_to_val_freq[key] = (val, freq + 1)
        self.freq_to_keys[freq + 1][key] = None
        
        return val
    
    def put(self, key: T, value: V) -> None:
        """
        Put key-value pair into cache.
        
        Args:
            key: Key
            value: Value
        """
        if self.capacity <= 0:
            return
        
        if key in self.key_to_val_freq:
            self.get(key)  # Update frequency
            self.key_to_val_freq[key] = (value, self.key_to_val_freq[key][1])
            return
        
        # Remove LFU item if at capacity
        if len(self.key_to_val_freq) >= self.capacity:
            # Get least frequently used key
            lfu_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]
            
            del self.key_to_val_freq[lfu_key]
        
        # Add new item
        self.key_to_val_freq[key] = (value, 1)
        self.freq_to_keys[1][key] = None
        self.min_freq = 1
    
    def __len__(self) -> int:
        """Get cache size."""
        return len(self.key_to_val_freq)
    
    def __repr__(self) -> str:
        return f"LFUCache(capacity={self.capacity}, size={len(self)})"


class CacheNode:
    """Node for doubly linked list cache."""
    
    def __init__(self, key: T, value: V) -> None:
        """Initialize cache node."""
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCacheDLL:
    """LRU cache using doubly linked list (manual implementation)."""
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize LRU cache.
        
        Args:
            capacity: Maximum number of items
        """
        self.capacity = capacity
        self.cache: dict = {}
        self.head = CacheNode(None, None)
        self.tail = CacheNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove_node(self, node: CacheNode) -> None:
        """Remove node from linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_head(self, node: CacheNode) -> None:
        """Add node to head of linked list."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def get(self, key: T) -> Optional[V]:
        """
        Get value for key.
        
        Args:
            key: Key to retrieve
            
        Returns:
            Value or None if not found
        """
        if key not in self.cache:
            return None
        
        node = self.cache[key]
        self._remove_node(node)
        self._add_to_head(node)
        
        return node.value
    
    def put(self, key: T, value: V) -> None:
        """
        Put key-value pair into cache.
        
        Args:
            key: Key
            value: Value
        """
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._add_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                # Remove LRU (tail.prev)
                lru_node = self.tail.prev
                self._remove_node(lru_node)
                del self.cache[lru_node.key]
            
            new_node = CacheNode(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
    
    def __len__(self) -> int:
        """Get cache size."""
        return len(self.cache)


class CacheStats:
    """Cache statistics tracker."""
    
    def __init__(self) -> None:
        """Initialize cache stats."""
        self.hits = 0
        self.misses = 0
    
    def record_hit(self) -> None:
        """Record cache hit."""
        self.hits += 1
    
    def record_miss(self) -> None:
        """Record cache miss."""
        self.misses += 1
    
    def get_hit_rate(self) -> float:
        """Calculate hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0
    
    def reset(self) -> None:
        """Reset statistics."""
        self.hits = 0
        self.misses = 0
    
    def __repr__(self) -> str:
        return f"CacheStats(hits={self.hits}, misses={self.misses}, hit_rate={self.get_hit_rate():.2%})"


class CachedLRU:
    """LRU cache with statistics."""
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize cached LRU.
        
        Args:
            capacity: Maximum number of items
        """
        self.cache = LRUCache(capacity)
        self.stats = CacheStats()
    
    def get(self, key: T) -> Optional[V]:
        """
        Get value with statistics.
        
        Args:
            key: Key to retrieve
            
        Returns:
            Value or None
        """
        value = self.cache.get(key)
        
        if value is not None:
            self.stats.record_hit()
        else:
            self.stats.record_miss()
        
        return value
    
    def put(self, key: T, value: V) -> None:
        """Put key-value pair."""
        self.cache.put(key, value)
    
    def get_stats(self) -> CacheStats:
        """Get cache statistics."""
        return self.stats


def main() -> None:
    """Demonstrate cache implementations."""
    
    print("=== Cache Implementation Demo ===")
    
    # LRU Cache
    print("\n--- LRU Cache ---")
    lru = LRUCache(3)
    
    lru.put(1, "one")
    lru.put(2, "two")
    lru.put(3, "three")
    
    print(f"Cache: {lru}")
    print(f"Get 1: {lru.get(1)}")
    print(f"Get 4: {lru.get(4)}")
    
    lru.put(4, "four")  # Evicts 2 (LRU)
    print(f"After put(4): {lru}")
    print(f"Get 2: {lru.get(2)}")  # Should be None
    print(f"Get 1: {lru.get(1)}")  # Should be "one"
    
    # LFU Cache
    print("\n--- LFU Cache ---")
    lfu = LFUCache(3)
    
    lfu.put(1, "one")
    lfu.put(2, "two")
    lfu.put(3, "three")
    
    print(f"Cache: {lfu}")
    lfu.get(1)  # freq: 1->2
    lfu.get(1)  # freq: 2->3
    lfu.get(2)  # freq: 1->2
    
    lfu.put(4, "four")  # Evicts 3 (least frequent)
    print(f"After put(4): {lfu}")
    print(f"Get 3: {lfu.get(3)}")  # Should be None
    
    # LRU with Doubly Linked List
    print("\n--- LRU with Doubly Linked List ---")
    lru_dll = LRUCacheDLL(3)
    
    lru_dll.put(1, "one")
    lru_dll.put(2, "two")
    lru_dll.put(3, "three")
    
    print(f"Get 1: {lru_dll.get(1)}")
    lru_dll.put(4, "four")
    print(f"Get 2: {lru_dll.get(2)}")  # Should be None
    
    # Cache with Statistics
    print("\n--- Cache with Statistics ---")
    cached = CachedLRU(2)
    
    cached.put(1, "one")
    cached.put(2, "two")
    
    print(f"Get 1: {cached.get(1)}")
    print(f"Get 3: {cached.get(3)}")
    print(f"Stats: {cached.get_stats()}")
    
    cached.put(3, "three")
    cached.put(4, "four")
    
    print(f"Get 1: {cached.get(1)}")
    print(f"Get 3: {cached.get(3)}")
    print(f"Stats: {cached.get_stats()}")


if __name__ == "__main__":
    main()
