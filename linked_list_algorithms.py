"""
Linked List Algorithms - Singly and doubly linked list operations.
Features: List operations, reversal, cycle detection, and common problems.
"""

from typing import Optional, TypeVar, Generic

T = TypeVar('T')


class ListNode:
    """Singly linked list node."""
    
    def __init__(self, val: T, next: 'ListNode' = None) -> None:
        """Initialize list node."""
        self.val = val
        self.next = next
    
    def __repr__(self) -> str:
        return f"ListNode({self.val})"


class DoublyListNode:
    """Doubly linked list node."""
    
    def __init__(self, val: T, prev: 'DoublyListNode' = None, 
                 next: 'DoublyListNode' = None) -> None:
        """Initialize doubly list node."""
        self.val = val
        self.prev = prev
        self.next = next
    
    def __repr__(self) -> str:
        return f"DoublyListNode({self.val})"


class LinkedList:
    """Singly linked list implementation."""
    
    def __init__(self) -> None:
        """Initialize empty linked list."""
        self.head: Optional[ListNode] = None
        self.size = 0
    
    def append(self, val: T) -> None:
        """
        Append value to end of list.
        
        Args:
            val: Value to append
        """
        new_node = ListNode(val)
        
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.size += 1
    
    def prepend(self, val: T) -> None:
        """
        Prepend value to beginning of list.
        
        Args:
            val: Value to prepend
        """
        new_node = ListNode(val, self.head)
        self.head = new_node
        self.size += 1
    
    def insert_at(self, index: int, val: T) -> None:
        """
        Insert value at specific index.
        
        Args:
            index: Index to insert at
            val: Value to insert
        """
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")
        
        if index == 0:
            self.prepend(val)
            return
        
        new_node = ListNode(val)
        current = self.head
        
        for _ in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self.size += 1
    
    def delete_at(self, index: int) -> Optional[T]:
        """
        Delete node at specific index.
        
        Args:
            index: Index to delete at
            
        Returns:
            Deleted value or None
        """
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        
        if index == 0:
            val = self.head.val
            self.head = self.head.next
            self.size -= 1
            return val
        
        current = self.head
        
        for _ in range(index - 1):
            current = current.next
        
        val = current.next.val
        current.next = current.next.next
        self.size -= 1
        
        return val
    
    def get(self, index: int) -> Optional[T]:
        """
        Get value at specific index.
        
        Args:
            index: Index to get
            
        Returns:
            Value at index or None
        """
        if index < 0 or index >= self.size:
            return None
        
        current = self.head
        
        for _ in range(index):
            current = current.next
        
        return current.val
    
    def find(self, val: T) -> int:
        """
        Find index of value.
        
        Args:
            val: Value to find
            
        Returns:
            Index or -1 if not found
        """
        current = self.head
        index = 0
        
        while current:
            if current.val == val:
                return index
            current = current.next
            index += 1
        
        return -1
    
    def to_list(self) -> List[T]:
        """
        Convert linked list to Python list.
        
        Returns:
            List of values
        """
        result = []
        current = self.head
        
        while current:
            result.append(current.val)
            current = current.next
        
        return result
    
    def __len__(self) -> int:
        """Get list size."""
        return self.size
    
    def __repr__(self) -> str:
        return f"LinkedList({self.to_list()})"


