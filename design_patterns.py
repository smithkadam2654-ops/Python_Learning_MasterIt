"""
Design Patterns Module

This module provides comprehensive design pattern implementations including:
- Creational patterns (Singleton, Factory, Builder, Prototype)
- Structural patterns (Adapter, Decorator, Facade, Proxy)
- Behavioral patterns (Observer, Strategy, Command, Iterator)
- Other useful patterns (Registry, Dependency Injection, State Machine)

All patterns include comprehensive docstrings and type hints.
"""

from typing import Any, Dict, List, Optional, Callable, Type
from dataclasses import dataclass
from enum import Enum
import threading
import json
from abc import ABC, abstractmethod


class SingletonMeta(type):
    """Metaclass for singleton pattern."""
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """Singleton pattern implementation."""
    
    def __init__(self):
        """Initialize singleton."""
        if not hasattr(self, 'initialized'):
            self.value = 0
            self.initialized = True
    
    def increment(self) -> int:
        """Increment value."""
        self.value += 1
        return self.value
    
    def get_value(self) -> int:
        """Get current value."""
        return self.value


class Factory:
    """Factory pattern implementation."""
    
    @staticmethod
    def create_product(product_type: str, *args, **kwargs) -> Any:
        """Factory method to create products."""
        products = {
            "A": ProductA,
            "B": ProductB,
            "C": ProductC
        }
        
        product_class = products.get(product_type)
        if product_class:
            return product_class(*args, **kwargs)
        
        raise ValueError(f"Unknown product type: {product_type}")


class Product(ABC):
    """Abstract product base class."""
    
    @abstractmethod
    def operation(self) -> str:
        """Product operation."""
        pass


class ProductA(Product):
    """Concrete product A."""
    
    def operation(self) -> str:
        """Product A operation."""
        return "Product A operation"


class ProductB(Product):
    """Concrete product B."""
    
    def operation(self) -> str:
        """Product B operation."""
        return "Product B operation"


class ProductC(Product):
    """Concrete product C."""
    
    def operation(self) -> str:
        """Product C operation."""
        return "Product C operation"


class Builder:
    """Builder pattern implementation."""
    
    def __init__(self):
        """Initialize builder."""
        self.reset()
    
    def reset(self) -> None:
        """Reset builder state."""
        self._product = ProductResult()
    
    def set_part_a(self, value: str) -> None:
        """Set part A."""
        self._product.parts.append(f"Part A: {value}")
    
    def set_part_b(self, value: str) -> None:
        """Set part B."""
        self._product.parts.append(f"Part B: {value}")
    
    def set_part_c(self, value: str) -> None:
        """Set part C."""
        self._product.parts.append(f"Part C: {value}")
    
    def get_result(self) -> 'ProductResult':
        """Get built product."""
        result = self._product
        self.reset()
        return result


class ProductResult:
    """Product built by builder."""
    
    def __init__(self):
        """Initialize product."""
        self.parts = []
    
    def list_parts(self) -> str:
        """List all parts."""
        return ", ".join(self.parts)


class Prototype:
    """Prototype pattern implementation."""
    
    def __init__(self, value: str):
        """Initialize prototype."""
        self.value = value
    
    def clone(self) -> 'Prototype':
        """Clone the prototype."""
        return Prototype(self.value)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Prototype({self.value})"


class Adapter:
    """Adapter pattern implementation."""
    
    def __init__(self, adaptee: 'Adaptee'):
        """Initialize adapter with adaptee."""
        self.adaptee = adaptee
    
    def request(self) -> str:
        """Adapt request to target interface."""
        return f"Adapter: {self.adaptee.specific_request()}"


class Adaptee:
    """Class with incompatible interface."""
    
    def specific_request(self) -> str:
        """Specific request."""
        return "Specific request from adaptee"


class Decorator:
    """Decorator pattern implementation."""
    
    def __init__(self, component: 'Component'):
        """Initialize decorator."""
        self._component = component
    
    def operation(self) -> str:
        """Delegate operation to component."""
        return self._component.operation()


class ConcreteDecoratorA(Decorator):
    """Concrete decorator A."""
    
    def operation(self) -> str:
        """Add decoration A."""
        return f"ConcreteDecoratorA({self._component.operation()})"
    
    def added_behavior(self) -> str:
        """Added behavior."""
        return "Added behavior A"


class ConcreteDecoratorB(Decorator):
    """Concrete decorator B."""
    
    def operation(self) -> str:
        """Add decoration B."""
        return f"ConcreteDecoratorB({self._component.operation()})"
    
    def added_behavior(self) -> str:
        """Added behavior."""
        return "Added behavior B"


