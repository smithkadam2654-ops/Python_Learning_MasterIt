"""
Jump Search - Search algorithm for sorted arrays with jumps.
Features: O(√n) time complexity, block-based search, and optimal jump size.
"""

from typing import List, Optional, TypeVar, Generic
import math

T = TypeVar('T')


class JumpSearch:
    """Jump search implementation."""
    
    @staticmethod
    def search(arr: List[T], target: T) -> Optional[int]:
        """
        Search for target using jump search.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Index of target or None if not found
        """
        if not arr:
            return None
        
        n = len(arr)
        step = int(math.sqrt(n))
        prev = 0
        
        # Find block where target might be
        while arr[min(step, n) - 1] < target:
            prev = step
            step += int(math.sqrt(n))
            
            if prev >= n:
                return None
        
        # Linear search in the block
        while arr[prev] < target:
            prev += 1
            
            if prev == min(step, n):
                return None
        
        if arr[prev] == target:
            return prev
        
        return None
    
    @staticmethod
    def search_with_custom_jump(arr: List[T], target: T, jump_size: int) -> Optional[int]:
        """
        Search with custom jump size.
        
        Args:
            arr: Sorted array
            target: Target value
            jump_size: Custom jump size
            
        Returns:
            Index of target or None if not found
        """
        if not arr:
            return None
        
        n = len(arr)
        step = jump_size
        prev = 0
        
        while arr[min(step, n) - 1] < target:
            prev = step
            step += jump_size
            
            if prev >= n:
                return None
        
        while arr[prev] < target:
            prev += 1
            
            if prev == min(step, n):
                return None
        
        if arr[prev] == target:
            return prev
        
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
        
        index = JumpSearch.search(arr, target)
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
    def optimal_jump_size(n: int) -> int:
        """
        Calculate optimal jump size.
        
        Args:
            n: Array length
            
        Returns:
            Optimal jump size
        """
        return int(math.sqrt(n))
    
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
        step = int(math.sqrt(n))
        prev = 0
        comparisons = 0
        
        while arr[min(step, n) - 1] < target:
            comparisons += 1
            prev = step
            step += int(math.sqrt(n))
            
            if prev >= n:
                return comparisons
        
        while arr[prev] < target:
            comparisons += 1
            prev += 1
            
            if prev == min(step, n):
                return comparisons
        
        comparisons += 1  # Final comparison
        
        return comparisons


class BidirectionalJumpSearch(JumpSearch):
    """Bidirectional jump search (search from both ends)."""
    
    @staticmethod
    def search(arr: List[T], target: T) -> Optional[int]:
        """
        Search using bidirectional jump search.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Index of target or None if not found
        """
        if not arr:
            return None
        
        n = len(arr)
        step = int(math.sqrt(n))
        
        left = 0
        right = n - 1
        
        while left <= right:
            # Jump from left
            left_end = min(left + step, n)
            if arr[left_end - 1] >= target:
                for i in range(left, left_end):
                    if arr[i] == target:
                        return i
                    if arr[i] > target:
                        return None
                return None
            
            # Jump from right
            right_start = max(right - step, 0)
            if arr[right_start] <= target:
                for i in range(right, right_start - 1, -1):
                    if arr[i] == target:
                        return i
                    if arr[i] < target:
                        return None
                return None
            
            left = left_end
            right = right_start - 1
        
        return None


def main() -> None:
    """Demonstrate jump search."""
    
    print("=== Jump Search Demo ===")
    
    # Basic search
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    print(f"Data: {data}")
    print(f"Optimal jump size: {JumpSearch.optimal_jump_size(len(data))}")
    
    print("\n--- Search ---")
    targets = [1, 8, 16, 5, 17]
    for target in targets:
        index = JumpSearch.search(data, target)
        print(f"Search {target}: {index}")
    
    # Custom jump size
    print("\n--- Custom Jump Size ---")
    custom_index = JumpSearch.search_with_custom_jump(data, 8, 4)
    print(f"Search 8 with jump size 4: {custom_index}")
    
    # Search all
    print("\n--- Search All ---")
    duplicates = [1, 2, 2, 2, 3, 4, 5, 5, 6, 7, 8]
    print(f"Data with duplicates: {duplicates}")
    print(f"All 2s: {JumpSearch.search_all(duplicates, 2)}")
    print(f"All 5s: {JumpSearch.search_all(duplicates, 5)}")
    
    # Comparison count
    print("\n--- Comparison Count ---")
    for target in [1, 8, 16]:
        comparisons = JumpSearch.count_comparisons(data, target)
        print(f"Search {target}: {comparisons} comparisons")
    
    # Bidirectional search
    print("\n--- Bidirectional Jump Search ---")
    for target in [1, 8, 16]:
        index = BidirectionalJumpSearch.search(data, target)
        print(f"Search {target}: {index}")
    
    # Performance comparison
    print("\n=== Performance Comparison ===")
    import time
    import bisect
    
    n = 100000
    large_array = list(range(n))
    
    # Jump search
    start = time.time()
    for _ in range(10000):
        JumpSearch.search(large_array, n // 2)
    jump_time = (time.time() - start) * 1000
    
    # Binary search (bisect)
    start = time.time()
    for _ in range(10000):
        bisect.bisect_left(large_array, n // 2)
    binary_time = (time.time() - start) * 1000
    
    # Linear search
    start = time.time()
    for _ in range(100):
        large_array.index(n // 2)
    linear_time = (time.time() - start) * 1000
    
    print(f"Jump search (10000 searches): {jump_time:.2f}ms")
    print(f"Binary search (10000 searches): {binary_time:.2f}ms")
    print(f"Linear search (100 searches): {linear_time:.2f}ms")
    print(f"Jump vs Binary ratio: {jump_time/binary_time:.2f}x")
    
    # Different positions
    print("\n--- Search at Different Positions ---")
    positions = [0, n // 4, n // 2, 3 * n // 4, n - 1]
    for pos in positions:
        target = large_array[pos]
        comparisons = JumpSearch.count_comparisons(large_array, target)
        print(f"Position {pos}: {comparisons} comparisons")
    
    # Optimal jump size analysis
    print("\n--- Optimal Jump Size Analysis ---")
    sizes = [100, 1000, 10000, 100000]
    for size in sizes:
        optimal = JumpSearch.optimal_jump_size(size)
        print(f"Size {size}: optimal jump = {optimal}")
    
    # Edge cases
    print("\n--- Edge Cases ---")
    
    # Empty array
    print(f"Empty array: {JumpSearch.search([], 5)}")
    
    # Single element
    print(f"Single [5], search 5: {JumpSearch.search([5], 5)}")
    print(f"Single [5], search 3: {JumpSearch.search([5], 3)}")
    
    # Two elements
    print(f"Two [1,2], search 1: {JumpSearch.search([1, 2], 1)}")
    print(f"Two [1,2], search 2: {JumpSearch.search([1, 2], 2)}")
    
    # All same
    same = [5, 5, 5, 5]
    print(f"All same [5,5,5,5], search 5: {JumpSearch.search(same, 5)}")


if __name__ == "__main__":
    main()
