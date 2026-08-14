class TypedProperty:
    """A descriptor that enforces type checking on an attribute."""
    def __init__(self, name: str, expected_type: type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Expected {self.name} to be {self.expected_type.__name__}, got {type(value).__name__}")
        instance.__dict__[self.name] = value

class RangeProperty:
    """A descriptor that enforces numeric boundaries."""
    def __init__(self, name: str, min_val: float, max_val: float):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"{self.name} must be between {self.min_val} and {self.max_val}")
        instance.__dict__[self.name] = value

class Person:
    # Use descriptors for attribute validation
    name = TypedProperty("name", str)
    age = RangeProperty("age", 0, 150)

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

if __name__ == "__main__":
    p = Person("Alice", 30)
    print(f"Created person: {p.name}, {p.age}")
    
    try:
        p.name = 123  # This will raise a TypeError
    except TypeError as e:
        print(f"Caught Type Error: {e}")
        
    try:
        p.age = -5    # This will raise a ValueError
    except ValueError as e:
        print(f"Caught Value Error: {e}")
