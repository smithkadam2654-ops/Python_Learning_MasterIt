"""
Fibonacci Heap - Fibonacci heap for priority queue operations.
Features: O(1) insert, decrease-key, and amortized O(log n) delete-min.
"""

from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')


class FibonacciNode(Generic[T]):
    """Node in Fibonacci heap."""
    
    def __init__(self, key: int, value: Optional[T] = None) -> None:
        """
        Initialize node.
        
        Args:
            key: Node key
            value: Node value
        """
        self.key = key
        self.value = value
        self.degree = 0
        self.parent: Optional['FibonacciNode[T]'] = None
        self.child: Optional['FibonacciNode[T]'] = None
        self.left: 'FibonacciNode[T]' = self
        self.right: 'FibonacciNode[T]' = self
        self.mark = False
    
    def __str__(self) -> str:
        """String representation."""
        return f"Node(key={self.key}, value={self.value})"


class FibonacciHeap(Generic[T]):
    """Fibonacci heap implementation."""
    
    def __init__(self) -> None:
        """Initialize Fibonacci heap."""
        self.min: Optional[FibonacciNode[T]] = None
        self.total_nodes = 0
    
    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return self.min is None
    
    def insert(self, key: int, value: Optional[T] = None) -> FibonacciNode[T]:
        """
        Insert node into heap.
        
        Args:
            key: Node key
            value: Node value
            
        Returns:
            Inserted node
        """
        node = FibonacciNode(key, value)
        
        if self.min is None:
            self.min = node
        else:
            self._add_to_root_list(node)
            if node.key < self.min.key:
                self.min = node
        
        self.total_nodes += 1
        return node
    
    def _add_to_root_list(self, node: FibonacciNode[T]) -> None:
        """Add node to root list."""
        if self.min is None:
            self.min = node
            node.left = node
            node.right = node
        else:
            # Insert node into root list
            node.left = self.min
            node.right = self.min.right
            self.min.right.left = node
            self.min.right = node
    
    def find_min(self) -> Optional[FibonacciNode[T]]:
        """
        Find minimum node.
        
        Returns:
            Minimum node or None if empty
        """
        return self.min
    
    def extract_min(self) -> Optional[FibonacciNode[T]]:
        """
        Extract minimum node.
        
        Returns:
            Minimum node or None if empty
        """
        if self.is_empty():
            return None
        
        min_node = self.min
        
        # Add children to root list
        if min_node.child is not None:
            child = min_node.child
            while True:
                next_child = child.right
                self._add_to_root_list(child)
                child.parent = None
                if child == next_child:
                    break
                child = next_child
        
        # Remove min from root list
        if min_node == min_node.right:
            self.min = None
        else:
            self.min = min_node.right
            self._remove_from_root_list(min_node)
            self._consolidate()
        
        self.total_nodes -= 1
        return min_node
    
    def _remove_from_root_list(self, node: FibonacciNode[T]) -> None:
        """Remove node from root list."""
        if node == node.right:
            return
        node.left.right = node.right
        node.right.left = node.left
    
    def _consolidate(self) -> None:
        """Consolidate trees in root list."""
        max_degree = self._calculate_max_degree()
        degree_table: List[Optional[FibonacciNode[T]]] = [None] * (max_degree + 1)
        
        nodes_to_process = []
        current = self.min
        
        # Collect all root nodes
        while True:
            nodes_to_process.append(current)
            current = current.right
            if current == self.min:
                break
        
        for node in nodes_to_process:
            degree = node.degree
            
            while degree_table[degree] is not None:
                other = degree_table[degree]
                
                if node.key > other.key:
                    node, other = other, node
                
                self._link(other, node)
                degree_table[degree] = None
                degree += 1
            
            degree_table[degree] = node
        
        # Find new minimum
        self.min = None
        for node in degree_table:
            if node is not None:
                if self.min is None or node.key < self.min.key:
                    self.min = node
    
    def _calculate_max_degree(self) -> int:
        """Calculate maximum possible degree."""
        import math
        return int(math.log(self.total_nodes, 1.618)) + 1
    
    def _link(self, child: FibonacciNode[T], parent: FibonacciNode[T]) -> None:
        """Link child under parent."""
        self._remove_from_root_list(child)
        child.parent = parent
        
        if parent.child is None:
            parent.child = child
            child.left = child
            child.right = child
        else:
            child.left = parent.child
            child.right = parent.child.right
            parent.child.right.left = child
            parent.child.right = child
        
        parent.degree += 1
        child.mark = False
    
    def decrease_key(self, node: FibonacciNode[T], new_key: int) -> bool:
        """
        Decrease key of node.
        
        Args:
            node: Node to update
            new_key: New key value
            
        Returns:
            True if successful
        """
        if new_key > node.key:
            return False
        
        node.key = new_key
        parent = node.parent
        
        if parent is not None and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)
        
        if node.key < self.min.key:
            self.min = node
        
        return True
    
    def _cut(self, node: FibonacciNode[T], parent: FibonacciNode[T]) -> None:
        """Cut node from parent."""
        if node.right == node:
            parent.child = None
        else:
            if parent.child == node:
                parent.child = node.right
            node.left.right = node.right
            node.right.left = node.left
        
        parent.degree -= 1
        self._add_to_root_list(node)
        node.parent = None
        node.mark = False
    
    def _cascading_cut(self, node: FibonacciNode[T]) -> None:
        """Perform cascading cut."""
        parent = node.parent
        
        if parent is not None:
            if not node.mark:
                node.mark = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)
    
    def delete(self, node: FibonacciNode[T]) -> bool:
        """
        Delete node from heap.
        
        Args:
            node: Node to delete
            
        Returns:
            True if successful
        """
        self.decrease_key(node, float('-inf'))
        self.extract_min()
        return True
    
    def size(self) -> int:
        """Get number of nodes."""
        return self.total_nodes
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return "FibonacciHeap(empty)"
        return f"FibonacciHeap(min={self.min.key}, nodes={self.total_nodes})"


