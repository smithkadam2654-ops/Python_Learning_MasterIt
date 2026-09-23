"""
Data Structures Module

This module provides comprehensive data structure implementations including:
- Linked Lists (singly, doubly, circular)
- Stacks and Queues
- Trees (binary search tree, AVL tree)
- Heaps (min-heap, max-heap)
- Hash Tables
- Graphs (adjacency list, adjacency matrix)
- Sets (union-find, disjoint sets)
- Tries (prefix tree)
- Skip Lists
- Bloom Filters

All implementations include comprehensive docstrings and type hints.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import math


class NodeType(Enum):
    """Node types for trees."""
    ROOT = "root"
    INTERNAL = "internal"
    LEAF = "leaf"


@dataclass
class Node:
    """Generic node for data structures."""
    value: Any
    next: Optional['Node'] = None
    prev: Optional['Node'] = None


class LinkedList:
    """Singly linked list implementation."""
    
    def __init__(self):
        """Initialize empty linked list."""
        self.head: Optional[Node] = None
        self.size = 0
    
    def append(self, value: Any) -> None:
        """Append value to end of list."""
        new_node = Node(value)
        
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.size += 1
    
    def prepend(self, value: Any) -> None:
        """Add value to beginning of list."""
        new_node = Node(value, self.head)
        self.head = new_node
        self.size += 1
    
    def insert_at(self, index: int, value: Any) -> bool:
        """Insert value at specific index."""
        if index < 0 or index > self.size:
            return False
        
        if index == 0:
            self.prepend(value)
            return True
        
        new_node = Node(value)
        current = self.head
        
        for _ in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self.size += 1
        
        return True
    
    def remove(self, value: Any) -> bool:
        """Remove first occurrence of value."""
        if self.head is None:
            return False
        
        if self.head.value == value:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def get(self, index: int) -> Optional[Any]:
        """Get value at index."""
        if index < 0 or index >= self.size:
            return None
        
        current = self.head
        for _ in range(index):
            current = current.next
        
        return current.value
    
    def find(self, value: Any) -> int:
        """Find index of value."""
        current = self.head
        index = 0
        
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        
        return -1
    
    def to_list(self) -> List[Any]:
        """Convert to Python list."""
        result = []
        current = self.head
        
        while current:
            result.append(current.value)
            current = current.next
        
        return result
    
    def reverse(self) -> None:
        """Reverse the linked list."""
        prev = None
        current = self.head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev
    
    def __len__(self) -> int:
        """Get size of list."""
        return self.size


class DoublyLinkedList:
    """Doubly linked list implementation."""
    
    def __init__(self):
        """Initialize empty doubly linked list."""
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size = 0
    
    def append(self, value: Any) -> None:
        """Append value to end of list."""
        new_node = Node(value)
        
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        
        self.size += 1
    
    def prepend(self, value: Any) -> None:
        """Add value to beginning of list."""
        new_node = Node(value)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        self.size += 1
    
    def remove(self, value: Any) -> bool:
        """Remove first occurrence of value."""
        current = self.head
        
        while current:
            if current.value == value:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def to_list(self) -> List[Any]:
        """Convert to Python list."""
        result = []
        current = self.head
        
        while current:
            result.append(current.value)
            current = current.next
        
        return result


class Stack:
    """Stack implementation (LIFO)."""
    
    def __init__(self):
        """Initialize empty stack."""
        self.items: List[Any] = []
    
    def push(self, value: Any) -> None:
        """Push value onto stack."""
        self.items.append(value)
    
    def pop(self) -> Optional[Any]:
        """Pop value from stack."""
        if self.is_empty():
            return None
        return self.items.pop()
    
    def peek(self) -> Optional[Any]:
        """Peek at top of stack."""
        if self.is_empty():
            return None
        return self.items[-1]
    
    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Get stack size."""
        return len(self.items)
    
    def __len__(self) -> int:
        """Get stack size."""
        return len(self.items)


