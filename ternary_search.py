"""
Ternary Search - Divide and conquer search for unimodal functions.
Features: O(log n) time complexity, two midpoints, and peak finding.
"""

from typing import List, Optional, TypeVar, Generic, Callable

T = TypeVar('T')


class TernarySearch:
    """Ternary search implementation."""
    
    @staticmethod
    def search(arr: List[T], target: T) -> Optional[int]:
        """
        Search for target in sorted array using ternary search.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Index of target or None if not found
        """
        if not arr:
            return None
        
        return TernarySearch._search_recursive(arr, target, 0, len(arr) - 1)
    
    @staticmethod
    def _search_recursive(arr: List[T], target: T, left: int, right: int) -> Optional[int]:
        """Recursive ternary search."""
        if left > right:
            return None
        
        # Divide into three parts
        third = (right - left) // 3
        mid1 = left + third
        mid2 = right - third
        
        if arr[mid1] == target:
            return mid1
        if arr[mid2] == target:
            return mid2
        
        if target < arr[mid1]:
            return TernarySearch._search_recursive(arr, target, left, mid1 - 1)
        elif target > arr[mid2]:
            return TernarySearch._search_recursive(arr, target, mid2 + 1, right)
        else:
            return TernarySearch._search_recursive(arr, target, mid1 + 1, mid2 - 1)
    
    @staticmethod
    def search_iterative(arr: List[T], target: T) -> Optional[int]:
        """
        Iterative ternary search.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Index of target or None if not found
        """
        if not arr:
            return None
        
        left = 0
        right = len(arr) - 1
        
        while left <= right:
            third = (right - left) // 3
            mid1 = left + third
            mid2 = right - third
            
            if arr[mid1] == target:
                return mid1
            if arr[mid2] == target:
                return mid2
            
            if target < arr[mid1]:
                right = mid1 - 1
            elif target > arr[mid2]:
                left = mid2 + 1
            else:
                left = mid1 + 1
                right = mid2 - 1
        
        return None
    
    @staticmethod
    def find_peak(arr: List[T]) -> Optional[int]:
        """
        Find peak element in unimodal array.
        
        Args:
            arr: Unimodal array (first increasing, then decreasing)
            
        Returns:
            Index of peak or None
        """
        if not arr:
            return None
        
        return TernarySearch._find_peak_recursive(arr, 0, len(arr) - 1)
    
    @staticmethod
    def _find_peak_recursive(arr: List[T], left: int, right: int) -> int:
        """Recursive peak finding."""
        if left == right:
            return left
        
        if right == left + 1:
            return left if arr[left] > arr[right] else right
        
        third = (right - left) // 3
        mid1 = left + third
        mid2 = right - third
        
        if arr[mid1] > arr[mid2]:
            return TernarySearch._find_peak_recursive(arr, left, mid2 - 1)
        else:
            return TernarySearch._find_peak_recursive(arr, mid1 + 1, right)
    
    @staticmethod
    def find_minimum(arr: List[T]) -> Optional[T]:
        """
        Find minimum in unimodal array (first decreasing, then increasing).
        
        Args:
            arr: Unimodal array (valley)
            
        Returns:
            Minimum value or None
        """
        if not arr:
            return None
        
        return TernarySearch._find_minimum_recursive(arr, 0, len(arr) - 1)
    
    @staticmethod
    def _find_minimum_recursive(arr: List[T], left: int, right: int) -> T:
        """Recursive minimum finding."""
        if left == right:
            return arr[left]
        
        if right == left + 1:
            return arr[left] if arr[left] < arr[right] else arr[right]
        
        third = (right - left) // 3
        mid1 = left + third
        mid2 = right - third
        
        if arr[mid1] < arr[mid2]:
            return TernarySearch._find_minimum_recursive(arr, left, mid2 - 1)
        else:
            return TernarySearch._find_minimum_recursive(arr, mid1 + 1, right)


