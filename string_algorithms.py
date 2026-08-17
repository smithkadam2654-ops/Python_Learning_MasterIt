"""
String Algorithms - Classic string manipulation and pattern matching algorithms.
Features: Pattern matching, substring search, and string transformations.
"""

from typing import List, Optional, Dict, Tuple


def is_anagram(s1: str, s2: str) -> bool:
    """
    Check if two strings are anagrams.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        True if anagrams, False otherwise
    """
    if len(s1) != len(s2):
        return False
    
    char_count = {}
    
    for char in s1:
        char_count[char] = char_count.get(char, 0) + 1
    
    for char in s2:
        if char not in char_count:
            return False
        char_count[char] -= 1
        if char_count[char] < 0:
            return False
    
    return True


def is_palindrome(s: str) -> bool:
    """
    Check if string is a palindrome.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        s: String to check
        
    Returns:
        True if palindrome, False otherwise
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True


def is_palindrome_ignore_case(s: str) -> bool:
    """
    Check if string is palindrome (case-insensitive, ignores non-alphanumeric).
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        s: String to check
        
    Returns:
        True if palindrome, False otherwise
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True


def longest_palindrome_substring(s: str) -> str:
    """
    Find longest palindromic substring.
    
    Time Complexity: O(n²)
    Space Complexity: O(1)
    
    Args:
        s: Input string
        
    Returns:
        Longest palindromic substring
    """
    if not s:
        return ""
    
    start = 0
    max_length = 1
    
    def expand_around_center(left: int, right: int) -> int:
        """Expand around center to find palindrome length."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    for i in range(len(s)):
        # Odd length palindrome
        len1 = expand_around_center(i, i)
        # Even length palindrome
        len2 = expand_around_center(i, i + 1)
        
        current_max = max(len1, len2)
        
        if current_max > max_length:
            max_length = current_max
            start = i - (current_max - 1) // 2
    
    return s[start:start + max_length]


def longest_common_subsequence(s1: str, s2: str) -> str:
    """
    Find longest common subsequence between two strings.
    
    Time Complexity: O(m*n)
    Space Complexity: O(m*n)
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Longest common subsequence
    """
    m, n = len(s1), len(s2)
    dp = [[""] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + s1[i - 1]
            else:
                dp[i][j] = dp[i - 1][j] if len(dp[i - 1][j]) >= len(dp[i][j - 1]) else dp[i][j - 1]
    
    return dp[m][n]


def longest_common_prefix(strs: List[str]) -> str:
    """
    Find longest common prefix among strings.
    
    Time Complexity: O(n*m) where n is number of strings, m is min length
    Space Complexity: O(1)
    
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


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Knuth-Morris-Pratt pattern matching algorithm.
    
    Time Complexity: O(n + m)
    Space Complexity: O(m)
    
    Args:
        text: Text to search in
        pattern: Pattern to search for
        
    Returns:
        List of starting indices where pattern is found
    """
    if not pattern:
        return []
    
    # Build partial match table
    def build_lps(pattern: str) -> List[int]:
        lps = [0] * len(pattern)
        length = 0
        i = 1
        
        while i < len(pattern):
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
        
        return lps
    
    lps = build_lps(pattern)
    result = []
    i = j = 0  # i for text, j for pattern
    
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
            if j == len(pattern):
                result.append(i - j)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return result


def rabin_karp_search(text: str, pattern: str, base: int = 256, prime: int = 101) -> List[int]:
    """
    Rabin-Karp pattern matching algorithm using rolling hash.
    
    Time Complexity: O(n + m) average, O(n*m) worst
    Space Complexity: O(1)
    
    Args:
        text: Text to search in
        pattern: Pattern to search for
        base: Base for hash calculation
        prime: Prime number for modulo
        
    Returns:
        List of starting indices where pattern is found
    """
    n, m = len(text), len(pattern)
    
    if m > n or m == 0:
        return []
    
    result = []
    
    # Calculate hash for pattern and first window of text
    pattern_hash = 0
    text_hash = 0
    h = 1
    
    for i in range(m - 1):
        h = (h * base) % prime
    
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        text_hash = (base * text_hash + ord(text[i])) % prime
    
    # Slide over text
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            # Check character by character
            if text[i:i + m] == pattern:
                result.append(i)
        
        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if text_hash < 0:
                text_hash += prime
    
    return result


def boyer_moore_search(text: str, pattern: str) -> List[int]:
    """
    Boyer-Moore pattern matching algorithm (simplified).
    
    Time Complexity: O(n/m) average, O(n*m) worst
    Space Complexity: O(m)
    
    Args:
        text: Text to search in
        pattern: Pattern to search for
        
    Returns:
        List of starting indices where pattern is found
    """
    if not pattern:
        return []
    
    n, m = len(text), len(pattern)
    result = []
    
    # Build bad character heuristic table
    bad_char = {}
    for i in range(m - 1):
        bad_char[pattern[i]] = m - 1 - i
    
    i = 0
    while i <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        
        if j < 0:
            result.append(i)
            i += m
        else:
            char_shift = bad_char.get(text[i + j], m)
            i += char_shift
    
    return result


def edit_distance(s1: str, s2: str) -> int:
    """
    Calculate minimum edit distance (Levenshtein distance).
    
    Time Complexity: O(m*n)
    Space Complexity: O(min(m,n))
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Minimum edit distance
    """
    if len(s1) < len(s2):
        return edit_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        
        previous_row = current_row
    
    return previous_row[-1]


def count_substrings(text: str, pattern: str) -> int:
    """
    Count occurrences of pattern in text (including overlapping).
    
    Time Complexity: O(n*m)
    Space Complexity: O(1)
    
    Args:
        text: Text to search in
        pattern: Pattern to count
        
    Returns:
        Number of occurrences
    """
    count = 0
    pattern_len = len(pattern)
    
    for i in range(len(text) - pattern_len + 1):
        if text[i:i + pattern_len] == pattern:
            count += 1
    
    return count


def remove_duplicates(s: str) -> str:
    """
    Remove duplicate characters from string.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Args:
        s: Input string
        
    Returns:
        String with duplicates removed
    """
    seen = set()
    result = []
    
    for char in s:
        if char not in seen:
            seen.add(char)
            result.append(char)
    
    return ''.join(result)


def compress_string(s: str) -> str:
    """
    Compress string using run-length encoding.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
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


