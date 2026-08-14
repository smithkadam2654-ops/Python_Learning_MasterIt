import time
from contextlib import contextmanager

# 1. Context Manager using a Class
class TimerContext:
    """A context manager that measures execution time."""
    def __init__(self, description: str):
        self.description = description

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        print(f"[{self.description}] Execution time: {self.end - self.start:.4f} seconds")
        # Returning False propagates exceptions, True suppresses them
        return False

# 2. Context Manager using a Generator (contextlib)
@contextmanager
def temporary_file(filename: str):
    """Simulates creating and cleaning up a temporary file."""
    print(f"Creating temporary file: {filename}")
    # Yield the resource to the block
    yield filename
    print(f"Cleaning up temporary file: {filename}")

if __name__ == "__main__":
    print("Testing Class-based Context Manager:")
    with TimerContext("Heavy Computation") as timer:
        # Simulate work
        time.sleep(0.5)
        sum(i * i for i in range(1_000_000))
        
    print("\nTesting Generator-based Context Manager:")
    with temporary_file("test.txt") as temp_file:
        print(f"Writing data to {temp_file}...")
        # Simulate an error to show cleanup still happens
        # raise ValueError("Oops!")
