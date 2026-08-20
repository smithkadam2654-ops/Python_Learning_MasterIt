from dataclasses import dataclass
from typing import List

# Using @dataclass automatically generates __init__, __repr__, and __eq__ methods
@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0  # Default value
    
    def total_value(self) -> float:
        """Calculate the total value of this product inventory."""
        return self.price * self.quantity

@dataclass
class ShoppingCart:
    items: List[Product]
    
    def calculate_total(self) -> float:
        return sum(item.total_value() for item in self.items)

if __name__ == "__main__":
    # Create some products
    apple = Product("Apple", 0.99, 5)
    laptop = Product("Laptop", 1200.00, 1)
    water = Product(name="Bottled Water", price=1.50) # Uses default quantity 0
    
    # Note the automatically generated __repr__
    print(f"Product info: {apple}")
    
    # Create a shopping cart
    cart = ShoppingCart(items=[apple, laptop])
    print(f"Total cart value: ${cart.calculate_total():.2f}")
