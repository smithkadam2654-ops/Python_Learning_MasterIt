"""
Suffix Array - Data structure for string processing.
Features: Efficient pattern matching, substring search, and string analysis.
"""

from typing import List, Tuple, Optional


class SuffixArray:
    """Suffix array implementation."""
    
    def __init__(self, text: str) -> None:
        """
        Initialize suffix array.
        
        Args:
            text: Input string
        """
        self.text = text
        self.suffixes = self._build_suffix_array()
    
    def _build_suffix_array(self) -> List[int]:
        """
        Build suffix array using sorting.
        
        Returns:
            List of suffix indices in sorted order
        """
        n = len(self.text)
        suffixes = []
        
        # Create suffixes with their starting indices
        for i in range(n):
            suffixes.append((self.text[i:], i))
        
        # Sort suffixes
        suffixes.sort(key=lambda x: x[0])
        
        # Extract indices
        return [suffix[1] for suffix in suffixes]
    
    def get_suffix_array(self) -> List[int]:
        """Get suffix array."""
        return self.suffixes
    
    def search(self, pattern: str) -> List[int]:
        """
        Search for pattern using binary search on suffix array.
        
        Args:
            pattern: Pattern to search
            
        Returns:
            List of starting indices where pattern occurs
        """
        n = len(self.text)
        m = len(pattern)
        
        if m == 0 or m > n:
            return []
        
        # Binary search for leftmost occurrence
        left = 0
        right = n - 1
        
        while left <= right:
            mid = (left + right) // 2
            suffix = self.text[self.suffixes[mid]:]
            
            # Compare pattern with suffix
            cmp = self._compare(pattern, suffix)
            
            if cmp == 0:
                # Found, find leftmost
                while mid > 0 and self._compare(pattern, self.text[self.suffixes[mid - 1]:]) == 0:
                    mid -= 1
                break
            elif cmp < 0:
                right = mid - 1
            else:
                left = mid + 1
        
        if left > right:
            return []
        
        # Collect all occurrences
        result = []
        i = mid
        while i < n and self._compare(pattern, self.text[self.suffixes[i]:]) == 0:
            result.append(self.suffixes[i])
            i += 1
        
        return result
    
    def _compare(self, pattern: str, suffix: str) -> int:
        """
        Compare pattern with suffix.
        
        Args:
            pattern: Pattern string
            suffix: Suffix string
            
        Returns:
            -1 if pattern < suffix, 0 if equal, 1 if pattern > suffix
        """
        min_len = min(len(pattern), len(suffix))
        
        for i in range(min_len):
            if pattern[i] < suffix[i]:
                return -1
            elif pattern[i] > suffix[i]:
                return 1
        
        if len(pattern) < len(suffix):
            return -1
        elif len(pattern) > len(suffix):
            return 1
        
        return 0
    
    def count_occurrences(self, pattern: str) -> int:
        """
        Count occurrences of pattern.
        
        Args:
            pattern: Pattern to count
            
        Returns:
            Number of occurrences
        """
        return len(self.search(pattern))
    
    def longest_repeated_substring(self) -> Optional[str]:
        """
        Find longest repeated substring.
        
        Returns:
            Longest repeated substring or None
        """
        n = len(self.text)
        if n == 0:
            return None
        
        max_len = 0
        result = ""
        
        for i in range(n - 1):
            # Compare adjacent suffixes
            suffix1 = self.text[self.suffixes[i]:]
            suffix2 = self.text[self.suffixes[i + 1]:]
            
            # Find common prefix
            common_len = 0
            min_len = min(len(suffix1), len(suffix2))
            
            for j in range(min_len):
                if suffix1[j] == suffix2[j]:
                    common_len += 1
                else:
                    break
            
            if common_len > max_len:
                max_len = common_len
                result = suffix1[:common_len]
        
        return result if result else None
    
    def longest_common_prefix(self, i: int, j: int) -> int:
        """
        Find LCP of suffixes at indices i and j.
        
        Args:
            i: First suffix index
            j: Second suffix index
            
        Returns:
            Length of longest common prefix
        """
        suffix1 = self.text[self.suffixes[i]:]
        suffix2 = self.text[self.suffixes[j]:]
        
        common_len = 0
        min_len = min(len(suffix1), len(suffix2))
        
        for k in range(min_len):
            if suffix1[k] == suffix2[k]:
                common_len += 1
            else:
                break
        
        return common_len
    
    def get_suffix(self, index: int) -> str:
        """
        Get suffix at index in original text.
        
        Args:
            index: Starting index
            
        Returns:
            Suffix string
        """
        return self.text[index:]
    
    def __str__(self) -> str:
        """String representation."""
        return f"SuffixArray(text='{self.text[:20]}...', n={len(self.text)})"


