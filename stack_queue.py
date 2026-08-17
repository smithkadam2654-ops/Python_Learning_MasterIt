"""
Stack and Queue - Implementation of stack and queue data structures.
Features: LIFO and FIFO operations with various implementations.
"""

from typing import Generic, TypeVar, Optional, List, Any
from collections import deque

T = TypeVar('T')


class Stack(Generic[T]):
    """Stack implementation using list (LIFO)."""
    
    def __init__(self) -> None:
        """Initialize an empty stack."""
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """
        Push item onto the stack.
        
        Args:
            item: Item to push
        """
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        """
        Remove and return the top item.
        
        Returns:
            Top item, or None if stack is empty
        """
        if self.is_empty():
            return None
        return self._items.pop()
    
    def peek(self) -> Optional[T]:
        """
        Return the top item without removing it.
        
        Returns:
            Top item, or None if stack is empty
        """
        if self.is_empty():
            return None
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Return the number of items in the stack."""
        return len(self._items)
    
    def __len__(self) -> int:
        """Return the size of the stack."""
        return len(self._items)
    
    def __str__(self) -> str:
        """String representation of the stack."""
        return f"Stack({self._items})"


class Queue(Generic[T]):
    """Queue implementation using deque (FIFO)."""
    
    def __init__(self) -> None:
        """Initialize an empty queue."""
        self._items = deque()
    
    def enqueue(self, item: T) -> None:
        """
        Add item to the back of the queue.
        
        Args:
            item: Item to enqueue
        """
        self._items.append(item)
    
    def dequeue(self) -> Optional[T]:
        """
        Remove and return the front item.
        
        Returns:
            Front item, or None if queue is empty
        """
        if self.is_empty():
            return None
        return self._items.popleft()
    
    def peek(self) -> Optional[T]:
        """
        Return the front item without removing it.
        
        Returns:
            Front item, or None if queue is empty
        """
        if self.is_empty():
            return None
        return self._items[0]
    
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Return the number of items in the queue."""
        return len(self._items)
    
    def __len__(self) -> int:
        """Return the size of the queue."""
        return len(self._items)
    
    def __str__(self) -> str:
        """String representation of the queue."""
        return f"Queue({list(self._items)})"


class CircularQueue(Generic[T]):
    """Circular queue implementation with fixed capacity."""
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize circular queue with given capacity.
        
        Args:
            capacity: Maximum number of items the queue can hold
        """
        self.capacity = capacity
        self._items: List[Optional[T]] = [None] * capacity
        self._front = 0
        self._rear = -1
        self._size = 0
    
    def enqueue(self, item: T) -> bool:
        """
        Add item to the back of the queue.
        
        Args:
            item: Item to enqueue
            
        Returns:
            True if successful, False if queue is full
        """
        if self.is_full():
            return False
        
        self._rear = (self._rear + 1) % self.capacity
        self._items[self._rear] = item
        self._size += 1
        return True
    
    def dequeue(self) -> Optional[T]:
        """
        Remove and return the front item.
        
        Returns:
            Front item, or None if queue is empty
        """
        if self.is_empty():
            return None
        
        item = self._items[self._front]
        self._items[self._front] = None
        self._front = (self._front + 1) % self.capacity
        self._size -= 1
        return item
    
    def peek(self) -> Optional[T]:
        """
        Return the front item without removing it.
        
        Returns:
            Front item, or None if queue is empty
        """
        if self.is_empty():
            return None
        return self._items[self._front]
    
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return self._size == 0
    
    def is_full(self) -> bool:
        """Check if the queue is full."""
        return self._size == self.capacity
    
    def size(self) -> int:
        """Return the number of items in the queue."""
        return self._size
    
    def __len__(self) -> int:
        """Return the size of the queue."""
        return self._size
    
    def __str__(self) -> str:
        """String representation of the circular queue."""
        items = []
        for i in range(self._size):
            idx = (self._front + i) % self.capacity
            items.append(str(self._items[idx]))
        return f"CircularQueue({items})"


class PriorityQueue(Generic[T]):
    """Priority queue implementation (min-heap behavior)."""
    
    def __init__(self) -> None:
        """Initialize an empty priority queue."""
        self._items: List[Tuple[int, T]] = []
    
    def enqueue(self, item: T, priority: int) -> None:
        """
        Add item with given priority (lower number = higher priority).
        
        Args:
            item: Item to enqueue
            priority: Priority value (lower = higher priority)
        """
        self._items.append((priority, item))
        self._items.sort(key=lambda x: x[0])
    
    def dequeue(self) -> Optional[T]:
        """
        Remove and return the highest priority item.
        
        Returns:
            Highest priority item, or None if queue is empty
        """
        if self.is_empty():
            return None
        return self._items.pop(0)[1]
    
    def peek(self) -> Optional[T]:
        """
        Return the highest priority item without removing it.
        
        Returns:
            Highest priority item, or None if queue is empty
        """
        if self.is_empty():
            return None
        return self._items[0][1]
    
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Return the number of items in the queue."""
        return len(self._items)
    
    def __len__(self) -> int:
        """Return the size of the priority queue."""
        return len(self._items)
    
    def __str__(self) -> str:
        """String representation of the priority queue."""
        items = [f"({p}: {v})" for p, v in self._items]
        return f"PriorityQueue([{', '.join(items)}])"


