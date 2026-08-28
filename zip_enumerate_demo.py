def demonstrate_zip_and_enumerate():
    """Demonstrate the useful built-in functions zip() and enumerate()."""
    
    # --- enumerate() ---
    print("--- Using enumerate() ---")
    fruits = ["Apple", "Banana", "Cherry", "Date"]
    
    # Instead of managing a counter variable, enumerate gives you both index and value
    for index, fruit in enumerate(fruits):
        print(f"Item {index}: {fruit}")
        
    print("\nWith a custom starting index:")
    for index, fruit in enumerate(fruits, start=1):
        print(f"Option {index}: {fruit}")
        
    # --- zip() ---
    print("\n--- Using zip() ---")
    names = ["Alice", "Bob", "Charlie"]
    ages = [25, 30, 35]
    cities = ["New York", "London", "Paris"]
    
    # zip() pairs items from multiple iterables together
    for name, age, city in zip(names, ages, cities):
        print(f"{name} is {age} years old and lives in {city}.")
        
    # Note: zip stops when the shortest iterable is exhausted
    print("\nZipping lists of unequal lengths:")
    short_list = [1, 2]
    long_list = ['A', 'B', 'C', 'D']
    for num, letter in zip(short_list, long_list):
        print(f"{num} -> {letter}")

if __name__ == "__main__":
    demonstrate_zip_and_enumerate()
