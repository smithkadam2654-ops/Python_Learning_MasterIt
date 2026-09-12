"""
Stack and Queue Operations - LIFO and FIFO data structures.
Features: Stack operations, queue operations, and common problems.
"""

from typing import List, Optional, TypeVar, Generic
from collections import deque

T = TypeVar('T')


class Stack:
    """Stack implementation (LIFO)."""
    
    def __init__(self) -> None:
        """Initialize empty stack."""
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        """
        Push item onto stack.
        
        Args:
            item: Item to push
        """
        self.items.append(item)
    
    def pop(self) -> Optional[T]:
        """
        Pop item from stack.
        
        Returns:
            Popped item or None if empty
        """
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self) -> Optional[T]:
        """
        Peek at top item without removing.
        
        Returns:
            Top item or None if empty
        """
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Get stack size."""
        return len(self.items)
    
    def __len__(self) -> int:
        """Get stack size."""
        return len(self.items)
    
    def __repr__(self) -> str:
        return f"Stack({self.items})"


class Queue:
    """Queue implementation (FIFO)."""
    
    def __init__(self) -> None:
        """Initialize empty queue."""
        self.items: deque = deque()
    
    def enqueue(self, item: T) -> None:
        """
        Enqueue item to back of queue.
        
        Args:
            item: Item to enqueue
        """
        self.items.append(item)
    
    def dequeue(self) -> Optional[T]:
        """
        Dequeue item from front of queue.
        
        Returns:
            Dequeued item or None if empty
        """
        if not self.is_empty():
            return self.items.popleft()
        return None
    
    def peek(self) -> Optional[T]:
        """
        Peek at front item without removing.
        
        Returns:
            Front item or None if empty
        """
        if not self.is_empty():
            return self.items[0]
        return None
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Get queue size."""
        return len(self.items)
    
    def __len__(self) -> int:
        """Get queue size."""
        return len(self.items)
    
    def __repr__(self) -> str:
        return f"Queue({list(self.items)})"


