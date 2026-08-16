"""
Linked List - Implementation of singly and doubly linked lists.
Features: Insertion, deletion, traversal, and common operations.
"""

from typing import Optional, TypeVar, Generic, List, Any
from dataclasses import dataclass


T = TypeVar('T')


@dataclass
class Node(Generic[T]):
    """Node for singly linked list."""
    data: T
    next: Optional['Node[T]'] = None


@dataclass
class DoublyNode(Generic[T]):
    """Node for doubly linked list."""
    data: T
    next: Optional['DoublyNode[T]'] = None
    prev: Optional['DoublyNode[T]'] = None


class LinkedList(Generic[T]):
    """Singly linked list implementation."""
    
    def __init__(self) -> None:
        """Initialize an empty linked list."""
        self.head: Optional[Node[T]] = None
        self.size: int = 0
    
    def is_empty(self) -> bool:
        """Check if the list is empty."""
        return self.head is None
    
    def append(self, data: T) -> None:
        """Add element to the end of the list."""
        new_node = Node(data)
        
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.size += 1
    
    def prepend(self, data: T) -> None:
        """Add element to the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def insert_at(self, index: int, data: T) -> None:
        """Insert element at specific index."""
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")
        
        if index == 0:
            self.prepend(data)
            return
        
        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self.size += 1
    
    def delete(self, data: T) -> bool:
        """Delete first occurrence of data from list."""
        if self.head is None:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def delete_at(self, index: int) -> T:
        """Delete element at specific index and return its data."""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        
        if index == 0:
            data = self.head.data
            self.head = self.head.next
            self.size -= 1
            return data
        
        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        data = current.next.data
        current.next = current.next.next
        self.size -= 1
        return data
    
    def find(self, data: T) -> Optional[int]:
        """Find index of first occurrence of data."""
        current = self.head
        index = 0
        
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        
        return None
    
    def to_list(self) -> List[T]:
        """Convert linked list to Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def reverse(self) -> None:
        """Reverse the linked list in place."""
        prev = None
        current = self.head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev
    
    def __len__(self) -> int:
        """Return the size of the list."""
        return self.size
    
    def __str__(self) -> str:
        """String representation of the list."""
        return " -> ".join(str(data) for data in self.to_list())


class DoublyLinkedList(Generic[T]):
    """Doubly linked list implementation."""
    
    def __init__(self) -> None:
        """Initialize an empty doubly linked list."""
        self.head: Optional[DoublyNode[T]] = None
        self.tail: Optional[DoublyNode[T]] = None
        self.size: int = 0
    
    def is_empty(self) -> bool:
        """Check if the list is empty."""
        return self.head is None
    
    def append(self, data: T) -> None:
        """Add element to the end of the list."""
        new_node = DoublyNode(data)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
    
    def prepend(self, data: T) -> None:
        """Add element to the beginning of the list."""
        new_node = DoublyNode(data)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        self.size += 1
    
    def delete(self, data: T) -> bool:
        """Delete first occurrence of data from list."""
        current = self.head
        
        while current:
            if current.data == data:
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
    
    def to_list(self) -> List[T]:
        """Convert doubly linked list to Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def to_list_reverse(self) -> List[T]:
        """Convert doubly linked list to Python list in reverse order."""
        result = []
        current = self.tail
        while current:
            result.append(current.data)
            current = current.prev
        return result
    
    def __len__(self) -> int:
        """Return the size of the list."""
        return self.size
    
    def __str__(self) -> str:
        """String representation of the list."""
        return " <-> ".join(str(data) for data in self.to_list())


def main() -> None:
    """Demonstrate linked list implementations."""
    
    print("=== Singly Linked List ===")
    sll = LinkedList[int]()
    
    # Add elements
    sll.append(10)
    sll.append(20)
    sll.append(30)
    sll.prepend(5)
    
    print(f"List: {sll}")
    print(f"Size: {len(sll)}")
    print(f"Find 20: Index {sll.find(20)}")
    print(f"Find 99: {sll.find(99)}")
    
    # Insert at index
    sll.insert_at(2, 15)
    print(f"After insert at index 2: {sll}")
    
    # Delete
    sll.delete(20)
    print(f"After deleting 20: {sll}")
    
    # Reverse
    sll.reverse()
    print(f"After reverse: {sll}")
    
    print("\n=== Doubly Linked List ===")
    dll = DoublyLinkedList[str]()
    
    # Add elements
    dll.append("first")
    dll.append("second")
    dll.append("third")
    dll.prepend("zero")
    
    print(f"List: {dll}")
    print(f"Size: {len(dll)}")
    print(f"Reverse: {' <-> '.join(dll.to_list_reverse())}")
    
    # Delete
    dll.delete("second")
    print(f"After deleting 'second': {dll}")


if __name__ == "__main__":
    main()
