"""
Beginner Project 50: Coin Flipper
A simple script that simulates flipping a coin one or multiple times.
"""
import random

def flip_coin():
    return random.choice(["Heads", "Tails"])

def main():
    print("Coin Flipper")
    
    try:
        flips = int(input("How many times do you want to flip the coin? "))
        
        if flips <= 0:
            print("Please enter a positive integer.")
            return
            
        heads_count = 0
        tails_count = 0
        
        print("\nFlipping...")
        for _ in range(flips):
            result = flip_coin()
            if result == "Heads":
                heads_count += 1
            else:
                tails_count += 1
                
        print(f"\nResults of {flips} flips:")
        print(f"Heads: {heads_count}")
        print(f"Tails: {tails_count}")
        
    except ValueError:
        print("Invalid input! Please enter a whole number.")

if __name__ == "__main__":
    main()
