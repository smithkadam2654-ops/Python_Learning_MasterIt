import time

# 1. A Decorator example
def timer_decorator(func):
    """A decorator that prints how long a function takes to execute."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds to run.")
        return result
    return wrapper

@timer_decorator
def slow_function():
    print("Starting a slow task...")
    time.sleep(1.5)  # Simulate a time-consuming operation
    print("Finished slow task.")

# 2. A Generator example
def fibonacci_generator(limit):
    """A generator that yields Fibonacci numbers up to a certain limit."""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

if __name__ == "__main__":
    print("--- Decorator Example ---")
    slow_function()
    
    print("\n--- Generator Example ---")
    print("Fibonacci numbers under 50:")
    
    # Generators are evaluated lazily (one at a time), which saves memory!
    for num in fibonacci_generator(50):
        print(num, end=" ")
    print() # Print a newline at the end
