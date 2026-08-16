"""
Binary Search - Efficient search algorithm for sorted arrays.
Features: Iterative and recursive implementations, with type hints and error handling.
"""

from typing import List, Optional, Callable, Any
import bisect


def binary_search_iterative(arr: List[int], target: int) -> Optional[int]:
    """
    Perform binary search iteratively to find target in sorted array.
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Args:
        arr: Sorted list of integers
        target: Integer to search for
        
    Returns:
        Index of target if found, None otherwise
        
    Examples:
        >>> binary_search_iterative([1, 3, 5, 7, 9], 5)
        2
        >>> binary_search_iterative([1, 3, 5, 7, 9], 4)
        None
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return None


def binary_search_recursive(arr: List[int], target: int, left: int = 0, right: Optional[int] = None) -> Optional[int]:
    """
    Perform binary search recursively to find target in sorted array.
    
    Time Complexity: O(log n)
    Space Complexity: O(log n) due to recursion stack
    
    Args:
        arr: Sorted list of integers
        target: Integer to search for
        left: Left boundary (default: 0)
        right: Right boundary (default: len(arr) - 1)
        
    Returns:
        Index of target if found, None otherwise
    """
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return None
    
    mid = left + (right - left) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def binary_search_first_occurrence(arr: List[int], target: int) -> Optional[int]:
    """
    Find the first occurrence of target in sorted array with duplicates.
    
    Args:
        arr: Sorted list of integers (may contain duplicates)
        target: Integer to search for
        
    Returns:
        Index of first occurrence if found, None otherwise
    """
    left, right = 0, len(arr) - 1
    result = None
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def binary_search_last_occurrence(arr: List[int], target: int) -> Optional[int]:
    """
    Find the last occurrence of target in sorted array with duplicates.
    
    Args:
        arr: Sorted list of integers (may contain duplicates)
        target: Integer to search for
        
    Returns:
        Index of last occurrence if found, None otherwise
    """
    left, right = 0, len(arr) - 1
    result = None
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            result = mid
            left = mid + 1  # Continue searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def binary_search_closest(arr: List[int], target: int) -> int:
    """
    Find the element closest to target in sorted array.
    
    Args:
        arr: Sorted list of integers
        target: Integer to find closest match for
        
    Returns:
        Index of the closest element
    """
    if not arr:
        raise ValueError("Array cannot be empty")
    
    # Use bisect to find insertion point
    pos = bisect.bisect_left(arr, target)
    
    # Handle edge cases
    if pos == 0:
        return 0
    if pos == len(arr):
        return len(arr) - 1
    
    # Compare distances
    if abs(arr[pos] - target) < abs(arr[pos - 1] - target):
        return pos
    else:
        return pos - 1


def binary_search_custom(arr: List[Any], target: Any, key: Callable[[Any], Any]) -> Optional[int]:
    """
    Binary search with custom key function for complex objects.
    
    Args:
        arr: Sorted list of objects
        target: Target value to search for
        key: Function to extract comparable value from objects
        
    Returns:
        Index of target if found, None otherwise
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        mid_value = key(arr[mid])
        target_value = key(target)
        
        if mid_value == target_value:
            return mid
        elif mid_value < target_value:
            left = mid + 1
        else:
            right = mid - 1
    
    return None


def main() -> None:
    """Demonstrate binary search implementations."""
    
    # Test data
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    arr_with_duplicates = [1, 2, 2, 2, 3, 4, 5]
    
    print("=== Binary Search - Iterative ===")
    targets = [5, 10, 1, 19]
    for target in targets:
        result = binary_search_iterative(arr, target)
        print(f"Search {target}: {'Found at index ' + str(result) if result is not None else 'Not found'}")
    
    print("\n=== Binary Search - Recursive ===")
    for target in targets:
        result = binary_search_recursive(arr, target)
        print(f"Search {target}: {'Found at index ' + str(result) if result is not None else 'Not found'}")
    
    print("\n=== First/Last Occurrence ===")
    print(f"Array with duplicates: {arr_with_duplicates}")
    print(f"First occurrence of 2: {binary_search_first_occurrence(arr_with_duplicates, 2)}")
    print(f"Last occurrence of 2: {binary_search_last_occurrence(arr_with_duplicates, 2)}")
    
    print("\n=== Closest Element ===")
    test_targets = [6, 10, 20, 0]
    for target in test_targets:
        idx = binary_search_closest(arr, target)
        print(f"Closest to {target}: {arr[idx]} (index {idx})")
    
    print("\n=== Custom Key Search ===")
    from dataclasses import dataclass
    
    @dataclass
    class Person:
        name: str
        age: int
    
    people = [
        Person("Alice", 25),
        Person("Bob", 30),
        Person("Charlie", 35),
        Person("David", 40),
    ]
    
    target_person = Person("", 35)
    idx = binary_search_custom(people, target_person, key=lambda p: p.age)
    print(f"Person with age 35: {people[idx].name if idx is not None else 'Not found'}")


if __name__ == "__main__":
    main()
