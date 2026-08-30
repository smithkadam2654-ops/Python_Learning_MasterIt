def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y

if __name__ == "__main__":
    print("Basic Calculator")
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 2 = {subtract(10, 2)}")
    print(f"4 * 6 = {multiply(4, 6)}")
    print(f"15 / 3 = {divide(15, 3)}")
