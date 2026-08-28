def demonstrate_sets():
    """Demonstrate set operations and frozensets."""
    
    # Sets are unordered collections of unique elements
    set_a = {1, 2, 3, 4, 5}
    set_b = {4, 5, 6, 7, 8}
    
    print(f"Set A: {set_a}")
    print(f"Set B: {set_b}")
    
    print("\n--- Set Operations ---")
    # Union: Elements in either A or B
    print(f"Union (A | B): {set_a | set_b}")
    
    # Intersection: Elements in both A and B
    print(f"Intersection (A & B): {set_a & set_b}")
    
    # Difference: Elements in A but NOT in B
    print(f"Difference (A - B): {set_a - set_b}")
    
    # Symmetric Difference: Elements in A or B, but NOT both
    print(f"Symmetric Difference (A ^ B): {set_a ^ set_b}")
    
    print("\n--- Modifying Sets ---")
    set_a.add(10)
    print(f"Added 10 to A: {set_a}")
    
    set_a.remove(1) # Raises KeyError if not found (use .discard() to avoid error)
    print(f"Removed 1 from A: {set_a}")
    
    print("\n--- Frozensets ---")
    # Frozensets are immutable sets (they can't be modified after creation)
    # This means they can be used as dictionary keys or elements of other sets
    frozen = frozenset([1, 2, 3])
    print(f"Frozenset: {frozen}")
    
    # frozen.add(4) # This would raise an AttributeError!
    
    my_dict = {frozen: "This key is a frozenset!"}
    print(f"Dictionary using a frozenset as a key: {my_dict}")

if __name__ == "__main__":
    demonstrate_sets()
