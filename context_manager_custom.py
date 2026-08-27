class TimerContextManager:
    """A custom context manager to measure execution time."""
    
    def __init__(self, description):
        self.description = description
        
    def __enter__(self):
        import time
        self.start_time = time.time()
        print(f"Starting: {self.description}")
        return self # We can return an object to use with 'as' keyword
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        
        if exc_type is not None:
            print(f"Failed: {self.description} (Exception: {exc_val})")
        else:
            print(f"Finished: {self.description} in {duration:.4f} seconds")
            
        # Return False to propagate exceptions, True to suppress them
        return False

def demonstrate_context_manager():
    """Demonstrate using the custom context manager."""
    import time
    
    # Normal execution
    with TimerContextManager("Simulated Work"):
        time.sleep(0.5)
        
    print("-" * 20)
    
    # Execution with an exception
    try:
        with TimerContextManager("Failing Work"):
            time.sleep(0.2)
            raise ValueError("Something went wrong!")
    except ValueError as e:
        print(f"Caught exception outside: {e}")

if __name__ == "__main__":
    demonstrate_context_manager()
