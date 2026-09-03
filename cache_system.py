"""
Cache System - Multi-level caching with eviction policies.
Features: LRU, LFU, TTL-based caching, and cache statistics.
"""

import time
from typing import Any, Optional, Dict, List, Tuple
from dataclasses import dataclass, field
from collections import OrderedDict, defaultdict
from enum import Enum
import threading


class EvictionPolicy(Enum):
    """Cache eviction policies."""
    LRU = "least_recently_used"
    LFU = "least_frequently_used"
    FIFO = "first_in_first_out"
    TTL = "time_to_live"


@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    value: Any
    timestamp: float = field(default_factory=time.time)
    access_count: int = 0
    ttl: Optional[float] = None
    
    def is_expired(self) -> bool:
        """Check if entry has expired."""
        if self.ttl is None:
            return False
        return time.time() - self.timestamp > self.ttl
    
    def touch(self) -> None:
        """Update access timestamp and count."""
        self.timestamp = time.time()
        self.access_count += 1


class CacheStats:
    """Cache statistics tracker."""
    
    def __init__(self) -> None:
        """Initialize cache statistics."""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.size = 0
    
    def record_hit(self) -> None:
        """Record a cache hit."""
        self.hits += 1
    
    def record_miss(self) -> None:
        """Record a cache miss."""
        self.misses += 1
    
    def record_eviction(self) -> None:
        """Record a cache eviction."""
        self.evictions += 1
    
    def update_size(self, delta: int) -> None:
        """Update cache size."""
        self.size += delta
    
    def get_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def reset(self) -> None:
        """Reset all statistics."""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.size = 0
    
    def __str__(self) -> str:
        """String representation of statistics."""
        return (f"CacheStats(hits={self.hits}, misses={self.misses}, "
                f"evictions={self.evictions}, size={self.size}, "
                f"hit_rate={self.get_hit_rate():.2%})")


class LRUCache:
    """LRU (Least Recently Used) cache implementation."""
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize LRU cache.
        
        Args:
            capacity: Maximum number of entries
        """
        self.capacity = capacity
        self.cache: OrderedDict = OrderedDict()
        self.stats = CacheStats()
        self._lock = threading.RLock()
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        with self._lock:
            if key in self.cache:
                # Move to end (most recently used)
                value = self.cache.pop(key)
                self.cache[key] = value
                self.stats.record_hit()
                return value
            else:
                self.stats.record_miss()
                return None
    
    def put(self, key: Any, value: Any) -> None:
        """
        Put value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        with self._lock:
            if key in self.cache:
                self.cache.pop(key)
            elif len(self.cache) >= self.capacity:
                # Evict least recently used (first item)
                self.cache.popitem(last=False)
                self.stats.record_eviction()
            
            self.cache[key] = value
            self.stats.update_size(1)
    
    def clear(self) -> None:
        """Clear all entries from cache."""
        with self._lock:
            old_size = len(self.cache)
            self.cache.clear()
            self.stats.update_size(-old_size)
    
    def size(self) -> int:
        """Return current cache size."""
        return len(self.cache)
    
    def get_stats(self) -> CacheStats:
        """Return cache statistics."""
        return self.stats


class LFUCache:
    """LFU (Least Frequently Used) cache implementation."""
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize LFU cache.
        
        Args:
            capacity: Maximum number of entries
        """
        self.capacity = capacity
        self.cache: Dict[Any, CacheEntry] = {}
        self.freq_map: Dict[int, List[Any]] = defaultdict(list)
        self.min_freq = 0
        self.stats = CacheStats()
        self._lock = threading.RLock()
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        with self._lock:
            if key not in self.cache:
                self.stats.record_miss()
                return None
            
            entry = self.cache[key]
            self._update_frequency(key, entry)
            self.stats.record_hit()
            return entry.value
    
    def put(self, key: Any, value: Any) -> None:
        """
        Put value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        with self._lock:
            if key in self.cache:
                entry = self.cache[key]
                entry.value = value
                self._update_frequency(key, entry)
            else:
                if len(self.cache) >= self.capacity:
                    # Evict least frequently used
                    if self.min_freq in self.freq_map and self.freq_map[self.min_freq]:
                        evict_key = self.freq_map[self.min_freq].pop()
                        del self.cache[evict_key]
                        self.stats.record_eviction()
                
                entry = CacheEntry(value=value)
                self.cache[key] = entry
                self.freq_map[1].append(key)
                self.min_freq = 1
                self.stats.update_size(1)
    
    def _update_frequency(self, key: Any, entry: CacheEntry) -> None:
        """Update access frequency for key."""
        old_freq = entry.access_count
        new_freq = old_freq + 1
        entry.access_count = new_freq
        
        # Remove from old frequency list
        if old_freq in self.freq_map and key in self.freq_map[old_freq]:
            self.freq_map[old_freq].remove(key)
        
        # Add to new frequency list
        self.freq_map[new_freq].append(key)
        
        # Update min frequency
        if old_freq == self.min_freq and not self.freq_map[old_freq]:
            self.min_freq = new_freq
    
    def clear(self) -> None:
        """Clear all entries from cache."""
        with self._lock:
            old_size = len(self.cache)
            self.cache.clear()
            self.freq_map.clear()
            self.min_freq = 0
            self.stats.update_size(-old_size)
    
    def size(self) -> int:
        """Return current cache size."""
        return len(self.cache)
    
    def get_stats(self) -> CacheStats:
        """Return cache statistics."""
        return self.stats


