"""
Binary Search Tree - BST implementation with insertion, search, and traversal.
Features: Insert, search, delete, and various traversal methods.
"""

from typing import Optional, List, Any


class TreeNode:
    """Node in binary search tree."""
    
    def __init__(self, value: Any) -> None:
        """
        Initialize tree node.
        
        Args:
            value: Node value
        """
        self.value = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None
    
    def __str__(self) -> str:
        """String representation."""
        return str(self.value)


class BinarySearchTree:
    """Binary search tree implementation."""
    
    def __init__(self) -> None:
        """Initialize BST."""
        self.root: Optional[TreeNode] = None
        self._size = 0
    
    def insert(self, value: Any) -> None:
        """
        Insert value into BST.
        
        Args:
            value: Value to insert
        """
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
        self._size += 1
    
    def _insert_recursive(self, node: TreeNode, value: Any) -> None:
        """Recursively insert value."""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value: Any) -> bool:
        """
        Search for value in BST.
        
        Args:
            value: Value to search
            
        Returns:
            True if value exists
        """
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node: Optional[TreeNode], value: Any) -> bool:
        """Recursively search for value."""
        if node is None:
            return False
        
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def delete(self, value: Any) -> bool:
        """
        Delete value from BST.
        
        Args:
            value: Value to delete
            
        Returns:
            True if value was deleted
        """
        if not self.search(value):
            return False
        
        self.root = self._delete_recursive(self.root, value)
        self._size -= 1
        return True
    
    def _delete_recursive(self, node: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
        """Recursively delete value."""
        if node is None:
            return None
        
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
            
            # Node has two children - find inorder successor
            successor = self._find_min(node.right)
            node.value = successor.value
            node.right = self._delete_recursive(node.right, successor.value)
        
        return node
    
    def _find_min(self, node: TreeNode) -> TreeNode:
        """Find minimum node in subtree."""
        while node.left:
            node = node.left
        return node
    
    def inorder_traversal(self) -> List[Any]:
        """
        Get inorder traversal (sorted order).
        
        Returns:
            List of values in sorted order
        """
        result: List[Any] = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Recursively perform inorder traversal."""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def preorder_traversal(self) -> List[Any]:
        """
        Get preorder traversal.
        
        Returns:
            List of values in preorder
        """
        result: List[Any] = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Recursively perform preorder traversal."""
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def postorder_traversal(self) -> List[Any]:
        """
        Get postorder traversal.
        
        Returns:
            List of values in postorder
        """
        result: List[Any] = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Recursively perform postorder traversal."""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
    
    def find_min(self) -> Optional[Any]:
        """
        Find minimum value in BST.
        
        Returns:
            Minimum value or None if empty
        """
        if self.root is None:
            return None
        return self._find_min(self.root).value
    
    def find_max(self) -> Optional[Any]:
        """
        Find maximum value in BST.
        
        Returns:
            Maximum value or None if empty
        """
        if self.root is None:
            return None
        
        node = self.root
        while node.right:
            node = node.right
        return node.value
    
    def get_height(self) -> int:
        """
        Get height of BST.
        
        Returns:
            Height of tree
        """
        return self._get_height_recursive(self.root)
    
    def _get_height_recursive(self, node: Optional[TreeNode]) -> int:
        """Recursively calculate height."""
        if node is None:
            return 0
        return 1 + max(self._get_height_recursive(node.left), 
                      self._get_height_recursive(node.right))
    
    def size(self) -> int:
        """Get number of nodes."""
        return self._size
    
    def is_empty(self) -> bool:
        """Check if BST is empty."""
        return self.root is None
    
    def clear(self) -> None:
        """Clear all nodes."""
        self.root = None
        self._size = 0
    
    def __str__(self) -> str:
        """String representation."""
        if self.root is None:
            return "Empty BST"
        return f"BST [{', '.join(map(str, self.inorder_traversal()))}]"


def main() -> None:
    """Demonstrate BST functionality."""
    
    print("=== Binary Search Tree Demo ===")
    
    bst = BinarySearchTree()
    
    # Insert values
    values = [50, 30, 70, 20, 40, 60, 80]
    print(f"\nInserting values: {values}")
    for value in values:
        bst.insert(value)
    
    print(f"BST: {bst}")
    print(f"Size: {bst.size()}")
    print(f"Height: {bst.get_height()}")
    
    # Traversals
    print(f"\nInorder (sorted): {bst.inorder_traversal()}")
    print(f"Preorder: {bst.preorder_traversal()}")
    print(f"Postorder: {bst.postorder_traversal()}")
    
    # Search
    print(f"\nSearch 40: {bst.search(40)}")
    print(f"Search 100: {bst.search(100)}")
    
    # Min/Max
    print(f"\nMin: {bst.find_min()}")
    print(f"Max: {bst.find_max()}")
    
    # Delete
    print(f"\nDeleting 20 (leaf node)")
    bst.delete(20)
    print(f"BST: {bst}")
    
    print(f"\nDeleting 30 (node with one child)")
    bst.delete(30)
    print(f"BST: {bst}")
    
    print(f"\nDeleting 50 (node with two children)")
    bst.delete(50)
    print(f"BST: {bst}")
    
    # String BST
    print("\n=== String BST ===")
    string_bst = BinarySearchTree()
    words = ["banana", "apple", "cherry", "date", "elderberry"]
    for word in words:
        string_bst.insert(word)
    
    print(f"String BST: {string_bst}")
    print(f"Sorted: {string_bst.inorder_traversal()}")


if __name__ == "__main__":
    main()
