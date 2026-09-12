"""
Heap Operations - Priority queue and heap algorithms.
Features: Min/max heap, heap operations, and heap-based problems.
"""

from typing import List, Optional, TypeVar, Generic
import heapq

T = TypeVar('T')


class MinHeap:
    """Min heap implementation."""
    
    def __init__(self) -> None:
        """Initialize empty min heap."""
        self.heap: List[T] = []
    
    def push(self, val: T) -> None:
        """
        Push value onto heap.
        
        Args:
            val: Value to push
        """
        heapq.heappush(self.heap, val)
    
    def pop(self) -> Optional[T]:
        """
        Pop minimum value from heap.
        
        Returns:
            Minimum value or None if empty
        """
        if not self.heap:
            return None
        return heapq.heappop(self.heap)
    
    def peek(self) -> Optional[T]:
        """
        Peek at minimum value without removing.
        
        Returns:
            Minimum value or None if empty
        """
        if not self.heap:
            return None
        return self.heap[0]
    
    def size(self) -> int:
        """Get heap size."""
        return len(self.heap)
    
    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return len(self.heap) == 0
    
    def __len__(self) -> int:
        """Get heap size."""
        return len(self.heap)


class MaxHeap:
    """Max heap implementation using negation."""
    
    def __init__(self) -> None:
        """Initialize empty max heap."""
        self.heap: List[T] = []
    
    def push(self, val: T) -> None:
        """
        Push value onto heap.
        
        Args:
            val: Value to push
        """
        heapq.heappush(self.heap, -val)
    
    def pop(self) -> Optional[T]:
        """
        Pop maximum value from heap.
        
        Returns:
            Maximum value or None if empty
        """
        if not self.heap:
            return None
        return -heapq.heappop(self.heap)
    
    def peek(self) -> Optional[T]:
        """
        Peek at maximum value without removing.
        
        Returns:
            Maximum value or None if empty
        """
        if not self.heap:
            return None
        return -self.heap[0]
    
    def size(self) -> int:
        """Get heap size."""
        return len(self.heap)
    
    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return len(self.heap) == 0


