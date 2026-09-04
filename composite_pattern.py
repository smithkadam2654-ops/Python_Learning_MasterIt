"""
Composite Pattern - Composite pattern for tree structures.
Features: Tree composition, uniform treatment, and recursive operations.
"""

from typing import List, Optional
from abc import ABC, abstractmethod


class Component(ABC):
    """Base component for composite pattern."""
    
    @abstractmethod
    def operation(self) -> str:
        """Perform operation."""
        pass
    
    @abstractmethod
    def add(self, component: 'Component') -> None:
        """Add child component."""
        pass
    
    @abstractmethod
    def remove(self, component: 'Component') -> None:
        """Remove child component."""
        pass
    
    @abstractmethod
    def get_child(self, index: int) -> Optional['Component']:
        """Get child component."""
        pass


class Leaf(Component):
    """Leaf component (no children)."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize leaf.
        
        Args:
            name: Leaf name
        """
        self.name = name
    
    def operation(self) -> str:
        """Perform operation."""
        return f"Leaf: {self.name}"
    
    def add(self, component: Component) -> None:
        """Cannot add to leaf."""
        raise NotImplementedError("Cannot add to leaf")
    
    def remove(self, component: Component) -> None:
        """Cannot remove from leaf."""
        raise NotImplementedError("Cannot remove from leaf")
    
    def get_child(self, index: int) -> Optional[Component]:
        """Leaf has no children."""
        return None


class Composite(Component):
    """Composite component (can have children)."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize composite.
        
        Args:
            name: Composite name
        """
        self.name = name
        self._children: List[Component] = []
    
    def operation(self) -> str:
        """Perform operation on self and children."""
        results = [f"Composite: {self.name}"]
        for child in self._children:
            results.append(f"  {child.operation()}")
        return "\n".join(results)
    
    def add(self, component: Component) -> None:
        """Add child component."""
        self._children.append(component)
    
    def remove(self, component: Component) -> None:
        """Remove child component."""
        if component in self._children:
            self._children.remove(component)
    
    def get_child(self, index: int) -> Optional[Component]:
        """Get child by index."""
        if 0 <= index < len(self._children):
            return self._children[index]
        return None


class FileSystemItem(ABC):
    """Base file system item."""
    
    @abstractmethod
    def get_size(self) -> int:
        """Get size in bytes."""
        pass
    
    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Display item with indentation."""
        pass


class File(FileSystemItem):
    """File in file system."""
    
    def __init__(self, name: str, size: int) -> None:
        """
        Initialize file.
        
        Args:
            name: File name
            size: File size in bytes
        """
        self.name = name
        self.size = size
    
    def get_size(self) -> int:
        """Get file size."""
        return self.size
    
    def display(self, indent: int = 0) -> str:
        """Display file."""
        return "  " * indent + f"📄 {self.name} ({self.size} bytes)"


class Directory(FileSystemItem):
    """Directory in file system."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize directory.
        
        Args:
            name: Directory name
        """
        self.name = name
        self._items: List[FileSystemItem] = []
    
    def add_item(self, item: FileSystemItem) -> None:
        """Add item to directory."""
        self._items.append(item)
    
    def remove_item(self, item: FileSystemItem) -> None:
        """Remove item from directory."""
        if item in self._items:
            self._items.remove(item)
    
    def get_size(self) -> int:
        """Get total size including subdirectories."""
        total = 0
        for item in self._items:
            total += item.get_size()
        return total
    
    def display(self, indent: int = 0) -> str:
        """Display directory and contents."""
        lines = ["  " * indent + f"📁 {self.name}/"]
        for item in self._items:
            lines.append(item.display(indent + 1))
        return "\n".join(lines)


class Employee(ABC):
    """Base employee class."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Get employee name."""
        pass
    
    @abstractmethod
    def get_salary(self) -> float:
        """Get employee salary."""
        pass
    
    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Display employee info."""
        pass


class IndividualEmployee(Employee):
    """Individual employee."""
    
    def __init__(self, name: str, salary: float) -> None:
        """
        Initialize individual employee.
        
        Args:
            name: Employee name
            salary: Employee salary
        """
        self.name = name
        self.salary = salary
    
    def get_name(self) -> str:
        """Get name."""
        return self.name
    
    def get_salary(self) -> float:
        """Get salary."""
        return self.salary
    
    def display(self, indent: int = 0) -> str:
        """Display employee."""
        return "  " * indent + f"👤 {self.name} (${self.salary:.2f})"


class Manager(Employee):
    """Manager with subordinates."""
    
    def __init__(self, name: str, salary: float) -> None:
        """
        Initialize manager.
        
        Args:
            name: Manager name
            salary: Manager salary
        """
        self.name = name
        self.salary = salary
        self._subordinates: List[Employee] = []
    
    def add_subordinate(self, employee: Employee) -> None:
        """Add subordinate."""
        self._subordinates.append(employee)
    
    def remove_subordinate(self, employee: Employee) -> None:
        """Remove subordinate."""
        if employee in self._subordinates:
            self._subordinates.remove(employee)
    
    def get_name(self) -> str:
        """Get name."""
        return self.name
    
    def get_salary(self) -> float:
        """Get salary."""
        return self.salary
    
    def get_total_salary(self) -> float:
        """Get total salary including subordinates."""
        total = self.salary
        for subordinate in self._subordinates:
            total += subordinate.get_salary()
        return total
    
    def display(self, indent: int = 0) -> str:
        """Display manager and subordinates."""
        lines = ["  " * indent + f"👔 {self.name} (${self.salary:.2f})"]
        for subordinate in self._subordinates:
            lines.append(subordinate.display(indent + 1))
        return "\n".join(lines)


class Graphic(ABC):
    """Base graphic element."""
    
    @abstractmethod
    def draw(self) -> str:
        """Draw the graphic."""
        pass
    
    @abstractmethod
    def add(self, graphic: 'Graphic') -> None:
        """Add child graphic."""
        pass
    
    @abstractmethod
    def remove(self, graphic: 'Graphic') -> None:
        """Remove child graphic."""
        pass


class Circle(Graphic):
    """Circle graphic."""
    
    def __init__(self, x: float, y: float, radius: float) -> None:
        """
        Initialize circle.
        
        Args:
            x: X coordinate
            y: Y coordinate
            radius: Circle radius
        """
        self.x = x
        self.y = y
        self.radius = radius
    
    def draw(self) -> str:
        """Draw circle."""
        return f"Circle at ({self.x}, {self.y}) with radius {self.radius}"
    
    def add(self, graphic: Graphic) -> None:
        """Cannot add to circle."""
        raise NotImplementedError("Cannot add to circle")
    
    def remove(self, graphic: Graphic) -> None:
        """Cannot remove from circle."""
        raise NotImplementedError("Cannot remove from circle")


class Rectangle(Graphic):
    """Rectangle graphic."""
    
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        """
        Initialize rectangle.
        
        Args:
            x: X coordinate
            y: Y coordinate
            width: Rectangle width
            height: Rectangle height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self) -> str:
        """Draw rectangle."""
        return f"Rectangle at ({self.x}, {self.y}) with size {self.width}x{self.height}"
    
    def add(self, graphic: Graphic) -> None:
        """Cannot add to rectangle."""
        raise NotImplementedError("Cannot add to rectangle")
    
    def remove(self, graphic: Graphic) -> None:
        """Cannot remove from rectangle."""
        raise NotImplementedError("Cannot remove from rectangle")


