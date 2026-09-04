"""
Visitor Pattern - Visitor pattern for separating algorithms from object structures.
Features: Operation separation, extensible operations, and double dispatch.
"""

from typing import List
from abc import ABC, abstractmethod


class Visitor(ABC):
    """Visitor interface."""
    
    @abstractmethod
    def visit_book(self, book: 'Book') -> None:
        """Visit book element."""
        pass
    
    @abstractmethod
    def visit_electronics(self, electronics: 'Electronics') -> None:
        """Visit electronics element."""
        pass
    
    @abstractmethod
    def visit_clothing(self, clothing: 'Clothing') -> None:
        """Visit clothing element."""
        pass


class Element(ABC):
    """Element interface."""
    
    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        """Accept visitor."""
        pass


class Book(Element):
    """Book element."""
    
    def __init__(self, title: str, price: float, weight: float) -> None:
        """
        Initialize book.
        
        Args:
            title: Book title
            price: Book price
            weight: Book weight in kg
        """
        self.title = title
        self.price = price
        self.weight = weight
    
    def accept(self, visitor: Visitor) -> None:
        """Accept visitor."""
        visitor.visit_book(self)
    
    def get_price(self) -> float:
        """Get price."""
        return self.price
    
    def get_weight(self) -> float:
        """Get weight."""
        return self.weight


class Electronics(Element):
    """Electronics element."""
    
    def __init__(self, name: str, price: float, power_consumption: float) -> None:
        """
        Initialize electronics.
        
        Args:
            name: Product name
            price: Product price
            power_consumption: Power consumption in watts
        """
        self.name = name
        self.price = price
        self.power_consumption = power_consumption
    
    def accept(self, visitor: Visitor) -> None:
        """Accept visitor."""
        visitor.visit_electronics(self)
    
    def get_price(self) -> float:
        """Get price."""
        return self.price
    
    def get_power_consumption(self) -> float:
        """Get power consumption."""
        return self.power_consumption


class Clothing(Element):
    """Clothing element."""
    
    def __init__(self, name: str, price: float, size: str) -> None:
        """
        Initialize clothing.
        
        Args:
            name: Clothing name
            price: Clothing price
            size: Clothing size
        """
        self.name = name
        self.price = price
        self.size = size
    
    def accept(self, visitor: Visitor) -> None:
        """Accept visitor."""
        visitor.visit_clothing(self)
    
    def get_price(self) -> float:
        """Get price."""
        return self.price
    
    def get_size(self) -> str:
        """Get size."""
        return self.size


class PriceVisitor(Visitor):
    """Visitor for calculating total price."""
    
    def __init__(self) -> None:
        """Initialize price visitor."""
        self.total_price = 0.0
    
    def visit_book(self, book: Book) -> None:
        """Visit book - add price."""
        self.total_price += book.get_price()
    
    def visit_electronics(self, electronics: Electronics) -> None:
        """Visit electronics - add price."""
        self.total_price += electronics.get_price()
    
    def visit_clothing(self, clothing: Clothing) -> None:
        """Visit clothing - add price."""
        self.total_price += clothing.get_price()
    
    def get_total(self) -> float:
        """Get total price."""
        return self.total_price
    
    def reset(self) -> None:
        """Reset total."""
        self.total_price = 0.0


class WeightVisitor(Visitor):
    """Visitor for calculating total weight."""
    
    def __init__(self) -> None:
        """Initialize weight visitor."""
        self.total_weight = 0.0
    
    def visit_book(self, book: Book) -> None:
        """Visit book - add weight."""
        self.total_weight += book.get_weight()
    
    def visit_electronics(self, electronics: Electronics) -> None:
        """Visit electronics - no weight."""
        pass
    
    def visit_clothing(self, clothing: Clothing) -> None:
        """Visit clothing - no weight."""
        pass
    
    def get_total(self) -> float:
        """Get total weight."""
        return self.total_weight
    
    def reset(self) -> None:
        """Reset total."""
        self.total_weight = 0.0