class Component:
    """Base component for decorators."""
    
    def operation(self) -> str:
        """Base operation."""
        return "Component operation"


class Facade:
    """Facade pattern implementation."""
    
    def __init__(self):
        """Initialize facade with subsystems."""
        self._subsystem_a = SubsystemA()
        self._subsystem_b = SubsystemB()
        self._subsystem_c = SubsystemC()
    
    def operation(self) -> str:
        """Simplified interface to subsystem."""
        results = []
        results.append("Facade initializes subsystems:")
        results.append(self._subsystem_a.operation_a())
        results.append(self._subsystem_b.operation_b())
        results.append(self._subsystem_c.operation_c())
        results.append("Facade orders subsystems to perform the action:")
        results.append(self._subsystem_a.operation_a1())
        results.append(self._subsystem_b.operation_b1())
        results.append(self._subsystem_c.operation_c1())
        
        return "\n".join(results)


class SubsystemA:
    """Subsystem A."""
    
    def operation_a(self) -> str:
        """Operation A."""
        return "SubsystemA: Ready"
    
    def operation_a1(self) -> str:
        """Operation A1."""
        return "SubsystemA: Action"


class SubsystemB:
    """Subsystem B."""
    
    def operation_b(self) -> str:
        """Operation B."""
        return "SubsystemB: Ready"
    
    def operation_b1(self) -> str:
        """Operation B1."""
        return "SubsystemB: Action"


class SubsystemC:
    """Subsystem C."""
    
    def operation_c(self) -> str:
        """Operation C."""
        return "SubsystemC: Ready"
    
    def operation_c1(self) -> str:
        """Operation C1."""
        return "SubsystemC: Action"


class Proxy:
    """Proxy pattern implementation."""
    
    def __init__(self, real_subject: 'RealSubject'):
        """Initialize proxy with real subject."""
        self._real_subject = real_subject
    
    def request(self) -> str:
        """Proxy request."""
        if self.check_access():
            return self._real_subject.request()
        return "Proxy: Access denied"
    
    def check_access(self) -> bool:
        """Check access permission."""
        return True


class RealSubject:
    """Real subject for proxy."""
    
    def request(self) -> str:
        """Real request."""
        return "RealSubject: Handling request"


class Observer(ABC):
    """Observer abstract base class."""
    
    @abstractmethod
    def update(self, event: str, data: Any) -> None:
        """Update observer with event."""
        pass


class Subject:
    """Subject (observable) for observer pattern."""
    
    def __init__(self):
        """Initialize subject."""
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """Attach observer."""
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach observer."""
        self._observers.remove(observer)
    
    def notify(self, event: str, data: Any) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(event, data)


class ConcreteObserverA(Observer):
    """Concrete observer A."""
    
    def update(self, event: str, data: Any) -> None:
        """Update observer A."""
        print(f"ObserverA: Received event '{event}' with data: {data}")


class ConcreteObserverB(Observer):
    """Concrete observer B."""
    
    def update(self, event: str, data: Any) -> None:
        """Update observer B."""
        print(f"ObserverB: Received event '{event}' with data: {data}")


class Strategy(ABC):
    """Strategy abstract base class."""
    
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute strategy."""
        pass


class ConcreteStrategyA(Strategy):
    """Concrete strategy A."""
    
    def execute(self, data: Any) -> Any:
        """Execute strategy A."""
        return f"Strategy A applied to {data}"


class ConcreteStrategyB(Strategy):
    """Concrete strategy B."""
    
    def execute(self, data: Any) -> Any:
        """Execute strategy B."""
        return f"Strategy B applied to {data}"


class Context:
    """Context for strategy pattern."""
    
    def __init__(self, strategy: Strategy):
        """Initialize context with strategy."""
        self._strategy = strategy
    
    def set_strategy(self, strategy: Strategy) -> None:
        """Set strategy."""
        self._strategy = strategy
    
    def execute_strategy(self, data: Any) -> Any:
        """Execute current strategy."""
        return self._strategy.execute(data)


class Command(ABC):
    """Command abstract base class."""
    
    @abstractmethod
    def execute(self) -> None:
        """Execute command."""
        pass
    
    @abstractmethod
    def undo(self) -> None:
        """Undo command."""
        pass


class SimpleCommand(Command):
    """Simple command."""
    
    def __init__(self, receiver: 'Receiver', action: str):
        """Initialize command."""
        self._receiver = receiver
        self._action = action
    
    def execute(self) -> None:
        """Execute command."""
        self._receiver.action(self._action)
    
    def undo(self) -> None:
        """Undo command."""
        self._receiver.undo(self._action)


