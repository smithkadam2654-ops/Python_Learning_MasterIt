def demonstrate_custom_sorting():
    """Demonstrate sorting using custom keys."""
    
    # 1. Sorting strings by their length instead of alphabetically
    words = ["banana", "pie", "apple", "strawberry", "kiwi"]
    
    print("--- Sorting Strings ---")
    print(f"Original: {words}")
    
    # Default (alphabetical)
    print(f"Alphabetical: {sorted(words)}")
    
    # Custom key (length)
    print(f"By length: {sorted(words, key=len)}")
    
    # 2. Sorting a list of dictionaries
    print("\n--- Sorting Dictionaries ---")
    students = [
        {"name": "Alice", "grade": 85},
        {"name": "Bob", "grade": 92},
        {"name": "Charlie", "grade": 78}
    ]
    
    # To sort dictionaries, we need to tell Python which value to look at
    # We can use a lambda function to extract the 'grade'
    sorted_students = sorted(students, key=lambda s: s["grade"], reverse=True)
    
    print("Students sorted by grade (highest first):")
    for student in sorted_students:
        print(f"{student['name']}: {student['grade']}")
        
    # 3. Sorting complex objects
    print("\n--- Sorting Complex Objects ---")
    class Product:
        def __init__(self, name, price):
            self.name = name
            self.price = price
        def __repr__(self):
            return f"Product({self.name}, ${self.price})"
            
    inventory = [
        Product("Laptop", 1200),
        Product("Mouse", 25),
        Product("Monitor", 300)
    ]
    
    # Sort in place using the list's sort() method
    inventory.sort(key=lambda p: p.price)
    print(f"Inventory sorted by price: {inventory}")

if __name__ == "__main__":
    demonstrate_custom_sorting()
