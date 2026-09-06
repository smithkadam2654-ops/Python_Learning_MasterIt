"""
Skip List - Probabilistic data structure for ordered data.
Features: O(log n) search, insert, and delete with probability-based levels.
"""

import random
from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')


class SkipListNode(Generic[T]):
    """Node in skip list."""
    
    def __init__(self, value: T, level: int) -> None:
        """
        Initialize skip list node.
        
        Args:
            value: Node value
            level: Node level (number of forward pointers)
        """
        self.value = value
        self.forward: List[Optional['SkipListNode[T]']] = [None] * (level + 1)
    
    def __str__(self) -> str:
        """String representation."""
        return str(self.value)


class SkipList(Generic[T]):
    """Skip list implementation."""
    
    def __init__(self, max_level: int = 16, probability: float = 0.5) -> None:
        """
        Initialize skip list.
        
        Args:
            max_level: Maximum level for nodes
            probability: Probability of promoting to next level
        """
        self.max_level = max_level
        self.probability = probability
        self.level = 0
        self.head = SkipListNode[T](None, max_level)  # Head node with max level
    
    def _random_level(self) -> int:
        """
        Generate random level for new node.
        
        Returns:
            Random level
        """
        level = 0
        while random.random() < self.probability and level < self.max_level:
            level += 1
        return level
    
    def insert(self, value: T) -> None:
        """
        Insert value into skip list.
        
        Args:
            value: Value to insert
        """
        update = [None] * (self.max_level + 1)
        current = self.head
        
        # Find insertion position
        for i in range(self.level, -1, -1):
            while (current.forward[i] and 
                   current.forward[i].value < value):
                current = current.forward[i]
            update[i] = current
        
        current = current.forward[0]
        
        # If value already exists, update it
        if current and current.value == value:
            return
        
        # Create new node with random level
        new_level = self._random_level()
        
        # Update list level if necessary
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.head
            self.level = new_level
        
        # Create new node
        new_node = SkipListNode(value, new_level)
        
        # Update forward pointers
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node
    
    def search(self, value: T) -> bool:
        """
        Search for value in skip list.
        
        Args:
            value: Value to search
            
        Returns:
            True if found
        """
        current = self.head
        
        for i in range(self.level, -1, -1):
            while (current.forward[i] and 
                   current.forward[i].value < value):
                current = current.forward[i]
        
        current = current.forward[0]
        return current is not None and current.value == value
    
    def delete(self, value: T) -> bool:
        """
        Delete value from skip list.
        
        Args:
            value: Value to delete
            
        Returns:
            True if deleted
        """
        update = [None] * (self.max_level + 1)
        current = self.head
        
        # Find node to delete
        for i in range(self.level, -1, -1):
            while (current.forward[i] and 
                   current.forward[i].value < value):
                current = current.forward[i]
            update[i] = current
        
        current = current.forward[0]
        
        # Value not found
        if not current or current.value != value:
            return False
        
        # Update forward pointers
        for i in range(self.level + 1):
            if update[i].forward[i] != current:
                break
            update[i].forward[i] = current.forward[i]
        
        # Update list level
        while self.level > 0 and self.head.forward[self.level] is None:
            self.level -= 1
        
        return True
    
    def to_list(self) -> List[T]:
        """Convert skip list to sorted list."""
        result = []
        current = self.head.forward[0]
        
        while current:
            result.append(current.value)
            current = current.forward[0]
        
        return result
    
    def is_empty(self) -> bool:
        """Check if skip list is empty."""
        return self.head.forward[0] is None
    
    def size(self) -> int:
        """Get number of elements."""
        count = 0
        current = self.head.forward[0]
        
        while current:
            count += 1
            current = current.forward[0]
        
        return count
    
    def clear(self) -> None:
        """Clear skip list."""
        self.head = SkipListNode[T](None, self.max_level)
        self.level = 0
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return f"SkipList(empty, level={self.level})"
        return f"SkipList({self.to_list()}, level={self.level})"
    
    def __len__(self) -> int:
        """Get length."""
        return self.size()
    
    def __contains__(self, value: T) -> bool:
        """Check if value exists."""
        return self.search(value)


def main() -> None:
    """Demonstrate skip list."""
    
    print("=== Skip List Demo ===")
    
    sl = SkipList[int]()
    
    # Insert
    values = [50, 25, 75, 10, 30, 60, 80]
    for value in values:
        sl.insert(value)
        print(f"Inserted {value}")
    
    print(f"\nSkip list: {sl}")
    print(f"Size: {sl.size()}")
    print(f"Level: {sl.level}")
    
    # Search
    print(f"\n--- Search ---")
    search_values = [25, 30, 100]
    for value in search_values:
        result = sl.search(value)
        print(f"Search {value}: {result}")
    
    # Delete
    print(f"\n--- Delete ---")
    sl.delete(30)
    print(f"After delete(30): {sl}")
    
    sl.delete(10)
    print(f"After delete(10): {sl}")
    
    # To list
    print(f"\nTo list: {sl.to_list()}")
    
    # String skip list
    print("\n=== String Skip List ===")
    str_sl = SkipList[str]()
    
    words = ["banana", "apple", "cherry", "date"]
    for word in words:
        str_sl.insert(word)
    
    print(f"String skip list: {str_sl}")
    print(f"Sorted: {str_sl.to_list()}")
    
    # Contains
    print(f"\n'apple' in list: {'apple' in str_sl}")
    print(f"'grape' in list: {'grape' in str_sl}")
    
    # Clear
    sl.clear()
    print(f"\nAfter clear: {sl}")
    print(f"Is empty: {sl.is_empty()}")
    
    # Performance comparison
    print("\n=== Performance Test ===")
    import time
    
    # Insert many items
    large_sl = SkipList[int]()
    n = 10000
    
    start = time.time()
    for i in range(n):
        large_sl.insert(i)
    insert_time = (time.time() - start) * 1000
    
    print(f"Inserted {n} items in {insert_time:.2f}ms")
    
    # Search
    start = time.time()
    for i in range(n):
        large_sl.search(i)
    search_time = (time.time() - start) * 1000
    
    print(f"Searched {n} items in {search_time:.2f}ms")
    
    # Delete
    start = time.time()
    for i in range(0, n, 2):
        large_sl.delete(i)
    delete_time = (time.time() - start) * 1000
    
    print(f"Deleted {n//2} items in {delete_time:.2f}ms")


if __name__ == "__main__":
    main()
