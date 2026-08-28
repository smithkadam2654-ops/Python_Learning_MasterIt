class UppercaseAttributeMetaclass(type):
    """A metaclass that automatically converts all class attribute names to uppercase."""
    
    def __new__(mcs, name, bases, namespace):
        uppercase_namespace = {}
        for attr_name, attr_value in namespace.items():
            # Don't modify magic methods (like __init__)
            if attr_name.startswith('__') and attr_name.endswith('__'):
                uppercase_namespace[attr_name] = attr_value
            else:
                # Convert the attribute name to uppercase
                uppercase_namespace[attr_name.upper()] = attr_value
                
        # Call the default type.__new__ to actually create the class
        return super().__new__(mcs, name, bases, uppercase_namespace)

class Configuration(metaclass=UppercaseAttributeMetaclass):
    """A class using the custom metaclass."""
    
    # We define these in lowercase
    host = "localhost"
    port = 8080
    debug_mode = True

def demonstrate_metaclasses():
    print("--- Metaclass Demonstration ---")
    print("We defined 'host', 'port', and 'debug_mode' in lowercase.")
    
    # But thanks to the metaclass, they are now uppercase!
    print(f"HOST: {Configuration.HOST}")
    print(f"PORT: {Configuration.PORT}")
    print(f"DEBUG_MODE: {Configuration.DEBUG_MODE}")
    
    # Trying to access the lowercase versions will raise an AttributeError
    try:
        print(Configuration.host)
    except AttributeError as e:
        print(f"\nCaught Expected Error: {e}")

if __name__ == "__main__":
    demonstrate_metaclasses()
