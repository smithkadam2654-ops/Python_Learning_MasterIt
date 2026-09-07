"""
Interpolation Search - Improved binary search for uniformly distributed data.
Features: O(log log n) average case, probe position estimation, and adaptive search.
"""

from typing import List, Optional, TypeVar, Generic

T = TypeVar('T', int, float)


class InterpolationSearch:
    """Interpolation search implementation."""
    
    @staticmethod
    def search(arr: List[T], target: T) -> Optional[int]:
        """
        Search for target using interpolation search.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Index of target or None if not found
        """
        if not arr:
            return None
        
        low = 0
        high = len(arr) - 1
        
        while low <= high and target >= arr[low] and target <= arr[high]:
            # Calculate probe position using interpolation formula
            if arr[high] == arr[low]:
                # All elements are same
                if arr[low] == target:
                    return low
                return None
            
            # Probe position formula
            pos = low + int(((target - arr[low]) * (high - low)) / 
                          (arr[high] - arr[low]))
            
            if pos < low or pos > high:
                break
            
            if arr[pos] == target:
                return pos
            elif arr[pos] < target:
                low = pos + 1
            else:
                high = pos - 1
        
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
        
        index = InterpolationSearch.search(arr, target)
        if index is None:
            return []
        
        # Find leftmost occurrence
        left = index
        while left > 0 and arr[left - 1] == target:
            left -= 1
        
        # Find rightmost occurrence
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
        return len(InterpolationSearch.search_all(arr, target))
    
    @staticmethod
    def find_closest(arr: List[T], target: T) -> Optional[T]:
        """
        Find closest value to target.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Closest value or None if array empty
        """
        if not arr:
            return None
        
        if target <= arr[0]:
            return arr[0]
        if target >= arr[-1]:
            return arr[-1]
        
        low = 0
        high = len(arr) - 1
        
        while low <= high and target >= arr[low] and target <= arr[high]:
            if arr[high] == arr[low]:
                return arr[low]
            
            pos = low + int(((target - arr[low]) * (high - low)) / 
                          (arr[high] - arr[low]))
            
            if pos < low or pos > high:
                break
            
            if arr[pos] == target:
                return arr[pos]
            elif arr[pos] < target:
                low = pos + 1
            else:
                high = pos - 1
        
        # Find closest among neighbors
        if low < len(arr) and high >= 0:
            if abs(arr[low] - target) < abs(arr[high] - target):
                return arr[low]
            return arr[high]
        
        return arr[high] if high >= 0 else arr[low]


class ExponentialInterpolationSearch(InterpolationSearch):
    """Hybrid exponential + interpolation search."""
    
    @staticmethod
    def search(arr: List[T], target: T) -> Optional[int]:
        """
        Search using exponential search followed by interpolation.
        
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
        
        # Find range using exponential search
        bound = 1
        while bound < len(arr) and arr[bound] < target:
            bound *= 2
        
        # Apply interpolation search in found range
        left = bound // 2
        right = min(bound, len(arr) - 1)
        
        while left <= right and target >= arr[left] and target <= arr[right]:
            if arr[right] == arr[left]:
                if arr[left] == target:
                    return left
                return None
            
            pos = left + int(((target - arr[left]) * (right - left)) / 
                           (arr[right] - arr[left]))
            
            if pos < left or pos > right:
                break
            
            if arr[pos] == target:
                return pos
            elif arr[pos] < target:
                left = pos + 1
            else:
                right = pos - 1
        
        return None


def main() -> None:
    """Demonstrate interpolation search."""
    
    print("=== Interpolation Search Demo ===")
    
    # Uniformly distributed data
    uniform_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Uniform data: {uniform_data}")
    
    # Search
    print("\n--- Search ---")
    targets = [5, 1, 10, 7, 11]
    for target in targets:
        index = InterpolationSearch.search(uniform_data, target)
        print(f"Search {target}: {index}")
    
    # Search all occurrences
    print("\n--- Search All ---")
    duplicates = [1, 2, 2, 2, 3, 4, 5, 5, 6]
    print(f"Data with duplicates: {duplicates}")
    print(f"All 2s: {InterpolationSearch.search_all(duplicates, 2)}")
    print(f"All 5s: {InterpolationSearch.search_all(duplicates, 5)}")
    
    # Count occurrences
    print(f"\nCount 2s: {InterpolationSearch.count_occurrences(duplicates, 2)}")
    print(f"Count 5s: {InterpolationSearch.count_occurrences(duplicates, 5)}")
    
    # Find closest
    print("\n--- Find Closest ---")
    print(f"Closest to 5.5: {InterpolationSearch.find_closest(uniform_data, 5.5)}")
    print(f"Closest to 0: {InterpolationSearch.find_closest(uniform_data, 0)}")
    print(f"Closest to 11: {InterpolationSearch.find_closest(uniform_data, 11)}")
    
    # Non-uniform data
    print("\n--- Non-Uniform Data ---")
    non_uniform = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    print(f"Non-uniform data: {non_uniform}")
    
    for target in [20, 55, 100]:
        index = InterpolationSearch.search(non_uniform, target)
        print(f"Search {target}: {index}")
    
    # Exponential interpolation search
    print("\n--- Exponential Interpolation Search ---")
    large_uniform = list(range(1, 10001))
    
    start = 0  # Placeholder for timing
    index = ExponentialInterpolationSearch.search(large_uniform, 5000)
    print(f"Found 5000 at index: {index}")
    
    # Performance comparison
    print("\n=== Performance Comparison ===")
    import time
    import bisect
    
    n = 100000
    uniform_array = list(range(n))
    
    # Interpolation search
    start = time.time()
    for _ in range(10000):
        InterpolationSearch.search(uniform_array, n // 2)
    interp_time = (time.time() - start) * 1000
    
    # Binary search (bisect)
    start = time.time()
    for _ in range(10000):
        bisect.bisect_left(uniform_array, n // 2)
    binary_time = (time.time() - start) * 1000
    
    print(f"Interpolation search (10000 searches): {interp_time:.2f}ms")
    print(f"Binary search (10000 searches): {binary_time:.2f}ms")
    print(f"Ratio: {interp_time/binary_time:.2f}x")
    
    # Non-uniform performance
    print("\n--- Non-Uniform Performance ---")
    non_uniform_array = [i * 10 for i in range(n)]
    
    start = time.time()
    for _ in range(10000):
        InterpolationSearch.search(non_uniform_array, n * 5)
    interp_non_uniform = (time.time() - start) * 1000
    
    start = time.time()
    for _ in range(10000):
        bisect.bisect_left(non_uniform_array, n * 5)
    binary_non_uniform = (time.time() - start) * 1000
    
    print(f"Interpolation (non-uniform): {interp_non_uniform:.2f}ms")
    print(f"Binary (non-uniform): {binary_non_uniform:.2f}ms")
    print(f"Ratio: {interp_non_uniform/binary_non_uniform:.2f}x")
    
    # Edge cases
    print("\n--- Edge Cases ---")
    
    # Empty array
    print(f"Empty array: {InterpolationSearch.search([], 5)}")
    
    # Single element
    print(f"Single element [5], search 5: {InterpolationSearch.search([5], 5)}")
    print(f"Single element [5], search 3: {InterpolationSearch.search([5], 3)}")
    
    # All same elements
    same = [5, 5, 5, 5, 5]
    print(f"All same [5,5,5,5,5], search 5: {InterpolationSearch.search(same, 5)}")
    print(f"All same [5,5,5,5,5], search 3: {InterpolationSearch.search(same, 3)}")


if __name__ == "__main__":
    main()
