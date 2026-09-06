"""
Doubly Linked List - Doubly linked list implementation.
Features: Insert, delete, traverse forward and backward.
"""

from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')


class Node(Generic[T]):
    """Node in doubly linked list."""
    
    def __init__(self, data: T) -> None:
        """
        Initialize node.
        
        Args:
            data: Node data
        """
        self.data = data
        self.prev: Optional['Node[T]'] = None
        self.next: Optional['Node[T]'] = None
    
    def __str__(self) -> str:
        """String representation."""
        return str(self.data)


class DoublyLinkedList(Generic[T]):
    """Doubly linked list implementation."""
    
    def __init__(self) -> None:
        """Initialize doubly linked list."""
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self._size = 0
    
    def append(self, data: T) -> None:
        """
        Append data to end of list.
        
        Args:
            data: Data to append
        """
        new_node = Node(data)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self._size += 1
    
    def prepend(self, data: T) -> None:
        """
        Prepend data to beginning of list.
        
        Args:
            data: Data to prepend
        """
        new_node = Node(data)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        self._size += 1
    
    def insert_at(self, index: int, data: T) -> bool:
        """
        Insert data at specific index.
        
        Args:
            index: Index to insert at
            data: Data to insert
            
        Returns:
            True if successful
        """
        if index < 0 or index > self._size:
            return False
        
        if index == 0:
            self.prepend(data)
            return True
        
        if index == self._size:
            self.append(data)
            return True
        
        new_node = Node(data)
        current = self._get_node_at(index - 1)
        
        if current and current.next:
            new_node.next = current.next
            new_node.prev = current
            current.next.prev = new_node
            current.next = new_node
        
        self._size += 1
        return True
    
    def remove(self, data: T) -> bool:
        """
        Remove first occurrence of data.
        
        Args:
            data: Data to remove
            
        Returns:
            True if removed
        """
        current = self.head
        
        while current:
            if current.data == data:
                self._remove_node(current)
                return True
            current = current.next
        
        return False
    
    def remove_at(self, index: int) -> bool:
        """
        Remove node at specific index.
        
        Args:
            index: Index to remove at
            
        Returns:
            True if removed
        """
        if index < 0 or index >= self._size:
            return False
        
        node = self._get_node_at(index)
        if node:
            self._remove_node(node)
            return True
        
        return False
    
    def _remove_node(self, node: Node[T]) -> None:
        """Remove node from list."""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        
        self._size -= 1
    
    def get(self, index: int) -> Optional[T]:
        """
        Get data at specific index.
        
        Args:
            index: Index to get
            
        Returns:
            Data or None
        """
        node = self._get_node_at(index)
        return node.data if node else None
    
    def _get_node_at(self, index: int) -> Optional[Node[T]]:
        """Get node at specific index."""
        if index < 0 or index >= self._size:
            return None
        
        # Optimize by starting from closest end
        if index < self._size // 2:
            current = self.head
            for _ in range(index):
                if current:
                    current = current.next
        else:
            current = self.tail
            for _ in range(self._size - 1 - index):
                if current:
                    current = current.prev
        
        return current
    
    def find(self, data: T) -> int:
        """
        Find index of data.
        
        Args:
            data: Data to find
            
        Returns:
            Index or -1 if not found
        """
        current = self.head
        index = 0
        
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        
        return -1
    
    def contains(self, data: T) -> bool:
        """
        Check if list contains data.
        
        Args:
            data: Data to check
            
        Returns:
            True if contains
        """
        return self.find(data) != -1
    
    def to_list(self) -> List[T]:
        """Convert to Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def to_list_reverse(self) -> List[T]:
        """Convert to Python list in reverse order."""
        result = []
        current = self.tail
        while current:
            result.append(current.data)
            current = current.prev
        return result
    
    def size(self) -> int:
        """Get size of list."""
        return self._size
    
    def is_empty(self) -> bool:
        """Check if list is empty."""
        return self.head is None
    
    def clear(self) -> None:
        """Clear all nodes."""
        self.head = None
        self.tail = None
        self._size = 0
    
    def reverse(self) -> None:
        """Reverse the list in place."""
        current = self.head
        
        while current:
            # Swap prev and next
            current.prev, current.next = current.next, current.prev
            current = current.prev
        
        # Swap head and tail
        self.head, self.tail = self.tail, self.head
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return "Empty DoublyLinkedList"
        
        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next
        
        return f"DoublyLinkedList([{', '.join(result)}])"
    
    def __len__(self) -> int:
        """Get length."""
        return self._size
    
    def __iter__(self):
        """Iterate forward."""
        current = self.head
        while current:
            yield current.data
            current = current.next
    
    def __reversed__(self):
        """Iterate backward."""
        current = self.tail
        while current:
            yield current.data
            current = current.prev


def main() -> None:
    """Demonstrate doubly linked list."""
    
    print("=== Doubly Linked List Demo ===")
    
    dll = DoublyLinkedList[int]()
    
    # Append
    dll.append(10)
    dll.append(20)
    dll.append(30)
    print(f"After append(10, 20, 30): {dll}")
    
    # Prepend
    dll.prepend(5)
    print(f"After prepend(5): {dll}")
    
    # Insert at
    dll.insert_at(2, 15)
    print(f"After insert_at(2, 15): {dll}")
    
    # Get
    print(f"get(2): {dll.get(2)}")
    print(f"get(0): {dll.get(0)}")
    
    # Find
    print(f"find(20): {dll.find(20)}")
    print(f"find(100): {dll.find(100)}")
    
    # Contains
    print(f"contains(15): {dll.contains(15)}")
    print(f"contains(100): {dll.contains(100)}")
    
    # Remove
    dll.remove(15)
    print(f"After remove(15): {dll}")
    
    # Remove at
    dll.remove_at(0)
    print(f"After remove_at(0): {dll}")
    
    # Size
    print(f"Size: {dll.size()}")
    
    # To list
    print(f"to_list(): {dll.to_list()}")
    print(f"to_list_reverse(): {dll.to_list_reverse()}")
    
    # Reverse
    dll.reverse()
    print(f"After reverse(): {dll}")
    
    # Iteration
    print("\nForward iteration:")
    for item in dll:
        print(f"  {item}")
    
    print("\nBackward iteration:")
    for item in reversed(dll):
        print(f"  {item}")
    
    # String list
    print("\n=== String Doubly Linked List ===")
    str_dll = DoublyLinkedList[str]()
    str_dll.append("Hello")
    str_dll.append("World")
    str_dll.append("Python")
    print(f"String list: {str_dll}")
    
    # Clear
    dll.clear()
    print(f"\nAfter clear(): {dll}")
    print(f"Is empty: {dll.is_empty()}")


if __name__ == "__main__":
    main()
