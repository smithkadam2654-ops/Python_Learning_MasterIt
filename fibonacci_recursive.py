def fibonacci(n):
    """Return the nth Fibonacci number using recursion."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Example usage
if __name__ == "__main__":
    terms = 10
    print(f"The first {terms} terms of the Fibonacci sequence are:")
    for i in range(terms):
        print(fibonacci(i), end=" ")
    print()
