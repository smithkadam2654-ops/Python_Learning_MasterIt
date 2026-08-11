"""
Advanced Python - Lesson 15: Enums & Type Hints
=================================================
Enums provide named constants, and type hints improve code
readability, IDE support, and static analysis.

Topics Covered:
- Enum basics and iteration
- IntEnum, StrEnum, Flag
- Enum with custom values and methods
- Type hints: basic types, Optional, Union
- Generic types (TypeVar)
- Type aliases and NewType
- TypedDict, NamedTuple with types
- Literal types
- Annotated types
"""

from enum import Enum, IntEnum, Flag, auto, unique
from typing import (
    Optional, Union, TypeVar, Generic,
    TypedDict, Literal, Annotated, NewType,
    Any, Callable
)
from dataclasses import dataclass


# ============================================================
# 1. BASIC ENUM
# ============================================================
class Color(Enum):
    """Basic enumeration of colors."""
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    PURPLE = 5

    # Custom method on enum
    def is_primary(self) -> bool:
        return self in (Color.RED, Color.GREEN, Color.BLUE)

    def complementary(self) -> "Color":
        """Return the complementary color."""
        complements = {
            Color.RED: Color.GREEN,
            Color.GREEN: Color.RED,
            Color.BLUE: Color.YELLOW,
            Color.YELLOW: Color.BLUE,
            Color.PURPLE: Color.YELLOW,
        }
        return complements[self]


def demonstrate_basic_enum():
    """Basic enum operations."""
    print(f"Color.RED = {Color.RED}")
    print(f"Name: {Color.RED.name}, Value: {Color.RED.value}")
    
    # Access by name or value
    print(f"Color['GREEN'] = {Color['GREEN']}")
    print(f"Color(3) = {Color(3)}")
    
    # Iteration
    print("\nAll colors:")
    for color in Color:
        print(f"  {color.name:8} = {color.value} (primary: {color.is_primary()})")
    
    # Comparison
    print(f"\nRED == RED: {Color.RED == Color.RED}")
    print(f"RED == GREEN: {Color.RED == Color.GREEN}")
    print(f"RED complementary: {Color.RED.complementary()}")


# ============================================================
# 2. AUTO-VALUED ENUM
# ============================================================
class Direction(Enum):
    """Enum with auto-generated values."""
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

    @property
    def opposite(self) -> "Direction":
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }
        return opposites[self]