class HeapOperations:
    """Heap-based algorithm implementations."""
    
    @staticmethod
    def heapify(arr: List[T]) -> List[T]:
        """
        Convert array to heap in-place.
        
        Args:
            arr: Input array
            
        Returns:
            Heapified array
        """
        heapq.heapify(arr)
        return arr
    
    @staticmethod
    def heap_sort(arr: List[T]) -> List[T]:
        """
        Sort array using heap sort.
        
        Args:
            arr: Input array
            
        Returns:
            Sorted array
        """
        heapq.heapify(arr)
        return [heapq.heappop(arr) for _ in range(len(arr))]
    
    @staticmethod
    def n_largest(arr: List[T], n: int) -> List[T]:
        """
        Find n largest elements.
        
        Args:
            arr: Input array
            n: Number of largest elements
            
        Returns:
            List of n largest elements
        """
        return heapq.nlargest(n, arr)
    
    @staticmethod
    def n_smallest(arr: List[T], n: int) -> List[T]:
        """
        Find n smallest elements.
        
        Args:
            arr: Input array
            n: Number of smallest elements
            
        Returns:
            List of n smallest elements
        """
        return heapq.nsmallest(n, arr)
    
    @staticmethod
    def merge_k_sorted_lists(lists: List[List[T]]) -> List[T]:
        """
        Merge k sorted lists using heap.
        
        Args:
            lists: List of sorted lists
            
        Returns:
            Merged sorted list
        """
        min_heap = []
        
        # Push first element of each list
        for i, lst in enumerate(lists):
            if lst:
                heapq.heappush(min_heap, (lst[0], i, 0))
        
        result = []
        
        while min_heap:
            val, list_idx, element_idx = heapq.heappop(min_heap)
            result.append(val)
            
            # Push next element from same list
            if element_idx + 1 < len(lists[list_idx]):
                next_val = lists[list_idx][element_idx + 1]
                heapq.heappush(min_heap, (next_val, list_idx, element_idx + 1))
        
        return result
    
    @staticmethod
    def kth_largest(arr: List[T], k: int) -> Optional[T]:
        """
        Find kth largest element using heap.
        
        Args:
            arr: Input array
            k: kth largest (1-indexed)
            
        Returns:
            kth largest element or None
        """
        if k < 1 or k > len(arr):
            return None
        
        # Use min heap of size k
        min_heap = arr[:k]
        heapq.heapify(min_heap)
        
        for val in arr[k:]:
            if val > min_heap[0]:
                heapq.heappop(min_heap)
                heapq.heappush(min_heap, val)
        
        return min_heap[0]
    
    @staticmethod
    def kth_smallest(arr: List[T], k: int) -> Optional[T]:
        """
        Find kth smallest element using heap.
        
        Args:
            arr: Input array
            k: kth smallest (1-indexed)
            
        Returns:
            kth smallest element or None
        """
        if k < 1 or k > len(arr):
            return None
        
        # Use max heap of size k
        max_heap = [-val for val in arr[:k]]
        heapq.heapify(max_heap)
        
        for val in arr[k:]:
            if val < -max_heap[0]:
                heapq.heappop(max_heap)
                heapq.heappush(max_heap, -val)
        
        return -max_heap[0]
    
    @staticmethod
    def median_from_stream() -> 'MedianFinder':
        """
        Create median finder for streaming data.
        
        Returns:
            MedianFinder instance
        """
        return MedianFinder()
    
    @staticmethod
    def top_k_frequent(arr: List[T], k: int) -> List[T]:
        """
        Find k most frequent elements.
        
        Args:
            arr: Input array
            k: Number of most frequent elements
            
        Returns:
            List of k most frequent elements
        """
        from collections import Counter
        
        # Count frequencies
        counter = Counter(arr)
        
        # Use heap to get top k
        return heapq.nlargest(k, counter.keys(), key=counter.get)
    
    @staticmethod
    def reorganize_string(s: str) -> str:
        """
        Reorganize string so no adjacent characters are same.
        
        Args:
            s: Input string
            
        Returns:
            Reorganized string or empty if impossible
        """
        from collections import Counter
        
        # Count frequencies
        counter = Counter(s)
        max_heap = [(-count, char) for char, count in counter.items()]
        heapq.heapify(max_heap)
        
        result = []
        prev_count, prev_char = 0, ''
        
        while max_heap:
            count, char = heapq.heappop(max_heap)
            result.append(char)
            
            if prev_count < 0:
                heapq.heappush(max_heap, (prev_count, prev_char))
            
            count += 1
            prev_count, prev_char = count, char
        
        if len(result) != len(s):
            return ""
        
        return ''.join(result)
    
    @staticmethod
    def task_scheduler(tasks: List[str], n: int) -> int:
        """
        Calculate minimum time to complete tasks with cooldown.
        
        Args:
            tasks: List of tasks
            n: Cooldown period
            
        Returns:
            Minimum time
        """
        from collections import Counter
        
        # Count frequencies
        counter = Counter(tasks)
        max_heap = [-count for count in counter.values()]
        heapq.heapify(max_heap)
        
        time = 0
        queue = []
        
        while max_heap or queue:
            time += 1
            
            if max_heap:
                count = heapq.heappop(max_heap) + 1
                if count < 0:
                    queue.append((count, time + n))
            
            if queue and queue[0][1] == time:
                heapq.heappush(max_heap, queue.pop(0)[0])
        
        return time
    
    @staticmethod
    def find_k_closest_points(points: List[tuple], k: int) -> List[tuple]:
        """
        Find k closest points to origin.
        
        Args:
            points: List of (x, y) coordinates
            k: Number of closest points
            
        Returns:
            List of k closest points
        """
        def distance(point: tuple) -> float:
            return point[0] ** 2 + point[1] ** 2
        
        # Use max heap to keep k closest
        max_heap = []
        
        for point in points:
            dist = distance(point)
            heapq.heappush(max_heap, (-dist, point))
            
            if len(max_heap) > k:
                heapq.heappop(max_heap)
        
        return [point for _, point in max_heap]


