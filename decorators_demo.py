import time

def timing_decorator(func):
    """A simple decorator that measures execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Starting {func.__name__}...")
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        print(f"Finished {func.__name__} in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

@timing_decorator
def slow_function(delay_seconds):
    """A function that intentionally sleeps to simulate work."""
    print(f"Sleeping for {delay_seconds} seconds...")
    time.sleep(delay_seconds)
    return "Work complete!"

if __name__ == "__main__":
    result = slow_function(1.5)
    print(f"Result: {result}")
