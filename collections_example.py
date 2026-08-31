from collections import Counter, namedtuple
import itertools

def advanced_collections():
    print("--- 1. Using collections.Counter ---")
    # Counter is great for tallying items quickly
    words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
    word_counts = Counter(words)
    print(f"Word tallies: {word_counts}")
    print(f"Most common word: {word_counts.most_common(1)[0]}")
    
    print("\n--- 2. Using collections.namedtuple ---")
    # namedtuple creates a quick, readable class-like object without needing a full 'class' definition
    Point = namedtuple('Point', ['x', 'y'])
    p1 = Point(10, 20)
    p2 = Point(x=5, y=15)
    
    print(f"Point 1: x={p1.x}, y={p1.y}")
    print(f"Point 2: {p2}")
    
    print("\n--- 3. Using itertools ---")
    # itertools provides memory-efficient looping tools
    
    # Permutations (all possible orderings)
    letters = ['A', 'B', 'C']
    perms = list(itertools.permutations(letters, 2))
    print(f"All 2-letter permutations of A,B,C: {perms}")
    
    # Chaining multiple lists together efficiently without creating a new combined list in memory
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    chained = list(itertools.chain(list1, list2))
    print(f"Chained lists: {chained}")

if __name__ == "__main__":
    advanced_collections()
