"""
Memoization - Caching decorator with TTL and size limits.
Features: Function result caching, time-based expiration, and cache management.
"""

import time
import threading
from typing import Callable, Any, Optional, Dict
from functools import wraps
from dataclasses import dataclass
from collections import OrderedDict


@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    value: Any
    timestamp: float
    ttl: Optional[float] = None
    
    def is_expired(self) -> bool:
        """Check if entry has expired."""
        if self.ttl is None:
            return False
        return time.time() - self.timestamp > self.ttl


class LRUCache:
    """LRU (Least Recently Used) cache."""
    
    def __init__(self, max_size: int = 128) -> None:
        """
        Initialize LRU cache.
        
        Args:
            max_size: Maximum number of entries
        """
        self.max_size = max_size
        self.cache: OrderedDict = OrderedDict()
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
                return value
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
            elif len(self.cache) >= self.max_size:
                # Evict least recently used (first item)
                self.cache.popitem(last=False)
            
            self.cache[key] = value
    
    def clear(self) -> None:
        """Clear all entries from cache."""
        with self._lock:
            self.cache.clear()
    
    def size(self) -> int:
        """Return current cache size."""
        return len(self.cache)


class TTLCache:
    """TTL (Time To Live) cache."""
    
    def __init__(self, default_ttl: float = 60.0) -> None:
        """
        Initialize TTL cache.
        
        Args:
            default_ttl: Default time to live in seconds
        """
        self.default_ttl = default_ttl
        self.cache: Dict[Any, CacheEntry] = {}
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
                return None
            
            entry = self.cache[key]
            
            if entry.is_expired():
                del self.cache[key]
                return None
            
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
            self.cache[key] = CacheEntry(value=value, timestamp=time.time(), ttl=ttl)
    
    def cleanup_expired(self) -> int:
        """Remove all expired entries."""
        with self._lock:
            expired_keys = [k for k, v in self.cache.items() if v.is_expired()]
            
            for key in expired_keys:
                del self.cache[key]
            
            return len(expired_keys)
    
    def clear(self) -> None:
        """Clear all entries from cache."""
        with self._lock:
            self.cache.clear()
    
    def size(self) -> int:
        """Return current cache size."""
        return len(self.cache)


def memoize(max_size: int = 128, ttl: Optional[float] = None) -> Callable:
    """
    Memoization decorator with size limit and optional TTL.
    
    Args:
        max_size: Maximum number of cached results
        ttl: Time to live for cached results (None for no expiration)
        
    Returns:
        Decorator function
    """
    cache = LRUCache(max_size) if ttl is None else TTLCache(ttl)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create cache key from arguments
            key = (args, frozenset(kwargs.items()))
            
            # Try to get from cache
            if isinstance(cache, TTLCache):
                cached_value = cache.get(key)
            else:
                cached_value = cache.get(key)
            
            if cached_value is not None:
                return cached_value
            
            # Compute and cache result
            result = func(*args, **kwargs)
            
            if isinstance(cache, TTLCache):
                cache.put(key, result)
            else:
                cache.put(key, result)
            
            return result
        
        # Add cache management methods
        wrapper.cache = cache
        wrapper.cache_clear = cache.clear
        wrapper.cache_info = lambda: {"size": cache.size(), "max_size": max_size, "ttl": ttl}
        
        return wrapper
    
    return decorator


def cached_property(func: Callable) -> property:
    """
    Decorator for cached properties.
    
    Args:
        func: Property getter function
        
    Returns:
        Property descriptor with caching
    """
    attr_name = f"_cached_{func.__name__}"
    
    @wraps(func)
    def wrapper(self):
        """Get cached property value."""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    
    return property(wrapper)