class Receiver:
    """Receiver for commands."""
    
    def action(self, action: str) -> None:
        """Perform action."""
        print(f"Receiver: Executing {action}")
    
    def undo(self, action: str) -> None:
        """Undo action."""
        print(f"Receiver: Undoing {action}")


class Invoker:
    """Invoker for commands."""
    
    def __init__(self):
        """Initialize invoker."""
        self._history: List[Command] = []
    
    def execute_command(self, command: Command) -> None:
        """Execute command."""
        command.execute()
        self._history.append(command)
    
    def undo_last(self) -> None:
        """Undo last command."""
        if self._history:
            command = self._history.pop()
            command.undo()


class Iterator(ABC):
    """Iterator abstract base class."""
    
    @abstractmethod
    def has_next(self) -> bool:
        """Check if has next element."""
        pass
    
    @abstractmethod
    def next(self) -> Any:
        """Get next element."""
        pass


class ConcreteIterator(Iterator):
    """Concrete iterator."""
    
    def __init__(self, collection: 'Collection'):
        """Initialize iterator."""
        self._collection = collection
        self._index = 0
    
    def has_next(self) -> bool:
        """Check if has next."""
        return self._index < len(self._collection.items)
    
    def next(self) -> Any:
        """Get next element."""
        if self.has_next():
            item = self._collection.items[self._index]
            self._index += 1
            return item
        raise StopIteration


class Collection:
    """Collection for iterator pattern."""
    
    def __init__(self):
        """Initialize collection."""
        self.items = []
    
    def add_item(self, item: Any) -> None:
        """Add item to collection."""
        self.items.append(item)
    
    def create_iterator(self) -> Iterator:
        """Create iterator."""
        return ConcreteIterator(self)


class Registry:
    """Registry pattern implementation."""
    
    def __init__(self):
        """Initialize registry."""
        self._registry: Dict[str, Any] = {}
    
    def register(self, name: str, item: Any) -> None:
        """Register item."""
        self._registry[name] = item
    
    def unregister(self, name: str) -> None:
        """Unregister item."""
        if name in self._registry:
            del self._registry[name]
    
    def get(self, name: str) -> Optional[Any]:
        """Get registered item."""
        return self._registry.get(name)
    
    def list_registered(self) -> List[str]:
        """List all registered names."""
        return list(self._registry.keys())


