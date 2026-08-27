def demonstrate_functional_tools():
    """Demonstrate lambda functions along with map() and filter()."""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Original numbers: {numbers}")
    
    # Using lambda with filter() to get only odd numbers
    odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
    print(f"Odd numbers (using filter): {odd_numbers}")
    
    # Using lambda with map() to double the numbers
    doubled = list(map(lambda x: x * 2, numbers))
    print(f"Doubled numbers (using map): {doubled}")
    
    # Combining map() and filter()
    # Double the odd numbers
    doubled_odds = list(map(lambda x: x * 2, filter(lambda x: x % 2 != 0, numbers)))
    print(f"Doubled odd numbers: {doubled_odds}")

if __name__ == "__main__":
    demonstrate_functional_tools()
