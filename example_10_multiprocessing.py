import multiprocessing
import time

def cpu_heavy_task(name, iterations):
    """Simulates a CPU-bound task that takes time to compute."""
    print(f"Task '{name}' starting...")
    result = 0
    for i in range(iterations):
        result += i * i
    print(f"Task '{name}' completed!")
    return result

if __name__ == "__main__":
    # Protects the entry point for multiprocessing on Windows
    print("Starting multiprocessing demo...")
    start_time = time.time()
    
    # Define arguments for 3 processes
    tasks = [
        ("Task A", 20_000_000),
        ("Task B", 20_000_000),
        ("Task C", 20_000_000)
    ]
    
    # Create a pool of worker processes
    # Using 'with' ensures the pool is properly cleaned up
    with multiprocessing.Pool(processes=3) as pool:
        # Map applies the function to all items in the iterable concurrently
        # We use starmap because our function takes multiple arguments
        results = pool.starmap(cpu_heavy_task, tasks)
        
    end_time = time.time()
    
    print(f"\nAll processes finished in {end_time - start_time:.2f} seconds")
    # Note: Running these sequentially would take roughly 3 times as long!
