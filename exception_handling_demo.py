def divide_numbers(a, b):
    """Demonstrate exception handling with try/except/finally."""
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
    except TypeError:
        print("Error: Both arguments must be numbers!")
    else:
        # Executes if no exception was raised
        print(f"The result is {result}")
    finally:
        # Always executes, regardless of exceptions
        print("Execution of divide_numbers completed.\n")

if __name__ == "__main__":
    # Test cases
    print("Test 1: Valid division")
    divide_numbers(10, 2)
    
    print("Test 2: Division by zero")
    divide_numbers(10, 0)
    
    print("Test 3: Invalid types")
    divide_numbers(10, "two")
