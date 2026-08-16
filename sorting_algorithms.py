"""
Sorting Algorithms - Implementation of common sorting algorithms.
Features: Comparison of different algorithms with time complexity analysis.
"""

from typing import List, Callable, Any
import time
import random
from dataclasses import dataclass


@dataclass
class SortResult:
    """Result of sorting operation."""
    algorithm: str
    time: float
    comparisons: int
    sorted: bool


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Bubble Sort - Simple but inefficient O(n²) algorithm.
    
    Time Complexity: O(n²) worst/average, O(n) best (with optimization)
    Space Complexity: O(1)
    Stable: Yes
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list
    """
    arr = arr.copy()
    n = len(arr)
    comparisons = 0
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    
    return arr


def selection_sort(arr: List[int]) -> List[int]:
    """
    Selection Sort - Simple O(n²) algorithm.
    
    Time Complexity: O(n²) all cases
    Space Complexity: O(1)
    Stable: No
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list
    """
    arr = arr.copy()
    n = len(arr)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr


def insertion_sort(arr: List[int]) -> List[int]:
    """
    Insertion Sort - Efficient for small/nearly sorted arrays.
    
    Time Complexity: O(n²) worst/average, O(n) best
    Space Complexity: O(1)
    Stable: Yes
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list
    """
    arr = arr.copy()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr


def merge_sort(arr: List[int]) -> List[int]:
    """
    Merge Sort - Divide and conquer O(n log n) algorithm.
    
    Time Complexity: O(n log n) all cases
    Space Complexity: O(n)
    Stable: Yes
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr.copy()
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left: List[int], right: List[int]) -> List[int]:
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr: List[int]) -> List[int]:
    """
    Quick Sort - Efficient divide and conquer algorithm.
    
    Time Complexity: O(n log n) average, O(n²) worst
    Space Complexity: O(log n) average
    Stable: No
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr.copy()
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


def heap_sort(arr: List[int]) -> List[int]:
    """
    Heap Sort - O(n log n) algorithm using heap data structure.
    
    Time Complexity: O(n log n) all cases
    Space Complexity: O(1)
    Stable: No
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list
    """
    arr = arr.copy()
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements from heap
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr


def heapify(arr: List[int], n: int, i: int) -> None:
    """Heapify a subtree rooted at index i."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def counting_sort(arr: List[int]) -> List[int]:
    """
    Counting Sort - O(n + k) algorithm for integers in known range.
    
    Time Complexity: O(n + k) where k is range of values
    Space Complexity: O(k)
    Stable: Yes
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list
    """
    if not arr:
        return []
    
    arr = arr.copy()
    min_val = min(arr)
    max_val = max(arr)
    range_val = max_val - min_val + 1
    
    count = [0] * range_val
    output = [0] * len(arr)
    
    # Count occurrences
    for num in arr:
        count[num - min_val] += 1
    
    # Calculate cumulative count
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    # Build output array (iterate in reverse for stability)
    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1
    
    return output


def benchmark_sort(
    algorithm: Callable[[List[int]], List[int]],
    data: List[int],
    name: str,
) -> SortResult:
    """
    Benchmark a sorting algorithm.
    
    Args:
        algorithm: Sorting function to benchmark
        data: Data to sort
        name: Name of the algorithm
        
    Returns:
        SortResult with timing information
    """
    start_time = time.perf_counter()
    sorted_data = algorithm(data)
    end_time = time.perf_counter()
    
    elapsed = end_time - start_time
    is_sorted = sorted_data == sorted(data)
    
    return SortResult(
        algorithm=name,
        time=elapsed,
        comparisons=0,
        sorted=is_sorted,
    )


def main() -> None:
    """Demonstrate and compare sorting algorithms."""
    
    # Test data
    test_data = [64, 34, 25, 12, 22, 11, 90, 5]
    
    print("=== Sorting Algorithm Comparison ===")
    print(f"Original array: {test_data}")
    print()
    
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort),
        ("Heap Sort", heap_sort),
        ("Counting Sort", counting_sort),
    ]
    
    for name, func in algorithms:
        sorted_result = func(test_data)
        print(f"{name:15s}: {sorted_result}")
    
    # Benchmark with larger dataset
    print("\n=== Performance Benchmark ===")
    large_data = [random.randint(1, 1000) for _ in range(1000)]
    
    results = []
    for name, func in algorithms:
        result = benchmark_sort(func, large_data, name)
        results.append(result)
    
    # Sort results by time
    results.sort(key=lambda x: x.time)
    
    print(f"{'Algorithm':<15s} {'Time (s)':<12s} {'Sorted':<8s}")
    print("-" * 35)
    for result in results:
        print(f"{result.algorithm:<15s} {result.time:<12.6f} {str(result.sorted):<8s}")
    
    # Demonstrate stability
    print("\n=== Stability Test ===")
    stable_data = [(3, 'a'), (1, 'b'), (3, 'c'), (1, 'd'), (2, 'e')]
    
    def sort_by_first(arr):
        return sorted(arr, key=lambda x: x[0])
    
    print(f"Original: {stable_data}")
    print(f"Sorted:   {sort_by_first(stable_data)}")


if __name__ == "__main__":
    main()
