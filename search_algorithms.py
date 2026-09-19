"""
Search Algorithms Module

This module provides comprehensive search algorithms including:
- Linear search variations
- Binary search and variants
- Interpolation search
- Exponential search
- Jump search
- Ternary search
- Fibonacci search
- Search in data structures
- String search algorithms
- Tree search algorithms
- Graph search utilities

All functions include comprehensive docstrings and type hints.
"""

from typing import Any, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
import bisect


class SearchStrategy(Enum):
    """Search strategy types."""
    LINEAR = "linear"
    BINARY = "binary"
    INTERPOLATION = "interpolation"
    EXPONENTIAL = "exponential"
    JUMP = "jump"
    TERNARY = "ternary"
    FIBONONACCI = "fibonacci"


@dataclass
class SearchResult:
    """Container for search results."""
    found: bool
    index: Optional[int]
    comparisons: int
    search_time: float
    strategy: SearchStrategy


class LinearSearch:
    """Linear search algorithms."""
    
    @staticmethod
    def search(arr: List[Any], target: Any) -> SearchResult:
        """Standard linear search."""
        import time
        start_time = time.time()
        comparisons = 0
        
        for i, item in enumerate(arr):
            comparisons += 1
            if item == target:
                return SearchResult(
                    found=True,
                    index=i,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.LINEAR
                )
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.LINEAR
        )
    
    @staticmethod
    def search_with_sentinel(arr: List[Any], target: Any) -> SearchResult:
        """Linear search with sentinel optimization."""
        import time
        start_time = time.time()
        comparisons = 0
        
        if not arr:
            return SearchResult(
                found=False,
                index=None,
                comparisons=0,
                search_time=time.time() - start_time,
                strategy=SearchStrategy.LINEAR
            )
        
        # Store last element and replace with target
        last = arr[-1]
        arr[-1] = target
        
        i = 0
        while arr[i] != target:
            comparisons += 1
            i += 1
        
        # Restore last element
        arr[-1] = last
        
        if i < len(arr) - 1 or last == target:
            return SearchResult(
                found=True,
                index=i,
                comparisons=comparisons,
                search_time=time.time() - start_time,
                strategy=SearchStrategy.LINEAR
            )
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.LINEAR
        )
    
    @staticmethod
    def search_all(arr: List[Any], target: Any) -> List[int]:
        """Find all occurrences of target."""
        indices = []
        for i, item in enumerate(arr):
            if item == target:
                indices.append(i)
        return indices


class BinarySearch:
    """Binary search algorithms."""
    
    @staticmethod
    def search(arr: List[Any], target: Any) -> SearchResult:
        """Standard binary search (requires sorted array)."""
        import time
        start_time = time.time()
        comparisons = 0
        
        left, right = 0, len(arr) - 1
        
        while left <= right:
            comparisons += 1
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return SearchResult(
                    found=True,
                    index=mid,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.BINARY
                )
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.BINARY
        )
    
    @staticmethod
    def search_first_occurrence(arr: List[Any], target: Any) -> SearchResult:
        """Binary search for first occurrence of target."""
        import time
        start_time = time.time()
        comparisons = 0
        
        left, right = 0, len(arr) - 1
        result = -1
        
        while left <= right:
            comparisons += 1
            mid = (left + right) // 2
            
            if arr[mid] == target:
                result = mid
                right = mid - 1  # Continue searching left
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return SearchResult(
            found=result != -1,
            index=result if result != -1 else None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.BINARY
        )
    
    @staticmethod
    def search_last_occurrence(arr: List[Any], target: Any) -> SearchResult:
        """Binary search for last occurrence of target."""
        import time
        start_time = time.time()
        comparisons = 0
        
        left, right = 0, len(arr) - 1
        result = -1
        
        while left <= right:
            comparisons += 1
            mid = (left + right) // 2
            
            if arr[mid] == target:
                result = mid
                left = mid + 1  # Continue searching right
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return SearchResult(
            found=result != -1,
            index=result if result != -1 else None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.BINARY
        )
    
    @staticmethod
    def search_range(arr: List[Any], target: Any) -> Tuple[int, int]:
        """Find range of target occurrences (first and last index)."""
        first = BinarySearch.search_first_occurrence(arr, target)
        last = BinarySearch.search_last_occurrence(arr, target)
        
        if first.found and last.found:
            return first.index, last.index
        return -1, -1
    
    @staticmethod
    def search_rotated(arr: List[Any], target: Any) -> SearchResult:
        """Binary search in rotated sorted array."""
        import time
        start_time = time.time()
        comparisons = 0
        
        if not arr:
            return SearchResult(
                found=False,
                index=None,
                comparisons=0,
                search_time=time.time() - start_time,
                strategy=SearchStrategy.BINARY
            )
        
        left, right = 0, len(arr) - 1
        
        while left <= right:
            comparisons += 1
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return SearchResult(
                    found=True,
                    index=mid,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.BINARY
                )
            
            # Check if left half is sorted
            if arr[left] <= arr[mid]:
                if arr[left] <= target < arr[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if arr[mid] < target <= arr[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.BINARY
        )


class InterpolationSearch:
    """Interpolation search algorithm."""
    
    @staticmethod
    def search(arr: List[Any], target: Any) -> SearchResult:
        """Interpolation search (requires sorted numeric array)."""
        import time
        start_time = time.time()
        comparisons = 0
        
        if not arr:
            return SearchResult(
                found=False,
                index=None,
                comparisons=0,
                search_time=time.time() - start_time,
                strategy=SearchStrategy.INTERPOLATION
            )
        
        left, right = 0, len(arr) - 1
        
        while left <= right and target >= arr[left] and target <= arr[right]:
            comparisons += 1
            
            # Calculate position using interpolation formula
            if arr[right] == arr[left]:
                pos = left
            else:
                pos = left + ((target - arr[left]) * (right - left)) // (arr[right] - arr[left])
            
            if arr[pos] == target:
                return SearchResult(
                    found=True,
                    index=pos,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.INTERPOLATION
                )
            
            if arr[pos] < target:
                left = pos + 1
            else:
                right = pos - 1
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.INTERPOLATION
        )


