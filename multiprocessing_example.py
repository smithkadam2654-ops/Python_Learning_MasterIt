import multiprocessing
import time
import math

def compute_heavy_task(number):
    """A CPU-bound task that takes some time."""
    process_name = multiprocessing.current_process().name
    print(f"[{process_name}] Computing factorial of {number}...")
    
    # Math.factorial on large numbers takes a lot of CPU power
    result = math.factorial(number)
    
    # Return the length of the number string, so we don't print massive numbers to the console
    digits = len(str(result))
    
    print(f"[{process_name}] Done! Result has {digits} digits.")
    return digits

def run_multiprocessing():
    print("--- Multiprocessing Demonstration ---")
    print("This will spin up separate Python processes to utilize multiple CPU cores.\n")
    
    numbers_to_compute = [50000, 60000, 70000, 80000]
    
    start_time = time.time()
    
    # Create a Pool of worker processes. 
    # By default, it creates one process for each core on your CPU.
    with multiprocessing.Pool() as pool:
        # pool.map distributes the numbers to the worker processes in parallel.
        # It waits until all processes are done, then returns the results in order.
        results = pool.map(compute_heavy_task, numbers_to_compute)
        
    end_time = time.time()
    
    print(f"\nAll tasks finished in {end_time - start_time:.2f} seconds!")
    print(f"Results (number of digits for each): {results}")

if __name__ == "__main__":
    # NOTE: The 'if __name__ == "__main__":' block is STRICTLY REQUIRED on Windows 
    # for multiprocessing to work without crashing or infinitely looping!
    run_multiprocessing()
