"""
Caching Utilities Module

This module provides comprehensive caching utilities including:
- In-memory caching with TTL
- File-based caching
- Decorator-based caching
- Cache statistics and monitoring
- Cache invalidation strategies
- Distributed caching patterns
- Memoization utilities
- Cache warming and preloading
- Cache compression
- Thread-safe caching

All functions include comprehensive docstrings and type hints.
"""

import time
import json
import pickle
import hashlib
import threading
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
from functools import wraps
import os


try:
    import gzip
    GZIP_AVAILABLE = True
except ImportError:
    GZIP_AVAILABLE = False


class CacheStrategy(Enum):
    """Cache eviction strategies."""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    FIFO = "fifo"  # First In First Out
    LIFO = "lifo"  # Last In First Out
    TTL = "ttl"  # Time To Live


@dataclass
class CacheEntry:
    """Container for cache entry."""
    key: str
    value: Any
    created_at: float
    last_accessed: float
    access_count: int
    ttl: Optional[float] = None
    size: int = 0


@dataclass
class CacheStats:
    """Cache statistics."""
    hits: int
    misses: int
    evictions: int
    size: int
    max_size: int
    hit_rate: float


class MemoryCache:
    """In-memory cache implementation."""
    
    def __init__(self, max_size: int = 1000,
                 strategy: CacheStrategy = CacheStrategy.LRU,
                 default_ttl: Optional[float] = None):
        """Initialize memory cache."""
        self.max_size = max_size
        self.strategy = strategy
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheEntry] = {}
        self.lock = threading.RLock()
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            if key not in self.cache:
                self.stats["misses"] += 1
                return None
            
            entry = self.cache[key]
            
            # Check TTL
            if entry.ttl and (time.time() - entry.created_at) > entry.ttl:
                del self.cache[key]
                self.stats["misses"] += 1
                return None
            
            # Update access statistics
            entry.last_accessed = time.time()
            entry.access_count += 1
            self.stats["hits"] += 1
            
            return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """Set value in cache."""
        with self.lock:
            # Calculate TTL
            cache_ttl = ttl if ttl is not None else self.default_ttl
            
            # Calculate size (approximate)
            size = len(str(value)) if isinstance(value, str) else 1
            
            # Check if cache is full
            if len(self.cache) >= self.max_size and key not in self.cache:
                self._evict()
            
            # Add/update entry
            self.cache[key] = CacheEntry(
                key=key,
                value=value,
                created_at=time.time(),
                last_accessed=time.time(),
                access_count=0,
                ttl=cache_ttl,
                size=size
            )
            
            return True
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self.lock:
            self.cache.clear()
            self.stats = {"hits": 0, "misses": 0, "evictions": 0}
    
    def _evict(self) -> None:
        """Evict entry based on strategy."""
        if not self.cache:
            return
        
        if self.strategy == CacheStrategy.LRU:
            # Evict least recently used
            key_to_evict = min(self.cache.keys(), 
                              key=lambda k: self.cache[k].last_accessed)
        elif self.strategy == CacheStrategy.LFU:
            # Evict least frequently used
            key_to_evict = min(self.cache.keys(),
                              key=lambda k: self.cache[k].access_count)
        elif self.strategy == CacheStrategy.FIFO:
            # Evict oldest
            key_to_evict = min(self.cache.keys(),
                              key=lambda k: self.cache[k].created_at)
        elif self.strategy == CacheStrategy.LIFO:
            # Evict newest
            key_to_evict = max(self.cache.keys(),
                              key=lambda k: self.cache[k].created_at)
        else:
            # Default to LRU
            key_to_evict = min(self.cache.keys(),
                              key=lambda k: self.cache[k].last_accessed)
        
        del self.cache[key_to_evict]
        self.stats["evictions"] += 1
    
    def get_stats(self) -> CacheStats:
        """Get cache statistics."""
        with self.lock:
            total_requests = self.stats["hits"] + self.stats["misses"]
            hit_rate = self.stats["hits"] / total_requests if total_requests > 0 else 0.0
            
            return CacheStats(
                hits=self.stats["hits"],
                misses=self.stats["misses"],
                evictions=self.stats["evictions"],
                size=len(self.cache),
                max_size=self.max_size,
                hit_rate=hit_rate
            )
    
    def get_keys(self) -> List[str]:
        """Get all cache keys."""
        with self.lock:
            return list(self.cache.keys())
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        with self.lock:
            return key in self.cache