class MedianFinder:
    """Find median from data stream using two heaps."""
    
    def __init__(self) -> None:
        """Initialize median finder."""
        self.small = []  # Max heap (left half)
        self.large = []  # Min heap (right half)
    
    def add_num(self, num: int) -> None:
        """
        Add number to data stream.
        
        Args:
            num: Number to add
        """
        # Push to small (max heap using negation)
        heapq.heappush(self.small, -num)
        
        # Balance: ensure all elements in small <= all in large
        if self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        if len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def find_median(self) -> float:
        """
        Find median of current data.
        
        Returns:
            Median value
        """
        if len(self.small) > len(self.large):
            return -self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        else:
            return (-self.small[0] + self.large[0]) / 2


def main() -> None:
    """Demonstrate heap operations."""
    
    print("=== Heap Operations Demo ===")
    
    # Min heap
    print("\n--- Min Heap ---")
    min_heap = MinHeap()
    for val in [5, 3, 7, 1, 9]:
        min_heap.push(val)
    
    print(f"Pushed: 5, 3, 7, 1, 9")
    print(f"Peek: {min_heap.peek()}")
    print(f"Pop: {min_heap.pop()}")
    print(f"Peek: {min_heap.peek()}")
    
    # Max heap
    print("\n--- Max Heap ---")
    max_heap = MaxHeap()
    for val in [5, 3, 7, 1, 9]:
        max_heap.push(val)
    
    print(f"Pushed: 5, 3, 7, 1, 9")
    print(f"Peek: {max_heap.peek()}")
    print(f"Pop: {max_heap.pop()}")
    print(f"Peek: {max_heap.peek()}")
    
    # Heapify and heap sort
    print("\n--- Heapify and Sort ---")
    arr = [5, 3, 7, 1, 9, 2]
    print(f"Original: {arr}")
    HeapOperations.heapify(arr.copy())
    print(f"Heapified: {arr}")
    print(f"Heap sort: {HeapOperations.heap_sort(arr.copy())}")
    
    # N largest/smallest
    print("\n--- N Largest/Smallest ---")
    arr = [5, 3, 7, 1, 9, 2, 8, 4, 6]
    print(f"Array: {arr}")
    print(f"3 largest: {HeapOperations.n_largest(arr, 3)}")
    print(f"3 smallest: {HeapOperations.n_smallest(arr, 3)}")
    
    # Merge k sorted lists
    print("\n--- Merge K Sorted Lists ---")
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    print(f"Lists: {lists}")
    print(f"Merged: {HeapOperations.merge_k_sorted_lists(lists)}")
    
    # Kth largest/smallest
    print("\n--- Kth Largest/Smallest ---")
    arr = [3, 2, 1, 5, 6, 4]
    print(f"Array: {arr}")
    print(f"2nd largest: {HeapOperations.kth_largest(arr, 2)}")
    print(f"2nd smallest: {HeapOperations.kth_smallest(arr, 2)}")
    
    # Median from stream
    print("\n--- Median from Stream ---")
    median_finder = HeapOperations.median_from_stream()
    for num in [1, 2, 3]:
        median_finder.add_num(num)
        print(f"Added {num}, median: {median_finder.find_median()}")
    
    # Top k frequent
    print("\n--- Top K Frequent ---")
    arr = [1, 1, 1, 2, 2, 3]
    print(f"Array: {arr}")
    print(f"Top 2 frequent: {HeapOperations.top_k_frequent(arr, 2)}")
    
    # Reorganize string
    print("\n--- Reorganize String ---")
    s = "aab"
    print(f"Original: '{s}'")
    print(f"Reorganized: '{HeapOperations.reorganize_string(s)}'")
    
    # Task scheduler
    print("\n--- Task Scheduler ---")
    tasks = ["A", "A", "A", "B", "B", "B"]
    n = 2
    print(f"Tasks: {tasks}, cooldown: {n}")
    print(f"Minimum time: {HeapOperations.task_scheduler(tasks, n)}")
    
    # K closest points
    print("\n--- K Closest Points ---")
    points = [(1, 3), (3, 4), (2, -1)]
    k = 2
    print(f"Points: {points}, k: {k}")
    print(f"Closest: {HeapOperations.find_k_closest_points(points, k)}")


if __name__ == "__main__":
    main()
