"""
Segment Tree - Segment tree for range queries and updates.
Features: Range sum, min, max queries with point updates.
"""

from typing import List, Optional, Callable
import math


class SegmentTree:
    """Segment tree for range queries."""
    
    def __init__(self, data: List[int], operation: str = "sum") -> None:
        """
        Initialize segment tree.
        
        Args:
            data: Initial data array
            operation: Operation type ("sum", "min", "max")
        """
        self.n = len(data)
        self.operation = operation
        self.tree = [0] * (4 * self.n)
        
        if operation == "sum":
            self._func = lambda a, b: a + b
            self._identity = 0
        elif operation == "min":
            self._func = lambda a, b: min(a, b)
            self._identity = math.inf
        elif operation == "max":
            self._func = lambda a, b: max(a, b)
            self._identity = -math.inf
        else:
            raise ValueError("Operation must be 'sum', 'min', or 'max'")
        
        self._build(data, 0, 0, self.n - 1)
    
    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        """Build segment tree."""
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self._build(data, 2 * node + 1, start, mid)
            self._build(data, 2 * node + 2, mid + 1, end)
            self.tree[node] = self._func(self.tree[2 * node + 1], self.tree[2 * node + 2])
    
    def update(self, index: int, value: int) -> None:
        """
        Update value at index.
        
        Args:
            index: Index to update
            value: New value
        """
        self._update_recursive(0, 0, self.n - 1, index, value)
    
    def _update_recursive(self, node: int, start: int, end: int, 
                         index: int, value: int) -> None:
        """Recursively update value."""
        if start == end:
            self.tree[node] = value
        else:
            mid = (start + end) // 2
            if index <= mid:
                self._update_recursive(2 * node + 1, start, mid, index, value)
            else:
                self._update_recursive(2 * node + 2, mid + 1, end, index, value)
            
            self.tree[node] = self._func(self.tree[2 * node + 1], self.tree[2 * node + 2])
    
    def query(self, left: int, right: int) -> int:
        """
        Query range [left, right].
        
        Args:
            left: Left index (inclusive)
            right: Right index (inclusive)
            
        Returns:
            Query result
        """
        return self._query_recursive(0, 0, self.n - 1, left, right)
    
    def _query_recursive(self, node: int, start: int, end: int, 
                        left: int, right: int) -> int:
        """Recursively query range."""
        if right < start or left > end:
            return self._identity
        
        if left <= start and end <= right:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_result = self._query_recursive(2 * node + 1, start, mid, left, right)
        right_result = self._query_recursive(2 * node + 2, mid + 1, end, left, right)
        
        return self._func(left_result, right_result)
    
    def __str__(self) -> str:
        """String representation."""
        return f"SegmentTree(n={self.n}, operation={self.operation})"


