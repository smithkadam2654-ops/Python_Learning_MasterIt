class DatabaseConnection:
    """A simple Singleton class to manage a database connection."""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Override __new__ to control object creation."""
        if cls._instance is None:
            print("Creating new DatabaseConnection instance...")
            # If no instance exists, create one and store it
            cls._instance = super().__new__(cls)
            # Initialize any state only once
            cls._instance.connection_string = "jdbc:mysql://localhost:3306/mydb"
            cls._instance.is_connected = False
        return cls._instance
        
    def connect(self):
        if not self.is_connected:
            print(f"Connecting to {self.connection_string}...")
            self.is_connected = True
        else:
            print("Already connected.")

def demonstrate_singleton():
    """Demonstrate that all instances of the Singleton are the same object."""
    print("--- Initializing DB1 ---")
    db1 = DatabaseConnection()
    db1.connect()
    
    print("\n--- Initializing DB2 ---")
    db2 = DatabaseConnection()
    db2.connect()
    
    print("\n--- Checking Identity ---")
    print(f"Are db1 and db2 the exact same object? {db1 is db2}")
    
    # Modifying state in one variable affects the other since they are the same object
    db1.connection_string = "jdbc:postgresql://remotehost:5432/otherdb"
    print(f"db2's connection string changed too: {db2.connection_string}")

if __name__ == "__main__":
    demonstrate_singleton()