class ExponentialSearch:
    """Exponential search algorithm."""
    
    @staticmethod
    def search(arr: List[Any], target: Any) -> SearchResult:
        """Exponential search (requires sorted array)."""
        import time
        start_time = time.time()
        comparisons = 0
        
        if not arr or arr[0] == target:
            if arr and arr[0] == target:
                return SearchResult(
                    found=True,
                    index=0,
                    comparisons=1,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.EXPONENTIAL
                )
            return SearchResult(
                found=False,
                index=None,
                comparisons=0,
                search_time=time.time() - start_time,
                strategy=SearchStrategy.EXPONENTIAL
            )
        
        # Find range where target might be
        index = 1
        while index < len(arr) and arr[index] <= target:
            comparisons += 1
            index *= 2
        
        # Perform binary search in the found range
        left = index // 2
        right = min(index, len(arr) - 1)
        
        while left <= right:
            comparisons += 1
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return SearchResult(
                    found=True,
                    index=mid,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.EXPONENTIAL
                )
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.EXPONENTIAL
        )


class JumpSearch:
    """Jump search algorithm."""
    
    @staticmethod
    def search(arr: List[Any], target: Any, jump_size: Optional[int] = None) -> SearchResult:
        """Jump search (requires sorted array)."""
        import time
        start_time = time.time()
        comparisons = 0
        
        if not arr:
            return SearchResult(
                found=False,
                index=None,
                comparisons=0,
                search_time=time.time() - start_time,
                strategy=SearchStrategy.JUMP
            )
        
        n = len(arr)
        step = jump_size if jump_size else int(math.sqrt(n))
        prev = 0
        
        # Find block where target might be
        while arr[min(step, n) - 1] < target:
            comparisons += 1
            prev = step
            step += int(math.sqrt(n))
            
            if prev >= n:
                return SearchResult(
                    found=False,
                    index=None,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.JUMP
                )
        
        # Linear search in the found block
        while arr[prev] < target:
            comparisons += 1
            prev += 1
            
            if prev == min(step, n):
                return SearchResult(
                    found=False,
                    index=None,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.JUMP
                )
        
        comparisons += 1
        if arr[prev] == target:
            return SearchResult(
                found=True,
                index=prev,
                comparisons=comparisons,
                search_time=time.time() - start_time,
                strategy=SearchStrategy.JUMP
            )
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.JUMP
        )


