# This script demonstrates how to define and use functions in Python.

def greet(name, greeting="Hello"):
    """This function greets a person with a given greeting."""
    print(f"{greeting}, {name}!")

def calculate_area(length, width):
    """This function calculates and returns the area of a rectangle."""
    return length * width

# Calling the functions
# Using the default greeting
greet("Alice")

# Providing a custom greeting
greet("Bob", "Good morning")

# Calling a function that returns a value
rect_length = 5
rect_width = 10
area = calculate_area(rect_length, rect_width)
print(f"The area of a rectangle with length {rect_length} and width {rect_width} is {area}.")
