"""
String Algorithms - Common string processing operations.
Features: Pattern matching, string manipulation, and text processing.
"""

from typing import List, Optional
import re


class StringAlgorithms:
    """String algorithm implementations."""
    
    @staticmethod
    def is_palindrome(s: str) -> bool:
        """
        Check if string is palindrome.
        
        Args:
            s: Input string
            
        Returns:
            True if palindrome
        """
        return s == s[::-1]
    
    @staticmethod
    def is_palindrome_ignore_case(s: str) -> bool:
        """
        Check if string is palindrome ignoring case.
        
        Args:
            s: Input string
            
        Returns:
            True if palindrome
        """
        s_lower = s.lower()
        return s_lower == s_lower[::-1]
    
    @staticmethod
    def is_palindrome_ignore_non_alphanumeric(s: str) -> bool:
        """
        Check if string is palindrome ignoring non-alphanumeric characters.
        
        Args:
            s: Input string
            
        Returns:
            True if palindrome
        """
        cleaned = ''.join(c.lower() for c in s if c.isalnum())
        return cleaned == cleaned[::-1]
    
    @staticmethod
    def reverse_words(s: str) -> str:
        """
        Reverse words in string.
        
        Args:
            s: Input string
            
        Returns:
            String with words reversed
        """
        words = s.split()
        return ' '.join(reversed(words))
    
    @staticmethod
    def reverse_words_in_place(s: str) -> str:
        """
        Reverse words in string (preserving whitespace).
        
        Args:
            s: Input string
            
        Returns:
            String with words reversed
        """
        return ' '.join(s.split()[::-1])
    
    @staticmethod
    def reverse_string(s: str) -> str:
        """
        Reverse string.
        
        Args:
            s: Input string
            
        Returns:
            Reversed string
        """
        return s[::-1]
    
    @staticmethod
    def count_vowels(s: str) -> int:
        """
        Count vowels in string.
        
        Args:
            s: Input string
            
        Returns:
            Number of vowels
        """
        vowels = set('aeiouAEIOU')
        return sum(1 for c in s if c in vowels)
    
    @staticmethod
    def count_consonants(s: str) -> int:
        """
        Count consonants in string.
        
        Args:
            s: Input string
            
        Returns:
            Number of consonants
        """
        vowels = set('aeiouAEIOU')
        return sum(1 for c in s if c.isalpha() and c not in vowels)
    
    @staticmethod
    def count_words(s: str) -> int:
        """
        Count words in string.
        
        Args:
            s: Input string
            
        Returns:
            Number of words
        """
        return len(s.split())
    
    @staticmethod
    def capitalize_words(s: str) -> str:
        """
        Capitalize first letter of each word.
        
        Args:
            s: Input string
            
        Returns:
            String with capitalized words
        """
        return ' '.join(word.capitalize() for word in s.split())
    
    @staticmethod
    def title_case(s: str) -> str:
        """
        Convert string to title case.
        
        Args:
            s: Input string
            
        Returns:
            Title cased string
        """
        return s.title()
    
    @staticmethod
    def remove_duplicates(s: str) -> str:
        """
        Remove duplicate characters from string.
        
        Args:
            s: Input string
            
        Returns:
            String with duplicates removed
        """
        seen = set()
        result = []
        for c in s:
            if c not in seen:
                seen.add(c)
                result.append(c)
        return ''.join(result)
    
    @staticmethod
    def remove_duplicates_preserve_order(s: str) -> str:
        """
        Remove duplicate characters preserving order.
        
        Args:
            s: Input string
            
        Returns:
            String with duplicates removed
        """
        return StringAlgorithms.remove_duplicates(s)
    
    @staticmethod
    def is_anagram(s1: str, s2: str) -> bool:
        """
        Check if two strings are anagrams.
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            True if anagrams
        """
        s1_clean = ''.join(c.lower() for c in s1 if c.isalnum())
        s2_clean = ''.join(c.lower() for c in s2 if c.isalnum())
        return sorted(s1_clean) == sorted(s2_clean)
    
    @staticmethod
    def is_anagram_count(s1: str, s2: str) -> bool:
        """
        Check if two strings are anagrams using character count.
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            True if anagrams
        """
        from collections import Counter
        
        s1_clean = ''.join(c.lower() for c in s1 if c.isalnum())
        s2_clean = ''.join(c.lower() for c in s2 if c.isalnum())
        return Counter(s1_clean) == Counter(s2_clean)
    
    @staticmethod
    def longest_common_prefix(strs: List[str]) -> str:
        """
        Find longest common prefix among strings.
        
        Args:
            strs: List of strings
            
        Returns:
            Longest common prefix
        """
        if not strs:
            return ""
        
        prefix = strs[0]
        
        for s in strs[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        
        return prefix
    
    @staticmethod
    def longest_palindromic_substring(s: str) -> str:
        """
        Find longest palindromic substring.
        
        Args:
            s: Input string
            
        Returns:
            Longest palindromic substring
        """
        if not s:
            return ""
        
        longest = s[0]
        
        for i in range(len(s)):
            # Odd length palindromes
            palindrome = StringAlgorithms._expand_around_center(s, i, i)
            if len(palindrome) > len(longest):
                longest = palindrome
            
            # Even length palindromes
            palindrome = StringAlgorithms._expand_around_center(s, i, i + 1)
            if len(palindrome) > len(longest):
                longest = palindrome
        
        return longest
    
    @staticmethod
    def _expand_around_center(s: str, left: int, right: int) -> str:
        """Helper for longest palindromic substring."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        
        return s[left + 1:right]
    
    @staticmethod
    def count_substrings(s: str) -> int:
        """
        Count all substrings of string.
        
        Args:
            s: Input string
            
        Returns:
            Number of substrings
        """
        n = len(s)
        return n * (n + 1) // 2
    
    @staticmethod
    def all_substrings(s: str) -> List[str]:
        """
        Generate all substrings of string.
        
        Args:
            s: Input string
            
        Returns:
            List of all substrings
        """
        n = len(s)
        substrings = []
        
        for i in range(n):
            for j in range(i + 1, n + 1):
                substrings.append(s[i:j])
        
        return substrings
    
    @staticmethod
    def is_rotation(s1: str, s2: str) -> bool:
        """
        Check if s2 is rotation of s1.
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            True if s2 is rotation of s1
        """
        if len(s1) != len(s2):
            return False
        
        return s2 in s1 + s1
    
    @staticmethod
    def compress_string(s: str) -> str:
        """
        Compress string using run-length encoding.
        
        Args:
            s: Input string
            
        Returns:
            Compressed string
        """
        if not s:
            return ""
        
        compressed = []
        count = 1
        
        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                count += 1
            else:
                compressed.append(s[i - 1] + str(count))
                count = 1
        
        compressed.append(s[-1] + str(count))
        
        result = ''.join(compressed)
        return result if len(result) < len(s) else s
    
    @staticmethod
    def decompress_string(s: str) -> str:
        """
        Decompress run-length encoded string.
        
        Args:
            s: Compressed string
            
        Returns:
            Decompressed string
        """
        if not s:
            return ""
        
        decompressed = []
        i = 0
        
        while i < len(s):
            char = s[i]
            i += 1
            
            count_str = ""
            while i < len(s) and s[i].isdigit():
                count_str += s[i]
                i += 1
            
            count = int(count_str) if count_str else 1
            decompressed.append(char * count)
        
        return ''.join(decompressed)
    
    @staticmethod
    def is_valid_parentheses(s: str) -> bool:
        """
        Check if string has valid parentheses.
        
        Args:
            s: Input string
            
        Returns:
            True if valid
        """
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        
        for char in s:
            if char in mapping.values():
                stack.append(char)
            elif char in mapping:
                if not stack or stack.pop() != mapping[char]:
                    return False
        
        return len(stack) == 0
    
    @staticmethod
    def min_insertions_for_palindrome(s: str) -> int:
        """
        Minimum insertions to make string palindrome.
        
        Args:
            s: Input string
            
        Returns:
            Minimum insertions
        """
        n = len(s)
        dp = [[0] * n for _ in range(n)]
        
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1]
                else:
                    dp[i][j] = min(dp[i + 1][j], dp[i][j - 1]) + 1
        
        return dp[0][n - 1] if n > 0 else 0
    
    @staticmethod
    def edit_distance(s1: str, s2: str) -> int:
        """
        Calculate edit distance (Levenshtein distance).
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            Edit distance
        """
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j],      # delete
                                      dp[i][j - 1],      # insert
                                      dp[i - 1][j - 1])  # replace
        
        return dp[m][n]
    
    @staticmethod
    def find_all_occurrences(text: str, pattern: str) -> List[int]:
        """
        Find all occurrences of pattern in text.
        
        Args:
            text: Text to search
            pattern: Pattern to find
            
        Returns:
            List of starting indices
        """
        indices = []
        pattern_len = len(pattern)
        
        for i in range(len(text) - pattern_len + 1):
            if text[i:i + pattern_len] == pattern:
                indices.append(i)
        
        return indices
    
    @staticmethod
    def find_all_occurrences_regex(text: str, pattern: str) -> List[int]:
        """
        Find all occurrences using regex.
        
        Args:
            text: Text to search
            pattern: Regex pattern
            
        Returns:
            List of starting indices
        """
        indices = []
        for match in re.finditer(pattern, text):
            indices.append(match.start())
        return indices


def main() -> None:
    """Demonstrate string algorithms."""
    
    print("=== String Algorithms Demo ===")
    
    # Palindrome
    print("\n--- Palindrome ---")
    s = "racecar"
    print(f"'{s}' is palindrome: {StringAlgorithms.is_palindrome(s)}")
    print(f"'A man, a plan, a canal: Panama' (ignore non-alnum): "
          f"{StringAlgorithms.is_palindrome_ignore_non_alphanumeric('A man, a plan, a canal: Panama')}")
    
    # Reverse words
    print("\n--- Reverse Words ---")
    s = "Hello World Python"
    print(f"Original: '{s}'")
    print(f"Reversed words: '{StringAlgorithms.reverse_words(s)}'")
    
    # Count characters
    print("\n--- Count Characters ---")
    s = "Hello World"
    print(f"'{s}'")
    print(f"Vowels: {StringAlgorithms.count_vowels(s)}")
    print(f"Consonants: {StringAlgorithms.count_consonants(s)}")
    print(f"Words: {StringAlgorithms.count_words(s)}")
    
    # Capitalize
    print("\n--- Capitalize ---")
    s = "hello world"
    print(f"Original: '{s}'")
    print(f"Capitalized: '{StringAlgorithms.capitalize_words(s)}'")
    
    # Remove duplicates
    print("\n--- Remove Duplicates ---")
    s = "hello world"
    print(f"Original: '{s}'")
    print(f"No duplicates: '{StringAlgorithms.remove_duplicates(s)}'")
    
    # Anagram
    print("\n--- Anagram ---")
    s1, s2 = "listen", "silent"
    print(f"'{s1}' and '{s2}' are anagrams: {StringAlgorithms.is_anagram(s1, s2)}")
    
    # Longest common prefix
    print("\n--- Longest Common Prefix ---")
    strs = ["flower", "flow", "flight"]
    print(f"Strings: {strs}")
    print(f"LCP: '{StringAlgorithms.longest_common_prefix(strs)}'")
    
    # Longest palindromic substring
    print("\n--- Longest Palindromic Substring ---")
    s = "babad"
    print(f"String: '{s}'")
    print(f"Longest palindrome: '{StringAlgorithms.longest_palindromic_substring(s)}'")
    
    # Count substrings
    print("\n--- Substrings ---")
    s = "abc"
    print(f"String: '{s}'")
    print(f"Total substrings: {StringAlgorithms.count_substrings(s)}")
    print(f"All substrings: {StringAlgorithms.all_substrings(s)}")
    
    # Rotation
    print("\n--- Rotation ---")
    s1, s2 = "waterbottle", "erbottlewat"
    print(f"'{s2}' is rotation of '{s1}': {StringAlgorithms.is_rotation(s1, s2)}")
    
    # Compress
    print("\n--- Compression ---")
    s = "aaabbbcc"
    print(f"Original: '{s}'")
    print(f"Compressed: '{StringAlgorithms.compress_string(s)}'")
    print(f"Decompressed: '{StringAlgorithms.decompress_string(StringAlgorithms.compress_string(s))}'")
    
    # Valid parentheses
    print("\n--- Valid Parentheses ---")
    s = "()[]{}"
    print(f"'{s}' is valid: {StringAlgorithms.is_valid_parentheses(s)}")
    
    # Edit distance
    print("\n--- Edit Distance ---")
    s1, s2 = "kitten", "sitting"
    print(f"Edit distance between '{s1}' and '{s2}': {StringAlgorithms.edit_distance(s1, s2)}")
    
    # Find occurrences
    print("\n--- Find Occurrences ---")
    text = "ababa"
    pattern = "aba"
    print(f"Text: '{text}', Pattern: '{pattern}'")
    print(f"Indices: {StringAlgorithms.find_all_occurrences(text, pattern)}")


if __name__ == "__main__":
    main()
