import itertools

def demonstrate_itertools():
    """Demonstrate useful functions from the itertools module."""
    
    print("--- itertools.chain() ---")
    # chain() combines multiple iterables sequentially
    list1 = [1, 2, 3]
    list2 = ['a', 'b', 'c']
    combined = list(itertools.chain(list1, list2))
    print(f"Chained lists: {combined}")
    
    print("\n--- itertools.combinations() ---")
    # combinations() returns all possible sets of items of a specific length (order doesn't matter)
    items = ['A', 'B', 'C', 'D']
    pairs = list(itertools.combinations(items, 2))
    print(f"All possible pairs from {items}:")
    print(pairs)
    
    print("\n--- itertools.permutations() ---")
    # permutations() returns all possible arrangements (order DOES matter)
    arrangements = list(itertools.permutations(['A', 'B', 'C'], 2))
    print(f"All permutations of length 2 from ['A', 'B', 'C']:")
    print(arrangements)
    
    print("\n--- itertools.cycle() ---")
    # cycle() repeats an iterable infinitely
    # We use a counter to break the loop for demonstration
    cycle_gen = itertools.cycle(["Red", "Green", "Blue"])
    print("Cycling through colors 5 times:")
    for _ in range(5):
        print(next(cycle_gen), end=" -> ")
    print("...")

if __name__ == "__main__":
    demonstrate_itertools()
