"""
Advanced Python - Lesson 01: Decorator Patterns
===============================================
Decorators are functions that modify the behavior of other functions or classes.
They are a powerful tool for code reuse, logging, access control, and more.

Topics Covered:
- Basic decorator recap
- Decorators with arguments
- Class-based decorators
- Decorator factories (parameterized decorators)
- Stacking multiple decorators
- Preserving metadata with functools.wraps
"""

import functools
import time
import logging
from typing import Any, Callable, TypeVar

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


# ============================================================
# 1. BASIC DECORATOR WITH FUNTOOLS.WRAPS
# ============================================================
def timer(func: F) -> F:
    """Decorator that measures execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"'{func.__name__}' executed in {elapsed:.6f} seconds")
        return result
    return wrapper


@timer
def slow_computation(n: int) -> int:
    """Simulate a slow computation."""
    total = sum(i * i for i in range(n))
    return total


# ============================================================
# 2. DECORATOR WITH ARGUMENTS (Decorator Factory)
# ============================================================
def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator factory: retries a function on failure.
    
    Usage:
        @retry(max_attempts=5, delay=0.5)
        def unstable_function():
            ...
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} for '{func.__name__}' "
                        f"failed: {e}"
                    )
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


# Simulated counter for demo
_call_count = 0

@retry(max_attempts=3, delay=0.1)
def unstable_network_call():
    """Simulates a flaky network call that fails sometimes."""
    global _call_count
    _call_count += 1
    if _call_count < 3:
        raise ConnectionError("Network timeout")
    return {"status": "success", "data": [1, 2, 3]}


# ============================================================
# 3. CLASS-BASED DECORATOR
# ============================================================
class CountCalls:
    """Decorator that counts how many times a function is called.
    
    Class-based decorators are useful when you need to maintain state
    across calls without using global variables.
    """
    def __init__(self, func: F):
        functools.update_wrapper(self, func)
        self.func = func
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        logger.info(f"Call #{self.call_count} of '{self.func.__name__}'")
        return self.func(*args, **kwargs)

    def reset(self):
        """Reset the call counter."""
        self.call_count = 0


@CountCalls
def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"


# ============================================================
# 4. DECORATOR WITH STATE AND CONFIGURATION
# ============================================================
class RateLimiter:
    """Rate-limit decorator that prevents a function from being
    called more than `max_calls` times within `period` seconds.
    """
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls: list[float] = []

    def __call__(self, func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.perf_counter()
            # Remove expired timestamps
            self.calls = [t for t in self.calls if now - t < self.period]
            if len(self.calls) >= self.max_calls:
                raise RuntimeError(
                    f"Rate limit exceeded: {self.max_calls} calls per "
                    f"{self.period}s for '{func.__name__}'"
                )
            self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper


@RateLimiter(max_calls=3, period=1.0)
def send_message(text: str) -> str:
    """Simulate sending a message with rate limiting."""
    return f"Sent: {text}"


# ============================================================
# 5. STACKING MULTIPLE DECORATORS
# ============================================================
def log_args(func: F) -> F:
    """Decorator that logs function arguments."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling '{func.__name__}' with args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper


def validate_positive(func: F) -> F:
    """Decorator that validates all numeric args are positive."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args):
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Argument at position {i} must be positive, got {arg}")
        for key, val in kwargs.items():
            if isinstance(val, (int, float)) and val < 0:
                raise ValueError(f"Keyword argument '{key}' must be positive, got {val}")
        return func(*args, **kwargs)
    return wrapper


# Decorators are applied bottom-up:
# validate_positive runs first, then log_args, then timer
@timer
@log_args
@validate_positive
def calculate_area(width: float, height: float) -> float:
    """Calculate rectangle area."""
    return width * height


# ============================================================
# 6. CACHING DECORATOR (Memoization)
# ============================================================
def memoize(func: F) -> F:
    """Custom caching decorator for expensive computations.
    
    Note: Python's functools.lru_cache does this better in production.
    This is for educational purposes.
    """
    cache: dict[tuple, Any] = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
            logger.info(f"Cache MISS for {func.__name__}{args}")
        else:
            logger.info(f"Cache HIT for {func.__name__}{args}")
        return cache[args]

    wrapper.cache = cache  # type: ignore
    wrapper.clear_cache = lambda: cache.clear()  # type: ignore
    return wrapper


@memoize
def fibonacci(n: int) -> int:
    """Compute the nth Fibonacci number (with caching)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ============================================================
# 7. AUTHORIZATION DECORATOR
# ============================================================
def requires_role(role: str):
    """Decorator factory that checks if the current user has the required role.
    
    Demonstrates a real-world use case for access control.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(user: dict, *args, **kwargs):
            if role not in user.get("roles", []):
                raise PermissionError(
                    f"User '{user['name']}' lacks required role '{role}' "
                    f"to access '{func.__name__}'"
                )
            return func(user, *args, **kwargs)
        return wrapper
    return decorator


@requires_role("admin")
def delete_user(user: dict, target_user_id: int) -> str:
    """Delete a user (admin-only operation)."""
    return f"Admin '{user['name']}' deleted user #{target_user_id}"


@requires_role("editor")
def publish_article(user: dict, article_title: str) -> str:
    """Publish an article (editor+ operation)."""
    return f"Editor '{user['name']}' published '{article_title}'"


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Timer Decorator")
    result = slow_computation(1_000_000)
    print(f"Result: {result}")

    separator("2. Retry Decorator")
    global _call_count
    _call_count = 0
    result = unstable_network_call()
    print(f"Result: {result}")

    separator("3. Class-Based Decorator (CountCalls)")
    print(greet("Alice"))
    print(greet("Bob"))
    print(greet("Charlie"))
    print(f"Total calls: {greet.call_count}")
    greet.reset()
    print(f"After reset: {greet.call_count}")

    separator("4. Rate Limiter")
    for i in range(3):
        print(send_message(f"Message {i + 1}"))
    try:
        send_message("Too fast!")
    except RuntimeError as e:
        print(f"Error: {e}")

    separator("5. Stacked Decorators")
    area = calculate_area(5.0, 3.0)
    print(f"Area: {area}")
    try:
        calculate_area(-2.0, 3.0)
    except ValueError as e:
        print(f"Validation error: {e}")

    separator("6. Memoize Decorator")
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"fibonacci(20) = {fibonacci(20)}")
    print(f"Cache size: {len(fibonacci.cache)}")

    separator("7. Authorization Decorator")
    admin = {"name": "Alice", "roles": ["admin", "editor"]}
    editor = {"name": "Bob", "roles": ["editor"]}
    viewer = {"name": "Charlie", "roles": ["viewer"]}

    print(delete_user(admin, 42))
    print(publish_article(editor, "Python Tips"))
    try:
        delete_user(viewer, 42)
    except PermissionError as e:
        print(f"Access denied: {e}")

    separator("Metadata Preservation")
    print(f"slow_computation name: {slow_computation.__name__}")
    print(f"greet name: {greet.__name__}")
    print(f"calculate_area doc: {calculate_area.__doc__}")


if __name__ == "__main__":
    main()
