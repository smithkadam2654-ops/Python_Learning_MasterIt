"""
Red-Black Tree - Self-balancing binary search tree.
Features: O(log n) operations, automatic balancing, and color-based rules.
"""

from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')


class Color:
    """Node colors."""
    RED = "RED"
    BLACK = "BLACK"


class RBNode(Generic[T]):
    """Red-black tree node."""
    
    def __init__(self, value: T) -> None:
        """
        Initialize node.
        
        Args:
            value: Node value
        """
        self.value = value
        self.color = Color.RED
        self.left: Optional['RBNode[T]'] = None
        self.right: Optional['RBNode[T]'] = None
        self.parent: Optional['RBNode[T]'] = None
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.value}({self.color})"


class RedBlackTree(Generic[T]):
    """Red-black tree implementation."""
    
    def __init__(self) -> None:
        """Initialize red-black tree."""
        self.NIL: RBNode[T] = RBNode(None)  # Sentinel NIL node
        self.NIL.color = Color.BLACK
        self.root: Optional[RBNode[T]] = self.NIL
    
    def insert(self, value: T) -> None:
        """
        Insert value into tree.
        
        Args:
            value: Value to insert
        """
        new_node = RBNode(value)
        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.parent = None
        
        # BST insert
        parent = None
        current = self.root
        
        while current != self.NIL:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        
        new_node.parent = parent
        
        if parent is None:
            self.root = new_node
        elif value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Fix red-black properties
        self._fix_insert(new_node)
    
    def _fix_insert(self, node: RBNode[T]) -> None:
        """Fix red-black properties after insert."""
        while node.parent and node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                
                if uncle.color == Color.RED:
                    # Case 1: Uncle is red
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # Case 2: Node is right child
                        node = node.parent
                        self._left_rotate(node)
                    
                    # Case 3: Node is left child
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._right_rotate(node.parent.parent)
            else:
                # Mirror cases
                uncle = node.parent.parent.left
                
                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._left_rotate(node.parent.parent)
        
        self.root.color = Color.BLACK
    
    def _left_rotate(self, x: RBNode[T]) -> None:
        """Left rotate around node x."""
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def _right_rotate(self, y: RBNode[T]) -> None:
        """Right rotate around node y."""
        x = y.left
        y.left = x.right
        
        if x.right != self.NIL:
            x.right.parent = y
        
        x.parent = y.parent
        
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        
        x.right = y
        y.parent = x
    
    def search(self, value: T) -> bool:
        """
        Search for value.
        
        Args:
            value: Value to search
            
        Returns:
            True if found
        """
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node: RBNode[T], value: T) -> bool:
        """Recursively search for value."""
        if node == self.NIL:
            return False
        
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def inorder_traversal(self) -> List[T]:
        """
        Get inorder traversal (sorted).
        
        Returns:
            List of values in sorted order
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: RBNode[T], result: List[T]) -> None:
        """Recursively perform inorder traversal."""
        if node != self.NIL:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def get_height(self) -> int:
        """Get tree height."""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node: RBNode[T]) -> int:
        """Recursively calculate height."""
        if node == self.NIL:
            return 0
        return 1 + max(self._height_recursive(node.left), 
                      self._height_recursive(node.right))
    
    def size(self) -> int:
        """Get number of nodes."""
        return self._size_recursive(self.root)
    
    def _size_recursive(self, node: RBNode[T]) -> int:
        """Recursively count nodes."""
        if node == self.NIL:
            return 0
        return 1 + self._size_recursive(node.left) + self._size_recursive(node.right)
    
    def is_empty(self) -> bool:
        """Check if tree is empty."""
        return self.root == self.NIL
    
    def clear(self) -> None:
        """Clear tree."""
        self.root = self.NIL
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return "RedBlackTree(empty)"
        return f"RedBlackTree({self.inorder_traversal()})"
    
    def __len__(self) -> int:
        """Get length."""
        return self.size()
    
    def __contains__(self, value: T) -> bool:
        """Check if value exists."""
        return self.search(value)


def main() -> None:
    """Demonstrate red-black tree."""
    
    print("=== Red-Black Tree Demo ===")
    
    rbt = RedBlackTree[int]()
    
    # Insert values
    values = [50, 25, 75, 10, 30, 60, 80, 5, 15]
    for value in values:
        rbt.insert(value)
        print(f"Inserted {value}")
    
    print(f"\nRed-black tree: {rbt}")
    print(f"Size: {rbt.size()}")
    print(f"Height: {rbt.get_height()}")
    
    # Inorder traversal
    print(f"\nInorder (sorted): {rbt.inorder_traversal()}")
    
    # Search
    print(f"\n--- Search ---")
    search_values = [25, 30, 100]
    for value in search_values:
        result = rbt.search(value)
        print(f"Search {value}: {result}")
    
    # Contains
    print(f"\n50 in tree: {50 in rbt}")
    print(f"100 in tree: {100 in rbt}")
    
    # String red-black tree
    print("\n=== String Red-Black Tree ===")
    str_rbt = RedBlackTree[str]()
    
    words = ["banana", "apple", "cherry", "date"]
    for word in words:
        str_rbt.insert(word)
    
    print(f"String tree: {str_rbt}")
    print(f"Sorted: {str_rbt.inorder_traversal()}")
    
    # Clear
    rbt.clear()
    print(f"\nAfter clear: {rbt}")
    print(f"Is empty: {rbt.is_empty()}")
    
    # Performance test
    print("\n=== Performance Test ===")
    import time
    
    large_rbt = RedBlackTree[int]()
    n = 10000
    
    start = time.time()
    for i in range(n):
        large_rbt.insert(i)
    insert_time = (time.time() - start) * 1000
    
    print(f"Inserted {n} items in {insert_time:.2f}ms")
    print(f"Height: {large_rbt.get_height()}")
    
    start = time.time()
    for i in range(n):
        large_rbt.search(i)
    search_time = (time.time() - start) * 1000
    
    print(f"Searched {n} items in {search_time:.2f}ms")


if __name__ == "__main__":
    main()
