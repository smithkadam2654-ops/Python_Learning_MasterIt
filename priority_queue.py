"""
Priority Queue - Priority queue implementation with heap operations.
Features: Min-heap, max-heap, and custom priority queues.
"""

import heapq
from typing import List, Tuple, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class PriorityQueueType(Enum):
    """Priority queue types."""
    MIN_HEAP = "min"
    MAX_HEAP = "max"


@dataclass(order=True)
class PriorityItem:
    """Item with priority for priority queue."""
    priority: int
    item: Any = field(compare=False)


class PriorityQueue:
    """Priority queue implementation using heapq."""
    
    def __init__(self, queue_type: PriorityQueueType = PriorityQueueType.MIN_HEAP) -> None:
        """
        Initialize priority queue.
        
        Args:
            queue_type: Type of priority queue (min or max heap)
        """
        self.queue_type = queue_type
        self._heap: List[PriorityItem] = []
    
    def push(self, item: Any, priority: int) -> None:
        """
        Add item to priority queue.
        
        Args:
            item: Item to add
            priority: Priority value (lower = higher priority for min-heap)
        """
        if self.queue_type == PriorityQueueType.MAX_HEAP:
            priority = -priority  # Negate for max-heap
        
        heapq.heappush(self._heap, PriorityItem(priority, item))
    
    def pop(self) -> Optional[Any]:
        """
        Remove and return highest priority item.
        
        Returns:
            Item with highest priority, or None if empty
        """
        if not self._heap:
            return None
        
        priority_item = heapq.heappop(self._heap)
        return priority_item.item
    
    def peek(self) -> Optional[Any]:
        """
        Return highest priority item without removing it.
        
        Returns:
            Item with highest priority, or None if empty
        """
        if not self._heap:
            return None
        
        return self._heap[0].item
    
    def is_empty(self) -> bool:
        """Check if priority queue is empty."""
        return len(self._heap) == 0
    
    def size(self) -> int:
        """Return number of items in queue."""
        return len(self._heap)
    
    def clear(self) -> None:
        """Clear all items from queue."""
        self._heap.clear()
    
    def __len__(self) -> int:
        """Return size of queue."""
        return len(self._heap)


class CustomPriorityQueue:
    """Priority queue with custom comparison function."""
    
    def __init__(self, compare_func: Optional[Callable] = None) -> None:
        """
        Initialize custom priority queue.
        
        Args:
            compare_func: Function to compare items (a, b) -> bool (True if a < b)
        """
        self._items: List[Any] = []
        self._compare = compare_func or (lambda a, b: a < b)
    
    def push(self, item: Any) -> None:
        """
        Add item to priority queue.
        
        Args:
            item: Item to add
        """
        self._items.append(item)
        self._sift_up(len(self._items) - 1)
    
    def pop(self) -> Optional[Any]:
        """
        Remove and return highest priority item.
        
        Returns:
            Item with highest priority, or None if empty
        """
        if not self._items:
            return None
        
        if len(self._items) == 1:
            return self._items.pop()
        
        result = self._items[0]
        self._items[0] = self._items.pop()
        self._sift_down(0)
        
        return result
    
    def peek(self) -> Optional[Any]:
        """
        Return highest priority item without removing it.
        
        Returns:
            Item with highest priority, or None if empty
        """
        if not self._items:
            return None
        return self._items[0]
    
    def _sift_up(self, index: int) -> None:
        """Sift item up to maintain heap property."""
        while index > 0:
            parent = (index - 1) // 2
            if self._compare(self._items[index], self._items[parent]):
                self._items[index], self._items[parent] = self._items[parent], self._items[index]
                index = parent
            else:
                break
    
    def _sift_down(self, index: int) -> None:
        """Sift item down to maintain heap property."""
        n = len(self._items)
        
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            
            if left < n and self._compare(self._items[left], self._items[smallest]):
                smallest = left
            
            if right < n and self._compare(self._items[right], self._items[smallest]):
                smallest = right
            
            if smallest != index:
                self._items[index], self._items[smallest] = self._items[smallest], self._items[index]
                index = smallest
            else:
                break
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Return size of queue."""
        return len(self._items)


class TaskScheduler:
    """Task scheduler using priority queue."""
    
    def __init__(self) -> None:
        """Initialize task scheduler."""
        self._queue = PriorityQueue(PriorityType.MIN_HEAP)
        self._task_id = 0
    
    def add_task(self, task: str, priority: int) -> int:
        """
        Add a task to the scheduler.
        
        Args:
            task: Task description
            priority: Task priority (lower = higher priority)
            
        Returns:
            Task ID
        """
        self._task_id += 1
        self._queue.push({"id": self._task_id, "task": task}, priority)
        return self._task_id
    
    def get_next_task(self) -> Optional[dict]:
        """
        Get the next highest priority task.
        
        Returns:
            Task dictionary or None if no tasks
        """
        return self._queue.pop()
    
    def peek_next_task(self) -> Optional[dict]:
        """
        Peek at the next task without removing it.
        
        Returns:
            Task dictionary or None if no tasks
        """
        return self._queue.peek()
    
    def has_tasks(self) -> bool:
        """Check if there are pending tasks."""
        return not self._queue.is_empty()
    
    def task_count(self) -> int:
        """Return number of pending tasks."""
        return self._queue.size()


class MedianFinder:
    """Find median from data stream using two heaps."""
    
    def __init__(self) -> None:
        """Initialize median finder."""
        self._max_heap: List[int] = []  # Left half (max-heap using negation)
        self._min_heap: List[int] = []  # Right half (min-heap)
    
    def add_num(self, num: int) -> None:
        """
        Add number to data stream.
        
        Args:
            num: Number to add
        """
        # Add to max-heap (left half)
        heapq.heappush(self._max_heap, -num)
        
        # Balance: move largest from left to right
        heapq.heappush(self._min_heap, -self._max_heap[0])
        heapq.heappop(self._max_heap)
        
        # Ensure left half has equal or one more element
        if len(self._max_heap) < len(self._min_heap):
            heapq.heappush(self._max_heap, -self._min_heap[0])
            heapq.heappop(self._min_heap)
    
    def find_median(self) -> Optional[float]:
        """
        Find median of current data stream.
        
        Returns:
            Median value, or None if no data
        """
        if not self._max_heap:
            return None
        
        if len(self._max_heap) > len(self._min_heap):
            return float(-self._max_heap[0])
        else:
            return (-self._max_heap[0] + self._min_heap[0]) / 2.0


def merge_k_sorted_lists(lists: List[List[int]]) -> List[int]:
    """
    Merge k sorted lists using priority queue.
    
    Args:
        lists: List of sorted lists
        
    Returns:
        Merged sorted list
    """
    if not lists:
        return []
    
    # Min-heap of (value, list_index, element_index)
    heap = []
    
    # Initialize heap with first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    
    result = []
    
    while heap:
        value, list_idx, elem_idx = heapq.heappop(heap)
        result.append(value)
        
        # Add next element from the same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_elem = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_elem, list_idx, elem_idx + 1))
    
    return result


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Find k most frequent elements using heap.
    
    Args:
        nums: List of numbers
        k: Number of top frequent elements to return
        
    Returns:
        List of k most frequent elements
    """
    from collections import Counter
    
    # Count frequencies
    counter = Counter(nums)
    
    # Use heap to get top k
    # Python's heapq is min-heap, so we negate for max-heap behavior
    heap = [(-count, num) for num, count in counter.items()]
    heapq.heapify(heap)
    
    result = []
    for _ in range(k):
        if heap:
            count, num = heapq.heappop(heap)
            result.append(num)
    
    return result


