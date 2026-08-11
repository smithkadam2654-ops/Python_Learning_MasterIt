"""
Advanced Python - Lesson 07: Advanced Dataclasses
===================================================
Dataclasses (Python 3.7+) reduce boilerplate for classes that
primarily store data. They auto-generate __init__, __repr__, etc.

Topics Covered:
- Basic dataclass features
- Field options (default, repr, compare, init)
- Frozen (immutable) dataclasses
- Post-init processing
- Inheritance with dataclasses
- Slots (Python 3.10+)
- KW_ONLY fields
- Custom __eq__ and __hash__
- dataclass_transform
"""

from dataclasses import dataclass, field, asdict, astuple, replace, fields
from typing import Any
from datetime import datetime
import json


# ============================================================
# 1. BASIC DATACLASS
# ============================================================
@dataclass
class Point:
    """A simple 2D point."""
    x: float
    y: float
    label: str = "origin"

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


# ============================================================
# 2. FIELD OPTIONS
# ============================================================
@dataclass
class Product:
    """Product with various field configurations."""
    name: str
    price: float
    quantity: int = 0
    # field(default_factory=...) for mutable defaults
    tags: list[str] = field(default_factory=list)
    # repr=False hides from __repr__
    internal_id: str = field(default="", repr=False)
    # compare=False excludes from equality/hash checks
    created_at: datetime = field(default_factory=datetime.now, compare=False)
    # init=False means it's not set in __init__
    is_available: bool = field(init=False, default=True)

    def __post_init__(self):
        """Called after __init__ for validation and computed fields."""
        if self.price < 0:
            raise ValueError(f"Price must be non-negative, got {self.price}")
        if self.quantity < 0:
            raise ValueError(f"Quantity must be non-negative, got {self.quantity}")
        self.is_available = self.quantity > 0


# ============================================================
# 3. FROZEN (IMMUTABLE) DATACLASSES
# ============================================================
@dataclass(frozen=True)
class Color:
    """An immutable RGB color.
    
    Frozen dataclasses are hashable and can be used as dict keys
    or in sets.
    """
    r: int
    g: int
    b: int
    name: str = ""

    def __post_init__(self):
        for channel_name, value in [("r", self.r), ("g", self.g), ("b", self.b)]:
            if not 0 <= value <= 255:
                raise ValueError(f"{channel_name} must be 0-255, got {value}")

    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def blend(self, other: "Color", ratio: float = 0.5) -> "Color":
        """Blend two colors together."""
        r = int(self.r * (1 - ratio) + other.r * ratio)
        g = int(self.g * (1 - ratio) + other.g * ratio)
        b = int(self.b * (1 - ratio) + other.b * ratio)
        return Color(r, g, b, name=f"{self.name}+{other.name}")


# ============================================================
# 4. NESTED DATACLASSES
# ============================================================
@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "US"

    def format(self) -> str:
        return f"{self.street}\n{self.city}, {self.state} {self.zip_code}\n{self.country}"


@dataclass
class Employee:
    name: str
    employee_id: int
    department: str
    salary: float
    address: Address
    skills: list[str] = field(default_factory=list)
    # Computed field
    annual_salary: float = field(init=False)

    def __post_init__(self):
        self.annual_salary = self.salary * 12

    def to_dict(self) -> dict:
        """Convert to dictionary (including nested dataclasses)."""
        return asdict(self)

    def to_json(self) -> str:
        """Serialize to JSON string."""
        d = asdict(self)
        # datetime objects need special handling
        return json.dumps(d, indent=2, default=str)


# ============================================================
# 5. INHERITANCE
# ============================================================
@dataclass
class Shape:
    """Base shape class."""
    color: str = "black"
    filled: bool = True

    def area(self) -> float:
        raise NotImplementedError


@dataclass
class Rectangle(Shape):
    """Rectangle inherits from Shape."""
    width: float = 0.0
    height: float = 0.0

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


@dataclass
class Circle(Shape):
    """Circle inherits from Shape."""
    radius: float = 0.0

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def circumference(self) -> float:
        return 2 * 3.14159 * self.radius


