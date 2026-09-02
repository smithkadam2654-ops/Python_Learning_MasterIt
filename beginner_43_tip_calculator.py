"""
Beginner Project 43: Tip Calculator
A simple program to calculate the tip and total bill per person.
"""

def main():
    print("Welcome to the Tip Calculator!")
    
    try:
        bill = float(input("What was the total bill? $"))
        tip_percentage = float(input("What percentage tip would you like to give? (e.g., 10, 15, 20): "))
        people = int(input("How many people are splitting the bill? "))
        
        if bill < 0 or tip_percentage < 0 or people <= 0:
            print("Please enter valid positive numbers.")
            return

        tip_amount = bill * (tip_percentage / 100)
        total_bill = bill + tip_amount
        amount_per_person = total_bill / people
        
        print(f"\nTotal tip amount: ${tip_amount:.2f}")
        print(f"Total bill including tip: ${total_bill:.2f}")
        print(f"Each person should pay: ${amount_per_person:.2f}")
        
    except ValueError:
        print("Invalid input! Please enter numbers only.")

if __name__ == "__main__":
    main()
