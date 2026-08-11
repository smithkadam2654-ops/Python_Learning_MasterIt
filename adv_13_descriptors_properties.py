"""
Advanced Python - Lesson 13: Descriptors & Properties
======================================================
Descriptors are objects that manage attribute access via the
descriptor protocol (__get__, __set__, __delete__).

Topics Covered:
- Property decorator (@property)
- Descriptor protocol
- Data vs non-data descriptors
- Reusable descriptor classes
- __slots__ for memory optimization
- Attribute access control
"""

from typing import Any


# ============================================================
# 1. PROPERTY DECORATOR (@property)
# ============================================================
class Temperature:
    """Demonstrates @property for computed/validated attributes."""
    
    def __init__(self, celsius: float = 0.0):
        self._celsius = celsius  # Internal storage

    @property
    def celsius(self) -> float:
        """Get temperature in Celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        """Set temperature with validation."""
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero (-273.15°C)")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Computed property: convert to Fahrenheit."""
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float):
        """Set via Fahrenheit (converts to Celsius internally)."""
        self.celsius = (value - 32) * 5 / 9

    @property
    def kelvin(self) -> float:
        """Computed property: convert to Kelvin."""
        return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, value: float):
        """Set via Kelvin."""
        self.celsius = value - 273.15

    def __repr__(self):
        return f"Temperature({self._celsius}°C / {self.fahrenheit:.1f}°F / {self.kelvin:.1f}K)"


# ============================================================
# 2. DESCRIPTOR PROTOCOL
# ============================================================
class Validated:
    """Base descriptor for validated attributes.
    
    A descriptor is any object that defines __get__, __set__, or __delete__.
    When assigned as a CLASS attribute, Python calls these methods
    instead of normal attribute access.
    """
    def __init__(self, validator=None):
        self.validator = validator

    def __set_name__(self, owner, name):
        """Called when the descriptor is assigned to a class attribute.
        Stores the attribute name for internal storage.
        """
        self.public_name = name
        self.private_name = f"_descriptor_{name}"

    def __get__(self, obj, objtype=None):
        """Called on attribute access: instance.attr"""
        if obj is None:
            return self  # Accessed from class, not instance
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        """Called on attribute assignment: instance.attr = value"""
        if self.validator and not self.validator(value):
            raise ValueError(f"Validation failed for '{self.public_name}': {value!r}")
        setattr(obj, self.private_name, value)


class RangeValidator(Validated):
    """Descriptor that validates values are within a range."""
    def __init__(self, min_val: float, max_val: float):
        self.min_val = min_val
        self.max_val = max_val
        super().__init__(
            validator=lambda v: self.min_val <= v <= self.max_val
        )

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)


class TypeValidator(Validated):
    """Descriptor that validates the type of a value."""
    def __init__(self, *types):
        self.types = types
        super().__init__(
            validator=lambda v: isinstance(v, types)
        )


class NonEmptyString(Validated):
    """Descriptor that ensures a non-empty string."""
    def __init__(self):
        super().__init__(
            validator=lambda v: isinstance(v, str) and len(v.strip()) > 0
        )


# ============================================================
# 3. USING DESCRIPTORS IN CLASSES
# ============================================================
class Employee:
    """Employee with descriptor-based attribute validation."""
    
    # Descriptors are CLASS attributes
    name = NonEmptyString()
    age = RangeValidator(18, 120)
    salary = RangeValidator(0, 10_000_000)
    email = TypeValidator(str)

    def __init__(self, name: str, age: int, salary: float, email: str):
        self.name = name
        self.age = age
        self.salary = salary
        self.email = email

    def __repr__(self):
        return (
            f"Employee(name={self.name!r}, age={self.age}, "
            f"salary={self.salary:,.0f}, email={self.email!r})"
        )


# ============================================================
# 4. DESCRIPTOR FOR CACHED PROPERTIES
# ============================================================
class CachedProperty:
    """Descriptor that computes a value once and caches it.
    
    Similar to functools.cached_property but implemented manually.
    """
    def __init__(self, func):
        self.func = func
        self.attr_name = func.__name__
        self.__doc__ = func.__doc__

    def __set_name__(self, owner, name):
        self.attr_name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # Check if already cached
        if self.attr_name not in obj.__dict__:
            print(f"  [Computing {self.attr_name}...]")
            obj.__dict__[self.attr_name] = self.func(obj)
        return obj.__dict__[self.attr_name]


class DataProcessor:
    """Processor with cached computed properties."""
    
    def __init__(self, data: list[float]):
        self.data = data

    @CachedProperty
    def mean(self) -> float:
        """Compute mean (cached after first access)."""
        return sum(self.data) / len(self.data)

    @CachedProperty
    def variance(self) -> float:
        """Compute variance (cached after first access)."""
        m = self.mean  # Uses cached mean
        return sum((x - m) ** 2 for x in self.data) / len(self.data)

    @CachedProperty
    def std_dev(self) -> float:
        """Compute standard deviation (cached)."""
        return self.variance ** 0.5  # Uses cached variance


