"""
Hash Map / Hash Table - Hash table implementation and operations.
Features: Hash table with collision handling, rehashing, and common operations.
"""

from typing import List, Optional, TypeVar, Generic
from collections import defaultdict

T = TypeVar('T')
V = TypeVar('V')


class HashMap:
    """Hash map implementation with separate chaining."""
    
    def __init__(self, capacity: int = 16, load_factor: float = 0.75) -> None:
        """
        Initialize hash map.
        
        Args:
            capacity: Initial capacity
            load_factor: Load factor for rehashing
        """
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets: List[List[tuple]] = [[] for _ in range(capacity)]
    
    def _hash(self, key: T) -> int:
        """Calculate hash for key."""
        return hash(key) % self.capacity
    
    def put(self, key: T, value: V) -> None:
        """
        Put key-value pair into hash map.
        
        Args:
            key: Key
            value: Value
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Update if key exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Add new key-value pair
        bucket.append((key, value))
        self.size += 1
        
        # Rehash if needed
        if self.size / self.capacity > self.load_factor:
            self._rehash()
    
    def get(self, key: T) -> Optional[V]:
        """
        Get value for key.
        
        Args:
            key: Key
            
        Returns:
            Value or None if not found
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return None
    
    def remove(self, key: T) -> bool:
        """
        Remove key-value pair.
        
        Args:
            key: Key to remove
            
        Returns:
            True if removed, False if not found
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        
        return False
    
    def contains_key(self, key: T) -> bool:
        """
        Check if key exists.
        
        Args:
            key: Key to check
            
        Returns:
            True if key exists
        """
        return self.get(key) is not None
    
    def keys(self) -> List[T]:
        """Get all keys."""
        return [k for bucket in self.buckets for k, v in bucket]
    
    def values(self) -> List[V]:
        """Get all values."""
        return [v for bucket in self.buckets for k, v in bucket]
    
    def items(self) -> List[tuple]:
        """Get all key-value pairs."""
        return [(k, v) for bucket in self.buckets for k, v in bucket]
    
    def _rehash(self) -> None:
        """Rehash all entries to new capacity."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        
        for bucket in old_buckets:
            for k, v in bucket:
                self.put(k, v)
    
    def __len__(self) -> int:
        """Get size."""
        return self.size
    
    def __repr__(self) -> str:
        return f"HashMap({dict(self.items())})"


