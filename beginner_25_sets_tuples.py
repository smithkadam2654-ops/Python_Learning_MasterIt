def main():
    # Tuples (Immutable - cannot be changed after creation)
    my_tuple = (10, 20, 30, 20)
    print("Tuple:", my_tuple)
    print("Count of 20 in tuple:", my_tuple.count(20))
    # my_tuple[0] = 50  <-- This would raise a TypeError

    # Sets (Unordered, no duplicate elements)
    my_set = {1, 2, 3, 3, 4, 5, 5}
    print("\nSet (duplicates removed):", my_set)
    
    # Adding and removing from a set
    my_set.add(6)
    my_set.remove(1)
    print("Modified Set:", my_set)

    # Set operations
    set_a = {1, 2, 3}
    set_b = {3, 4, 5}
    print("\nUnion:", set_a | set_b)
    print("Intersection:", set_a & set_b)
    print("Difference (A - B):", set_a - set_b)

if __name__ == "__main__":
    main()
