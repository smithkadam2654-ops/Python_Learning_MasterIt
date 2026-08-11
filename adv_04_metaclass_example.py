"""
Advanced Python - Lesson 04: Metaclasses
==========================================
Metaclasses are "classes of classes" — they define how classes behave.
Just as an object is an instance of a class, a class is an instance of a metaclass.

Topics Covered:
- Understanding type() as the default metaclass
- Creating custom metaclasses
- Class validation and auto-registration
- Singleton pattern via metaclass
- Auto-attribute injection
- Practical use cases

WARNING: Metaclasses are powerful but complex. Use them only when
simpler solutions (decorators, __init_subclass__) won't work.
"""


# ============================================================
# 1. UNDERSTANDING THE TYPE HIERARCHY
# ============================================================
def demonstrate_type_hierarchy():
    """Everything in Python is an object, and every object has a type."""
    
    class MyClass:
        pass

    obj = MyClass()

    print("Object hierarchy:")
    print(f"  type(obj)     = {type(obj)}")        # MyClass
    print(f"  type(MyClass) = {type(MyClass)}")     # type (the metaclass)
    print(f"  type(type)    = {type(type)}")         # type (type is its own metaclass)
    print(f"  type(int)     = {type(int)}")           # type
    print(f"  type(str)     = {type(str)}")           # type

    print("\nInheritance chain:")
    print(f"  isinstance(obj, MyClass)   = {isinstance(obj, MyClass)}")
    print(f"  isinstance(MyClass, type)   = {isinstance(MyClass, type)}")
    print(f"  issubclass(MyClass, object) = {issubclass(MyClass, object)}")


# ============================================================
# 2. BASIC CUSTOM METACLASS
# ============================================================
class VerboseMeta(type):
    """A metaclass that prints information when a class is created."""

    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        print(f"\n[Meta] Creating class: {name}")
        print(f"  Bases: {bases}")
        print(f"  Attributes: {[k for k in namespace if not k.startswith('_')]}")

        # Add a class attribute automatically
        namespace["created_by"] = "VerboseMeta"

        cls = super().__new__(mcs, name, bases, namespace)
        return cls

    def __init__(cls, name: str, bases: tuple, namespace: dict):
        super().__init__(name, bases, namespace)
        print(f"  [Meta] Class '{name}' initialized successfully")


class Animal(metaclass=VerboseMeta):
    """A class created with VerboseMeta."""
    species = "unknown"

    def speak(self) -> str:
        return "..."


class Dog(Animal):
    """Dog inherits from Animal and is also affected by VerboseMeta."""
    species = "Canis familiaris"

    def speak(self) -> str:
        return "Woof!"


# ============================================================
# 3. VALIDATION METACLASS
# ============================================================
class ValidationMeta(type):
    """Metaclass that validates class definitions.
    
    Ensures that:
    - Every class has a docstring
    - Every public method has a type-annotated return value
    - Class names use CamelCase
    """

    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        # Skip validation for base classes
        if not bases:
            return super().__new__(mcs, name, bases, namespace)

        # Validate CamelCase naming
        if not name[0].isupper():
            raise TypeError(
                f"Class name '{name}' must use CamelCase (start with uppercase)"
            )

        # Validate docstring
        if "__doc__" not in namespace or not namespace["__doc__"]:
            raise TypeError(f"Class '{name}' must have a docstring")

        # Validate method return annotations
        for attr_name, attr_value in namespace.items():
            if attr_name.startswith("_"):
                continue
            if callable(attr_value) and hasattr(attr_value, "__annotations__"):
                if "return" not in attr_value.__annotations__:
                    print(f"  Warning: '{name}.{attr_name}' has no return type annotation")

        return super().__new__(mcs, name, bases, namespace)


class ValidatedService(metaclass=ValidationMeta):
    """A service class that passes all validation checks."""

    def process(self, data: str) -> str:
        return f"Processed: {data}"

    def save(self, record: dict) -> bool:
        return True


# ============================================================
# 4. SINGLETON METACLASS
# ============================================================
class SingletonMeta(type):
    """Metaclass that ensures only one instance of a class exists.
    
    Every call to ClassName() returns the same instance.
    """
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
            print(f"  [Singleton] Created instance of '{cls.__name__}'")
        else:
            print(f"  [Singleton] Reusing existing instance of '{cls.__name__}'")
        return cls._instances[cls]


class AppConfig(metaclass=SingletonMeta):
    """Application configuration singleton."""

    def __init__(self):
        self.settings: dict = {
            "debug": False,
            "log_level": "INFO",
            "max_connections": 10,
        }

    def get(self, key: str) -> any:
        return self.settings.get(key)

    def set(self, key: str, value: any):
        self.settings[key] = value