class FileCache:
    """File-based cache implementation."""
    
    def __init__(self, cache_dir: str = ".cache",
                 default_ttl: Optional[float] = None):
        """Initialize file cache."""
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl
        self.lock = threading.RLock()
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_file_path(self, key: str) -> str:
        """Get file path for cache key."""
        # Hash key to create safe filename
        hashed_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hashed_key}.cache")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from file cache."""
        with self.lock:
            file_path = self._get_file_path(key)
            
            if not os.path.exists(file_path):
                return None
            
            try:
                with open(file_path, 'rb') as f:
                    data = pickle.load(f)
                
                # Check TTL
                if data.get("ttl") and (time.time() - data["created_at"]) > data["ttl"]:
                    os.remove(file_path)
                    return None
                
                return data["value"]
            except Exception:
                return None
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """Set value in file cache."""
        with self.lock:
            file_path = self._get_file_path(key)
            
            try:
                data = {
                    "value": value,
                    "created_at": time.time(),
                    "ttl": ttl if ttl is not None else self.default_ttl
                }
                
                with open(file_path, 'wb') as f:
                    pickle.dump(data, f)
                
                return True
            except Exception:
                return False
    
    def delete(self, key: str) -> bool:
        """Delete key from file cache."""
        with self.lock:
            file_path = self._get_file_path(key)
            
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    return True
                except Exception:
                    return False
            
            return False
    
    def clear(self) -> None:
        """Clear all cache files."""
        with self.lock:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    file_path = os.path.join(self.cache_dir, filename)
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass
    
    def get_size(self) -> int:
        """Get total cache size in bytes."""
        total_size = 0
        
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.cache'):
                file_path = os.path.join(self.cache_dir, filename)
                try:
                    total_size += os.path.getsize(file_path)
                except Exception:
                    pass
        
        return total_size


class CacheDecorator:
    """Decorator-based caching utilities."""
    
    @staticmethod
    def cache_result(ttl: Optional[float] = None,
                    cache_instance: Optional[MemoryCache] = None):
        """Decorator to cache function results."""
        if cache_instance is None:
            cache_instance = MemoryCache()
        
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key from function name and arguments
                key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
                
                # Try to get from cache
                cached_value = cache_instance.get(key)
                if cached_value is not None:
                    return cached_value
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                cache_instance.set(key, result, ttl)
                
                return result
            
            return wrapper
        return decorator
    
    @staticmethod
    def cache_by_key(key_func: Callable,
                    ttl: Optional[float] = None,
                    cache_instance: Optional[MemoryCache] = None):
        """Decorator to cache function results with custom key function."""
        if cache_instance is None:
            cache_instance = MemoryCache()
        
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Use custom key function
                key = key_func(*args, **kwargs)
                
                # Try to get from cache
                cached_value = cache_instance.get(key)
                if cached_value is not None:
                    return cached_value
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                cache_instance.set(key, result, ttl)
                
                return result
            
            return wrapper
        return decorator


class Memoizer:
    """Memoization utilities."""
    
    @staticmethod
    def memoize(func: Callable,
                max_size: Optional[int] = None,
                ttl: Optional[float] = None) -> Callable:
        """Memoize function results."""
        cache = {}
        cache_info = {"hits": 0, "misses": 0}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create key from arguments
            key = (args, frozenset(kwargs.items()))
            
            # Check cache
            if key in cache:
                entry = cache[key]
                
                # Check TTL
                if ttl and (time.time() - entry["time"]) > ttl:
                    del cache[key]
                    cache_info["misses"] += 1
                else:
                    cache_info["hits"] += 1
                    return entry["value"]
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Check max size
            if max_size and len(cache) >= max_size:
                # Remove oldest entry
                oldest_key = min(cache.keys(), key=lambda k: cache[k]["time"])
                del cache[oldest_key]
            
            # Cache result
            cache[key] = {"value": result, "time": time.time()}
            cache_info["misses"] += 1
            
            return result
        
        wrapper.cache_info = lambda: cache_info
        wrapper.cache_clear = lambda: cache.clear()
        
        return wrapper
    
    @staticmethod
    def memoize_property(func: Callable) -> property:
        """Memoize property accessor."""
        attr_name = f"_memoized_{func.__name__}"
        
        @wraps(func)
        def wrapper(self):
            if not hasattr(self, attr_name):
                setattr(self, attr_name, func(self))
            return getattr(self, attr_name)
        
        return property(wrapper)


