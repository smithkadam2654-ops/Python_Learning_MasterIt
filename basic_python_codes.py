#!/usr/bin/env python3
"""
Collection of basic Python codes for learning and practice
"""

def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def is_even(number):
    """Check if a number is even."""
    return number % 2 == 0

def factorial(n):
    """Calculate factorial of a number."""
    if n < 0:
        return "Factorial not defined for negative numbers"
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def reverse_string(text):
    """Reverse a given string."""
    return text[::-1]

def is_palindrome(text):
    """Check if a string is a palindrome."""
    cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
    return cleaned_text == cleaned_text[::-1]

def find_max(numbers):
    """Find the maximum number in a list."""
    if not numbers:
        return None
    return max(numbers)

def main():
    print("=== Basic Python Codes Examples ===\n")
    
    # Example 1: Calculate average
    numbers = [10, 20, 30, 40, 50]
    avg = calculate_average(numbers)
    print(f"Example 1 - Calculate Average:")
    print(f"Numbers: {numbers}")
    print(f"Average: {avg}\n")
    
    # Example 2: Check if number is even
    test_numbers = [4, 7, 12, 15, 22]
    print("Example 2 - Check Even Numbers:")
    for num in test_numbers:
        print(f"{num} is {'even' if is_even(num) else 'odd'}")
    print()
    
    # Example 3: Calculate factorial
    for i in range(6):
        print(f"Example 3 - Factorial of {i}: {factorial(i)}")
    print()
    
    # Example 4: Reverse string
    text = "Hello World"
    reversed_text = reverse_string(text)
    print(f"Example 4 - Reverse String:")
    print(f"Original: {text}")
    print(f"Reversed: {reversed_text}\n")
    
    # Example 5: Check palindrome
    test_words = ["racecar", "hello", "madam", "python"]
    print("Example 5 - Palindrome Check:")
    for word in test_words:
        print(f"'{word}' is {'a' if is_palindrome(word) else 'not a'} palindrome")
    print()
    
    # Example 6: Find maximum
    scores = [85, 92, 78, 95, 87]
    max_score = find_max(scores)
    print(f"Example 6 - Find Maximum:")
    print(f"Numbers: {scores}")
    print(f"Maximum: {max_score}\n")

if __name__ == "__main__":
    main()