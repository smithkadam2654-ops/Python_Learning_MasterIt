def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

def multiply(a, b):
    """Returns the product of two numbers."""
    return a * b

def main():
    num1 = 5
    num2 = 10
    
    sum_result = add(num1, num2)
    prod_result = multiply(num1, num2)
    
    print(f"The sum of {num1} and {num2} is {sum_result}.")
    print(f"The product of {num1} and {num2} is {prod_result}.")

if __name__ == "__main__":
    main()