class CacheWarmer:
    """Cache warming and preloading utilities."""
    
    @staticmethod
    def warm_cache(cache: MemoryCache,
                  data_generator: Callable[[], Dict[str, Any]],
                  ttl: Optional[float] = None) -> int:
        """Warm cache with preloaded data."""
        data = data_generator()
        count = 0
        
        for key, value in data.items():
            if cache.set(key, value, ttl):
                count += 1
        
        return count
    
    @staticmethod
    def preload_data(cache: MemoryCache,
                    keys: List[str],
                    value_func: Callable[[str], Any],
                    ttl: Optional[float] = None) -> int:
        """Preload data for given keys."""
        count = 0
        
        for key in keys:
            value = value_func(key)
            if cache.set(key, value, ttl):
                count += 1
        
        return count


class CacheCompression:
    """Cache compression utilities."""
    
    @staticmethod
    def compress(data: Any) -> bytes:
        """Compress data using gzip."""
        if not GZIP_AVAILABLE:
            raise ImportError("gzip module is required")
        
        serialized = pickle.dumps(data)
        return gzip.compress(serialized)
    
    @staticmethod
    def decompress(compressed_data: bytes) -> Any:
        """Decompress gzip data."""
        if not GZIP_AVAILABLE:
            raise ImportError("gzip module is required")
        
        decompressed = gzip.decompress(compressed_data)
        return pickle.loads(decompressed)
    
    @staticmethod
    def get_compression_ratio(original: Any, compressed: bytes) -> float:
        """Calculate compression ratio."""
        original_size = len(pickle.dumps(original))
        compressed_size = len(compressed)
        
        if original_size == 0:
            return 0.0
        
        return (1 - compressed_size / original_size) * 100


class CacheInvalidation:
    """Cache invalidation strategies."""
    
    @staticmethod
    def invalidate_by_pattern(cache: MemoryCache, pattern: str) -> int:
        """Invalidate cache entries matching pattern."""
        import re
        
        keys_to_delete = []
        pattern_re = re.compile(pattern)
        
        for key in cache.get_keys():
            if pattern_re.match(key):
                keys_to_delete.append(key)
        
        for key in keys_to_delete:
            cache.delete(key)
        
        return len(keys_to_delete)
    
    @staticmethod
    def invalidate_by_prefix(cache: MemoryCache, prefix: str) -> int:
        """Invalidate cache entries with given prefix."""
        keys_to_delete = [key for key in cache.get_keys() if key.startswith(prefix)]
        
        for key in keys_to_delete:
            cache.delete(key)
        
        return len(keys_to_delete)
    
    @staticmethod
    def invalidate_by_tag(cache: MemoryCache, tag: str) -> int:
        """Invalidate cache entries by tag (requires tag support)."""
        # This would require cache entries to have tag metadata
        # For now, invalidate by pattern
        return CacheInvalidation.invalidate_by_pattern(cache, f".*{tag}.*")


