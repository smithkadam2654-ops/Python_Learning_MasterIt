"""
Advanced Python - Lesson 20: Advanced Data Structures
======================================================
Beyond lists and dicts, Python can implement powerful data structures
for efficient searching, sorting, and graph operations.

Topics Covered:
- Binary Search Tree (BST)
- Priority Queue / Min-Heap
- Trie (prefix tree)
- Disjoint Set (Union-Find)
- Graph (adjacency list with BFS/DFS)
- Linked List
- LRU Cache (from scratch)
"""

from typing import Any, Optional
from collections import deque
import heapq


# ============================================================
# 1. BINARY SEARCH TREE
# ============================================================
class BSTNode:
    """Node in a Binary Search Tree."""
    def __init__(self, value: int):
        self.value = value
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None


class BinarySearchTree:
    """Binary Search Tree with insert, search, delete, and traversals."""
    
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, value: int):
        """Insert a value into the BST."""
        if self.root is None:
            self.root = BSTNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node: BSTNode, value: int):
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value)
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = BSTNode(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value: int) -> bool:
        """Search for a value in the BST."""
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node: Optional[BSTNode], value: int) -> bool:
        if node is None:
            return False
        if value == node.value:
            return True
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    def inorder(self) -> list[int]:
        """In-order traversal: returns sorted values."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[BSTNode], result: list):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def preorder(self) -> list[int]:
        """Pre-order traversal."""
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node: Optional[BSTNode], result: list):
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self) -> list[int]:
        """Post-order traversal."""
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node: Optional[BSTNode], result: list):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)

    def min_value(self) -> int:
        """Find the minimum value."""
        node = self.root
        while node.left:
            node = node.left
        return node.value

    def max_value(self) -> int:
        """Find the maximum value."""
        node = self.root
        while node.right:
            node = node.right
        return node.value

    def height(self) -> int:
        """Calculate tree height."""
        return self._height(self.root)

    def _height(self, node: Optional[BSTNode]) -> int:
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))


def demonstrate_bst():
    """BST keeps elements sorted for fast lookups."""
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 35, 45]
    
    for v in values:
        bst.insert(v)
    
    print(f"Inserted: {values}")
    print(f"In-order (sorted):  {bst.inorder()}")
    print(f"Pre-order:          {bst.preorder()}")
    print(f"Post-order:         {bst.postorder()}")
    print(f"Min: {bst.min_value()}, Max: {bst.max_value()}")
    print(f"Height: {bst.height()}")
    print(f"Search 40: {bst.search(40)}")
    print(f"Search 99: {bst.search(99)}")


# ============================================================
# 2. PRIORITY QUEUE / MIN-HEAP
# ============================================================
class PriorityQueue:
    """Priority queue backed by Python's heapq module.
    
    Lower priority number = higher priority.
    """
    def __init__(self):
        self._heap: list[tuple[int, int, Any]] = []
        self._counter = 0  # Tie-breaker for equal priorities

    def push(self, item: Any, priority: int = 0):
        """Add an item with a priority."""
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self) -> Any:
        """Remove and return the highest-priority item."""
        if not self._heap:
            raise IndexError("Priority queue is empty")
        return heapq.heappop(self._heap)[2]

    def peek(self) -> Any:
        """View the highest-priority item without removing it."""
        if not self._heap:
            raise IndexError("Priority queue is empty")
        return self._heap[0][2]

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return len(self._heap) > 0


def demonstrate_priority_queue():
    """Priority queue processes items by importance, not insertion order."""
    pq = PriorityQueue()
    
    tasks = [
        ("Send email", 3),
        ("Fix critical bug", 1),
        ("Update docs", 5),
        ("Deploy hotfix", 1),
        ("Refactor code", 4),
        ("Review PR", 2),
    ]
    
    print("Adding tasks:")
    for task, priority in tasks:
        pq.push(task, priority)
        print(f"  [{priority}] {task}")
    
    print("\nProcessing order (lowest number first):")
    while pq:
        task = pq.pop()
        print(f"  Processing: {task}")


# ============================================================
# 3. TRIE (PREFIX TREE)
# ============================================================
class TrieNode:
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end: bool = False
        self.count: int = 0  # How many words pass through this node


class Trie:
    """Trie for efficient prefix-based string operations."""
    
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        """Insert a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1
        node.is_end = True

    def search(self, word: str) -> bool:
        """Check if a word exists in the trie."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Check if any word starts with the given prefix."""
        return self._find_node(prefix) is not None

    def count_prefix(self, prefix: str) -> int:
        """Count how many words have this prefix."""
        node = self._find_node(prefix)
        return node.count if node else 0

    def autocomplete(self, prefix: str, max_results: int = 10) -> list[str]:
        """Find all words with the given prefix."""
        node = self._find_node(prefix)
        if node is None:
            return []
        results = []
        self._dfs(node, prefix, results, max_results)
        return results

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _dfs(self, node: TrieNode, path: str, results: list, max_results: int):
        if len(results) >= max_results:
            return
        if node.is_end:
            results.append(path)
        for char in sorted(node.children):
            self._dfs(node.children[char], path + char, results, max_results)


