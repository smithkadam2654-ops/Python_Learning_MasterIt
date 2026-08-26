def divide_numbers(a, b):
    try:
        # Try to perform the division
        result = a / b
        print(f"The result of {a} / {b} is {result}")
    except ZeroDivisionError:
        # Catch a specific error when dividing by zero
        print("Error: Cannot divide by zero!")
    except TypeError:
        # Catch an error when input types are wrong
        print("Error: Both arguments must be numbers.")
    finally:
        # This block always executes, whether an exception occurred or not
        print("Execution of divide_numbers completed.\n")

if __name__ == "__main__":
    print("Test 1: Normal Division")
    divide_numbers(10, 2)
    
    print("Test 2: Division by Zero")
    divide_numbers(5, 0)
    
    print("Test 3: Incorrect Data Types")
    divide_numbers(10, "two")