# ============================================================
# 5. DESCRIPTOR FOR EVENT/LOGGING
# ============================================================
class LoggedAttribute:
    """Descriptor that logs every get and set operation."""
    
    def __init__(self, default=None):
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"_logged_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = getattr(obj, self.storage_name, self.default)
        print(f"  [LOG] GET {self.name} = {value!r}")
        return value

    def __set__(self, obj, value):
        old = getattr(obj, self.storage_name, self.default)
        print(f"  [LOG] SET {self.name}: {old!r} -> {value!r}")
        setattr(obj, self.storage_name, value)


class TrackedConfig:
    """Configuration object with logged attribute access."""
    
    debug = LoggedAttribute(default=False)
    log_level = LoggedAttribute(default="INFO")
    max_retries = LoggedAttribute(default=3)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# ============================================================
# 6. __SLOTS__ FOR MEMORY OPTIMIZATION
# ============================================================
class RegularPoint:
    """Regular class — uses __dict__ for attributes."""
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class SlottedPoint:
    """Class with __slots__ — no __dict__, saves memory."""
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def distance(self) -> float:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5


def demonstrate_slots():
    """Show memory savings from __slots__."""
    import sys
    
    regular = RegularPoint(1.0, 2.0, 3.0)
    slotted = SlottedPoint(1.0, 2.0, 3.0)
    
    print(f"RegularPoint size: {sys.getsizeof(regular)} bytes + __dict__")
    print(f"  __dict__ size:   {sys.getsizeof(regular.__dict__)} bytes")
    print(f"  Total: ~{sys.getsizeof(regular) + sys.getsizeof(regular.__dict__)} bytes")
    
    print(f"\nSlottedPoint size: {sys.getsizeof(slotted)} bytes (no __dict__)")
    print(f"  Has __dict__?    {hasattr(slotted, '__dict__')}")
    print(f"  Distance:        {slotted.distance():.2f}")
    
    # Memory comparison with many instances
    n = 100_000
    regular_list = [RegularPoint(1.0, 2.0, 3.0) for _ in range(n)]
    slotted_list = [SlottedPoint(1.0, 2.0, 3.0) for _ in range(n)]
    
    import sys
    reg_mem = sum(sys.getsizeof(p) + sys.getsizeof(p.__dict__) for p in regular_list)
    slot_mem = sum(sys.getsizeof(p) for p in slotted_list)
    
    print(f"\n{n:,} instances:")
    print(f"  Regular: {reg_mem / 1024 / 1024:.1f} MB")
    print(f"  Slotted: {slot_mem / 1024 / 1024:.1f} MB")
    print(f"  Savings: {(1 - slot_mem/reg_mem) * 100:.0f}%")
    
    # Slotted objects can't have new attributes
    try:
        slotted.w = 4.0
    except AttributeError:
        print("\n  Cannot add new attributes to slotted objects (as expected)")


# ============================================================
# 7. READ-ONLY DESCRIPTOR (Immutable Attributes)
# ============================================================
class ReadOnly:
    """Descriptor that allows setting only once (immutable after init)."""
    
    def __init__(self):
        pass

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_readonly_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        if hasattr(obj, self.storage):
            raise AttributeError(f"'{self.name}' is read-only and cannot be modified")
        setattr(obj, self.storage, value)


class ImmutableConfig:
    """Configuration that can't be changed after initialization."""
    app_name = ReadOnly()
    version = ReadOnly()
    build_date = ReadOnly()

    def __init__(self, app_name: str, version: str, build_date: str):
        self.app_name = app_name
        self.version = version
        self.build_date = build_date


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Property Decorator")
    temp = Temperature(100.0)
    print(f"Boiling water: {temp}")
    temp.fahrenheit = 32
    print(f"Freezing point: {temp}")
    temp.kelvin = 0
    print(f"Absolute zero: {temp}")
    try:
        temp.celsius = -300
    except ValueError as e:
        print(f"Validation: {e}")

    separator("2-3. Descriptors in Action")
    emp = Employee("Alice", 30, 95000, "alice@example.com")
    print(f"Created: {emp}")
    
    emp.salary = 105000
    print(f"Updated: {emp}")
    
    try:
        emp.age = 15
    except ValueError as e:
        print(f"Validation: {e}")
    
    try:
        emp.salary = -5000
    except ValueError as e:
        print(f"Validation: {e}")

    separator("4. Cached Property")
    data = [2.5, 4.1, 3.7, 5.2, 4.8, 3.9, 6.1]
    processor = DataProcessor(data)
    print(f"First access:")
    print(f"  Mean:     {processor.mean:.4f}")
    print(f"  Variance: {processor.variance:.4f}")
    print(f"  Std Dev:  {processor.std_dev:.4f}")
    print(f"Second access (cached):")
    print(f"  Mean:     {processor.mean:.4f}")
    print(f"  Std Dev:  {processor.std_dev:.4f}")

    separator("5. Logged Attributes")
    config = TrackedConfig(debug=True, log_level="DEBUG")
    _ = config.debug
    config.max_retries = 5

    separator("6. __slots__ Memory Optimization")
    demonstrate_slots()

    separator("7. Read-Only Descriptor")
    cfg = ImmutableConfig("MyApp", "2.1.0", "2024-06-15")
    print(f"App: {cfg.app_name} v{cfg.version}")
    try:
        cfg.version = "3.0.0"
    except AttributeError as e:
        print(f"Immutable: {e}")


if __name__ == "__main__":
    main()
