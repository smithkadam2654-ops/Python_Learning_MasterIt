"""
Rabin-Karp String Search - Rolling hash-based pattern matching.
Features: O(n+m) average time, multiple pattern search, and hash collision handling.
"""

from typing import List, Optional


class RabinKarp:
    """Rabin-Karp string search implementation."""
    
    def __init__(self, pattern: str, base: int = 256, prime: int = 101) -> None:
        """
        Initialize Rabin-Karp with pattern.
        
        Args:
            pattern: Pattern to search for
            base: Base for hash calculation
            prime: Prime number for modulo
        """
        self.pattern = pattern
        self.base = base
        self.prime = prime
        self.pattern_hash = self._calculate_hash(pattern)
        self.power = self._calculate_power(len(pattern))
    
    def _calculate_hash(self, s: str) -> int:
        """Calculate hash of string."""
        hash_value = 0
        for char in s:
            hash_value = (hash_value * self.base + ord(char)) % self.prime
        return hash_value
    
    def _calculate_power(self, length: int) -> int:
        """Calculate base^(length-1) % prime."""
        power = 1
        for _ in range(length - 1):
            power = (power * self.base) % self.prime
        return power
    
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
        text_hash = self._calculate_hash(text[:pattern_len])
        
        for i in range(text_len - pattern_len + 1):
            # Check hash match
            if text_hash == self.pattern_hash:
                # Verify actual match (handle collisions)
                if text[i:i + pattern_len] == self.pattern:
                    result.append(i)
            
            # Calculate rolling hash for next window
            if i < text_len - pattern_len:
                text_hash = self._recalculate_hash(
                    text_hash, text[i], text[i + pattern_len], pattern_len
                )
        
        return result
    
    def _recalculate_hash(self, old_hash: int, old_char: str, 
                         new_char: str, length: int) -> int:
        """Recalculate hash using rolling hash."""
        # Remove leading character
        hash_value = (old_hash - ord(old_char) * self.power) % self.prime
        # Ensure positive
        hash_value = (hash_value + self.prime) % self.prime
        # Add new character
        hash_value = (hash_value * self.base + ord(new_char)) % self.prime
        return hash_value
    
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


class RabinKarpMultiple:
    """Rabin-Karp for multiple pattern search."""
    
    def __init__(self, patterns: List[str], base: int = 256, prime: int = 101) -> None:
        """
        Initialize with multiple patterns.
        
        Args:
            patterns: List of patterns to search for
            base: Base for hash calculation
            prime: Prime number for modulo
        """
        self.patterns = patterns
        self.base = base
        self.prime = prime
        self.pattern_hashes = {pattern: self._calculate_hash(pattern) 
                              for pattern in patterns}
        self.max_length = max(len(p) for p in patterns) if patterns else 0
    
    def _calculate_hash(self, s: str) -> int:
        """Calculate hash of string."""
        hash_value = 0
        for char in s:
            hash_value = (hash_value * self.base + ord(char)) % self.prime
        return hash_value
    
    def search(self, text: str) -> dict:
        """
        Search for all patterns in text.
        
        Args:
            text: Text to search in
            
        Returns:
            Dictionary mapping pattern to list of indices
        """
        if not self.patterns or not text:
            return {}
        
        result = {pattern: [] for pattern in self.patterns}
        
        for pattern in self.patterns:
            pattern_len = len(pattern)
            if pattern_len > len(text):
                continue
            
            rk = RabinKarp(pattern, self.base, self.prime)
            occurrences = rk.search(text)
            result[pattern] = occurrences
        
        return result


class RabinKarpWithDoubleHash(RabinKarp):
    """Rabin-Karp with double hashing for collision reduction."""
    
    def __init__(self, pattern: str, base: int = 256, 
                 prime1: int = 101, prime2: int = 103) -> None:
        """
        Initialize with double hashing.
        
        Args:
            pattern: Pattern to search for
            base: Base for hash calculation
            prime1: First prime number
            prime2: Second prime number
        """
        self.pattern = pattern
        self.base = base
        self.prime1 = prime1
        self.prime2 = prime2
        self.pattern_hash1 = self._calculate_hash(pattern, prime1)
        self.pattern_hash2 = self._calculate_hash(pattern, prime2)
        self.power1 = self._calculate_power(len(pattern), prime1)
        self.power2 = self._calculate_power(len(pattern), prime2)
    
    def _calculate_hash(self, s: str, prime: int) -> int:
        """Calculate hash with given prime."""
        hash_value = 0
        for char in s:
            hash_value = (hash_value * self.base + ord(char)) % prime
        return hash_value
    
    def _calculate_power(self, length: int, prime: int) -> int:
        """Calculate base^(length-1) % prime."""
        power = 1
        for _ in range(length - 1):
            power = (power * self.base) % prime
        return power
    
    def search(self, text: str) -> List[int]:
        """Search with double hash verification."""
        if not self.pattern or not text:
            return []
        
        pattern_len = len(self.pattern)
        text_len = len(text)
        
        if pattern_len > text_len:
            return []
        
        result = []
        text_hash1 = self._calculate_hash(text[:pattern_len], self.prime1)
        text_hash2 = self._calculate_hash(text[:pattern_len], self.prime2)
        
        for i in range(text_len - pattern_len + 1):
            if (text_hash1 == self.pattern_hash1 and 
                text_hash2 == self.pattern_hash2):
                if text[i:i + pattern_len] == self.pattern:
                    result.append(i)
            
            if i < text_len - pattern_len:
                text_hash1 = self._recalculate_hash(
                    text_hash1, text[i], text[i + pattern_len], 
                    pattern_len, self.prime1, self.power1
                )
                text_hash2 = self._recalculate_hash(
                    text_hash2, text[i], text[i + pattern_len], 
                    pattern_len, self.prime2, self.power2
                )
        
        return result
    
    def _recalculate_hash(self, old_hash: int, old_char: str, new_char: str, 
                         length: int, prime: int, power: int) -> int:
        """Recalculate hash with given parameters."""
        hash_value = (old_hash - ord(old_char) * power) % prime
        hash_value = (hash_value + prime) % prime
        hash_value = (hash_value * self.base + ord(new_char)) % prime
        return hash_value