class LazySegmentTree:
    """Segment tree with lazy propagation for range updates."""
    
    def __init__(self, data: List[int]) -> None:
        """
        Initialize lazy segment tree.
        
        Args:
            data: Initial data array
        """
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(data, 0, 0, self.n - 1)
    
    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        """Build segment tree."""
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self._build(data, 2 * node + 1, start, mid)
            self._build(data, 2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def _push_down(self, node: int, start: int, end: int) -> None:
        """Push lazy value down to children."""
        if self.lazy[node] != 0:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            
            # Update left child
            self.tree[left_child] += self.lazy[node] * (mid - start + 1)
            self.lazy[left_child] += self.lazy[node]
            
            # Update right child
            self.tree[right_child] += self.lazy[node] * (end - mid)
            self.lazy[right_child] += self.lazy[node]
            
            # Clear lazy value
            self.lazy[node] = 0
    
    def range_update(self, left: int, right: int, value: int) -> None:
        """
        Update range [left, right] by adding value.
        
        Args:
            left: Left index (inclusive)
            right: Right index (inclusive)
            value: Value to add
        """
        self._range_update_recursive(0, 0, self.n - 1, left, right, value)
    
    def _range_update_recursive(self, node: int, start: int, end: int,
                               left: int, right: int, value: int) -> None:
        """Recursively update range."""
        if right < start or left > end:
            return
        
        if left <= start and end <= right:
            self.tree[node] += value * (end - start + 1)
            self.lazy[node] += value
            return
        
        self._push_down(node, start, end)
        
        mid = (start + end) // 2
        self._range_update_recursive(2 * node + 1, start, mid, left, right, value)
        self._range_update_recursive(2 * node + 2, mid + 1, end, left, right, value)
        
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def range_query(self, left: int, right: int) -> int:
        """
        Query range sum [left, right].
        
        Args:
            left: Left index (inclusive)
            right: Right index (inclusive)
            
        Returns:
            Sum of range
        """
        return self._range_query_recursive(0, 0, self.n - 1, left, right)
    
    def _range_query_recursive(self, node: int, start: int, end: int,
                               left: int, right: int) -> int:
        """Recursively query range."""
        if right < start or left > end:
            return 0
        
        if left <= start and end <= right:
            return self.tree[node]
        
        self._push_down(node, start, end)
        
        mid = (start + end) // 2
        left_result = self._range_query_recursive(2 * node + 1, start, mid, left, right)
        right_result = self._range_query_recursive(2 * node + 2, mid + 1, end, left, right)
        
        return left_result + right_result


def main() -> None:
    """Demonstrate segment tree."""
    
    print("=== Segment Tree Demo ===")
    
    data = [1, 3, 5, 7, 9, 11]
    
    # Sum segment tree
    print("--- Sum Segment Tree ---")
    sum_tree = SegmentTree(data, "sum")
    
    print(f"Data: {data}")
    print(f"Sum of [0, 2]: {sum_tree.query(0, 2)}")
    print(f"Sum of [1, 4]: {sum_tree.query(1, 4)}")
    print(f"Sum of [0, 5]: {sum_tree.query(0, 5)}")
    
    print(f"\nUpdate index 2 to 10")
    sum_tree.update(2, 10)
    print(f"Sum of [0, 2]: {sum_tree.query(0, 2)}")
    print(f"Sum of [0, 5]: {sum_tree.query(0, 5)}")
    
    # Min segment tree
    print("\n--- Min Segment Tree ---")
    min_tree = SegmentTree(data, "min")
    
    print(f"Data: {data}")
    print(f"Min of [0, 2]: {min_tree.query(0, 2)}")
    print(f"Min of [1, 4]: {min_tree.query(1, 4)}")
    print(f"Min of [0, 5]: {min_tree.query(0, 5)}")
    
    # Max segment tree
    print("\n--- Max Segment Tree ---")
    max_tree = SegmentTree(data, "max")
    
    print(f"Data: {data}")
    print(f"Max of [0, 2]: {max_tree.query(0, 2)}")
    print(f"Max of [1, 4]: {max_tree.query(1, 4)}")
    print(f"Max of [0, 5]: {max_tree.query(0, 5)}")
    
    # Lazy segment tree
    print("\n=== Lazy Segment Tree Demo ===")
    
    lazy_data = [1, 2, 3, 4, 5]
    lazy_tree = LazySegmentTree(lazy_data)
    
    print(f"Data: {lazy_data}")
    print(f"Sum of [0, 4]: {lazy_tree.range_query(0, 4)}")
    
    print(f"\nAdd 5 to range [1, 3]")
    lazy_tree.range_update(1, 3, 5)
    print(f"Sum of [0, 4]: {lazy_tree.range_query(0, 4)}")
    print(f"Sum of [1, 3]: {lazy_tree.range_query(1, 3)}")
    
    print(f"\nAdd 10 to range [0, 2]")
    lazy_tree.range_update(0, 2, 10)
    print(f"Sum of [0, 4]: {lazy_tree.range_query(0, 4)}")
    
    # Performance comparison
    print("\n=== Performance Test ===")
    import time
    
    n = 100000
    large_data = list(range(n))
    
    # Build segment tree
    start = time.time()
    large_tree = SegmentTree(large_data, "sum")
    build_time = (time.time() - start) * 1000
    
    print(f"Built segment tree with {n} elements in {build_time:.2f}ms")
    
    # Query performance
    start = time.time()
    for _ in range(1000):
        large_tree.query(0, n - 1)
    query_time = (time.time() - start) * 1000
    
    print(f"1000 range queries in {query_time:.2f}ms")
    
    # Update performance
    start = time.time()
    for i in range(0, n, 100):
        large_tree.update(i, i * 2)
    update_time = (time.time() - start) * 1000
    
    print(f"{n//100} point updates in {update_time:.2f}ms")


if __name__ == "__main__":
    main()
