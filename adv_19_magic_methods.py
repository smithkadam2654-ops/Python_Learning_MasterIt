"""
Advanced Python - Lesson 19: Magic (Dunder) Methods
=====================================================
Magic methods (double-underscore / dunder methods) let you define
how your objects behave with built-in Python operations.

Topics Covered:
- Object representation (__repr__, __str__, __format__)
- Comparison (__eq__, __lt__, __hash__)
- Arithmetic operators (__add__, __mul__, etc.)
- Container protocols (__len__, __getitem__, __contains__)
- Context managers (__enter__, __exit__)
- Callable objects (__call__)
- Attribute access (__getattr__, __setattr__)
- Descriptor protocol (__get__, __set__)
"""

from typing import Any
import math
from functools import total_ordering


# ============================================================
# 1. OBJECT REPRESENTATION
# ============================================================
class Money:
    """Demonstrates __repr__, __str__, and __format__."""
    
    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = amount
        self.currency = currency

    def __repr__(self) -> str:
        """Unambiguous representation for developers."""
        return f"Money({self.amount}, {self.currency!r})"

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"${self.amount:,.2f} {self.currency}"

    def __format__(self, format_spec: str) -> str:
        """Custom format specifications.
        
        Usage:
            f"{money:short}"  -> "$1,234.56"
            f"{money:full}"   -> "1,234.56 USD"
            f"{money:.0f}"    -> "$1,235"
        """
        if format_spec == "short":
            return f"${self.amount:,.2f}"
        elif format_spec == "full":
            return f"{self.amount:,.2f} {self.currency}"
        elif format_spec:
            return f"${self.amount:{format_spec}}"
        return str(self)

    def __bool__(self) -> bool:
        """Truthy if amount is non-zero."""
        return self.amount != 0


# ============================================================
# 2. COMPARISON AND ORDERING
# ============================================================
@total_ordering  # Only need __eq__ and one of __lt__, __le__, __gt__, __ge__
class Version:
    """Software version with comparison support (e.g., 1.2.3)."""
    
    def __init__(self, major: int, minor: int = 0, patch: int = 0):
        self.major = major
        self.minor = minor
        self.patch = patch
        self._tuple = (major, minor, patch)

    def __repr__(self) -> str:
        return f"Version({self.major}, {self.minor}, {self.patch})"

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            other = Version.from_string(other)
        if not isinstance(other, Version):
            return NotImplemented
        return self._tuple == other._tuple

    def __lt__(self, other: "Version") -> bool:
        if isinstance(other, str):
            other = Version.from_string(other)
        return self._tuple < other._tuple

    def __hash__(self) -> int:
        return hash(self._tuple)

    @classmethod
    def from_string(cls, version_str: str) -> "Version":
        parts = version_str.split(".")
        return cls(int(parts[0]), int(parts[1]) if len(parts) > 1 else 0,
                   int(parts[2]) if len(parts) > 2 else 0)


# ============================================================
# 3. ARITHMETIC OPERATORS
# ============================================================
class Vector:
    """2D vector with full arithmetic support."""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    # Addition
    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    # In-place addition
    def __iadd__(self, other: "Vector") -> "Vector":
        self.x += other.x
        self.y += other.y
        return self

    # Subtraction
    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    # Negation
    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y)

    # Multiplication (scalar and dot product)
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        if isinstance(other, Vector):
            # Dot product
            return self.x * other.x + self.y * other.y
        return NotImplemented

    def __rmul__(self, other):
        """Right multiplication: scalar * vector."""
        return self.__mul__(other)

    # True division
    def __truediv__(self, scalar: float) -> "Vector":
        return Vector(self.x / scalar, self.y / scalar)

    # Floor division
    def __floordiv__(self, scalar: float) -> "Vector":
        return Vector(self.x // scalar, self.y // scalar)

    # Power (magnitude to a power)
    def __pow__(self, exp: int) -> float:
        return self.magnitude() ** exp

    # Absolute value (magnitude)
    def __abs__(self) -> float:
        return self.magnitude()

    # Magnitude
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # Equality
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    # Hash
    def __hash__(self) -> int:
        return hash((round(self.x, 10), round(self.y, 10)))

    # Boolean (zero vector is falsy)
    def __bool__(self) -> bool:
        return self.x != 0 or self.y != 0


# ============================================================
# 4. CONTAINER PROTOCOL
# ============================================================
class SortedList:
    """Custom sorted container with full sequence protocol."""
    
    def __init__(self, items: list | None = None):
        self._items: list = sorted(items) if items else []

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return SortedList(self._items[index])
        return self._items[index]

    def __setitem__(self, index: int, value):
        self._items[index] = value
        self._items.sort()  # Re-sort after modification

    def __delitem__(self, index: int):
        del self._items[index]

    def __contains__(self, item) -> bool:
        """Membership test."""
        return item in self._items

    def __iter__(self):
        return iter(self._items)

    def __reversed__(self):
        return reversed(self._items)

    def __repr__(self) -> str:
        return f"SortedList({self._items})"

    def __add__(self, other: "SortedList") -> "SortedList":
        return SortedList(self._items + other._items)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SortedList):
            return NotImplemented
        return self._items == other._items

    def add(self, item):
        """Insert in sorted position."""
        import bisect
        bisect.insort(self._items, item)

    def __bool__(self) -> bool:
        return len(self._items) > 0


