"""
Counting Sort - Non-comparative integer sorting algorithm.
Features: O(n+k) time complexity, stable sort, and limited range requirement.
"""

from typing import List


class CountingSort:
    """Counting sort implementation."""
    
    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        """
        Sort array using counting sort.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        if not arr:
            return []
        
        # Find range
        min_val = min(arr)
        max_val = max(arr)
        range_val = max_val - min_val + 1
        
        # Create count array
        count = [0] * range_val
        output = [0] * len(arr)
        
        # Count occurrences
        for num in arr:
            count[num - min_val] += 1
        
        # Calculate cumulative count
        for i in range(1, range_val):
            count[i] += count[i - 1]
        
        # Build output array (stable)
        for num in reversed(arr):
            output[count[num - min_val] - 1] = num
            count[num - min_val] -= 1
        
        return output
    
    @staticmethod
    def sort_unsigned(arr: List[int]) -> List[int]:
        """
        Sort array assuming non-negative integers.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        if not arr:
            return []
        
        max_val = max(arr)
        
        # Create count array
        count = [0] * (max_val + 1)
        output = [0] * len(arr)
        
        # Count occurrences
        for num in arr:
            count[num] += 1
        
        # Calculate cumulative count
        for i in range(1, max_val + 1):
            count[i] += count[i - 1]
        
        # Build output array
        for num in reversed(arr):
            output[count[num] - 1] = num
            count[num] -= 1
        
        return output
    
    @staticmethod
    def sort_simple(arr: List[int]) -> List[int]:
        """
        Simple counting sort (not stable).
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        if not arr:
            return []
        
        min_val = min(arr)
        max_val = max(arr)
        range_val = max_val - min_val + 1
        
        # Create count array
        count = [0] * range_val
        
        # Count occurrences
        for num in arr:
            count[num - min_val] += 1
        
        # Build output array
        output = []
        for i, c in enumerate(count):
            output.extend([i + min_val] * c)
        
        return output
    
    @staticmethod
    def count_frequencies(arr: List[int]) -> dict:
        """
        Count frequency of each element.
        
        Args:
            arr: Array to analyze
            
        Returns:
            Dictionary of element frequencies
        """
        if not arr:
            return {}
        
        min_val = min(arr)
        max_val = max(arr)
        range_val = max_val - min_val + 1
        
        count = [0] * range_val
        
        for num in arr:
            count[num - min_val] += 1
        
        # Convert to dictionary
        freq = {}
        for i, c in enumerate(count):
            if c > 0:
                freq[i + min_val] = c
        
        return freq


class RadixCountingSort:
    """Counting sort used within radix sort."""
    
    @staticmethod
    def sort_by_digit(arr: List[int], exp: int) -> List[int]:
        """
        Sort array by specific digit using counting sort.
        
        Args:
            arr: Array to sort
            exp: Exponent (1, 10, 100, etc.)
            
        Returns:
            Sorted array
        """
        n = len(arr)
        output = [0] * n
        count = [0] * 10  # Digits 0-9
        
        # Count occurrences of digit
        for num in arr:
            digit = (num // exp) % 10
            count[digit] += 1
        
        # Calculate cumulative count
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        # Build output array
        for num in reversed(arr):
            digit = (num // exp) % 10
            output[count[digit] - 1] = num
            count[digit] -= 1
        
        return output


def main() -> None:
    """Demonstrate counting sort."""
    
    print("=== Counting Sort Demo ===")
    
    # Basic sorting
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {numbers}")
    
    sorted_numbers = CountingSort.sort(numbers)
    print(f"Sorted: {sorted_numbers}")
    
    # Unsigned sorting
    print("\n--- Unsigned Sorting ---")
    unsigned = [5, 2, 8, 1, 9, 3]
    print(f"Original: {unsigned}")
    
    unsigned_sorted = CountingSort.sort_unsigned(unsigned)
    print(f"Sorted (unsigned): {unsigned_sorted}")
    
    # Simple sorting
    print("\n--- Simple Sorting ---")
    simple = [4, 2, 2, 8, 3, 3, 1]
    print(f"Original: {simple}")
    
    simple_sorted = CountingSort.sort_simple(simple)
    print(f"Sorted (simple): {simple_sorted}")
    
    # Frequency counting
    print("\n--- Frequency Counting ---")
    freq = CountingSort.count_frequencies(simple)
    print(f"Frequencies: {freq}")
    
    # Stability test
    print("\n--- Stability Test ---")
    # Counting sort is stable when using cumulative count
    tuples = [(3, 'a'), (1, 'b'), (2, 'c'), (1, 'd'), (3, 'e')]
    keys = [t[0] for t in tuples]
    
    sorted_keys = CountingSort.sort(keys)
    print(f"Original keys: {keys}")
    print(f"Sorted keys: {sorted_keys}")
    
    # Performance test
    print("\n=== Performance Test ===")
    import time
    import random
    
    n = 100000
    # Small range for counting sort
    small_range = [random.randint(0, 1000) for _ in range(n)]
    
    # Counting sort
    start = time.time()
    CountingSort.sort(small_range.copy())
    counting_time = (time.time() - start) * 1000
    
    # Python sort
    start = time.time()
    sorted(small_range)
    python_time = (time.time() - start) * 1000
    
    print(f"Counting sort: {counting_time:.2f}ms")
    print(f"Python sort: {python_time:.2f}ms")
    print(f"Ratio: {counting_time/python_time:.2f}x")
    
    # Large range (counting sort disadvantage)
    print("\n--- Large Range ---")
    large_range = [random.randint(0, 1000000) for _ in range(10000)]
    
    start = time.time()
    CountingSort.sort(large_range.copy())
    counting_large_time = (time.time() - start) * 1000
    
    start = time.time()
    sorted(large_range)
    python_large_time = (time.time() - start) * 1000
    
    print(f"Counting sort (large range): {counting_large_time:.2f}ms")
    print(f"Python sort (large range): {python_large_time:.2f}ms")
    print(f"Ratio: {counting_large_time/python_large_time:.2f}x")
    
    # Radix counting sort
    print("\n--- Radix Counting Sort ---")
    radix_numbers = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"Original: {radix_numbers}")
    
    exp = 1
    while max(radix_numbers) // exp > 0:
        radix_numbers = RadixCountingSort.sort_by_digit(radix_numbers, exp)
        exp *= 10
    
    print(f"Sorted by radix: {radix_numbers}")
    
    # Edge cases
    print("\n--- Edge Cases ---")
    
    # Empty array
    empty = []
    print(f"Empty: {CountingSort.sort(empty)}")
    
    # Single element
    single = [5]
    print(f"Single: {CountingSort.sort(single)}")
    
    # Already sorted
    sorted_input = [1, 2, 3, 4, 5]
    print(f"Already sorted: {CountingSort.sort(sorted_input)}")
    
    # Reverse sorted
    reverse = [5, 4, 3, 2, 1]
    print(f"Reverse sorted: {CountingSort.sort(reverse)}")
    
    # All same
    same = [5, 5, 5, 5]
    print(f"All same: {CountingSort.sort(same)}")


if __name__ == "__main__":
    main()
