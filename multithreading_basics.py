import threading
import time

def worker_function(name, delay, count):
    """A simple worker function that simulates a long-running task."""
    print(f"Thread '{name}' starting.")
    for i in range(count):
        time.sleep(delay)
        print(f"Thread '{name}' processing step {i+1}/{count}")
    print(f"Thread '{name}' finished.")

def demonstrate_threading():
    """Run multiple threads concurrently."""
    print("Main program started.")
    
    # Create two threads
    thread1 = threading.Thread(target=worker_function, args=("Worker-A", 0.5, 3))
    thread2 = threading.Thread(target=worker_function, args=("Worker-B", 0.3, 5))
    
    # Start the threads
    thread1.start()
    thread2.start()
    
    # Wait for both threads to finish before the main program exits
    thread1.join()
    thread2.join()
    
    print("Main program finished.")

if __name__ == "__main__":
    demonstrate_threading()
