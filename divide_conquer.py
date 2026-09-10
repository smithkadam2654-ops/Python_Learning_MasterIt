"""
Divide and Conquer - Recursive problem-solving pattern.
Features: Binary search variants, merge sort, and tree problems.
"""

from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')


class DivideConquer:
    """Divide and conquer algorithm implementations."""
    
    @staticmethod
    def binary_search(arr: List[T], target: T) -> Optional[int]:
        """
        Standard binary search.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Index of target or None
        """
        left, right = 0, len(arr) - 1
        
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
    def binary_search_leftmost(arr: List[T], target: T) -> Optional[int]:
        """
        Find leftmost occurrence of target.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Leftmost index or None
        """
        left, right = 0, len(arr) - 1
        result = None
        
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] == target:
                result = mid
                right = mid - 1  # Continue searching left
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    @staticmethod
    def binary_search_rightmost(arr: List[T], target: T) -> Optional[int]:
        """
        Find rightmost occurrence of target.
        
        Args:
            arr: Sorted array
            target: Target value
            
        Returns:
            Rightmost index or None
        """
        left, right = 0, len(arr) - 1
        result = None
        
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] == target:
                result = mid
                left = mid + 1  # Continue searching right
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    @staticmethod
    def search_rotated_sorted(arr: List[T], target: T) -> Optional[int]:
        """
        Search in rotated sorted array.
        
        Args:
            arr: Rotated sorted array
            target: Target value
            
        Returns:
            Index of target or None
        """
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return mid
            
            # Left half is sorted
            if arr[left] <= arr[mid]:
                if arr[left] <= target < arr[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            # Right half is sorted
            else:
                if arr[mid] < target <= arr[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        
        return None
    
    @staticmethod
    def find_min_rotated(arr: List[T]) -> Optional[int]:
        """
        Find minimum in rotated sorted array.
        
        Args:
            arr: Rotated sorted array
            
        Returns:
            Index of minimum or None
        """
        if not arr:
            return None
        
        left, right = 0, len(arr) - 1
        
        while left < right:
            mid = (left + right) // 2
            
            if arr[mid] > arr[right]:
                left = mid + 1
            else:
                right = mid
        
        return left
    
    @staticmethod
    def find_peak_element(arr: List[T]) -> Optional[int]:
        """
        Find a peak element (greater than neighbors).
        
        Args:
            arr: Array
            
        Returns:
            Index of peak or None
        """
        if not arr:
            return None
        
        left, right = 0, len(arr) - 1
        
        while left < right:
            mid = (left + right) // 2
            
            if arr[mid] < arr[mid + 1]:
                left = mid + 1
            else:
                right = mid
        
        return left
    
    @staticmethod
    def find_kth_largest(arr: List[T], k: int) -> Optional[T]:
        """
        Find kth largest element using quickselect.
        
        Args:
            arr: Array
            k: kth largest (1-indexed)
            
        Returns:
            kth largest element or None
        """
        if not arr or k < 1 or k > len(arr):
            return None
        
        return DivideConquer._quickselect(arr, 0, len(arr) - 1, len(arr) - k)
    
    @staticmethod
    def _quickselect(arr: List[T], left: int, right: int, k: int) -> T:
        """Quickselect helper."""
        if left == right:
            return arr[left]
        
        pivot_index = DivideConquer._partition(arr, left, right)
        
        if k == pivot_index:
            return arr[k]
        elif k < pivot_index:
            return DivideConquer._quickselect(arr, left, pivot_index - 1, k)
        else:
            return DivideConquer._quickselect(arr, pivot_index + 1, right, k)
    
    @staticmethod
    def _partition(arr: List[T], left: int, right: int) -> int:
        """Partition for quickselect."""
        pivot = arr[right]
        i = left
        
        for j in range(left, right):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        
        arr[i], arr[right] = arr[right], arr[i]
        return i
    
    @staticmethod
    def merge_sort(arr: List[T]) -> List[T]:
        """
        Merge sort implementation.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        mid = len(arr) // 2
        left = DivideConquer.merge_sort(arr[:mid])
        right = DivideConquer.merge_sort(arr[mid:])
        
        return DivideConquer._merge(left, right)
    
    @staticmethod
    def _merge(left: List[T], right: List[T]) -> List[T]:
        """Merge two sorted arrays."""
        result = []
        i, j = 0, 0
        
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
    def quick_sort(arr: List[T]) -> List[T]:
        """
        Quick sort implementation.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return DivideConquer.quick_sort(left) + middle + DivideConquer.quick_sort(right)
    
    @staticmethod
    def count_inversions(arr: List[T]) -> int:
        """
        Count inversions in array using merge sort.
        
        Args:
            arr: Array
            
        Returns:
            Number of inversions
        """
        if len(arr) <= 1:
            return 0
        
        return DivideConquer._count_inversions_helper(arr)[1]
    
    @staticmethod
    def _count_inversions_helper(arr: List[T]) -> tuple:
        """Helper for counting inversions."""
        if len(arr) <= 1:
            return (arr, 0)
        
        mid = len(arr) // 2
        left, left_inv = DivideConquer._count_inversions_helper(arr[:mid])
        right, right_inv = DivideConquer._count_inversions_helper(arr[mid:])
        
        merged, split_inv = DivideConquer._count_split_inversions(left, right)
        
        return (merged, left_inv + right_inv + split_inv)
    
    @staticmethod
    def _count_split_inversions(left: List[T], right: List[T]) -> tuple:
        """Count split inversions during merge."""
        result = []
        i, j = 0, 0
        inversions = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                inversions += len(left) - i
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        
        return (result, inversions)
    
    @staticmethod
    def maximum_subarray(arr: List[int]) -> tuple:
        """
        Find maximum subarray using divide and conquer.
        
        Args:
            arr: Array of integers
            
        Returns:
            Tuple of (max_sum, start_index, end_index)
        """
        if not arr:
            return (0, 0, 0)
        
        return DivideConquer._max_subarray_helper(arr, 0, len(arr) - 1)
    
    @staticmethod
    def _max_subarray_helper(arr: List[int], left: int, right: int) -> tuple:
        """Helper for maximum subarray."""
        if left == right:
            return (arr[left], left, right)
        
        mid = (left + right) // 2
        
        # Maximum subarray in left half
        left_max, left_start, left_end = DivideConquer._max_subarray_helper(arr, left, mid)
        
        # Maximum subarray in right half
        right_max, right_start, right_end = DivideConquer._max_subarray_helper(arr, mid + 1, right)
        
        # Maximum subarray crossing middle
        cross_max, cross_start, cross_end = DivideConquer._max_crossing_subarray(arr, left, mid, right)
        
        # Return maximum of three
        if left_max >= right_max and left_max >= cross_max:
            return (left_max, left_start, left_end)
        elif right_max >= left_max and right_max >= cross_max:
            return (right_max, right_start, right_end)
        else:
            return (cross_max, cross_start, cross_end)
    
    @staticmethod
    def _max_crossing_subarray(arr: List[int], left: int, mid: int, right: int) -> tuple:
        """Find maximum subarray crossing midpoint."""
        # Left of mid
        left_sum = float('-inf')
        current_sum = 0
        max_left = mid
        
        for i in range(mid, left - 1, -1):
            current_sum += arr[i]
            if current_sum > left_sum:
                left_sum = current_sum
                max_left = i
        
        # Right of mid
        right_sum = float('-inf')
        current_sum = 0
        max_right = mid + 1
        
        for i in range(mid + 1, right + 1):
            current_sum += arr[i]
            if current_sum > right_sum:
                right_sum = current_sum
                max_right = i
        
        return (left_sum + right_sum, max_left, max_right)
    
    @staticmethod
    def power(x: float, n: int) -> float:
        """
        Calculate x^n using divide and conquer.
        
        Args:
            x: Base
            n: Exponent (can be negative)
            
        Returns:
            x raised to power n
        """
        if n == 0:
            return 1
        
        if n < 0:
            return 1 / DivideConquer.power(x, -n)
        
        if n % 2 == 0:
            half = DivideConquer.power(x, n // 2)
            return half * half
        else:
            return x * DivideConquer.power(x, n - 1)
    
    @staticmethod
    def multiply_strings(num1: str, num2: str) -> str:
        """
        Multiply two large numbers as strings using divide and conquer (Karatsuba).
        
        Args:
            num1: First number as string
            num2: Second number as string
            
        Returns:
            Product as string
        """
        # Simple implementation for demonstration
        n1 = int(num1)
        n2 = int(num2)
        return str(n1 * n2)


def main() -> None:
    """Demonstrate divide and conquer algorithms."""
    
    print("=== Divide and Conquer Demo ===")
    
    # Binary search
    print("\n--- Binary Search ---")
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    target = 5
    print(f"Array: {arr}, target: {target}")
    print(f"Index: {DivideConquer.binary_search(arr, target)}")
    
    # Leftmost/Rightmost
    print("\n--- Leftmost/Rightmost Binary Search ---")
    arr = [1, 2, 2, 2, 3, 4]
    target = 2
    print(f"Array: {arr}, target: {target}")
    print(f"Leftmost: {DivideConquer.binary_search_leftmost(arr, target)}")
    print(f"Rightmost: {DivideConquer.binary_search_rightmost(arr, target)}")
    
    # Rotated sorted search
    print("\n--- Search in Rotated Sorted ---")
    arr = [4, 5, 6, 7, 0, 1, 2]
    target = 0
    print(f"Array: {arr}, target: {target}")
    print(f"Index: {DivideConquer.search_rotated_sorted(arr, target)}")
    
    # Find min in rotated
    print("\n--- Find Min in Rotated ---")
    arr = [4, 5, 6, 7, 0, 1, 2]
    print(f"Array: {arr}")
    print(f"Min index: {DivideConquer.find_min_rotated(arr)}")
    
    # Peak element
    print("\n--- Find Peak Element ---")
    arr = [1, 2, 1, 3, 5, 6, 4]
    print(f"Array: {arr}")
    print(f"Peak index: {DivideConquer.find_peak_element(arr)}")
    
    # Kth largest
    print("\n--- Find Kth Largest ---")
    arr = [3, 2, 1, 5, 6, 4]
    k = 2
    print(f"Array: {arr}, k: {k}")
    print(f"Kth largest: {DivideConquer.find_kth_largest(arr, k)}")
    
    # Merge sort
    print("\n--- Merge Sort ---")
    arr = [5, 2, 8, 1, 9, 3]
    print(f"Original: {arr}")
    print(f"Sorted: {DivideConquer.merge_sort(arr)}")
    
    # Quick sort
    print("\n--- Quick Sort ---")
    arr = [5, 2, 8, 1, 9, 3]
    print(f"Original: {arr}")
    print(f"Sorted: {DivideConquer.quick_sort(arr)}")
    
    # Count inversions
    print("\n--- Count Inversions ---")
    arr = [2, 4, 1, 3, 5]
    print(f"Array: {arr}")
    print(f"Inversions: {DivideConquer.count_inversions(arr)}")
    
    # Maximum subarray
    print("\n--- Maximum Subarray ---")
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"Array: {arr}")
    max_sum, start, end = DivideConquer.maximum_subarray(arr)
    print(f"Max sum: {max_sum}, indices: [{start}:{end}]")
    
    # Power
    print("\n--- Power ---")
    print(f"2^10: {DivideConquer.power(2, 10)}")
    print(f"2^-3: {DivideConquer.power(2, -3):.4f}")


if __name__ == "__main__":
    main()
