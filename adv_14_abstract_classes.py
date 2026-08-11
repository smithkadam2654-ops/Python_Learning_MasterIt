"""
Advanced Python - Lesson 14: Abstract Base Classes & Interfaces
================================================================
ABCs define contracts that subclasses must follow. They enforce
a consistent interface across different implementations.

Topics Covered:
- abc.ABC and @abstractmethod
- Interface-like classes
- Mixin classes
- Protocol classes (structural subtyping)
- Registering virtual subclasses
- Abstract properties and class methods
- Template Method pattern with ABCs
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
import json
import math


# ============================================================
# 1. ABSTRACT BASE CLASS (ABC)
# ============================================================
class Shape(ABC):
    """Abstract base class for geometric shapes.
    
    Cannot be instantiated directly — only subclasses can be.
    """
    
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape."""
        pass

    @abstractmethod
    def describe(self) -> str:
        """Return a text description."""
        pass

    # Concrete method — available to all subclasses
    def is_larger_than(self, other: "Shape") -> bool:
        return self.area() > other.area()

    def __repr__(self):
        return f"{type(self).__name__}(area={self.area():.2f})"


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius

    def describe(self) -> str:
        return f"Circle with radius {self.radius}"


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def describe(self) -> str:
        return f"Rectangle {self.width}x{self.height}"


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c

    def describe(self) -> str:
        return f"Triangle with sides {self.a}, {self.b}, {self.c}"


# ============================================================
# 2. INTERFACE-LIKE ABC (All abstract, no implementation)
# ============================================================
class Serializable(ABC):
    """Interface for objects that can be serialized to/from JSON."""
    
    @abstractmethod
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "Serializable":
        """Create from dictionary."""
        pass

    def to_json(self) -> str:
        """Convert to JSON string (concrete helper)."""
        return json.dumps(self.to_dict(), indent=2)


class Printable(ABC):
    """Interface for objects that support formatted printing."""
    
    @abstractmethod
    def format_table(self) -> str:
        """Format as a table row."""
        pass

    @abstractmethod
    def format_summary(self) -> str:
        """Format as a summary."""
        pass


# ============================================================
# 3. IMPLEMENTING INTERFACES
# ============================================================
class User(Serializable, Printable):
    """User implements multiple interfaces."""
    
    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self.email = email
        self.age = age

    def to_dict(self) -> dict:
        return {"name": self.name, "email": self.email, "age": self.age}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(data["name"], data["email"], data["age"])

    def format_table(self) -> str:
        return f"| {self.name:15} | {self.email:25} | {self.age:3} |"

    def format_summary(self) -> str:
        return f"{self.name} ({self.age}) - {self.email}"


class Product(Serializable, Printable):
    """Product implements the same interfaces."""
    
    def __init__(self, title: str, price: float, stock: int):
        self.title = title
        self.price = price
        self.stock = stock

    def to_dict(self) -> dict:
        return {"title": self.title, "price": self.price, "stock": self.stock}

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(data["title"], data["price"], data["stock"])

    def format_table(self) -> str:
        return f"| {self.title:20} | ${self.price:>8.2f} | {self.stock:>5} |"

    def format_summary(self) -> str:
        return f"{self.title}: ${self.price:.2f} ({self.stock} in stock)"


# ============================================================
# 4. MIXIN CLASSES
# ============================================================
class JsonMixin:
    """Mixin that adds JSON serialization to any class with to_dict()."""
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)


class ComparisonMixin:
    """Mixin that adds comparison operators based on a key."""
    
    @abstractmethod
    def sort_key(self):
        """Return the value to use for comparisons."""
        pass

    def __lt__(self, other):
        return self.sort_key() < other.sort_key()

    def __le__(self, other):
        return self.sort_key() <= other.sort_key()

    def __gt__(self, other):
        return self.sort_key() > other.sort_key()

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.sort_key() == other.sort_key()

    def __hash__(self):
        return hash(self.sort_key())


class Student(JsonMixin, ComparisonMixin):
    """Student with JSON and comparison mixins."""
    
    def __init__(self, name: str, gpa: float, credits: int):
        self.name = name
        self.gpa = gpa
        self.credits = credits

    def to_dict(self) -> dict:
        return {"name": self.name, "gpa": self.gpa, "credits": self.credits}

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(data["name"], data["gpa"], data["credits"])

    def sort_key(self):
        return self.gpa  # Sort by GPA

    def __repr__(self):
        return f"Student({self.name}, GPA={self.gpa:.2f})"


# ============================================================
# 5. PROTOCOL (Structural Subtyping / Duck Typing)
# ============================================================
@runtime_checkable
class Drawable(Protocol):
    """Protocol: any object with a draw() method.
    
    Unlike ABCs, Protocols don't require explicit inheritance.
    Any class with the right methods satisfies the protocol.
    """
    def draw(self) -> str:
        ...


@runtime_checkable
class Resizable(Protocol):
    """Protocol for resizable objects."""
    def resize(self, factor: float) -> None:
        ...


class Button:
    """Button doesn't inherit from Drawable, but has draw()."""
    def __init__(self, label: str):
        self.label = label

    def draw(self) -> str:
        return f"[ {self.label} ]"


class Icon:
    """Icon also satisfies the Drawable protocol."""
    def __init__(self, name: str):
        self.name = name

    def draw(self) -> str:
        return f"({self.name})"


def render_all(items: list[Drawable]):
    """Accepts anything with a draw() method."""
    for item in items:
        print(f"  Rendering: {item.draw()}")


