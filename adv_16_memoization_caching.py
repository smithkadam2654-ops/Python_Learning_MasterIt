"""
Advanced Python - Lesson 16: Memoization & Caching
====================================================
Caching stores results of expensive computations to avoid
redundant work. Memoization is a specific form for pure functions.

Topics Covered:
- Manual memoization with dictionaries
- functools.lru_cache
- functools.cache (Python 3.9+)
- Custom memoization decorator with TTL
- Cache eviction strategies (LRU, LFU)
- Memoization for recursive algorithms
- Cache statistics and monitoring
- Disk-based caching
"""

import functools
import time
import hashlib
import json
import os
import tempfile
from typing import Any, Callable, TypeVar
from collections import OrderedDict

F = TypeVar("F", bound=Callable)


# ============================================================
# 1. MANUAL MEMOIZATION
# ============================================================
def fibonacci_naive(n: int) -> int:
    """Naive recursive Fibonacci — exponential time O(2^n)."""
    if n < 2:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


# Manual cache dictionary
_fib_cache: dict[int, int] = {0: 0, 1: 1}

def fibonacci_memoized(n: int) -> int:
    """Memoized Fibonacci — linear time O(n)."""
    if n not in _fib_cache:
        _fib_cache[n] = fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)
    return _fib_cache[n]


def compare_fibonacci():
    """Compare naive vs memoized performance."""
    import sys
    sys.setrecursionlimit(2000)
    
    n = 30
    start = time.perf_counter()
    result1 = fibonacci_naive(n)
    naive_time = time.perf_counter() - start
    
    start = time.perf_counter()
    result2 = fibonacci_memoized(n)
    memo_time = time.perf_counter() - start
    
    print(f"fibonacci_naive({n})     = {result1} in {naive_time:.4f}s")
    print(f"fibonacci_memoized({n})  = {result2} in {memo_time:.6f}s")
    print(f"Speedup: {naive_time/memo_time:.0f}x")
    
    # Larger value (only memoized can handle this)
    n2 = 500
    start = time.perf_counter()
    result3 = fibonacci_memoized(n2)
    print(f"\nfibonacci_memoized({n2}) = {result3} in {time.perf_counter()-start:.6f}s")


# ============================================================
# 2. FUNCTOOLS.LRU_CACHE
# ============================================================
@functools.lru_cache(maxsize=128)
def expensive_computation(x: int, y: int) -> int:
    """Simulate an expensive computation with LRU caching.
    
    lru_cache automatically caches results and evicts
    least-recently-used entries when maxsize is reached.
    """
    time.sleep(0.01)  # Simulate expensive work
    return x ** 2 + y ** 2 + x * y


@functools.lru_cache(maxsize=None)  # Unlimited cache
def cached_api_call(url: str, params: tuple) -> dict:
    """Simulate cached API calls.
    
    Note: Arguments must be hashable for caching.
    Use tuples instead of lists/dicts.
    """
    time.sleep(0.05)  # Simulate network delay
    return {"url": url, "params": params, "data": f"Result for {params}"}


def demonstrate_lru_cache():
    """Show LRU cache features and statistics."""
    
    print("Computing with LRU cache:")
    
    # First call — cache miss
    start = time.perf_counter()
    r1 = expensive_computation(3, 4)
    first_time = time.perf_counter() - start
    print(f"  (3,4) = {r1} in {first_time:.4f}s (cache miss)")
    
    # Second call — cache hit
    start = time.perf_counter()
    r2 = expensive_computation(3, 4)
    second_time = time.perf_counter() - start
    print(f"  (3,4) = {r2} in {second_time:.6f}s (cache hit)")
    
    # Cache statistics
    info = expensive_computation.cache_info()
    print(f"\n  Cache info: hits={info.hits}, misses={info.misses}, "
          f"size={info.currsize}/{info.maxsize}")
    
    # Fill cache beyond maxsize
    for i in range(150):
        expensive_computation(i, i + 1)
    
    info = expensive_computation.cache_info()
    print(f"  After 150 more calls: hits={info.hits}, misses={info.misses}, "
          f"size={info.currsize}/{info.maxsize}")
    
    # Clear cache
    expensive_computation.cache_clear()
    print(f"  After clear: {expensive_computation.cache_info()}")