class DistributedCache:
    """Distributed cache patterns (simplified)."""
    
    def __init__(self, local_cache: MemoryCache,
                 backup_cache: Optional[FileCache] = None):
        """Initialize distributed cache with local and backup."""
        self.local_cache = local_cache
        self.backup_cache = backup_cache
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from distributed cache."""
        # Try local cache first
        value = self.local_cache.get(key)
        if value is not None:
            return value
        
        # Try backup cache
        if self.backup_cache:
            value = self.backup_cache.get(key)
            if value is not None:
                # Repopulate local cache
                self.local_cache.set(key, value)
                return value
        
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """Set value in distributed cache."""
        # Set in local cache
        local_success = self.local_cache.set(key, value, ttl)
        
        # Set in backup cache
        backup_success = True
        if self.backup_cache:
            backup_success = self.backup_cache.set(key, value, ttl)
        
        return local_success and backup_success
    
    def delete(self, key: str) -> bool:
        """Delete from distributed cache."""
        local_success = self.local_cache.delete(key)
        
        backup_success = True
        if self.backup_cache:
            backup_success = self.backup_cache.delete(key)
        
        return local_success or backup_success


class CacheMonitor:
    """Cache monitoring and metrics."""
    
    @staticmethod
    def monitor_cache(cache: MemoryCache, interval: float = 60) -> Dict:
        """Monitor cache performance."""
        stats = cache.get_stats()
        
        return {
            "hit_rate": stats.hit_rate,
            "hits": stats.hits,
            "misses": stats.misses,
            "evictions": stats.evictions,
            "size": stats.size,
            "max_size": stats.max_size,
            "utilization": stats.size / stats.max_size if stats.max_size > 0 else 0
        }
    
    @staticmethod
    def compare_caches(caches: Dict[str, MemoryCache]) -> Dict:
        """Compare multiple caches."""
        comparison = {}
        
        for name, cache in caches.items():
            stats = cache.get_stats()
            comparison[name] = {
                "hit_rate": stats.hit_rate,
                "size": stats.size,
                "utilization": stats.size / stats.max_size if stats.max_size > 0 else 0
            }
        
        return comparison


class TieredCache:
    """Multi-tier caching (L1, L2, L3)."""
    
    def __init__(self, l1_cache: MemoryCache,
                 l2_cache: Optional[MemoryCache] = None,
                 l3_cache: Optional[FileCache] = None):
        """Initialize tiered cache."""
        self.l1_cache = l1_cache
        self.l2_cache = l2_cache
        self.l3_cache = l3_cache
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from tiered cache."""
        # L1 cache
        value = self.l1_cache.get(key)
        if value is not None:
            return value
        
        # L2 cache
        if self.l2_cache:
            value = self.l2_cache.get(key)
            if value is not None:
                # Promote to L1
                self.l1_cache.set(key, value)
                return value
        
        # L3 cache
        if self.l3_cache:
            value = self.l3_cache.get(key)
            if value is not None:
                # Promote to L1 and L2
                self.l1_cache.set(key, value)
                if self.l2_cache:
                    self.l2_cache.set(key, value)
                return value
        
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """Set value in all cache tiers."""
        l1_success = self.l1_cache.set(key, value, ttl)
        
        l2_success = True
        if self.l2_cache:
            l2_success = self.l2_cache.set(key, value, ttl)
        
        l3_success = True
        if self.l3_cache:
            l3_success = self.l3_cache.set(key, value, ttl)
        
        return l1_success and l2_success and l3_success
    
    def delete(self, key: str) -> bool:
        """Delete from all cache tiers."""
        self.l1_cache.delete(key)
        
        if self.l2_cache:
            self.l2_cache.delete(key)
        
        if self.l3_cache:
            self.l3_cache.delete(key)
        
        return True


