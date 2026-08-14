from typing import TypeVar, Generic, Callable, List, Optional, Protocol

# 1. Generics and TypeVars
T = TypeVar('T')

class Stack(Generic[T]):
    """A generic stack data structure."""
    def __init__(self):
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# 2. Protocols (Structural Subtyping / Duck Typing)
class Serializable(Protocol):
    """Defines a structural type that requires a serialize method."""
    def serialize(self) -> str:
        ...

class User:
    def __init__(self, name: str):
        self.name = name
    
    def serialize(self) -> str:
        return f"User({self.name})"

def process_serializable(obj: Serializable) -> None:
    """Accepts any object that has a serialize() -> str method."""
    print(f"Serialized object: {obj.serialize()}")

# 3. Callables
def apply_operation(x: int, y: int, op: Callable[[int, int], int]) -> int:
    return op(x, y)

if __name__ == "__main__":
    # Generic Stack
    int_stack = Stack[int]()
    int_stack.push(10)
    int_stack.push(20)
    print(f"Popped from int stack: {int_stack.pop()}")

    str_stack = Stack[str]()
    str_stack.push("hello")
    print(f"Popped from str stack: {str_stack.pop()}")

    # Protocol
    user = User("Alice")
    process_serializable(user)
    
    # Callable
    result = apply_operation(5, 3, lambda a, b: a * b)
    print(f"Operation result: {result}")
