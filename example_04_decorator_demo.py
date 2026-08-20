import time
from functools import wraps

def time_it(func):
    """A decorator that measures the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Call the original function
        result = func(*args, **kwargs)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
        return result
    return wrapper

@time_it
def slow_function(delay_seconds):
    """A function that intentionally sleeps to simulate a slow process."""
    print(f"Starting slow operation (sleeping for {delay_seconds}s)...")
    time.sleep(delay_seconds)
    print("Operation complete!")

@time_it
def compute_squares(n):
    """Computes the squares of numbers up to n."""
    return [i * i for i in range(n)]

if __name__ == "__main__":
    slow_function(1.5)
    print("---")
    
    squares = compute_squares(1_000_000)
    print(f"Computed {len(squares)} squares.")