def demonstrate_caching_utils():
    """Demonstrate caching utilities functionality."""
    print("=== Caching Utilities Demonstration ===\n")
    
    # Memory Cache
    print("1. Memory Cache:")
    cache = MemoryCache(max_size=100, strategy=CacheStrategy.LRU)
    
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    
    print(f"   Get key1: {cache.get('key1')}")
    print(f"   Get key4: {cache.get('key4')}")
    print(f"   Key1 exists: {cache.exists('key1')}")
    
    stats = cache.get_stats()
    print(f"   Cache stats: hits={stats.hits}, misses={stats.misses}, hit_rate={stats.hit_rate:.2f}")
    
    # File Cache
    print("\n2. File Cache:")
    file_cache = FileCache(cache_dir=".test_cache")
    
    file_cache.set("file_key1", {"data": "test"})
    file_cache.set("file_key2", [1, 2, 3])
    
    print(f"   Get file_key1: {file_cache.get('file_key1')}")
    print(f"   Cache size: {file_cache.get_size()} bytes")
    
    # Cache Decorator
    print("\n3. Cache Decorator:")
    decorator_cache = MemoryCache()
    
    @CacheDecorator.cache_result(ttl=60, cache_instance=decorator_cache)
    def expensive_function(x):
        print(f"   Computing {x}...")
        time.sleep(0.1)
        return x * 2
    
    result1 = expensive_function(5)
    result2 = expensive_function(5)
    print(f"   Results: {result1}, {result2}")
    
    # Memoization
    print("\n4. Memoization:")
    
    @Memoizer.memoize(max_size=100)
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    start = time.time()
    fib_result = fibonacci(35)
    elapsed = time.time() - start
    print(f"   Fibonacci(35): {fib_result}, time: {elapsed:.4f}s")
    
    # Cache Warming
    print("\n5. Cache Warming:")
    warm_cache = MemoryCache()
    
    def data_generator():
        return {"key1": "value1", "key2": "value2", "key3": "value3"}
    
    warmed = CacheWarmer.warm_cache(warm_cache, data_generator)
    print(f"   Warmed {warmed} cache entries")
    
    # Cache Compression
    print("\n6. Cache Compression:")
    if GZIP_AVAILABLE:
        data = {"large": "x" * 1000}
        compressed = CacheCompression.compress(data)
        ratio = CacheCompression.get_compression_ratio(data, compressed)
        print(f"   Compression ratio: {ratio:.2f}%")
    else:
        print("   Gzip not available")
    
    # Cache Invalidation
    print("\n7. Cache Invalidation:")
    invalidation_cache = MemoryCache()
    
    for i in range(5):
        invalidation_cache.set(f"user_{i}", f"data_{i}")
    
    invalidated = CacheInvalidation.invalidate_by_prefix(invalidation_cache, "user_")
    print(f"   Invalidated {invalidated} entries")
    
    # Distributed Cache
    print("\n8. Distributed Cache:")
    local = MemoryCache(max_size=10)
    backup = FileCache(cache_dir=".backup_cache")
    
    dist_cache = DistributedCache(local, backup)
    
    dist_cache.set("dist_key", "dist_value")
    retrieved = dist_cache.get("dist_key")
    print(f"   Distributed cache get: {retrieved}")
    
    # Tiered Cache
    print("\n9. Tiered Cache:")
    l1 = MemoryCache(max_size=5)
    l2 = MemoryCache(max_size=20)
    l3 = FileCache(cache_dir=".tier3_cache")
    
    tiered = TieredCache(l1, l2, l3)
    
    tiered.set("tier_key", "tier_value")
    tiered_value = tiered.get("tier_key")
    print(f"   Tiered cache get: {tiered_value}")
    
    # Cache Monitoring
    print("\n10. Cache Monitoring:")
    monitor_cache = MemoryCache(max_size=50)
    
    for i in range(30):
        monitor_cache.set(f"key_{i}", f"value_{i}")
        monitor_cache.get(f"key_{i}")
    
    metrics = CacheMonitor.monitor_cache(monitor_cache)
    print(f"   Cache metrics: {metrics}")
    
    # Cleanup
    print("\n11. Cleanup:")
    file_cache.clear()
    dist_cache.backup_cache.clear() if dist_cache.backup_cache else None
    tiered.l3_cache.clear() if tiered.l3_cache else None
    
    # Remove test directories
    import shutil
    for dir_name in [".test_cache", ".backup_cache", ".tier3_cache"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    print("   Test cache directories cleaned up")
    
    print("\n=== Demonstration Complete ===")
    print("\nCaching Best Practices:")
    print("- Use appropriate cache size for your memory constraints")
    print("- Choose eviction strategy based on access patterns")
    print("- Set appropriate TTL to prevent stale data")
    print("- Monitor cache hit rates to optimize performance")
    print("- Use compression for large cached values")
    print("- Implement cache invalidation for data consistency")
    print("- Use tiered caching for optimal performance")
    print("- Consider distributed caching for scalability")
    print("- Use memoization for expensive function calls")
    print("- Warm cache with frequently accessed data")


if __name__ == "__main__":
    demonstrate_caching_utils()