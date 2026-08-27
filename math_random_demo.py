import math
import random

def demonstrate_math_and_random():
    """Demonstrate useful functions from the math and random modules."""
    
    print("--- Math Module ---")
    # Constants
    print(f"Pi: {math.pi}")
    print(f"Euler's number (e): {math.e}")
    
    # Common operations
    number = 16.5
    print(f"\nCeiling of {number}: {math.ceil(number)}")
    print(f"Floor of {number}: {math.floor(number)}")
    print(f"Square root of 144: {math.sqrt(144)}")
    
    print("\n--- Random Module ---")
    # Random floats and integers
    print(f"Random float between 0 and 1: {random.random()}")
    print(f"Random integer between 1 and 100: {random.randint(1, 100)}")
    
    # Choosing from a sequence
    options = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
    print(f"\nRandom choice from list: {random.choice(options)}")
    
    # Sampling multiple unique items
    sample = random.sample(options, k=3)
    print(f"Random sample of 3 items: {sample}")
    
    # Shuffling a list in place
    deck = [1, 2, 3, 4, 5]
    random.shuffle(deck)
    print(f"Shuffled deck: {deck}")

if __name__ == "__main__":
    demonstrate_math_and_random()