def main() -> None:
    """Demonstrate Fibonacci heap."""
    
    print("=== Fibonacci Heap Demo ===")
    
    fh = FibonacciHeap[str]()
    
    # Insert
    print("--- Insert ---")
    fh.insert(5, "Five")
    fh.insert(3, "Three")
    fh.insert(7, "Seven")
    fh.insert(1, "One")
    fh.insert(9, "Nine")
    
    print(f"Heap: {fh}")
    print(f"Min: {fh.find_min()}")
    
    # Extract min
    print("\n--- Extract Min ---")
    while not fh.is_empty():
        min_node = fh.extract_min()
        print(f"Extracted: {min_node}")
        print(f"Heap: {fh}")
    
    # Decrease key
    print("\n--- Decrease Key ---")
    fh2 = FibonacciHeap[str]()
    
    node1 = fh2.insert(10, "Ten")
    node2 = fh2.insert(5, "Five")
    node3 = fh2.insert(15, "Fifteen")
    
    print(f"Heap: {fh2}")
    print(f"Min: {fh2.find_min()}")
    
    print(f"\nDecrease key of 'Ten' to 3")
    fh2.decrease_key(node1, 3)
    print(f"Heap: {fh2}")
    print(f"Min: {fh2.find_min()}")
    
    # Delete
    print("\n--- Delete ---")
    fh3 = FibonacciHeap[str]()
    
    node_a = fh3.insert(20, "A")
    node_b = fh3.insert(10, "B")
    node_c = fh3.insert(30, "C")
    
    print(f"Heap: {fh3}")
    
    print(f"\nDelete 'B'")
    fh3.delete(node_b)
    print(f"Heap: {fh3}")
    print(f"Min: {fh3.find_min()}")
    
    # Performance test
    print("\n=== Performance Test ===")
    import time
    
    large_fh = FibonacciHeap[int]()
    n = 10000
    
    start = time.time()
    for i in range(n):
        large_fh.insert(i, f"Value{i}")
    insert_time = (time.time() - start) * 1000
    
    print(f"Inserted {n} items in {insert_time:.2f}ms")
    
    start = time.time()
    for _ in range(n // 2):
        large_fh.extract_min()
    extract_time = (time.time() - start) * 1000
    
    print(f"Extracted {n//2} items in {extract_time:.2f}ms")


if __name__ == "__main__":
    main()
