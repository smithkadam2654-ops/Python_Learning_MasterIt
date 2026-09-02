"""
Beginner Project 51: Random Quote Generator
Displays a random motivational quote from a predefined list.
"""
import random

QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Everything you've ever wanted is on the other side of fear. - George Addair",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "Hardships often prepare ordinary people for an extraordinary destiny. - C.S. Lewis"
]

def main():
    print("Random Quote Generator")
    print("-" * 30)
    
    while True:
        quote = random.choice(QUOTES)
        print(f"\n{quote}\n")
        
        again = input("Press ENTER for another quote, or type 'q' to quit: ").lower().strip()
        if again == 'q':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