class XMLExportVisitor(Visitor):
    """Visitor for exporting to XML format."""
    
    def __init__(self) -> None:
        """Initialize XML visitor."""
        self.xml_elements: List[str] = []
    
    def visit_book(self, book: Book) -> None:
        """Visit book - create XML element."""
        xml = f'<book title="{book.title}" price="{book.price}" weight="{book.weight}"/>'
        self.xml_elements.append(xml)
    
    def visit_electronics(self, electronics: Electronics) -> None:
        """Visit electronics - create XML element."""
        xml = f'<electronics name="{electronics.name}" price="{electronics.price}" power="{electronics.power_consumption}"/>'
        self.xml_elements.append(xml)
    
    def visit_clothing(self, clothing: Clothing) -> None:
        """Visit clothing - create XML element."""
        xml = f'<clothing name="{clothing.name}" price="{clothing.price}" size="{clothing.size}"/>'
        self.xml_elements.append(xml)
    
    def get_xml(self) -> str:
        """Get XML output."""
        return "\n".join(self.xml_elements)
    
    def reset(self) -> None:
        """Reset XML elements."""
        self.xml_elements.clear()


class DiscountVisitor(Visitor):
    """Visitor for applying discounts."""
    
    def __init__(self, discount_percent: float) -> None:
        """
        Initialize discount visitor.
        
        Args:
            discount_percent: Discount percentage (0-100)
        """
        self.discount_percent = discount_percent
        self.discounted_items: List[str] = []
    
    def visit_book(self, book: Book) -> None:
        """Visit book - apply discount."""
        discounted_price = book.get_price() * (1 - self.discount_percent / 100)
        self.discounted_items.append(f"Book '{book.title}': ${book.get_price():.2f} -> ${discounted_price:.2f}")
    
    def visit_electronics(self, electronics: Electronics) -> None:
        """Visit electronics - apply discount."""
        discounted_price = electronics.get_price() * (1 - self.discount_percent / 100)
        self.discounted_items.append(f"Electronics '{electronics.name}': ${electronics.get_price():.2f} -> ${discounted_price:.2f}")
    
    def visit_clothing(self, clothing: Clothing) -> None:
        """Visit clothing - apply discount."""
        discounted_price = clothing.get_price() * (1 - self.discount_percent / 100)
        self.discounted_items.append(f"Clothing '{clothing.name}': ${clothing.get_price():.2f} -> ${discounted_price:.2f}")
    
    def get_discounted_items(self) -> List[str]:
        """Get discounted items."""
        return self.discounted_items
    
    def reset(self) -> None:
        """Reset discounted items."""
        self.discounted_items.clear()


class ShoppingCart:
    """Shopping cart containing elements."""
    
    def __init__(self) -> None:
        """Initialize shopping cart."""
        self.items: List[Element] = []
    
    def add_item(self, item: Element) -> None:
        """Add item to cart."""
        self.items.append(item)
    
    def remove_item(self, item: Element) -> None:
        """Remove item from cart."""
        if item in self.items:
            self.items.remove(item)
    
    def accept(self, visitor: Visitor) -> None:
        """Accept visitor for all items."""
        for item in self.items:
            item.accept(visitor)


# File system visitor example
class File(ABC):
    """File system element."""
    
    @abstractmethod
    def accept(self, visitor: 'FileSystemVisitor') -> None:
        """Accept visitor."""
        pass
    
    @abstractmethod
    def get_size(self) -> int:
        """Get size in bytes."""
        pass


class TextFile(File):
    """Text file."""
    
    def __init__(self, name: str, size: int) -> None:
        """Initialize text file."""
        self.name = name
        self._size = size
    
    def accept(self, visitor: 'FileSystemVisitor') -> None:
        """Accept visitor."""
        visitor.visit_text_file(self)
    
    def get_size(self) -> int:
        """Get size."""
        return self._size


class ImageFile(File):
    """Image file."""
    
    def __init__(self, name: str, size: int) -> None:
        """Initialize image file."""
        self.name = name
        self._size = size
    
    def accept(self, visitor: 'FileSystemVisitor') -> None:
        """Accept visitor."""
        visitor.visit_image_file(self)
    
    def get_size(self) -> int:
        """Get size."""
        return self._size


class Directory(File):
    """Directory containing files."""
    
    def __init__(self, name: str) -> None:
        """Initialize directory."""
        self.name = name
        self.children: List[File] = []
    
    def add_child(self, child: File) -> None:
        """Add child file/directory."""
        self.children.append(child)
    
    def accept(self, visitor: 'FileSystemVisitor') -> None:
        """Accept visitor."""
        visitor.visit_directory(self)
    
    def get_size(self) -> int:
        """Get total size."""
        return sum(child.get_size() for child in self.children)


class FileSystemVisitor(ABC):
    """File system visitor interface."""
    
    @abstractmethod
    def visit_text_file(self, file: TextFile) -> None:
        """Visit text file."""
        pass
    
    @abstractmethod
    def visit_image_file(self, file: ImageFile) -> None:
        """Visit image file."""
        pass
    
    @abstractmethod
    def visit_directory(self, directory: Directory) -> None:
        """Visit directory."""
        pass


