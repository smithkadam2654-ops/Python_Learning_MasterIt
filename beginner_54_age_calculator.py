"""
Beginner Project 54: Age Calculator
Calculates a person's exact age in years based on their birth year.
"""
from datetime import datetime

def main():
    print("Age Calculator")
    
    try:
        birth_year = int(input("Enter your birth year (e.g., 1990): "))
        current_year = datetime.now().year
        
        if birth_year > current_year:
            print("You can't be born in the future!")
            return
            
        age = current_year - birth_year
        print(f"\nYou are turning (or have turned) {age} years old in {current_year}.")
        
    except ValueError:
        print("Invalid input! Please enter a valid 4-digit year.")

if __name__ == "__main__":
    main()
