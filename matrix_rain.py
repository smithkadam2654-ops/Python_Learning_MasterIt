import time
import random
import os

def matrix_rain():
    # A mix of characters for the rain effect
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()_+"
    
    # Try to get the terminal width, default to 80 if it fails
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80
        
    # ANSI escape code for bright green text
    green = '\033[1;32m'
    reset = '\033[0m'
    
    print(green, end='')
    try:
        while True:
            # Generate a random line of characters loaded with lots of spaces for the "falling" look
            line = "".join(random.choice(characters + " " * 15) for _ in range(width))
            print(line)
            time.sleep(0.05)
    except KeyboardInterrupt:
        # Reset color when exiting
        print(reset)
        print("\nDisconnected from the Matrix.")

if __name__ == "__main__":
    # Clear screen first
    os.system('cls' if os.name == 'nt' else 'clear')
    matrix_rain()
