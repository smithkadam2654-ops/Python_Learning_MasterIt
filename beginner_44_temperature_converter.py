"""
Beginner Project 44: Temperature Converter
A script to convert temperatures between Celsius and Fahrenheit.
"""

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def main():
    print("Temperature Converter")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    
    choice = input("Choose an option (1 or 2): ").strip()
    
    try:
        if choice == '1':
            c = float(input("Enter temperature in Celsius: "))
            f = celsius_to_fahrenheit(c)
            print(f"{c:.2f}°C is equal to {f:.2f}°F")
        elif choice == '2':
            f = float(input("Enter temperature in Fahrenheit: "))
            c = fahrenheit_to_celsius(f)
            print(f"{f:.2f}°F is equal to {c:.2f}°C")
        else:
            print("Invalid choice. Please select 1 or 2.")
    except ValueError:
        print("Invalid input! Please enter a numerical temperature.")

if __name__ == "__main__":
    main()