class TernarySearch:
    """Ternary search algorithm."""
    
    @staticmethod
    def search(arr: List[Any], target: Any) -> SearchResult:
        """Ternary search (requires sorted array)."""
        import time
        start_time = time.time()
        comparisons = 0
        
        if not arr:
            return SearchResult(
                found=False,
                index=None,
                comparisons=0,
                search_time=time.time() - start_time,
                strategy=SearchStrategy.TERNARY
            )
        
        left, right = 0, len(arr) - 1
        
        while left <= right:
            comparisons += 1
            
            partition_size = (right - left) // 3
            mid1 = left + partition_size
            mid2 = right - partition_size
            
            if arr[mid1] == target:
                return SearchResult(
                    found=True,
                    index=mid1,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.TERNARY
                )
            
            if arr[mid2] == target:
                return SearchResult(
                    found=True,
                    index=mid2,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.TERNARY
                )
            
            if target < arr[mid1]:
                right = mid1 - 1
            elif target > arr[mid2]:
                left = mid2 + 1
            else:
                left = mid1 + 1
                right = mid2 - 1
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.TERNARY
        )
    
    @staticmethod
    def find_maximum(f: Callable[[float], float], left: float, right: float, 
                     epsilon: float = 1e-6) -> float:
        """Find maximum of unimodal function using ternary search."""
        while right - left > epsilon:
            mid1 = left + (right - left) / 3
            mid2 = right - (right - left) / 3
            
            if f(mid1) < f(mid2):
                left = mid1
            else:
                right = mid2
        
        return (left + right) / 2


class FibonacciSearch:
    """Fibonacci search algorithm."""
    
    @staticmethod
    def search(arr: List[Any], target: Any) -> SearchResult:
        """Fibonacci search (requires sorted array)."""
        import time
        start_time = time.time()
        comparisons = 0
        
        if not arr:
            return SearchResult(
                found=False,
                index=None,
                comparisons=0,
                search_time=time.time() - start_time,
                strategy=SearchStrategy.FIBONONACCI
            )
        
        n = len(arr)
        
        # Initialize fibonacci numbers
        fib2 = 1  # F(k-2)
        fib1 = 1  # F(k-1)
        fib = fib2 + fib1  # F(k)
        
        # Find smallest fibonacci number >= n
        while fib < n:
            fib2 = fib1
            fib1 = fib
            fib = fib2 + fib1
        
        offset = -1
        
        while fib > 1:
            comparisons += 1
            i = min(offset + fib2, n - 1)
            
            if arr[i] < target:
                fib = fib1
                fib1 = fib2
                fib2 = fib - fib1
                offset = i
            elif arr[i] > target:
                fib = fib2
                fib1 = fib1 - fib2
                fib2 = fib - fib1
            else:
                return SearchResult(
                    found=True,
                    index=i,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.FIBONONACCI
                )
        
        # Check last element
        comparisons += 1
        if fib1 and offset + 1 < n and arr[offset + 1] == target:
            return SearchResult(
                found=True,
                index=offset + 1,
                comparisons=comparisons,
                search_time=time.time() - start_time,
                strategy=SearchStrategy.FIBONONACCI
            )
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.FIBONONACCI
        )


class StringSearch:
    """String search algorithms."""
    
    @staticmethod
    def naive_search(text: str, pattern: str) -> List[int]:
        """Naive string matching algorithm."""
        n = len(text)
        m = len(pattern)
        occurrences = []
        
        for i in range(n - m + 1):
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            
            if match:
                occurrences.append(i)
        
        return occurrences
    
    @staticmethod
    def rabin_karp(text: str, pattern: str, base: int = 256, prime: int = 101) -> List[int]:
        """Rabin-Karp string matching algorithm."""
        n = len(text)
        m = len(pattern)
        occurrences = []
        
        if m > n:
            return occurrences
        
        # Calculate hash for pattern and first window
        pattern_hash = 0
        text_hash = 0
        h = 1  # base^(m-1) % prime
        
        for i in range(m):
            pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
            text_hash = (base * text_hash + ord(text[i])) % prime
            if i < m - 1:
                h = (h * base) % prime
        
        # Slide the pattern over text
        for i in range(n - m + 1):
            if pattern_hash == text_hash:
                # Check for actual match
                match = True
                for j in range(m):
                    if text[i + j] != pattern[j]:
                        match = False
                        break
                
                if match:
                    occurrences.append(i)
            
            # Calculate hash for next window
            if i < n - m:
                text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
                if text_hash < 0:
                    text_hash += prime
        
        return occurrences
    
    @staticmethod
    def kmp_search(text: str, pattern: str) -> List[int]:
        """Knuth-Morris-Pratt string matching algorithm."""
        n = len(text)
        m = len(pattern)
        occurrences = []
        
        if m == 0:
            return occurrences
        
        # Build lps array (longest proper prefix which is also suffix)
        lps = [0] * m
        length = 0  # length of the previous longest prefix suffix
        i = 1
        
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        
        # Search using lps array
        i = 0  # index for text
        j = 0  # index for pattern
        
        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m:
                occurrences.append(i - j)
                j = lps[j - 1]
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
        return occurrences


