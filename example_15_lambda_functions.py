from functools import reduce

def main():
    """Demonstrates lambda functions with map, filter, and reduce."""
    
    # A standard function
    def square(x):
        return x ** 2
        
    # The equivalent lambda function
    square_lambda = lambda x: x ** 2
    
    print(f"Standard function square(5): {square(5)}")
    print(f"Lambda function square(5): {square_lambda(5)}\n")
    
    # Real-world usage: Sorting a list of dictionaries by a specific key
    users = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35}
    ]
    
    # Sort users by age using a lambda
    sorted_users = sorted(users, key=lambda user: user["age"])
    print("Users sorted by age:")
    for user in sorted_users:
        print(f" - {user['name']} ({user['age']})")
        
    print("\n--- Map, Filter, Reduce ---")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Map: apply a function to every item
    # Let's double all the numbers
    doubled = list(map(lambda x: x * 2, numbers))
    print(f"Doubled numbers: {doubled}")
    
    # Filter: keep only items that return True for the condition
    # Let's keep only even numbers
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Even numbers: {evens}")
    
    # Reduce: apply a rolling computation to sequential pairs of values
    # Let's find the product of all numbers
    product = reduce(lambda x, y: x * y, numbers)
    print(f"Product of all numbers: {product}")

if __name__ == "__main__":
    main()