# ============================================================
# 3. TTL CACHE (Time-To-Live)
# ============================================================
class TTLCache:
    """Cache with time-to-live expiration.
    
    Entries automatically expire after a configurable duration.
    """
    def __init__(self, ttl_seconds: float = 60.0, maxsize: int = 128):
        self.ttl = ttl_seconds
        self.maxsize = maxsize
        self._cache: OrderedDict[Any, tuple[Any, float]] = OrderedDict()
        self._hits = 0
        self._misses = 0

    def get(self, key: Any) -> Any:
        """Get value from cache, checking expiration."""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl:
                self._hits += 1
                self._cache.move_to_end(key)  # Mark as recently used
                return value
            else:
                del self._cache[key]  # Expired
        
        self._misses += 1
        return None

    def put(self, key: Any, value: Any):
        """Store value with current timestamp."""
        if key in self._cache:
            del self._cache[key]
        elif len(self._cache) >= self.maxsize:
            self._cache.popitem(last=False)  # Evict oldest
        self._cache[key] = (value, time.time())

    def invalidate(self, key: Any = None):
        """Invalidate one or all entries."""
        if key is None:
            self._cache.clear()
        elif key in self._cache:
            del self._cache[key]

    def stats(self) -> dict:
        total = self._hits + self._misses
        return {
            "hits": self._hits,
            "misses": self._misses,
            "size": len(self._cache),
            "hit_rate": self._hits / total if total > 0 else 0,
        }


def ttl_cache_decorator(ttl: float = 60.0, maxsize: int = 128):
    """Decorator factory for TTL caching."""
    cache = TTLCache(ttl_seconds=ttl, maxsize=maxsize)
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache.put(key, result)
            return result
        wrapper.cache_stats = cache.stats  # type: ignore
        wrapper.cache_clear = cache.invalidate  # type: ignore
        return wrapper
    return decorator


@ttl_cache_decorator(ttl=2.0)  # 2-second TTL
def fetch_weather(city: str) -> dict:
    """Simulated weather API with TTL cache."""
    time.sleep(0.1)  # Simulate API delay
    return {
        "city": city,
        "temp": 22.5,
        "condition": "sunny",
        "timestamp": time.time(),
    }


def demonstrate_ttl_cache():
    """TTL cache expires entries after a time period."""
    
    print("First call (cache miss):")
    start = time.perf_counter()
    r1 = fetch_weather("NYC")
    print(f"  {r1} ({time.perf_counter()-start:.4f}s)")
    
    print("Second call (cache hit):")
    start = time.perf_counter()
    r2 = fetch_weather("NYC")
    print(f"  {r2} ({time.perf_counter()-start:.6f}s)")
    
    print(f"\nStats: {fetch_weather.cache_stats()}")
    
    print("\nWaiting for TTL to expire...")
    time.sleep(2.1)
    
    print("After expiry (cache miss):")
    start = time.perf_counter()
    r3 = fetch_weather("NYC")
    print(f"  {r3} ({time.perf_counter()-start:.4f}s)")
    
    print(f"\nFinal stats: {fetch_weather.cache_stats()}")


# ============================================================
# 4. MEMOIZATION FOR CLASSIC ALGORITHMS
# ============================================================
@functools.lru_cache(maxsize=None)
def longest_common_subsequence(s1: str, s2: str) -> str:
    """LCS with memoization — exponential becomes polynomial."""
    if not s1 or not s2:
        return ""
    if s1[-1] == s2[-1]:
        return longest_common_subsequence(s1[:-1], s2[:-1]) + s1[-1]
    
    lcs1 = longest_common_subsequence(s1[:-1], s2)
    lcs2 = longest_common_subsequence(s1, s2[:-1])
    return lcs1 if len(lcs1) > len(lcs2) else lcs2


@functools.lru_cache(maxsize=None)
def knapsack(weights: tuple, values: tuple, capacity: int) -> int:
    """0/1 Knapsack problem with memoization.
    
    Args must be tuples (hashable) for caching.
    """
    n = len(weights)
    if n == 0 or capacity <= 0:
        return 0
    
    # Skip item if too heavy
    if weights[0] > capacity:
        return knapsack(weights[1:], values[1:], capacity)
    
    # Max of: include item vs skip item
    include = values[0] + knapsack(weights[1:], values[1:], capacity - weights[0])
    skip = knapsack(weights[1:], values[1:], capacity)
    return max(include, skip)


@functools.lru_cache(maxsize=None)
def edit_distance(s1: str, s2: str) -> int:
    """Minimum edit distance (Levenshtein) with memoization."""
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    
    if s1[-1] == s2[-1]:
        return edit_distance(s1[:-1], s2[:-1])
    
    insert = edit_distance(s1, s2[:-1])
    delete = edit_distance(s1[:-1], s2)
    replace = edit_distance(s1[:-1], s2[:-1])
    return 1 + min(insert, delete, replace)