# ============================================================
# 5. CALLABLE OBJECTS
# ============================================================
class FunctionPipeline:
    """Callable object that chains transformations.
    
    __call__ makes instances behave like functions.
    """
    
    def __init__(self, *functions):
        self.functions = list(functions)

    def __call__(self, value):
        """Make the object callable."""
        result = value
        for func in self.functions:
            result = func(result)
        return result

    def __or__(self, other: "FunctionPipeline") -> "FunctionPipeline":
        """Pipe operator: pipeline1 | pipeline2."""
        return FunctionPipeline(*(self.functions + other.functions))

    def __rshift__(self, func) -> "FunctionPipeline":
        """Right shift: pipeline >> function."""
        return FunctionPipeline(*(self.functions + [func]))

    def __repr__(self) -> str:
        names = [f.__name__ if hasattr(f, '__name__') else str(f)
                 for f in self.functions]
        return f"Pipeline({' >> '.join(names)})"


class Accumulator:
    """Callable accumulator that maintains state."""
    
    def __init__(self, initial: float = 0):
        self.total = initial
        self._history: list[float] = []

    def __call__(self, value: float = 0) -> float:
        self.total += value
        self._history.append(value)
        return self.total

    def __iadd__(self, value: float):
        self.total += value
        self._history.append(value)
        return self

    def reset(self):
        self.total = 0
        self._history.clear()

    def __repr__(self) -> str:
        return f"Accumulator(total={self.total}, count={len(self._history)})"


# ============================================================
# 6. ATTRIBUTE ACCESS CONTROL
# ============================================================
class DynamicAttributes:
    """Control attribute access with __getattr__ and __setattr__."""
    
    def __init__(self, **kwargs):
        # Use object.__setattr__ to avoid triggering our custom __setattr__
        object.__setattr__(self, "_data", {})
        for key, value in kwargs.items():
            self._data[key] = value

    def __getattr__(self, name: str) -> Any:
        """Called when normal attribute lookup fails."""
        if name.startswith("_"):
            raise AttributeError(f"No attribute '{name}'")
        # Auto-vivification: create nested objects on access
        if name not in self._data:
            self._data[name] = DynamicAttributes()
        return self._data[name]

    def __setattr__(self, name: str, value: Any):
        """Called on every attribute assignment."""
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            print(f"  [SET] {name} = {value!r}")
            self._data[name] = value

    def __delattr__(self, name: str):
        """Called on del obj.attr."""
        if name in self._data:
            del self._data[name]
            print(f"  [DEL] {name}")
        else:
            raise AttributeError(f"No attribute '{name}'")

    def __dir__(self) -> list[str]:
        """Custom dir() output."""
        return list(self._data.keys())

    def __repr__(self) -> str:
        return f"DynamicAttributes({self._data})"


# ============================================================
# 7. NUMERIC PROTOCOL: FRACTION CLASS
# ============================================================
class Fraction:
    """Custom fraction with full numeric protocol."""
    
    def __init__(self, numerator: int, denominator: int = 1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        # Simplify
        g = math.gcd(abs(numerator), abs(denominator))
        self.num = numerator // g
        self.den = denominator // g
        # Keep denominator positive
        if self.den < 0:
            self.num = -self.num
            self.den = -self.den

    def __repr__(self) -> str:
        return f"Fraction({self.num}, {self.den})"

    def __str__(self) -> str:
        if self.den == 1:
            return str(self.num)
        return f"{self.num}/{self.den}"

    def __add__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        new_num = self.num * other.den + other.num * self.den
        new_den = self.den * other.den
        return Fraction(new_num, new_den)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        new_num = self.num * other.den - other.num * self.den
        new_den = self.den * other.den
        return Fraction(new_num, new_den)

    def __mul__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.num * other.num, self.den * other.den)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.num * other.den, self.den * other.num)

    def __float__(self) -> float:
        """Convert to float."""
        return self.num / self.den

    def __int__(self) -> int:
        """Convert to int (truncated)."""
        return self.num // self.den

    def __eq__(self, other) -> bool:
        if isinstance(other, int):
            return self.num == other and self.den == 1
        if isinstance(other, Fraction):
            return self.num == other.num and self.den == other.den
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.num, self.den))

    def __lt__(self, other) -> bool:
        if isinstance(other, (int, Fraction)):
            return float(self) < float(other)
        return NotImplemented


