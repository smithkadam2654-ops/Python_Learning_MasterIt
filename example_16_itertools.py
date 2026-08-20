import itertools
import time

def main():
    """Demonstrates powerful iterators from the itertools module."""
    
    # 1. itertools.count(start, step)
    # Creates an infinite iterator counting upwards
    print("Counting evens (stopping manually at 10):")
    for evens in itertools.count(0, 2):
        print(evens, end=" ")
        if evens >= 10:
            break
    print("\n")
    
    # 2. itertools.cycle(iterable)
    # Cycles through an iterable infinitely
    colors = ["Red", "Green", "Blue"]
    print("Cycling through colors 5 times:")
    color_cycle = itertools.cycle(colors)
    for _ in range(5):
        print(next(color_cycle), end=" ")
    print("\n")
    
    # 3. itertools.combinations(iterable, r)
    # Returns all possible combinations of length r
    letters = ['A', 'B', 'C', 'D']
    print(f"Combinations of length 2 from {letters}:")
    combos = list(itertools.combinations(letters, 2))
    print(combos)
    print()
    
    # 4. itertools.permutations(iterable, r)
    # Returns all possible permutations (order matters!)
    print(f"Permutations of length 2 from {letters[:3]}:")
    perms = list(itertools.permutations(letters[:3], 2))
    print(perms)
    print()
    
    # 5. itertools.groupby(iterable, key)
    # Groups consecutive identical items
    data = [
        ("Animal", "Dog"), ("Animal", "Cat"),
        ("Bird", "Parrot"), ("Bird", "Eagle"),
        ("Animal", "Elephant") # Note: groupby only groups CONSECUTIVE items
    ]
    
    print("Grouping data:")
    # Data must be sorted by the key first for groupby to group ALL identical keys
    data.sort(key=lambda x: x[0]) 
    
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        items = [item[1] for item in group]
        print(f" - {key}: {', '.join(items)}")

if __name__ == "__main__":
    main()
