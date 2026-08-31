import threading
import time

# A simple function that simulates a time-consuming task
def worker_task(worker_name, delay):
    print(f"[{worker_name}] Starting task...")
    # Simulate work by sleeping
    time.sleep(delay)
    print(f"[{worker_name}] Finished task!")

def run_threads():
    start_time = time.time()
    
    # Create multiple thread objects
    # They point to our 'worker_task' function and pass arguments to it
    thread1 = threading.Thread(target=worker_task, args=("Thread-1", 2))
    thread2 = threading.Thread(target=worker_task, args=("Thread-2", 3))
    thread3 = threading.Thread(target=worker_task, args=("Thread-3", 1))
    
    print("Main Program: Starting threads...")
    
    # Start the threads (they run concurrently in the background)
    thread1.start()
    thread2.start()
    thread3.start()
    
    # The main program continues immediately without waiting for them to finish!
    print("Main Program: Doing other work while threads run...")
    
    # We use .join() to tell the main program to wait here until the threads are done
    thread1.join()
    thread2.join()
    thread3.join()
    
    end_time = time.time()
    print(f"\nMain Program: All threads completed in {end_time - start_time:.2f} seconds.")
    # Notice it takes ~3 seconds (the longest thread) instead of 2+3+1 = 6 seconds!

if __name__ == "__main__":
    run_threads()
