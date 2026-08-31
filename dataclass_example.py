from dataclasses import dataclass
from typing import List

# @dataclass automatically generates the __init__, __repr__, and __eq__ methods for us!
# We also use Type Hinting (str, float, int) to declare what type of data is expected.
@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0 # Default value of 0
    
    # We can still add our own custom methods
    def total_value(self) -> float:
        """Returns the total value of this product in inventory."""
        return self.price * self.quantity

def dataclass_demo():
    print("--- Dataclass Demonstration ---")
    
    # Creating instances is clean and simple
    laptop = Product(name="Gaming Laptop", price=1299.99, quantity=5)
    mouse = Product(name="Wireless Mouse", price=25.50, quantity=50)
    keyboard = Product(name="Mechanical Keyboard", price=105.00) # Uses default quantity 0
    
    # Because of the automatically generated __repr__ method, printing the object looks great!
    print(laptop)
    print(mouse)
    print(keyboard)
    
    print("\n--- Method calls ---")
    print(f"Total value of laptops in stock: ${laptop.total_value():.2f}")
    
    print("\n--- Equality check ---")
    # Dataclasses also generate __eq__, so we can easily compare objects based on their data
    mouse1 = Product("Mouse", 10.0, 1)
    mouse2 = Product("Mouse", 10.0, 1)
    
    # This evaluates to True because their data is identical.
    # Normal classes would evaluate to False because they are different objects in memory.
    print(f"Are mouse1 and mouse2 identical? {mouse1 == mouse2}")

if __name__ == "__main__":
    dataclass_demo()
