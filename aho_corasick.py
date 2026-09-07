"""
Aho-Corasick Algorithm - Multi-pattern string matching.
Features: Trie-based automaton, failure links, and linear time search.
"""

from typing import List, Dict, Set, Optional
from collections import deque, defaultdict


class AhoCorasickNode:
    """Node in Aho-Corasick automaton."""
    
    def __init__(self) -> None:
        """Initialize node."""
        self.children: Dict[str, 'AhoCorasickNode'] = {}
        self.fail: Optional['AhoCorasickNode'] = None
        self.output: Set[str] = set()
        self.depth = 0


class AhoCorasick:
    """Aho-Corasick multi-pattern search implementation."""
    
    def __init__(self, patterns: List[str]) -> None:
        """
        Initialize Aho-Corasick with patterns.
        
        Args:
            patterns: List of patterns to search for
        """
        self.patterns = patterns
        self.root = AhoCorasickNode()
        self._build_trie()
        self._build_failure_links()
    
    def _build_trie(self) -> None:
        """Build trie from patterns."""
        for pattern in self.patterns:
            node = self.root
            for char in pattern:
                if char not in node.children:
                    node.children[char] = AhoCorasickNode()
                    node.children[char].depth = node.depth + 1
                node = node.children[char]
            node.output.add(pattern)
    
    def _build_failure_links(self) -> None:
        """Build failure links using BFS."""
        queue = deque()
        
        # Set fail of root's children to root
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)
        
        # BFS to set fail for all nodes
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                # Find fail state
                fail = current.fail
                while fail and char not in fail.children:
                    fail = fail.fail
                
                child.fail = fail.children[char] if fail else self.root
                
                # Merge outputs
                child.output.update(child.fail.output)
                
                queue.append(child)
    
    def search(self, text: str) -> Dict[str, List[int]]:
        """
        Search for all patterns in text.
        
        Args:
            text: Text to search in
            
        Returns:
            Dictionary mapping pattern to list of starting indices
        """
        result = defaultdict(list)
        node = self.root
        
        for i, char in enumerate(text):
            # Follow failure links if needed
            while node and char not in node.children:
                node = node.fail
            
            if not node:
                node = self.root
                continue
            
            node = node.children[char]
            
            # Report all patterns ending at this position
            for pattern in node.output:
                start_index = i - len(pattern) + 1
                result[pattern].append(start_index)
        
        return result
    
    def search_with_positions(self, text: str) -> List[tuple]:
        """
        Search and return all matches with positions.
        
        Args:
            text: Text to search in
            
        Returns:
            List of (pattern, start_index, end_index) tuples
        """
        result = []
        node = self.root
        
        for i, char in enumerate(text):
            while node and char not in node.children:
                node = node.fail
            
            if not node:
                node = self.root
                continue
            
            node = node.children[char]
            
            for pattern in node.output:
                start_index = i - len(pattern) + 1
                result.append((pattern, start_index, i))
        
        return result
    
    def count_occurrences(self, text: str) -> Dict[str, int]:
        """
        Count occurrences of each pattern.
        
        Args:
            text: Text to search in
            
        Returns:
            Dictionary mapping pattern to count
        """
        search_result = self.search(text)
        return {pattern: len(indices) for pattern, indices in search_result.items()}
    
    def has_match(self, text: str) -> bool:
        """
        Check if any pattern matches in text.
        
        Args:
            text: Text to search in
            
        Returns:
            True if any pattern found
        """
        node = self.root
        
        for char in text:
            while node and char not in node.children:
                node = node.fail
            
            if not node:
                node = self.root
                continue
            
            node = node.children[char]
            
            if node.output:
                return True
        
        return False


class AhoCorasickCaseInsensitive(AhoCorasick):
    """Case-insensitive Aho-Corasick."""
    
    def __init__(self, patterns: List[str]) -> None:
        """Initialize with case-insensitive patterns."""
        self.patterns = [p.lower() for p in patterns]
        self.root = AhoCorasickNode()
        self._build_trie()
        self._build_failure_links()
    
    def search(self, text: str) -> Dict[str, List[int]]:
        """Search case-insensitively."""
        return super().search(text.lower())


