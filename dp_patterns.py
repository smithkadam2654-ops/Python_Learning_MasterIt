"""
Dynamic Programming Patterns - Common DP problem patterns.
Features: Memoization, tabulation, and classic DP problems.
"""

from typing import List, Dict, Optional


class DPPatterns:
    """Common dynamic programming patterns and solutions."""
    
    @staticmethod
    def fibonacci_memo(n: int, memo: Dict[int, int] = None) -> int:
        """
        Fibonacci with memoization (top-down).
        
        Args:
            n: nth Fibonacci number
            memo: Memoization dictionary
            
        Returns:
            nth Fibonacci number
        """
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return n
        
        memo[n] = DPPatterns.fibonacci_memo(n - 1, memo) + DPPatterns.fibonacci_memo(n - 2, memo)
        return memo[n]
    
    @staticmethod
    def fibonacci_tab(n: int) -> int:
        """
        Fibonacci with tabulation (bottom-up).
        
        Args:
            n: nth Fibonacci number
            
        Returns:
            nth Fibonacci number
        """
        if n <= 1:
            return n
        
        dp = [0] * (n + 1)
        dp[0] = 0
        dp[1] = 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n]
    
    @staticmethod
    def fibonacci_optimized(n: int) -> int:
        """
        Fibonacci with space optimization.
        
        Args:
            n: nth Fibonacci number
            
        Returns:
            nth Fibonacci number
        """
        if n <= 1:
            return n
        
        prev2 = 0
        prev1 = 1
        
        for _ in range(2, n + 1):
            curr = prev1 + prev2
            prev2 = prev1
            prev1 = curr
        
        return prev1
    
    @staticmethod
    def climb_stairs(n: int) -> int:
        """
        Count ways to climb n stairs (1 or 2 steps at a time).
        
        Args:
            n: Number of stairs
            
        Returns:
            Number of ways
        """
        if n <= 1:
            return 1
        
        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n]
    
    @staticmethod
    def coin_change(coins: List[int], amount: int) -> int:
        """
        Minimum number of coins to make amount.
        
        Args:
            coins: List of coin denominations
            amount: Target amount
            
        Returns:
            Minimum number of coins or -1 if not possible
        """
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        
        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] = min(dp[i], dp[i - coin] + 1)
        
        return dp[amount] if dp[amount] != float('inf') else -1
    
    @staticmethod
    def coin_change_ways(coins: List[int], amount: int) -> int:
        """
        Number of ways to make amount with coins.
        
        Args:
            coins: List of coin denominations
            amount: Target amount
            
        Returns:
            Number of ways
        """
        dp = [0] * (amount + 1)
        dp[0] = 1
        
        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]
        
        return dp[amount]
    
    @staticmethod
    def longest_increasing_subsequence(nums: List[int]) -> int:
        """
        Length of longest increasing subsequence.
        
        Args:
            nums: List of numbers
            
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
    
    @staticmethod
    def longest_common_subsequence(text1: str, text2: str) -> int:
        """
        Length of longest common subsequence.
        
        Args:
            text1: First string
            text2: Second string
            
        Returns:
            Length of LCS
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        return dp[m][n]
    
    @staticmethod
    def edit_distance(word1: str, word2: str) -> int:
        """
        Minimum edit distance (Levenshtein distance).
        
        Args:
            word1: First word
            word2: Second word
            
        Returns:
            Minimum edit distance
        """
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j],      # delete
                                      dp[i][j - 1],      # insert
                                      dp[i - 1][j - 1])  # replace
        
        return dp[m][n]
    
    @staticmethod
    def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
        """
        0/1 Knapsack problem.
        
        Args:
            weights: List of weights
            values: List of values
            capacity: Knapsack capacity
            
        Returns:
            Maximum value
        """
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i - 1] <= w:
                    dp[i][w] = max(dp[i - 1][w], 
                                  values[i - 1] + dp[i - 1][w - weights[i - 1]])
                else:
                    dp[i][w] = dp[i - 1][w]
        
        return dp[n][capacity]
    
    @staticmethod
    def knapsack_unbounded(weights: List[int], values: List[int], capacity: int) -> int:
        """
        Unbounded Knapsack problem (items can be used multiple times).
        
        Args:
            weights: List of weights
            values: List of values
            capacity: Knapsack capacity
            
        Returns:
            Maximum value
        """
        n = len(weights)
        dp = [0] * (capacity + 1)
        
        for w in range(capacity + 1):
            for i in range(n):
                if weights[i] <= w:
                    dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
        
        return dp[capacity]
    
    @staticmethod
    def max_subarray_sum(nums: List[int]) -> int:
        """
        Maximum subarray sum (Kadane's algorithm).
        
        Args:
            nums: List of numbers
            
        Returns:
            Maximum subarray sum
        """
        if not nums:
            return 0
        
        max_sum = nums[0]
        current_sum = nums[0]
        
        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    @staticmethod
    def palindrome_partitioning(s: str) -> int:
        """
        Minimum cuts to partition string into palindromes.
        
        Args:
            s: String
            
        Returns:
            Minimum cuts
        """
        n = len(s)
        if n == 0:
            return 0
        
        # Precompute palindrome table
        is_pal = [[False] * n for _ in range(n)]
        
        for i in range(n):
            is_pal[i][i] = True
        
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if length == 2:
                    is_pal[i][j] = s[i] == s[j]
                else:
                    is_pal[i][j] = s[i] == s[j] and is_pal[i + 1][j - 1]
        
        # DP for minimum cuts
        dp = [float('inf')] * n
        
        for i in range(n):
            if is_pal[0][i]:
                dp[i] = 0
            else:
                for j in range(i):
                    if is_pal[j + 1][i]:
                        dp[i] = min(dp[i], dp[j] + 1)
        
        return dp[n - 1]