class DependencyInjector:
    """Dependency injection container."""
    
    def __init__(self):
        """Initialize injector."""
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
    
    def register(self, name: str, service: Any) -> None:
        """Register service."""
        self._services[name] = service
    
    def register_factory(self, name: str, factory: Callable) -> None:
        """Register factory."""
        self._factories[name] = factory
    
    def get(self, name: str) -> Any:
        """Get service."""
        if name in self._services:
            return self._services[name]
        elif name in self._factories:
            return self._factories[name]()
        raise ValueError(f"Service '{name}' not found")
    
    def inject(self, *dependencies: str):
        """Decorator for dependency injection."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                injected = {dep: self.get(dep) for dep in dependencies}
                return func(*args, **kwargs, **injected)
            return wrapper
        return decorator


class State(ABC):
    """State abstract base class."""
    
    @abstractmethod
    def handle(self) -> str:
        """Handle state."""
        pass


class ConcreteStateA(State):
    """Concrete state A."""
    
    def handle(self) -> str:
        """Handle state A."""
        return "Handling in State A"


class ConcreteStateB(State):
    """Concrete state B."""
    
    def handle(self) -> str:
        """Handle state B."""
        return "Handling in State B"


class StateMachine:
    """State machine implementation."""
    
    def __init__(self, initial_state: State):
        """Initialize state machine."""
        self._state = initial_state
    
    def set_state(self, state: State) -> None:
        """Set current state."""
        self._state = state
    
    def handle(self) -> str:
        """Handle current state."""
        return self._state.handle()


class ChainOfResponsibility:
    """Chain of responsibility pattern."""
    
    def __init__(self):
        """Initialize chain."""
        self._handlers: List[Callable] = []
    
    def add_handler(self, handler: Callable) -> None:
        """Add handler to chain."""
        self._handlers.append(handler)
    
    def handle(self, request: Any) -> Any:
        """Handle request through chain."""
        for handler in self._handlers:
            result = handler(request)
            if result is not None:
                return result
        return None


class Memento:
    """Memento pattern for undo/redo."""
    
    def __init__(self, state: Any):
        """Initialize memento."""
        self._state = state
        self._timestamp = None
    
    def get_state(self) -> Any:
        """Get saved state."""
        return self._state
    
    def get_timestamp(self) -> Optional[float]:
        """Get timestamp."""
        return self._timestamp
    
    def set_timestamp(self, timestamp: float) -> None:
        """Set timestamp."""
        self._timestamp = timestamp


class Caretaker:
    """Caretaker for mementos."""
    
    def __init__(self):
        """Initialize caretaker."""
        self._mementos: List[Memento] = []
    
    def save(self, memento: Memento) -> None:
        """Save memento."""
        memento.set_timestamp(time.time())
        self._mementos.append(memento)
    
    def restore(self, index: int) -> Optional[Memento]:
        """Restore memento."""
        if 0 <= index < len(self._mementos):
            return self._mementos[index]
        return None
    
    def get_history(self) -> List[Memento]:
        """Get memento history."""
        return self._mementos.copy()


class Lazy:
    """Lazy initialization pattern."""
    
    def __init__(self, factory: Callable):
        """Initialize lazy object."""
        self._factory = factory
        self._value = None
        self._initialized = False
    
    def get(self) -> Any:
        """Get value, initializing if necessary."""
        if not self._initialized:
            self._value = self._factory()
            self._initialized = True
        return self._value
    
    def reset(self) -> None:
        """Reset lazy initialization."""
        self._value = None
        self._initialized = False


class ObjectPool:
    """Object pool pattern."""
    
    def __init__(self, factory: Callable, max_size: int = 10):
        """Initialize object pool."""
        self._factory = factory
        self._pool: List[Any] = []
        self._max_size = max_size
    
    def acquire(self) -> Any:
        """Acquire object from pool."""
        if self._pool:
            return self._pool.pop()
        return self._factory()
    
    def release(self, obj: Any) -> None:
        """Release object back to pool."""
        if len(self._pool) < self._max_size:
            self._pool.append(obj)
    
    def get_pool_size(self) -> int:
        """Get current pool size."""
        return len(self._pool)


def demonstrate_design_patterns():
    """Demonstrate design patterns functionality."""
    print("=== Design Patterns Demonstration ===\n")
    
    # Singleton
    print("1. Singleton Pattern:")
    singleton1 = Singleton()
    singleton2 = Singleton()
    
    print(f"   Same instance: {singleton1 is singleton2}")
    singleton1.increment()
    print(f"   Value: {singleton2.get_value()}")
    
    # Factory
    print("\n2. Factory Pattern:")
    product_a = Factory.create_product("A")
    product_b = Factory.create_product("B")
    
    print(f"   Product A: {product_a.operation()}")
    print(f"   Product B: {product_b.operation()}")
    
    # Builder
    print("\n3. Builder Pattern:")
    builder = Builder()
    builder.set_part_a("Value 1")
    builder.set_part_b("Value 2")
    builder.set_part_c("Value 3")
    
    product = builder.get_result()
    print(f"   Built product: {product.list_parts()}")
    
    # Prototype
    print("\n4. Prototype Pattern:")
    prototype = Prototype("Original")
    clone = prototype.clone()
    
    print(f"   Original: {prototype}")
    print(f"   Clone: {clone}")
    
    # Adapter
    print("\n5. Adapter Pattern:")
    adaptee = Adaptee()
    adapter = Adapter(adaptee)
    
    print(f"   Adapted request: {adapter.request()}")
    
    # Decorator
    print("\n6. Decorator Pattern:")
    component = Component()
    decorator_a = ConcreteDecoratorA(component)
    decorator_b = ConcreteDecoratorB(decorator_a)
    
    print(f"   Decorated: {decorator_b.operation()}")
    
    # Facade
    print("\n7. Facade Pattern:")
    facade = Facade()
    print(f"   Facade operation:\n{facade.operation()}")
    
    # Proxy
    print("\n8. Proxy Pattern:")
    real_subject = RealSubject()
    proxy = Proxy(real_subject)
    
    print(f"   Proxy request: {proxy.request()}")
    
    # Observer
    print("\n9. Observer Pattern:")
    subject = Subject()
    observer_a = ConcreteObserverA()
    observer_b = ConcreteObserverB()
    
    subject.attach(observer_a)
    subject.attach(observer_b)
    
    print("   Notifying observers:")
    subject.notify("test_event", {"data": "test"})
    
    # Strategy
    print("\n10. Strategy Pattern:")
    context = Context(ConcreteStrategyA())
    print(f"   Strategy A: {context.execute_strategy('test')}")
    
    context.set_strategy(ConcreteStrategyB())
    print(f"   Strategy B: {context.execute_strategy('test')}")
    
    # Command
    print("\n11. Command Pattern:")
    receiver = Receiver()
    invoker = Invoker()
    
    command = SimpleCommand(receiver, "action1")
    invoker.execute_command(command)
    
    print("   Undoing last command:")
    invoker.undo_last()
    
    # Iterator
    print("\n12. Iterator Pattern:")
    collection = Collection()
    collection.add_item("Item 1")
    collection.add_item("Item 2")
    collection.add_item("Item 3")
    
    iterator = collection.create_iterator()
    print("   Iterating:")
    while iterator.has_next():
        print(f"     {iterator.next()}")
    
    # Registry
    print("\n13. Registry Pattern:")
    registry = Registry()
    registry.register("service1", "Value 1")
    registry.register("service2", "Value 2")
    
    print(f"   Registered: {registry.list_registered()}")
    print(f"   Get service1: {registry.get('service1')}")
    
    # Dependency Injection
    print("\n14. Dependency Injection:")
    injector = DependencyInjector()
    injector.register("db_connection", "mock_connection")
    injector.register("logger", "mock_logger")
    
    @injector.inject("db_connection", "logger")
    def process_data(db_connection, logger):
        return f"Processing with {db_connection} and {logger}"
    
    print(f"   Injected function: {process_data()}")
    
    # State Machine
    print("\n15. State Machine:")
    state_machine = StateMachine(ConcreteStateA())
    print(f"   State A: {state_machine.handle()}")
    
    state_machine.set_state(ConcreteStateB())
    print(f"   State B: {state_machine.handle()}")
    
    # Chain of Responsibility
    print("\n16. Chain of Responsibility:")
    chain = ChainOfResponsibility()
    
    def handler1(request):
        if request == "type1":
            return "Handled by handler1"
        return None
    
    def handler2(request):
        if request == "type2":
            return "Handled by handler2"
        return None
    
    chain.add_handler(handler1)
    chain.add_handler(handler2)
    
    print(f"   Request type1: {chain.handle('type1')}")
    print(f"   Request type2: {chain.handle('type2')}")
    
    # Memento
    print("\n17. Memento Pattern:")
    caretaker = Caretaker()
    
    memento1 = Memento("State 1")
    memento2 = Memento("State 2")
    
    caretaker.save(memento1)
    caretaker.save(memento2)
    
    restored = caretaker.restore(0)
    print(f"   Restored state: {restored.get_state()}")
    
    # Lazy Initialization
    print("\n18. Lazy Initialization:")
    
    def expensive_operation():
        print("   Computing expensive value...")
        return "Expensive Result"
    
    lazy_value = Lazy(expensive_operation)
    print(f"   First get: {lazy_value.get()}")
    print(f"   Second get: {lazy_value.get()}")
    
    # Object Pool
    print("\n19. Object Pool:")
    
    def create_object():
        print("   Creating new object")
        return {"id": id(object())}
    
    pool = ObjectPool(create_object, max_size=3)
    
    obj1 = pool.acquire()
    obj2 = pool.acquire()
    
    print(f"   Pool size: {pool.get_pool_size()}")
    
    pool.release(obj1)
    print(f"   After release: {pool.get_pool_size()}")
    
    print("\n=== Demonstration Complete ===")
    print("\nDesign Patterns Best Practices:")
    print("- Use Singleton for shared resources (databases, loggers)")
    print("- Use Factory for object creation with complex logic")
    print("- Use Builder for complex object construction")
    print("- Use Prototype for object cloning")
    print("- Use Adapter to make incompatible interfaces work together")
    print("- Use Decorator to add behavior dynamically")
    print("- Use Facade to simplify complex subsystems")
    print("- Use Proxy to control access to objects")
    print("- Use Observer for event-driven communication")
    print("- Use Strategy for interchangeable algorithms")
    print("- Use Command for encapsulating requests")
    print("- Use Iterator for traversing collections")
    print("- Use Registry for managing objects by name")
    print("- Use Dependency Injection for loose coupling")
    print("- Use State Machine for state-dependent behavior")
    print("- Use Chain of Responsibility for processing pipelines")
    print("- Use Memento for undo/redo functionality")
    print("- Use Lazy for expensive initialization")
    print("- Use Object Pool for reusable objects")


if __name__ == "__main__":
    import time
    demonstrate_design_patterns()