def is_valid_parentheses(s: str) -> bool:
    """
    Check if a string has valid parentheses using stack.
    
    Args:
        s: String containing parentheses
        
    Returns:
        True if parentheses are valid, False otherwise
    """
    stack = Stack[str]()
    pairs = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in '({[':
            stack.push(char)
        elif char in ')}]':
            if stack.is_empty() or stack.pop() != pairs[char]:
                return False
    
    return stack.is_empty()


def reverse_string(s: str) -> str:
    """
    Reverse a string using stack.
    
    Args:
        s: String to reverse
        
    Returns:
        Reversed string
    """
    stack = Stack[str]()
    
    for char in s:
        stack.push(char)
    
    result = []
    while not stack.is_empty():
        result.append(stack.pop())
    
    return ''.join(result)


def main() -> None:
    """Demonstrate stack and queue operations."""
    
    print("=== Stack Operations ===")
    stack = Stack[int]()
    
    for i in range(1, 6):
        stack.push(i)
        print(f"Push {i}: {stack}")
    
    print(f"Peek: {stack.peek()}")
    print(f"Size: {stack.size()}")
    
    while not stack.is_empty():
        item = stack.pop()
        print(f"Pop {item}: {stack}")
    
    print("\n=== Queue Operations ===")
    queue = Queue[str]()
    
    for item in ["Alice", "Bob", "Charlie", "David"]:
        queue.enqueue(item)
        print(f"Enqueue {item}: {queue}")
    
    print(f"Peek: {queue.peek()}")
    print(f"Size: {queue.size()}")
    
    while not queue.is_empty():
        item = queue.dequeue()
        print(f"Dequeue {item}: {queue}")
    
    print("\n=== Circular Queue ===")
    cq = CircularQueue[int](3)
    
    print(f"Enqueue 1: {cq.enqueue(1)}")
    print(f"Enqueue 2: {cq.enqueue(2)}")
    print(f"Enqueue 3: {cq.enqueue(3)}")
    print(f"Enqueue 4 (full): {cq.enqueue(4)}")
    print(f"Circular queue: {cq}")
    
    print(f"Dequeue: {cq.dequeue()}")
    print(f"Enqueue 4: {cq.enqueue(4)}")
    print(f"Circular queue: {cq}")
    
    print("\n=== Priority Queue ===")
    pq = PriorityQueue[str]()
    
    pq.enqueue("Task A", 3)
    pq.enqueue("Task B", 1)
    pq.enqueue("Task C", 2)
    pq.enqueue("Task D", 0)
    
    print(f"Priority queue: {pq}")
    
    while not pq.is_empty():
        item = pq.dequeue()
        print(f"Dequeue: {item}")
    
    print("\n=== Stack Applications ===")
    
    # Valid parentheses
    test_strings = ["()", "()[]{}", "(]", "([{}])", "((())"]
    for s in test_strings:
        valid = is_valid_parentheses(s)
        print(f"is_valid_parentheses('{s}'): {valid}")
    
    # Reverse string
    original = "Hello, World!"
    reversed_str = reverse_string(original)
    print(f"\nOriginal: {original}")
    print(f"Reversed: {reversed_str}")


if __name__ == "__main__":
    main()
