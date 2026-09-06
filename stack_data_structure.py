"""
Stack Data Structure - Stack implementation with multiple operations.
Features: Push, pop, peek, min, and stack reversal.
"""

from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')


class Stack(Generic[T]):
    """Stack implementation using list."""
    
    def __init__(self) -> None:
        """Initialize stack."""
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """
        Push item onto stack.
        
        Args:
            item: Item to push
        """
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        """
        Pop item from stack.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        return self._items.pop()
    
    def peek(self) -> Optional[T]:
        """
        Peek at top item without removing.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Get stack size."""
        return len(self._items)
    
    def clear(self) -> None:
        """Clear stack."""
        self._items.clear()
    
    def to_list(self) -> List[T]:
        """Convert stack to list (top to bottom)."""
        return self._items.copy()
    
    def reverse(self) -> None:
        """Reverse stack in place."""
        self._items.reverse()
    
    def __len__(self) -> int:
        """Get length."""
        return len(self._items)
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return "Stack(empty)"
        return f"Stack({self._items})"


class MinStack(Generic[T]):
    """Stack that can return minimum element in O(1)."""
    
    def __init__(self) -> None:
        """Initialize min stack."""
        self._stack: List[T] = []
        self._min_stack: List[T] = []
    
    def push(self, item: T) -> None:
        """
        Push item onto stack.
        
        Args:
            item: Item to push
        """
        self._stack.append(item)
        
        if not self._min_stack or item <= self._min_stack[-1]:
            self._min_stack.append(item)
    
    def pop(self) -> Optional[T]:
        """
        Pop item from stack.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        
        item = self._stack.pop()
        
        if item == self._min_stack[-1]:
            self._min_stack.pop()
        
        return item
    
    def peek(self) -> Optional[T]:
        """
        Peek at top item.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        return self._stack[-1]
    
    def get_min(self) -> Optional[T]:
        """
        Get minimum element.
        
        Returns:
            Minimum or None if empty
        """
        if self.is_empty():
            return None
        return self._min_stack[-1]
    
    def is_empty(self) -> bool:
        """Check if empty."""
        return len(self._stack) == 0
    
    def size(self) -> int:
        """Get size."""
        return len(self._stack)
    
    def __len__(self) -> int:
        """Get length."""
        return len(self._stack)
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return "MinStack(empty)"
        return f"MinStack({self._stack}, min={self.get_min()})"


def main() -> None:
    """Demonstrate stack."""
    
    print("=== Stack Demo ===")
    
    stack = Stack[int]()
    
    # Push
    stack.push(10)
    stack.push(20)
    stack.push(30)
    print(f"After push(10, 20, 30): {stack}")
    
    # Peek
    print(f"Peek: {stack.peek()}")
    
    # Pop
    print(f"Pop: {stack.pop()}")
    print(f"After pop: {stack}")
    
    # Size
    print(f"Size: {stack.size()}")
    
    # Is empty
    print(f"Is empty: {stack.is_empty()}")
    
    # To list
    print(f"To list: {stack.to_list()}")
    
    # Reverse
    stack.reverse()
    print(f"After reverse: {stack}")
    
    # Clear
    stack.clear()
    print(f"After clear: {stack}")
    print(f"Is empty: {stack.is_empty()}")
    
    # String stack
    print("\n=== String Stack ===")
    str_stack = Stack[str]()
    
    str_stack.push("Hello")
    str_stack.push("World")
    str_stack.push("Python")
    print(f"String stack: {str_stack}")
    
    # Min stack
    print("\n=== Min Stack Demo ===")
    min_stack = MinStack[int]()
    
    values = [5, 3, 7, 2, 8, 1]
    for value in values:
        min_stack.push(value)
        print(f"Push {value}: Stack={min_stack._stack}, Min={min_stack.get_min()}")
    
    print(f"\nCurrent min: {min_stack.get_min()}")
    
    while not min_stack.is_empty():
        popped = min_stack.pop()
        print(f"Pop {popped}: Stack={min_stack._stack}, Min={min_stack.get_min()}")
    
    # Stack applications
    print("\n=== Stack Applications ===")
    
    # Parentheses matching
    def is_balanced(s: str) -> bool:
        """Check if parentheses are balanced."""
        stack = Stack[str]()
        pairs = {')': '(', '}': '{', ']': '['}
        
        for char in s:
            if char in '({[':
                stack.push(char)
            elif char in ')}]':
                if stack.is_empty() or stack.pop() != pairs[char]:
                    return False
        
        return stack.is_empty()
    
    test_strings = ["()", "()[]{}", "(]", "([{}])", "((()))"]
    for test in test_strings:
        print(f"'{test}' is balanced: {is_balanced(test)}")
    
    # Reverse string
    def reverse_string(s: str) -> str:
        """Reverse string using stack."""
        stack = Stack[str]()
        for char in s:
            stack.push(char)
        
        result = ""
        while not stack.is_empty():
            result += stack.pop()
        
        return result
    
    print(f"\nReverse 'hello': {reverse_string('hello')}")
    print(f"Reverse 'Python': {reverse_string('Python')}")


if __name__ == "__main__":
    main()
