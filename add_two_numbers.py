#!/usr/bin/env python3
"""
Simple program to add two numbers entered by the user.
"""

def get_number(prompt):
    """Get a number from user input with error handling."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    """Main function to add two numbers."""
    print("=== Number Addition Program ===")
    print("This program will add two numbers together.")
    
    # Get first number from user
    num1 = get_number("Enter the first number: ")
    
    # Get second number from user
    num2 = get_number("Enter the second number: ")
    
    # Calculate sum
    result = num1 + num2
    
    # Display result
    print(f"\nThe sum of {num1} and {num2} is: {result}")
    
    # If both numbers are integers, show as integer
    if num1.is_integer() and num2.is_integer():
        print(f"As integer: {int(num1)} + {int(num2)} = {int(result)}")

if __name__ == "__main__":
    main()