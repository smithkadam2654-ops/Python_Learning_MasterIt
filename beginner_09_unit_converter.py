def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def km_to_miles(km):
    return km * 0.621371

def miles_to_km(miles):
    return miles / 0.621371

def main():
    while True:
        print("\n--- Unit Converter ---")
        print("1. Celsius to Fahrenheit")
        print("2. Fahrenheit to Celsius")
        print("3. Kilometers to Miles")
        print("4. Miles to Kilometers")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '5':
            break
            
        if choice in ('1', '2', '3', '4'):
            try:
                value = float(input("Enter value to convert: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
                
            if choice == '1':
                print(f"{value}°C = {celsius_to_fahrenheit(value):.2f}°F")
            elif choice == '2':
                print(f"{value}°F = {fahrenheit_to_celsius(value):.2f}°C")
            elif choice == '3':
                print(f"{value} km = {km_to_miles(value):.2f} miles")
            elif choice == '4':
                print(f"{value} miles = {miles_to_km(value):.2f} km")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
