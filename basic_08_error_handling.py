def safe_divide(a, b):
    """Safely divides two numbers, catching potential errors."""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Cannot divide by zero!"
    except TypeError:
        return "Error: Please provide numbers only."

def main():
    print(f"10 / 2 = {safe_divide(10, 2)}")
    print(f"10 / 0 = {safe_divide(10, 0)}")
    print(f"10 / 'a' = {safe_divide(10, 'a')}")

if __name__ == "__main__":
    main()
