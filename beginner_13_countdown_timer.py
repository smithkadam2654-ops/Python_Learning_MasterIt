import time
import sys

def countdown(seconds):
    print(f"Starting countdown for {seconds} seconds...")
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        sys.stdout.write(f'\r{timer}')
        sys.stdout.flush()
        time.sleep(1)
        seconds -= 1
        
    print("\nTime's up!")

def main():
    while True:
        try:
            time_input = input("Enter time in seconds to countdown (or 'q' to quit): ")
            if time_input.lower() == 'q':
                break
            
            seconds = int(time_input)
            if seconds <= 0:
                print("Please enter a positive number.")
                continue
                
            countdown(seconds)
            
        except ValueError:
            print("Invalid input. Please enter an integer.")

if __name__ == "__main__":
    main()
