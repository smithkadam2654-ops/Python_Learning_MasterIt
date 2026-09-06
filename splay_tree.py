"""
Splay Tree - Self-adjusting binary search tree.
Features: Splaying operation, amortized O(log n) operations, and recent access optimization.
"""

from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')


class SplayNode(Generic[T]):
    """Node in splay tree."""
    
    def __init__(self, value: T) -> None:
        """
        Initialize splay node.
        
        Args:
            value: Node value
        """
        self.value = value
        self.left: Optional['SplayNode[T]'] = None
        self.right: Optional['SplayNode[T]'] = None
        self.parent: Optional['SplayNode[T]'] = None
    
    def __str__(self) -> str:
        """String representation."""
        return str(self.value)


class SplayTree(Generic[T]):
    """Splay tree implementation."""
    
    def __init__(self) -> None:
        """Initialize splay tree."""
        self.root: Optional[SplayNode[T]] = None
    
    def _right_rotate(self, x: SplayNode[T]) -> None:
        """Right rotate around node x."""
        y = x.left
        if y is None:
            return
        
        x.left = y.right
        if y.right:
            y.right.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.right = x
        x.parent = y
    
    def _left_rotate(self, x: SplayNode[T]) -> None:
        """Left rotate around node x."""
        y = x.right
        if y is None:
            return
        
        x.right = y.left
        if y.left:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        
        y.left = x
        x.parent = y
    
    def _splay(self, node: SplayNode[T]) -> None:
        """Splay node to root."""
        while node.parent is not None:
            # Zig case
            if node.parent.parent is None:
                if node == node.parent.left:
                    self._right_rotate(node.parent)
                else:
                    self._left_rotate(node.parent)
            # Zig-zig case
            elif (node == node.parent.left and 
                  node.parent == node.parent.parent.left):
                self._right_rotate(node.parent.parent)
                self._right_rotate(node.parent)
            elif (node == node.parent.right and 
                  node.parent == node.parent.parent.right):
                self._left_rotate(node.parent.parent)
                self._left_rotate(node.parent)
            # Zig-zag case
            elif (node == node.parent.right and 
                  node.parent == node.parent.parent.left):
                self._left_rotate(node.parent)
                self._right_rotate(node.parent)
            else:
                self._right_rotate(node.parent)
                self._left_rotate(node.parent)
    
    def insert(self, value: T) -> None:
        """
        Insert value into splay tree.
        
        Args:
            value: Value to insert
        """
        node = SplayNode(value)
        
        if self.root is None:
            self.root = node
            return
        
        # BST insert
        current = self.root
        parent = None
        
        while current is not None:
            parent = current
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                # Value already exists, splay and return
                self._splay(current)
                return
        
        # Insert new node
        node.parent = parent
        if value < parent.value:
            parent.left = node
        else:
            parent.right = node
        
        # Splay new node to root
        self._splay(node)
    
    def search(self, value: T) -> bool:
        """
        Search for value in splay tree.
        
        Args:
            value: Value to search
            
        Returns:
            True if found
        """
        current = self.root
        
        while current is not None:
            if value == current.value:
                self._splay(current)
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        
        return False
    
    def delete(self, value: T) -> bool:
        """
        Delete value from splay tree.
        
        Args:
            value: Value to delete
            
        Returns:
            True if deleted
        """
        if not self.search(value):
            return False
        
        # Now the node to delete is at root
        if self.root is None:
            return False
        
        # If root has no left child
        if self.root.left is None:
            self.root = self.root.right
            if self.root:
                self.root.parent = None
        # If root has no right child
        elif self.root.right is None:
            self.root = self.root.left
            if self.root:
                self.root.parent = None
        else:
            # Find inorder successor (minimum in right subtree)
            successor = self._get_min(self.root.right)
            
            # Splay successor to root
            self._splay(successor)
            
            # Now successor is root, attach left subtree
            successor.left = self.root.left
            if successor.left:
                successor.left.parent = successor
            
            self.root = successor
            self.root.parent = None
        
        return True
    
    def _get_min(self, node: SplayNode[T]) -> SplayNode[T]:
        """Get minimum node in subtree."""
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def find_max(self) -> Optional[T]:
        """Find maximum value in tree."""
        if self.root is None:
            return None
        
        current = self.root
        while current.right is not None:
            current = current.right
        
        self._splay(current)
        return current.value
    
    def find_min(self) -> Optional[T]:
        """Find minimum value in tree."""
        if self.root is None:
            return None
        
        current = self.root
        while current.left is not None:
            current = current.left
        
        self._splay(current)
        return current.value
    
    def inorder_traversal(self) -> List[T]:
        """
        Get inorder traversal (sorted).
        
        Returns:
            List of values in sorted order
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[SplayNode[T]], result: List[T]) -> None:
        """Recursively perform inorder traversal."""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def size(self) -> int:
        """Get number of nodes."""
        return self._size_recursive(self.root)
    
    def _size_recursive(self, node: Optional[SplayNode[T]]) -> int:
        """Recursively count nodes."""
        if node is None:
            return 0
        return 1 + self._size_recursive(node.left) + self._size_recursive(node.right)
    
    def is_empty(self) -> bool:
        """Check if tree is empty."""
        return self.root is None
    
    def clear(self) -> None:
        """Clear tree."""
        self.root = None
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return "SplayTree(empty)"
        return f"SplayTree({self.inorder_traversal()})"
    
    def __len__(self) -> int:
        """Get length."""
        return self.size()
    
    def __contains__(self, value: T) -> bool:
        """Check if value exists."""
        return self.search(value)


def main() -> None:
    """Demonstrate splay tree."""
    
    print("=== Splay Tree Demo ===")
    
    st = SplayTree[int]()
    
    # Insert values
    values = [10, 20, 30, 40, 50, 25]
    for value in values:
        st.insert(value)
        print(f"Inserted {value}")
    
    print(f"\nSplay tree: {st}")
    print(f"Size: {st.size()}")
    
    # Inorder traversal
    print(f"\nInorder (sorted): {st.inorder_traversal()}")
    
    # Search (this will splay the found node to root)
    print(f"\n--- Search ---")
    print(f"Search 25: {st.search(25)}")
    print(f"After search, root should be 25")
    
    # Find min/max
    print(f"\n--- Min/Max ---")
    print(f"Min: {st.find_min()}")
    print(f"Max: {st.find_max()}")
    
    # Delete
    print(f"\n--- Delete ---")
    st.delete(25)
    print(f"After delete(25): {st}")
    
    st.delete(10)
    print(f"After delete(10): {st}")
    
    # String splay tree
    print("\n=== String Splay Tree ===")
    str_st = SplayTree[str]()
    
    words = ["banana", "apple", "cherry", "date"]
    for word in words:
        str_st.insert(word)
    
    print(f"String tree: {str_st}")
    print(f"Sorted: {str_st.inorder_traversal()}")
    
    # Contains
    print(f"\n'apple' in tree: {'apple' in str_st}")
    print(f"'grape' in tree: {'grape' in str_st}")
    
    # Clear
    st.clear()
    print(f"\nAfter clear: {st}")
    print(f"Is empty: {st.is_empty()}")
    
    # Access pattern demonstration
    print("\n=== Access Pattern Demo ===")
    pattern_st = SplayTree[int]()
    
    # Insert values
    for i in range(1, 11):
        pattern_st.insert(i)
    
    # Access same value multiple times (should stay near root)
    print("Accessing value 5 multiple times:")
    for _ in range(5):
        pattern_st.search(5)
    
    print(f"Root should be 5 (recently accessed)")
    print(f"Tree: {pattern_st}")
    
    # Performance test
    print("\n=== Performance Test ===")
    import time
    
    large_st = SplayTree[int]()
    n = 10000
    
    start = time.time()
    for i in range(n):
        large_st.insert(i)
    insert_time = (time.time() - start) * 1000
    
    print(f"Inserted {n} items in {insert_time:.2f}ms")
    
    # Search for recently accessed item (should be fast)
    large_st.search(n - 1)
    
    start = time.time()
    for _ in range(1000):
        large_st.search(n - 1)
    search_time = (time.time() - start) * 1000
    
    print(f"1000 searches for recent item in {search_time:.2f}ms")


if __name__ == "__main__":
    main()
