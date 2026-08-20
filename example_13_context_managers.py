import time
from contextlib import contextmanager

# 1. Class-based Context Manager
class TimerContextManager:
    """A context manager to measure execution time of a code block."""
    def __init__(self, description):
        self.description = description
        
    def __enter__(self):
        print(f"Starting: {self.description}")
        self.start_time = time.time()
        return self # This is bound to the 'as' variable
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        execution_time = self.end_time - self.start_time
        print(f"Finished: {self.description} (took {execution_time:.4f} seconds)")
        
        # If an exception occurred, returning False will propagate it.
        # Returning True would swallow the exception.
        return False

# 2. Generator-based Context Manager using contextlib
@contextmanager
def temp_file_simulator(filename):
    """Simulates creating and automatically cleaning up a temporary file."""
    print(f"\n[Simulator] Creating temporary file '{filename}'...")
    file_object = {"name": filename, "is_open": True}
    
    try:
        # The code inside the 'with' block runs at this yield
        yield file_object
    finally:
        # This code runs when the 'with' block exits, even if exceptions occurred
        print(f"[Simulator] Deleting temporary file '{filename}'...")
        file_object["is_open"] = False

if __name__ == "__main__":
    # Using the class-based context manager
    with TimerContextManager("Simulated Database Query"):
        time.sleep(1.2)
        print("Querying database...")
        
    # Using the generator-based context manager
    with temp_file_simulator("temp_data_export.csv") as f:
        print(f"Writing data to {f['name']}...")
        print(f"Is file open? {f['is_open']}")
