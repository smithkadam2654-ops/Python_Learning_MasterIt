"""
Bloom Filter - Probabilistic data structure for membership testing.
Features: Space-efficient, false positives possible, no false negatives.
"""

import hashlib
from typing import List, Optional


class BloomFilter:
    """Bloom filter implementation."""
    
    def __init__(self, size: int, hash_count: int) -> None:
        """
        Initialize bloom filter.
        
        Args:
            size: Size of bit array
            hash_count: Number of hash functions
        """
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [False] * size
    
    def _hashes(self, item: str) -> List[int]:
        """
        Generate hash values for item.
        
        Args:
            item: Item to hash
            
        Returns:
            List of hash values
        """
        hashes = []
        
        # Use different hash algorithms
        algorithms = ['md5', 'sha1', 'sha256']
        
        for i in range(self.hash_count):
            # Combine item with index to create different hashes
            data = f"{item}{i}".encode()
            algo = algorithms[i % len(algorithms)]
            hash_obj = hashlib.new(algo)
            hash_obj.update(data)
            hash_value = int(hash_obj.hexdigest(), 16)
            hashes.append(hash_value % self.size)
        
        return hashes
    
    def add(self, item: str) -> None:
        """
        Add item to bloom filter.
        
        Args:
            item: Item to add
        """
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = True
    
    def contains(self, item: str) -> bool:
        """
        Check if item might be in filter.
        
        Args:
            item: Item to check
            
        Returns:
            True if possibly in set, False if definitely not
        """
        for hash_value in self._hashes(item):
            if not self.bit_array[hash_value]:
                return False
        return True
    
    def clear(self) -> None:
        """Clear bloom filter."""
        self.bit_array = [False] * self.size
    
    def count_bits_set(self) -> int:
        """Count number of bits set."""
        return sum(self.bit_array)
    
    def approximate_count(self) -> int:
        """
        Approximate number of items in filter.
        
        Returns:
            Approximate count
        """
        bits_set = self.count_bits_set()
        if bits_set == 0:
            return 0
        
        # Formula: - (m/n) * ln(1 - k/m)
        # where m = size, k = bits set, n = hash_count
        m = self.size
        k = bits_set
        n = self.hash_count
        
        return int(-(m / n) * (1 - k / m).__ln__())
    
    def __str__(self) -> str:
        """String representation."""
        return f"BloomFilter(size={self.size}, hash_count={self.hash_count}, bits_set={self.count_bits_set()})"


class CountingBloomFilter:
    """Counting bloom filter that supports deletion."""
    
    def __init__(self, size: int, hash_count: int) -> None:
        """
        Initialize counting bloom filter.
        
        Args:
            size: Size of counter array
            hash_count: Number of hash functions
        """
        self.size = size
        self.hash_count = hash_count
        self.counters = [0] * size
    
    def _hashes(self, item: str) -> List[int]:
        """Generate hash values for item."""
        import hashlib
        hashes = []
        
        for i in range(self.hash_count):
            data = f"{item}{i}".encode()
            hash_obj = hashlib.md5(data)
            hash_value = int(hash_obj.hexdigest(), 16)
            hashes.append(hash_value % self.size)
        
        return hashes
    
    def add(self, item: str) -> None:
        """Add item to filter."""
        for hash_value in self._hashes(item):
            self.counters[hash_value] += 1
    
    def remove(self, item: str) -> bool:
        """
        Remove item from filter.
        
        Args:
            item: Item to remove
            
        Returns:
            True if removed
        """
        for hash_value in self._hashes(item):
            if self.counters[hash_value] == 0:
                return False
            self.counters[hash_value] -= 1
        return True
    
    def contains(self, item: str) -> bool:
        """Check if item might be in filter."""
        for hash_value in self._hashes(item):
            if self.counters[hash_value] == 0:
                return False
        return True
    
    def clear(self) -> None:
        """Clear filter."""
        self.counters = [0] * self.size


def calculate_optimal_size(expected_items: int, false_positive_rate: float) -> int:
    """
    Calculate optimal size for bloom filter.
    
    Args:
        expected_items: Expected number of items
        false_positive_rate: Desired false positive rate
        
    Returns:
        Optimal size in bits
    """
    import math
    m = -(expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2)
    return int(m)


def calculate_optimal_hash_count(size: int, expected_items: int) -> int:
    """
    Calculate optimal number of hash functions.
    
    Args:
        size: Size of bit array
        expected_items: Expected number of items
        
    Returns:
        Optimal hash count
    """
    import math
    k = (size / expected_items) * math.log(2)
    return int(k)


def main() -> None:
    """Demonstrate bloom filter."""
    
    print("=== Bloom Filter Demo ===")
    
    # Create bloom filter
    size = 1000
    hash_count = 3
    bf = BloomFilter(size, hash_count)
    
    print(f"Bloom filter: {bf}")
    
    # Add items
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    for item in items:
        bf.add(item)
        print(f"Added: {item}")
    
    print(f"\nBloom filter after adds: {bf}")
    
    # Test membership
    print("\n--- Membership Tests ---")
    test_items = ["apple", "banana", "fig", "grape"]
    for item in test_items:
        result = bf.contains(item)
        print(f"'{item}' in filter: {result}")
    
    # False positive demonstration
    print("\n--- False Positive Test ---")
    # Add many items and test non-existent items
    bf2 = BloomFilter(10000, 7)
    
    for i in range(1000):
        bf2.add(f"item_{i}")
    
    false_positives = 0
    tests = 100
    
    for i in range(1000, 1000 + tests):
        if bf2.contains(f"item_{i}"):
            false_positives += 1
    
    print(f"False positives: {false_positives}/{tests} ({false_positives/tests:.2%})")
    
    # Counting bloom filter
    print("\n=== Counting Bloom Filter ===")
    cbf = CountingBloomFilter(100, 3)
    
    cbf.add("apple")
    cbf.add("banana")
    print(f"Added 'apple' and 'banana'")
    print(f"Contains 'apple': {cbf.contains('apple')}")
    print(f"Contains 'banana': {cbf.contains('banana')}")
    
    cbf.remove("apple")
    print(f"\nRemoved 'apple'")
    print(f"Contains 'apple': {cbf.contains('apple')}")
    print(f"Contains 'banana': {cbf.contains('banana')}")
    
    # Optimal parameters
    print("\n=== Optimal Parameters ===")
    expected_items = 1000
    desired_fpr = 0.01  # 1%
    
    optimal_size = calculate_optimal_size(expected_items, desired_fpr)
    optimal_hash_count = calculate_optimal_hash_count(optimal_size, expected_items)
    
    print(f"Expected items: {expected_items}")
    print(f"Desired false positive rate: {desired_fpr:.2%}")
    print(f"Optimal size: {optimal_size} bits")
    print(f"Optimal hash count: {optimal_hash_count}")
    
    # Create filter with optimal parameters
    optimal_bf = BloomFilter(optimal_size, optimal_hash_count)
    print(f"Optimal bloom filter: {optimal_bf}")


if __name__ == "__main__":
    main()
