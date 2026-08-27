from dataclasses import dataclass, field
from typing import List

# Using @dataclass automatically generates __init__, __repr__, and __eq__ methods!
@dataclass
class Product:
    name: str
    price: float
    in_stock: bool = True
    tags: List[str] = field(default_factory=list)

    def apply_discount(self, percentage: float):
        """Method to apply a discount to the product price."""
        discount_amount = self.price * (percentage / 100)
        self.price -= discount_amount

def demonstrate_dataclasses():
    """Demonstrate the benefits of using dataclasses."""
    
    # Create an instance easily
    laptop = Product(name="Gaming Laptop", price=1200.00, tags=["electronics", "gaming"])
    mouse = Product(name="Wireless Mouse", price=25.50)
    
    # __repr__ is automatically clean and readable
    print("Initial Products:")
    print(laptop)
    print(mouse)
    
    # Apply a discount
    laptop.apply_discount(10)
    print(f"\nLaptop price after 10% discount: ${laptop.price:.2f}")

if __name__ == "__main__":
    demonstrate_dataclasses()