def demonstrate_trie():
    """Trie enables fast prefix-based lookups."""
    trie = Trie()
    
    words = [
        "apple", "application", "apply", "appetite",
        "banana", "band", "bandwidth",
        "cat", "category", "catalog",
        "dog", "document", "docker",
    ]
    
    for word in words:
        trie.insert(word)
    
    print(f"Inserted {len(words)} words")
    
    print(f"\nSearch 'apple': {trie.search('apple')}")
    print(f"Search 'app': {trie.search('app')}")
    print(f"Prefix 'app': {trie.starts_with('app')}")
    print(f"Count 'app': {trie.count_prefix('app')}")
    
    print(f"\nAutocomplete 'app': {trie.autocomplete('app')}")
    print(f"Autocomplete 'ban': {trie.autocomplete('ban')}")
    print(f"Autocomplete 'do':  {trie.autocomplete('do')}")
    print(f"Autocomplete 'cat': {trie.autocomplete('cat')}")


# ============================================================
# 4. DISJOINT SET (UNION-FIND)
# ============================================================
class DisjointSet:
    """Union-Find with path compression and union by rank.
    
    Efficiently tracks connected components.
    Used in: Kruskal's MST, connected components, cycle detection.
    """
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        """Find root with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union by rank. Returns False if already in same set."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Check if two elements are in the same set."""
        return self.find(x) == self.find(y)


def demonstrate_union_find():
    """Union-Find for connectivity problems."""
    # Simulate a social network
    ds = DisjointSet(7)  # 7 people: 0-6
    
    friendships = [(0, 1), (1, 2), (3, 4), (5, 6), (2, 3)]
    
    print("Building friendships:")
    for a, b in friendships:
        ds.union(a, b)
        print(f"  {a}-{b}: {ds.components} groups remaining")
    
    print(f"\n0 connected to 4? {ds.connected(0, 4)}")  # True (0-1-2-3-4)
    print(f"0 connected to 5? {ds.connected(0, 5)}")  # False
    print(f"5 connected to 6? {ds.connected(5, 6)}")  # True
    
    ds.union(4, 5)  # Connect the two groups
    print(f"\nAfter connecting 4-5:")
    print(f"0 connected to 5? {ds.connected(0, 5)}")  # Now True
    print(f"Total groups: {ds.components}")


