"""
B-Tree - Multi-way search tree for disk storage.
Features: Balanced structure, multiple keys per node, and efficient disk operations.
"""

from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')


class BTreeNode(Generic[T]):
    """Node in B-tree."""
    
    def __init__(self, is_leaf: bool = True) -> None:
        """
        Initialize B-tree node.
        
        Args:
            is_leaf: Whether node is a leaf
        """
        self.keys: List[T] = []
        self.children: List['BTreeNode[T]'] = []
        self.is_leaf = is_leaf
    
    def __str__(self) -> str:
        """String representation."""
        return f"Node({self.keys})"


class BTree(Generic[T]):
    """B-tree implementation."""
    
    def __init__(self, degree: int = 3) -> None:
        """
        Initialize B-tree.
        
        Args:
            degree: Minimum degree (each node has at least degree-1 keys)
        """
        if degree < 2:
            raise ValueError("Degree must be at least 2")
        
        self.degree = degree
        self.root = BTreeNode(True)
    
    def search(self, key: T) -> bool:
        """
        Search for key in B-tree.
        
        Args:
            key: Key to search
            
        Returns:
            True if found
        """
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node: BTreeNode[T], key: T) -> bool:
        """Recursively search for key."""
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        if i < len(node.keys) and key == node.keys[i]:
            return True
        
        if node.is_leaf:
            return False
        
        return self._search_recursive(node.children[i], key)
    
    def insert(self, key: T) -> None:
        """
        Insert key into B-tree.
        
        Args:
            key: Key to insert
        """
        root = self.root
        
        # If root is full, split it
        if len(root.keys) == 2 * self.degree - 1:
            new_root = BTreeNode(False)
            new_root.children.append(self.root)
            self.root = new_root
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)
    
    def _insert_non_full(self, node: BTreeNode[T], key: T) -> None:
        """Insert key into non-full node."""
        i = len(node.keys) - 1
        
        if node.is_leaf:
            # Insert key into leaf node
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            # Find child where key should be inserted
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            # If child is full, split it
            if len(node.children[i].keys) == 2 * self.degree - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            
            self._insert_non_full(node.children[i], key)
    
    def _split_child(self, parent: BTreeNode[T], index: int) -> None:
        """Split child node at index."""
        degree = self.degree
        child = parent.children[index]
        new_node = BTreeNode(child.is_leaf)
        
        # Move keys to new node
        new_node.keys = child.keys[degree:]
        child.keys = child.keys[:degree - 1]
        
        # Move children if not leaf
        if not child.is_leaf:
            new_node.children = child.children[degree:]
            child.children = child.children[:degree]
        
        # Insert new node into parent
        parent.children.insert(index + 1, new_node)
        parent.keys.insert(index, child.keys[degree - 1])
    
    def delete(self, key: T) -> bool:
        """
        Delete key from B-tree.
        
        Args:
            key: Key to delete
            
        Returns:
            True if deleted
        """
        if not self.search(key):
            return False
        
        self._delete_recursive(self.root, key)
        
        # If root has no keys, make first child the new root
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]
        
        return True
    
    def _delete_recursive(self, node: BTreeNode[T], key: T) -> None:
        """Recursively delete key."""
        t = self.degree
        i = 0
        
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        # Key found in this node
        if i < len(node.keys) and key == node.keys[i]:
            if node.is_leaf:
                # Remove key from leaf
                node.keys.pop(i)
            else:
                # Key in internal node
                if len(node.children[i].keys) >= t:
                    # Replace with predecessor
                    pred = self._get_predecessor(node, i)
                    node.keys[i] = pred
                    self._delete_recursive(node.children[i], pred)
                else:
                    # Replace with successor
                    succ = self._get_successor(node, i)
                    node.keys[i] = succ
                    self._delete_recursive(node.children[i + 1], succ)
        else:
            # Key not in this node
            if node.is_leaf:
                return  # Key not found
            
            # Ensure child has enough keys
            if len(node.children[i].keys) < t:
                self._fill(node, i)
            
            # Recurse
            if i > len(node.keys):
                self._delete_recursive(node.children[i - 1], key)
            else:
                self._delete_recursive(node.children[i], key)
    
    def _get_predecessor(self, node: BTreeNode[T], index: int) -> T:
        """Get predecessor key."""
        current = node.children[index]
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]
    
    def _get_successor(self, node: BTreeNode[T], index: int) -> T:
        """Get successor key."""
        current = node.children[index + 1]
        while not current.is_leaf:
            current = current.children[0]
        return current.keys[0]
    
    def _fill(self, node: BTreeNode[T], index: int) -> None:
        """Fill child at index to ensure it has enough keys."""
        t = self.degree
        
        if index > 0 and len(node.children[index - 1].keys) >= t:
            # Borrow from previous sibling
            child = node.children[index]
            sibling = node.children[index - 1]
            
            child.keys.insert(0, node.keys[index - 1])
            node.keys[index - 1] = sibling.keys.pop()
            
            if not child.is_leaf:
                child.children.insert(0, sibling.children.pop())
        elif index < len(node.children) - 1 and len(node.children[index + 1].keys) >= t:
            # Borrow from next sibling
            child = node.children[index]
            sibling = node.children[index + 1]
            
            child.keys.append(node.keys[index])
            node.keys[index] = sibling.keys.pop(0)
            
            if not child.is_leaf:
                child.children.append(sibling.children.pop(0))
        else:
            # Merge with sibling
            if index < len(node.children) - 1:
                self._merge(node, index)
            else:
                self._merge(node, index - 1)
    
    def _merge(self, node: BTreeNode[T], index: int) -> None:
        """Merge child at index with sibling."""
        child = node.children[index]
        sibling = node.children[index + 1]
        
        # Move key from node to child
        child.keys.append(node.keys.pop(index))
        
        # Add sibling's keys and children
        child.keys.extend(sibling.keys)
        if not child.is_leaf:
            child.children.extend(sibling.children)
        
        # Remove sibling
        node.children.pop(index + 1)
    
    def inorder_traversal(self) -> List[T]:
        """
        Get inorder traversal (sorted).
        
        Returns:
            List of values in sorted order
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: BTreeNode[T], result: List[T]) -> None:
        """Recursively perform inorder traversal."""
        i = 0
        for i in range(len(node.keys)):
            if not node.is_leaf:
                self._inorder_recursive(node.children[i], result)
            result.append(node.keys[i])
        
        if not node.is_leaf:
            self._inorder_recursive(node.children[i + 1], result)
    
    def size(self) -> int:
        """Get number of keys."""
        return self._size_recursive(self.root)
    
    def _size_recursive(self, node: BTreeNode[T]) -> int:
        """Recursively count keys."""
        count = len(node.keys)
        if not node.is_leaf:
            for child in node.children:
                count += self._size_recursive(child)
        return count
    
    def is_empty(self) -> bool:
        """Check if tree is empty."""
        return len(self.root.keys) == 0
    
    def clear(self) -> None:
        """Clear tree."""
        self.root = BTreeNode(True)
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return f"BTree(degree={self.degree}, empty)"
        return f"BTree(degree={self.degree}, keys={self.inorder_traversal()})"
    
    def __len__(self) -> int:
        """Get length."""
        return self.size()
    
    def __contains__(self, key: T) -> bool:
        """Check if key exists."""
        return self.search(key)


def main() -> None:
    """Demonstrate B-tree."""
    
    print("=== B-Tree Demo ===")
    
    bt = BTree[int](degree=2)
    
    # Insert values
    values = [10, 20, 5, 6, 12, 30, 7, 17]
    for value in values:
        bt.insert(value)
        print(f"Inserted {value}")
    
    print(f"\nB-tree: {bt}")
    print(f"Size: {bt.size()}")
    
    # Inorder traversal
    print(f"\nInorder (sorted): {bt.inorder_traversal()}")
    
    # Search
    print(f"\n--- Search ---")
    search_values = [10, 15, 20]
    for value in search_values:
        result = bt.search(value)
        print(f"Search {value}: {result}")
    
    # Delete
    print(f"\n--- Delete ---")
    bt.delete(6)
    print(f"After delete(6): {bt}")
    
    bt.delete(10)
    print(f"After delete(10): {bt}")
    
    # String B-tree
    print("\n=== String B-Tree ===")
    str_bt = BTree[str](degree=2)
    
    words = ["banana", "apple", "cherry", "date", "elderberry"]
    for word in words:
        str_bt.insert(word)
    
    print(f"String tree: {str_bt}")
    print(f"Sorted: {str_bt.inorder_traversal()}")
    
    # Contains
    print(f"\n'apple' in tree: {'apple' in str_bt}")
    print(f"'grape' in tree: {'grape' in str_bt}")
    
    # Clear
    bt.clear()
    print(f"\nAfter clear: {bt}")
    print(f"Is empty: {bt.is_empty()}")
    
    # Different degrees
    print("\n=== Different Degrees ===")
    
    bt2 = BTree[int](degree=3)
    for i in range(1, 11):
        bt2.insert(i)
    
    print(f"Degree 3: {bt2}")
    print(f"Size: {bt2.size()}")
    
    bt3 = BTree[int](degree=4)
    for i in range(1, 11):
        bt3.insert(i)
    
    print(f"Degree 4: {bt3}")
    print(f"Size: {bt3.size()}")


if __name__ == "__main__":
    main()