class HashSet:
    """Hash set implementation."""
    
    def __init__(self, capacity: int = 16, load_factor: float = 0.75) -> None:
        """
        Initialize hash set.
        
        Args:
            capacity: Initial capacity
            load_factor: Load factor for rehashing
        """
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets: List[List[T]] = [[] for _ in range(capacity)]
    
    def _hash(self, item: T) -> int:
        """Calculate hash for item."""
        return hash(item) % self.capacity
    
    def add(self, item: T) -> bool:
        """
        Add item to set.
        
        Args:
            item: Item to add
            
        Returns:
            True if added, False if already exists
        """
        index = self._hash(item)
        bucket = self.buckets[index]
        
        if item in bucket:
            return False
        
        bucket.append(item)
        self.size += 1
        
        if self.size / self.capacity > self.load_factor:
            self._rehash()
        
        return True
    
    def remove(self, item: T) -> bool:
        """
        Remove item from set.
        
        Args:
            item: Item to remove
            
        Returns:
            True if removed, False if not found
        """
        index = self._hash(item)
        bucket = self.buckets[index]
        
        if item in bucket:
            bucket.remove(item)
            self.size -= 1
            return True
        
        return False
    
    def contains(self, item: T) -> bool:
        """
        Check if item exists in set.
        
        Args:
            item: Item to check
            
        Returns:
            True if item exists
        """
        index = self._hash(item)
        return item in self.buckets[index]
    
    def _rehash(self) -> None:
        """Rehash all entries to new capacity."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        
        for bucket in old_buckets:
            for item in bucket:
                self.add(item)
    
    def __len__(self) -> int:
        """Get size."""
        return self.size
    
    def __contains__(self, item: T) -> bool:
        """Check if item in set."""
        return self.contains(item)
    
    def __repr__(self) -> str:
        return f"HashSet({set().union(*self.buckets)})"


class HashAlgorithms:
    """Hash-based algorithm implementations."""
    
    @staticmethod
    def two_sum(nums: List[int], target: int) -> Optional[List[int]]:
        """
        Find two numbers that sum to target using hash map.
        
        Args:
            nums: List of numbers
            target: Target sum
            
        Returns:
            Indices of two numbers or None
        """
        seen = {}
        
        for i, num in enumerate(nums):
            complement = target - num
            
            if complement in seen:
                return [seen[complement], i]
            
            seen[num] = i
        
        return None
    
    @staticmethod
    def group_anagrams(strs: List[str]) -> List[List[str]]:
        """
        Group anagrams using hash map.
        
        Args:
            strs: List of strings
            
        Returns:
            List of anagram groups
        """
        groups = defaultdict(list)
        
        for s in strs:
            # Use sorted string as key
            key = ''.join(sorted(s))
            groups[key].append(s)
        
        return list(groups.values())
    
    @staticmethod
    def longest_consecutive_sequence(nums: List[int]) -> int:
        """
        Find longest consecutive sequence using hash set.
        
        Args:
            nums: List of numbers
            
        Returns:
            Length of longest consecutive sequence
        """
        num_set = set(nums)
        max_length = 0
        
        for num in num_set:
            # Only start if it's the beginning of sequence
            if num - 1 not in num_set:
                current_num = num
                current_length = 1
                
                while current_num + 1 in num_set:
                    current_num += 1
                    current_length += 1
                
                max_length = max(max_length, current_length)
        
        return max_length
    
    @staticmethod
    def subarray_sum(nums: List[int], k: int) -> int:
        """
        Count subarrays with sum k using hash map.
        
        Args:
            nums: List of numbers
            k: Target sum
            
        Returns:
            Count of subarrays
        """
        count = 0
        prefix_sum = 0
        prefix_counts = defaultdict(int)
        prefix_counts[0] = 1
        
        for num in nums:
            prefix_sum += num
            
            if prefix_sum - k in prefix_counts:
                count += prefix_counts[prefix_sum - k]
            
            prefix_counts[prefix_sum] += 1
        
        return count
    
    @staticmethod
    def find_duplicate(nums: List[int]) -> int:
        """
        Find duplicate number using Floyd's cycle detection (hash-based).
        
        Args:
            nums: Array with n+1 integers from 1 to n
            
        Returns:
            Duplicate number
        """
        seen = set()
        
        for num in nums:
            if num in seen:
                return num
            seen.add(num)
        
        return -1
    
    @staticmethod
    def single_number(nums: List[int]) -> int:
        """
        Find single number using hash map (every other appears twice).
        
        Args:
            nums: List of numbers
            
        Returns:
            Single number
        """
        counts = defaultdict(int)
        
        for num in nums:
            counts[num] += 1
        
        for num, count in counts.items():
            if count == 1:
                return num
        
        return -1
    
    @staticmethod
    def first_repeating_char(s: str) -> Optional[str]:
        """
        Find first repeating character using hash map.
        
        Args:
            s: Input string
            
        Returns:
            First repeating character or None
        """
        seen = {}
        
        for i, char in enumerate(s):
            if char in seen:
                return char
            seen[char] = i
        
        return None
    
    @staticmethod
    def first_non_repeating_char(s: str) -> Optional[str]:
        """
        Find first non-repeating character using hash map.
        
        Args:
            s: Input string
            
        Returns:
            First non-repeating character or None
        """
        counts = defaultdict(int)
        
        for char in s:
            counts[char] += 1
        
        for char in s:
            if counts[char] == 1:
                return char
        
        return None
    
    @staticmethod
    def is_isomorphic(s: str, t: str) -> bool:
        """
        Check if two strings are isomorphic using hash maps.
        
        Args:
            s: First string
            t: Second string
            
        Returns:
            True if isomorphic
        """
        if len(s) != len(t):
            return False
        
        s_to_t = {}
        t_to_s = {}
        
        for char_s, char_t in zip(s, t):
            if char_s in s_to_t:
                if s_to_t[char_s] != char_t:
                    return False
            else:
                s_to_t[char_s] = char_t
            
            if char_t in t_to_s:
                if t_to_s[char_t] != char_s:
                    return False
            else:
                t_to_s[char_t] = char_s
        
        return True
    
    @staticmethod
    def word_pattern(pattern: str, s: str) -> bool:
        """
        Check if string follows word pattern using hash map.
        
        Args:
            pattern: Pattern string
            s: String of words
            
        Returns:
            True if follows pattern
        """
        words = s.split()
        
        if len(pattern) != len(words):
            return False
        
        char_to_word = {}
        word_to_char = {}
        
        for char, word in zip(pattern, words):
            if char in char_to_word:
                if char_to_word[char] != word:
                    return False
            else:
                char_to_word[char] = word
            
            if word in word_to_char:
                if word_to_char[word] != char:
                    return False
            else:
                word_to_char[word] = char
        
        return True
    
    @staticmethod
    def ransom_note(ransom_note: str, magazine: str) -> bool:
        """
        Check if ransom note can be constructed from magazine using hash map.
        
        Args:
            ransom_note: Ransom note text
            magazine: Magazine text
            
        Returns:
            True if constructible
        """
        from collections import Counter
        
        ransom_counts = Counter(ransom_note)
        magazine_counts = Counter(magazine)
        
        for char, count in ransom_counts.items():
            if magazine_counts[char] < count:
                return False
        
        return True
    
    @staticmethod
    def top_k_frequent(nums: List[int], k: int) -> List[int]:
        """
        Find k most frequent elements using hash map.
        
        Args:
            nums: List of numbers
            k: Number of most frequent elements
            
        Returns:
            List of k most frequent elements
        """
        from collections import Counter
        
        counts = Counter(nums)
        return [item for item, _ in counts.most_common(k)]


def main() -> None:
    """Demonstrate hash map operations."""
    
    print("=== Hash Map Demo ===")
    
    # HashMap
    print("\n--- HashMap ---")
    hm = HashMap()
    hm.put("name", "Alice")
    hm.put("age", 25)
    hm.put("city", "NYC")
    
    print(f"HashMap: {hm}")
    print(f"Get 'name': {hm.get('name')}")
    print(f"Contains 'age': {hm.contains_key('age')}")
    print(f"Keys: {hm.keys()}")
    print(f"Values: {hm.values()}")
    
    hm.remove("age")
    print(f"After removing 'age': {hm}")
    
    # HashSet
    print("\n--- HashSet ---")
    hs = HashSet()
    hs.add(1)
    hs.add(2)
    hs.add(3)
    hs.add(2)  # Duplicate
    
    print(f"HashSet: {hs}")
    print(f"Contains 2: {hs.contains(2)}")
    print(f"Size: {len(hs)}")
    
    hs.remove(2)
    print(f"After removing 2: {hs}")
    
    # Two sum
    print("\n--- Two Sum ---")
    nums = [2, 7, 11, 15]
    target = 9
    print(f"Array: {nums}, target: {target}")
    print(f"Indices: {HashAlgorithms.two_sum(nums, target)}")
    
    # Group anagrams
    print("\n--- Group Anagrams ---")
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"Strings: {strs}")
    print(f"Groups: {HashAlgorithms.group_anagrams(strs)}")
    
    # Longest consecutive sequence
    print("\n--- Longest Consecutive Sequence ---")
    nums = [100, 4, 200, 1, 3, 2]
    print(f"Array: {nums}")
    print(f"Longest: {HashAlgorithms.longest_consecutive_sequence(nums)}")
    
    # Subarray sum
    print("\n--- Subarray Sum ---")
    nums = [1, 1, 1]
    k = 2
    print(f"Array: {nums}, k: {k}")
    print(f"Count: {HashAlgorithms.subarray_sum(nums, k)}")
    
    # First repeating/non-repeating
    print("\n--- Character Analysis ---")
    s = "swiss"
    print(f"String: '{s}'")
    print(f"First repeating: {HashAlgorithms.first_repeating_char(s)}")
    print(f"First non-repeating: {HashAlgorithms.first_non_repeating_char(s)}")
    
    # Isomorphic strings
    print("\n--- Isomorphic Strings ---")
    s1, s2 = "egg", "add"
    print(f"'{s1}' and '{s2}': {HashAlgorithms.is_isomorphic(s1, s2)}")
    
    # Word pattern
    print("\n--- Word Pattern ---")
    pattern = "abba"
    s = "dog cat cat dog"
    print(f"Pattern: '{pattern}', string: '{s}'")
    print(f"Matches: {HashAlgorithms.word_pattern(pattern, s)}")
    
    # Ransom note
    print("\n--- Ransom Note ---")
    ransom = "aa"
    magazine = "aab"
    print(f"Ransom: '{ransom}', Magazine: '{magazine}'")
    print(f"Can construct: {HashAlgorithms.ransom_note(ransom, magazine)}")
    
    # Top k frequent
    print("\n--- Top K Frequent ---")
    nums = [1, 1, 1, 2, 2, 3]
    k = 2
    print(f"Array: {nums}, k: {k}")
    print(f"Top {k}: {HashAlgorithms.top_k_frequent(nums, k)}")


if __name__ == "__main__":
    main()
