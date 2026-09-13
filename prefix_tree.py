"""
Prefix Tree (Trie) - Tree-like data structure for storing strings.
Features: Insert, search, prefix search, autocomplete, and word suggestions.
"""

from typing import List, Optional, Dict


class TrieNode:
    """Trie node implementation."""
    
    def __init__(self) -> None:
        """Initialize trie node."""
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word = False
        self.word_count = 0
    
    def __repr__(self) -> str:
        return f"TrieNode(end={self.is_end_of_word}, children={len(self.children)})"


class PrefixTree:
    """Prefix tree (Trie) implementation."""
    
    def __init__(self) -> None:
        """Initialize empty prefix tree."""
        self.root = TrieNode()
        self.size = 0
    
    def insert(self, word: str) -> None:
        """
        Insert word into trie.
        
        Args:
            word: Word to insert
        """
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_end_of_word:
            node.is_end_of_word = True
            self.size += 1
        
        node.word_count += 1
    
    def search(self, word: str) -> bool:
        """
        Search for exact word in trie.
        
        Args:
            word: Word to search
            
        Returns:
            True if word exists
        """
        node = self._find_node(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word starts with prefix.
        
        Args:
            prefix: Prefix to check
            
        Returns:
            True if prefix exists
        """
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Find node corresponding to prefix."""
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def count_words_with_prefix(self, prefix: str) -> int:
        """
        Count words starting with prefix.
        
        Args:
            prefix: Prefix to count
            
        Returns:
            Number of words with prefix
        """
        node = self._find_node(prefix)
        
        if node is None:
            return 0
        
        return self._count_words(node)
    
    def _count_words(self, node: TrieNode) -> int:
        """Count words from given node."""
        count = node.word_count if node.is_end_of_word else 0
        
        for child in node.children.values():
            count += self._count_words(child)
        
        return count
    
    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """
        Get all words starting with prefix.
        
        Args:
            prefix: Prefix to search
            
        Returns:
            List of words with prefix
        """
        node = self._find_node(prefix)
        
        if node is None:
            return []
        
        words = []
        self._collect_words(node, prefix, words)
        
        return words
    
    def _collect_words(self, node: TrieNode, current: str, words: List[str]) -> None:
        """Collect all words from given node."""
        if node.is_end_of_word:
            words.append(current)
        
        for char, child in node.children.items():
            self._collect_words(child, current + char, words)
    
    def delete(self, word: str) -> bool:
        """
        Delete word from trie.
        
        Args:
            word: Word to delete
            
        Returns:
            True if deleted, False if not found
        """
        if not self.search(word):
            return False
        
        nodes = [self.root]
        
        for char in word:
            nodes.append(nodes[-1].children[char])
        
        # Remove word end marker
        nodes[-1].is_end_of_word = False
        nodes[-1].word_count -= 1
        self.size -= 1
        
        # Remove unused nodes
        for i in range(len(word), 0, -1):
            if not nodes[i].children and not nodes[i].is_end_of_word:
                del nodes[i - 1].children[word[i - 1]]
            else:
                break
        
        return True
    
    def autocomplete(self, prefix: str, limit: int = 5) -> List[str]:
        """
        Get autocomplete suggestions for prefix.
        
        Args:
            prefix: Prefix to autocomplete
            limit: Maximum number of suggestions
            
        Returns:
            List of suggested words
        """
        words = self.get_words_with_prefix(prefix)
        return words[:limit]
    
    def get_all_words(self) -> List[str]:
        """
        Get all words in trie.
        
        Returns:
            List of all words
        """
        words = []
        self._collect_words(self.root, "", words)
        return words
    
    def __len__(self) -> int:
        """Get number of words in trie."""
        return self.size
    
    def __contains__(self, word: str) -> bool:
        """Check if word in trie."""
        return self.search(word)
    
    def __repr__(self) -> str:
        return f"PrefixTree(size={self.size})"


class TrieSet:
    """Trie-based set for string storage."""
    
    def __init__(self) -> None:
        """Initialize trie set."""
        self.trie = PrefixTree()
    
    def add(self, word: str) -> None:
        """Add word to set."""
        self.trie.insert(word)
    
    def remove(self, word: str) -> bool:
        """Remove word from set."""
        return self.trie.delete(word)
    
    def contains(self, word: str) -> bool:
        """Check if word in set."""
        return self.trie.search(word)
    
    def __len__(self) -> int:
        """Get set size."""
        return len(self.trie)


class TrieMap:
    """Trie-based map for string storage with values."""
    
    def __init__(self) -> None:
        """Initialize trie map."""
        self.root = TrieNode()
        self.values: Dict[str, object] = {}
    
    def put(self, key: str, value: object) -> None:
        """
        Put key-value pair.
        
        Args:
            key: String key
            value: Value to store
        """
        self.root.insert(key)
        self.values[key] = value
    
    def get(self, key: str) -> Optional[object]:
        """
        Get value for key.
        
        Args:
            key: String key
            
        Returns:
            Value or None if not found
        """
        if self.root.search(key):
            return self.values.get(key)
        return None
    
    def remove(self, key: str) -> bool:
        """
        Remove key-value pair.
        
        Args:
            key: Key to remove
            
        Returns:
            True if removed
        """
        if self.root.delete(key):
            del self.values[key]
            return True
        return False
    
    def keys_with_prefix(self, prefix: str) -> List[str]:
        """
        Get all keys starting with prefix.
        
        Args:
            prefix: Prefix to search
            
        Returns:
            List of keys
        """
        return self.root.get_words_with_prefix(prefix)


def main() -> None:
    """Demonstrate prefix tree operations."""
    
    print("=== Prefix Tree Demo ===")
    
    # Basic operations
    print("\n--- Basic Operations ---")
    trie = PrefixTree()
    
    words = ["apple", "app", "application", "banana", "band", "bandana"]
    for word in words:
        trie.insert(word)
    
    print(f"Inserted: {words}")
    print(f"Size: {len(trie)}")
    
    print(f"Search 'apple': {trie.search('apple')}")
    print(f"Search 'app': {trie.search('app')}")
    print(f"Search 'appl': {trie.search('appl')}")
    
    print(f"Starts with 'app': {trie.starts_with('app')}")
    print(f"Starts with 'ban': {trie.starts_with('ban')}")
    print(f"Starts with 'xyz': {trie.starts_with('xyz')}")
    
    # Prefix operations
    print("\n--- Prefix Operations ---")
    prefix = "app"
    print(f"Words with prefix '{prefix}': {trie.get_words_with_prefix(prefix)}")
    print(f"Count with prefix '{prefix}': {trie.count_words_with_prefix(prefix)}")
    
    # Autocomplete
    print("\n--- Autocomplete ---")
    prefix = "ban"
    suggestions = trie.autocomplete(prefix, limit=3)
    print(f"Autocomplete '{prefix}': {suggestions}")
    
    # Delete
    print("\n--- Delete ---")
    print(f"Before delete 'app': {trie.search('app')}")
    trie.delete("app")
    print(f"After delete 'app': {trie.search('app')}")
    print(f"Words with prefix 'app': {trie.get_words_with_prefix('app')}")
    
    # Get all words
    print("\n--- All Words ---")
    print(f"All words: {trie.get_all_words()}")
    
    # TrieSet
    print("\n--- TrieSet ---")
    trie_set = TrieSet()
    for word in ["hello", "world", "hello", "python"]:
        trie_set.add(word)
    
    print(f"Set contains 'hello': {trie_set.contains('hello')}")
    print(f"Set contains 'java': {trie_set.contains('java')}")
    print(f"Set size: {len(trie_set)}")
    
    trie_set.remove("hello")
    print(f"After removing 'hello': {trie_set.contains('hello')}")
    
    # TrieMap
    print("\n--- TrieMap ---")
    trie_map = TrieMap()
    trie_map.put("name", "Alice")
    trie_map.put("age", 25)
    trie_map.put("name", "Bob")  # Update
    
    print(f"Get 'name': {trie_map.get('name')}")
    print(f"Get 'age': {trie_map.get('age')}")
    print(f"Keys with prefix 'na': {trie_map.keys_with_prefix('na')}")


if __name__ == "__main__":
    main()
