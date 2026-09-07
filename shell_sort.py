"""
Shell Sort - Improved insertion sort with gap sequence.
Features: In-place sorting, adaptive performance, and multiple gap sequences.
"""

from typing import List, TypeVar, Generic

T = TypeVar('T')


class ShellSort:
    """Shell sort implementation."""
    
    @staticmethod
    def sort(arr: List[T]) -> List[T]:
        """
        Sort array using Shell sort with Shell's original gap sequence.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        n = len(result)
        
        # Start with gap = n/2, reduce by half
        gap = n // 2
        
        while gap > 0:
            # Do gapped insertion sort
            for i in range(gap, n):
                temp = result[i]
                j = i
                
                while j >= gap and result[j - gap] > temp:
                    result[j] = result[j - gap]
                    j -= gap
                
                result[j] = temp
            
            gap //= 2
        
        return result
    
    @staticmethod
    def sort_knuth(arr: List[T]) -> List[T]:
        """
        Sort using Knuth's gap sequence (1, 4, 13, 40, 121, ...).
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        n = len(result)
        
        # Calculate initial gap using Knuth's sequence
        gap = 1
        while gap < n // 3:
            gap = 3 * gap + 1  # 1, 4, 13, 40, 121, ...
        
        while gap > 0:
            for i in range(gap, n):
                temp = result[i]
                j = i
                
                while j >= gap and result[j - gap] > temp:
                    result[j] = result[j - gap]
                    j -= gap
                
                result[j] = temp
            
            gap //= 3
        
        return result
    
    @staticmethod
    def sort_sedgewick(arr: List[T]) -> List[T]:
        """
        Sort using Sedgewick's gap sequence.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        n = len(result)
        
        # Generate Sedgewick gaps
        gaps = []
        k = 0
        while True:
            if k % 2 == 0:
                gap = 9 * (2 ** k) - 9 * (2 ** (k // 2)) + 1
            else:
                gap = 8 * (2 ** k) - 6 * (2 ** ((k + 1) // 2)) + 1
            
            if gap > n:
                break
            
            gaps.append(gap)
            k += 1
        
        # Sort in reverse order of gaps
        for gap in reversed(gaps):
            for i in range(gap, n):
                temp = result[i]
                j = i
                
                while j >= gap and result[j - gap] > temp:
                    result[j] = result[j - gap]
                    j -= gap
                
                result[j] = temp
        
        return result
    
    @staticmethod
    def sort_ciura(arr: List[T]) -> List[T]:
        """
        Sort using Ciura's empirically determined gap sequence.
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        n = len(result)
        
        # Ciura's gap sequence (empirically best known)
        ciura_gaps = [701, 301, 132, 57, 23, 10, 4, 1]
        
        # Filter gaps smaller than array size
        gaps = [gap for gap in ciura_gaps if gap < n]
        
        for gap in gaps:
            for i in range(gap, n):
                temp = result[i]
                j = i
                
                while j >= gap and result[j - gap] > temp:
                    result[j] = result[j - gap]
                    j -= gap
                
                result[j] = temp
        
        return result
    
    @staticmethod
    def sort_custom_gap(arr: List[T], gap_sequence: List[int]) -> List[T]:
        """
        Sort using custom gap sequence.
        
        Args:
            arr: Array to sort
            gap_sequence: Custom gap sequence
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        n = len(result)
        
        # Filter and sort gaps
        gaps = [gap for gap in gap_sequence if gap < n]
        gaps.sort(reverse=True)
        
        for gap in gaps:
            for i in range(gap, n):
                temp = result[i]
                j = i
                
                while j >= gap and result[j - gap] > temp:
                    result[j] = result[j - gap]
                    j -= gap
                
                result[j] = temp
        
        return result


class HibbardShellSort(ShellSort):
    """Shell sort with Hibbard's gap sequence."""
    
    @staticmethod
    def sort(arr: List[T]) -> List[T]:
        """
        Sort using Hibbard's gap sequence (2^k - 1).
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        if len(arr) <= 1:
            return arr.copy()
        
        result = arr.copy()
        n = len(result)
        
        # Generate Hibbard gaps: 1, 3, 7, 15, 31, ... (2^k - 1)
        gaps = []
        k = 1
        while (2 ** k) - 1 < n:
            gaps.append((2 ** k) - 1)
            k += 1
        
        for gap in reversed(gaps):
            for i in range(gap, n):
                temp = result[i]
                j = i
                
                while j >= gap and result[j - gap] > temp:
                    result[j] = result[j - gap]
                    j -= gap
                
                result[j] = temp
        
        return result


def main() -> None:
    """Demonstrate Shell sort."""
    
    print("=== Shell Sort Demo ===")
    
    # Basic sorting
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {numbers}")
    
    sorted_numbers = ShellSort.sort(numbers)
    print(f"Sorted (Shell's gaps): {sorted_numbers}")
    
    # Knuth's sequence
    print("\n--- Knuth's Gap Sequence ---")
    knuth_sorted = ShellSort.sort_knuth(numbers)
    print(f"Sorted (Knuth's gaps): {knuth_sorted}")
    
    # Sedgewick's sequence
    print("\n--- Sedgewick's Gap Sequence ---")
    sedgewick_sorted = ShellSort.sort_sedgewick(numbers)
    print(f"Sorted (Sedgewick's gaps): {sedgewick_sorted}")
    
    # Ciura's sequence
    print("\n--- Ciura's Gap Sequence ---")
    ciura_sorted = ShellSort.sort_ciura(numbers)
    print(f"Sorted (Ciura's gaps): {ciura_sorted}")
    
    # Hibbard's sequence
    print("\n--- Hibbard's Gap Sequence ---")
    hibbard_sorted = HibbardShellSort.sort(numbers)
    print(f"Sorted (Hibbard's gaps): {hibbard_sorted}")
    
    # Custom gap sequence
    print("\n--- Custom Gap Sequence ---")
    custom_gaps = [5, 3, 1]
    custom_sorted = ShellSort.sort_custom_gap(numbers, custom_gaps)
    print(f"Sorted (custom gaps {custom_gaps}): {custom_sorted}")
    
    # String sorting
    print("\n--- String Sorting ---")
    words = ["banana", "apple", "cherry", "date"]
    print(f"Original: {words}")
    
    sorted_words = ShellSort.sort(words)
    print(f"Sorted: {sorted_words}")
    
    # Performance comparison
    print("\n=== Performance Comparison ===")
    import time
    import random
    
    n = 100000
    large_array = [random.randint(0, 1000000) for _ in range(n)]
    
    # Shell's original
    start = time.time()
    ShellSort.sort(large_array.copy())
    shell_time = (time.time() - start) * 1000
    
    # Knuth's
    start = time.time()
    ShellSort.sort_knuth(large_array.copy())
    knuth_time = (time.time() - start) * 1000
    
    # Sedgewick's
    start = time.time()
    ShellSort.sort_sedgewick(large_array.copy())
    sedgewick_time = (time.time() - start) * 1000
    
    # Ciura's
    start = time.time()
    ShellSort.sort_ciura(large_array.copy())
    ciura_time = (time.time() - start) * 1000
    
    # Hibbard's
    start = time.time()
    HibbardShellSort.sort(large_array.copy())
    hibbard_time = (time.time() - start) * 1000
    
    # Python sort
    start = time.time()
    sorted(large_array)
    python_time = (time.time() - start) * 1000
    
    print(f"Shell's original: {shell_time:.2f}ms")
    print(f"Knuth's: {knuth_time:.2f}ms")
    print(f"Sedgewick's: {sedgewick_time:.2f}ms")
    print(f"Ciura's: {ciura_time:.2f}ms")
    print(f"Hibbard's: {hibbard_time:.2f}ms")
    print(f"Python sort: {python_time:.2f}ms")
    
    # Best gap sequence
    best = min([("Shell", shell_time), ("Knuth", knuth_time), 
                ("Sedgewick", sedgewick_time), ("Ciura", ciura_time),
                ("Hibbard", hibbard_time)], key=lambda x: x[1])
    print(f"\nBest sequence: {best[0]} ({best[1]:.2f}ms)")
    
    # Already sorted (best case)
    print("\n--- Already Sorted ---")
    sorted_array = list(range(n))
    
    start = time.time()
    ShellSort.sort(sorted_array.copy())
    sorted_case_time = (time.time() - start) * 1000
    
    start = time.time()
    ShellSort.sort(large_array.copy())
    random_case_time = (time.time() - start) * 1000
    
    print(f"Already sorted: {sorted_case_time:.2f}ms")
    print(f"Random order: {random_case_time:.2f}ms")
    print(f"Ratio: {sorted_case_time/random_case_time:.2f}x")
    
    # Reverse sorted (worst case)
    print("\n--- Reverse Sorted ---")
    reverse_array = list(range(n, 0, -1))
    
    start = time.time()
    ShellSort.sort(reverse_array.copy())
    reverse_case_time = (time.time() - start) * 1000
    
    print(f"Reverse sorted: {reverse_case_time:.2f}ms")
    print(f"Random order: {random_case_time:.2f}ms")
    print(f"Ratio: {reverse_case_time/random_case_time:.2f}x")


if __name__ == "__main__":
    main()