# ============================================================
# 3. IntEnum (Comparable with integers)
# ============================================================
class Priority(IntEnum):
    """Priority levels — comparable with integers."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    def __str__(self) -> str:
        return f"{self.name}({self.value})"


class HttpStatus(IntEnum):
    """HTTP status codes as an enum."""
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    SERVER_ERROR = 500

    @property
    def is_success(self) -> bool:
        return 200 <= self < 300

    @property
    def is_client_error(self) -> bool:
        return 400 <= self < 500

    @property
    def message(self) -> str:
        messages = {
            200: "OK",
            201: "Created",
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        }
        return messages.get(self.value, "Unknown")


def demonstrate_int_enum():
    """IntEnum values can be compared with integers."""
    print(f"Priority.HIGH > Priority.LOW: {Priority.HIGH > Priority.LOW}")
    print(f"Priority.HIGH > 2: {Priority.HIGH > 2}")
    
    tasks = [
        ("Fix typo", Priority.LOW),
        ("Server down", Priority.CRITICAL),
        ("Add feature", Priority.MEDIUM),
        ("Security bug", Priority.HIGH),
    ]
    
    print("\nTasks sorted by priority:")
    for name, priority in sorted(tasks, key=lambda t: t[1], reverse=True):
        print(f"  [{priority}] {name}")
    
    print("\nHTTP Status codes:")
    for status in HttpStatus:
        category = "success" if status.is_success else "error"
        print(f"  {status.value} {status.message} ({category})")


# ============================================================
# 4. FLAG ENUM (Bitwise operations)
# ============================================================
class Permission(Flag):
    """Permissions that can be combined with bitwise OR."""
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    DELETE = auto()
    ADMIN = READ | WRITE | EXECUTE | DELETE

    def describe(self) -> str:
        if self == Permission.ADMIN:
            return "Full access"
        parts = []
        for perm in Permission:
            if perm in self and perm != Permission.ADMIN:
                parts.append(perm.name)
        return ", ".join(parts)


def demonstrate_flags():
    """Flag enums support bitwise operations."""
    user_perm = Permission.READ | Permission.WRITE
    admin_perm = Permission.ADMIN
    
    print(f"User permissions:  {user_perm} ({user_perm.describe()})")
    print(f"Admin permissions: {admin_perm} ({admin_perm.describe()})")
    
    print(f"\n  Can user read?    {Permission.READ in user_perm}")
    print(f"  Can user delete?  {Permission.DELETE in user_perm}")
    print(f"  Can admin delete? {Permission.DELETE in admin_perm}")
    
    # Add permission
    upgraded = user_perm | Permission.EXECUTE
    print(f"\n  After adding EXECUTE: {upgraded.describe()}")
    
    # Remove permission
    reduced = admin_perm & ~Permission.DELETE
    print(f"  After removing DELETE: {reduced.describe()}")
    
    # Check if has all
    has_rw = (Permission.READ | Permission.WRITE) in user_perm
    print(f"  Has READ+WRITE: {has_rw}")


# ============================================================
# 5. TYPE HINTS — BASIC AND ADVANCED
# ============================================================
# Type aliases
UserId = NewType("UserId", int)
Email = NewType("Email", str)
Score = Annotated[float, "Value between 0.0 and 100.0"]

# TypedDict for structured dictionaries
class UserRecord(TypedDict):
    name: str
    email: str
    age: int
    active: bool


def demonstrate_type_hints():
    """Type hints improve code clarity and tooling support."""
    
    # Basic type hints (shown in function signatures)
    def greet(name: str, times: int = 1) -> str:
        return (f"Hello, {name}! " * times).strip()

    def process_scores(scores: list[float]) -> dict[str, float]:
        return {
            "mean": sum(scores) / len(scores),
            "min": min(scores),
            "max": max(scores),
        }

    # Optional (can be None)
    def find_user(user_id: UserId) -> Optional[UserRecord]:
        users: dict[UserId, UserRecord] = {
            UserId(1): {"name": "Alice", "email": "alice@ex.com", "age": 30, "active": True},
            UserId(2): {"name": "Bob", "email": "bob@ex.com", "age": 25, "active": False},
        }
        return users.get(user_id)

    # Union types
    def format_value(value: Union[int, float, str]) -> str:
        if isinstance(value, (int, float)):
            return f"Number: {value}"
        return f"String: {value}"

    # Literal types
    def set_mode(mode: Literal["fast", "safe", "debug"]) -> str:
        return f"Mode set to: {mode}"

    # Callable types
    def apply(func: Callable[[int], int], values: list[int]) -> list[int]:
        return [func(v) for v in values]

    print(f"greet: {greet('Alice', 2)}")
    print(f"scores: {process_scores([85.5, 92.0, 78.5, 95.0])}")
    print(f"find user 1: {find_user(UserId(1))}")
    print(f"find user 9: {find_user(UserId(9))}")
    print(f"format int: {format_value(42)}")
    print(f"format str: {format_value('hello')}")
    print(f"set_mode: {set_mode('fast')}")
    print(f"apply: {apply(lambda x: x**2, [1,2,3,4])}")


# ============================================================
# 6. GENERICS WITH TYPEVAR
# ============================================================
T = TypeVar("T")


class Stack(Generic[T]):
    """A type-safe generic stack."""
    
    def __init__(self):
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items[-1]

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items})"


class Result(Generic[T]):
    """Generic result type (like Rust's Result)."""
    
    def __init__(self, value: T | None = None, error: str | None = None):
        self._value = value
        self._error = error

    @staticmethod
    def ok(value: T) -> "Result[T]":
        return Result(value=value)

    @staticmethod
    def err(message: str) -> "Result[Any]":
        return Result(error=message)

    @property
    def is_ok(self) -> bool:
        return self._error is None

    def unwrap(self) -> T:
        if self._error:
            raise RuntimeError(f"Unwrapping error result: {self._error}")
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value if self._value is not None else default

    def __repr__(self) -> str:
        if self.is_ok:
            return f"Ok({self._value!r})"
        return f"Err({self._error!r})"


def safe_divide(a: float, b: float) -> Result[float]:
    """Division that returns Result instead of raising."""
    if b == 0:
        return Result.err("Division by zero")
    return Result.ok(a / b)


def demonstrate_generics():
    """Generic classes work with any type while being type-safe."""
    
    # Stack of integers
    int_stack: Stack[int] = Stack()
    for n in [10, 20, 30]:
        int_stack.push(n)
    print(f"Int stack: {int_stack}")
    print(f"Pop: {int_stack.pop()}")
    
    # Stack of strings
    str_stack: Stack[str] = Stack()
    str_stack.push("hello")
    str_stack.push("world")
    print(f"String stack: {str_stack}")
    
    # Result type
    print(f"\nResult examples:")
    print(f"  10/3 = {safe_divide(10, 3)}")
    print(f"  10/0 = {safe_divide(10, 0)}")
    
    r = safe_divide(10, 3)
    print(f"  unwrap: {r.unwrap()}")
    
    r2 = safe_divide(10, 0)
    print(f"  unwrap_or: {r2.unwrap_or(0.0)}")


# ============================================================
# 7. ENUM WITH RICH BEHAVIOR
# ============================================================
class Operation(Enum):
    """Enum with embedded behavior (strategy-like)."""
    ADD = ("+", lambda a, b: a + b)
    SUBTRACT = ("-", lambda a, b: a - b)
    MULTIPLY = ("*", lambda a, b: a * b)
    DIVIDE = ("/", lambda a, b: a / b if b != 0 else float("inf"))

    def __init__(self, symbol: str, func: Callable):
        self.symbol = symbol
        self._func = func

    def apply(self, a: float, b: float) -> float:
        return self._func(a, b)

    def __str__(self) -> str:
        return self.symbol


def demonstrate_rich_enum():
    """Enums can carry data and behavior."""
    a, b = 10, 3
    print(f"Operations on {a} and {b}:")
    for op in Operation:
        result = op.apply(a, b)
        print(f"  {a} {op.symbol} {b} = {result}")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Basic Enum")
    demonstrate_basic_enum()

    separator("2. Auto-Valued Enum")
    for d in Direction:
        print(f"  {d.name:5} (val={d.value}) -> opposite: {d.opposite.name}")

    separator("3. IntEnum")
    demonstrate_int_enum()

    separator("4. Flag Enum")
    demonstrate_flags()

    separator("5. Type Hints")
    demonstrate_type_hints()

    separator("6. Generics")
    demonstrate_generics()

    separator("7. Enum with Rich Behavior")
    demonstrate_rich_enum()


if __name__ == "__main__":
    main()
