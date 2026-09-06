"""
Radix Sort - Non-comparative sorting algorithm.
Features: LSD and MSD variants, integer and string sorting.
"""

from typing import List, Optional
from collections import deque


class RadixSort:
    """Radix sort implementation."""
    
    @staticmethod
    def sort_integers(arr: List[int]) -> List[int]:
        """
        Sort integers using LSD radix sort.
        
        Args:
            arr: List of integers to sort
            
        Returns:
            Sorted list
        """
        if not arr:
            return []
        
        # Find maximum number to know number of digits
        max_num = max(arr)
        exp = 1  # 10^0, 10^1, 10^2, ...
        
        while max_num // exp > 0:
            arr = RadixSort._counting_sort_by_digit(arr, exp)
            exp *= 10
        
        return arr
    
    @staticmethod
    def _counting_sort_by_digit(arr: List[int], exp: int) -> List[int]:
        """Counting sort based on digit at exp place."""
        n = len(arr)
        output = [0] * n
        count = [0] * 10  # Digits 0-9
        
        # Count occurrences
        for num in arr:
            digit = (num // exp) % 10
            count[digit] += 1
        
        # Change count to cumulative
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        # Build output array
        for i in range(n - 1, -1, -1):
            num = arr[i]
            digit = (num // exp) % 10
            output[count[digit] - 1] = num
            count[digit] -= 1
        
        return output
    
    @staticmethod
    def sort_strings(arr: List[str]) -> List[str]:
        """
        Sort strings using LSD radix sort.
        
        Args:
            arr: List of strings to sort
            
        Returns:
            Sorted list
        """
        if not arr:
            return []
        
        # Find maximum length
        max_len = max(len(s) for s in arr)
        
        # Sort from least significant character (rightmost)
        for pos in range(max_len - 1, -1, -1):
            arr = RadixSort._counting_sort_by_char(arr, pos)
        
        return arr
    
    @staticmethod
    def _counting_sort_by_char(arr: List[str], pos: int) -> List[str]:
        """Counting sort based on character at position."""
        n = len(arr)
        output = ["" for _ in range(n)]
        count = [0] * 256  # ASCII characters
        
        # Count occurrences
        for s in arr:
            char = ord(s[pos]) if pos < len(s) else 0
            count[char] += 1
        
        # Change count to cumulative
        for i in range(1, 256):
            count[i] += count[i - 1]
        
        # Build output array
        for i in range(n - 1, -1, -1):
            s = arr[i]
            char = ord(s[pos]) if pos < len(s) else 0
            output[count[char] - 1] = s
            count[char] -= 1
        
        return output
    
    @staticmethod
    def sort_negative_integers(arr: List[int]) -> List[int]:
        """
        Sort integers including negative numbers.
        
        Args:
            arr: List of integers to sort
            
        Returns:
            Sorted list
        """
        if not arr:
            return []
        
        # Separate positive and negative numbers
        positive = [x for x in arr if x >= 0]
        negative = [-x for x in arr if x < 0]
        
        # Sort positive numbers
        positive_sorted = RadixSort.sort_integers(positive)
        
        # Sort negative numbers (inverted)
        negative_sorted = RadixSort.sort_integers(negative)
        
        # Combine: negative (inverted back) + positive
        result = [-x for x in reversed(negative_sorted)] + positive_sorted
        
        return result


class MSDRadixSort:
    """MSD (Most Significant Digit) radix sort for strings."""
    
    @staticmethod
    def sort(arr: List[str]) -> List[str]:
        """
        Sort strings using MSD radix sort.
        
        Args:
            arr: List of strings to sort
            
        Returns:
            Sorted list
        """
        if not arr:
            return []
        
        result = arr.copy()
        MSDRadixSort._sort_recursive(result, 0, len(result) - 1, 0)
        return result
    
    @staticmethod
    def _sort_recursive(arr: List[str], left: int, right: int, pos: int) -> None:
        """Recursively sort strings by character at position."""
        if left >= right:
            return
        
        # Counting sort by character at position
        count = [0] * 256
        
        for i in range(left, right + 1):
            char = ord(arr[i][pos]) if pos < len(arr[i]) else 0
            count[char] += 1
        
        # Calculate positions
        for i in range(1, 256):
            count[i] += count[i - 1]
        
        # Build output array
        output = [""] * (right - left + 1)
        for i in range(right, left - 1, -1):
            char = ord(arr[i][pos]) if pos < len(arr[i]) else 0
            output[count[char] - 1] = arr[i]
            count[char] -= 1
        
        # Copy back
        for i in range(left, right + 1):
            arr[i] = output[i - left]
        
        # Recursively sort each bucket
        for i in range(256):
            if count[i] > 0:
                new_left = left + (count[i - 1] if i > 0 else 0)
                new_right = left + count[i] - 1
                MSDRadixSort._sort_recursive(arr, new_left, new_right, pos + 1)


def main() -> None:
    """Demonstrate radix sort."""
    
    print("=== Radix Sort Demo ===")
    
    # Integer sorting
    print("--- Integer Sorting ---")
    numbers = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"Original: {numbers}")
    
    sorted_numbers = RadixSort.sort_integers(numbers.copy())
    print(f"Sorted: {sorted_numbers}")
    
    # Negative integers
    print("\n--- Negative Integer Sorting ---")
    neg_numbers = [170, -45, 75, -90, 802, 24, -2, 66]
    print(f"Original: {neg_numbers}")
    
    sorted_neg = RadixSort.sort_negative_integers(neg_numbers.copy())
    print(f"Sorted: {sorted_neg}")
    
    # String sorting (LSD)
    print("\n--- String Sorting (LSD) ---")
    strings = ["banana", "apple", "cherry", "date", "elderberry"]
    print(f"Original: {strings}")
    
    sorted_strings = RadixSort.sort_strings(strings.copy())
    print(f"Sorted: {sorted_strings}")
    
    # String sorting (MSD)
    print("\n--- String Sorting (MSD) ---")
    strings2 = ["banana", "apple", "apricot", "cherry", "date"]
    print(f"Original: {strings2}")
    
    sorted_strings2 = MSDRadixSort.sort(strings2.copy())
    print(f"Sorted: {sorted_strings2}")
    
    # Performance test
    print("\n=== Performance Test ===")
    import time
    import random
    
    n = 100000
    large_numbers = [random.randint(0, 1000000) for _ in range(n)]
    
    start = time.time()
    RadixSort.sort_integers(large_numbers.copy())
    radix_time = (time.time() - start) * 1000
    
    start = time.time()
    sorted(large_numbers)
    python_time = (time.time() - start) * 1000
    
    print(f"Radix sort: {radix_time:.2f}ms")
    print(f"Python sort: {python_time:.2f}ms")
    print(f"Ratio: {radix_time/python_time:.2f}x")
    
    # Fixed-width numbers
    print("\n=== Fixed-Width Numbers ===")
    fixed_numbers = [123, 456, 789, 321, 654, 987]
    print(f"Original: {fixed_numbers}")
    print(f"Sorted: {RadixSort.sort_integers(fixed_numbers.copy())}")


if __name__ == "__main__":
    main()
