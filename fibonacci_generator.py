#!/usr/bin/env python3
"""
Fibonacci Sequence Generator
Generates Fibonacci sequences with multiple generation methods
"""

def fibonacci_naive(n: int) -> int:
    """Generate nth Fibonacci number (naive recursive approach)."""
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)

def fibonacci_iterative(n: int) -> int:
    """Generate nth Fibonacci number (iterative approach)."""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_sequence(n: int, method: str = 'iterative') -> list:
    """Generate Fibonacci sequence up to n terms."""
    if method == 'iterative':
        fib_func = fibonacci_iterative
    elif method == 'naive':
        fib_func = fibonacci_naive
    else:
        raise ValueError("Method must be 'iterative' or 'naive'")
    
    return [fib_func(i) for i in range(n)]

def fibonacci_generator(n: int):
    """Generate Fibonacci sequence using yield."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def main():
    print("=== Fibonacci Sequence Generator ===\n")
    
    # Get number of terms
    while True:
        try:
            num_terms = int(input("Enter number of Fibonacci terms to generate: "))
            if num_terms <= 0:
                print("Please enter a positive number!")
                continue
            break
        except ValueError:
            print("Please enter a valid number!")
    
    # Display sequences using different methods
    print(f"\nFibonacci Sequence ({num_terms} terms):")
    fib_seq = fibonacci_sequence(num_terms, 'iterative')
    print(f"Iterative: {fib_seq}")
    
    # Show generator approach
    print(f"Generator: {list(fibonacci_generator(num_terms))}")
    
    # Find specific Fibonacci numbers
    print("\nSpecific Fibonacci numbers:")
    for i in range(min(num_terms, 10)):  # Show first 10
        fib_num = fibonacci_iterative(i)
        print(f"F({i}) = {fib_num}")

if __name__ == "__main__":
    main()