class TTLCache:
    """TTL (Time To Live) cache implementation."""
    
    def __init__(self, capacity: int, default_ttl: float = 60.0) -> None:
        """
        Initialize TTL cache.
        
        Args:
            capacity: Maximum number of entries
            default_ttl: Default time to live in seconds
        """
        self.capacity = capacity
        self.default_ttl = default_ttl
        self.cache: Dict[Any, CacheEntry] = {}
        self.stats = CacheStats()
        self._lock = threading.RLock()
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            if key not in self.cache:
                self.stats.record_miss()
                return None
            
            entry = self.cache[key]
            
            if entry.is_expired():
                del self.cache[key]
                self.stats.update_size(-1)
                self.stats.record_miss()
                return None
            
            entry.touch()
            self.stats.record_hit()
            return entry.value
    
    def put(self, key: Any, value: Any, ttl: Optional[float] = None) -> None:
        """
        Put value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (uses default if None)
        """
        with self._lock:
            ttl = ttl if ttl is not None else self.default_ttl
            
            if key in self.cache:
                self.stats.update_size(-1)
            elif len(self.cache) >= self.capacity:
                # Evict a random entry (simplified)
                evict_key = next(iter(self.cache))
                del self.cache[evict_key]
                self.stats.record_eviction()
            
            entry = CacheEntry(value=value, ttl=ttl)
            self.cache[key] = entry
            self.stats.update_size(1)
    
    def cleanup_expired(self) -> int:
        """Remove all expired entries."""
        with self._lock:
            expired_keys = [k for k, v in self.cache.items() if v.is_expired()]
            
            for key in expired_keys:
                del self.cache[key]
                self.stats.update_size(-1)
            
            return len(expired_keys)
    
    def clear(self) -> None:
        """Clear all entries from cache."""
        with self._lock:
            old_size = len(self.cache)
            self.cache.clear()
            self.stats.update_size(-old_size)
    
    def size(self) -> int:
        """Return current cache size."""
        return len(self.cache)
    
    def get_stats(self) -> CacheStats:
        """Return cache statistics."""
        return self.stats


class MultiLevelCache:
    """Multi-level cache with L1 (memory) and L2 (slower storage)."""
    
    def __init__(self, l1_capacity: int, l2_capacity: int) -> None:
        """
        Initialize multi-level cache.
        
        Args:
            l1_capacity: L1 cache capacity
            l2_capacity: L2 cache capacity
        """
        self.l1 = LRUCache(l1_capacity)
        self.l2 = LRUCache(l2_capacity)
        self.stats = CacheStats()
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Get value from cache (checks L1 then L2).
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        # Check L1 first
        value = self.l1.get(key)
        if value is not None:
            self.stats.record_hit()
            return value
        
        # Check L2
        value = self.l2.get(key)
        if value is not None:
            self.stats.record_hit()
            # Promote to L1
            self.l1.put(key, value)
            return value
        
        self.stats.record_miss()
        return None
    
    def put(self, key: Any, value: Any) -> None:
        """
        Put value in cache (stores in both levels).
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self.l1.put(key, value)
        self.l2.put(key, value)
    
    def clear(self) -> None:
        """Clear all entries from both cache levels."""
        self.l1.clear()
        self.l2.clear()
    
    def get_stats(self) -> Dict[str, CacheStats]:
        """Return statistics for all cache levels."""
        return {
            "overall": self.stats,
            "l1": self.l1.get_stats(),
            "l2": self.l2.get_stats()
        }


def main() -> None:
    """Demonstrate cache systems."""
    
    print("=== LRU Cache ===")
    lru = LRUCache(capacity=3)
    
    lru.put("a", 1)
    lru.put("b", 2)
    lru.put("c", 3)
    
    print(f"Get 'a': {lru.get('a')}")
    print(f"Get 'd': {lru.get('d')}")
    
    lru.put("d", 4)  # Should evict 'b' (least recently used)
    print(f"After putting 'd', get 'b': {lru.get('b')}")
    print(f"Get 'd': {lru.get('d')}")
    
    print(f"\nLRU Stats: {lru.get_stats()}")
    
    print("\n=== LFU Cache ===")
    lfu = LFUCache(capacity=3)
    
    lfu.put("a", 1)
    lfu.put("b", 2)
    lfu.put("c", 3)
    
    # Access 'a' multiple times
    lfu.get("a")
    lfu.get("a")
    lfu.get("a")
    
    # Access 'b' once
    lfu.get("b")
    
    lfu.put("d", 4)  # Should evict 'c' (least frequently used)
    print(f"After putting 'd', get 'c': {lfu.get('c')}")
    print(f"Get 'a': {lfu.get('a')}")
    
    print(f"\nLFU Stats: {lfu.get_stats()}")
    
    print("\n=== TTL Cache ===")
    ttl = TTLCache(capacity=3, default_ttl=1.0)
    
    ttl.put("a", 1, ttl=2.0)
    ttl.put("b", 2, ttl=0.5)
    ttl.put("c", 3)
    
    print(f"Get 'a': {ttl.get('a')}")
    print(f"Get 'b': {ttl.get('b')}")
    
    import time
    time.sleep(0.6)
    
    print(f"After 0.6s, get 'b': {ttl.get('b')}")
    print(f"After 0.6s, get 'a': {ttl.get('a')}")
    
    print(f"\nTTL Stats: {ttl.get_stats()}")
    
    print("\n=== Multi-Level Cache ===")
    mlc = MultiLevelCache(l1_capacity=2, l2_capacity=4)
    
    mlc.put("x", 10)
    mlc.put("y", 20)
    mlc.put("z", 30)
    
    print(f"Get 'x': {mlc.get('x')}")
    print(f"Get 'w': {mlc.get('w')}")
    
    print("\nMulti-Level Stats:")
    for level, stats in mlc.get_stats().items():
        print(f"  {level}: {stats}")


if __name__ == "__main__":
    main()