class Deque:
    """Double-ended queue implementation."""
    
    def __init__(self) -> None:
        """Initialize empty deque."""
        self.items: deque = deque()
    
    def add_front(self, item: T) -> None:
        """Add item to front."""
        self.items.appendleft(item)
    
    def add_rear(self, item: T) -> None:
        """Add item to rear."""
        self.items.append(item)
    
    def remove_front(self) -> Optional[T]:
        """Remove item from front."""
        if not self.is_empty():
            return self.items.popleft()
        return None
    
    def remove_rear(self) -> Optional[T]:
        """Remove item from rear."""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self) -> bool:
        """Check if deque is empty."""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Get deque size."""
        return len(self.items)
    
    def __repr__(self) -> str:
        return f"Deque({list(self.items)})"


class StackQueueAlgorithms:
    """Stack and queue algorithm implementations."""
    
    @staticmethod
    def is_valid_parentheses(s: str) -> bool:
        """
        Check if string has valid parentheses using stack.
        
        Args:
            s: Input string
            
        Returns:
            True if valid
        """
        stack = Stack()
        mapping = {')': '(', '}': '{', ']': '['}
        
        for char in s:
            if char in mapping.values():
                stack.push(char)
            elif char in mapping:
                if stack.is_empty() or stack.pop() != mapping[char]:
                    return False
        
        return stack.is_empty()
    
    @staticmethod
    def evaluate_postfix(expression: str) -> int:
        """
        Evaluate postfix expression using stack.
        
        Args:
            expression: Postfix expression string
            
        Returns:
            Result of evaluation
        """
        stack = Stack()
        
        for token in expression.split():
            if token.isdigit():
                stack.push(int(token))
            else:
                b = stack.pop()
                a = stack.pop()
                
                if token == '+':
                    stack.push(a + b)
                elif token == '-':
                    stack.push(a - b)
                elif token == '*':
                    stack.push(a * b)
                elif token == '/':
                    stack.push(a // b)
        
        return stack.pop()
    
    @staticmethod
    def infix_to_postfix(expression: str) -> str:
        """
        Convert infix expression to postfix.
        
        Args:
            expression: Infix expression string
            
        Returns:
            Postfix expression string
        """
        stack = Stack()
        output = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        
        for token in expression:
            if token.isalnum():
                output.append(token)
            elif token == '(':
                stack.push(token)
            elif token == ')':
                while not stack.is_empty() and stack.peek() != '(':
                    output.append(stack.pop())
                stack.pop()  # Remove '('
            else:
                while (not stack.is_empty() and stack.peek() != '(' and
                       precedence.get(stack.peek(), 0) >= precedence.get(token, 0)):
                    output.append(stack.pop())
                stack.push(token)
        
        while not stack.is_empty():
            output.append(stack.pop())
        
        return ''.join(output)
    
    @staticmethod
    def reverse_string(s: str) -> str:
        """
        Reverse string using stack.
        
        Args:
            s: Input string
            
        Returns:
            Reversed string
        """
        stack = Stack()
        
        for char in s:
            stack.push(char)
        
        result = []
        while not stack.is_empty():
            result.append(stack.pop())
        
        return ''.join(result)
    
    @staticmethod
    def next_greater_element(arr: List[int]) -> List[int]:
        """
        Find next greater element for each element using stack.
        
        Args:
            arr: Input array
            
        Returns:
            Array of next greater elements
        """
        n = len(arr)
        result = [-1] * n
        stack = Stack()
        
        for i in range(n):
            while not stack.is_empty() and arr[i] > arr[stack.peek()]:
                result[stack.pop()] = arr[i]
            stack.push(i)
        
        return result
    
    @staticmethod
    def next_smaller_element(arr: List[int]) -> List[int]:
        """
        Find next smaller element for each element using stack.
        
        Args:
            arr: Input array
            
        Returns:
            Array of next smaller elements
        """
        n = len(arr)
        result = [-1] * n
        stack = Stack()
        
        for i in range(n):
            while not stack.is_empty() and arr[i] < arr[stack.peek()]:
                result[stack.pop()] = arr[i]
            stack.push(i)
        
        return result
    
    @staticmethod
    def largest_rectangle_area(heights: List[int]) -> int:
        """
        Calculate largest rectangle in histogram using stack.
        
        Args:
            heights: Array of heights
            
        Returns:
            Maximum area
        """
        stack = Stack()
        max_area = 0
        heights.append(0)  # Sentinel
        
        for i, h in enumerate(heights):
            while not stack.is_empty() and h < heights[stack.peek()]:
                height = heights[stack.pop()]
                width = i if stack.is_empty() else i - stack.peek() - 1
                max_area = max(max_area, height * width)
            stack.push(i)
        
        heights.pop()  # Remove sentinel
        return max_area
    
    @staticmethod
    def min_stack() -> 'MinStack':
        """
        Create stack that supports getting minimum in O(1).
        
        Returns:
            MinStack instance
        """
        return MinStack()
    
    @staticmethod
    def implement_queue_using_stacks() -> 'MyQueue':
        """
        Create queue implemented using two stacks.
        
        Returns:
            MyQueue instance
        """
        return MyQueue()
    
    @staticmethod
    def implement_stack_using_queues() -> 'MyStack':
        """
        Create stack implemented using two queues.
        
        Returns:
            MyStack instance
        """
        return MyStack()
    
    @staticmethod
    def simplify_path(path: str) -> str:
        """
        Simplify Unix file path using stack.
        
        Args:
            path: File path
            
        Returns:
            Simplified path
        """
        stack = Stack()
        parts = path.split('/')
        
        for part in parts:
            if part == '..':
                if not stack.is_empty():
                    stack.pop()
            elif part and part != '.':
                stack.push(part)
        
        result = []
        while not stack.is_empty():
            result.insert(0, stack.pop())
        
        return '/' + '/'.join(result)
    
    @staticmethod
    def remove_duplicates(s: str) -> str:
        """
        Remove adjacent duplicates from string using stack.
        
        Args:
            s: Input string
            
        Returns:
            String with duplicates removed
        """
        stack = Stack()
        
        for char in s:
            if not stack.is_empty() and stack.peek() == char:
                stack.pop()
            else:
                stack.push(char)
        
        result = []
        while not stack.is_empty():
            result.append(stack.pop())
        
        return ''.join(reversed(result))
    
    @staticmethod
    def sliding_window_maximum(nums: List[int], k: int) -> List[int]:
        """
        Find maximum in each sliding window using deque.
        
        Args:
            nums: Input array
            k: Window size
            
        Returns:
            Array of maximums
        """
        from collections import deque
        
        result = []
        dq = deque()
        
        for i, num in enumerate(nums):
            # Remove elements outside window
            while dq and dq[0] < i - k + 1:
                dq.popleft()
            
            # Remove smaller elements
            while dq and nums[dq[-1]] < num:
                dq.pop()
            
            dq.append(i)
            
            # Add to result when window is complete
            if i >= k - 1:
                result.append(nums[dq[0]])
        
        return result


class MinStack:
    """Stack with O(1) minimum retrieval."""
    
    def __init__(self) -> None:
        """Initialize min stack."""
        self.stack = Stack()
        self.min_stack = Stack()
    
    def push(self, val: int) -> None:
        """Push value onto stack."""
        self.stack.push(val)
        
        if self.min_stack.is_empty() or val <= self.min_stack.peek():
            self.min_stack.push(val)
    
    def pop(self) -> Optional[int]:
        """Pop value from stack."""
        val = self.stack.pop()
        
        if val == self.min_stack.peek():
            self.min_stack.pop()
        
        return val
    
    def top(self) -> Optional[int]:
        """Get top value."""
        return self.stack.peek()
    
    def get_min(self) -> Optional[int]:
        """Get minimum value."""
        return self.min_stack.peek()


class MyQueue:
    """Queue implemented using two stacks."""
    
    def __init__(self) -> None:
        """Initialize queue."""
        self.in_stack = Stack()
        self.out_stack = Stack()
    
    def push(self, x: int) -> None:
        """Push element to back of queue."""
        self.in_stack.push(x)
    
    def pop(self) -> Optional[int]:
        """Pop element from front of queue."""
        if self.out_stack.is_empty():
            while not self.in_stack.is_empty():
                self.out_stack.push(self.in_stack.pop())
        
        return self.out_stack.pop()
    
    def peek(self) -> Optional[int]:
        """Peek at front element."""
        if self.out_stack.is_empty():
            while not self.in_stack.is_empty():
                self.out_stack.push(self.in_stack.pop())
        
        return self.out_stack.peek()
    
    def empty(self) -> bool:
        """Check if queue is empty."""
        return self.in_stack.is_empty() and self.out_stack.is_empty()


class MyStack:
    """Stack implemented using two queues."""
    
    def __init__(self) -> None:
        """Initialize stack."""
        self.queue1 = Queue()
        self.queue2 = Queue()
    
    def push(self, x: int) -> None:
        """Push element onto stack."""
        self.queue2.enqueue(x)
        
        while not self.queue1.is_empty():
            self.queue2.enqueue(self.queue1.dequeue())
        
        self.queue1, self.queue2 = self.queue2, self.queue1
    
    def pop(self) -> Optional[int]:
        """Pop element from stack."""
        return self.queue1.dequeue()
    
    def top(self) -> Optional[int]:
        """Get top element."""
        return self.queue1.peek()
    
    def empty(self) -> bool:
        """Check if stack is empty."""
        return self.queue1.is_empty()


def main() -> None:
    """Demonstrate stack and queue operations."""
    
    print("=== Stack and Queue Operations Demo ===")
    
    # Stack
    print("\n--- Stack ---")
    stack = Stack()
    for val in [1, 2, 3, 4, 5]:
        stack.push(val)
    
    print(f"Stack: {stack}")
    print(f"Peek: {stack.peek()}")
    print(f"Pop: {stack.pop()}")
    print(f"After pop: {stack}")
    
    # Queue
    print("\n--- Queue ---")
    queue = Queue()
    for val in [1, 2, 3, 4, 5]:
        queue.enqueue(val)
    
    print(f"Queue: {queue}")
    print(f"Peek: {queue.peek()}")
    print(f"Dequeue: {queue.dequeue()}")
    print(f"After dequeue: {queue}")
    
    # Valid parentheses
    print("\n--- Valid Parentheses ---")
    s = "()[]{}"
    print(f"'{s}' is valid: {StackQueueAlgorithms.is_valid_parentheses(s)}")
    
    # Postfix evaluation
    print("\n--- Postfix Evaluation ---")
    expr = "2 3 1 * + 9 -"
    print(f"Expression: {expr}")
    print(f"Result: {StackQueueAlgorithms.evaluate_postfix(expr)}")
    
    # Infix to postfix
    print("\n--- Infix to Postfix ---")
    infix = "a+b*(c^d-e)^(f+g*h)-i"
    print(f"Infix: {infix}")
    print(f"Postfix: {StackQueueAlgorithms.infix_to_postfix(infix)}")
    
    # Reverse string
    print("\n--- Reverse String ---")
    s = "Hello World"
    print(f"Original: '{s}'")
    print(f"Reversed: '{StackQueueAlgorithms.reverse_string(s)}'")
    
    # Next greater element
    print("\n--- Next Greater Element ---")
    arr = [4, 5, 2, 25]
    print(f"Array: {arr}")
    print(f"Next greater: {StackQueueAlgorithms.next_greater_element(arr)}")
    
    # Largest rectangle
    print("\n--- Largest Rectangle ---")
    heights = [2, 1, 5, 6, 2, 3]
    print(f"Heights: {heights}")
    print(f"Max area: {StackQueueAlgorithms.largest_rectangle_area(heights)}")
    
    # Simplify path
    print("\n--- Simplify Path ---")
    path = "/a/./b/../../c/"
    print(f"Original: '{path}'")
    print(f"Simplified: '{StackQueueAlgorithms.simplify_path(path)}'")
    
    # Remove duplicates
    print("\n--- Remove Duplicates ---")
    s = "abbaca"
    print(f"Original: '{s}'")
    print(f"After: '{StackQueueAlgorithms.remove_duplicates(s)}'")
    
    # Sliding window maximum
    print("\n--- Sliding Window Maximum ---")
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(f"Array: {nums}, k: {k}")
    print(f"Maximums: {StackQueueAlgorithms.sliding_window_maximum(nums, k)}")


if __name__ == "__main__":
    main()