# ============================================================
# 6. DATACLASS WITH SLOTS (Python 3.10+)
# ============================================================
@dataclass(slots=True)
class Vector3D:
    """Memory-efficient 3D vector using __slots__.
    
    Slots prevent __dict__ creation, saving memory for
    classes with many instances.
    """
    x: float
    y: float
    z: float

    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def dot(self, other: "Vector3D") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def __add__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar: float) -> "Vector3D":
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)


# ============================================================
# 7. DATACLASS UTILITIES
# ============================================================
def demonstrate_utilities():
    """Show asdict, astuple, replace, and fields utilities."""
    
    p1 = Point(3.0, 4.0, "A")
    
    # asdict: convert to dictionary
    print(f"asdict:  {asdict(p1)}")
    
    # astuple: convert to tuple
    print(f"astuple: {astuple(p1)}")
    
    # replace: create modified copy (like dataclass copy)
    p2 = replace(p1, x=6.0, label="B")
    print(f"replace: {p1} -> {p2}")
    
    # fields: inspect field metadata
    print(f"\nFields of Product:")
    for f in fields(Product):
        print(f"  {f.name}: {f.type}, default={f.default}, repr={f.repr}")


# ============================================================
# 8. ORDERED DATACLASS
# ============================================================
@dataclass(order=True)
class StudentGrade:
    """Dataclass with automatic comparison methods for sorting.
    
    order=True generates __lt__, __le__, __gt__, __ge__
    based on field order.
    """
    grade: float  # Primary sort key (first field)
    name: str = field(compare=True)
    student_id: int = field(compare=False)  # Exclude from comparison


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Basic Dataclass")
    p1 = Point(3.0, 4.0, "A")
    p2 = Point(0.0, 0.0, "B")
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"Distance: {p1.distance_to(p2):.2f}")
    print(f"Equality: {Point(1, 2) == Point(1, 2)}")

    separator("2. Field Options & Post-Init")
    widget = Product("Widget", 29.99, 100, tags=["sale", "new"])
    print(f"Product: {widget}")
    print(f"Available: {widget.is_available}")
    
    out_of_stock = Product("Gadget", 49.99, 0)
    print(f"Out of stock: {out_of_stock.is_available}")
    
    try:
        Product("Bad", -10.0)
    except ValueError as e:
        print(f"Validation: {e}")

    separator("3. Frozen (Immutable)")
    red = Color(255, 0, 0, "red")
    blue = Color(0, 0, 255, "blue")
    print(f"Red hex:  {red.to_hex()}")
    print(f"Blue hex: {blue.to_hex()}")
    purple = red.blend(blue)
    print(f"Blended:  {purple} -> {purple.to_hex()}")
    
    # Frozen dataclasses are hashable
    color_set = {red, blue, Color(255, 0, 0, "red")}
    print(f"Color set size: {len(color_set)} (red is deduplicated)")
    
    try:
        red.r = 100
    except AttributeError:
        print("Cannot modify frozen dataclass (as expected)")

    separator("4. Nested Dataclasses")
    addr = Address("123 Main St", "Springfield", "IL", "62701")
    emp = Employee("Alice", 1001, "Engineering", 8500.0, addr,
                   skills=["Python", "SQL"])
    print(f"Employee JSON:\n{emp.to_json()}")

    separator("5. Inheritance")
    rect = Rectangle(color="blue", width=5.0, height=3.0)
    circle = Circle(color="red", radius=4.0)
    print(f"Rectangle: {rect}, area={rect.area():.1f}")
    print(f"Circle:    {circle}, area={circle.area():.1f}")

    separator("6. Slots (Memory Efficient)")
    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(4, 5, 6)
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 * 2  = {v1 * 2}")
    print(f"Dot product:  {v1.dot(v2)}")
    print(f"Cross product: {v1.cross(v2)}")
    print(f"Has __dict__?  {hasattr(v1, '__dict__')}")  # False with slots

    separator("7. Dataclass Utilities")
    demonstrate_utilities()

    separator("8. Ordered Dataclass")
    students = [
        StudentGrade(92.5, "Alice", 101),
        StudentGrade(85.0, "Bob", 102),
        StudentGrade(95.0, "Charlie", 103),
        StudentGrade(85.0, "Diana", 104),
    ]
    ranked = sorted(students)
    print("Students ranked by grade:")
    for s in ranked:
        print(f"  {s.grade:5.1f} - {s.name}")


if __name__ == "__main__":
    main()
