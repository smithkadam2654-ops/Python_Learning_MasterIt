"""
Boyer-Moore String Search - Efficient pattern matching algorithm.
Features: Bad character heuristic, good suffix heuristic, and skip-based search.
"""

from typing import List, Optional, Dict


class BoyerMoore:
    """Boyer-Moore string search implementation."""
    
    def __init__(self, pattern: str) -> None:
        """
        Initialize Boyer-Moore with pattern.
        
        Args:
            pattern: Pattern to search for
        """
        self.pattern = pattern
        self.bad_char = self._build_bad_char_table()
    
    def _build_bad_char_table(self) -> Dict[str, int]:
        """Build bad character heuristic table."""
        table = {}
        length = len(self.pattern)
        
        for i in range(length - 1):
            table[self.pattern[i]] = length - 1 - i
        
        return table
    
    def search(self, text: str) -> List[int]:
        """
        Search for pattern in text.
        
        Args:
            text: Text to search in
            
        Returns:
            List of starting indices where pattern occurs
        """
        if not self.pattern or not text:
            return []
        
        pattern_len = len(self.pattern)
        text_len = len(text)
        
        if pattern_len > text_len:
            return []
        
        result = []
        i = 0  # Position in text
        
        while i <= text_len - pattern_len:
            j = pattern_len - 1  # Position in pattern
            
            # Match from right to left
            while j >= 0 and self.pattern[j] == text[i + j]:
                j -= 1
            
            if j < 0:
                # Pattern found
                result.append(i)
                # Shift using bad character rule
                if i + pattern_len < text_len:
                    char = text[i + pattern_len]
                    shift = self.bad_char.get(char, pattern_len)
                    i += shift
                else:
                    i += 1
            else:
                # Mismatch, use bad character rule
                char = text[i + j]
                shift = self.bad_char.get(char, pattern_len)
                i += max(1, shift - (pattern_len - 1 - j))
        
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
    
    def first_occurrence(self, text: str) -> Optional[int]:
        """
        Find first occurrence of pattern.
        
        Args:
            text: Text to search in
            
        Returns:
            Index of first occurrence or None
        """
        occurrences = self.search(text)
        return occurrences[0] if occurrences else None


class BoyerMooreHorspool(BoyerMoore):
    """Simplified Boyer-Moore-Horspool algorithm."""
    
    def _build_bad_char_table(self) -> Dict[str, int]:
        """Build bad character table (Horspool variant)."""
        table = {}
        pattern_len = len(self.pattern)
        
        for i in range(pattern_len - 1):
            table[self.pattern[i]] = pattern_len - 1 - i
        
        # Default shift is pattern length
        return table
    
    def search(self, text: str) -> List[int]:
        """Search using Horspool variant."""
        if not self.pattern or not text:
            return []
        
        pattern_len = len(self.pattern)
        text_len = len(text)
        
        if pattern_len > text_len:
            return []
        
        result = []
        i = 0
        
        while i <= text_len - pattern_len:
            j = pattern_len - 1
            
            while j >= 0 and self.pattern[j] == text[i + j]:
                j -= 1
            
            if j < 0:
                result.append(i)
                # Shift by pattern length
                char = text[i + pattern_len] if i + pattern_len < text_len else None
                shift = self.bad_char.get(char, pattern_len) if char else 1
                i += shift
            else:
                # Shift based on mismatched character
                char = text[i + pattern_len - 1]
                shift = self.bad_char.get(char, pattern_len)
                i += shift
        
        return result


class BoyerMooreWithGoodSuffix(BoyerMoore):
    """Boyer-Moore with good suffix heuristic."""
    
    def __init__(self, pattern: str) -> None:
        """Initialize with good suffix table."""
        super().__init__(pattern)
        self.good_suffix = self._build_good_suffix_table()
    
    def _build_good_suffix_table(self) -> List[int]:
        """Build good suffix heuristic table."""
        pattern_len = len(self.pattern)
        good_suffix = [0] * (pattern_len + 1)
        
        # Case 1: Matching suffix appears elsewhere in pattern
        for i in range(pattern_len):
            j = pattern_len - 1
            while j >= 0 and (pattern_len - 1 - i) < pattern_len - j:
                if self.pattern[j] == self.pattern[j - (pattern_len - 1 - i)]:
                    good_suffix[i] = pattern_len - 1 - j
                    break
                j -= 1
        
        # Case 2: Partial match of suffix
        for i in range(pattern_len):
            j = pattern_len - 1
            while j >= 0:
                if self.pattern[j] != self.pattern[j - i]:
                    break
                j -= 1
            if j < 0:
                good_suffix[i] = i + 1
        
        return good_suffix
    
    def search(self, text: str) -> List[int]:
        """Search with both heuristics."""
        if not self.pattern or not text:
            return []
        
        pattern_len = len(self.pattern)
        text_len = len(text)
        
        if pattern_len > text_len:
            return []
        
        result = []
        i = 0
        
        while i <= text_len - pattern_len:
            j = pattern_len - 1
            
            while j >= 0 and self.pattern[j] == text[i + j]:
                j -= 1
            
            if j < 0:
                result.append(i)
                i += 1
            else:
                # Use both heuristics
                bad_char_shift = self.bad_char.get(text[i + j], pattern_len)
                good_suffix_shift = self.good_suffix[j]
                i += max(bad_char_shift - (pattern_len - 1 - j), good_suffix_shift)
        
        return result