class Picture(Graphic):
    """Composite picture containing graphics."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize picture.
        
        Args:
            name: Picture name
        """
        self.name = name
        self._graphics: List[Graphic] = []
    
    def add(self, graphic: Graphic) -> None:
        """Add graphic to picture."""
        self._graphics.append(graphic)
    
    def remove(self, graphic: Graphic) -> None:
        """Remove graphic from picture."""
        if graphic in self._graphics:
            self._graphics.remove(graphic)
    
    def draw(self) -> str:
        """Draw all graphics in picture."""
        lines = [f"Picture '{self.name}':"]
        for graphic in self._graphics:
            lines.append(f"  {graphic.draw()}")
        return "\n".join(lines)


def main() -> None:
    """Demonstrate composite pattern."""
    
    print("=== Basic Composite ===")
    
    # Create composite structure
    root = Composite("Root")
    branch1 = Composite("Branch 1")
    branch2 = Composite("Branch 2")
    
    leaf1 = Leaf("Leaf 1")
    leaf2 = Leaf("Leaf 2")
    leaf3 = Leaf("Leaf 3")
    
    # Build tree
    root.add(branch1)
    root.add(branch2)
    
    branch1.add(leaf1)
    branch1.add(leaf2)
    branch2.add(leaf3)
    
    print(root.operation())
    
    print("\n=== File System ===")
    
    # Create file system structure
    root_dir = Directory("root")
    
    docs = Directory("documents")
    docs.add_item(File("readme.txt", 1024))
    docs.add_item(File("notes.txt", 2048))
    
    images = Directory("images")
    images.add_item(File("photo1.jpg", 51200))
    images.add_item(File("photo2.jpg", 76800))
    
    root_dir.add_item(docs)
    root_dir.add_item(images)
    root_dir.add_item(File("config.ini", 512))
    
    print(root_dir.display())
    print(f"\nTotal size: {root_dir.get_size()} bytes ({root_dir.get_size() / 1024:.2f} KB)")
    
    print("\n=== Organization Hierarchy ===")
    
    # Create organization structure
    ceo = Manager("Alice CEO", 200000)
    
    cto = Manager("Bob CTO", 150000)
    cfo = Manager("Charlie CFO", 150000)
    
    dev_lead = Manager("Dave Dev Lead", 120000)
    dev1 = IndividualEmployee("Eve Dev", 90000)
    dev2 = IndividualEmployee("Frank Dev", 85000)
    
    accountant = IndividualEmployee("Grace Accountant", 70000)
    
    # Build hierarchy
    ceo.add_subordinate(cto)
    ceo.add_subordinate(cfo)
    
    cto.add_subordinate(dev_lead)
    dev_lead.add_subordinate(dev1)
    dev_lead.add_subordinate(dev2)
    
    cfo.add_subordinate(accountant)
    
    print(ceo.display())
    print(f"\nTotal salary budget: ${ceo.get_total_salary():.2f}")
    
    print("\n=== Graphics Composition ===")
    
    # Create picture with shapes
    picture = Picture("My Drawing")
    
    picture.add(Circle(10, 10, 5))
    picture.add(Rectangle(20, 20, 15, 10))
    picture.add(Circle(50, 50, 8))
    
    print(picture.draw())
    
    print("\n=== Composite Benefits ===")
    print("1. Treat individual objects and compositions uniformly")
    print("2. Simplifies client code - no need to distinguish between leaf and composite")
    print("3. Easy to add new types of components")
    print("4. Enables tree structures naturally")


if __name__ == "__main__":
    main()