class TreeSearch:
    """Tree search algorithms."""
    
    @staticmethod
    def binary_tree_search(root: Optional[dict], target: Any) -> Optional[dict]:
        """Search in binary search tree."""
        if root is None:
            return None
        
        if root['value'] == target:
            return root
        elif target < root['value']:
            return TreeSearch.binary_tree_search(root.get('left'), target)
        else:
            return TreeSearch.binary_tree_search(root.get('right'), target)
    
    @staticmethod
    def binary_tree_insert(root: Optional[dict], value: Any) -> dict:
        """Insert value into binary search tree."""
        if root is None:
            return {'value': value, 'left': None, 'right': None}
        
        if value < root['value']:
            root['left'] = TreeSearch.binary_tree_insert(root.get('left'), value)
        else:
            root['right'] = TreeSearch.binary_tree_insert(root.get('right'), value)
        
        return root
    
    @staticmethod
    def bst_inorder_traversal(root: Optional[dict]) -> List[Any]:
        """In-order traversal of BST (sorted order)."""
        result = []
        
        def traverse(node):
            if node is None:
                return
            
            traverse(node.get('left'))
            result.append(node['value'])
            traverse(node.get('right'))
        
        traverse(root)
        return result


class AdvancedSearch:
    """Advanced search utilities."""
    
    @staticmethod
    def binary_search_with_comparator(arr: List[Any], target: Any,
                                     comparator: Callable[[Any, Any], int]) -> SearchResult:
        """Binary search with custom comparator function."""
        import time
        start_time = time.time()
        comparisons = 0
        
        left, right = 0, len(arr) - 1
        
        while left <= right:
            comparisons += 1
            mid = (left + right) // 2
            
            cmp_result = comparator(arr[mid], target)
            
            if cmp_result == 0:
                return SearchResult(
                    found=True,
                    index=mid,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.BINARY
                )
            elif cmp_result < 0:
                left = mid + 1
            else:
                right = mid - 1
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.BINARY
        )
    
    @staticmethod
    def search_with_key(data: List[Dict], key: str, target: Any) -> SearchResult:
        """Search in list of dictionaries by key."""
        import time
        start_time = time.time()
        comparisons = 0
        
        for i, item in enumerate(data):
            comparisons += 1
            if item.get(key) == target:
                return SearchResult(
                    found=True,
                    index=i,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.LINEAR
                )
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.LINEAR
        )
    
    @staticmethod
    def search_sorted_with_key(data: List[Dict], key: str, target: Any) -> SearchResult:
        """Binary search in sorted list of dictionaries by key."""
        import time
        start_time = time.time()
        comparisons = 0
        
        left, right = 0, len(data) - 1
        
        while left <= right:
            comparisons += 1
            mid = (left + right) // 2
            
            if data[mid].get(key) == target:
                return SearchResult(
                    found=True,
                    index=mid,
                    comparisons=comparisons,
                    search_time=time.time() - start_time,
                    strategy=SearchStrategy.BINARY
                )
            elif data[mid].get(key) < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            search_time=time.time() - start_time,
            strategy=SearchStrategy.BINARY
        )
    
    @staticmethod
    def find_closest(arr: List[Any], target: Any) -> Tuple[int, Any]:
        """Find closest element to target."""
        if not arr:
            return -1, None
        
        closest_index = 0
        closest_diff = abs(arr[0] - target) if isinstance(arr[0], (int, float)) else 0
        
        for i, item in enumerate(arr[1:], 1):
            if isinstance(item, (int, float)):
                diff = abs(item - target)
                if diff < closest_diff:
                    closest_diff = diff
                    closest_index = i
        
        return closest_index, arr[closest_index]
    
    @staticmethod
    def find_k_closest(arr: List[Any], target: Any, k: int) -> List[Any]:
        """Find k closest elements to target."""
        if not arr or k <= 0:
            return []
        
        k = min(k, len(arr))
        
        # Find k closest using quickselect-like approach
        def partition(left, right):
            pivot = arr[right]
            i = left
            
            for j in range(left, right):
                if abs(arr[j] - target) < abs(pivot - target):
                    arr[i], arr[j] = arr[j], arr[i]
                    i += 1
            
            arr[i], arr[right] = arr[right], arr[i]
            return i
        
        def quickselect(left, right, k_smallest):
            if left == right:
                return
            
            pivot_index = partition(left, right)
            
            if k_smallest == pivot_index:
                return
            elif k_smallest < pivot_index:
                quickselect(left, pivot_index - 1, k_smallest)
            else:
                quickselect(pivot_index + 1, right, k_smallest)
        
        quickselect(0, len(arr) - 1, k)
        return arr[:k]


