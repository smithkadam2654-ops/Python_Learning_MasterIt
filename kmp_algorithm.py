"""
KMP Algorithm - Knuth-Morris-Pratt string matching algorithm.
Features: Pattern preprocessing, O(n+m) time complexity, and failure function.
"""

from typing import List, Tuple


class KMPAlgorithm:
    """Knuth-Morris-Pratt algorithm implementation."""
    
    def __init__(self, pattern: str) -> None:
        """
        Initialize KMP algorithm with pattern.
        
        Args:
            pattern: Pattern to search for
        """
        self.pattern = pattern
        self.lps = self._build_lps_array()
    
    def _build_lps_array(self) -> List[int]:
        """
        Build Longest Prefix Suffix (LPS) array.
        
        Returns:
            LPS array where LPS[i] = length of longest proper prefix
            which is also suffix of pattern[0..i]
        """
        m = len(self.pattern)
        lps = [0] * m
        length = 0  # Length of previous longest prefix suffix
        i = 1
        
        while i < m:
            if self.pattern[i] == self.pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    # Try shorter prefix
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        
        return lps
    
    def search(self, text: str) -> List[int]:
        """
        Search for pattern in text.
        
        Args:
            text: Text to search in
            
        Returns:
            List of starting indices where pattern occurs
        """
        n = len(text)
        m = len(self.pattern)
        
        if m == 0 or n < m:
            return []
        
        result = []
        i = 0  # Index for text
        j = 0  # Index for pattern
        
        while i < n:
            if self.pattern[j] == text[i]:
                i += 1
                j += 1
                
                if j == m:
                    # Pattern found
                    result.append(i - j)
                    # Continue searching for more occurrences
                    j = self.lps[j - 1]
            else:
                if j != 0:
                    # Use LPS to skip comparisons
                    j = self.lps[j - 1]
                else:
                    i += 1
        
        return result
    
    def count_occurrences(self, text: str) -> int:
        """
        Count occurrences of pattern in text.
        
        Args:
            text: Text to search in
            
        Returns:
            Number of occurrences
        """
        return len(self.search(text))
    
    def get_lps_array(self) -> List[int]:
        """Get LPS array."""
        return self.lps
    
    def first_occurrence(self, text: str) -> int:
        """
        Find first occurrence of pattern.
        
        Args:
            text: Text to search in
            
        Returns:
            Index of first occurrence or -1 if not found
        """
        occurrences = self.search(text)
        return occurrences[0] if occurrences else -1
    
    def contains(self, text: str) -> bool:
        """
        Check if text contains pattern.
        
        Args:
            text: Text to search in
            
        Returns:
            True if pattern is found
        """
        return self.first_occurrence(text) != -1


class KMPWithWildcards(KMPAlgorithm):
    """KMP algorithm with wildcard support."""
    
    def __init__(self, pattern: str, wildcard: str = '*') -> None:
        """
        Initialize KMP with wildcard support.
        
        Args:
            pattern: Pattern to search for (may contain wildcards)
            wildcard: Wildcard character
        """
        self.wildcard = wildcard
        super().__init__(pattern)
    
    def _build_lps_array(self) -> List[int]:
        """Build LPS array with wildcard support."""
        m = len(self.pattern)
        lps = [0] * m
        length = 0
        i = 1
        
        while i < m:
            if (self.pattern[i] == self.pattern[length] or 
                self.pattern[i] == self.wildcard or 
                self.pattern[length] == self.wildcard):
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
    
    def search(self, text: str) -> List[int]:
        """Search with wildcard support."""
        n = len(text)
        m = len(self.pattern)
        
        if m == 0 or n < m:
            return []
        
        result = []
        i = 0
        j = 0
        
        while i < n:
            if (self.pattern[j] == text[i] or 
                self.pattern[j] == self.wildcard):
                i += 1
                j += 1
                
                if j == m:
                    result.append(i - j)
                    j = self.lps[j - 1]
            else:
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1
        
        return result


def compute_lps_brute_force(pattern: str) -> List[int]:
    """
    Compute LPS array using brute force (for verification).
    
    Args:
        pattern: Pattern string
        
    Returns:
        LPS array
    """
    m = len(pattern)
    lps = [0] * m
    
    for i in range(m):
        for length in range(i, 0, -1):
            prefix = pattern[:length]
            suffix = pattern[i - length + 1:i + 1]
            if prefix == suffix:
                lps[i] = length
                break
    
    return lps


