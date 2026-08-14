import multiprocessing
import time
import math

def compute_factorial(number: int) -> int:
    """CPU-bound task to calculate factorial."""
    print(f"Process {multiprocessing.current_process().name} computing factorial of {number}")
    return math.factorial(number)

def run_synchronous(numbers):
    start_time = time.time()
    results = [compute_factorial(n) for n in numbers]
    print(f"Synchronous execution took {time.time() - start_time:.4f} seconds.")
    return results

def run_parallel(numbers):
    start_time = time.time()
    # Create a pool of workers matching the CPU core count
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        # Map the function to the list of inputs
        results = pool.map(compute_factorial, numbers)
    print(f"Parallel execution took {time.time() - start_time:.4f} seconds.")
    return results

if __name__ == "__main__":
    # We use relatively large numbers to make the CPU work a bit
    test_numbers = [50000, 50000, 50000, 50000]
    
    print("--- Synchronous Execution ---")
    run_synchronous(test_numbers)
    
    print("\n--- Parallel Execution ---")
    run_parallel(test_numbers)
