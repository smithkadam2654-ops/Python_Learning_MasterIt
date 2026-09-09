"""
Backtracking Algorithms - Recursive problem-solving with pruning.
Features: N-Queens, Sudoku, subsets, permutations, and combination problems.
"""

from typing import List, Optional


class Backtracking:
    """Backtracking algorithm implementations."""
    
    @staticmethod
    def generate_subsets(nums: List[int]) -> List[List[int]]:
        """
        Generate all subsets (power set).
        
        Args:
            nums: List of numbers
            
        Returns:
            List of all subsets
        """
        result = []
        
        def backtrack(start: int, current: List[int]) -> None:
            result.append(current.copy())
            
            for i in range(start, len(nums)):
                current.append(nums[i])
                backtrack(i + 1, current)
                current.pop()
        
        backtrack(0, [])
        return result
    
    @staticmethod
    def generate_permutations(nums: List[int]) -> List[List[int]]:
        """
        Generate all permutations.
        
        Args:
            nums: List of numbers
            
        Returns:
            List of all permutations
        """
        result = []
        used = [False] * len(nums)
        
        def backtrack(current: List[int]) -> None:
            if len(current) == len(nums):
                result.append(current.copy())
                return
            
            for i in range(len(nums)):
                if not used[i]:
                    used[i] = True
                    current.append(nums[i])
                    backtrack(current)
                    current.pop()
                    used[i] = False
        
        backtrack([])
        return result
    
    @staticmethod
    def generate_combinations(n: int, k: int) -> List[List[int]]:
        """
        Generate all combinations of k numbers from 1 to n.
        
        Args:
            n: Upper bound
            k: Size of combinations
            
        Returns:
            List of all combinations
        """
        result = []
        
        def backtrack(start: int, current: List[int]) -> None:
            if len(current) == k:
                result.append(current.copy())
                return
            
            for i in range(start, n + 1):
                current.append(i)
                backtrack(i + 1, current)
                current.pop()
        
        backtrack(1, [])
        return result
    
    @staticmethod
    def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
        """
        Find all unique combinations that sum to target (can reuse candidates).
        
        Args:
            candidates: List of numbers
            target: Target sum
            
        Returns:
            List of combinations
        """
        result = []
        candidates.sort()
        
        def backtrack(start: int, current: List[int], remaining: int) -> None:
            if remaining == 0:
                result.append(current.copy())
                return
            
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break
                
                current.append(candidates[i])
                backtrack(i, current, remaining - candidates[i])
                current.pop()
        
        backtrack(0, [], target)
        return result
    
    @staticmethod
    def combination_sum_ii(candidates: List[int], target: int) -> List[List[int]]:
        """
        Find all unique combinations (each candidate used once).
        
        Args:
            candidates: List of numbers (may have duplicates)
            target: Target sum
            
        Returns:
            List of unique combinations
        """
        result = []
        candidates.sort()
        
        def backtrack(start: int, current: List[int], remaining: int) -> None:
            if remaining == 0:
                result.append(current.copy())
                return
            
            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i - 1]:
                    continue  # Skip duplicates
                
                if candidates[i] > remaining:
                    break
                
                current.append(candidates[i])
                backtrack(i + 1, current, remaining - candidates[i])
                current.pop()
        
        backtrack(0, [], target)
        return result
    
    @staticmethod
    def n_queens(n: int) -> List[List[str]]:
        """
        Solve N-Queens problem.
        
        Args:
            n: Board size
            
        Returns:
            List of board configurations
        """
        result = []
        board = [['.' for _ in range(n)] for _ in range(n)]
        
        def is_safe(row: int, col: int) -> bool:
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
        
        def backtrack(row: int) -> None:
            if row == n:
                result.append([''.join(r) for r in board])
                return
            
            for col in range(n):
                if is_safe(row, col):
                    board[row][col] = 'Q'
                    backtrack(row + 1)
                    board[row][col] = '.'
        
        backtrack(0)
        return result
    
    @staticmethod
    def solve_sudoku(board: List[List[str]]) -> Optional[List[List[str]]]:
        """
        Solve Sudoku puzzle.
        
        Args:
            board: 9x9 Sudoku board with '.' for empty cells
            
        Returns:
            Solved board or None if no solution
        """
        def is_valid(row: int, col: int, num: str) -> bool:
            # Check row
            for i in range(9):
                if board[row][i] == num:
                    return False
            
            # Check column
            for i in range(9):
                if board[i][col] == num:
                    return False
            
            # Check 3x3 box
            box_row, box_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if board[i][j] == num:
                        return False
            
            return True
        
        def solve() -> bool:
            for i in range(9):
                for j in range(9):
                    if board[i][j] == '.':
                        for num in map(str, range(1, 10)):
                            if is_valid(i, j, num):
                                board[i][j] = num
                                if solve():
                                    return True
                                board[i][j] = '.'
                        return False
            return True
        
        board_copy = [row.copy() for row in board]
        if solve():
            return board_copy
        return None
    
    @staticmethod
    def word_search(board: List[List[str]], word: str) -> bool:
        """
        Search for word in word search board.
        
        Args:
            board: 2D grid of characters
            word: Word to search
            
        Returns:
            True if word exists
        """
        if not board or not board[0]:
            return False
        
        rows, cols = len(board), len(board[0])
        
        def dfs(row: int, col: int, index: int) -> bool:
            if index == len(word):
                return True
            
            if (row < 0 or row >= rows or col < 0 or col >= cols or 
                board[row][col] != word[index]):
                return False
            
            # Mark as visited
            temp = board[row][col]
            board[row][col] = '#'
            
            found = (dfs(row + 1, col, index + 1) or
                    dfs(row - 1, col, index + 1) or
                    dfs(row, col + 1, index + 1) or
                    dfs(row, col - 1, index + 1))
            
            board[row][col] = temp
            return found
        
        for i in range(rows):
            for j in range(cols):
                if board[i][j] == word[0]:
                    if dfs(i, j, 0):
                        return True
        
        return False
    
    @staticmethod
    def palindrome_partitioning(s: str) -> List[List[str]]:
        """
        Partition string into palindromic substrings.
        
        Args:
            s: Input string
            
        Returns:
            List of all palindrome partitions
        """
        result = []
        
        def is_palindrome(sub: str) -> bool:
            return sub == sub[::-1]
        
        def backtrack(start: int, current: List[str]) -> None:
            if start == len(s):
                result.append(current.copy())
                return
            
            for end in range(start + 1, len(s) + 1):
                substring = s[start:end]
                if is_palindrome(substring):
                    current.append(substring)
                    backtrack(end, current)
                    current.pop()
        
        backtrack(0, [])
        return result


