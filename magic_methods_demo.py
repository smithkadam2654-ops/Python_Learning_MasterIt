class Vector:
    """Demonstrate magic methods (dunder methods) for operator overloading."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        """Called by str() and print() to return a user-friendly string."""
        return f"Vector({self.x}, {self.y})"
        
    def __repr__(self):
        """Called by repr() to return a developer-friendly string (fallback for print)."""
        return f"Vector(x={self.x}, y={self.y})"
        
    def __add__(self, other):
        """Overload the '+' operator."""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        raise TypeError("Can only add two Vectors together.")
        
    def __eq__(self, other):
        """Overload the '==' operator."""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False
        
    def __len__(self):
        """Overload the len() function (returning a simplistic mock length here)."""
        # In reality, a vector's length would be its magnitude, but len() requires an integer.
        # We'll just return 2 since it has 2 dimensions.
        return 2

def demonstrate_magic_methods():
    v1 = Vector(2, 4)
    v2 = Vector(3, -1)
    
    # Demonstrating __str__
    print(f"v1: {v1}")
    print(f"v2: {v2}")
    
    # Demonstrating __add__
    v3 = v1 + v2
    print(f"\nv1 + v2 = {v3}")
    
    # Demonstrating __eq__
    v4 = Vector(2, 4)
    print(f"\nIs v1 equal to v2? {v1 == v2}")
    print(f"Is v1 equal to v4? {v1 == v4}")
    
    # Demonstrating __len__
    print(f"\nDimensions of v1 (using len): {len(v1)}")

if __name__ == "__main__":
    demonstrate_magic_methods()
