def fibonacci_generator(n):
    """A generator that yields the first n Fibonacci numbers."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

if __name__ == "__main__":
    # Generators are memory efficient because they yield items one at a time
    # rather than building the entire list in memory.
    
    print("First 10 Fibonacci numbers:")
    for num in fibonacci_generator(10):
        print(num, end=" ")
    print()
    
    # We can also use generator expressions (similar to list comprehensions)
    squares_gen = (x * x for x in range(1, 6))
    print("\nSquares from a generator expression:")
    for square in squares_gen:
        print(square, end=" ")
    print()