def main() -> None:
    """Demonstrate Aho-Corasick algorithm."""
    
    print("=== Aho-Corasick Search Demo ===")
    
    patterns = ["he", "she", "his", "hers"]
    text = "ushers"
    
    print(f"Patterns: {patterns}")
    print(f"Text: {text}")
    
    ac = AhoCorasick(patterns)
    
    # Basic search
    print("\n--- Basic Search ---")
    result = ac.search(text)
    for pattern, indices in result.items():
        print(f"'{pattern}': {indices}")
    
    # Search with positions
    print("\n--- Search with Positions ---")
    positions = ac.search_with_positions(text)
    for pattern, start, end in positions:
        print(f"'{pattern}' at [{start}:{end}]")
    
    # Count occurrences
    print("\n--- Count Occurrences ---")
    counts = ac.count_occurrences(text)
    for pattern, count in counts.items():
        print(f"'{pattern}': {count}")
    
    # Has match
    print(f"\n--- Has Match ---")
    print(f"Has 'he': {ac.has_match(text)}")
    print(f"Has 'xyz': {ac.has_match('xyz')}")
    
    # Case insensitive
    print("\n--- Case Insensitive ---")
    ac_ci = AhoCorasickCaseInsensitive(patterns)
    result_ci = ac_ci.search("UsHeRs")
    for pattern, indices in result_ci.items():
        print(f"'{pattern}': {indices}")
    
    # Multiple patterns in large text
    print("\n--- Large Text Search ---")
    large_patterns = ["error", "warning", "info", "debug"]
    large_text = "error: file not found\nwarning: low memory\ninfo: process started\ndebug: variable x=5\nerror: connection failed"
    
    ac_large = AhoCorasick(large_patterns)
    large_result = ac_large.search(large_text)
    for pattern, indices in large_result.items():
        print(f"'{pattern}': {indices}")
    
    # Performance comparison
    print("\n=== Performance Comparison ===")
    import time
    
    # Generate large text
    n = 100000
    large_text_gen = "A" * n + "B" * n + "C" * n
    patterns_gen = ["AAA", "BBB", "CCC", "ABC"]
    
    # Aho-Corasick
    ac_perf = AhoCorasick(patterns_gen)
    start = time.time()
    ac_result = ac_perf.search(large_text_gen)
    ac_time = (time.time() - start) * 1000
    
    # Naive search
    start = time.time()
    naive_result = defaultdict(list)
    for pattern in patterns_gen:
        for i in range(len(large_text_gen) - len(pattern) + 1):
            if large_text_gen[i:i+len(pattern)] == pattern:
                naive_result[pattern].append(i)
    naive_time = (time.time() - start) * 1000
    
    print(f"Text length: {len(large_text_gen)}")
    print(f"Patterns: {patterns_gen}")
    print(f"Aho-Corasick: {ac_time:.2f}ms")
    print(f"Naive search: {naive_time:.2f}ms")
    print(f"Speedup: {naive_time/ac_time:.2f}x")
    
    # Edge cases
    print("\n--- Edge Cases ---")
    
    # Empty patterns
    ac_empty = AhoCorasick([])
    print(f"Empty patterns: {ac_empty.search(text)}")
    
    # Empty text
    print(f"Empty text: {ac.search('')}")
    
    # Pattern not found
    ac_not_found = AhoCorasick(["xyz"])
    print(f"Pattern not found: {ac_not_found.search(text)}")
    
    # Single character patterns
    ac_single = AhoCorasick(["a", "b", "c"])
    print(f"Single chars in 'abc': {ac_single.search('abc')}")
    
    # Overlapping patterns
    ac_overlap = AhoCorasick(["ab", "abc", "bc"])
    print(f"Overlapping in 'abc': {ac_overlap.search('abc')}")


if __name__ == "__main__":
    main()
