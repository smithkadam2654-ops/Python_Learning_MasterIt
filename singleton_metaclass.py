class SingletonMeta(type):
    """
    A metaclass for implementing the Singleton design pattern.
    Any class using this metaclass will only ever have one instance.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        __call__ is invoked when the class is instantiated.
        We intercept it to return the existing instance if it exists.
        """
        if cls not in cls._instances:
            print(f"Creating new instance of {cls.__name__}")
            # Call the superclass to actually create the object
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        else:
            print(f"Returning existing instance of {cls.__name__}")
            
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    """A mock database connection class using the Singleton metaclass."""
    def __init__(self):
        print("Initializing Database Connection...")
        self.connected = True
        
    def query(self, sql: str) -> str:
        return f"Executing query: {sql}"

if __name__ == "__main__":
    # Attempt to create multiple instances
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    db3 = DatabaseConnection()
    
    print(f"\nAre db1 and db2 the exact same object? {db1 is db2}")
    print(f"Are db2 and db3 the exact same object? {db2 is db3}")
    
    print(db1.query("SELECT * FROM users"))
