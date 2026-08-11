#!/usr/bin/env python3
"""
Basic Calculator Program
Performs basic arithmetic operations with user input
"""

def get_number(prompt):
    """Get a number from user input with error handling."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero!"
    return a / b

def main():
    print("=== Basic Calculator ===")
    print("Available operations: +, -, *, /")
    
    try:
        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")
        
        operation = input("Enter operation (+, -, *, /): ")
        
        if operation == '+':
            result = add(num1, num2)
            print(f"Result: {num1} + {num2} = {result}")
        elif operation == '-':
            result = subtract(num1, num2)
            print(f"Result: {num1} - {num2} = {result}")
        elif operation == '*':
            result = multiply(num1, num2)
            print(f"Result: {num1} * {num2} = {result}")
        elif operation == '/':
            result = divide(num1, num2)
            if isinstance(result, str):
                print(result)
            else:
                print(f"Result: {num1} / {num2} = {result}")
        else:
            print("Invalid operation!")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

if __name__ == "__main__":
    main()