import itertools

def main():
    # The itertools module provides fast, memory-efficient tools for iteration
    
    print("1. itertools.count(start, step) - Infinite counting")
    # count() creates an infinite iterator, so we use zip to limit it
    for i, count in zip(range(5), itertools.count(10, 2)):
        print(count)
        
    print("\n2. itertools.cycle(iterable) - Infinite looping")
    # cycle() loops over an iterable indefinitely
    colors = ["Red", "Green", "Blue"]
    for i, color in zip(range(7), itertools.cycle(colors)):
        print(color)
        
    print("\n3. itertools.combinations(iterable, r) - All possible combinations")
    # combinations() returns all possible groups of size 'r'
    items = ["A", "B", "C", "D"]
    combos = list(itertools.combinations(items, 2))
    print(f"Combinations of 2 from {items}:")
    for combo in combos:
        print(combo)

if __name__ == "__main__":
    main()