class DatabasePool(metaclass=SingletonMeta):
    """Database connection pool singleton."""

    def __init__(self):
        self.connections: list = []
        self.max_size: int = 5

    def add_connection(self, conn_str: str):
        if len(self.connections) < self.max_size:
            self.connections.append(conn_str)


# ============================================================
# 5. AUTO-REGISTRATION METACLASS
# ============================================================
class PluginRegistry:
    """Registry that stores all registered plugins."""
    _plugins: dict[str, type] = {}

    @classmethod
    def register(cls, plugin_class: type):
        name = plugin_class.__name__
        cls._plugins[name] = plugin_class
        print(f"  [Registry] Registered plugin: {name}")

    @classmethod
    def get_plugin(cls, name: str) -> type:
        if name not in cls._plugins:
            raise KeyError(f"Plugin '{name}' not found")
        return cls._plugins[name]

    @classmethod
    def list_plugins(cls) -> list[str]:
        return list(cls._plugins.keys())


class AutoRegisterMeta(type):
    """Metaclass that automatically registers every subclass."""

    def __init__(cls, name: str, bases: tuple, namespace: dict):
        super().__init__(name, bases, namespace)
        if bases:  # Don't register the base class
            PluginRegistry.register(cls)


class BasePlugin(metaclass=AutoRegisterMeta):
    """Base class for all plugins. Subclasses are auto-registered."""

    def execute(self) -> str:
        raise NotImplementedError


class ImageProcessor(BasePlugin):
    """Processes image files."""
    def execute(self) -> str:
        return "Processing image..."


class VideoConverter(BasePlugin):
    """Converts video formats."""
    def execute(self) -> str:
        return "Converting video..."


class AudioNormalizer(BasePlugin):
    """Normalizes audio levels."""
    def execute(self) -> str:
        return "Normalizing audio..."


# ============================================================
# 6. ATTRIBUTE INJECTION METACLASS
# ============================================================
class InjectAttributesMeta(type):
    """Metaclass that injects common attributes and methods into classes."""

    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        # Inject a version attribute
        namespace["version"] = "1.0.0"

        # Inject a __repr__ if not defined
        if "__repr__" not in namespace:
            def auto_repr(self):
                attrs = {k: v for k, v in self.__dict__.items()
                         if not k.startswith("_")}
                attr_str = ", ".join(f"{k}={v!r}" for k, v in attrs.items())
                return f"{name}({attr_str})"
            namespace["__repr__"] = auto_repr

        # Inject a to_dict method
        if "to_dict" not in namespace:
            def to_dict(self) -> dict:
                return {k: v for k, v in self.__dict__.items()
                        if not k.startswith("_")}
            namespace["to_dict"] = to_dict

        return super().__new__(mcs, name, bases, namespace)


class User(metaclass=InjectAttributesMeta):
    """User model with auto-injected attributes."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class Product(metaclass=InjectAttributesMeta):
    """Product model with auto-injected attributes."""

    def __init__(self, title: str, price: float):
        self.title = title
        self.price = price


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Type Hierarchy")
    demonstrate_type_hierarchy()

    separator("2. Verbose Metaclass")
    print(f"\nAnimal.created_by = {Animal.created_by}")
    print(f"Dog.created_by    = {Dog.created_by}")
    print(f"Dog().speak()     = {Dog().speak()}")

    separator("3. Validation Metaclass")
    service = ValidatedService()
    print(f"Service result: {service.process('hello')}")

    separator("4. Singleton Metaclass")
    config1 = AppConfig()
    config2 = AppConfig()
    print(f"\nSame instance? {config1 is config2}")
    config1.set("debug", True)
    print(f"config1 debug = {config1.get('debug')}")
    print(f"config2 debug = {config2.get('debug')}")  # Also True

    pool1 = DatabasePool()
    pool1.add_connection("conn_1")
    pool2 = DatabasePool()
    print(f"Pool connections: {pool2.connections}")  # Shows conn_1

    separator("5. Auto-Registration")
    print(f"Registered plugins: {PluginRegistry.list_plugins()}")
    plugin_cls = PluginRegistry.get_plugin("ImageProcessor")
    plugin = plugin_cls()
    print(f"Plugin execute: {plugin.execute()}")

    separator("6. Attribute Injection")
    user = User("Alice", "alice@example.com")
    print(f"repr:     {user!r}")
    print(f"version:  {user.version}")
    print(f"to_dict:  {user.to_dict()}")

    product = Product("Widget", 29.99)
    print(f"repr:     {product!r}")
    print(f"version:  {product.version}")
    print(f"to_dict:  {product.to_dict()}")

    separator("Key Takeaway")
    print("Metaclasses are powerful but should be used sparingly.")
    print("Prefer simpler alternatives when possible:")
    print("  - __init_subclass__ for class-level hooks")
    print("  - Decorators for class modification")
    print("  - Class methods for factory patterns")


if __name__ == "__main__":
    main()
