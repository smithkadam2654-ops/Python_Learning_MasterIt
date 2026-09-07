"""
Merge Sort - Divide and conquer sorting algorithm.
Features: Stable sort, O(n log n) time complexity, and external sorting capability.
"""

from typing import List, TypeVar, Generic, Callable

T = TypeVar('T')


class MergeSort:
    """Merge sort implementation."""
    
    @staticmethod
    def sort(arr: List[T]) -> List[T]:
        """
        Sort array using merge sort.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        return MergeSort._sort_recursive(arr)
    
    @staticmethod
    def _sort_recursive(arr: List[T]) -> List[T]:
        """Recursively sort array."""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = MergeSort._sort_recursive(arr[:mid])
        right = MergeSort._sort_recursive(arr[mid:])
        
        return MergeSort._merge(left, right)
    
    @staticmethod
    def _merge(left: List[T], right: List[T]) -> List[T]:
        """Merge two sorted arrays."""
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
    
    @staticmethod
    def sort_in_place(arr: List[T]) -> None:
        """
        Sort array in place using merge sort.
        
        Args:
            arr: Array to sort
        """
        if len(arr) <= 1:
            return
        
        temp = [None] * len(arr)
        MergeSort._sort_in_place_recursive(arr, temp, 0, len(arr) - 1)
    
    @staticmethod
    def _sort_in_place_recursive(arr: List[T], temp: List[Optional[T]], 
                                  left: int, right: int) -> None:
        """Recursively sort array in place."""
        if left < right:
            mid = (left + right) // 2
            MergeSort._sort_in_place_recursive(arr, temp, left, mid)
            MergeSort._sort_in_place_recursive(arr, temp, mid + 1, right)
            MergeSort._merge_in_place(arr, temp, left, mid, right)
    
    @staticmethod
    def _merge_in_place(arr: List[T], temp: List[Optional[T]], 
                        left: int, mid: int, right: int) -> None:
        """Merge two sorted subarrays in place."""
        # Copy to temp array
        for i in range(left, right + 1):
            temp[i] = arr[i]
        
        i = left
        j = mid + 1
        k = left
        
        while i <= mid and j <= right:
            if temp[i] <= temp[j]:  # type: ignore
                arr[k] = temp[i]  # type: ignore
                i += 1
            else:
                arr[k] = temp[j]  # type: ignore
                j += 1
            k += 1
        
        while i <= mid:
            arr[k] = temp[i]  # type: ignore
            i += 1
            k += 1
    
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
        
        mid = len(arr) // 2
        left = MergeSort.sort_with_key(arr[:mid], key)
        right = MergeSort.sort_with_key(arr[mid:], key)
        
        return MergeSort._merge_with_key(left, right, key)
    
    @staticmethod
    def _merge_with_key(left: List[T], right: List[T], 
                       key: Callable[[T], any]) -> List[T]:
        """Merge two sorted arrays using key function."""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result


class NaturalMergeSort(MergeSort):
    """Natural merge sort that exploits existing order."""
    
    @staticmethod
    def sort(arr: List[T]) -> List[T]:
        """
        Sort using natural merge sort.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        runs = NaturalMergeSort._find_runs(result)
        
        while len(runs) > 1:
            new_runs = []
            for i in range(0, len(runs), 2):
                if i + 1 < len(runs):
                    merged = NaturalMergeSort._merge(
                        result[runs[i][0]:runs[i][1]],
                        result[runs[i+1][0]:runs[i+1][1]]
                    )
                    new_runs.append((runs[i][0], runs[i][0] + len(merged)))
                    result[runs[i][0]:runs[i+1][1]] = merged
                else:
                    new_runs.append(runs[i])
            runs = new_runs
        
        return result
    
    @staticmethod
    def _find_runs(arr: List[T]) -> List[tuple]:
        """Find naturally sorted runs in array."""
        runs = []
        start = 0
        
        for i in range(1, len(arr)):
            if arr[i] < arr[i - 1]:
                runs.append((start, i))
                start = i
        
        runs.append((start, len(arr)))
        return runs


def main() -> None:
    """Demonstrate merge sort."""
    
    print("=== Merge Sort Demo ===")
    
    # Basic sorting
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {numbers}")
    
    sorted_numbers = MergeSort.sort(numbers)
    print(f"Sorted: {sorted_numbers}")
    
    # In-place sorting
    print("\n--- In-Place Sorting ---")
    arr = [5, 2, 8, 1, 9, 3]
    print(f"Original: {arr}")
    
    MergeSort.sort_in_place(arr)
    print(f"Sorted in-place: {arr}")
    
    # String sorting
    print("\n--- String Sorting ---")
    words = ["banana", "apple", "cherry", "date"]
    print(f"Original: {words}")
    
    sorted_words = MergeSort.sort(words)
    print(f"Sorted: {sorted_words}")
    
    # Sorting with key
    print("\n--- Sorting with Key ---")
    students = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 20},
        {"name": "Charlie", "age": 30}
    ]
    
    sorted_students = MergeSort.sort_with_key(students, key=lambda x: x["age"])
    print(f"Sorted by age: {sorted_students}")
    
    # Natural merge sort
    print("\n--- Natural Merge Sort ---")
    partially_sorted = [1, 2, 3, 1, 2, 3, 1, 2, 3]
    print(f"Partially sorted: {partially_sorted}")
    
    natural_sorted = NaturalMergeSort.sort(partially_sorted)
    print(f"Naturally sorted: {natural_sorted}")
    
    # Stability test
    print("\n--- Stability Test ---")
    tuples = [(3, 'a'), (1, 'b'), (2, 'c'), (1, 'd'), (3, 'e')]
    print(f"Original: {tuples}")
    
    sorted_tuples = MergeSort.sort(tuples)
    print(f"Sorted (stable): {sorted_tuples}")
    
    # Performance test
    print("\n=== Performance Test ===")
    import time
    import random
    
    n = 100000
    large_array = [random.randint(0, 1000000) for _ in range(n)]
    
    start = time.time()
    MergeSort.sort(large_array.copy())
    merge_time = (time.time() - start) * 1000
    
    start = time.time()
    sorted(large_array)
    python_time = (time.time() - start) * 1000
    
    print(f"Merge sort: {merge_time:.2f}ms")
    print(f"Python sort: {python_time:.2f}ms")
    print(f"Ratio: {merge_time/python_time:.2f}x")
    
    # Already sorted array (best case for natural merge sort)
    print("\n--- Best Case (Already Sorted) ---")
    sorted_array = list(range(n))
    
    start = time.time()
    MergeSort.sort(sorted_array.copy())
    merge_sorted_time = (time.time() - start) * 1000
    
    start = time.time()
    NaturalMergeSort.sort(sorted_array.copy())
    natural_sorted_time = (time.time() - start) * 1000
    
    print(f"Regular merge sort: {merge_sorted_time:.2f}ms")
    print(f"Natural merge sort: {natural_sorted_time:.2f}ms")
    print(f"Improvement: {merge_sorted_time/natural_sorted_time:.2f}x")


if __name__ == "__main__":
    main()