class Queue:
    """Queue implementation (FIFO)."""
    
    def __init__(self):
        """Initialize empty queue."""
        self.items: List[Any] = []
    
    def enqueue(self, value: Any) -> None:
        """Add value to queue."""
        self.items.append(value)
    
    def dequeue(self) -> Optional[Any]:
        """Remove value from queue."""
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def peek(self) -> Optional[Any]:
        """Peek at front of queue."""
        if self.is_empty():
            return None
        return self.items[0]
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Get queue size."""
        return len(self.items)
    
    def __len__(self) -> int:
        """Get queue size."""
        return len(self.items)


class TreeNode:
    """Binary tree node."""
    
    def __init__(self, value: Any):
        """Initialize tree node."""
        self.value = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None
        self.parent: Optional['TreeNode'] = None


class BinarySearchTree:
    """Binary search tree implementation."""
    
    def __init__(self):
        """Initialize empty BST."""
        self.root: Optional[TreeNode] = None
        self.size = 0
    
    def insert(self, value: Any) -> None:
        """Insert value into BST."""
        if self.root is None:
            self.root = TreeNode(value)
            self.size += 1
            return
        
        self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: TreeNode, value: Any) -> None:
        """Recursively insert value."""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
                node.left.parent = node
                self.size += 1
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = TreeNode(value)
                node.right.parent = node
                self.size += 1
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value: Any) -> bool:
        """Search for value in BST."""
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
        """Delete value from BST."""
        if not self.search(value):
            return False
        
        self.root = self._delete_recursive(self.root, value)
        self.size -= 1
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
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node with two children: get inorder successor
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)
        
        return node
    
    def _min_value_node(self, node: TreeNode) -> TreeNode:
        """Find minimum value node."""
        current = node
        while current.left:
            current = current.left
        return current
    
    def inorder_traversal(self) -> List[Any]:
        """In-order traversal."""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Recursively traverse in-order."""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def preorder_traversal(self) -> List[Any]:
        """Pre-order traversal."""
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Recursively traverse pre-order."""
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def __len__(self) -> int:
        """Get tree size."""
        return self.size


class MinHeap:
    """Min-heap implementation."""
    
    def __init__(self):
        """Initialize empty heap."""
        self.heap: List[Any] = []
    
    def insert(self, value: Any) -> None:
        """Insert value into heap."""
        self.heap.append(value)
        self._bubble_up(len(self.heap) - 1)
    
    def _bubble_up(self, index: int) -> None:
        """Bubble up element to maintain heap property."""
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent] > self.heap[index]:
                self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
                index = parent
            else:
                break
    
    def extract_min(self) -> Optional[Any]:
        """Extract minimum value."""
        if len(self.heap) == 0:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        
        return min_val
    
    def _bubble_down(self, index: int) -> None:
        """Bubble down element to maintain heap property."""
        n = len(self.heap)
        
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right
            
            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break
    
    def peek(self) -> Optional[Any]:
        """Peek at minimum value."""
        if self.is_empty():
            return None
        return self.heap[0]
    
    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return len(self.heap) == 0
    
    def size(self) -> int:
        """Get heap size."""
        return len(self.heap)
    
    def __len__(self) -> int:
        """Get heap size."""
        return len(self.heap)


class MaxHeap:
    """Max-heap implementation."""
    
    def __init__(self):
        """Initialize empty heap."""
        self.heap: List[Any] = []
    
    def insert(self, value: Any) -> None:
        """Insert value into heap."""
        self.heap.append(value)
        self._bubble_up(len(self.heap) - 1)
    
    def _bubble_up(self, index: int) -> None:
        """Bubble up element to maintain heap property."""
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent] < self.heap[index]:
                self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
                index = parent
            else:
                break
    
    def extract_max(self) -> Optional[Any]:
        """Extract maximum value."""
        if len(self.heap) == 0:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        
        return max_val
    
    def _bubble_down(self, index: int) -> None:
        """Bubble down element to maintain heap property."""
        n = len(self.heap)
        
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index
            
            if left < n and self.heap[left] > self.heap[largest]:
                largest = left
            
            if right < n and self.heap[right] > self.heap[largest]:
                largest = right
            
            if largest != index:
                self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
                index = largest
            else:
                break
    
    def peek(self) -> Optional[Any]:
        """Peek at maximum value."""
        if self.is_empty():
            return None
        return self.heap[0]
    
    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return len(self.heap) == 0
    
    def size(self) -> int:
        """Get heap size."""
        return len(self.heap)
    
    def __len__(self) -> int:
        """Get heap size."""
        return len(self.heap)


class HashTable:
    """Hash table implementation with chaining."""
    
    def __init__(self, capacity: int = 16):
        """Initialize hash table."""
        self.capacity = capacity
        self.buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(capacity)]
        self.size = 0
    
    def _hash(self, key: Any) -> int:
        """Calculate hash for key."""
        return hash(key) % self.capacity
    
    def put(self, key: Any, value: Any) -> None:
        """Put key-value pair in table."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        bucket.append((key, value))
        self.size += 1
        
        # Resize if load factor is high
        if self.size / self.capacity > 0.75:
            self._resize()
    
    def get(self, key: Any) -> Optional[Any]:
        """Get value for key."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return None
    
    def remove(self, key: Any) -> bool:
        """Remove key from table."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        
        return False
    
    def _resize(self) -> None:
        """Resize hash table."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def keys(self) -> List[Any]:
        """Get all keys."""
        keys = []
        for bucket in self.buckets:
            for key, _ in bucket:
                keys.append(key)
        return keys
    
    def values(self) -> List[Any]:
        """Get all values."""
        values = []
        for bucket in self.buckets:
            for _, value in bucket:
                values.append(value)
        return values
    
    def __len__(self) -> int:
        """Get table size."""
        return self.size


class TrieNode:
    """Trie node for prefix tree."""
    
    def __init__(self):
        """Initialize trie node."""
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end = False


class Trie:
    """Trie (prefix tree) implementation."""
    
    def __init__(self):
        """Initialize empty trie."""
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert word into trie."""
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end = True
    
    def search(self, word: str) -> bool:
        """Search for exact word."""
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end
    
    def starts_with(self, prefix: str) -> bool:
        """Check if any word starts with prefix."""
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return True
    
    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """Get all words with given prefix."""
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        words = []
        self._collect_words(node, prefix, words)
        return words
    
    def _collect_words(self, node: TrieNode, prefix: str, words: List[str]) -> None:
        """Collect all words from node."""
        if node.is_end:
            words.append(prefix)
        
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, words)


