from collections import Counter, defaultdict, namedtuple

def demonstrate_collections():
    """Demonstrate useful data structures from the collections module."""
    
    print("--- Counter ---")
    # Counter is great for tallying elements
    words = ['apple', 'banana', 'apple', 'cherry', 'apple', 'banana']
    word_counts = Counter(words)
    print(f"Counts: {word_counts}")
    print(f"Most common: {word_counts.most_common(1)}")
    
    print("\n--- defaultdict ---")
    # defaultdict provides a default value for missing keys (no KeyError)
    # E.g., defaulting to a list so we can immediately append
    grouped_data = defaultdict(list)
    
    # Group names by their first letter
    names = ["Alice", "Arthur", "Bob", "Charlie", "Cathy"]
    for name in names:
        first_letter = name[0]
        grouped_data[first_letter].append(name)
        
    print(f"Grouped names: {dict(grouped_data)}")
    
    print("\n--- namedtuple ---")
    # namedtuple creates lightweight, memory-efficient classes for data
    Point = namedtuple('Point', ['x', 'y', 'z'])
    p1 = Point(10, 20, z=30)
    
    print(f"Point: {p1}")
    print(f"Accessing x: {p1.x}")
    
    # Note: namedtuples are immutable! 
    # p1.x = 15 # This would raise an AttributeError

if __name__ == "__main__":
    demonstrate_collections()
