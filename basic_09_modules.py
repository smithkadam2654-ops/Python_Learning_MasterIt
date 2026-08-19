import math
import random

def main():
    print("Using the 'math' module:")
    print(f"Pi is approximately {math.pi:.4f}")
    print(f"The square root of 16 is {math.sqrt(16)}")
    
    print("\nUsing the 'random' module:")
    # Generate a random integer between 1 and 10
    random_num = random.randint(1, 10)
    print(f"Random number between 1 and 10: {random_num}")
    
    choices = ["Rock", "Paper", "Scissors"]
    print(f"Random choice from list: {random.choice(choices)}")

if __name__ == "__main__":
    main()