def main() -> None:
    """Demonstrate Boyer-Moore algorithm."""
    
    print("=== Boyer-Moore Search Demo ===")
    
    text = "ABAAABCDABAAABCDABAAABCD"
    pattern = "ABAAABCD"
    
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    
    # Basic Boyer-Moore
    print("\n--- Boyer-Moore ---")
    bm = BoyerMoore(pattern)
    occurrences = bm.search(text)
    print(f"Occurrences at: {occurrences}")
    print(f"Count: {bm.count_occurrences(text)}")
    print(f"First occurrence: {bm.first_occurrence(text)}")
    
    # Boyer-Moore-Horspool
    print("\n--- Boyer-Moore-Horspool ---")
    bmh = BoyerMooreHorspool(pattern)
    occurrences_h = bmh.search(text)
    print(f"Occurrences at: {occurrences_h}")
    
    # With good suffix
    print("\n--- Boyer-Moore with Good Suffix ---")
    bmgs = BoyerMooreWithGoodSuffix(pattern)
    occurrences_gs = bmgs.search(text)
    print(f"Occurrences at: {occurrences_gs}")
    
    # Different patterns
    print("\n--- Different Patterns ---")
    test_cases = [
        ("ABABABAB", "ABAB"),
        ("AAAAAAA", "AA"),
        ("ABCDEF", "XYZ"),
        ("HELLO WORLD", "LLO")
    ]
    
    for txt, pat in test_cases:
        bm_test = BoyerMoore(pat)
        result = bm_test.search(txt)
        print(f"'{pat}' in '{txt}': {result}")
    
    # Performance comparison
    print("\n=== Performance Comparison ===")
    import time
    
    # Generate large text
    n = 1000000
    large_text = "A" * n + "B" * n
    large_pattern = "A" * 100 + "B" * 100
    
    # Boyer-Moore
    bm_large = BoyerMoore(large_pattern)
    start = time.time()
    bm_result = bm_large.search(large_text)
    bm_time = (time.time() - start) * 1000
    
    # Boyer-Moore-Horspool
    bmh_large = BoyerMooreHorspool(large_pattern)
    start = time.time()
    bmh_result = bmh_large.search(large_text)
    bmh_time = (time.time() - start) * 1000
    
    # Naive search
    start = time.time()
    naive_result = []
    for i in range(len(large_text) - len(large_pattern) + 1):
        if large_text[i:i+len(large_pattern)] == large_pattern:
            naive_result.append(i)
    naive_time = (time.time() - start) * 1000
    
    print(f"Text length: {len(large_text)}")
    print(f"Pattern length: {len(large_pattern)}")
    print(f"Boyer-Moore: {bm_time:.2f}ms")
    print(f"Boyer-Moore-Horspool: {bmh_time:.2f}ms")
    print(f"Naive search: {naive_time:.2f}ms")
    print(f"Speedup (BM vs Naive): {naive_time/bm_time:.2f}x")
    
    # Edge cases
    print("\n--- Edge Cases ---")
    
    # Empty pattern
    bm_empty = BoyerMoore("")
    print(f"Empty pattern: {bm_empty.search(text)}")
    
    # Empty text
    print(f"Empty text: {bm.search('')}")
    
    # Pattern longer than text
    bm_long = BoyerMoore("ABCDEFGHIJKL")
    print(f"Pattern longer than text: {bm_long.search(text)}")
    
    # Single character
    bm_single = BoyerMoore("A")
    print(f"Single character 'A': {bm_single.search(text)}")
    
    # Pattern not found
    bm_not_found = BoyerMoore("XYZ")
    print(f"Pattern not found: {bm_not_found.search(text)}")


if __name__ == "__main__":
    main()