def main() -> None:
    """Demonstrate Rabin-Karp algorithm."""
    
    print("=== Rabin-Karp Search Demo ===")
    
    text = "ABAAABCDABAAABCDABAAABCD"
    pattern = "ABAAABCD"
    
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    
    # Basic Rabin-Karp
    print("\n--- Basic Rabin-Karp ---")
    rk = RabinKarp(pattern)
    occurrences = rk.search(text)
    print(f"Occurrences at: {occurrences}")
    print(f"Count: {rk.count_occurrences(text)}")
    print(f"First occurrence: {rk.first_occurrence(text)}")
    
    # Multiple patterns
    print("\n--- Multiple Patterns ---")
    patterns = ["ABA", "ABC", "ABCD"]
    rkm = RabinKarpMultiple(patterns)
    multi_result = rkm.search(text)
    for pat, occ in multi_result.items():
        print(f"'{pat}': {occ}")
    
    # Double hash
    print("\n--- Double Hash ---")
    rkdh = RabinKarpWithDoubleHash(pattern)
    occurrences_dh = rkdh.search(text)
    print(f"Occurrences at: {occurrences_dh}")
    
    # Different patterns
    print("\n--- Different Patterns ---")
    test_cases = [
        ("ABABABAB", "ABAB"),
        ("AAAAAAA", "AA"),
        ("ABCDEF", "XYZ"),
        ("HELLO WORLD", "LLO")
    ]
    
    for txt, pat in test_cases:
        rk_test = RabinKarp(pat)
        result = rk_test.search(txt)
        print(f"'{pat}' in '{txt}': {result}")
    
    # Performance comparison
    print("\n=== Performance Comparison ===")
    import time
    
    # Generate large text
    n = 1000000
    large_text = "A" * n + "B" * n
    large_pattern = "A" * 100 + "B" * 100
    
    # Rabin-Karp
    rk_large = RabinKarp(large_pattern)
    start = time.time()
    rk_result = rk_large.search(large_text)
    rk_time = (time.time() - start) * 1000
    
    # Double hash
    rkdh_large = RabinKarpWithDoubleHash(large_pattern)
    start = time.time()
    rkdh_result = rkdh_large.search(large_text)
    rkdh_time = (time.time() - start) * 1000
    
    # Naive search
    start = time.time()
    naive_result = []
    for i in range(len(large_text) - len(large_pattern) + 1):
        if large_text[i:i+len(large_pattern)] == large_pattern:
            naive_result.append(i)
    naive_time = (time.time() - start) * 1000
    
    print(f"Text length: {len(large_text)}")
    print(f"Pattern length: {len(large_pattern)}")
    print(f"Rabin-Karp: {rk_time:.2f}ms")
    print(f"Rabin-Karp (double hash): {rkdh_time:.2f}ms")
    print(f"Naive search: {naive_time:.2f}ms")
    print(f"Speedup (RK vs Naive): {naive_time/rk_time:.2f}x")
    
    # Edge cases
    print("\n--- Edge Cases ---")
    
    # Empty pattern
    rk_empty = RabinKarp("")
    print(f"Empty pattern: {rk_empty.search(text)}")
    
    # Empty text
    print(f"Empty text: {rk.search('')}")
    
    # Pattern longer than text
    rk_long = RabinKarp("ABCDEFGHIJKL")
    print(f"Pattern longer than text: {rk_long.search(text)}")
    
    # Single character
    rk_single = RabinKarp("A")
    print(f"Single character 'A': {rk_single.search(text)}")
    
    # Pattern not found
    rk_not_found = RabinKarp("XYZ")
    print(f"Pattern not found: {rk_not_found.search(text)}")


if __name__ == "__main__":
    main()