class SearchBenchmark:
    """Search algorithm benchmarking utilities."""
    
    @staticmethod
    def benchmark_algorithms(arr: List[Any], target: Any,
                           strategies: List[SearchStrategy] = None) -> Dict[str, SearchResult]:
        """Benchmark multiple search algorithms."""
        if strategies is None:
            strategies = [SearchStrategy.LINEAR, SearchStrategy.BINARY, SearchStrategy.JUMP]
        
        results = {}
        
        for strategy in strategies:
            if strategy == SearchStrategy.LINEAR:
                results["linear"] = LinearSearch.search(arr, target)
            elif strategy == SearchStrategy.BINARY:
                results["binary"] = BinarySearch.search(arr, target)
            elif strategy == SearchStrategy.INTERPOLATION:
                results["interpolation"] = InterpolationSearch.search(arr, target)
            elif strategy == SearchStrategy.EXPONENTIAL:
                results["exponential"] = ExponentialSearch.search(arr, target)
            elif strategy == SearchStrategy.JUMP:
                results["jump"] = JumpSearch.search(arr, target)
            elif strategy == SearchStrategy.TERNARY:
                results["ternary"] = TernarySearch.search(arr, target)
            elif strategy == SearchStrategy.FIBONONACCI:
                results["fibonacci"] = FibonacciSearch.search(arr, target)
        
        return results
    
    @staticmethod
    def compare_results(results: Dict[str, SearchResult]) -> Dict[str, Any]:
        """Compare benchmark results."""
        comparison = {
            "fastest": None,
            "slowest": None,
            "fewest_comparisons": None,
            "most_comparisons": None
        }
        
        if not results:
            return comparison
        
        # Find fastest
        fastest = min(results.items(), key=lambda x: x[1].search_time)
        comparison["fastest"] = fastest[0]
        
        # Find slowest
        slowest = max(results.items(), key=lambda x: x[1].search_time)
        comparison["slowest"] = slowest[0]
        
        # Find fewest comparisons
        fewest = min(results.items(), key=lambda x: x[1].comparisons)
        comparison["fewest_comparisons"] = fewest[0]
        
        # Find most comparisons
        most = max(results.items(), key=lambda x: x[1].comparisons)
        comparison["most_comparisons"] = most[0]
        
        return comparison


