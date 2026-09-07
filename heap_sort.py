"""
Heap Sort - Comparison-based sorting using heap data structure.
Features: In-place sorting, O(n log n) time complexity, and no additional memory.
"""

from typing import List, TypeVar, Generic

T = TypeVar('T')


class HeapSort:
    """Heap sort implementation."""
    
    @staticmethod
    def sort(arr: List[T]) -> List[T]:
        """
        Sort array using heap sort.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        n = len(result)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            HeapSort._heapify(result, n, i)
        
        # Extract elements from heap
        for i in range(n - 1, 0, -1):
            result[0], result[i] = result[i], result[0]
            HeapSort._heapify(result, i, 0)
        
        return result
    
    @staticmethod
    def _heapify(arr: List[T], n: int, i: int) -> None:
        """
        Heapify subtree rooted at index i.
        
        Args:
            arr: Array to heapify
            n: Size of heap
            i: Root index
        """
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            HeapSort._heapify(arr, n, largest)
    
    @staticmethod
    def sort_min_heap(arr: List[T]) -> List[T]:
        """
        Sort using min heap (ascending order).
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        n = len(result)
        
        # Build min heap
        for i in range(n // 2 - 1, -1, -1):
            HeapSort._heapify_min(result, n, i)
        
        # Extract elements
        sorted_result = []
        for _ in range(n):
            sorted_result.append(result[0])
            result[0] = result[-1]
            result.pop()
            if result:
                HeapSort._heapify_min(result, len(result), 0)
        
        return sorted_result
    
    @staticmethod
    def _heapify_min(arr: List[T], n: int, i: int) -> None:
        """Heapify for min heap."""
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] < arr[smallest]:
            smallest = left
        
        if right < n and arr[right] < arr[smallest]:
            smallest = right
        
        if smallest != i:
            arr[i], arr[smallest] = arr[smallest], arr[i]
            HeapSort._heapify_min(arr, n, smallest)
    
    @staticmethod
    def sort_descending(arr: List[T]) -> List[T]:
        """
        Sort array in descending order.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array (descending)
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        n = len(result)
        
        # Build min heap for descending order
        for i in range(n // 2 - 1, -1, -1):
            HeapSort._heapify_min(result, n, i)
        
        # Extract elements
        for i in range(n - 1, 0, -1):
            result[0], result[i] = result[i], result[0]
            HeapSort._heapify_min(result, i, 0)
        
        return result
    
    @staticmethod
    def kth_largest(arr: List[T], k: int) -> Optional[T]:
        """
        Find kth largest element using heap.
        
        Args:
            arr: Array to search
            k: kth largest to find
            
        Returns:
            kth largest element or None
        """
        if k < 1 or k > len(arr):
            return None
        
        result = arr.copy()
        n = len(result)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            HeapSort._heapify(result, n, i)
        
        # Extract k elements
        for i in range(n - 1, n - k, -1):
            result[0], result[i] = result[i], result[0]
            HeapSort._heapify(result, i, 0)
        
        return result[n - k]
    
    @staticmethod
    def kth_smallest(arr: List[T], k: int) -> Optional[T]:
        """
        Find kth smallest element using heap.
        
        Args:
            arr: Array to search
            k: kth smallest to find
            
        Returns:
            kth smallest element or None
        """
        if k < 1 or k > len(arr):
            return None
        
        result = arr.copy()
        n = len(result)
        
        # Build min heap
        for i in range(n // 2 - 1, -1, -1):
            HeapSort._heapify_min(result, n, i)
        
        # Extract k elements
        for i in range(n - 1, n - k, -1):
            result[0], result[i] = result[i], result[0]
            HeapSort._heapify_min(result, i, 0)
        
        return result[n - k]


class IterativeHeapSort(HeapSort):
    """Iterative heap sort implementation."""
    
    @staticmethod
    def sort(arr: List[T]) -> List[T]:
        """Sort using iterative heapify."""
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        n = len(result)
        
        # Build max heap iteratively
        for i in range(n // 2 - 1, -1, -1):
            IterativeHeapSort._heapify_iterative(result, n, i)
        
        # Extract elements
        for i in range(n - 1, 0, -1):
            result[0], result[i] = result[i], result[0]
            IterativeHeapSort._heapify_iterative(result, i, 0)
        
        return result
    
    @staticmethod
    def _heapify_iterative(arr: List[T], n: int, i: int) -> None:
        """Heapify iteratively."""
        while True:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n and arr[left] > arr[largest]:
                largest = left
            
            if right < n and arr[right] > arr[largest]:
                largest = right
            
            if largest == i:
                break
            
            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest


def main() -> None:
    """Demonstrate heap sort."""
    
    print("=== Heap Sort Demo ===")
    
    # Basic sorting
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {numbers}")
    
    sorted_numbers = HeapSort.sort(numbers)
    print(f"Sorted: {sorted_numbers}")
    
    # Descending order
    print("\n--- Descending Order ---")
    descending = HeapSort.sort_descending(numbers)
    print(f"Sorted descending: {descending}")
    
    # Min heap sort
    print("\n--- Min Heap Sort ---")
    min_sorted = HeapSort.sort_min_heap(numbers)
    print(f"Sorted with min heap: {min_sorted}")
    
    # Kth largest/smallest
    print("\n--- Kth Element ---")
    print(f"2nd largest: {HeapSort.kth_largest(numbers, 2)}")
    print(f"3rd smallest: {HeapSort.kth_smallest(numbers, 3)}")
    
    # String sorting
    print("\n--- String Sorting ---")
    words = ["banana", "apple", "cherry", "date"]
    print(f"Original: {words}")
    
    sorted_words = HeapSort.sort(words)
    print(f"Sorted: {sorted_words}")
    
    # Iterative heap sort
    print("\n--- Iterative Heap Sort ---")
    iterative_sorted = IterativeHeapSort.sort(numbers)
    print(f"Iteratively sorted: {iterative_sorted}")
    
    # Performance test
    print("\n=== Performance Test ===")
    import time
    import random
    
    n = 100000
    large_array = [random.randint(0, 1000000) for _ in range(n)]
    
    # Recursive heap sort
    start = time.time()
    HeapSort.sort(large_array.copy())
    recursive_time = (time.time() - start) * 1000
    
    # Iterative heap sort
    start = time.time()
    IterativeHeapSort.sort(large_array.copy())
    iterative_time = (time.time() - start) * 1000
    
    # Python sort
    start = time.time()
    sorted(large_array)
    python_time = (time.time() - start) * 1000
    
    print(f"Recursive heap sort: {recursive_time:.2f}ms")
    print(f"Iterative heap sort: {iterative_time:.2f}ms")
    print(f"Python sort: {python_time:.2f}ms")
    print(f"Ratio (recursive/python): {recursive_time/python_time:.2f}x")
    
    # Kth element performance
    print("\n--- Kth Element Performance ---")
    
    start = time.time()
    kth = HeapSort.kth_largest(large_array, 1000)
    kth_time = (time.time() - start) * 1000
    
    start = time.time()
    sorted_kth = sorted(large_array, reverse=True)[999]
    sorted_kth_time = (time.time() - start) * 1000
    
    print(f"Heap sort kth: {kth_time:.4f}ms")
    print(f"Full sort kth: {sorted_kth_time:.4f}ms")
    print(f"Speedup: {sorted_kth_time/kth_time:.2f}x")
    
    # Already sorted (best case for heap sort)
    print("\n--- Already Sorted ---")
    sorted_array = list(range(n))
    
    start = time.time()
    HeapSort.sort(sorted_array.copy())
    sorted_case_time = (time.time() - start) * 1000
    
    start = time.time()
    HeapSort.sort(large_array.copy())
    random_case_time = (time.time() - start) * 1000
    
    print(f"Already sorted: {sorted_case_time:.2f}ms")
    print(f"Random order: {random_case_time:.2f}ms")
    print(f"Ratio: {sorted_case_time/random_case_time:.2f}x")


if __name__ == "__main__":
    main()