class LinkedListAlgorithms:
    """Linked list algorithm implementations."""
    
    @staticmethod
    def reverse(head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Reverse linked list.
        
        Args:
            head: List head
            
        Returns:
            New head of reversed list
        """
        prev = None
        current = head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        return prev
    
    @staticmethod
    def reverse_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Reverse linked list recursively.
        
        Args:
            head: List head
            
        Returns:
            New head of reversed list
        """
        if not head or not head.next:
            return head
        
        new_head = LinkedListAlgorithms.reverse_recursive(head.next)
        head.next.next = head
        head.next = None
        
        return new_head
    
    @staticmethod
    def has_cycle(head: Optional[ListNode]) -> bool:
        """
        Detect cycle using Floyd's algorithm.
        
        Args:
            head: List head
            
        Returns:
            True if cycle exists
        """
        if not head or not head.next:
            return False
        
        slow = head
        fast = head.next
        
        while fast and fast.next:
            if slow == fast:
                return True
            slow = slow.next
            fast = fast.next.next
        
        return False
    
    @staticmethod
    def find_cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Find start node of cycle.
        
        Args:
            head: List head
            
        Returns:
            Cycle start node or None
        """
        if not head or not head.next:
            return None
        
        # Find meeting point
        slow = head
        fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        
        if slow != fast:
            return None
        
        # Find cycle start
        slow = head
        
        while slow != fast:
            slow = slow.next
            fast = fast.next
        
        return slow
    
    @staticmethod
    def find_middle(head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Find middle node of linked list.
        
        Args:
            head: List head
            
        Returns:
            Middle node
        """
        if not head:
            return None
        
        slow = head
        fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        return slow
    
    @staticmethod
    def merge_sorted(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Merge two sorted linked lists.
        
        Args:
            l1: First list head
            l2: Second list head
            
        Returns:
            Merged list head
        """
        dummy = ListNode(0)
        current = dummy
        
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        
        current.next = l1 if l1 else l2
        
        return dummy.next
    
    @staticmethod
    def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Remove nth node from end of list.
        
        Args:
            head: List head
            n: Position from end (1-indexed)
            
        Returns:
            New head
        """
        dummy = ListNode(0, head)
        fast = dummy
        slow = dummy
        
        # Move fast n+1 steps ahead
        for _ in range(n + 1):
            if fast:
                fast = fast.next
        
        # Move both until fast reaches end
        while fast:
            fast = fast.next
            slow = slow.next
        
        # Remove node
        slow.next = slow.next.next
        
        return dummy.next
    
    @staticmethod
    def is_palindrome(head: Optional[ListNode]) -> bool:
        """
        Check if linked list is palindrome.
        
        Args:
            head: List head
            
        Returns:
            True if palindrome
        """
        if not head or not head.next:
            return True
        
        # Find middle
        middle = LinkedListAlgorithms.find_middle(head)
        
        # Reverse second half
        second_half = LinkedListAlgorithms.reverse(middle)
        
        # Compare
        first_half = head
        second_half_copy = second_half
        
        result = True
        while second_half:
            if first_half.val != second_half.val:
                result = False
                break
            first_half = first_half.next
            second_half = second_half.next
        
        # Restore list
        LinkedListAlgorithms.reverse(second_half_copy)
        
        return result
    
    @staticmethod
    def detect_intersection(headA: Optional[ListNode], headB: Optional[ListNode]) -> Optional[ListNode]:
        """
        Detect intersection of two linked lists.
        
        Args:
            headA: First list head
            headB: Second list head
            
        Returns:
            Intersection node or None
        """
        if not headA or not headB:
            return None
        
        # Get lengths
        lenA = LinkedListAlgorithms._get_length(headA)
        lenB = LinkedListAlgorithms._get_length(headB)
        
        # Align starting points
        currentA = headA
        currentB = headB
        
        if lenA > lenB:
            for _ in range(lenA - lenB):
                currentA = currentA.next
        else:
            for _ in range(lenB - lenA):
                currentB = currentB.next
        
        # Find intersection
        while currentA and currentB:
            if currentA == currentB:
                return currentA
            currentA = currentA.next
            currentB = currentB.next
        
        return None
    
    @staticmethod
    def _get_length(head: Optional[ListNode]) -> int:
        """Get length of linked list."""
        length = 0
        current = head
        
        while current:
            length += 1
            current = current.next
        
        return length
    
    @staticmethod
    def sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Sort linked list using merge sort.
        
        Args:
            head: List head
            
        Returns:
            Sorted list head
        """
        if not head or not head.next:
            return head
        
        # Split list
        middle = LinkedListAlgorithms.find_middle(head)
        right = middle.next
        middle.next = None
        
        # Recursively sort
        left = LinkedListAlgorithms.sort_list(head)
        right = LinkedListAlgorithms.sort_list(right)
        
        # Merge
        return LinkedListAlgorithms.merge_sorted(left, right)
    
    @staticmethod
    def rotate_right(head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """
        Rotate linked list to the right by k places.
        
        Args:
            head: List head
            k: Number of rotations
            
        Returns:
            New head
        """
        if not head or not head.next or k == 0:
            return head
        
        # Get length and make it circular
        length = 1
        tail = head
        
        while tail.next:
            tail = tail.next
            length += 1
        
        k = k % length
        if k == 0:
            return head
        
        # Break the circle
        tail.next = head
        
        # Find new tail
        steps_to_new_tail = length - k
        new_tail = head
        
        for _ in range(steps_to_new_tail - 1):
            new_tail = new_tail.next
        
        new_head = new_tail.next
        new_tail.next = None
        
        return new_head


def main() -> None:
    """Demonstrate linked list algorithms."""
    
    print("=== Linked List Algorithms Demo ===")
    
    # Basic operations
    print("\n--- Basic Operations ---")
    ll = LinkedList()
    for val in [1, 2, 3, 4, 5]:
        ll.append(val)
    
    print(f"List: {ll}")
    print(f"Get index 2: {ll.get(2)}")
    print(f"Find 3: {ll.find(3)}")
    
    ll.insert_at(2, 10)
    print(f"After insert at 2: {ll}")
    
    ll.delete_at(2)
    print(f"After delete at 2: {ll}")
    
    ll.prepend(0)
    print(f"After prepend 0: {ll}")
    
    # Reverse
    print("\n--- Reverse ---")
    ll = LinkedList()
    for val in [1, 2, 3, 4, 5]:
        ll.append(val)
    
    print(f"Original: {ll}")
    reversed_head = LinkedListAlgorithms.reverse(ll.head)
    print(f"Reversed: {LinkedListAlgorithms._to_list(reversed_head)}")
    
    # Middle
    print("\n--- Middle ---")
    ll = LinkedList()
    for val in [1, 2, 3, 4, 5]:
        ll.append(val)
    
    middle = LinkedListAlgorithms.find_middle(ll.head)
    print(f"List: {ll}")
    print(f"Middle: {middle.val if middle else None}")
    
    # Merge sorted
    print("\n--- Merge Sorted ---")
    ll1 = LinkedList()
    for val in [1, 3, 5]:
        ll1.append(val)
    
    ll2 = LinkedList()
    for val in [2, 4, 6]:
        ll2.append(val)
    
    merged = LinkedListAlgorithms.merge_sorted(ll1.head, ll2.head)
    print(f"Merged: {LinkedListAlgorithms._to_list(merged)}")
    
    # Remove nth from end
    print("\n--- Remove Nth from End ---")
    ll = LinkedList()
    for val in [1, 2, 3, 4, 5]:
        ll.append(val)
    
    print(f"Original: {ll}")
    new_head = LinkedListAlgorithms.remove_nth_from_end(ll.head, 2)
    print(f"After removing 2nd from end: {LinkedListAlgorithms._to_list(new_head)}")
    
    # Palindrome
    print("\n--- Palindrome ---")
    ll = LinkedList()
    for val in [1, 2, 3, 2, 1]:
        ll.append(val)
    
    print(f"List: {ll}")
    print(f"Is palindrome: {LinkedListAlgorithms.is_palindrome(ll.head)}")
    
    # Sort
    print("\n--- Sort ---")
    ll = LinkedList()
    for val in [3, 1, 4, 2, 5]:
        ll.append(val)
    
    print(f"Original: {ll}")
    sorted_head = LinkedListAlgorithms.sort_list(ll.head)
    print(f"Sorted: {LinkedListAlgorithms._to_list(sorted_head)}")
    
    # Rotate
    print("\n--- Rotate Right ---")
    ll = LinkedList()
    for val in [1, 2, 3, 4, 5]:
        ll.append(val)
    
    print(f"Original: {ll}")
    rotated_head = LinkedListAlgorithms.rotate_right(ll.head, 2)
    print(f"Rotated by 2: {LinkedListAlgorithms._to_list(rotated_head)}")


# Helper function for demo
def _to_list(head: Optional[ListNode]) -> List[T]:
    """Convert linked list to Python list."""
    result = []
    current = head
    
    while current:
        result.append(current.val)
        current = current.next
    
    return result


# Add helper to class
LinkedListAlgorithms._to_list = staticmethod(_to_list)


if __name__ == "__main__":
    main()
