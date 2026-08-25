import time
import datetime

def set_alarm():
    print("--- Simple Alarm Clock ---")
    print("Current time:", datetime.datetime.now().strftime("%H:%M:%S"))
    
    alarm_time = input("Enter alarm time (HH:MM:SS in 24-hour format): ")
    
    try:
        # Validate format
        datetime.datetime.strptime(alarm_time, "%H:%M:%S")
    except ValueError:
        print("Invalid time format. Please use HH:MM:SS")
        return
        
    print(f"Alarm set for {alarm_time}. Waiting...")
    
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if current_time == alarm_time:
            print("\n" + "="*20)
            print("WAKE UP! ALARM RINGING!")
            print("="*20)
            
            # Beep 5 times (frequency, duration in milliseconds)
            try:
                import winsound
                for _ in range(5):
                    winsound.Beep(1000, 1000) 
            except ImportError:
                for _ in range(5):
                    print("\a", end="") # ASCII Bell
                    time.sleep(1)
            break
        # Sleep slightly less than 1 second to avoid missing the exact second
        time.sleep(0.5)

if __name__ == "__main__":
    set_alarm()