# ============================================================
# 8. CONTEXT MANAGER + ITERABLE: DATABASE MOCK
# ============================================================
class MockDatabase:
    """Object that is a context manager, iterable, and callable."""
    
    def __init__(self, name: str):
        self.name = name
        self._data: list[dict] = []
        self._connected = False

    # Context manager protocol
    def __enter__(self):
        print(f"  Connecting to {self.name}...")
        self._connected = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  Disconnecting from {self.name}...")
        self._connected = False
        return False

    # Callable protocol
    def __call__(self, query: str) -> list[dict]:
        """Execute a query."""
        if not self._connected:
            raise RuntimeError("Not connected")
        print(f"  Query: {query}")
        return self._data

    # Container protocol
    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __contains__(self, item: dict) -> bool:
        return item in self._data

    def insert(self, record: dict):
        self._data.append(record)

    def __repr__(self) -> str:
        status = "connected" if self._connected else "disconnected"
        return f"MockDatabase({self.name!r}, {status}, {len(self._data)} records)"


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Object Representation (Money)")
    price = Money(1234.56, "USD")
    print(f"repr:  {price!r}")
    print(f"str:   {price}")
    print(f"short: {price:short}")
    print(f"full:  {price:full}")
    print(f".0f:   {price:.0f}")
    print(f"bool(Money(0)): {bool(Money(0, 'USD'))}")
    print(f"bool(Money(1)): {bool(Money(1, 'USD'))}")

    separator("2. Comparison (Version)")
    versions = [
        Version(2, 1, 0),
        Version(1, 9, 5),
        Version(2, 0, 0),
        Version(1, 0, 0),
        Version.from_string("3.0.1"),
    ]
    print("Unsorted:", [str(v) for v in versions])
    print("Sorted:  ", [str(v) for v in sorted(versions)])
    print(f"v2.1.0 > v1.9.5: {Version(2,1,0) > Version(1,9,5)}")
    print(f"v1.0.0 == '1.0.0': {Version(1,0,0) == '1.0.0'}")

    separator("3. Arithmetic (Vector)")
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3  = {v1 * 3}")
    print(f"2 * v1  = {2 * v1}")
    print(f"v1 * v2 (dot) = {v1 * v2}")
    print(f"|v1| = {abs(v1)}")
    print(f"-v1 = {-v1}")
    print(f"v1 / 2 = {v1 / 2}")

    separator("4. Container (SortedList)")
    sl = SortedList([5, 3, 1, 4, 2])
    print(f"Created: {sl}")
    sl.add(6)
    sl.add(0)
    print(f"After add: {sl}")
    print(f"len: {len(sl)}")
    print(f"sl[2]: {sl[2]}")
    print(f"3 in sl: {3 in sl}")
    print(f"Reversed: {list(reversed(sl))}")
    print(f"Slice [1:4]: {sl[1:4]}")

    separator("5. Callable Objects")
    pipeline = FunctionPipeline(
        lambda x: x * 2,
        lambda x: x + 1,
        lambda x: x ** 2,
    )
    print(f"Pipeline: {pipeline}")
    print(f"Pipeline(5) = {pipeline(5)}")  # ((5*2)+1)^2 = 121
    
    p2 = pipeline >> (lambda x: x - 1)
    print(f"Extended: {p2}")
    print(f"Extended(5) = {p2(5)}")  # 121 - 1 = 120

    acc = Accumulator(100)
    acc(50)
    acc(25)
    print(f"\nAccumulator: {acc}")
    print(f"Total: {acc()}")

    separator("6. Dynamic Attributes")
    obj = DynamicAttributes(name="Alice", age=30)
    print(f"Created: {obj}")
    obj.email = "alice@example.com"
    print(f"dir: {dir(obj)}")
    del obj.age
    print(f"After del: {obj}")

    separator("7. Fraction Class")
    f1 = Fraction(1, 3)
    f2 = Fraction(1, 6)
    f3 = Fraction(1, 2)
    print(f"{f1} + {f2} = {f1 + f2}")
    print(f"{f1} + {f3} = {f1 + f3}")
    print(f"{f1} * {f3} = {f1 * f3}")
    print(f"{f1} / {f2} = {f1 / f2}")
    print(f"float({f1}) = {float(f1):.4f}")
    print(f"1 + {f1} = {1 + f1}")
    print(f"{f1} + 2 = {f1 + 2}")

    separator("8. Multi-Protocol Object (MockDatabase)")
    db = MockDatabase("test_db")
    with db:
        db.insert({"id": 1, "name": "Alice"})
        db.insert({"id": 2, "name": "Bob"})
        results = db("SELECT * FROM users")
        print(f"  Query returned {len(results)} records")
        for record in db:
            print(f"    {record}")
    print(f"  After context: {db}")


if __name__ == "__main__":
    main()
