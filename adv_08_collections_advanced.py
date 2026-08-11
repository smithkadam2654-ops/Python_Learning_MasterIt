"""
Advanced Python - Lesson 08: Collections Module
=================================================
The collections module provides specialized container datatypes
that are more powerful and efficient than built-in types.

Topics Covered:
- Counter: count hashable objects
- defaultdict: auto-initialize missing keys
- OrderedDict: insertion-ordered dictionary (Python 3.7+ dicts are ordered)
- deque: fast appends/pops from both ends
- namedtuple: lightweight data objects
- ChainMap: group multiple dicts
"""

from collections import Counter, defaultdict, deque, namedtuple, ChainMap
import re


# ============================================================
# 1. COUNTER
# ============================================================
def demonstrate_counter():
    """Counter counts occurrences of elements."""
    
    # Count characters in a string
    text = "supercalifragilisticexpialidocious"
    char_count = Counter(text)
    print(f"Text: '{text}'")
    print(f"  Most common chars: {char_count.most_common(5)}")
    print(f"  Total unique: {len(char_count)}")
    print(f"  Total chars:  {sum(char_count.values())}")

    # Count words in a sentence
    sentence = "the quick brown fox jumps over the lazy dog the fox"
    words = sentence.split()
    word_count = Counter(words)
    print(f"\nSentence: '{sentence}'")
    print(f"  Word counts: {dict(word_count)}")
    print(f"  'the' appears: {word_count['the']} times")
    print(f"  'fox' appears: {word_count['fox']} times")

    # Counter arithmetic
    inventory1 = Counter(apples=10, bananas=5, oranges=8)
    inventory2 = Counter(apples=3, bananas=7, grapes=12)
    
    print(f"\nInventory arithmetic:")
    print(f"  Store 1: {dict(inventory1)}")
    print(f"  Store 2: {dict(inventory2)}")
    print(f"  Combined: {dict(inventory1 + inventory2)}")
    print(f"  Difference: {dict(inventory1 - inventory2)}")
    print(f"  Intersection: {dict(inventory1 & inventory2)}")
    print(f"  Union: {dict(inventory1 | inventory2)}")

    # Find top-N elements
    scores = Counter({
        "Alice": 95, "Bob": 87, "Charlie": 92,
        "Diana": 98, "Eve": 85, "Frank": 91,
    })
    print(f"\n  Top 3 scorers: {scores.most_common(3)}")


# ============================================================
# 2. DEFAULTDICT
# ============================================================
def demonstrate_defaultdict():
    """defaultdict auto-creates missing keys with a default value."""
    
    # Group words by first letter
    words = ["apple", "avocado", "banana", "blueberry", "cherry",
             "coconut", "date", "dragonfruit", "elderberry"]
    
    by_letter: defaultdict[str, list[str]] = defaultdict(list)
    for word in words:
        by_letter[word[0]].append(word)
    
    print("Words grouped by first letter:")
    for letter, group in sorted(by_letter.items()):
        print(f"  '{letter}': {group}")

    # Count with defaultdict
    text = "mississippi"
    char_count: defaultdict[str, int] = defaultdict(int)
    for char in text:
        char_count[char] += 1
    print(f"\nCharacter count in '{text}':")
    for char, count in sorted(char_count.items(), key=lambda x: -x[1]):
        print(f"  '{char}': {'#' * count} ({count})")

    # Nested defaultdict (2D grid)
    grid: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
    grid["A"]["B"] = 10
    grid["A"]["C"] = 20
    grid["B"]["C"] = 15
    print(f"\nDistance grid:")
    for src in sorted(grid):
        for dst in sorted(grid[src]):
            print(f"  {src} -> {dst}: {grid[src][dst]}")

    # Default factory with custom function
    def default_entry():
        return {"count": 0, "items": []}
    
    tracker: defaultdict[str, dict] = defaultdict(default_entry)
    tracker["errors"]["count"] += 1
    tracker["errors"]["items"].append("timeout")
    tracker["errors"]["items"].append("500 error")
    print(f"\nError tracker: {dict(tracker)}")


# ============================================================
# 3. DEQUE (Double-Ended Queue)
# ============================================================
def demonstrate_deque():
    """Deque provides O(1) appends and pops from both ends."""
    
    # Basic operations
    dq: deque[int] = deque([1, 2, 3, 4, 5])
    print(f"Initial: {list(dq)}")
    
    dq.appendleft(0)
    dq.append(6)
    print(f"After appendleft(0), append(6): {list(dq)}")
    
    left = dq.popleft()
    right = dq.pop()
    print(f"After popleft()={left}, pop()={right}: {list(dq)}")

    # Rotation
    dq = deque([1, 2, 3, 4, 5])
    dq.rotate(2)
    print(f"\nRotate right by 2: {list(dq)}")
    dq.rotate(-2)
    print(f"Rotate left by 2:  {list(dq)}")

    # Max-length deque (sliding window)
    window: deque[int] = deque(maxlen=3)
    print(f"\nSliding window (maxlen=3):")
    for i in range(7):
        window.append(i)
        print(f"  append({i}) -> {list(window)}")

    # Implement a queue
    print("\nQueue simulation:")
    queue: deque[str] = deque()
    for task in ["email", "report", "meeting", "code review"]:
        queue.append(task)
        print(f"  Enqueued: {task}")
    while queue:
        print(f"  Dequeued: {queue.popleft()}")

    # Implement a stack
    print("\nStack simulation:")
    stack: deque[str] = deque()
    for item in ["first", "second", "third"]:
        stack.append(item)
        print(f"  Pushed: {item}")
    while stack:
        print(f"  Popped: {stack.pop()}")