def main() -> None:
    """Demonstrate priority queue operations."""
    
    print("=== Min-Heap Priority Queue ===")
    min_pq = PriorityQueue(PriorityType.MIN_HEAP)
    
    min_pq.push("Low priority task", 10)
    min_pq.push("High priority task", 1)
    min_pq.push("Medium priority task", 5)
    
    print(f"Size: {min_pq.size()}")
    print(f"Peek: {min_pq.peek()}")
    
    while not min_pq.is_empty():
        print(f"Pop: {min_pq.pop()}")
    
    print("\n=== Max-Heap Priority Queue ===")
    max_pq = PriorityQueue(PriorityType.MAX_HEAP)
    
    max_pq.push("Low priority", 1)
    max_pq.push("High priority", 10)
    max_pq.push("Medium priority", 5)
    
    while not max_pq.is_empty():
        print(f"Pop: {max_pq.pop()}")
    
    print("\n=== Custom Priority Queue ===")
    custom_pq = CustomPriorityQueue(compare_func=lambda a, b: a['value'] < b['value'])
    
    custom_pq.push({'name': 'Task A', 'value': 30})
    custom_pq.push({'name': 'Task B', 'value': 10})
    custom_pq.push({'name': 'Task C', 'value': 20})
    
    while not custom_pq.is_empty():
        print(f"Pop: {custom_pq.pop()}")
    
    print("\n=== Task Scheduler ===")
    scheduler = TaskScheduler()
    
    scheduler.add_task("Fix bug", 1)
    scheduler.add_task("Write documentation", 3)
    scheduler.add_task("Deploy to production", 2)
    scheduler.add_task("Code review", 1)
    
    print(f"Pending tasks: {scheduler.task_count()}")
    
    while scheduler.has_tasks():
        task = scheduler.get_next_task()
        print(f"Executing: {task['task']} (ID: {task['id']}, Priority: {task.get('priority', 'N/A')})")
    
    print("\n=== Median Finder ===")
    finder = MedianFinder()
    
    for num in [1, 2, 3, 4, 5]:
        finder.add_num(num)
        print(f"Added {num}, Median: {finder.find_median()}")
    
    print("\n=== Merge K Sorted Lists ===")
    lists = [
        [1, 4, 5],
        [1, 3, 4],
        [2, 6]
    ]
    print(f"Input: {lists}")
    merged = merge_k_sorted_lists(lists)
    print(f"Merged: {merged}")
    
    print("\n=== Top K Frequent Elements ===")
    nums = [1, 1, 1, 2, 2, 3]
    k = 2
    print(f"Numbers: {nums}")
    print(f"Top {k} frequent: {top_k_frequent(nums, k)}")


if __name__ == "__main__":
    main()