def demonstrate_algorithmic_caching():
    """Classic algorithms benefit enormously from memoization."""
    
    # LCS
    s1, s2 = "ABCBDAB", "BDCABA"
    start = time.perf_counter()
    lcs = longest_common_subsequence(s1, s2)
    t = time.perf_counter() - start
    print(f"LCS('{s1}', '{s2}') = '{lcs}' (length {len(lcs)}) in {t:.4f}s")
    print(f"  Cache: {longest_common_subsequence.cache_info()}")
    
    # Knapsack
    weights = (2, 3, 4, 5, 6)
    values = (3, 4, 5, 6, 7)
    capacity = 10
    start = time.perf_counter()
    max_val = knapsack(weights, values, capacity)
    t = time.perf_counter() - start
    print(f"\nKnapsack(capacity={capacity}) = {max_val} in {t:.4f}s")
    print(f"  Cache: {knapsack.cache_info()}")
    
    # Edit Distance
    word1, word2 = "kitten", "sitting"
    start = time.perf_counter()
    dist = edit_distance(word1, word2)
    t = time.perf_counter() - start
    print(f"\nEdit distance('{word1}', '{word2}') = {dist} in {t:.4f}s")
    print(f"  Cache: {edit_distance.cache_info()}")


# ============================================================
# 5. DISK-BASED CACHE
# ============================================================
class DiskCache:
    """Simple disk-based cache using JSON files.
    
    Persists cached data across program restarts.
    """
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or tempfile.mkdtemp(prefix="pycache_")
        os.makedirs(self.cache_dir, exist_ok=True)

    def _key_to_path(self, key: str) -> str:
        """Convert key to a safe filename."""
        hashed = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hashed}.json")

    def get(self, key: str) -> Any:
        """Retrieve from disk cache."""
        path = self._key_to_path(key)
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                return data.get("value")
        return None

    def put(self, key: str, value: Any):
        """Store to disk cache."""
        path = self._key_to_path(key)
        with open(path, "w") as f:
            json.dump({"key": key, "value": value, "time": time.time()}, f)

    def clear(self):
        """Remove all cached files."""
        import shutil
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
            os.makedirs(self.cache_dir)

    @property
    def size(self) -> int:
        return len([f for f in os.listdir(self.cache_dir) if f.endswith(".json")])


def demonstrate_disk_cache():
    """Disk cache persists data across program runs."""
    
    cache = DiskCache()
    
    # Store some data
    cache.put("user:1", {"name": "Alice", "score": 95})
    cache.put("user:2", {"name": "Bob", "score": 87})
    cache.put("config", {"theme": "dark", "lang": "en"})
    
    print(f"Cache directory: {cache.cache_dir}")
    print(f"Cached items: {cache.size}")
    
    # Retrieve
    user = cache.get("user:1")
    print(f"Retrieved: {user}")
    
    config = cache.get("config")
    print(f"Config: {config}")
    
    # Missing key
    missing = cache.get("user:999")
    print(f"Missing key: {missing}")
    
    # Cleanup
    cache.clear()
    print(f"After clear: {cache.size} items")


# ============================================================
# 6. CACHE WITH SIZE LIMITS AND EVICTION
# ============================================================
class LRUCache:
    """Least Recently Used cache implementation.
    
    Uses OrderedDict for O(1) get/put with LRU eviction.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key: Any) -> Any:
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)  # Mark as recently used
        return self.cache[key]

    def put(self, key: Any, value: Any):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            evicted_key, _ = self.cache.popitem(last=False)  # Evict LRU
            print(f"  [Evict] Removed key: {evicted_key}")
        self.cache[key] = value

    def __repr__(self):
        items = list(self.cache.items())
        return f"LRU[{', '.join(f'{k}:{v}' for k, v in items)}]"


def demonstrate_lru():
    """Show LRU eviction behavior."""
    
    cache = LRUCache(capacity=3)
    
    operations = [
        ("put", "a", 1),
        ("put", "b", 2),
        ("put", "c", 3),
        ("get", "a", None),   # Access 'a' (makes it recently used)
        ("put", "d", 4),      # Evicts 'b' (least recently used)
        ("get", "c", None),   # Access 'c'
        ("put", "e", 5),      # Evicts 'a' (now least recently used)
    ]
    
    for op in operations:
        if op[0] == "put":
            cache.put(op[1], op[2])
            print(f"  PUT {op[1]}={op[2]} -> {cache}")
        else:
            val = cache.get(op[1])
            print(f"  GET {op[1]}={val}   -> {cache}")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Manual Memoization (Fibonacci)")
    compare_fibonacci()

    separator("2. functools.lru_cache")
    demonstrate_lru_cache()

    separator("3. TTL Cache")
    demonstrate_ttl_cache()

    separator("4. Algorithmic Caching")
    demonstrate_algorithmic_caching()

    separator("5. Disk-Based Cache")
    demonstrate_disk_cache()

    separator("6. LRU Eviction")
    demonstrate_lru()


if __name__ == "__main__":
    main()