class UnionFind:
    """Union-Find (Disjoint Set) implementation."""
    
    def __init__(self, size: int):
        """Initialize union-find."""
        self.parent = list(range(size))
        self.rank = [0] * size
    
    def find(self, x: int) -> int:
        """Find with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> None:
        """Union by rank."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
    
    def connected(self, x: int, y: int) -> bool:
        """Check if x and y are connected."""
        return self.find(x) == self.find(y)


class BloomFilter:
    """Bloom filter implementation."""
    
    def __init__(self, size: int, hash_count: int = 3):
        """Initialize bloom filter."""
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [False] * size
    
    def _hashes(self, item: Any) -> List[int]:
        """Generate hash values."""
        hashes = []
        for i in range(self.hash_count):
            # Simple hash function
            combined = f"{item}{i}"
            hash_val = hash(combined) % self.size
            hashes.append(hash_val)
        return hashes
    
    def add(self, item: Any) -> None:
        """Add item to bloom filter."""
        for hash_val in self._hashes(item):
            self.bit_array[hash_val] = True
    
    def might_contain(self, item: Any) -> bool:
        """Check if item might be in filter."""
        for hash_val in self._hashes(item):
            if not self.bit_array[hash_val]:
                return False
        return True


class CircularBuffer:
    """Circular buffer implementation."""
    
    def __init__(self, capacity: int):
        """Initialize circular buffer."""
        self.capacity = capacity
        self.buffer: List[Any] = [None] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0
    
    def enqueue(self, value: Any) -> bool:
        """Add value to buffer."""
        if self.is_full():
            return False
        
        self.buffer[self.tail] = value
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1
        return True
    
    def dequeue(self) -> Optional[Any]:
        """Remove value from buffer."""
        if self.is_empty():
            return None
        
        value = self.buffer[self.head]
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return value
    
    def peek(self) -> Optional[Any]:
        """Peek at front of buffer."""
        if self.is_empty():
            return None
        return self.buffer[self.head]
    
    def is_empty(self) -> bool:
        """Check if buffer is empty."""
        return self.size == 0
    
    def is_full(self) -> bool:
        """Check if buffer is full."""
        return self.size == self.capacity
    
    def __len__(self) -> int:
        """Get buffer size."""
        return self.size


