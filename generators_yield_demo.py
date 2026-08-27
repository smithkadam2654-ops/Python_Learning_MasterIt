def fibonacci_generator(limit):
    """A generator function that yields Fibonacci numbers up to a limit."""
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

def demonstrate_generators():
    """Demonstrate how to use the generator."""
    # Using the generator in a loop
    print("First 10 Fibonacci numbers:")
    for num in fibonacci_generator(10):
        print(num, end=" ")
    print()

    # Generators evaluate lazily, saving memory
    gen = fibonacci_generator(5)
    print("\nGetting values manually:")
    print(next(gen))
    print(next(gen))
    print(next(gen))

if __name__ == "__main__":
    demonstrate_generators()