class SuffixArrayWithLCP(SuffixArray):
    """Suffix array with LCP (Longest Common Prefix) array."""
    
    def __init__(self, text: str) -> None:
        """
        Initialize suffix array with LCP.
        
        Args:
            text: Input string
        """
        super().__init__(text)
        self.lcp_array = self._build_lcp_array()
    
    def _build_lcp_array(self) -> List[int]:
        """
        Build LCP array.
        
        Returns:
            LCP array where LCP[i] = LCP of suffixes at SA[i] and SA[i-1]
        """
        n = len(self.text)
        lcp = [0] * n
        
        for i in range(1, n):
            lcp[i] = self.longest_common_prefix(i, i - 1)
        
        return lcp
    
    def get_lcp_array(self) -> List[int]:
        """Get LCP array."""
        return self.lcp_array
    
    def count_distinct_substrings(self) -> int:
        """
        Count distinct substrings.
        
        Returns:
            Number of distinct substrings
        """
        n = len(self.text)
        total = n * (n + 1) // 2  # Total possible substrings
        
        # Subtract LCP values
        lcp_sum = sum(self.lcp_array)
        
        return total - lcp_sum


def main() -> None:
    """Demonstrate suffix array."""
    
    print("=== Suffix Array Demo ===")
    
    text = "banana"
    sa = SuffixArray(text)
    
    print(f"Text: {text}")
    print(f"Suffix array: {sa.get_suffix_array()}")
    
    # Show all suffixes
    print("\n--- All Suffixes ---")
    for i, idx in enumerate(sa.get_suffix_array()):
        print(f"{i}: [{idx}] {sa.get_suffix(idx)}")
    
    # Search
    print("\n--- Search ---")
    patterns = ["ana", "nan", "ban", "xyz"]
    for pattern in patterns:
        occurrences = sa.search(pattern)
        print(f"'{pattern}': {occurrences} (count: {len(occurrences)})")
    
    # Count occurrences
    print(f"\n--- Count Occurrences ---")
    print(f"'ana' occurs {sa.count_occurrences('ana')} times")
    print(f"'a' occurs {sa.count_occurrences('a')} times")
    
    # Longest repeated substring
    print(f"\n--- Longest Repeated Substring ---")
    lrs = sa.longest_repeated_substring()
    print(f"Longest repeated substring: {lrs}")
    
    # LCP
    print(f"\n--- Longest Common Prefix ---")
    print(f"LCP of suffixes 0 and 1: {sa.longest_common_prefix(0, 1)}")
    print(f"LCP of suffixes 1 and 2: {sa.longest_common_prefix(1, 2)}")
    
    # Suffix array with LCP
    print("\n=== Suffix Array with LCP ===")
    sa_lcp = SuffixArrayWithLCP(text)
    
    print(f"LCP array: {sa_lcp.get_lcp_array()}")
    print(f"Distinct substrings: {sa_lcp.count_distinct_substrings()}")
    
    # Different text
    print("\n=== Different Text ===")
    text2 = "mississippi"
    sa2 = SuffixArray(text2)
    
    print(f"Text: {text2}")
    print(f"Suffix array: {sa2.get_suffix_array()}")
    
    lrs2 = sa2.longest_repeated_substring()
    print(f"Longest repeated substring: {lrs2}")
    
    # Pattern matching
    print(f"\n--- Pattern Matching ---")
    pattern = "iss"
    occurrences = sa2.search(pattern)
    print(f"'{pattern}' found at: {occurrences}")
    
    # Performance test
    print("\n=== Performance Test ===")
    import time
    import random
    
    # Generate random string
    n = 10000
    chars = "abcdefghijklmnopqrstuvwxyz"
    random_text = ''.join(random.choice(chars) for _ in range(n))
    
    start = time.time()
    large_sa = SuffixArray(random_text)
    build_time = (time.time() - start) * 1000
    
    print(f"Built suffix array for {n} characters in {build_time:.2f}ms")
    
    # Search performance
    pattern = random_text[:10]
    start = time.time()
    occurrences = large_sa.search(pattern)
    search_time = (time.time() - start) * 1000
    
    print(f"Search for pattern in {search_time:.4f}ms")
    print(f"Found {len(occurrences)} occurrences")


if __name__ == "__main__":
    main()