class TernarySearchFunction(TernarySearch):
    """Ternary search for finding maximum/minimum of unimodal functions."""
    
    @staticmethod
    def find_maximum(func: Callable[[float], float], left: float, 
                    right: float, epsilon: float = 1e-6) -> float:
        """
        Find maximum of unimodal function in range [left, right].
        
        Args:
            func: Unimodal function
            left: Left bound
            right: Right bound
            epsilon: Precision
            
        Returns:
            x value where function is maximum
        """
        while right - left > epsilon:
            third = (right - left) / 3
            mid1 = left + third
            mid2 = right - third
            
            if func(mid1) < func(mid2):
                left = mid1
            else:
                right = mid2
        
        return (left + right) / 2
    
    @staticmethod
    def find_minimum(func: Callable[[float], float], left: float, 
                    right: float, epsilon: float = 1e-6) -> float:
        """
        Find minimum of unimodal function in range [left, right].
        
        Args:
            func: Unimodal function
            left: Left bound
            right: Right bound
            epsilon: Precision
            
        Returns:
            x value where function is minimum
        """
        while right - left > epsilon:
            third = (right - left) / 3
            mid1 = left + third
            mid2 = right - third
            
            if func(mid1) > func(mid2):
                left = mid1
            else:
                right = mid2
        
        return (left + right) / 2


def main() -> None:
    """Demonstrate ternary search."""
    
    print("=== Ternary Search Demo ===")
    
    # Basic search
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    print(f"Data: {data}")
    
    print("\n--- Recursive Search ---")
    targets = [1, 8, 16, 5, 17]
    for target in targets:
        index = TernarySearch.search(data, target)
        print(f"Search {target}: {index}")
    
    # Iterative search
    print("\n--- Iterative Search ---")
    for target in [1, 8, 16]:
        index = TernarySearch.search_iterative(data, target)
        print(f"Search {target}: {index}")
    
    # Peak finding
    print("\n--- Peak Finding ---")
    unimodal = [1, 3, 5, 7, 9, 11, 10, 8, 6, 4, 2]
    print(f"Unimodal array: {unimodal}")
    peak_index = TernarySearch.find_peak(unimodal)
    print(f"Peak at index {peak_index}: {unimodal[peak_index]}")
    
    # Minimum finding
    print("\n--- Minimum Finding ---")
    valley = [10, 8, 6, 4, 2, 1, 3, 5, 7, 9]
    print(f"Valley array: {valley}")
    minimum = TernarySearch.find_minimum(valley)
    print(f"Minimum: {minimum}")
    
    # Function optimization
    print("\n--- Function Optimization ---")
    
    # Parabola: -(x-2)^2 + 4 (maximum at x=2)
    def parabola(x: float) -> float:
        return -(x - 2) ** 2 + 4
    
    max_x = TernarySearchFunction.find_maximum(parabola, 0, 4)
    print(f"Maximum of parabola at x = {max_x:.6f}")
    print(f"Value: {parabola(max_x):.6f}")
    
    # Inverted parabola: (x-2)^2 (minimum at x=2)
    def inverted_parabola(x: float) -> float:
        return (x - 2) ** 2
    
    min_x = TernarySearchFunction.find_minimum(inverted_parabola, 0, 4)
    print(f"Minimum of inverted parabola at x = {min_x:.6f}")
    print(f"Value: {inverted_parabola(min_x):.6f}")
    
    # Performance comparison
    print("\n=== Performance Comparison ===")
    import time
    import bisect
    
    n = 100000
    large_array = list(range(n))
    
    # Ternary search
    start = time.time()
    for _ in range(10000):
        TernarySearch.search(large_array, n // 2)
    ternary_time = (time.time() - start) * 1000
    
    # Binary search (bisect)
    start = time.time()
    for _ in range(10000):
        bisect.bisect_left(large_array, n // 2)
    binary_time = (time.time() - start) * 1000
    
    print(f"Ternary search (10000 searches): {ternary_time:.2f}ms")
    print(f"Binary search (10000 searches): {binary_time:.2f}ms")
    print(f"Ratio: {ternary_time/binary_time:.2f}x")
    
    # Different positions
    print("\n--- Search at Different Positions ---")
    positions = [0, n // 4, n // 2, 3 * n // 4, n - 1]
    for pos in positions:
        target = large_array[pos]
        index = TernarySearch.search(large_array, target)
        print(f"Position {pos}: found at {index}")
    
    # Edge cases
    print("\n--- Edge Cases ---")
    
    # Empty array
    print(f"Empty array: {TernarySearch.search([], 5)}")
    
    # Single element
    print(f"Single [5], search 5: {TernarySearch.search([5], 5)}")
    print(f"Single [5], search 3: {TernarySearch.search([5], 3)}")
    
    # Two elements
    print(f"Two [1,2], search 1: {TernarySearch.search([1, 2], 1)}")
    print(f"Two [1,2], search 2: {TernarySearch.search([1, 2], 2)}")
    
    # All same
    same = [5, 5, 5, 5]
    print(f"All same [5,5,5,5], search 5: {TernarySearch.search(same, 5)}")


if __name__ == "__main__":
    main()
