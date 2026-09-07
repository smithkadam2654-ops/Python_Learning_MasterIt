"""
Exponential Search - Search algorithm for infinite/unbounded arrays.
Features: O(log n) time complexity, range finding, and binary search combination.
"""

from typing import List, Optional, TypeVar, Generic
import bisect

T = TypeVar('T')


class ExponentialSearch:
    """Exponential search implementation."""
    
    @staticmethod
    def search(arr: List[T], target: T) -> Optional[int]:
        """
        Search for target using exponential search.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Index of target or None if not found
        """
        if not arr:
            return None
        
        n = len(arr)
        
        # If first element is target
        if arr[0] == target:
            return 0
        
        # Find range where target might be
        i = 1
        while i < n and arr[i] <= target:
            i *= 2
        
        # Apply binary search in found range
        left = i // 2
        right = min(i, n - 1)
        
        return ExponentialSearch._binary_search(arr, left, right, target)
    
    @staticmethod
    def _binary_search(arr: List[T], left: int, right: int, target: T) -> Optional[int]:
        """Binary search helper."""
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return None
    
    @staticmethod
    def search_with_bisect(arr: List[T], target: T) -> Optional[int]:
        """
        Search using exponential range finding with bisect.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Index of target or None if not found
        """
        if not arr:
            return None
        
        if arr[0] == target:
            return 0
        
        n = len(arr)
        i = 1
        
        while i < n and arr[i] <= target:
            i *= 2
        
        left = i // 2
        right = min(i, n)
        
        index = bisect.bisect_left(arr, target, left, right)
        
        if index < n and arr[index] == target:
            return index
        
        return None
    
    @staticmethod
    def search_all(arr: List[T], target: T) -> List[int]:
        """
        Find all occurrences of target.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            List of indices where target occurs
        """
        if not arr:
            return []
        
        index = ExponentialSearch.search(arr, target)
        if index is None:
            return []
        
        # Find leftmost
        left = index
        while left > 0 and arr[left - 1] == target:
            left -= 1
        
        # Find rightmost
        right = index
        while right < len(arr) - 1 and arr[right + 1] == target:
            right += 1
        
        return list(range(left, right + 1))
    
    @staticmethod
    def count_occurrences(arr: List[T], target: T) -> int:
        """
        Count occurrences of target.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Number of occurrences
        """
        return len(ExponentialSearch.search_all(arr, target))
    
    @staticmethod
    def find_first_greater(arr: List[T], target: T) -> Optional[T]:
        """
        Find first element greater than target.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            First greater element or None
        """
        if not arr:
            return None
        
        if arr[-1] <= target:
            return None
        
        # Find range
        i = 1
        while i < len(arr) and arr[i] <= target:
            i *= 2
        
        left = i // 2
        right = min(i, len(arr) - 1)
        
        # Binary search for first greater
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] <= target:
                left = mid + 1
            else:
                right = mid - 1
        
        return arr[left] if left < len(arr) else None
    
    @staticmethod
    def count_comparisons(arr: List[T], target: T) -> int:
        """
        Count number of comparisons made during search.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Number of comparisons
        """
        if not arr:
            return 0
        
        n = len(arr)
        comparisons = 0
        
        if arr[0] == target:
            return 1
        
        comparisons += 1
        
        i = 1
        while i < n and arr[i] <= target:
            comparisons += 1
            i *= 2
        
        # Binary search comparisons
        left = i // 2
        right = min(i, n - 1)
        
        while left <= right:
            comparisons += 1
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return comparisons
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return comparisons


class RecursiveExponentialSearch(ExponentialSearch):
    """Recursive exponential search implementation."""
    
    @staticmethod
    def search(arr: List[T], target: T) -> Optional[int]:
        """
        Search using recursive exponential search.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Index of target or None if not found
        """
        if not arr:
            return None
        
        return RecursiveExponentialSearch._search_recursive(arr, target, 0, 1)
    
    @staticmethod
    def _search_recursive(arr: List[T], target: T, left: int, right: int) -> Optional[int]:
        """Recursive search helper."""
        if right >= len(arr):
            right = len(arr) - 1
        
        if arr[right] == target:
            return right
        
        if arr[right] < target or left > right:
            return None
        
        # Binary search in range
        return RecursiveExponentialSearch._binary_search(arr, left, right, target)