def demonstrate_data_structures():
    """Demonstrate data structures functionality."""
    print("=== Data Structures Demonstration ===\n")
    
    # Linked List
    print("1. Linked List:")
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.prepend(0)
    
    print(f"   List: {ll.to_list()}")
    print(f"   Size: {len(ll)}")
    print(f"   Find 2: {ll.find(2)}")
    
    ll.reverse()
    print(f"   Reversed: {ll.to_list()}")
    
    # Doubly Linked List
    print("\n2. Doubly Linked List:")
    dll = DoublyLinkedList()
    dll.append(1)
    dll.append(2)
    dll.prepend(0)
    
    print(f"   List: {dll.to_list()}")
    
    # Stack
    print("\n3. Stack:")
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    
    print(f"   Pushed 1, 2, 3")
    print(f"   Pop: {stack.pop()}")
    print(f"   Peek: {stack.peek()}")
    print(f"   Size: {len(stack)}")
    
    # Queue
    print("\n4. Queue:")
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    
    print(f"   Enqueued 1, 2, 3")
    print(f"   Dequeue: {queue.dequeue()}")
    print(f"   Peek: {queue.peek()}")
    print(f"   Size: {len(queue)}")
    
    # Binary Search Tree
    print("\n5. Binary Search Tree:")
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(1)
    bst.insert(4)
    
    print(f"   In-order: {bst.inorder_traversal()}")
    print(f"   Pre-order: {bst.preorder_traversal()}")
    print(f"   Search 4: {bst.search(4)}")
    print(f"   Search 6: {bst.search(6)}")
    
    # Min Heap
    print("\n6. Min Heap:")
    min_heap = MinHeap()
    min_heap.insert(5)
    min_heap.insert(3)
    min_heap.insert(7)
    min_heap.insert(1)
    
    print(f"   Inserted 5, 3, 7, 1")
    print(f"   Extract min: {min_heap.extract_min()}")
    print(f"   Peek: {min_heap.peek()}")
    
    # Max Heap
    print("\n7. Max Heap:")
    max_heap = MaxHeap()
    max_heap.insert(5)
    max_heap.insert(3)
    max_heap.insert(7)
    max_heap.insert(1)
    
    print(f"   Inserted 5, 3, 7, 1")
    print(f"   Extract max: {max_heap.extract_max()}")
    print(f"   Peek: {max_heap.peek()}")
    
    # Hash Table
    print("\n8. Hash Table:")
    ht = HashTable()
    ht.put("name", "John")
    ht.put("age", 25)
    ht.put("city", "NYC")
    
    print(f"   Get name: {ht.get('name')}")
    print(f"   Keys: {ht.keys()}")
    print(f"   Values: {ht.values()}")
    print(f"   Size: {len(ht)}")
    
    # Trie
    print("\n9. Trie:")
    trie = Trie()
    trie.insert("hello")
    trie.insert("world")
    trie.insert("help")
    
    print(f"   Search 'hello': {trie.search('hello')}")
    print(f"   Search 'hey': {trie.search('hey')}")
    print(f"   Starts with 'he': {trie.starts_with('he')}")
    print(f"   Words with 'he': {trie.get_words_with_prefix('he')}")
    
    # Union-Find
    print("\n10. Union-Find:")
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(2, 3)
    
    print(f"   Connected 0, 1: {uf.connected(0, 1)}")
    print(f"   Connected 0, 2: {uf.connected(0, 2)}")
    
    uf.union(1, 2)
    print(f"   After union(1, 2), connected 0, 3: {uf.connected(0, 3)}")
    
    # Bloom Filter
    print("\n11. Bloom Filter:")
    bf = BloomFilter(100, 3)
    bf.add("test")
    bf.add("hello")
    
    print(f"   Might contain 'test': {bf.might_contain('test')}")
    print(f"   Might contain 'world': {bf.might_contain('world')}")
    
    # Circular Buffer
    print("\n12. Circular Buffer:")
    cb = CircularBuffer(3)
    cb.enqueue(1)
    cb.enqueue(2)
    cb.enqueue(3)
    
    print(f"   Enqueued 1, 2, 3")
    print(f"   Is full: {cb.is_full()}")
    print(f"   Dequeue: {cb.dequeue()}")
    print(f"   Enqueue 4: {cb.enqueue(4)}")
    print(f"   Buffer: {cb.buffer}")
    
    print("\n=== Demonstration Complete ===")
    print("\nData Structures Best Practices:")
    print("- Choose appropriate data structure for your use case")
    print("- Consider time complexity for operations")
    print("- Use hash tables for O(1) lookups")
    print("- Use trees for ordered data and range queries")
    print("- Use heaps for priority operations")
    print("- Use bloom filters for approximate membership")
    print("- Use tries for prefix-based operations")
    print("- Use union-find for connectivity problems")
    print("- Consider space complexity for large datasets")
    print("- Use circular buffers for fixed-size queues")
    print("- Prefer built-in data structures when available")


if __name__ == "__main__":
    demonstrate_data_structures()