def demonstrate_search_algorithms():
    """Demonstrate search algorithms functionality."""
    print("=== Search Algorithms Demonstration ===\n")
    
    # Linear Search
    print("1. Linear Search:")
    arr = [5, 3, 8, 1, 9, 2, 7, 4, 6]
    target = 7
    
    linear_result = LinearSearch.search(arr, target)
    print(f"   Linear search for {target}: found={linear_result.found}, index={linear_result.index}")
    print(f"   Comparisons: {linear_result.comparisons}, Time: {linear_result.search_time:.6f}s")
    
    # Binary Search
    print("\n2. Binary Search:")
    sorted_arr = sorted(arr)
    print(f"   Sorted array: {sorted_arr}")
    
    binary_result = BinarySearch.search(sorted_arr, target)
    print(f"   Binary search for {target}: found={binary_result.found}, index={binary_result.index}")
    print(f"   Comparisons: {binary_result.comparisons}, Time: {binary_result.search_time:.6f}s")
    
    # Binary Search Variants
    print("\n3. Binary Search Variants:")
    arr_with_duplicates = [1, 2, 2, 2, 3, 4, 4, 5]
    
    first = BinarySearch.search_first_occurrence(arr_with_duplicates, 2)
    last = BinarySearch.search_last_occurrence(arr_with_duplicates, 2)
    print(f"   First occurrence of 2: index {first.index}")
    print(f"   Last occurrence of 2: index {last.index}")
    
    # Interpolation Search
    print("\n4. Interpolation Search:")
    numeric_arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    
    interp_result = InterpolationSearch.search(numeric_arr, 13)
    print(f"   Interpolation search for 13: found={interp_result.found}, index={interp_result.index}")
    print(f"   Comparisons: {interp_result.comparisons}")
    
    # Exponential Search
    print("\n5. Exponential Search:")
    exp_result = ExponentialSearch.search(numeric_arr, 13)
    print(f"   Exponential search for 13: found={exp_result.found}, index={exp_result.index}")
    print(f"   Comparisons: {exp_result.comparisons}")
    
    # Jump Search
    print("\n6. Jump Search:")
    jump_result = JumpSearch.search(numeric_arr, 13)
    print(f"   Jump search for 13: found={jump_result.found}, index={jump_result.index}")
    print(f"   Comparisons: {jump_result.comparisons}")
    
    # Ternary Search
    print("\n7. Ternary Search:")
    ternary_result = TernarySearch.search(numeric_arr, 13)
    print(f"   Ternary search for 13: found={ternary_result.found}, index={ternary_result.index}")
    print(f"   Comparisons: {ternary_result.comparisons}")
    
    # Fibonacci Search
    print("\n8. Fibonacci Search:")
    fib_result = FibonacciSearch.search(numeric_arr, 13)
    print(f"   Fibonacci search for 13: found={fib_result.found}, index={fib_result.index}")
    print(f"   Comparisons: {fib_result.comparisons}")
    
    # String Search
    print("\n9. String Search:")
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    
    naive = StringSearch.naive_search(text, pattern)
    print(f"   Naive search occurrences: {naive}")
    
    rabin_karp = StringSearch.rabin_karp(text, pattern)
    print(f"   Rabin-Karp occurrences: {rabin_karp}")
    
    kmp = StringSearch.kmp_search(text, pattern)
    print(f"   KMP occurrences: {kmp}")
    
    # Tree Search
    print("\n10. Tree Search:")
    bst_root = None
    values = [5, 3, 7, 2, 4, 6, 8]
    
    for value in values:
        bst_root = TreeSearch.binary_tree_insert(bst_root, value)
    
    found = TreeSearch.binary_tree_search(bst_root, 6)
    print(f"   BST search for 6: found={found is not None}")
    
    inorder = TreeSearch.bst_inorder_traversal(bst_root)
    print(f"   In-order traversal: {inorder}")
    
    # Advanced Search
    print("\n11. Advanced Search:")
    dict_data = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
        {"name": "Charlie", "age": 35}
    ]
    
    dict_result = AdvancedSearch.search_with_key(dict_data, "name", "Bob")
    print(f"   Search dict by key: found={dict_result.found}, index={dict_result.index}")
    
    closest = AdvancedSearch.find_closest([1, 3, 5, 7, 9], 6)
    print(f"   Closest to 6: index {closest[0]}, value {closest[1]}")
    
    k_closest = AdvancedSearch.find_k_closest([1, 3, 5, 7, 9, 11, 13], 6, 3)
    print(f"   3 closest to 6: {k_closest}")
    
    # Benchmark
    print("\n12. Benchmark Comparison:")
    large_array = list(range(10000))
    target_value = 5000
    
    benchmark_results = SearchBenchmark.benchmark_algorithms(large_array, target_value)
    comparison = SearchBenchmark.compare_results(benchmark_results)
    
    print(f"   Fastest: {comparison['fastest']}")
    print(f"   Slowest: {comparison['slowest']}")
    print(f"   Fewest comparisons: {comparison['fewest_comparisons']}")
    print(f"   Most comparisons: {comparison['most_comparisons']}")
    
    # Rotated Array Search
    print("\n13. Rotated Array Search:")
    rotated = [4, 5, 6, 7, 0, 1, 2, 3]
    rotated_result = BinarySearch.search_rotated(rotated, 5)
    print(f"   Search in rotated array: found={rotated_result.found}, index={rotated_result.index}")
    
    print("\n=== Demonstration Complete ===")
    print("\nSearch Algorithm Best Practices:")
    print("- Use binary search for sorted arrays (O(log n))")
    print("- Use linear search for unsorted data (O(n))")
    print("- Interpolation search is best for uniformly distributed data")
    print("- Exponential search is good for unbounded/infinite arrays")
    print("- Jump search works well on sorted arrays with jump = sqrt(n)")
    print("- Ternary search is useful for finding maxima/minima in unimodal functions")
    print("- KMP is efficient for pattern matching in strings")
    print("- Rabin-Karp is good for multiple pattern searches")
    print("- Consider time vs. space trade-offs")
    print("- Preprocessing (sorting) can improve search performance")


if __name__ == "__main__":
    import math
    demonstrate_search_algorithms()