def main() -> None:
    """Demonstrate exponential search."""
    
    print("=== Exponential Search Demo ===")
    
    # Basic search
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    print(f"Data: {data}")
    
    print("\n--- Search ---")
    targets = [1, 8, 16, 5, 17]
    for target in targets:
        index = ExponentialSearch.search(data, target)
        print(f"Search {target}: {index}")
    
    # Search with bisect
    print("\n--- Search with Bisect ---")
    for target in [1, 8, 16]:
        index = ExponentialSearch.search_with_bisect(data, target)
        print(f"Search {target}: {index}")
    
    # Search all
    print("\n--- Search All ---")
    duplicates = [1, 2, 2, 2, 3, 4, 5, 5, 6, 7, 8]
    print(f"Data with duplicates: {duplicates}")
    print(f"All 2s: {ExponentialSearch.search_all(duplicates, 2)}")
    print(f"All 5s: {ExponentialSearch.search_all(duplicates, 5)}")
    
    # Count occurrences
    print(f"\nCount 2s: {ExponentialSearch.count_occurrences(duplicates, 2)}")
    print(f"Count 5s: {ExponentialSearch.count_occurrences(duplicates, 5)}")
    
    # First greater
    print("\n--- First Greater ---")
    print(f"First greater than 5: {ExponentialSearch.find_first_greater(data, 5)}")
    print(f"First greater than 10: {ExponentialSearch.find_first_greater(data, 10)}")
    print(f"First greater than 16: {ExponentialSearch.find_first_greater(data, 16)}")
    
    # Comparison count
    print("\n--- Comparison Count ---")
    for target in [1, 8, 16]:
        comparisons = ExponentialSearch.count_comparisons(data, target)
        print(f"Search {target}: {comparisons} comparisons")
    
    # Recursive search
    print("\n--- Recursive Search ---")
    for target in [1, 8, 16]:
        index = RecursiveExponentialSearch.search(data, target)
        print(f"Search {target}: {index}")
    
    # Performance comparison
    print("\n=== Performance Comparison ===")
    import time
    
    n = 100000
    large_array = list(range(n))
    
    # Exponential search
    start = time.time()
    for _ in range(10000):
        ExponentialSearch.search(large_array, n // 2)
    exp_time = (time.time() - start) * 1000
    
    # Binary search (bisect)
    start = time.time()
    for _ in range(10000):
        bisect.bisect_left(large_array, n // 2)
    binary_time = (time.time() - start) * 1000
    
    print(f"Exponential search (10000 searches): {exp_time:.2f}ms")
    print(f"Binary search (10000 searches): {binary_time:.2f}ms")
    print(f"Ratio: {exp_time/binary_time:.2f}x")
    
    # Different positions
    print("\n--- Search at Different Positions ---")
    positions = [0, n // 4, n // 2, 3 * n // 4, n - 1]
    for pos in positions:
        target = large_array[pos]
        comparisons = ExponentialSearch.count_comparisons(large_array, target)
        print(f"Position {pos}: {comparisons} comparisons")
    
    # Edge cases
    print("\n--- Edge Cases ---")
    
    # Empty array
    print(f"Empty array: {ExponentialSearch.search([], 5)}")
    
    # Single element
    print(f"Single [5], search 5: {ExponentialSearch.search([5], 5)}")
    print(f"Single [5], search 3: {ExponentialSearch.search([5], 3)}")
    
    # Two elements
    print(f"Two [1,2], search 1: {ExponentialSearch.search([1, 2], 1)}")
    print(f"Two [1,2], search 2: {ExponentialSearch.search([1, 2], 2)}")
    
    # All same
    same = [5, 5, 5, 5]
    print(f"All same [5,5,5,5], search 5: {ExponentialSearch.search(same, 5)}")


if __name__ == "__main__":
    main()
