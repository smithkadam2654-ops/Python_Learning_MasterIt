"""
Recursion Algorithms - Classic recursive algorithms and problem solving.
Features: Divide and conquer, backtracking, and memoization examples.
"""

from typing import List, Optional, Set, Tuple
from functools import lru_cache


# ==================== BASIC RECURSION ====================

def factorial(n: int) -> int:
    """
    Calculate factorial recursively.
    
    Time Complexity: O(n)
    Space Complexity: O(n) due to call stack
    
    Args:
        n: Non-negative integer
        
    Returns:
        Factorial of n
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """
    Calculate nth Fibonacci number recursively.
    
    Time Complexity: O(2^n) - inefficient
    Space Complexity: O(n)
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """
    Calculate nth Fibonacci number with memoization.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def power(base: float, exponent: int) -> float:
    """
    Calculate base^exponent recursively.
    
    Time Complexity: O(log n) with optimization
    Space Complexity: O(log n)
    
    Args:
        base: Base number
        exponent: Non-negative integer
        
    Returns:
        base raised to exponent
    """
    if exponent == 0:
        return 1
    if exponent == 1:
        return base
    
    half = power(base, exponent // 2)
    
    if exponent % 2 == 0:
        return half * half
    else:
        return base * half * half


# ==================== DIVIDE AND CONQUER ====================

def binary_search_recursive(arr: List[int], target: int, left: int = 0, right: Optional[int] = None) -> Optional[int]:
    """
    Binary search using recursion.
    
    Time Complexity: O(log n)
    Space Complexity: O(log n)
    
    Args:
        arr: Sorted array
        target: Value to search for
        left: Left boundary
        right: Right boundary
        
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


def merge_sort(arr: List[int]) -> List[int]:
    """
    Merge sort using divide and conquer.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        arr: Array to sort
        
    Returns:
        Sorted array
    """
    if len(arr) <= 1:
        return arr.copy()
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left: List[int], right: List[int]) -> List[int]:
    """Merge two sorted arrays."""
    result = []
    i = j = 0
    
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


