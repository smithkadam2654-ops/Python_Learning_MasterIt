"""
Tree Traversal - Binary tree implementation with traversal algorithms.
Features: Pre-order, In-order, Post-order, Level-order traversals.
"""

from typing import Optional, List, Any
from collections import deque
from dataclasses import dataclass


@dataclass
class TreeNode:
    """Node for binary tree."""
    val: Any
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None


class BinaryTree:
    """Binary tree implementation with various traversals."""
    
    def __init__(self, root: Optional[TreeNode] = None) -> None:
        """Initialize binary tree with optional root."""
        self.root = root
    
    def insert(self, val: Any) -> None:
        """Insert value into tree (level-order insertion)."""
        new_node = TreeNode(val)
        
        if self.root is None:
            self.root = new_node
            return
        
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            
            if node.left is None:
                node.left = new_node
                return
            else:
                queue.append(node.left)
            
            if node.right is None:
                node.right = new_node
                return
            else:
                queue.append(node.right)
    
    def preorder_traversal(self) -> List[Any]:
        """
        Pre-order traversal: Root -> Left -> Right.
        
        Returns:
            List of values in pre-order
        """
        result = []
        
        def traverse(node: Optional[TreeNode]) -> None:
            if node:
                result.append(node.val)
                traverse(node.left)
                traverse(node.right)
        
        traverse(self.root)
        return result
    
    def inorder_traversal(self) -> List[Any]:
        """
        In-order traversal: Left -> Root -> Right.
        
        Returns:
            List of values in in-order
        """
        result = []
        
        def traverse(node: Optional[TreeNode]) -> None:
            if node:
                traverse(node.left)
                result.append(node.val)
                traverse(node.right)
        
        traverse(self.root)
        return result
    
    def postorder_traversal(self) -> List[Any]:
        """
        Post-order traversal: Left -> Right -> Root.
        
        Returns:
            List of values in post-order
        """
        result = []
        
        def traverse(node: Optional[TreeNode]) -> None:
            if node:
                traverse(node.left)
                traverse(node.right)
                result.append(node.val)
        
        traverse(self.root)
        return result
    
    def level_order_traversal(self) -> List[List[Any]]:
        """
        Level-order (BFS) traversal.
        
        Returns:
            List of lists, each containing values at a level
        """
        if self.root is None:
            return []
        
        result = []
        queue = deque([self.root])
        
        while queue:
            level_size = len(queue)
            level_values = []
            
            for _ in range(level_size):
                node = queue.popleft()
                level_values.append(node.val)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(level_values)
        
        return result
    
    def preorder_iterative(self) -> List[Any]:
        """
        Pre-order traversal using stack (iterative).
        
        Returns:
            List of values in pre-order
        """
        if self.root is None:
            return []
        
        result = []
        stack = [self.root]
        
        while stack:
            node = stack.pop()
            result.append(node.val)
            
            # Push right first, then left (so left is processed first)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        
        return result
    
    def inorder_iterative(self) -> List[Any]:
        """
        In-order traversal using stack (iterative).
        
        Returns:
            List of values in in-order
        """
        if self.root is None:
            return []
        
        result = []
        stack = []
        current = self.root
        
        while current or stack:
            # Go to leftmost node
            while current:
                stack.append(current)
                current = current.left
            
            # Process node
            current = stack.pop()
            result.append(current.val)
            
            # Move to right subtree
            current = current.right
        
        return result
    
    def find_max(self) -> Optional[Any]:
        """Find maximum value in the tree."""
        if self.root is None:
            return None
        
        max_val = self.root.val
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            max_val = max(max_val, node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return max_val
    
    def find_min(self) -> Optional[Any]:
        """Find minimum value in the tree."""
        if self.root is None:
            return None
        
        min_val = self.root.val
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            min_val = min(min_val, node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return min_val
    
    def height(self) -> int:
        """Calculate the height of the tree."""
        def calculate_height(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            left_height = calculate_height(node.left)
            right_height = calculate_height(node.right)
            return max(left_height, right_height) + 1
        
        return calculate_height(self.root)
    
    def count_nodes(self) -> int:
        """Count total number of nodes in the tree."""
        def count(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            return 1 + count(node.left) + count(node.right)
        
        return count(self.root)
    
    def is_balanced(self) -> bool:
        """Check if the tree is height-balanced."""
        def check_balance(node: Optional[TreeNode]) -> tuple[bool, int]:
            if node is None:
                return (True, 0)
            
            left_balanced, left_height = check_balance(node.left)
            right_balanced, right_height = check_balance(node.right)
            
            balanced = (
                left_balanced and 
                right_balanced and 
                abs(left_height - right_height) <= 1
            )
            
            return (balanced, max(left_height, right_height) + 1)
        
        balanced, _ = check_balance(self.root)
        return balanced
    
    def __str__(self) -> str:
        """String representation using level-order traversal."""
        levels = self.level_order_traversal()
        return " -> ".join(" | ".join(map(str, level)) for level in levels)


def main() -> None:
    """Demonstrate binary tree operations."""
    
    # Create tree and insert values
    tree = BinaryTree()
    values = [1, 2, 3, 4, 5, 6, 7]
    
    for val in values:
        tree.insert(val)
    
    print("=== Binary Tree Operations ===")
    print(f"Inserted values: {values}")
    print(f"Tree structure: {tree}")
    
    print("\n=== Traversals ===")
    print(f"Pre-order (recursive): {tree.preorder_traversal()}")
    print(f"Pre-order (iterative): {tree.preorder_iterative()}")
    print(f"In-order (recursive): {tree.inorder_traversal()}")
    print(f"In-order (iterative): {tree.inorder_iterative()}")
    print(f"Post-order: {tree.postorder_traversal()}")
    print(f"Level-order: {tree.level_order_traversal()}")
    
    print("\n=== Tree Properties ===")
    print(f"Height: {tree.height()}")
    print(f"Total nodes: {tree.count_nodes()}")
    print(f"Max value: {tree.find_max()}")
    print(f"Min value: {tree.find_min()}")
    print(f"Is balanced: {tree.is_balanced()}")
    
    # Create an unbalanced tree
    print("\n=== Unbalanced Tree Example ===")
    unbalanced = BinaryTree()
    unbalanced.root = TreeNode(1)
    unbalanced.root.left = TreeNode(2)
    unbalanced.root.left.left = TreeNode(3)
    unbalanced.root.left.left.left = TreeNode(4)
    
    print(f"Height: {unbalanced.height()}")
    print(f"Is balanced: {unbalanced.is_balanced()}")


if __name__ == "__main__":
    main()