class MemoizedClass:
    """Example class using memoization."""
    
    def __init__(self) -> None:
        """Initialize memoized class."""
        self._compute_count = 0
    
    @memoize(max_size=64)
    def expensive_computation(self, x: int, y: int) -> int:
        """
        Expensive computation with memoization.
        
        Args:
            x: First parameter
            y: Second parameter
            
        Returns:
            Computation result
        """
        self._compute_count += 1
        print(f"Computing ({x}, {y}) - call #{self._compute_count}")
        time.sleep(0.1)  # Simulate expensive operation
        return x ** 2 + y ** 2
    
    @cached_property
    def heavy_property(self) -> str:
        """
        Heavy property computation with caching.
        
        Returns:
            Computed property value
        """
        print("Computing heavy property...")
        time.sleep(0.2)
        return "Cached Result"
    
    def get_compute_count(self) -> int:
        """Get number of actual computations."""
        return self._compute_count


def fibonacci(n: int) -> int:
    """
    Fibonacci without memoization (slow).
    
    Args:
        n: Position in sequence
        
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@memoize(max_size=256)
def fibonacci_memoized(n: int) -> int:
    """
    Fibonacci with memoization (fast).
    
    Args:
        n: Position in sequence
        
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


@memoize(ttl=5.0)
def api_call(endpoint: str, params: dict = None) -> str:
    """
    Simulated API call with TTL caching.
    
    Args:
        endpoint: API endpoint
        params: Request parameters
        
    Returns:
        Simulated response
    """
    if params is None:
        params = {}
    
    print(f"Making API call to {endpoint} with params {params}")
    time.sleep(0.3)  # Simulate network delay
    return f"Response from {endpoint}"


def main() -> None:
    """Demonstrate memoization functionality."""
    
    print("=== Basic Memoization ===")
    obj = MemoizedClass()
    
    # First call - computes
    result1 = obj.expensive_computation(5, 3)
    print(f"Result 1: {result1}")
    
    # Second call with same args - uses cache
    result2 = obj.expensive_computation(5, 3)
    print(f"Result 2: {result2}")
    
    # Third call with different args - computes
    result3 = obj.expensive_computation(3, 4)
    print(f"Result 3: {result3}")
    
    # Fourth call - uses cache
    result4 = obj.expensive_computation(5, 3)
    print(f"Result 4: {result4}")
    
    print(f"\nTotal computations: {obj.get_compute_count()}")
    print(f"Cache info: {obj.expensive_computation.cache_info()}")
    
    print("\n=== Cached Property ===")
    # First access - computes
    prop1 = obj.heavy_property
    print(f"Property 1: {prop1}")
    
    # Second access - uses cache
    prop2 = obj.heavy_property
    print(f"Property 2: {prop2}")
    
    print("\n=== Fibonacci Comparison ===")
    import time
    
    # Without memoization
    start = time.time()
    result = fibonacci(30)
    elapsed = time.time() - start
    print(f"Fibonacci(30) without memoization: {result} (took {elapsed:.4f}s)")
    
    # With memoization
    start = time.time()
    result = fibonacci_memoized(30)
    elapsed = time.time() - start
    print(f"Fibonacci(30) with memoization: {result} (took {elapsed:.4f}s)")
    
    print(f"Cache info: {fibonacci_memoized.cache_info()}")
    
    print("\n=== TTL Caching ===")
    # First call - makes API call
    response1 = api_call("/users", {"page": 1})
    print(f"Response 1: {response1}")
    
    # Second call - uses cache
    response2 = api_call("/users", {"page": 1})
    print(f"Response 2: {response2}")
    
    # Different params - makes API call
    response3 = api_call("/users", {"page": 2})
    print(f"Response 3: {response3}")
    
    print(f"\nWaiting for TTL to expire...")
    time.sleep(6.0)
    
    # After TTL - makes API call again
    response4 = api_call("/users", {"page": 1})
    print(f"Response 4 (after TTL): {response4}")
    
    print("\n=== Cache Management ===")
    print(f"Cache size before clear: {fibonacci_memoized.cache.size()}")
    fibonacci_memoized.cache_clear()
    print(f"Cache size after clear: {fibonacci_memoized.cache.size()}")


if __name__ == "__main__":
    main()
