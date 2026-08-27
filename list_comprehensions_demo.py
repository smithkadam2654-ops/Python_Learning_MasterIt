def demonstrate_comprehensions():
    """Demonstrate list, dictionary, and set comprehensions."""
    
    # List comprehension: squares of even numbers from 0 to 9
    squares = [x**2 for x in range(10) if x % 2 == 0]
    print(f"Squares of even numbers: {squares}")
    
    # Dictionary comprehension: mapping numbers to their cubes
    cubes_dict = {x: x**3 for x in range(1, 6)}
    print(f"Dictionary of cubes: {cubes_dict}")
    
    # Set comprehension: unique lengths of words
    words = ["hello", "world", "python", "code", "hello", "code"]
    lengths = {len(word) for word in words}
    print(f"Unique word lengths: {lengths}")

if __name__ == "__main__":
    demonstrate_comprehensions()
