import time
import os

def digital_clock():
    try:
        while True:
            # Get current time
            current_time = time.strftime("%H:%M:%S")
            
            # Clear the terminal screen (works on Windows/Linux/Mac)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Print the clock
            print("=" * 20)
            print(f"   {current_time}   ")
            print("=" * 20)
            print("\nPress Ctrl+C to stop.")
            
            # Wait for 1 second before updating
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nClock stopped!")

if __name__ == "__main__":
    digital_clock()
