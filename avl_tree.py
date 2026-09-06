"""
AVL Tree - Self-balancing binary search tree.
Features: O(log n) operations, height balancing, and rotations.
"""

from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')


class AVLNode(Generic[T]):
    """Node in AVL tree."""
    
    def __init__(self, value: T) -> None:
        """
        Initialize AVL node.
        
        Args:
            value: Node value
        """
        self.value = value
        self.left: Optional['AVLNode[T]'] = None
        self.right: Optional['AVLNode[T]'] = None
        self.height = 1
    
    def __str__(self) -> str:
        """String representation."""
        return str(self.value)


class AVLTree(Generic[T]):
    """AVL tree implementation."""
    
    def __init__(self) -> None:
        """Initialize AVL tree."""
        self.root: Optional[AVLNode[T]] = None
    
    def _get_height(self, node: Optional[AVLNode[T]]) -> int:
        """Get height of node."""
        if node is None:
            return 0
        return node.height
    
    def _get_balance(self, node: Optional[AVLNode[T]]) -> int:
        """Get balance factor of node."""
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _update_height(self, node: AVLNode[T]) -> None:
        """Update height of node."""
        node.height = 1 + max(self._get_height(node.left), 
                           self._get_height(node.right))
    
    def _right_rotate(self, y: AVLNode[T]) -> AVLNode[T]:
        """Right rotate around node y."""
        x = y.left
        T2 = x.right if x else None
        
        # Perform rotation
        x.right = y
        y.left = T2
        
        # Update heights
        self._update_height(y)
        self._update_height(x)
        
        return x
    
    def _left_rotate(self, x: AVLNode[T]) -> AVLNode[T]:
        """Left rotate around node x."""
        y = x.right
        T2 = y.left if y else None
        
        # Perform rotation
        y.left = x
        x.right = T2
        
        # Update heights
        self._update_height(x)
        self._update_height(y)
        
        return y
    
    def insert(self, value: T) -> None:
        """
        Insert value into AVL tree.
        
        Args:
            value: Value to insert
        """
        self.root = self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: Optional[AVLNode[T]], value: T) -> AVLNode[T]:
        """Recursively insert value."""
        if node is None:
            return AVLNode(value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node  # Duplicate values not allowed
        
        # Update height
        self._update_height(node)
        
        # Get balance factor
        balance = self._get_balance(node)
        
        # Left Left Case
        if balance > 1 and value < node.left.value:
            return self._right_rotate(node)
        
        # Right Right Case
        if balance < -1 and value > node.right.value:
            return self._left_rotate(node)
        
        # Left Right Case
        if balance > 1 and value > node.left.value:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        
        # Right Left Case
        if balance < -1 and value < node.right.value:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        
        return node
    
    def delete(self, value: T) -> bool:
        """
        Delete value from AVL tree.
        
        Args:
            value: Value to delete
            
        Returns:
            True if deleted
        """
        if not self.search(value):
            return False
        
        self.root = self._delete_recursive(self.root, value)
        return True
    
    def _delete_recursive(self, node: Optional[AVLNode[T]], value: T) -> Optional[AVLNode[T]]:
        """Recursively delete value."""
        if node is None:
            return node
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Node with two children
                successor = self._get_min_value_node(node.right)
                node.value = successor.value
                node.right = self._delete_recursive(node.right, successor.value)
        
        if node is None:
            return node
        
        # Update height
        self._update_height(node)
        
        # Get balance factor
        balance = self._get_balance(node)
        
        # Left Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)
        
        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        
        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)
        
        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        
        return node
    
    def _get_min_value_node(self, node: AVLNode[T]) -> AVLNode[T]:
        """Get node with minimum value."""
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def search(self, value: T) -> bool:
        """
        Search for value in AVL tree.
        
        Args:
            value: Value to search
            
        Returns:
            True if found
        """
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node: Optional[AVLNode[T]], value: T) -> bool:
        """Recursively search for value."""
        if node is None:
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
    
    def _inorder_recursive(self, node: Optional[AVLNode[T]], result: List[T]) -> None:
        """Recursively perform inorder traversal."""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def get_height(self) -> int:
        """Get tree height."""
        return self._get_height(self.root)
    
    def size(self) -> int:
        """Get number of nodes."""
        return self._size_recursive(self.root)
    
    def _size_recursive(self, node: Optional[AVLNode[T]]) -> int:
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
            return "AVLTree(empty)"
        return f"AVLTree({self.inorder_traversal()}, height={self.get_height()})"
    
    def __len__(self) -> int:
        """Get length."""
        return self.size()
    
    def __contains__(self, value: T) -> bool:
        """Check if value exists."""
        return self.search(value)


def main() -> None:
    """Demonstrate AVL tree."""
    
    print("=== AVL Tree Demo ===")
    
    avl = AVLTree[int]()
    
    # Insert values
    values = [10, 20, 30, 40, 50, 25]
    for value in values:
        avl.insert(value)
        print(f"Inserted {value}, Height: {avl.get_height()}")
    
    print(f"\nAVL tree: {avl}")
    print(f"Size: {avl.size()}")
    print(f"Height: {avl.get_height()}")
    
    # Inorder traversal
    print(f"\nInorder (sorted): {avl.inorder_traversal()}")
    
    # Search
    print(f"\n--- Search ---")
    search_values = [20, 25, 100]
    for value in search_values:
        result = avl.search(value)
        print(f"Search {value}: {result}")
    
    # Delete
    print(f"\n--- Delete ---")
    avl.delete(30)
    print(f"After delete(30): {avl}")
    print(f"Height: {avl.get_height()}")
    
    avl.delete(10)
    print(f"After delete(10): {avl}")
    print(f"Height: {avl.get_height()}")
    
    # String AVL tree
    print("\n=== String AVL Tree ===")
    str_avl = AVLTree[str]()
    
    words = ["banana", "apple", "cherry", "date"]
    for word in words:
        str_avl.insert(word)
    
    print(f"String tree: {str_avl}")
    print(f"Sorted: {str_avl.inorder_traversal()}")
    
    # Contains
    print(f"\n'apple' in tree: {'apple' in str_avl}")
    print(f"'grape' in tree: {'grape' in str_avl}")
    
    # Clear
    avl.clear()
    print(f"\nAfter clear: {avl}")
    print(f"Is empty: {avl.is_empty()}")
    
    # Balance verification
    print("\n=== Balance Verification ===")
    balanced_avl = AVLTree[int]()
    
    # Insert values that would cause rotations
    test_values = [41, 20, 65, 11, 29, 50, 26]
    for value in test_values:
        balanced_avl.insert(value)
        print(f"Inserted {value}, Height: {balanced_avl.get_height()}")
    
    print(f"\nFinal tree: {balanced_avl}")
    print(f"Height: {balanced_avl.get_height()}")
    print(f"Size: {balanced_avl.size()}")
    
    # Performance test
    print("\n=== Performance Test ===")
    import time
    
    large_avl = AVLTree[int]()
    n = 10000
    
    start = time.time()
    for i in range(n):
        large_avl.insert(i)
    insert_time = (time.time() - start) * 1000
    
    print(f"Inserted {n} items in {insert_time:.2f}ms")
    print(f"Height: {large_avl.get_height()}")
    
    start = time.time()
    for i in range(n):
        large_avl.search(i)
    search_time = (time.time() - start) * 1000
    
    print(f"Searched {n} items in {search_time:.2f}ms")


if __name__ == "__main__":
    main()
