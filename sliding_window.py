"""
Sliding Window Technique - Pattern for array/string problems.
Features: Fixed and variable window sizes, two pointers, and substring problems.
"""

from typing import List, Optional


class SlidingWindow:
    """Sliding window algorithm implementations."""
    
    @staticmethod
    def max_sum_subarray(nums: List[int], k: int) -> Optional[int]:
        """
        Maximum sum of subarray of size k (fixed window).
        
        Args:
            nums: List of numbers
            k: Window size
            
        Returns:
            Maximum sum or None if invalid
        """
        if len(nums) < k:
            return None
        
        # Calculate first window
        window_sum = sum(nums[:k])
        max_sum = window_sum
        
        # Slide window
        for i in range(k, len(nums)):
            window_sum += nums[i] - nums[i - k]
            max_sum = max(max_sum, window_sum)
        
        return max_sum
    
    @staticmethod
    def min_sum_subarray(nums: List[int], k: int) -> Optional[int]:
        """
        Minimum sum of subarray of size k.
        
        Args:
            nums: List of numbers
            k: Window size
            
        Returns:
            Minimum sum or None if invalid
        """
        if len(nums) < k:
            return None
        
        window_sum = sum(nums[:k])
        min_sum = window_sum
        
        for i in range(k, len(nums)):
            window_sum += nums[i] - nums[i - k]
            min_sum = min(min_sum, window_sum)
        
        return min_sum
    
    @staticmethod
    def max_average_subarray(nums: List[int], k: int) -> Optional[float]:
        """
        Maximum average of subarray of size k.
        
        Args:
            nums: List of numbers
            k: Window size
            
        Returns:
            Maximum average or None if invalid
        """
        if len(nums) < k:
            return None
        
        window_sum = sum(nums[:k])
        max_sum = window_sum
        
        for i in range(k, len(nums)):
            window_sum += nums[i] - nums[i - k]
            max_sum = max(max_sum, window_sum)
        
        return max_sum / k
    
    @staticmethod
    def longest_substring_without_repeating(s: str) -> int:
        """
        Length of longest substring without repeating characters (variable window).
        
        Args:
            s: Input string
            
        Returns:
            Maximum length
        """
        char_index = {}
        max_length = 0
        left = 0
        
        for right, char in enumerate(s):
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1
            
            char_index[char] = right
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    @staticmethod
    def longest_substring_with_at_most_k_distinct(s: str, k: int) -> int:
        """
        Longest substring with at most k distinct characters.
        
        Args:
            s: Input string
            k: Maximum distinct characters
            
        Returns:
            Maximum length
        """
        if k == 0:
            return 0
        
        char_count = {}
        max_length = 0
        left = 0
        
        for right, char in enumerate(s):
            char_count[char] = char_count.get(char, 0) + 1
            
            while len(char_count) > k:
                left_char = s[left]
                char_count[left_char] -= 1
                if char_count[left_char] == 0:
                    del char_count[left_char]
                left += 1
            
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    @staticmethod
    def minimum_window_substring(s: str, t: str) -> str:
        """
        Minimum window substring containing all characters of t.
        
        Args:
            s: Source string
            t: Target string
            
        Returns:
            Minimum window or empty string if not found
        """
        from collections import Counter
        
        if not s or not t or len(s) < len(t):
            return ""
        
        target_count = Counter(t)
        required = len(target_count)
        
        window_count = {}
        formed = 0
        
        left = 0
        min_length = float('inf')
        min_window = (0, 0)
        
        for right, char in enumerate(s):
            window_count[char] = window_count.get(char, 0) + 1
            
            if char in target_count and window_count[char] == target_count[char]:
                formed += 1
            
            while left <= right and formed == required:
                # Update minimum window
                if right - left + 1 < min_length:
                    min_length = right - left + 1
                    min_window = (left, right)
                
                # Remove left character
                left_char = s[left]
                window_count[left_char] -= 1
                if left_char in target_count and window_count[left_char] < target_count[left_char]:
                    formed -= 1
                
                left += 1
        
        return s[min_window[0]:min_window[1] + 1] if min_length != float('inf') else ""
    
    @staticmethod
    def longest_subarray_with_sum(nums: List[int], target: int) -> int:
        """
        Length of longest subarray with sum equal to target.
        
        Args:
            nums: List of numbers (can be negative)
            target: Target sum
            
        Returns:
            Maximum length or 0 if not found
        """
        prefix_sum = {0: -1}
        current_sum = 0
        max_length = 0
        
        for i, num in enumerate(nums):
            current_sum += num
            
            if current_sum - target in prefix_sum:
                max_length = max(max_length, i - prefix_sum[current_sum - target])
            
            if current_sum not in prefix_sum:
                prefix_sum[current_sum] = i
        
        return max_length
    
    @staticmethod
    def subarray_sum_equals_k(nums: List[int], k: int) -> int:
        """
        Count number of subarrays with sum equal to k.
        
        Args:
            nums: List of numbers (can be negative)
            k: Target sum
            
        Returns:
            Count of subarrays
        """
        prefix_sum = {0: 1}
        current_sum = 0
        count = 0
        
        for num in nums:
            current_sum += num
            
            if current_sum - k in prefix_sum:
                count += prefix_sum[current_sum - k]
            
            prefix_sum[current_sum] = prefix_sum.get(current_sum, 0) + 1
        
        return count
    
    @staticmethod
    def max_consecutive_ones(nums: List[int]) -> int:
        """
        Maximum number of consecutive 1s (can flip k zeros).
        
        Args:
            nums: Binary array
            
        Returns:
            Maximum consecutive 1s
        """
        left = 0
        max_length = 0
        zero_count = 0
        
        for right in range(len(nums)):
            if nums[right] == 0:
                zero_count += 1
            
            while zero_count > 1:
                if nums[left] == 0:
                    zero_count -= 1
                left += 1
            
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    @staticmethod
    def max_consecutive_ones_k(nums: List[int], k: int) -> int:
        """
        Maximum consecutive 1s with at most k flips.
        
        Args:
            nums: Binary array
            k: Maximum flips allowed
            
        Returns:
            Maximum consecutive 1s
        """
        left = 0
        max_length = 0
        zero_count = 0
        
        for right in range(len(nums)):
            if nums[right] == 0:
                zero_count += 1
            
            while zero_count > k:
                if nums[left] == 0:
                    zero_count -= 1
                left += 1
            
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    @staticmethod
    def longest_subarray_with_ones_after_deletion(nums: List[int]) -> int:
        """
        Longest subarray of 1s after deleting one element.
        
        Args:
            nums: Binary array
            
        Returns:
            Maximum length
        """
        left = 0
        max_length = 0
        zero_count = 0
        
        for right in range(len(nums)):
            if nums[right] == 0:
                zero_count += 1
            
            while zero_count > 1:
                if nums[left] == 0:
                    zero_count -= 1
                left += 1
            
            max_length = max(max_length, right - left)
        
        return max_length
    
    @staticmethod
    def minimum_size_subarray_sum(nums: List[int], target: int) -> int:
        """
        Minimum length subarray with sum >= target (positive numbers only).
        
        Args:
            nums: List of positive numbers
            target: Target sum
            
        Returns:
            Minimum length or 0 if not found
        """
        left = 0
        current_sum = 0
        min_length = float('inf')
        
        for right in range(len(nums)):
            current_sum += nums[right]
            
            while current_sum >= target:
                min_length = min(min_length, right - left + 1)
                current_sum -= nums[left]
                left += 1
        
        return min_length if min_length != float('inf') else 0