def main() -> None:
    """Demonstrate string algorithms."""
    
    print("=== Anagram Check ===")
    print(f"is_anagram('listen', 'silent'): {is_anagram('listen', 'silent')}")
    print(f"is_anagram('hello', 'world'): {is_anagram('hello', 'world')}")
    
    print("\n=== Palindrome Check ===")
    print(f"is_palindrome('racecar'): {is_palindrome('racecar')}")
    print(f"is_palindrome('hello'): {is_palindrome('hello')}")
    print(f"is_palindrome_ignore_case('A man, a plan, a canal: Panama'): {is_palindrome_ignore_case('A man, a plan, a canal: Panama')}")
    
    print("\n=== Longest Palindromic Substring ===")
    s = "babad"
    print(f"String: {s}")
    print(f"Longest palindrome: {longest_palindrome_substring(s)}")
    
    print("\n=== Longest Common Subsequence ===")
    s1, s2 = "ABCDGH", "AEDFHR"
    print(f"LCS of '{s1}' and '{s2}': {longest_common_subsequence(s1, s2)}")
    
    print("\n=== Longest Common Prefix ===")
    strs = ["flower", "flow", "flight"]
    print(f"Strings: {strs}")
    print(f"Common prefix: {longest_common_prefix(strs)}")
    
    print("\n=== Pattern Matching ===")
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    print(f"KMP: {kmp_search(text, pattern)}")
    print(f"Rabin-Karp: {rabin_karp_search(text, pattern)}")
    print(f"Boyer-Moore: {boyer_moore_search(text, pattern)}")
    
    print("\n=== Edit Distance ===")
    s1, s2 = "kitten", "sitting"
    print(f"Edit distance between '{s1}' and '{s2}': {edit_distance(s1, s2)}")
    
    print("\n=== Count Substrings ===")
    text = "abababa"
    pattern = "aba"
    print(f"Count '{pattern}' in '{text}': {count_substrings(text, pattern)}")
    
    print("\n=== Remove Duplicates ===")
    s = "programming"
    print(f"Original: {s}")
    print(f"Without duplicates: {remove_duplicates(s)}")
    
    print("\n=== String Compression ===")
    s = "aaabbcddd"
    print(f"Original: {s}")
    print(f"Compressed: {compress_string(s)}")


if __name__ == "__main__":
    main()