def demonstrate_protocols():
    """Protocols enable duck typing with type checker support."""
    
    button = Button("Submit")
    icon = Icon("star")
    
    # Both satisfy Drawable protocol without inheriting from it
    print(f"Button is Drawable: {isinstance(button, Drawable)}")
    print(f"Icon is Drawable:   {isinstance(icon, Drawable)}")
    print(f"'hello' is Drawable: {isinstance('hello', Drawable)}")
    
    render_all([button, icon])


# ============================================================
# 6. TEMPLATE METHOD PATTERN
# ============================================================
class DataPipeline(ABC):
    """Template Method: defines algorithm skeleton in base class.
    
    Subclasses override specific steps without changing the structure.
    """
    
    def run(self):
        """Template method — defines the algorithm structure."""
        raw_data = self.extract()
        cleaned = self.transform(raw_data)
        validated = self.validate(cleaned)
        result = self.load(validated)
        self.on_complete(result)
        return result

    @abstractmethod
    def extract(self) -> list:
        """Step 1: Extract raw data."""
        pass

    @abstractmethod
    def transform(self, data: list) -> list:
        """Step 2: Transform/clean data."""
        pass

    def validate(self, data: list) -> list:
        """Step 3: Validate (default implementation)."""
        return [item for item in data if item is not None]

    @abstractmethod
    def load(self, data: list) -> dict:
        """Step 4: Load/store the result."""
        pass

    def on_complete(self, result: dict):
        """Step 5: Hook for completion callback (optional)."""
        print(f"  Pipeline complete: {len(result.get('data', []))} records processed")


class CSVPipeline(DataPipeline):
    """Pipeline for CSV data."""
    
    def __init__(self, raw_lines: list[str]):
        self.raw_lines = raw_lines

    def extract(self) -> list:
        print("  [CSV] Extracting data...")
        return [line.strip() for line in self.raw_lines if line.strip()]

    def transform(self, data: list) -> list:
        print("  [CSV] Transforming data...")
        result = []
        for line in data[1:]:  # Skip header
            parts = line.split(",")
            if len(parts) >= 3:
                result.append({
                    "name": parts[0].strip(),
                    "age": int(parts[1].strip()),
                    "score": float(parts[2].strip()),
                })
        return result

    def load(self, data: list) -> dict:
        print("  [CSV] Loading data...")
        return {"source": "csv", "data": data, "count": len(data)}


class APIPipeline(DataPipeline):
    """Pipeline for API data."""
    
    def __init__(self, mock_response: dict):
        self.mock_response = mock_response

    def extract(self) -> list:
        print("  [API] Extracting data...")
        return self.mock_response.get("items", [])

    def transform(self, data: list) -> list:
        print("  [API] Transforming data...")
        return [
            {"name": item["n"], "value": item["v"]}
            for item in data
            if "n" in item and "v" in item
        ]

    def load(self, data: list) -> dict:
        print("  [API] Loading data...")
        return {"source": "api", "data": data, "count": len(data)}


# ============================================================
# 7. VIRTUAL SUBCLASS REGISTRATION
# ============================================================
class Iterable(ABC):
    """Custom iterable ABC."""
    
    @abstractmethod
    def __iter__(self):
        pass


class CustomRange:
    """Custom range — NOT inheriting from Iterable."""
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop

    def __iter__(self):
        current = self.start
        while current < self.stop:
            yield current
            current += 1


# Register as virtual subclass
Iterable.register(CustomRange)


def demonstrate_virtual_subclass():
    """Virtual subclasses satisfy isinstance without inheritance."""
    cr = CustomRange(1, 5)
    print(f"CustomRange is Iterable: {isinstance(cr, Iterable)}")
    print(f"CustomRange.__mro__: {[c.__name__ for c in CustomRange.__mro__]}")
    print(f"Values: {list(cr)}")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Abstract Base Class (Shapes)")
    shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
    for shape in shapes:
        print(f"  {shape.describe()}")
        print(f"    Area: {shape.area():.2f}, Perimeter: {shape.perimeter():.2f}")
    
    print(f"\n  Circle > Rectangle? {shapes[0].is_larger_than(shapes[1])}")
    
    # Cannot instantiate abstract class
    try:
        Shape()
    except TypeError as e:
        print(f"  Cannot create Shape: {e}")

    separator("2-3. Interfaces (Serializable + Printable)")
    user = User("Alice", "alice@example.com", 30)
    product = Product("Widget", 29.99, 100)
    
    print(f"User JSON:\n{user.to_json()}")
    print(f"\nProduct table: {product.format_table()}")
    print(f"Product summary: {product.format_summary()}")
    
    # Round-trip serialization
    user_dict = user.to_dict()
    restored = User.from_dict(user_dict)
    print(f"Restored: {restored.format_summary()}")

    separator("4. Mixins")
    students = [
        Student("Alice", 3.8, 90),
        Student("Bob", 3.5, 85),
        Student("Charlie", 3.9, 92),
    ]
    ranked = sorted(students, reverse=True)
    print("Students ranked by GPA:")
    for s in ranked:
        print(f"  {s}")
    
    print(f"\nStudent JSON:\n{students[0].to_json()}")

    separator("5. Protocols (Structural Subtyping)")
    demonstrate_protocols()

    separator("6. Template Method Pattern")
    csv_lines = [
        "name, age, score",
        "Alice, 30, 95.5",
        "Bob, 25, 87.0",
        "Charlie, 35, 92.3",
    ]
    print("\nCSV Pipeline:")
    csv_result = CSVPipeline(csv_lines).run()
    
    print("\nAPI Pipeline:")
    api_data = {"items": [{"n": "item1", "v": 100}, {"n": "item2", "v": 200}]}
    api_result = APIPipeline(api_data).run()

    separator("7. Virtual Subclass")
    demonstrate_virtual_subclass()


if __name__ == "__main__":
    main()
