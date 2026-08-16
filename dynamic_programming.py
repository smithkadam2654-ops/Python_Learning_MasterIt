"""
Dynamic Programming - Implementation of classic DP problems.
Features: Memoization, tabulation, and optimization techniques.
"""

from typing import Dict, List, Optional
from functools import lru_cache
from dataclasses import dataclass


# ==================== FIBONACCI ====================

def fibonacci_recursive(n: int) -> int:
    """
    Calculate nth Fibonacci number using naive recursion.
    
    Time Complexity: O(2^n)
    Space Complexity: O(n)
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """
    Calculate nth Fibonacci number using memoization.
    
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


def fibonacci_tabulation(n: int) -> int:
    """
    Calculate nth Fibonacci number using tabulation.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]


def fibonacci_optimized(n: int) -> int:
    """
    Calculate nth Fibonacci number with space optimization.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr


# ==================== LONGEST COMMON SUBSEQUENCE ====================

def lcs_recursive(s1: str, s2: str, i: int = 0, j: int = 0, memo: Optional[Dict] = None) -> int:
    """
    Find length of longest common subsequence using memoization.
    
    Time Complexity: O(m*n)
    Space Complexity: O(m*n)
    
    Args:
        s1: First string
        s2: Second string
        i: Current index in s1
        j: Current index in s2
        memo: Memoization dictionary
        
    Returns:
        Length of LCS
    """
    if memo is None:
        memo = {}
    
    if i == len(s1) or j == len(s2):
        return 0
    
    if (i, j) in memo:
        return memo[(i, j)]
    
    if s1[i] == s2[j]:
        result = 1 + lcs_recursive(s1, s2, i + 1, j + 1, memo)
    else:
        result = max(
            lcs_recursive(s1, s2, i + 1, j, memo),
            lcs_recursive(s1, s2, i, j + 1, memo)
        )
    
    memo[(i, j)] = result
    return result


def lcs_tabulation(s1: str, s2: str) -> int:
    """
    Find length of longest common subsequence using tabulation.
    
    Time Complexity: O(m*n)
    Space Complexity: O(m*n)
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Length of LCS
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


def lcs_reconstruct(s1: str, s2: str) -> str:
    """
    Reconstruct the actual longest common subsequence.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        The LCS string
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Build DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Reconstruct LCS
    lcs = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs))


# ==================== KNAPSACK PROBLEM ====================

@dataclass
class Item:
    """Item for knapsack problem."""
    weight: int
    value: int


def knapsack_0_1(items: List[Item], capacity: int) -> int:
    """
    Solve 0/1 Knapsack problem using dynamic programming.
    
    Time Complexity: O(n*W)
    Space Complexity: O(n*W)
    
    Args:
        items: List of items with weight and value
        capacity: Maximum weight capacity
        
    Returns:
        Maximum value achievable
    """
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if items[i - 1].weight <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - items[i - 1].weight] + items[i - 1].value
                )
            else:
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]


def knapsack_0_1_optimized(items: List[Item], capacity: int) -> int:
    """
    Solve 0/1 Knapsack with space optimization.
    
    Time Complexity: O(n*W)
    Space Complexity: O(W)
    
    Args:
        items: List of items with weight and value
        capacity: Maximum weight capacity
        
    Returns:
        Maximum value achievable
    """
    dp = [0] * (capacity + 1)
    
    for item in items:
        for w in range(capacity, item.weight - 1, -1):
            dp[w] = max(dp[w], dp[w - item.weight] + item.value)
    
    return dp[capacity]


# ==================== COIN CHANGE ====================

def coin_change(coins: List[int], amount: int) -> int:
    """
    Find minimum number of coins to make amount.
    
    Time Complexity: O(n*amount)
    Space Complexity: O(amount)
    
    Args:
        coins: List of coin denominations
        amount: Target amount
        
    Returns:
        Minimum number of coins, or -1 if impossible
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_ways(coins: List[int], amount: int) -> int:
    """
    Find number of ways to make amount with coins.
    
    Time Complexity: O(n*amount)
    Space Complexity: O(amount)
    
    Args:
        coins: List of coin denominations
        amount: Target amount
        
    Returns:
        Number of ways to make the amount
    """
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    
    return dp[amount]


# ==================== LONGEST INCREASING SUBSEQUENCE ====================

def lis_length(nums: List[int]) -> int:
    """
    Find length of longest increasing subsequence.
    
    Time Complexity: O(n²)
    Space Complexity: O(n)
    
    Args:
        nums: List of integers
        
    Returns:
        Length of LIS
    """
    if not nums:
        return 0
    
    n = len(nums)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


def lis_length_optimized(nums: List[int]) -> int:
    """
    Find LIS length using binary search (O(n log n)).
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        nums: List of integers
        
    Returns:
        Length of LIS
    """
    if not nums:
        return 0
    
    tails = []
    
    for num in nums:
        # Binary search for position
        left, right = 0, len(tails)
        
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        
        if left == len(tails):
            tails.append(num)
        else:
            tails[left] = num
    
    return len(tails)


# ==================== EDIT DISTANCE ====================

def edit_distance(s1: str, s2: str) -> int:
    """
    Calculate minimum edit distance (Levenshtein distance).
    
    Operations: insert, delete, replace (all cost 1)
    
    Time Complexity: O(m*n)
    Space Complexity: O(m*n)
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Minimum edit distance
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )
    
    return dp[m][n]


def main() -> None:
    """Demonstrate dynamic programming algorithms."""
    
    print("=== Fibonacci Comparison ===")
    n = 10
    print(f"fibonacci_recursive({n}): {fibonacci_recursive(n)}")
    print(f"fibonacci_memoized({n}): {fibonacci_memoized(n)}")
    print(f"fibonacci_tabulation({n}): {fibonacci_tabulation(n)}")
    print(f"fibonacci_optimized({n}): {fibonacci_optimized(n)}")
    
    print("\n=== Longest Common Subsequence ===")
    s1, s2 = "ABCDGH", "AEDFHR"
    print(f"LCS length of '{s1}' and '{s2}': {lcs_tabulation(s1, s2)}")
    print(f"LCS string: '{lcs_reconstruct(s1, s2)}'")
    
    print("\n=== 0/1 Knapsack Problem ===")
    items = [Item(2, 3), Item(3, 4), Item(4, 5), Item(5, 8)]
    capacity = 5
    max_value = knapsack_0_1(items, capacity)
    print(f"Max value with capacity {capacity}: {max_value}")
    print(f"Optimized: {knapsack_0_1_optimized(items, capacity)}")
    
    print("\n=== Coin Change ===")
    coins = [1, 2, 5]
    amount = 11
    print(f"Min coins for {amount}: {coin_change(coins, amount)}")
    print(f"Number of ways: {coin_change_ways(coins, amount)}")
    
    print("\n=== Longest Increasing Subsequence ===")
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"LIS length of {nums}: {lis_length(nums)}")
    print(f"Optimized: {lis_length_optimized(nums)}")
    
    print("\n=== Edit Distance ===")
    s1, s2 = "kitten", "sitting"
    print(f"Edit distance between '{s1}' and '{s2}': {edit_distance(s1, s2)}")


if __name__ == "__main__":
    main()
