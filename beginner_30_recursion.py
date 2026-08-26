def main():
    # Recursion is a function calling itself to solve a smaller piece of the problem.
    # Every recursive function must have a "base case" to stop the recursion.

    def factorial(n):
        # Base case: if n is 1 or 0, the factorial is 1
        if n <= 1:
            return 1
        # Recursive case: n * factorial(n - 1)
        else:
            return n * factorial(n - 1)

    number = 5
    print(f"The factorial of {number} is: {factorial(number)}")

    print("\nCountdown using recursion:")
    def countdown(n):
        if n <= 0:
            print("Blastoff!")
        else:
            print(n)
            countdown(n - 1)  # Function calls itself

    countdown(3)

if __name__ == "__main__":
    main()
