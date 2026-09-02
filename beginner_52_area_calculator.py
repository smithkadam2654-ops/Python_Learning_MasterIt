"""
Beginner Project 52: Area Calculator
A menu-driven program to calculate the area of various shapes.
"""
import math

def area_rectangle(length, width):
    return length * width

def area_circle(radius):
    return math.pi * (radius ** 2)

def area_triangle(base, height):
    return 0.5 * base * height

def main():
    print("Area Calculator")
    print("1. Rectangle")
    print("2. Circle")
    print("3. Triangle")
    
    choice = input("\nChoose a shape (1/2/3): ").strip()
    
    try:
        if choice == '1':
            l = float(input("Enter length: "))
            w = float(input("Enter width: "))
            print(f"Area of Rectangle: {area_rectangle(l, w):.2f}")
            
        elif choice == '2':
            r = float(input("Enter radius: "))
            print(f"Area of Circle: {area_circle(r):.2f}")
            
        elif choice == '3':
            b = float(input("Enter base: "))
            h = float(input("Enter height: "))
            print(f"Area of Triangle: {area_triangle(b, h):.2f}")
            
        else:
            print("Invalid choice.")
            
    except ValueError:
        print("Invalid input! Please enter numerical values.")

if __name__ == "__main__":
    main()
