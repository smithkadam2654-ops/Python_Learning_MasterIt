"""
Quick Sort - Divide and conquer sorting algorithm.
Features: In-place sorting, O(n log n) average case, and multiple pivot strategies.
"""

from typing import List, TypeVar, Generic, Callable, Optional

T = TypeVar('T')


class QuickSort:
    """Quick sort implementation."""
    
    @staticmethod
    def sort(arr: List[T]) -> List[T]:
        """
        Sort array using quick sort.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        QuickSort._sort_recursive(result, 0, len(result) - 1)
        return result
    
    @staticmethod
    def _sort_recursive(arr: List[T], low: int, high: int) -> None:
        """Recursively sort array."""
        if low < high:
            pivot_index = QuickSort._partition(arr, low, high)
            QuickSort._sort_recursive(arr, low, pivot_index - 1)
            QuickSort._sort_recursive(arr, pivot_index + 1, high)
    
    @staticmethod
    def _partition(arr: List[T], low: int, high: int) -> int:
        """Partition array around pivot."""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    @staticmethod
    def sort_random_pivot(arr: List[T]) -> List[T]:
        """
        Sort using random pivot selection.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        import random
        
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        QuickSort._sort_random_pivot(result, 0, len(result) - 1)
        return result
    
    @staticmethod
    def _sort_random_pivot(arr: List[T], low: int, high: int) -> None:
        """Recursively sort with random pivot."""
        if low < high:
            # Random pivot
            pivot_index = QuickSort._partition_random(arr, low, high)
            QuickSort._sort_random_pivot(arr, low, pivot_index - 1)
            QuickSort._sort_random_pivot(arr, pivot_index + 1, high)
    
    @staticmethod
    def _partition_random(arr: List[T], low: int, high: int) -> int:
        """Partition with random pivot."""
        import random
        pivot_index = random.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
        return QuickSort._partition(arr, low, high)
    
    @staticmethod
    def sort_median_of_three(arr: List[T]) -> List[T]:
        """
        Sort using median-of-three pivot selection.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        QuickSort._sort_median_of_three(result, 0, len(result) - 1)
        return result
    
    @staticmethod
    def _sort_median_of_three(arr: List[T], low: int, high: int) -> None:
        """Recursively sort with median-of-three pivot."""
        if low < high:
            pivot_index = QuickSort._partition_median_of_three(arr, low, high)
            QuickSort._sort_median_of_three(arr, low, pivot_index - 1)
            QuickSort._sort_median_of_three(arr, pivot_index + 1, high)
    
    @staticmethod
    def _partition_median_of_three(arr: List[T], low: int, high: int) -> int:
        """Partition with median-of-three pivot."""
        mid = (low + high) // 2
        
        # Find median of first, middle, last
        if arr[low] > arr[mid]:
            arr[low], arr[mid] = arr[mid], arr[low]
        if arr[low] > arr[high]:
            arr[low], arr[high] = arr[high], arr[low]
        if arr[mid] > arr[high]:
            arr[mid], arr[high] = arr[high], arr[mid]
        
        # Use median as pivot
        arr[mid], arr[high] = arr[high], arr[mid]
        return QuickSort._partition(arr, low, high)
    
    @staticmethod
    def sort_three_way(arr: List[T]) -> List[T]:
        """
        Sort using three-way partition (Dutch national flag).
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        QuickSort._sort_three_way(result, 0, len(result) - 1)
        return result
    
    @staticmethod
    def _sort_three_way(arr: List[T], low: int, high: int) -> None:
        """Recursively sort with three-way partition."""
        if low < high:
            lt, gt = QuickSort._partition_three_way(arr, low, high)
            QuickSort._sort_three_way(arr, low, lt - 1)
            QuickSort._sort_three_way(arr, gt + 1, high)
    
    @staticmethod
    def _partition_three_way(arr: List[T], low: int, high: int) -> tuple:
        """Three-way partition (Dutch national flag)."""
        pivot = arr[low]
        lt = low
        i = low + 1
        gt = high
        
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1
        
        return lt, gt
    
    @staticmethod
    def sort_with_key(arr: List[T], key: Callable[[T], any]) -> List[T]:
        """
        Sort array using key function.
        
        Args:
            arr: Array to sort
            key: Key function
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        QuickSort._sort_with_key_recursive(result, 0, len(result) - 1, key)
        return result
    
    @staticmethod
    def _sort_with_key_recursive(arr: List[T], low: int, high: int, 
                                  key: Callable[[T], any]) -> None:
        """Recursively sort with key function."""
        if low < high:
            pivot_index = QuickSort._partition_with_key(arr, low, high, key)
            QuickSort._sort_with_key_recursive(arr, low, pivot_index - 1, key)
            QuickSort._sort_with_key_recursive(arr, pivot_index + 1, high, key)
    
    @staticmethod
    def _partition_with_key(arr: List[T], low: int, high: int, 
                           key: Callable[[T], any]) -> int:
        """Partition using key function."""
        pivot = key(arr[high])
        i = low - 1
        
        for j in range(low, high):
            if key(arr[j]) <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1


class HybridQuickSort(QuickSort):
    """Hybrid quick sort that switches to insertion sort for small arrays."""
    
    INSERTION_THRESHOLD = 10
    
    @staticmethod
    def sort(arr: List[T]) -> List[T]:
        """Sort using hybrid approach."""
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        HybridQuickSort._sort_hybrid(result, 0, len(result) - 1)
        return result
    
    @staticmethod
    def _sort_hybrid(arr: List[T], low: int, high: int) -> None:
        """Recursively sort with insertion sort for small arrays."""
        if high - low + 1 <= HybridQuickSort.INSERTION_THRESHOLD:
            HybridQuickSort._insertion_sort(arr, low, high)
        elif low < high:
            pivot_index = QuickSort._partition(arr, low, high)
            HybridQuickSort._sort_hybrid(arr, low, pivot_index - 1)
            HybridQuickSort._sort_hybrid(arr, pivot_index + 1, high)
    
    @staticmethod
    def _insertion_sort(arr: List[T], low: int, high: int) -> None:
        """Insertion sort for small subarrays."""
        for i in range(low + 1, high + 1):
            key = arr[i]
            j = i - 1
            while j >= low and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key


def main() -> None:
    """Demonstrate quick sort."""
    
    print("=== Quick Sort Demo ===")
    
    # Basic sorting
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {numbers}")
    
    sorted_numbers = QuickSort.sort(numbers.copy())
    print(f"Sorted: {sorted_numbers}")
    
    # Random pivot
    print("\n--- Random Pivot ---")
    random_sorted = QuickSort.sort_random_pivot(numbers.copy())
    print(f"Sorted with random pivot: {random_sorted}")
    
    # Median of three
    print("\n--- Median of Three ---")
    median_sorted = QuickSort.sort_median_of_three(numbers.copy())
    print(f"Sorted with median-of-three: {median_sorted}")
    
    # Three-way partition
    print("\n--- Three-Way Partition ---")
    duplicates = [3, 1, 2, 3, 1, 2, 3, 1]
    print(f"Original: {duplicates}")
    
    three_way_sorted = QuickSort.sort_three_way(duplicates.copy())
    print(f"Sorted with three-way: {three_way_sorted}")
    
    # Sorting with key
    print("\n--- Sorting with Key ---")
    students = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 20},
        {"name": "Charlie", "age": 30}
    ]
    
    sorted_students = QuickSort.sort_with_key(students.copy(), key=lambda x: x["age"])
    print(f"Sorted by age: {sorted_students}")
    
    # Hybrid quick sort
    print("\n--- Hybrid Quick Sort ---")
    hybrid_sorted = HybridQuickSort.sort(numbers.copy())
    print(f"Hybrid sorted: {hybrid_sorted}")
    
    # String sorting
    print("\n--- String Sorting ---")
    words = ["banana", "apple", "cherry", "date"]
    print(f"Original: {words}")
    
    sorted_words = QuickSort.sort(words.copy())
    print(f"Sorted: {sorted_words}")
    
    # Performance test
    print("\n=== Performance Test ===")
    import time
    import random
    
    n = 100000
    large_array = [random.randint(0, 1000000) for _ in range(n)]
    
    # Standard quick sort
    start = time.time()
    QuickSort.sort(large_array.copy())
    quick_time = (time.time() - start) * 1000
    
    # Random pivot
    start = time.time()
    QuickSort.sort_random_pivot(large_array.copy())
    random_time = (time.time() - start) * 1000
    
    # Median of three
    start = time.time()
    QuickSort.sort_median_of_three(large_array.copy())
    median_time = (time.time() - start) * 1000
    
    # Hybrid
    start = time.time()
    HybridQuickSort.sort(large_array.copy())
    hybrid_time = (time.time() - start) * 1000
    
    # Python sort
    start = time.time()
    sorted(large_array)
    python_time = (time.time() - start) * 1000
    
    print(f"Standard quick sort: {quick_time:.2f}ms")
    print(f"Random pivot: {random_time:.2f}ms")
    print(f"Median of three: {median_time:.2f}ms")
    print(f"Hybrid: {hybrid_time:.2f}ms")
    print(f"Python sort: {python_time:.2f}ms")
    
    # Worst case test (already sorted)
    print("\n--- Worst Case (Already Sorted) ---")
    sorted_array = list(range(n))
    
    start = time.time()
    QuickSort.sort(sorted_array.copy())
    worst_time = (time.time() - start) * 1000
    
    start = time.time()
    QuickSort.sort_random_pivot(sorted_array.copy())
    random_worst_time = (time.time() - start) * 1000
    
    print(f"Standard (worst case): {worst_time:.2f}ms")
    print(f"Random pivot (avoids worst): {random_worst_time:.2f}ms")
    print(f"Improvement: {worst_time/random_worst_time:.2f}x")


if __name__ == "__main__":
    main()
