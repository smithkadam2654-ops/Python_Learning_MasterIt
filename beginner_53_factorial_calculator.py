"""
Beginner Project 53: Factorial Calculator
Calculates the factorial of a given number using a simple loop.
"""

def calculate_factorial(n):
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def main():
    print("Factorial Calculator")
    
    try:
        num = int(input("Enter a non-negative integer: "))
        
        if num < 0:
            print("Factorial is not defined for negative numbers.")
            return
            
        fact = calculate_factorial(num)
        print(f"\nThe factorial of {num} is: {fact}")
        
    except ValueError:
        print("Invalid input! Please enter a whole number.")

if __name__ == "__main__":
    main()