# ============================================================
# 4. NAMEDTUPLE
# ============================================================
def demonstrate_namedtuple():
    """namedtuple creates lightweight data objects with named fields."""
    
    # Basic namedtuple
    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 4)
    print(f"Point: {p}")
    print(f"  x={p.x}, y={p.y}")
    print(f"  tuple access: p[0]={p[0]}, p[1]={p[1]}")

    # With defaults (Python 3.6.1+)
    Color = namedtuple("Color", "r g b alpha", defaults=[255])
    red = Color(255, 0, 0)
    transparent = Color(0, 0, 0, 128)
    print(f"\nColor with defaults:")
    print(f"  Red:         {red}")
    print(f"  Transparent: {transparent}")

    # _replace (create modified copy)
    p2 = p._replace(x=10)
    print(f"\n_replace: {p} -> {p2}")

    # _asdict
    print(f"_asdict: {p._asdict()}")

    # _fields
    print(f"_fields: {Point._fields}")

    # Practical use: parsing CSV-like data
    Record = namedtuple("Record", "name age city salary")
    data = [
        "Alice,30,NYC,85000",
        "Bob,25,LA,72000",
        "Charlie,35,Chicago,95000",
    ]
    
    print("\nParsed records:")
    records = []
    for line in data:
        parts = line.split(",")
        record = Record(parts[0], int(parts[1]), parts[2], float(parts[3]))
        records.append(record)
        print(f"  {record.name}: ${record.salary:,.0f} in {record.city}")

    # Sorting namedtuples
    by_salary = sorted(records, key=lambda r: r.salary, reverse=True)
    print("\nSorted by salary:")
    for r in by_salary:
        print(f"  {r.name}: ${r.salary:,.0f}")


# ============================================================
# 5. CHAINMAP
# ============================================================
def demonstrate_chainmap():
    """ChainMap groups multiple dicts into a single view.
    
    Lookups search maps in order; writes go to the first map.
    """
    
    # Configuration with defaults and overrides
    defaults = {"color": "blue", "size": "medium", "debug": False}
    user_prefs = {"color": "red", "font": "Arial"}
    cli_args = {"debug": True, "verbose": True}

    config = ChainMap(cli_args, user_prefs, defaults)
    
    print("Configuration ChainMap:")
    print(f"  color   = {config['color']}")     # cli_args -> user_prefs -> defaults
    print(f"  size    = {config['size']}")       # defaults
    print(f"  debug   = {config['debug']}")      # cli_args overrides
    print(f"  font    = {config['font']}")       # user_prefs
    print(f"  verbose = {config['verbose']}")    # cli_args

    print(f"\n  All keys: {list(config.keys())}")
    print(f"  Maps count: {len(config.maps)}")

    # New_child: add a new layer
    overrides = {"color": "green", "size": "large"}
    extended = config.new_child(overrides)
    print(f"\n  With overrides: color={extended['color']}, size={extended['size']}")

    # Practical use: variable scope resolution
    global_scope = {"x": 10, "y": 20, "z": 30}
    local_scope = {"x": 100, "w": 40}
    
    scopes = ChainMap(local_scope, global_scope)
    print(f"\nScope resolution:")
    print(f"  x = {scopes['x']} (local wins)")
    print(f"  y = {scopes['y']} (from global)")
    print(f"  w = {scopes['w']} (from local)")


# ============================================================
# 6. PRACTICAL: WORD FREQUENCY ANALYZER
# ============================================================
def word_frequency_analyzer():
    """Build a word frequency analyzer using collections."""
    
    sample_text = """
    Python is a versatile programming language. Python is used for
    web development, data science, automation, and more. Python is
    known for its simple and readable syntax. Many developers choose
    Python for rapid prototyping and production systems.
    """

    # Clean and split
    words = re.findall(r'\b\w+\b', sample_text.lower())
    
    # Count with Counter
    freq = Counter(words)
    
    print("Word Frequency Analysis:")
    print(f"  Total words: {len(words)}")
    print(f"  Unique words: {len(freq)}")
    print(f"\n  Top 10 words:")
    for word, count in freq.most_common(10):
        bar = "█" * count
        print(f"    {word:15} {bar} ({count})")

    # Words appearing exactly once (hapax legomena)
    hapax = [word for word, count in freq.items() if count == 1]
    print(f"\n  Words appearing once: {sorted(hapax)}")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Counter")
    demonstrate_counter()

    separator("2. defaultdict")
    demonstrate_defaultdict()

    separator("3. deque")
    demonstrate_deque()

    separator("4. namedtuple")
    demonstrate_namedtuple()

    separator("5. ChainMap")
    demonstrate_chainmap()

    separator("6. Word Frequency Analyzer")
    word_frequency_analyzer()


if __name__ == "__main__":
    main()
