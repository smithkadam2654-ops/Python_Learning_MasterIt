import time
import os

def pomodoro_timer(minutes):
    seconds = minutes * 60
    
    print(f"--- Pomodoro Timer Started: {minutes} minutes ---")
    print("Focus on your task! Do not get distracted.")
    
    try:
        while seconds > 0:
            # Calculate minutes and seconds remaining
            mins, secs = divmod(seconds, 60)
            timer = f'{mins:02d}:{secs:02d}'
            
            # Print over the same line using \r (carriage return)
            print(f"\rTime remaining: {timer}", end="")
            
            time.sleep(1)
            seconds -= 1
            
        print("\n\nTime's up! Great job. Take a 5 minute break.")
        
        # Try to play an alert sound (works on Windows)
        if os.name == 'nt':
            import winsound
            winsound.Beep(1000, 1000) # frequency 1000Hz, duration 1000ms
            
    except KeyboardInterrupt:
        print("\n\nTimer stopped early. Taking a break?")

if __name__ == "__main__":
    # Standard pomodoro is 25 minutes, but we'll ask the user
    try:
        user_input = input("Enter minutes for Pomodoro session (default 25): ")
        mins = int(user_input) if user_input.strip() else 25
        pomodoro_timer(mins)
    except ValueError:
        print("Invalid input. Using default 25 minutes.")
        pomodoro_timer(25)
