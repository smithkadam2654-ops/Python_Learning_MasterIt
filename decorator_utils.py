import time
import functools
import logging
from typing import Callable, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0, exceptions: tuple = (Exception,)):
    """
    A decorator that retries the wrapped function upon failure.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 1
            current_delay = delay
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logging.warning(f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}")
                    if attempt == max_attempts:
                        logging.error(f"All {max_attempts} attempts failed for {func.__name__}.")
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
                    attempt += 1
        return wrapper
    return decorator

def memoize(func: Callable) -> Callable:
    """Caches the results of the function based on arguments."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a cache key using args and frozenset of kwargs for hashability
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

@retry(max_attempts=3, delay=0.5, exceptions=(ValueError,))
def flaky_function():
    """Simulates a function that fails sometimes."""
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    return "Success!"

@memoize
def expensive_computation(x: int, y: int) -> int:
    """Simulates a slow computation."""
    print(f"Computing {x} + {y}...")
    time.sleep(1)
    return x + y

if __name__ == "__main__":
    print("Testing retry decorator:")
    try:
        print(flaky_function())
    except ValueError:
        print("Function ultimately failed.")
        
    print("\nTesting memoize decorator:")
    print(expensive_computation(5, 10))
    print(expensive_computation(5, 10)) # Should return instantly from cache