# ============================================================
# 5. GRAPH (Adjacency List)
# ============================================================
class Graph:
    """Weighted directed graph with BFS, DFS, and shortest path."""
    
    def __init__(self, directed: bool = True):
        self.directed = directed
        self.adj: dict[str, list[tuple[str, float]]] = {}

    def add_edge(self, u: str, v: str, weight: float = 1.0):
        self.adj.setdefault(u, []).append((v, weight))
        if not self.directed:
            self.adj.setdefault(v, []).append((u, weight))
        self.adj.setdefault(v, [])  # Ensure v exists
        self.adj.setdefault(u, [])

    def bfs(self, start: str) -> list[str]:
        """Breadth-first search."""
        visited = set()
        queue = deque([start])
        order = []
        
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                order.append(node)
                for neighbor, _ in self.adj.get(node, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return order

    def dfs(self, start: str) -> list[str]:
        """Depth-first search (iterative)."""
        visited = set()
        stack = [start]
        order = []
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                order.append(node)
                # Add neighbors in reverse for left-first traversal
                for neighbor, _ in reversed(self.adj.get(node, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return order

    def dijkstra(self, start: str) -> dict[str, float]:
        """Dijkstra's shortest path algorithm."""
        dist: dict[str, float] = {start: 0}
        pq = [(0, start)]
        visited = set()
        
        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            
            for v, w in self.adj.get(u, []):
                new_dist = d + w
                if new_dist < dist.get(v, float("inf")):
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))
        
        return dist

    def has_path(self, start: str, end: str) -> bool:
        """Check if a path exists between two nodes."""
        visited = set()
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node == end:
                return True
            if node not in visited:
                visited.add(node)
                for neighbor, _ in self.adj.get(node, []):
                    queue.append(neighbor)
        return False


def demonstrate_graph():
    """Graph with BFS, DFS, and shortest path."""
    g = Graph(directed=True)
    
    # Build a road network
    edges = [
        ("A", "B", 4), ("A", "C", 2),
        ("B", "D", 3), ("B", "C", 1),
        ("C", "D", 5), ("C", "E", 8),
        ("D", "E", 2), ("D", "F", 6),
        ("E", "F", 1),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    
    print("Graph edges:")
    for u, neighbors in sorted(g.adj.items()):
        for v, w in neighbors:
            print(f"  {u} --({w})--> {v}")
    
    print(f"\nBFS from A: {g.bfs('A')}")
    print(f"DFS from A: {g.dfs('A')}")
    
    distances = g.dijkstra("A")
    print(f"\nShortest paths from A:")
    for node, dist in sorted(distances.items()):
        print(f"  A -> {node}: {dist}")
    
    print(f"\nPath A->F exists? {g.has_path('A', 'F')}")
    print(f"Path F->A exists? {g.has_path('F', 'A')}")


# ============================================================
# 6. DOUBLY LINKED LIST
# ============================================================
class DLLNode:
    def __init__(self, value: Any):
        self.value = value
        self.prev: Optional["DLLNode"] = None
        self.next: Optional["DLLNode"] = None


class DoublyLinkedList:
    """Doubly linked list with O(1) operations at both ends."""
    
    def __init__(self):
        self.head: Optional[DLLNode] = None
        self.tail: Optional[DLLNode] = None
        self._size = 0

    def append(self, value: Any):
        """Add to end — O(1)."""
        node = DLLNode(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    def prepend(self, value: Any):
        """Add to beginning — O(1)."""
        node = DLLNode(value)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1

    def pop_back(self) -> Any:
        """Remove from end — O(1)."""
        if self.tail is None:
            raise IndexError("List is empty")
        value = self.tail.value
        if self.tail.prev:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            self.head = self.tail = None
        self._size -= 1
        return value

    def pop_front(self) -> Any:
        """Remove from beginning — O(1)."""
        if self.head is None:
            raise IndexError("List is empty")
        value = self.head.value
        if self.head.next:
            self.head = self.head.next
            self.head.prev = None
        else:
            self.head = self.tail = None
        self._size -= 1
        return value

    def to_list(self) -> list:
        """Convert to Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    def to_list_reversed(self) -> list:
        """Traverse in reverse."""
        result = []
        current = self.tail
        while current:
            result.append(current.value)
            current = current.prev
        return result

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        items = " <-> ".join(str(v) for v in self)
        return f"DLL[{items}]"


def demonstrate_linked_list():
    """Doubly linked list with O(1) operations at both ends."""
    dll = DoublyLinkedList()
    
    for v in [10, 20, 30, 40, 50]:
        dll.append(v)
    
    print(f"List: {dll}")
    print(f"Reversed: {dll.to_list_reversed()}")
    
    dll.prepend(5)
    dll.append(60)
    print(f"After prepend(5), append(60): {dll}")
    
    print(f"pop_front: {dll.pop_front()}")
    print(f"pop_back:  {dll.pop_back()}")
    print(f"Final: {dll} (length={len(dll)})")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Binary Search Tree")
    demonstrate_bst()

    separator("2. Priority Queue (Min-Heap)")
    demonstrate_priority_queue()

    separator("3. Trie (Prefix Tree)")
    demonstrate_trie()

    separator("4. Disjoint Set (Union-Find)")
    demonstrate_union_find()

    separator("5. Graph (BFS, DFS, Dijkstra)")
    demonstrate_graph()

    separator("6. Doubly Linked List")
    demonstrate_linked_list()


if __name__ == "__main__":
    main()