class SizeCalculatorVisitor(FileSystemVisitor):
    """Visitor for calculating total size."""
    
    def __init__(self) -> None:
        """Initialize size calculator."""
        self.total_size = 0
    
    def visit_text_file(self, file: TextFile) -> None:
        """Visit text file - add size."""
        self.total_size += file.get_size()
    
    def visit_image_file(self, file: ImageFile) -> None:
        """Visit image file - add size."""
        self.total_size += file.get_size()
    
    def visit_directory(self, directory: Directory) -> None:
        """Visit directory - recursively visit children."""
        for child in directory.children:
            child.accept(self)
    
    def get_total_size(self) -> int:
        """Get total size."""
        return self.total_size


class FileListVisitor(FileSystemVisitor):
    """Visitor for listing files."""
    
    def __init__(self) -> None:
        """Initialize file list visitor."""
        self.files: List[str] = []
    
    def visit_text_file(self, file: TextFile) -> None:
        """Visit text file - add to list."""
        self.files.append(f"[TEXT] {file.name} ({file.get_size()} bytes)")
    
    def visit_image_file(self, file: ImageFile) -> None:
        """Visit image file - add to list."""
        self.files.append(f"[IMAGE] {file.name} ({file.get_size()} bytes)")
    
    def visit_directory(self, directory: Directory) -> None:
        """Visit directory - add to list and visit children."""
        self.files.append(f"[DIR] {directory.name}/")
        for child in directory.children:
            child.accept(self)
    
    def get_file_list(self) -> List[str]:
        """Get file list."""
        return self.files


def main() -> None:
    """Demonstrate visitor pattern."""
    
    print("=== Shopping Cart Visitors ===")
    
    cart = ShoppingCart()
    
    # Add items
    cart.add_item(Book("Python Programming", 49.99, 0.5))
    cart.add_item(Book("Design Patterns", 59.99, 0.7))
    cart.add_item(Electronics("Laptop", 999.99, 65.0))
    cart.add_item(Electronics("Mouse", 29.99, 0.5))
    cart.add_item(Clothing("T-Shirt", 19.99, "M"))
    cart.add_item(Clothing("Jeans", 49.99, "32"))
    
    # Calculate total price
    price_visitor = PriceVisitor()
    cart.accept(price_visitor)
    print(f"Total price: ${price_visitor.get_total():.2f}")
    
    # Calculate total weight
    weight_visitor = WeightVisitor()
    cart.accept(weight_visitor)
    print(f"Total weight: {weight_visitor.get_total():.2f} kg")
    
    # Export to XML
    xml_visitor = XMLExportVisitor()
    cart.accept(xml_visitor)
    print("\nXML Export:")
    print("<items>")
    for xml in xml_visitor.get_xml().split("\n"):
        print(f"  {xml}")
    print("</items>")
    
    # Apply discount
    discount_visitor = DiscountVisitor(10)  # 10% discount
    cart.accept(discount_visitor)
    print("\nDiscounted Prices (10% off):")
    for item in discount_visitor.get_discounted_items():
        print(f"  {item}")
    
    print("\n=== File System Visitors ===")
    
    # Create file system structure
    root = Directory("root")
    docs = Directory("documents")
    images = Directory("images")
    
    docs.add_child(TextFile("readme.txt", 1024))
    docs.add_child(TextFile("notes.txt", 2048))
    
    images.add_child(ImageFile("photo1.jpg", 51200))
    images.add_child(ImageFile("photo2.jpg", 76800))
    
    root.add_child(docs)
    root.add_child(images)
    root.add_child(TextFile("config.ini", 512))
    
    # Calculate total size
    size_visitor = SizeCalculatorVisitor()
    root.accept(size_visitor)
    print(f"Total size: {size_visitor.get_total_size()} bytes ({size_visitor.get_total_size() / 1024:.2f} KB)")
    
    # List files
    list_visitor = FileListVisitor()
    root.accept(list_visitor)
    print("\nFile listing:")
    for file in list_visitor.get_file_list():
        print(f"  {file}")
    
    print("\n=== Visitor Benefits ===")
    print("1. Separates operations from object structure")
    print("2. Easy to add new operations without modifying elements")
    print("3. Related operations grouped in visitor")
    print("4. Can maintain state across element visits")


if __name__ == "__main__":
    main()
