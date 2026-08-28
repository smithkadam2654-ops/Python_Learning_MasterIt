class ValidatedString:
    """A descriptor that ensures a string attribute is not empty and is properly capitalized."""
    
    def __init__(self, name=None):
        self.name = name
        
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, "")
        
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"Expected a string for {self.name}, got {type(value).__name__}")
        if not value.strip():
            raise ValueError(f"{self.name} cannot be empty")
            
        # Capitalize the first letter and store it in the instance's dictionary
        instance.__dict__[self.name] = value.strip().capitalize()
        
    def __delete__(self, instance):
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

class Person:
    """A class using our custom descriptor."""
    # We create the descriptors at the class level
    first_name = ValidatedString("first_name")
    last_name = ValidatedString("last_name")
    
    def __init__(self, first, last):
        # When we assign here, it calls the descriptor's __set__ method!
        self.first_name = first
        self.last_name = last
        
    def __repr__(self):
        return f"Person(first_name='{self.first_name}', last_name='{self.last_name}')"

def demonstrate_descriptors():
    print("--- Using Descriptors ---")
    
    # 1. Valid Assignment
    print("Creating a person with messy casing...")
    p1 = Person("  john  ", "DOE")
    print(p1) # Output should be nicely capitalized!
    
    # 2. Type Checking
    print("\nAttempting to assign a number to a string field...")
    try:
        p1.first_name = 123
    except TypeError as e:
        print(f"Caught Error: {e}")
        
    # 3. Value Validation
    print("\nAttempting to assign an empty string...")
    try:
        p2 = Person("", "Smith")
    except ValueError as e:
        print(f"Caught Error: {e}")

if __name__ == "__main__":
    demonstrate_descriptors()
