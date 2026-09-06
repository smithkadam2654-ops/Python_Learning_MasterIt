"""
Circular Buffer - Circular buffer/ring buffer implementation.
Features: Fixed size, overwrite policy, and efficient operations.
"""

from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')


class CircularBuffer(Generic[T]):
    """Circular buffer implementation."""
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize circular buffer.
        
        Args:
            capacity: Buffer capacity
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.capacity = capacity
        self.buffer: List[Optional[T]] = [None] * capacity
        self.head = 0
        self.tail = 0
        self._size = 0
        self.overwrite = False
    
    def is_empty(self) -> bool:
        """Check if buffer is empty."""
        return self._size == 0
    
    def is_full(self) -> bool:
        """Check if buffer is full."""
        return self._size == self.capacity
    
    def size(self) -> int:
        """Get current size."""
        return self._size
    
    def write(self, item: T) -> bool:
        """
        Write item to buffer.
        
        Args:
            item: Item to write
            
        Returns:
            True if successful, False if buffer was full
        """
        if self.is_full():
            if not self.overwrite:
                return False
            # Overwrite oldest item
            self.head = (self.head + 1) % self.capacity
            self._size -= 1
        
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        self._size += 1
        return True
    
    def read(self) -> Optional[T]:
        """
        Read item from buffer.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        
        item = self.buffer[self.head]
        self.buffer[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self._size -= 1
        
        return item
    
    def peek(self) -> Optional[T]:
        """
        Peek at next item without removing.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        return self.buffer[self.head]
    
    def peek_last(self) -> Optional[T]:
        """
        Peek at last item without removing.
        
        Returns:
            Item or None if empty
        """
        if self.is_empty():
            return None
        last_index = (self.tail - 1) % self.capacity
        return self.buffer[last_index]
    
    def clear(self) -> None:
        """Clear buffer."""
        self.buffer = [None] * self.capacity
        self.head = 0
        self.tail = 0
        self._size = 0
    
    def to_list(self) -> List[T]:
        """Convert buffer to list."""
        result = []
        for i in range(self._size):
            index = (self.head + i) % self.capacity
            item = self.buffer[index]
            if item is not None:
                result.append(item)
        return result
    
    def __len__(self) -> int:
        """Get length."""
        return self._size
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_empty():
            return f"CircularBuffer(empty, capacity={self.capacity})"
        return f"CircularBuffer({self.to_list()}, capacity={self.capacity})"


class SlidingWindow(CircularBuffer[T]):
    """Sliding window using circular buffer."""
    
    def __init__(self, window_size: int) -> None:
        """
        Initialize sliding window.
        
        Args:
            window_size: Size of sliding window
        """
        super().__init__(window_size)
        self.overwrite = True  # Always overwrite oldest
    
    def add(self, item: T) -> None:
        """
        Add item to window (overwrites if full).
        
        Args:
            item: Item to add
        """
        self.write(item)
    
    def get_window(self) -> List[T]:
        """Get current window contents."""
        return self.to_list()
    
    def sum(self) -> T:
        """Get sum of window (requires numeric type)."""
        return sum(self.to_list())  # type: ignore
    
    def average(self) -> float:
        """Get average of window."""
        items = self.to_list()
        if not items:
            return 0.0
        return sum(items) / len(items)  # type: ignore


def main() -> None:
    """Demonstrate circular buffer."""
    
    print("=== Circular Buffer Demo ===")
    
    # Basic circular buffer
    buffer = CircularBuffer[int](5)
    
    print(f"Empty: {buffer.is_empty()}")
    print(f"Full: {buffer.is_full()}")
    
    # Write items
    for i in range(5):
        buffer.write(i * 10)
        print(f"After write({i * 10}): {buffer}")
    
    print(f"Full: {buffer.is_full()}")
    
    # Try to write when full
    result = buffer.write(50)
    print(f"Write when full (no overwrite): {result}")
    
    # Read items
    print("\nReading items:")
    while not buffer.is_empty():
        item = buffer.read()
        print(f"  Read: {item}")
        print(f"  Buffer: {buffer}")
    
    # With overwrite
    print("\n=== With Overwrite ===")
    buffer.overwrite = True
    
    for i in range(7):
        buffer.write(i * 10)
        print(f"After write({i * 10}): {buffer}")
    
    # Peek
    print(f"\nPeek: {buffer.peek()}")
    print(f"Peek last: {buffer.peek_last()}")
    
    # Sliding window
    print("\n=== Sliding Window ===")
    window = SlidingWindow[int](3)
    
    data = [10, 20, 30, 40, 50, 60]
    for value in data:
        window.add(value)
        print(f"Add {value}: Window = {window.get_window()}, Sum = {window.sum()}, Avg = {window.average():.2f}")
    
    # String buffer
    print("\n=== String Buffer ===")
    str_buffer = CircularBuffer[str](4)
    
    words = ["Hello", "World", "Python", "Circular", "Buffer"]
    for word in words:
        str_buffer.write(word)
        print(f"After write('{word}'): {str_buffer}")
    
    print(f"To list: {str_buffer.to_list()}")


if __name__ == "__main__":
    main()
