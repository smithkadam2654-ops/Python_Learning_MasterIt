"""
Beginner Project 42: Simple Stopwatch
A command-line stopwatch that tracks time elapsed using the time module.
"""
import time

def main():
    print("Simple Stopwatch")
    print("Press ENTER to start the stopwatch.")
    print("Press ENTER again to stop it.")
    
    input()
    start_time = time.time()
    print("Stopwatch started...")
    
    try:
        input()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Stopwatch stopped! Elapsed time: {elapsed_time:.2f} seconds.")
    except KeyboardInterrupt:
        print("\nStopwatch stopped forcefully.")

if __name__ == "__main__":
    main()