def main() -> None:
    """Demonstrate DP patterns."""
    
    print("=== Dynamic Programming Patterns Demo ===")
    
    # Fibonacci
    print("\n--- Fibonacci ---")
    for n in [10, 20, 30]:
        print(f"Fib({n}): memo={DPPatterns.fibonacci_memo(n)}, "
              f"tab={DPPatterns.fibonacci_tab(n)}, "
              f"opt={DPPatterns.fibonacci_optimized(n)}")
    
    # Climb stairs
    print("\n--- Climb Stairs ---")
    for n in [5, 10, 15]:
        print(f"Stairs({n}): {DPPatterns.climb_stairs(n)} ways")
    
    # Coin change
    print("\n--- Coin Change ---")
    coins = [1, 2, 5]
    amount = 11
    print(f"Coins: {coins}, Amount: {amount}")
    print(f"Min coins: {DPPatterns.coin_change(coins, amount)}")
    print(f"Number of ways: {DPPatterns.coin_change_ways(coins, amount)}")
    
    # LIS
    print("\n--- Longest Increasing Subsequence ---")
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"Array: {nums}")
    print(f"LIS length: {DPPatterns.longest_increasing_subsequence(nums)}")
    
    # LCS
    print("\n--- Longest Common Subsequence ---")
    text1 = "abcde"
    text2 = "ace"
    print(f"'{text1}' and '{text2}'")
    print(f"LCS length: {DPPatterns.longest_common_subsequence(text1, text2)}")
    
    # Edit distance
    print("\n--- Edit Distance ---")
    word1 = "horse"
    word2 = "ros"
    print(f"'{word1}' -> '{word2}'")
    print(f"Edit distance: {DPPatterns.edit_distance(word1, word2)}")
    
    # Knapsack
    print("\n--- Knapsack ---")
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    print(f"0/1 Knapsack: {DPPatterns.knapsack_01(weights, values, capacity)}")
    print(f"Unbounded Knapsack: {DPPatterns.knapsack_unbounded(weights, values, capacity)}")
    
    # Max subarray sum
    print("\n--- Max Subarray Sum ---")
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"Array: {nums}")
    print(f"Max sum: {DPPatterns.max_subarray_sum(nums)}")
    
    # Palindrome partitioning
    print("\n--- Palindrome Partitioning ---")
    s = "aab"
    print(f"String: '{s}'")
    print(f"Min cuts: {DPPatterns.palindrome_partitioning(s)}")


if __name__ == "__main__":
    main()
