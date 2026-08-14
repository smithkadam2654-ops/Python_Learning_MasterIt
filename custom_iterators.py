class SlidingWindow:
    """
    An iterator that yields a sliding window of items from an iterable.
    Example: SlidingWindow([1, 2, 3, 4], size=2) -> (1, 2), (2, 3), (3, 4)
    """
    def __init__(self, sequence, size: int):
        self.sequence = list(sequence)
        self.size = size
        self.current_index = 0

    def __iter__(self):
        # The object itself is the iterator
        return self

    def __next__(self):
        if self.current_index + self.size > len(self.sequence):
            raise StopIteration
        
        window = tuple(self.sequence[self.current_index : self.current_index + self.size])
        self.current_index += 1
        return window

if __name__ == "__main__":
    data = [10, 20, 30, 40, 50, 60]
    
    print("Testing Sliding Window (size=3):")
    window_iter = SlidingWindow(data, size=3)
    
    for w in window_iter:
        print(w)
        
    print("\nTesting Sliding Window on a string (size=2):")
    for chars in SlidingWindow("PYTHON", size=2):
        print("".join(chars))