def main() -> None:
    """Demonstrate backtracking algorithms."""
    
    print("=== Backtracking Algorithms Demo ===")
    
    # Subsets
    print("\n--- Subsets ---")
    nums = [1, 2, 3]
    subsets = Backtracking.generate_subsets(nums)
    print(f"Subsets of {nums}: {subsets}")
    
    # Permutations
    print("\n--- Permutations ---")
    perms = Backtracking.generate_permutations(nums)
    print(f"Permutations of {nums}: {perms}")
    
    # Combinations
    print("\n--- Combinations ---")
    combos = Backtracking.generate_combinations(4, 2)
    print(f"Combinations of 4 choose 2: {combos}")
    
    # Combination sum
    print("\n--- Combination Sum ---")
    candidates = [2, 3, 6, 7]
    target = 7
    result = Backtracking.combination_sum(candidates, target)
    print(f"Combinations summing to {target}: {result}")
    
    # Combination sum II
    print("\n--- Combination Sum II ---")
    candidates = [10, 1, 2, 7, 6, 1, 5]
    target = 8
    result = Backtracking.combination_sum_ii(candidates, target)
    print(f"Unique combinations summing to {target}: {result}")
    
    # N-Queens
    print("\n--- N-Queens ---")
    n = 4
    solutions = Backtracking.n_queens(n)
    print(f"N-Queens (n={n}): {len(solutions)} solutions")
    for i, sol in enumerate(solutions):
        print(f"Solution {i + 1}:")
        for row in sol:
            print(f"  {row}")
    
    # Sudoku
    print("\n--- Sudoku ---")
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"]
    ]
    solved = Backtracking.solve_sudoku(board)
    if solved:
        print("Solved Sudoku:")
        for row in solved:
            print(f"  {row}")
    
    # Word search
    print("\n--- Word Search ---")
    board = [['A', 'B', 'C', 'E'], ['S', 'F', 'C', 'S'], ['A', 'D', 'E', 'E']]
    word = "ABCCED"
    print(f"Word '{word}' found: {Backtracking.word_search(board, word)}")
    
    # Palindrome partitioning
    print("\n--- Palindrome Partitioning ---")
    s = "aab"
    partitions = Backtracking.palindrome_partitioning(s)
    print(f"Palindrome partitions of '{s}': {partitions}")


if __name__ == "__main__":
    main()
