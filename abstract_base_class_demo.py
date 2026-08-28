from abc import ABC, abstractmethod
import math

class Shape(ABC):
    """An abstract base class representing a generic shape."""
    
    @abstractmethod
    def area(self):
        """Calculate the area of the shape. Must be implemented by subclasses."""
        pass
        
    @abstractmethod
    def perimeter(self):
        """Calculate the perimeter of the shape. Must be implemented by subclasses."""
        pass
        
    def describe(self):
        """A concrete method that can be used by all subclasses."""
        return f"This is a {self.__class__.__name__} with area {self.area():.2f}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
        
    def area(self):
        return math.pi * (self.radius ** 2)
        
    def perimeter(self):
        return 2 * math.pi * self.radius

class Square(Shape):
    def __init__(self, side):
        self.side = side
        
    def area(self):
        return self.side ** 2
        
    def perimeter(self):
        return 4 * self.side

def demonstrate_abc():
    print("--- Abstract Base Classes ---")
    
    # 1. You cannot instantiate an abstract class directly!
    try:
        generic_shape = Shape()
    except TypeError as e:
        print(f"Error instantiating Shape: {e}\n")
        
    # 2. Instantiating valid subclasses
    c = Circle(5)
    s = Square(4)
    
    print(c.describe())
    print(f"Circle Perimeter: {c.perimeter():.2f}\n")
    
    print(s.describe())
    print(f"Square Perimeter: {s.perimeter():.2f}")

if __name__ == "__main__":
    demonstrate_abc()
