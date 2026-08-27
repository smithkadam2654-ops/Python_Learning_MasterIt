class Employee:
    """Demonstrate encapsulation using property decorators."""
    
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        
    @property
    def email(self):
        """Getter for email: dynamically created from first and last name."""
        return f"{self.first_name.lower()}.{self.last_name.lower()}@company.com"
        
    @property
    def fullname(self):
        """Getter for full name."""
        return f"{self.first_name} {self.last_name}"
        
    @fullname.setter
    def fullname(self, name):
        """Setter for full name: allows setting first and last name simultaneously."""
        first, last = name.split(' ')
        self.first_name = first
        self.last_name = last
        
    @fullname.deleter
    def fullname(self):
        """Deleter for full name: clears out the name fields."""
        print('Delete Name!')
        self.first_name = None
        self.last_name = None

def demonstrate_properties():
    emp = Employee('John', 'Doe')
    
    print(f"Initial Full Name: {emp.fullname}")
    print(f"Initial Email: {emp.email}")
    
    # Use the setter
    print("\nChanging full name to 'Jane Smith'...")
    emp.fullname = "Jane Smith"
    
    print(f"New First Name: {emp.first_name}")
    print(f"New Email (automatically updated): {emp.email}")
    
    # Use the deleter
    print("\nDeleting full name...")
    del emp.fullname
    print(f"First Name after deletion: {emp.first_name}")

if __name__ == "__main__":
    demonstrate_properties()