def quick_sort(arr: List[int]) -> List[int]:
    """
    Quick sort using divide and conquer.
    
    Time Complexity: O(n log n) average, O(n²) worst
    Space Complexity: O(log n) average
    
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
    
    return quick_sort(left) + middle + quick_sort(right)


# ==================== BACKTRACKING ====================

def generate_permutations(elements: List[str]) -> List[List[str]]:
    """
    Generate all permutations of elements using backtracking.
    
    Time Complexity: O(n!)
    Space Complexity: O(n!)
    
    Args:
        elements: List of elements to permute
        
    Returns:
        List of all permutations
    """
    result = []
    
    def backtrack(current: List[str], remaining: List[str]) -> None:
        if not remaining:
            result.append(current[:])
            return
        
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i + 1:])
            current.pop()
    
    backtrack([], elements)
    return result


def generate_combinations(elements: List[str], k: int) -> List[List[str]]:
    """
    Generate all combinations of k elements using backtracking.
    
    Time Complexity: O(C(n,k))
    Space Complexity: O(C(n,k))
    
    Args:
        elements: List of elements
        k: Size of combinations
        
    Returns:
        List of all combinations
    """
    result = []
    
    def backtrack(start: int, current: List[str]) -> None:
        if len(current) == k:
            result.append(current[:])
            return
        
        for i in range(start, len(elements)):
            current.append(elements[i])
            backtrack(i + 1, current)
            current.pop()
    
    backtrack(0, [])
    return result


def solve_n_queens(n: int) -> List[List[str]]:
    """
    Solve N-Queens problem using backtracking.
    
    Time Complexity: O(n!)
    Space Complexity: O(n²)
    
    Args:
        n: Board size (n x n)
        
    Returns:
        List of solutions (each solution is list of strings)
    """
    solutions = []
    
    def is_safe(board: List[List[str]], row: int, col: int) -> bool:
        # Check column
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        
        # Check upper left diagonal
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if board[i][j] == 'Q':
                return False
        
        # Check upper right diagonal
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, n)):
            if board[i][j] == 'Q':
                return False
        
        return True
    
    def backtrack(row: int, board: List[List[str]]) -> None:
        if row == n:
            solutions.append([''.join(row) for row in board])
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row][col] = 'Q'
                backtrack(row + 1, board)
                board[row][col] = '.'
    
    board = [['.' for _ in range(n)] for _ in range(n)]
    backtrack(0, board)
    
    return solutions


def generate_subsets(elements: List[str]) -> List[List[str]]:
    """
    Generate all subsets (power set) using backtracking.
    
    Time Complexity: O(2^n)
    Space Complexity: O(2^n)
    
    Args:
        elements: List of elements
        
    Returns:
        List of all subsets
    """
    result = []
    
    def backtrack(start: int, current: List[str]) -> None:
        result.append(current[:])
        
        for i in range(start, len(elements)):
            current.append(elements[i])
            backtrack(i + 1, current)
            current.pop()
    
    backtrack(0, [])
    return result


# ==================== RECURSIVE PROBLEM SOLVING ====================

def tower_of_hanoi(n: int, source: str, auxiliary: str, target: str) -> List[Tuple[str, str]]:
    """
    Solve Tower of Hanoi problem.
    
    Time Complexity: O(2^n)
    Space Complexity: O(n)
    
    Args:
        n: Number of disks
        source: Source peg name
        auxiliary: Auxiliary peg name
        target: Target peg name
        
    Returns:
        List of moves as (from_peg, to_peg) tuples
    """
    moves = []
    
    def solve(n: int, source: str, auxiliary: str, target: str) -> None:
        if n == 1:
            moves.append((source, target))
            return
        
        solve(n - 1, source, target, auxiliary)
        moves.append((source, target))
        solve(n - 1, auxiliary, source, target)
    
    solve(n, source, auxiliary, target)
    return moves


def generate_parentheses(n: int) -> List[str]:
    """
    Generate all valid combinations of n pairs of parentheses.
    
    Time Complexity: O(4^n / sqrt(n)) - Catalan number
    Space Complexity: O(4^n / sqrt(n))
    
    Args:
        n: Number of pairs
        
    Returns:
        List of valid combinations
    """
    result = []
    
    def backtrack(current: str, open_count: int, close_count: int) -> None:
        if len(current) == 2 * n:
            result.append(current)
            return
        
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result


def word_search(board: List[List[str]], word: str) -> bool:
    """
    Search for word in 2D board using backtracking.
    
    Time Complexity: O(m * n * 4^L) where L is word length
    Space Complexity: O(L)
    
    Args:
        board: 2D grid of characters
        word: Word to search for
        
    Returns:
        True if word exists, False otherwise
    """
    if not board or not word:
        return False
    
    rows, cols = len(board), len(board[0])
    
    def backtrack(row: int, col: int, index: int, visited: Set[Tuple[int, int]]) -> bool:
        if index == len(word):
            return True
        
        if (row < 0 or row >= rows or col < 0 or col >= cols or
            (row, col) in visited or board[row][col] != word[index]):
            return False
        
        visited.add((row, col))
        
        # Check all 4 directions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if backtrack(row + dr, col + dc, index + 1, visited):
                return True
        
        visited.remove((row, col))
        return False
    
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == word[0]:
                if backtrack(i, j, 0, set()):
                    return True
    
    return False


def main() -> None:
    """Demonstrate recursive algorithms."""
    
    print("=== Basic Recursion ===")
    print(f"factorial(5): {factorial(5)}")
    print(f"fibonacci(10): {fibonacci(10)}")
    print(f"fibonacci_memoized(10): {fibonacci_memoized(10)}")
    print(f"power(2, 10): {power(2, 10)}")
    
    print("\n=== Divide and Conquer ===")
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {arr}")
    print(f"Merge sort: {merge_sort(arr)}")
    print(f"Quick sort: {quick_sort(arr)}")
    print(f"Binary search for 25: {binary_search_recursive(merge_sort(arr), 25)}")
    
    print("\n=== Backtracking - Permutations ===")
    elements = ['A', 'B', 'C']
    perms = generate_permutations(elements)
    print(f"Permutations of {elements}: {perms}")
    
    print("\n=== Backtracking - Combinations ===")
    combos = generate_combinations(elements, 2)
    print(f"Combinations of {elements} (size 2): {combos}")
    
    print("\n=== Backtracking - Subsets ===")
    subsets = generate_subsets(elements)
    print(f"Subsets of {elements}: {subsets}")
    
    print("\n=== N-Queens ===")
    solutions = solve_n_queens(4)
    print(f"Number of solutions for 4-Queens: {len(solutions)}")
    for i, solution in enumerate(solutions[:2]):  # Show first 2 solutions
        print(f"Solution {i + 1}:")
        for row in solution:
            print(f"  {row}")
    
    print("\n=== Tower of Hanoi ===")
    moves = tower_of_hanoi(3, 'A', 'B', 'C')
    print(f"Moves for 3 disks: {moves}")
    print(f"Total moves: {len(moves)}")
    
    print("\n=== Generate Parentheses ===")
    parens = generate_parentheses(3)
    print(f"Valid parentheses for n=3: {parens}")
    
    print("\n=== Word Search ===")
    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    word = "ABCCED"
    print(f"Board:")
    for row in board:
        print(f"  {' '.join(row)}")
    print(f"Search '{word}': {word_search(board, word)}")
    print(f"Search 'SEE': {word_search(board, 'SEE')}")
    print(f"Search 'ABCB': {word_search(board, 'ABCB')}")


if __name__ == "__main__":
    main()
