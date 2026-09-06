"""
Queue Data Structure - Queue implementation with multiple operations.
Features: Enqueue, dequeue, peek, circular queue, and priority queue.
"""

from typing import Optional, TypeVar, Generic, List
import heapq

T = TypeVar('T')


class Queue(Generic[T]):
    """Queue implementation using list."""
    
    def __init__(self) -> None:
        """Initialize queue."""
        self._items: List[T] = []
    
    def enqueue(self, item: T) -> None:
        """
        Add item to back of queue.
        
        Args:
            item: Item to enqueue
        """
        self._items.append(item)
    
    def dequeue(self) -> Optional[T]:
        """
        Remove item from front of queue.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        return self._items.pop(0)
    
    def peek(self) -> Optional[T]:
        """
        Peek at front item without removing.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        return self._items[0]
    
    def peek_back(self) -> Optional[T]:
        """
        Peek at back item without removing.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Get queue size."""
        return len(self._items)
    
    def clear(self) -> None:
        """Clear queue."""
        self._items.clear()
    
    def to_list(self) -> List[T]:
        """Convert queue to list."""
        return self._items.copy()
    
    def __len__(self) -> int:
        """Get length."""
        return len(self._items)
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return "Queue(empty)"
        return f"Queue({self._items})"


class CircularQueue(Generic[T]):
    """Circular queue implementation."""
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize circular queue.
        
        Args:
            capacity: Maximum capacity
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.capacity = capacity
        self._items: List[Optional[T]] = [None] * capacity
        self._front = 0
        self._rear = -1
        self._size = 0
    
    def enqueue(self, item: T) -> bool:
        """
        Add item to queue.
        
        Args:
            item: Item to enqueue
            
        Returns:
            True if successful, False if full
        """
        if self.is_full():
            return False
        
        self._rear = (self._rear + 1) % self.capacity
        self._items[self._rear] = item
        self._size += 1
        return True
    
    def dequeue(self) -> Optional[T]:
        """
        Remove item from front.
        
        Returns:
            Item or None if empty
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
        Peek at front item.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        return self._items[self._front]
    
    def is_empty(self) -> bool:
        """Check if empty."""
        return self._size == 0
    
    def is_full(self) -> bool:
        """Check if full."""
        return self._size == self.capacity
    
    def size(self) -> int:
        """Get size."""
        return self._size
    
    def clear(self) -> None:
        """Clear queue."""
        self._items = [None] * self.capacity
        self._front = 0
        self._rear = -1
        self._size = 0
    
    def to_list(self) -> List[T]:
        """Convert to list."""
        result = []
        for i in range(self._size):
            index = (self._front + i) % self.capacity
            item = self._items[index]
            if item is not None:
                result.append(item)
        return result
    
    def __len__(self) -> int:
        """Get length."""
        return self._size
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return f"CircularQueue(empty, capacity={self.capacity})"
        return f"CircularQueue({self.to_list()}, capacity={self.capacity})"


class PriorityQueue(Generic[T]):
    """Priority queue implementation using heap."""
    
    def __init__(self) -> None:
        """Initialize priority queue."""
        self._heap: List[tuple] = []
        self._counter = 0
    
    def enqueue(self, item: T, priority: int) -> None:
        """
        Add item with priority.
        
        Args:
            item: Item to enqueue
            priority: Priority (lower = higher priority)
        """
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1
    
    def dequeue(self) -> Optional[T]:
        """
        Remove highest priority item.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        return heapq.heappop(self._heap)[2]
    
    def peek(self) -> Optional[T]:
        """
        Peek at highest priority item.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        return self._heap[0][2]
    
    def is_empty(self) -> bool:
        """Check if empty."""
        return len(self._heap) == 0
    
    def size(self) -> int:
        """Get size."""
        return len(self._heap)
    
    def clear(self) -> None:
        """Clear queue."""
        self._heap.clear()
        self._counter = 0
    
    def to_list(self) -> List[T]:
        """Convert to list (sorted by priority)."""
        return [item for _, _, item in sorted(self._heap)]
    
    def __len__(self) -> int:
        """Get length."""
        return len(self._heap)
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return "PriorityQueue(empty)"
        items = [(p, item) for p, _, item in sorted(self._heap)]
        return f"PriorityQueue({items})"


def main() -> None:
    """Demonstrate queue."""
    
    print("=== Queue Demo ===")
    
    queue = Queue[int]()
    
    # Enqueue
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    print(f"After enqueue(10, 20, 30): {queue}")
    
    # Peek
    print(f"Peek: {queue.peek()}")
    print(f"Peek back: {queue.peek_back()}")
    
    # Dequeue
    print(f"Dequeue: {queue.dequeue()}")
    print(f"After dequeue: {queue}")
    
    # Size
    print(f"Size: {queue.size()}")
    
    # Is empty
    print(f"Is empty: {queue.is_empty()}")
    
    # To list
    print(f"To list: {queue.to_list()}")
    
    # Clear
    queue.clear()
    print(f"After clear: {queue}")
    print(f"Is empty: {queue.is_empty()}")
    
    # String queue
    print("\n=== String Queue ===")
    str_queue = Queue[str]()
    
    str_queue.enqueue("Hello")
    str_queue.enqueue("World")
    str_queue.enqueue("Python")
    print(f"String queue: {str_queue}")
    
    # Circular queue
    print("\n=== Circular Queue Demo ===")
    circular = CircularQueue[int](3)
    
    for i in range(3):
        result = circular.enqueue(i * 10)
        print(f"Enqueue {i * 10}: {circular}, Success: {result}")
    
    print(f"Is full: {circular.is_full()}")
    
    result = circular.enqueue(40)
    print(f"Enqueue 40 (full): Success: {result}")
    
    print(f"\nDequeue: {circular.dequeue()}")
    print(f"After dequeue: {circular}")
    
    result = circular.enqueue(40)
    print(f"Enqueue 40: Success: {result}")
    print(f"After enqueue: {circular}")
    
    # Priority queue
    print("\n=== Priority Queue Demo ===")
    pq = PriorityQueue[str]()
    
    pq.enqueue("Low priority task", 3)
    pq.enqueue("High priority task", 1)
    pq.enqueue("Medium priority task", 2)
    pq.enqueue("Critical task", 0)
    
    print(f"Priority queue: {pq}")
    
    print(f"\nDequeue (should get highest priority first):")
    while not pq.is_empty():
        item = pq.dequeue()
        print(f"  {item}")
    
    # Queue applications
    print("\n=== Queue Applications ===")
    
    # Task simulation
    def simulate_tasks(tasks: List[str]) -> None:
        """Simulate task processing."""
        queue = Queue[str]()
        
        for task in tasks:
            queue.enqueue(task)
        
        print(f"Processing tasks:")
        while not queue.is_empty():
            task = queue.dequeue()
            print(f"  Processing: {task}")
    
    simulate_tasks(["Task 1", "Task 2", "Task 3"])
    
    # Level order traversal simulation
    print("\n=== Level Order Simulation ===")
    from collections import deque
    
    def level_order_simulation() -> None:
        """Simulate level order traversal."""
        levels = [
            ["A"],
            ["B", "C"],
            ["D", "E", "F", "G"]
        ]
        
        queue = Queue[str]()
        queue.enqueue("A")
        
        print("Level order:")
        while not queue.is_empty():
            node = queue.dequeue()
            print(f"  Visit: {node}")
    
    level_order_simulation()


if __name__ == "__main__":
    main()
