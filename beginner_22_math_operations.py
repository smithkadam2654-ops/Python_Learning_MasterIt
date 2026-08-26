import math

def main():
    number = 16.5

    print(f"Original Number: {number}")
    print(f"Ceiling (round up): {math.ceil(number)}")
    print(f"Floor (round down): {math.floor(number)}")
    
    # Using constants from math module
    print(f"Value of Pi: {math.pi}")
    
    # Calculating square root
    val = 25
    print(f"Square root of {val} is {math.sqrt(val)}")
    
    # Power
    print(f"2 to the power of 3: {math.pow(2, 3)}")

if __name__ == "__main__":
    main()