def main() -> None:
    """Demonstrate sliding window techniques."""
    
    print("=== Sliding Window Demo ===")
    
    # Fixed window - max sum
    print("\n--- Max Sum Subarray (Fixed Window) ---")
    nums = [2, 1, 5, 1, 3, 2]
    k = 3
    print(f"Array: {nums}, k={k}")
    print(f"Max sum: {SlidingWindow.max_sum_subarray(nums, k)}")
    
    # Fixed window - min sum
    print("\n--- Min Sum Subarray ---")
    print(f"Min sum: {SlidingWindow.min_sum_subarray(nums, k)}")
    
    # Fixed window - max average
    print("\n--- Max Average Subarray ---")
    print(f"Max average: {SlidingWindow.max_average_subarray(nums, k):.2f}")
    
    # Variable window - longest substring without repeating
    print("\n--- Longest Substring Without Repeating ---")
    s = "abcabcbb"
    print(f"String: '{s}'")
    print(f"Max length: {SlidingWindow.longest_substring_without_repeating(s)}")
    
    # Variable window - at most k distinct
    print("\n--- Longest Substring with K Distinct ---")
    s = "eceba"
    k = 2
    print(f"String: '{s}', k={k}")
    print(f"Max length: {SlidingWindow.longest_substring_with_at_most_k_distinct(s, k)}")
    
    # Minimum window substring
    print("\n--- Minimum Window Substring ---")
    s = "ADOBECODEBANC"
    t = "ABC"
    print(f"Source: '{s}', Target: '{t}'")
    print(f"Min window: '{SlidingWindow.minimum_window_substring(s, t)}'")
    
    # Longest subarray with sum
    print("\n--- Longest Subarray with Sum ---")
    nums = [1, -1, 5, -2, 3]
    target = 3
    print(f"Array: {nums}, target={target}")
    print(f"Max length: {SlidingWindow.longest_subarray_with_sum(nums, target)}")
    
    # Subarray sum equals k
    print("\n--- Subarray Sum Equals K ---")
    nums = [1, 1, 1]
    k = 2
    print(f"Array: {nums}, k={k}")
    print(f"Count: {SlidingWindow.subarray_sum_equals_k(nums, k)}")
    
    # Max consecutive ones
    print("\n--- Max Consecutive Ones ---")
    nums = [1, 1, 0, 1, 1, 1]
    print(f"Array: {nums}")
    print(f"Max consecutive: {SlidingWindow.max_consecutive_ones(nums)}")
    
    # Max consecutive ones with k flips
    print("\n--- Max Consecutive Ones with K Flips ---")
    nums = [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1]
    k = 2
    print(f"Array: {nums}, k={k}")
    print(f"Max consecutive: {SlidingWindow.max_consecutive_ones_k(nums, k)}")
    
    # Longest subarray after deletion
    print("\n--- Longest Subarray After Deletion ---")
    nums = [0, 1, 1, 1, 0, 1, 1, 0, 1]
    print(f"Array: {nums}")
    print(f"Max length: {SlidingWindow.longest_subarray_with_ones_after_deletion(nums)}")
    
    # Minimum size subarray sum
    print("\n--- Minimum Size Subarray Sum ---")
    nums = [2, 3, 1, 2, 4, 3]
    target = 7
    print(f"Array: {nums}, target={target}")
    print(f"Min length: {SlidingWindow.minimum_size_subarray_sum(nums, target)}")


if __name__ == "__main__":
    main()
