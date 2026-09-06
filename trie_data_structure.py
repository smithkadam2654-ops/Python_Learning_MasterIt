"""
Trie Data Structure - Trie/prefix tree implementation.
Features: Insert, search, autocomplete, and prefix operations.
"""

from typing import Optional, Dict, List


class TrieNode:
    """Node in trie."""
    
    def __init__(self) -> None:
        """Initialize trie node."""
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word = False
        self.word_count = 0
    
    def has_child(self, char: str) -> bool:
        """Check if node has child."""
        return char in self.children
    
    def get_child(self, char: str) -> Optional['TrieNode']:
        """Get child node."""
        return self.children.get(char)
    
    def add_child(self, char: str) -> 'TrieNode':
        """Add child node."""
        if char not in self.children:
            self.children[char] = TrieNode()
        return self.children[char]


class Trie:
    """Trie (prefix tree) implementation."""
    
    def __init__(self) -> None:
        """Initialize trie."""
        self.root = TrieNode()
        self._size = 0
    
    def insert(self, word: str) -> None:
        """
        Insert word into trie.
        
        Args:
            word: Word to insert
        """
        node = self.root
        
        for char in word:
            node = node.add_child(char)
        
        if not node.is_end_of_word:
            node.is_end_of_word = True
            node.word_count += 1
            self._size += 1
        else:
            node.word_count += 1
    
    def search(self, word: str) -> bool:
        """
        Search for exact word.
        
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
        """Find node for prefix."""
        node = self.root
        
        for char in prefix:
            node = node.get_child(char)
            if node is None:
                return None
        
        return node
    
    def autocomplete(self, prefix: str, limit: int = 10) -> List[str]:
        """
        Get autocomplete suggestions.
        
        Args:
            prefix: Prefix to complete
            limit: Maximum number of suggestions
            
        Returns:
            List of suggestions
        """
        node = self._find_node(prefix)
        if node is None:
            return []
        
        suggestions = []
        self._collect_words(node, prefix, suggestions, limit)
        return suggestions
    
    def _collect_words(self, node: TrieNode, prefix: str, 
                      suggestions: List[str], limit: int) -> None:
        """Collect all words from node."""
        if len(suggestions) >= limit:
            return
        
        if node.is_end_of_word:
            suggestions.append(prefix)
        
        for char, child in sorted(node.children.items()):
            self._collect_words(child, prefix + char, suggestions, limit)
    
    def get_all_words(self) -> List[str]:
        """
        Get all words in trie.
        
        Returns:
            List of all words
        """
        words = []
        self._collect_words(self.root, "", words, float('inf'))
        return words
    
    def delete(self, word: str) -> bool:
        """
        Delete word from trie.
        
        Args:
            word: Word to delete
            
        Returns:
            True if deleted
        """
        nodes = []
        node = self.root
        
        # Find path to word
        for char in word:
            nodes.append((char, node))
            node = node.get_child(char)
            if node is None:
                return False
        
        if not node.is_end_of_word:
            return False
        
        # Decrement word count
        node.word_count -= 1
        if node.word_count > 0:
            return True
        
        node.is_end_of_word = False
        
        # Remove unused nodes
        for i in range(len(nodes) - 1, -1, -1):
            char, parent_node = nodes[i]
            current_node = parent_node.get_child(char)
            
            if not current_node.is_end_of_word and not current_node.children:
                del parent_node.children[char]
            else:
                break
        
        self._size -= 1
        return True
    
    def count_words(self) -> int:
        """Get total word count."""
        return self._size
    
    def count_prefix(self, prefix: str) -> int:
        """
        Count words with given prefix.
        
        Args:
            prefix: Prefix to count
            
        Returns:
            Number of words with prefix
        """
        node = self._find_node(prefix)
        if node is None:
            return 0
        
        count = 0
        self._count_words_recursive(node, count)
        return count
    
    def _count_words_recursive(self, node: TrieNode, count: int) -> int:
        """Recursively count words."""
        if node.is_end_of_word:
            count += node.word_count
        
        for child in node.children.values():
            count = self._count_words_recursive(child, count)
        
        return count
    
    def clear(self) -> None:
        """Clear all words."""
        self.root = TrieNode()
        self._size = 0
    
    def is_empty(self) -> bool:
        """Check if trie is empty."""
        return self._size == 0
    
    def __str__(self) -> str:
        """String representation."""
        words = self.get_all_words()
        return f"Trie({len(words)} words: {words[:10]}{'...' if len(words) > 10 else ''})"


def main() -> None:
    """Demonstrate trie."""
    
    print("=== Trie Data Structure Demo ===")
    
    trie = Trie()
    
    # Insert words
    words = ["apple", "app", "application", "apply", "banana", "band", "bandana"]
    for word in words:
        trie.insert(word)
        print(f"Inserted: {word}")
    
    print(f"\nTrie: {trie}")
    print(f"Word count: {trie.count_words()}")
    
    # Search
    print(f"\nSearch 'app': {trie.search('app')}")
    print(f"Search 'apple': {trie.search('apple')}")
    print(f"Search 'appl': {trie.search('appl')}")
    print(f"Search 'orange': {trie.search('orange')}")
    
    # Starts with
    print(f"\nStarts with 'app': {trie.starts_with('app')}")
    print(f"Starts with 'ban': {trie.starts_with('ban')}")
    print(f"Starts with 'ora': {trie.starts_with('ora')}")
    
    # Autocomplete
    print(f"\nAutocomplete 'app': {trie.autocomplete('app')}")
    print(f"Autocomplete 'ban': {trie.autocomplete('ban')}")
    print(f"Autocomplete 'x': {trie.autocomplete('x')}")
    
    # Count prefix
    print(f"\nCount words with prefix 'app': {trie.count_prefix('app')}")
    print(f"Count words with prefix 'ban': {trie.count_prefix('ban')}")
    
    # Get all words
    print(f"\nAll words: {trie.get_all_words()}")
    
    # Delete
    print(f"\nDelete 'app': {trie.delete('app')}")
    print(f"Search 'app': {trie.search('app')}")
    print(f"Autocomplete 'app': {trie.autocomplete('app')}")
    
    print(f"\nDelete 'apple': {trie.delete('apple')}")
    print(f"Search 'apple': {trie.search('apple')}")
    print(f"Autocomplete 'app': {trie.autocomplete('app')}")
    
    # Clear
    trie.clear()
    print(f"\nAfter clear: {trie}")
    print(f"Is empty: {trie.is_empty()}")


if __name__ == "__main__":
    main()
