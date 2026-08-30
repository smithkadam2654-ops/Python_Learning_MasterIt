def safe_divide(a, b):
    try:
        # Attempt to perform the division
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None
    except TypeError:
        print("Error: Please provide numbers only.")
        return None
    else:
        # This block runs only if NO exception was raised in the try block
        print("Division successful.")
        return result
    finally:
        # This block ALWAYS runs, whether an exception happened or not
        print("Finished attempting division.\n")

if __name__ == "__main__":
    print("Test 1: Normal Division")
    print(f"Result: {safe_divide(10, 2)}")
    
    print("Test 2: Division by Zero")
    print(f"Result: {safe_divide(10, 0)}")
    
    print("Test 3: Invalid Types")
    print(f"Result: {safe_divide(10, 'two')}")