def main() -> None:
    """Demonstrate KMP algorithm."""
    
    print("=== KMP Algorithm Demo ===")
    
    pattern = "ABABCABAB"
    text = "ABABDABACDABABCABAB"
    
    kmp = KMPAlgorithm(pattern)
    
    print(f"Pattern: {pattern}")
    print(f"Text: {text}")
    
    # LPS array
    print(f"\n--- LPS Array ---")
    print(f"LPS array: {kmp.get_lps_array()}")
    
    # Verification with brute force
    brute_lps = compute_lps_brute_force(pattern)
    print(f"Brute force LPS: {brute_lps}")
    print(f"Match: {kmp.get_lps_array() == brute_lps}")
    
    # Search
    print(f"\n--- Search ---")
    occurrences = kmp.search(text)
    print(f"Pattern found at indices: {occurrences}")
    print(f"Number of occurrences: {len(occurrences)}")
    
    # First occurrence
    first = kmp.first_occurrence(text)
    print(f"First occurrence: {first}")
    
    # Contains
    print(f"Contains pattern: {kmp.contains(text)}")
    
    # Different patterns
    print("\n=== Different Patterns ===")
    
    test_cases = [
        ("AABA", "AABAACAADAABAAABAA"),
        ("ABC", "ABABABABABABC"),
        ("AAA", "AAAAAA"),
        ("AB", "CD")
    ]
    
    for pat, txt in test_cases:
        kmp_test = KMPAlgorithm(pat)
        occurrences = kmp_test.search(txt)
        print(f"Pattern '{pat}' in '{txt}': {occurrences}")
    
    # Wildcard support
    print("\n=== Wildcard Support ===")
    
    wildcard_pattern = "A*B*C"
    wildcard_kmp = KMPWithWildcards(wildcard_pattern, '*')
    
    wildcard_text = "AABBC"
    print(f"Pattern with wildcard: {wildcard_pattern}")
    print(f"Text: {wildcard_text}")
    print(f"Found: {wildcard_kmp.search(wildcard_text)}")
    
    # Count occurrences
    print("\n=== Count Occurrences ===")
    
    text2 = "ABABABABAB"
    pattern2 = "ABA"
    kmp2 = KMPAlgorithm(pattern2)
    
    count = kmp2.count_occurrences(text2)
    print(f"'{pattern2}' occurs {count} times in '{text2}'")
    
    # Performance comparison
    print("\n=== Performance Comparison ===")
    import time
    
    # Generate large text
    n = 100000
    large_text = "A" * n + "B" * n
    large_pattern = "A" * 100 + "B" * 100
    
    # KMP
    kmp_large = KMPAlgorithm(large_pattern)
    start = time.time()
    kmp_result = kmp_large.search(large_text)
    kmp_time = (time.time() - start) * 1000
    
    # Naive search
    start = time.time()
    naive_result = []
    for i in range(len(large_text) - len(large_pattern) + 1):
        if large_text[i:i+len(large_pattern)] == large_pattern:
            naive_result.append(i)
    naive_time = (time.time() - start) * 1000
    
    print(f"Text length: {len(large_text)}")
    print(f"Pattern length: {len(large_pattern)}")
    print(f"KMP time: {kmp_time:.2f}ms")
    print(f"Naive time: {naive_time:.2f}ms")
    print(f"Speedup: {naive_time/kmp_time:.2f}x")
    
    # Edge cases
    print("\n=== Edge Cases ===")
    
    # Empty pattern
    kmp_empty = KMPAlgorithm("")
    print(f"Empty pattern search: {kmp_empty.search(text)}")
    
    # Pattern longer than text
    kmp_long = KMPAlgorithm("ABCDEFGHIJKL")
    print(f"Long pattern search: {kmp_long.search(text)}")
    
    # Pattern not found
    kmp_not_found = KMPAlgorithm("XYZ")
    print(f"Not found pattern: {kmp_not_found.search(text)}")
    
    # Single character
    kmp_single = KMPAlgorithm("A")
    print(f"Single character 'A': {kmp_single.search(text)}")


if __name__ == "__main__":
    main()
