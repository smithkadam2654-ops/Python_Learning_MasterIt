"""
Advanced Python - Lesson 02: Generators & Advanced Iterators
=============================================================
Generators produce sequences of values lazily (one at a time),
making them memory-efficient for large datasets and infinite sequences.

Topics Covered:
- Generator functions (yield)
- Generator expressions
- yield from and sub-generators
- Custom iterator classes
- Infinite sequences
- Coroutines (send, throw, close)
- itertools integration
"""

import itertools
from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


# ============================================================
# 1. BASIC GENERATOR FUNCTIONS
# ============================================================
def countdown(n: int) -> Generator[int, None, None]:
    """Count down from n to 1."""
    while n > 0:
        yield n
        n -= 1


def fibonacci_gen(limit: int) -> Generator[int, None, None]:
    """Generate Fibonacci numbers up to a limit."""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b


# ============================================================
# 2. INFINITE SEQUENCES
# ============================================================
def infinite_counter(start: int = 0, step: int = 1) -> Generator[int, None, None]:
    """Generate an infinite sequence of numbers.
    
    WARNING: Always use break or itertools.islice when consuming!
    """
    current = start
    while True:
        yield current
        current += step


def infinite_primes() -> Generator[int, None, None]:
    """Yield prime numbers indefinitely using trial division."""
    yield 2
    candidate = 3
    while True:
        is_prime = True
        for i in range(2, int(candidate**0.5) + 1):
            if candidate % i == 0:
                is_prime = False
                break
        if is_prime:
            yield candidate
        candidate += 2


# ============================================================
# 3. YIELD FROM - DELEGATING TO SUB-GENERATORS
# ============================================================
def flatten(nested_list: list) -> Generator:
    """Recursively flatten a nested list of arbitrary depth.
    
    yield from delegates to another generator, simplifying
    recursive generator patterns.
    """
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def chain_generators(*generators: Iterable) -> Generator:
    """Chain multiple generators/iterables into one sequence.
    
    This is equivalent to itertools.chain but demonstrates yield from.
    """
    for gen in generators:
        yield from gen


# ============================================================
# 4. CUSTOM ITERATOR CLASS
# ============================================================
class FibonacciIterator:
    """Custom iterator that produces Fibonacci numbers.
    
    Implements the iterator protocol: __iter__ and __next__.
    """
    def __init__(self, max_value: int):
        self.max_value = max_value
        self.a = 0
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.a > self.max_value:
            raise StopIteration
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result


class CircularBuffer:
    """A circular buffer iterator that cycles through elements infinitely."""
    def __init__(self, items: list):
        if not items:
            raise ValueError("Buffer cannot be empty")
        self.items = items
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        item = self.items[self.index]
        self.index = (self.index + 1) % len(self.items)
        return item

    def take(self, n: int) -> list:
        """Take n items from the circular buffer."""
        return [next(self) for _ in range(n)]


# ============================================================
# 5. GENERATOR COROUTINES (send, throw, close)
# ============================================================
def accumulator() -> Generator:
    """A coroutine that accumulates values sent to it.
    
    Uses (yield) as an expression to receive values via .send().
    """
    total = 0.0
    count = 0
    while True:
        try:
            value = yield  # Receive a value
            if value is None:
                break
            total += value
            count += 1
            print(f"  Received: {value} | Total: {total} | Avg: {total/count:.2f}")
        except GeneratorExit:
            print(f"  Coroutine closed. Final total: {total}")
            return


def running_average() -> Generator[float, float, None]:
    """Coroutine that maintains a running average of sent values.
    
    Type: Generator[yield_type, send_type, return_type]
    """
    total = 0.0
    count = 0
    while True:
        value = yield total / count if count > 0 else 0.0
        total += value
        count += 1


# ============================================================
# 6. GENERATOR PIPELINES
# ============================================================
def read_data() -> Generator[str, None, None]:
    """Simulate reading lines of raw data."""
    data = [
        "  Alice, 85  ",
        "  Bob, 92  ",
        "  Charlie, -1  ",
        "  Diana, 78  ",
        "  Eve, 95  ",
        "  Frank, invalid  ",
        "  Grace, 88  ",
    ]
    yield from data


def clean_lines(lines: Iterable[str]) -> Generator[str, None, None]:
    """Pipeline stage: strip whitespace from lines."""
    for line in lines:
        cleaned = line.strip()
        if cleaned:
            yield cleaned


