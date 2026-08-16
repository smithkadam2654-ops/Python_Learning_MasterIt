"""
Decorator Tools - A collection of useful Python decorators.
Features: Timing, caching, logging, retry logic, and input validation.
"""

import time
import functools
from typing import Callable, Any, Optional, Dict
from functools import wraps


def timer(func: Callable) -> Callable:
    """
    Decorator to measure and print function execution time.
    
    Example:
        @timer
        def slow_function():
            time.sleep(1)
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        print(f"{func.__name__} executed in {elapsed:.4f} seconds")
        return result
    return wrapper


def cache(max_size: int = 128) -> Callable:
    """
    Decorator to cache function results with size limit.
    
    Args:
        max_size: Maximum number of results to cache
        
    Example:
        @cache(max_size=64)
        def expensive_computation(n):
            return n ** 2
    """
    def decorator(func: Callable) -> Callable:
        cache_dict: Dict = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create a hashable key from arguments
            key = (args, frozenset(kwargs.items()))
            
            if key in cache_dict:
                return cache_dict[key]
            
            result = func(*args, **kwargs)
            
            # Implement size limit
            if len(cache_dict) >= max_size:
                cache_dict.pop(next.iter(cache_dict))
            
            cache_dict[key] = result
            return result
        
        wrapper.cache_clear = lambda: cache_dict.clear()
        wrapper.cache_info = lambda: {"size": len(cache_dict), "max_size": max_size}
        return wrapper
    return decorator


def logger(log_level: str = "INFO") -> Callable:
    """
    Decorator to log function calls and returns.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Example:
        @logger(log_level="DEBUG")
        def process_data(data):
            return data * 2
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            print(f"[{log_level}] Calling {func.__name__} with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                print(f"[{log_level}] {func.__name__} returned {result}")
                return result
            except Exception as e:
                print(f"[ERROR] {func.__name__} raised {type(e).__name__}: {e}")
                raise
        return wrapper
    return decorator


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """
    Decorator to retry function on failure with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between attempts in seconds
        
    Example:
        @retry(max_attempts=5, delay=0.5)
        def unstable_function():
            # Might fail occasionally
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = delay * (2 ** attempt)
                        print(f"Attempt {attempt + 1} failed, retrying in {wait_time:.2f}s...")
                        time.sleep(wait_time)
            
            raise last_exception
        return wrapper
    return decorator


def validate_types(**type_hints) -> Callable:
    """
    Decorator to validate function argument types.
    
    Args:
        type_hints: Parameter name to type mapping
        
    Example:
        @validate_types(x=int, y=str, z=list)
        def process(x, y, z):
            return len(z)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate types
            for param_name, expected_type in type_hints.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Argument '{param_name}' must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def count_calls(func: Callable) -> Callable:
    """
    Decorator to count how many times a function is called.
    
    Example:
        @count_calls
        def frequently_called():
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        wrapper.call_count += 1
        return func(*args, **kwargs)
    
    wrapper.call_count = 0
    return wrapper


def main() -> None:
    """Demonstrate decorator functionality."""
    
    # Timer decorator
    @timer
    def compute_fibonacci(n: int) -> int:
        """Compute Fibonacci number (inefficiently for demo)."""
        if n <= 1:
            return n
        return compute_fibonacci(n - 1) + compute_fibonacci(n - 2)
    
    # Cache decorator
    @cache(max_size=32)
    def cached_fibonacci(n: int) -> int:
        """Compute Fibonacci number with caching."""
        if n <= 1:
            return n
        return cached_fibonacci(n - 1) + cached_fibonacci(n - 2)
    
    # Retry decorator
    @retry(max_attempts=3, delay=0.5)
    def unstable_operation() -> str:
        """Simulate an operation that might fail."""
        import random
        if random.random() < 0.7:
            raise ValueError("Random failure occurred")
        return "Success!"
    
    # Type validation decorator
    @validate_types(name=str, age=int, scores=list)
    def process_student(name: str, age: int, scores: list) -> dict:
        """Process student data with type validation."""
        return {"name": name, "age": age, "average": sum(scores) / len(scores)}
    
    # Count calls decorator
    @count_calls
    def increment_counter() -> int:
        """Increment and return counter."""
        return 42
    
    # Demonstrate decorators
    print("=== Timer Decorator ===")
    compute_fibonacci(10)
    
    print("\n=== Cache Decorator ===")
    cached_fibonacci(30)
    print(f"Cache info: {cached_fibonacci.cache_info()}")
    
    print("\n=== Retry Decorator ===")
    try:
        result = unstable_operation()
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Failed after retries: {e}")
    
    print("\n=== Type Validation Decorator ===")
    try:
        student = process_student("Alice", 20, [85, 90, 78])
        print(f"Student: {student}")
        process_student("Bob", "twenty", [80, 85])  # Should fail
    except TypeError as e:
        print(f"Type error: {e}")
    
    print("\n=== Count Calls Decorator ===")
    for _ in range(5):
        increment_counter()
    print(f"Function called {increment_counter.call_count} times")


if __name__ == "__main__":
    main()
