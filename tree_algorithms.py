"""
Tree Algorithms - Binary tree operations and traversals.
Features: Tree traversals, BST operations, and tree problems.
"""

from typing import List, Optional, TypeVar, Generic
from collections import deque

T = TypeVar('T')


class TreeNode:
    """Binary tree node."""
    
    def __init__(self, val: T, left: 'TreeNode' = None, right: 'TreeNode' = None) -> None:
        """Initialize tree node."""
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


class TreeAlgorithms:
    """Tree algorithm implementations."""
    
    @staticmethod
    def preorder_traversal(root: Optional[TreeNode]) -> List[T]:
        """
        Preorder traversal (root, left, right).
        
        Args:
            root: Tree root
            
        Returns:
            List of values in preorder
        """
        result = []
        
        def traverse(node: Optional[TreeNode]) -> None:
            if not node:
                return
            result.append(node.val)
            traverse(node.left)
            traverse(node.right)
        
        traverse(root)
        return result
    
    @staticmethod
    def preorder_iterative(root: Optional[TreeNode]) -> List[T]:
        """
        Preorder traversal iterative.
        
        Args:
            root: Tree root
            
        Returns:
            List of values in preorder
        """
        if not root:
            return []
        
        result = []
        stack = [root]
        
        while stack:
            node = stack.pop()
            result.append(node.val)
            
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        
        return result
    
    @staticmethod
    def inorder_traversal(root: Optional[TreeNode]) -> List[T]:
        """
        Inorder traversal (left, root, right).
        
        Args:
            root: Tree root
            
        Returns:
            List of values in inorder
        """
        result = []
        
        def traverse(node: Optional[TreeNode]) -> None:
            if not node:
                return
            traverse(node.left)
            result.append(node.val)
            traverse(node.right)
        
        traverse(root)
        return result
    
    @staticmethod
    def inorder_iterative(root: Optional[TreeNode]) -> List[T]:
        """
        Inorder traversal iterative.
        
        Args:
            root: Tree root
            
        Returns:
            List of values in inorder
        """
        result = []
        stack = []
        current = root
        
        while current or stack:
            while current:
                stack.append(current)
                current = current.left
            
            current = stack.pop()
            result.append(current.val)
            current = current.right
        
        return result
    
    @staticmethod
    def postorder_traversal(root: Optional[TreeNode]) -> List[T]:
        """
        Postorder traversal (left, right, root).
        
        Args:
            root: Tree root
            
        Returns:
            List of values in postorder
        """
        result = []
        
        def traverse(node: Optional[TreeNode]) -> None:
            if not node:
                return
            traverse(node.left)
            traverse(node.right)
            result.append(node.val)
        
        traverse(root)
        return result
    
    @staticmethod
    def postorder_iterative(root: Optional[TreeNode]) -> List[T]:
        """
        Postorder traversal iterative (using two stacks).
        
        Args:
            root: Tree root
            
        Returns:
            List of values in postorder
        """
        if not root:
            return []
        
        result = []
        stack1 = [root]
        stack2 = []
        
        while stack1:
            node = stack1.pop()
            stack2.append(node)
            
            if node.left:
                stack1.append(node.left)
            if node.right:
                stack1.append(node.right)
        
        while stack2:
            result.append(stack2.pop().val)
        
        return result
    
    @staticmethod
    def level_order_traversal(root: Optional[TreeNode]) -> List[List[T]]:
        """
        Level order (BFS) traversal.
        
        Args:
            root: Tree root
            
        Returns:
            List of levels, each level is a list of values
        """
        if not root:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            level_size = len(queue)
            level = []
            
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(level)
        
        return result
    
    @staticmethod
    def level_order_zigzag(root: Optional[TreeNode]) -> List[List[T]]:
        """
        Zigzag level order traversal.
        
        Args:
            root: Tree root
            
        Returns:
            List of levels in zigzag order
        """
        if not root:
            return []
        
        result = []
        queue = deque([root])
        left_to_right = True
        
        while queue:
            level_size = len(queue)
            level = []
            
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            if not left_to_right:
                level.reverse()
            
            result.append(level)
            left_to_right = not left_to_right
        
        return result
    
    @staticmethod
    def max_depth(root: Optional[TreeNode]) -> int:
        """
        Calculate maximum depth of tree.
        
        Args:
            root: Tree root
            
        Returns:
            Maximum depth
        """
        if not root:
            return 0
        
        return 1 + max(TreeAlgorithms.max_depth(root.left), 
                       TreeAlgorithms.max_depth(root.right))
    
    @staticmethod
    def min_depth(root: Optional[TreeNode]) -> int:
        """
        Calculate minimum depth of tree.
        
        Args:
            root: Tree root
            
        Returns:
            Minimum depth
        """
        if not root:
            return 0
        
        if not root.left:
            return 1 + TreeAlgorithms.min_depth(root.right)
        if not root.right:
            return 1 + TreeAlgorithms.min_depth(root.left)
        
        return 1 + min(TreeAlgorithms.min_depth(root.left), 
                       TreeAlgorithms.min_depth(root.right))
    
    @staticmethod
    def is_balanced(root: Optional[TreeNode]) -> bool:
        """
        Check if tree is height-balanced.
        
        Args:
            root: Tree root
            
        Returns:
            True if balanced
        """
        def check(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            
            left_height = check(node.left)
            if left_height == -1:
                return -1
            
            right_height = check(node.right)
            if right_height == -1:
                return -1
            
            if abs(left_height - right_height) > 1:
                return -1
            
            return 1 + max(left_height, right_height)
        
        return check(root) != -1
    
    @staticmethod
    def is_symmetric(root: Optional[TreeNode]) -> bool:
        """
        Check if tree is symmetric.
        
        Args:
            root: Tree root
            
        Returns:
            True if symmetric
        """
        def is_mirror(left: Optional[TreeNode], right: Optional[TreeNode]) -> bool:
            if not left and not right:
                return True
            if not left or not right:
                return False
            
            return (left.val == right.val and
                    is_mirror(left.left, right.right) and
                    is_mirror(left.right, right.left))
        
        if not root:
            return True
        
        return is_mirror(root.left, root.right)
    
    @staticmethod
    def has_path_sum(root: Optional[TreeNode], target: int) -> bool:
        """
        Check if root-to-leaf path sums to target.
        
        Args:
            root: Tree root
            target: Target sum
            
        Returns:
            True if path exists
        """
        if not root:
            return False
        
        if not root.left and not root.right:
            return root.val == target
        
        target -= root.val
        
        return (TreeAlgorithms.has_path_sum(root.left, target) or
                TreeAlgorithms.has_path_sum(root.right, target))
    
    @staticmethod
    def path_sum(root: Optional[TreeNode], target: int) -> List[List[T]]:
        """
        Find all root-to-leaf paths that sum to target.
        
        Args:
            root: Tree root
            target: Target sum
            
        Returns:
            List of paths
        """
        result = []
        
        def find_paths(node: Optional[TreeNode], current: List[T], remaining: int) -> None:
            if not node:
                return
            
            current.append(node.val)
            remaining -= node.val
            
            if not node.left and not node.right and remaining == 0:
                result.append(current.copy())
            else:
                find_paths(node.left, current, remaining)
                find_paths(node.right, current, remaining)
            
            current.pop()
        
        find_paths(root, [], target)
        return result
    
    @staticmethod
    def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Invert binary tree (mirror).
        
        Args:
            root: Tree root
            
        Returns:
            Inverted tree root
        """
        if not root:
            return None
        
        root.left, root.right = root.right, root.left
        TreeAlgorithms.invert_tree(root.left)
        TreeAlgorithms.invert_tree(root.right)
        
        return root
    
    @staticmethod
    def lowest_common_ancestor(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
        """
        Find lowest common ancestor of two nodes.
        
        Args:
            root: Tree root
            p: First node
            q: Second node
            
        Returns:
            LCA node
        """
        if not root or root == p or root == q:
            return root
        
        left = TreeAlgorithms.lowest_common_ancestor(root.left, p, q)
        right = TreeAlgorithms.lowest_common_ancestor(root.right, p, q)
        
        if left and right:
            return root
        
        return left if left else right
    
    @staticmethod
    def count_nodes(root: Optional[TreeNode]) -> int:
        """
        Count total nodes in tree.
        
        Args:
            root: Tree root
            
        Returns:
            Number of nodes
        """
        if not root:
            return 0
        
        return 1 + TreeAlgorithms.count_nodes(root.left) + TreeAlgorithms.count_nodes(root.right)
    
    @staticmethod
    def count_leaves(root: Optional[TreeNode]) -> int:
        """
        Count leaf nodes.
        
        Args:
            root: Tree root
            
        Returns:
            Number of leaf nodes
        """
        if not root:
            return 0
        
        if not root.left and not root.right:
            return 1
        
        return TreeAlgorithms.count_leaves(root.left) + TreeAlgorithms.count_leaves(root.right)
    
    @staticmethod
    def diameter(root: Optional[TreeNode]) -> int:
        """
        Calculate diameter of tree (longest path between any two nodes).
        
        Args:
            root: Tree root
            
        Returns:
            Diameter
        """
        diameter = 0
        
        def height(node: Optional[TreeNode]) -> int:
            nonlocal diameter
            if not node:
                return 0
            
            left_height = height(node.left)
            right_height = height(node.right)
            
            diameter = max(diameter, left_height + right_height)
            
            return 1 + max(left_height, right_height)
        
        height(root)
        return diameter


class BST:
    """Binary Search Tree implementation."""
    
    def __init__(self) -> None:
        """Initialize empty BST."""
        self.root: Optional[TreeNode] = None
    
    def insert(self, val: T) -> None:
        """Insert value into BST."""
        self.root = self._insert(self.root, val)
    
    def _insert(self, node: Optional[TreeNode], val: T) -> TreeNode:
        """Helper for insert."""
        if not node:
            return TreeNode(val)
        
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        
        return node
    
    def search(self, val: T) -> bool:
        """Search for value in BST."""
        return self._search(self.root, val)
    
    def _search(self, node: Optional[TreeNode], val: T) -> bool:
        """Helper for search."""
        if not node:
            return False
        
        if val == node.val:
            return True
        elif val < node.val:
            return self._search(node.left, val)
        else:
            return self._search(node.right, val)
    
    def delete(self, val: T) -> None:
        """Delete value from BST."""
        self.root = self._delete(self.root, val)
    
    def _delete(self, node: Optional[TreeNode], val: T) -> Optional[TreeNode]:
        """Helper for delete."""
        if not node:
            return None
        
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # Node with one child or no child
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            
            # Node with two children: get inorder successor
            temp = self._min_value_node(node.right)
            node.val = temp.val
            node.right = self._delete(node.right, temp.val)
        
        return node
    
    def _min_value_node(self, node: TreeNode) -> TreeNode:
        """Find node with minimum value."""
        current = node
        while current.left:
            current = current.left
        return current
    
    def inorder(self) -> List[T]:
        """Return inorder traversal."""
        return TreeAlgorithms.inorder_traversal(self.root)


def main() -> None:
    """Demonstrate tree algorithms."""
    
    print("=== Tree Algorithms Demo ===")
    
    # Build tree
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    # Traversals
    print("\n--- Traversals ---")
    print(f"Preorder: {TreeAlgorithms.preorder_traversal(root)}")
    print(f"Inorder: {TreeAlgorithms.inorder_traversal(root)}")
    print(f"Postorder: {TreeAlgorithms.postorder_traversal(root)}")
    print(f"Level order: {TreeAlgorithms.level_order_traversal(root)}")
    print(f"Zigzag: {TreeAlgorithms.level_order_zigzag(root)}")
    
    # Tree properties
    print("\n--- Tree Properties ---")
    print(f"Max depth: {TreeAlgorithms.max_depth(root)}")
    print(f"Min depth: {TreeAlgorithms.min_depth(root)}")
    print(f"Is balanced: {TreeAlgorithms.is_balanced(root)}")
    print(f"Is symmetric: {TreeAlgorithms.is_symmetric(root)}")
    print(f"Count nodes: {TreeAlgorithms.count_nodes(root)}")
    print(f"Count leaves: {TreeAlgorithms.count_leaves(root)}")
    print(f"Diameter: {TreeAlgorithms.diameter(root)}")
    
    # Path sum
    print("\n--- Path Sum ---")
    print(f"Has path sum 7: {TreeAlgorithms.has_path_sum(root, 7)}")
    print(f"Paths summing to 7: {TreeAlgorithms.path_sum(root, 7)}")
    
    # Invert tree
    print("\n--- Invert Tree ---")
    print(f"Original inorder: {TreeAlgorithms.inorder_traversal(root)}")
    TreeAlgorithms.invert_tree(root)
    print(f"Inverted inorder: {TreeAlgorithms.inorder_traversal(root)}")
    
    # BST
    print("\n--- Binary Search Tree ---")
    bst = BST()
    for val in [5, 3, 7, 2, 4, 6, 8]:
        bst.insert(val)
    
    print(f"Inorder: {bst.inorder()}")
    print(f"Search 4: {bst.search(4)}")
    print(f"Search 10: {bst.search(10)}")
    
    bst.delete(3)
    print(f"After deleting 3: {bst.inorder()}")


if __name__ == "__main__":
    main()