def parse_records(lines: Iterable[str]) -> Generator[tuple[str, int], None, None]:
    """Pipeline stage: parse name,score pairs."""
    for line in lines:
        try:
            name, score_str = line.split(",")
            name = name.strip()
            score = int(score_str.strip())
            if score >= 0:
                yield name, score
        except (ValueError, IndexError):
            continue  # Skip malformed lines


def filter_passing(records: Iterable[tuple[str, int]]) -> Generator[tuple[str, int], None, None]:
    """Pipeline stage: filter students with score >= 70."""
    for name, score in records:
        if score >= 70:
            yield name, score


# ============================================================
# 7. GENERATOR EXPRESSIONS (Memory-Efficient)
# ============================================================
def demonstrate_generator_expressions():
    """Show how generator expressions save memory vs list comprehensions."""
    import sys

    # List comprehension - stores everything in memory
    squares_list = [x**2 for x in range(10_000)]
    list_size = sys.getsizeof(squares_list)

    # Generator expression - produces values lazily
    squares_gen = (x**2 for x in range(10_000))
    gen_size = sys.getsizeof(squares_gen)

    print(f"List size:      {list_size:>10,} bytes")
    print(f"Generator size: {gen_size:>10,} bytes")
    print(f"Memory saved:   {list_size - gen_size:>10,} bytes")

    # Both produce the same sum
    print(f"Sum from list: {sum(squares_list):,}")
    print(f"Sum from gen:  {sum(squares_gen):,}")


# ============================================================
# 8. ITERTOOLS INTEGRATION
# ============================================================
def demonstrate_itertools():
    """Show powerful itertools functions combined with generators."""
    
    # islice: take a slice from an infinite generator
    first_20_primes = list(itertools.islice(infinite_primes(), 20))
    print(f"First 20 primes: {first_20_primes}")

    # takewhile: take while condition is true
    small_fibs = list(itertools.takewhile(lambda x: x < 100, fibonacci_gen(1000)))
    print(f"Fibonacci < 100: {small_fibs}")

    # groupby: group consecutive elements
    words = ["apple", "avocado", "banana", "blueberry", "cherry", "coconut"]
    grouped = itertools.groupby(words, key=lambda w: w[0])
    for letter, group in grouped:
        print(f"  '{letter}': {list(group)}")

    # product: cartesian product
    colors = ["red", "blue"]
    sizes = ["S", "M", "L"]
    combos = list(itertools.product(colors, sizes))
    print(f"Color-Size combos: {combos}")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Basic Generators")
    print("Countdown:", list(countdown(5)))
    print("Fibonacci < 50:", list(fibonacci_gen(50)))

    separator("2. Infinite Sequences (with islice)")
    first_10 = list(itertools.islice(infinite_counter(1, 3), 10))
    print(f"Counter (start=1, step=3): {first_10}")
    first_15_primes = list(itertools.islice(infinite_primes(), 15))
    print(f"First 15 primes: {first_15_primes}")

    separator("3. Yield From - Flatten")
    nested = [1, [2, 3], [4, [5, 6]], 7, [8, [9, [10]]]]
    print(f"Nested: {nested}")
    print(f"Flattened: {list(flatten(nested))}")

    chained = list(chain_generators([1, 2], (3, 4), range(5, 8)))
    print(f"Chained: {chained}")

    separator("4. Custom Iterator Class")
    fib_iter = FibonacciIterator(50)
    print(f"Fibonacci via iterator: {list(fib_iter)}")

    buffer = CircularBuffer(["red", "green", "blue"])
    print(f"Circular buffer (take 10): {buffer.take(10)}")

    separator("5. Coroutines (send)")
    print("Accumulator:")
    acc = accumulator()
    next(acc)  # Prime the coroutine
    acc.send(10.0)
    acc.send(20.0)
    acc.send(30.0)
    acc.close()

    print("\nRunning Average:")
    avg = running_average()
    next(avg)  # Prime
    for val in [10, 20, 30, 40, 50]:
        current_avg = avg.send(val)
        print(f"  Sent {val:3} -> Average: {current_avg:.2f}")

    separator("6. Generator Pipelines")
    raw_data = read_data()
    cleaned = clean_lines(raw_data)
    parsed = parse_records(cleaned)
    passing = filter_passing(parsed)
    
    print("Students who passed (score >= 70):")
    for name, score in passing:
        print(f"  {name}: {score}")

    separator("7. Generator Expressions (Memory)")
    demonstrate_generator_expressions()

    separator("8. Itertools Integration")
    demonstrate_itertools()


if __name__ == "__main__":
    main()
