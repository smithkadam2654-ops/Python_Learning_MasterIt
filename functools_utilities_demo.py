import functools
import time

# 1. lru_cache: Memoization to speed up function calls
@functools.lru_cache(maxsize=128)
def expensive_computation(n):
    """Simulate a time-consuming calculation."""
    print(f"  [Computing value for {n} taking time...]")
    time.sleep(1) # Simulate slow processing
    return n * n

# 2. wraps: Preserving function metadata when writing decorators
def my_decorator(func):
    @functools.wraps(func) # <--- This is crucial!
    def wrapper(*args, **kwargs):
        """Wrapper function documentation."""
        print(f"Calling {func.__name__}...")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Say hello to someone."""
    return f"Hello, {name}!"

# 3. partial: Freezing some arguments of a function
def power(base, exponent):
    return base ** exponent

# Create a new function that acts like power(base, 2)
square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)

def demonstrate_functools():
    print("--- 1. @functools.lru_cache ---")
    print("First call (will take 1 second):")
    print(f"Result: {expensive_computation(5)}")
    
    print("Second call (should be instant!):")
    print(f"Result: {expensive_computation(5)}")
    
    print("\n--- 2. @functools.wraps ---")
    print(greet("Alice"))
    # Without @wraps, this would print 'wrapper' and 'Wrapper function documentation.'
    print(f"Function Name: {greet.__name__}")
    print(f"Function Doc: {greet.__doc__}")
    
    print("\n--- 3. functools.partial ---")
    print(f"Square of 5: {square(5)}")
    print(f"Cube of 5: {cube(5)}")

if __name__ == "__main__":
    demonstrate_functools()
