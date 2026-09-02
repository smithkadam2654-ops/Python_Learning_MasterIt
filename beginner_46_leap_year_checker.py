"""
Beginner Project 46: Leap Year Checker
A program that determines if a given year is a leap year.
"""

def is_leap_year(year):
    # A year is a leap year if it is divisible by 4
    # EXCEPT if it is divisible by 100, then it is NOT a leap year
    # UNLESS it is also divisible by 400.
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

def main():
    print("Leap Year Checker")
    
    try:
        year = int(input("Enter a year (e.g., 2024): "))
        
        if year <= 0:
            print("Please enter a valid positive year.")
            return

        if is_leap_year(year):
            print(f"\n{year} is a leap year!")
        else:
            print(f"\n{year} is NOT a leap year.")
            
    except ValueError:
        print("Invalid input! Please enter a valid numerical year.")

if __name__ == "__main__":
    main()
