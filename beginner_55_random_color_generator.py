"""
Beginner Project 55: Random Color Hex Generator
Generates a random hex color code (e.g., #FF5733) commonly used in web design.
"""
import random

def generate_hex_color():
    # Hex characters: 0-9 and A-F
    hex_chars = "0123456789ABCDEF"
    color = "#"
    
    for _ in range(6):
        color += random.choice(hex_chars)
        
    return color

def main():
    print("Random Hex Color Generator")
    print("-" * 30)
    
    while True:
        color = generate_hex_color()
        print(f"Your random color is: {color}")
        
        again = input("Press ENTER for another color, or type 'q' to quit: ").lower().strip()
        if again == 'q':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
