"""
Generator Tools - Advanced generator patterns for data processing.
Features: Lazy evaluation, pipeline processing, infinite sequences, and memory efficiency.
"""

from typing import Generator, Iterable, Callable, Any, List
import random
import time
from functools import wraps


def fibonacci_sequence() -> Generator[int, None, None]:
    """
    Generate an infinite Fibonacci sequence.
    
    Yields:
        Next Fibonacci number in the sequence
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def prime_numbers() -> Generator[int, None, None]:
    """
    Generate an infinite sequence of prime numbers.
    
    Yields:
        Next prime number
    """
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    num = 2
    while True:
        if is_prime(num):
            yield num
        num += 1


def read_file_lines(file_path: str) -> Generator[str, None, None]:
    """
    Read file line by line (memory efficient for large files).
    
    Args:
        file_path: Path to the file to read
        
    Yields:
        Each line from the file
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


def batch_generator(
    iterable: Iterable[Any],
    batch_size: int,
) -> Generator[List[Any], None, None]:
    """
    Split an iterable into batches of specified size.
    
    Args:
        iterable: Source iterable to batch
        batch_size: Number of items per batch
        
    Yields:
        List containing batch_size items
    """
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    
    if batch:  # Yield remaining items
        yield batch


def filter_generator(
    generator: Generator[Any, None, None],
    predicate: Callable[[Any], bool],
) -> Generator[Any, None, None]:
    """
    Filter generator items based on a predicate function.
    
    Args:
        generator: Source generator
        predicate: Function that returns True for items to keep
        
    Yields:
        Items that satisfy the predicate
    """
    for item in generator:
        if predicate(item):
            yield item


def map_generator(
    generator: Generator[Any, None, None],
    transform: Callable[[Any], Any],
) -> Generator[Any, None, None]:
    """
    Transform generator items using a function.
    
    Args:
        generator: Source generator
        transform: Function to apply to each item
        
    Yields:
        Transformed items
    """
    for item in generator:
        yield transform(item)


def take_generator(
    generator: Generator[Any, None, None],
    n: int,
) -> Generator[Any, None, None]:
    """
    Take first n items from a generator.
    
    Args:
        generator: Source generator
        n: Number of items to take
        
    Yields:
        First n items from the generator
    """
    count = 0
    for item in generator:
        if count >= n:
            break
        yield item
        count += 1


def tee_generator(
    generator: Generator[Any, None, None],
    n: int = 2,
) -> List[Generator[Any, None, None]]:
    """
    Split a generator into n independent generators.
    
    Args:
        generator: Source generator
        n: Number of output generators
        
    Returns:
        List of n independent generators
    """
    from itertools import tee
    return tee(generator, n)


def chunk_text(text: str, chunk_size: int) -> Generator[str, None, None]:
    """
    Split text into chunks of specified size.
    
    Args:
        text: Text to chunk
        chunk_size: Maximum size of each chunk
        
    Yields:
        Text chunks
    """
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]


def sliding_window(
    sequence: Iterable[Any],
    window_size: int,
) -> Generator[List[Any], None, None]:
    """
    Generate sliding windows over a sequence.
    
    Args:
        sequence: Input sequence
        window_size: Size of each window
        
    Yields:
        Lists representing sliding windows
    """
    from collections import deque
    window = deque(maxlen=window_size)
    
    for item in sequence:
        window.append(item)
        if len(window) == window_size:
            yield list(window)


def interleave_generators(*generators: Generator[Any, None, None]) -> Generator[Any, None, None]:
    """
    Interleave items from multiple generators.
    
    Args:
        generators: Variable number of generators to interleave
        
    Yields:
        Items from generators in round-robin fashion
    """
    from itertools import cycle
    active_generators = cycle([g for g in generators if g is not None])
    
    for gen in active_generators:
        try:
            yield next(gen)
        except StopIteration:
            continue


def progress_generator(
    generator: Generator[Any, None, None],
    total: Optional[int] = None,
    description: str = "Processing",
) -> Generator[Any, None, None]:
    """
    Add progress tracking to a generator.
    
    Args:
        generator: Source generator
        total: Total number of items (if known)
        description: Description for progress display
        
    Yields:
        Items from the source generator with progress updates
    """
    count = 0
    start_time = time.time()
    
    for item in generator:
        count += 1
        elapsed = time.time() - start_time
        
        if total:
            progress = (count / total) * 100
            print(f"\r{description}: {count}/{total} ({progress:.1f}%) - {elapsed:.1f}s", end="")
        else:
            print(f"\r{description}: {count} items - {elapsed:.1f}s", end="")
        
        yield item
    
    print()  # New line after completion


def main() -> None:
    """Demonstrate generator functionality."""
    
    print("=== Fibonacci Sequence ===")
    fib = take_generator(fibonacci_sequence(), 10)
    print(list(fib))
    
    print("\n=== Prime Numbers ===")
    primes = take_generator(prime_numbers(), 10)
    print(list(primes))
    
    print("\n=== Batch Processing ===")
    numbers = range(1, 21)
    batches = list(batch_generator(numbers, 5))
    print(f"Batches: {batches}")
    
    print("\n=== Filter and Map Pipeline ===")
    # Create a pipeline: filter evens, square them, take first 5
    numbers = (n for n in range(1, 100))
    evens = filter_generator(numbers, lambda x: x % 2 == 0)
    squared = map_generator(evens, lambda x: x ** 2)
    result = list(take_generator(squared, 5))
    print(f"First 5 squared evens: {result}")
    
    print("\n=== Sliding Window ===")
    data = [1, 2, 3, 4, 5]
    windows = list(sliding_window(data, 3))
    print(f"Sliding windows of size 3: {windows}")
    
    print("\n=== Text Chunking ===")
    text = "This is a long text that needs to be chunked"
    chunks = list(chunk_text(text, 10))
    print(f"Text chunks: {chunks}")
    
    print("\n=== Progress Generator ===")
    def data_generator():
        for i in range(1, 11):
            time.sleep(0.1)
            yield i
    
    tracked = progress_generator(data_generator(), total=10, description="Loading")
    result = list(tracked)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
