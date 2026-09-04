"""
Dependency Injection - Dependency injection container implementation.
Features: Service registration, singleton and transient lifetimes, and automatic resolution.
"""

import inspect
from typing import Type, TypeVar, Callable, Dict, Any, Optional, get_type_hints
from dataclasses import dataclass
from enum import Enum


T = TypeVar('T')


class Lifetime(Enum):
    """Service lifetime."""
    TRANSIENT = "transient"  # New instance each time
    SINGLETON = "singleton"  # Same instance for all requests
    SCOPED = "scoped"  # Same instance within scope


@dataclass
class ServiceDescriptor:
    """Service registration descriptor."""
    factory: Callable
    lifetime: Lifetime
    instance: Any = None


class ServiceContainer:
    """Dependency injection container."""
    
    def __init__(self) -> None:
        """Initialize service container."""
        self._services: Dict[Type, ServiceDescriptor] = {}
        self._instances: Dict[Type, Any] = {}
        self._scoped_instances: Dict[Type, Any] = {}
    
    def register_transient(self, interface: Type[T], implementation: Type[T] = None) -> None:
        """
        Register transient service (new instance each time).
        
        Args:
            interface: Service interface/type
            implementation: Implementation class (same as interface if None)
        """
        impl = implementation or interface
        self._services[interface] = ServiceDescriptor(
            factory=lambda: self._create_instance(impl),
            lifetime=Lifetime.TRANSIENT
        )
    
    def register_singleton(self, interface: Type[T], implementation: Type[T] = None) -> None:
        """
        Register singleton service (same instance always).
        
        Args:
            interface: Service interface/type
            implementation: Implementation class (same as interface if None)
        """
        impl = implementation or interface
        self._services[interface] = ServiceDescriptor(
            factory=lambda: self._create_instance(impl),
            lifetime=Lifetime.SINGLETON
        )
    
    def register_scoped(self, interface: Type[T], implementation: Type[T] = None) -> None:
        """
        Register scoped service (same instance within scope).
        
        Args:
            interface: Service interface/type
            implementation: Implementation class (same as interface if None)
        """
        impl = implementation or interface
        self._services[interface] = ServiceDescriptor(
            factory=lambda: self._create_instance(impl),
            lifetime=Lifetime.SCOPED
        )
    
    def register_instance(self, interface: Type[T], instance: T) -> None:
        """
        Register an existing instance.
        
        Args:
            interface: Service interface/type
            instance: Instance to register
        """
        self._services[interface] = ServiceDescriptor(
            factory=lambda: instance,
            lifetime=Lifetime.SINGLETON,
            instance=instance
        )
        self._instances[interface] = instance
    
    def register_factory(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """
        Register a factory function.
        
        Args:
            interface: Service interface/type
            factory: Factory function
        """
        self._services[interface] = ServiceDescriptor(
            factory=factory,
            lifetime=Lifetime.TRANSIENT
        )
    
    def resolve(self, interface: Type[T]) -> T:
        """
        Resolve a service from the container.
        
        Args:
            interface: Service interface/type
            
        Returns:
            Resolved service instance
        """
        if interface not in self._services:
            raise ValueError(f"Service {interface} not registered")
        
        descriptor = self._services[interface]
        
        # Return existing instance for singletons
        if descriptor.lifetime == Lifetime.SINGLETON:
            if interface not in self._instances:
                self._instances[interface] = descriptor.factory()
            return self._instances[interface]
        
        # Return scoped instance
        if descriptor.lifetime == Lifetime.SCOPED:
            if interface not in self._scoped_instances:
                self._scoped_instances[interface] = descriptor.factory()
            return self._scoped_instances[interface]
        
        # Create new instance for transient
        return descriptor.factory()
    
    def _create_instance(self, cls: Type) -> Any:
        """
        Create instance with dependency injection.
        
        Args:
            cls: Class to instantiate
            
        Returns:
            Created instance
        """
        constructor = cls.__init__
        signature = inspect.signature(constructor)
        
        kwargs = {}
        
        for param_name, param in signature.parameters.items():
            if param_name == 'self':
                continue
            
            if param.annotation != inspect.Parameter.empty:
                dependency = self.resolve(param.annotation)
                kwargs[param_name] = dependency
        
        return cls(**kwargs)
    
    def begin_scope(self) -> 'Scope':
        """
        Begin a new scope.
        
        Returns:
            New scope
        """
        return Scope(self)
    
    def clear_scoped(self) -> None:
        """Clear all scoped instances."""
        self._scoped_instances.clear()


class Scope:
    """Dependency injection scope."""
    
    def __init__(self, container: ServiceContainer) -> None:
        """
        Initialize scope.
        
        Args:
            container: Parent container
        """
        self.container = container
        self._previous_scoped: Dict[Type, Any] = {}
    
    def __enter__(self) -> 'Scope':
        """Enter scope."""
        self._previous_scoped = self.container._scoped_instances.copy()
        self.container._scoped_instances.clear()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit scope."""
        self.container._scoped_instances = self._previous_scoped


# Example services
class ILogger:
    """Logger interface."""
    
    def log(self, message: str) -> None:
        """Log a message."""
        pass


class ConsoleLogger(ILogger):
    """Console logger implementation."""
    
    def log(self, message: str) -> None:
        """Log to console."""
        print(f"[LOG] {message}")


class FileLogger(ILogger):
    """File logger implementation."""
    
    def __init__(self, filename: str) -> None:
        """Initialize file logger."""
        self.filename = filename
    
    def log(self, message: str) -> None:
        """Log to file."""
        print(f"[FILE:{self.filename}] {message}")


class ICache:
    """Cache interface."""
    
    def get(self, key: str) -> Any:
        """Get value from cache."""
        pass
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        pass


class MemoryCache(ICache):
    """In-memory cache implementation."""
    
    def __init__(self) -> None:
        """Initialize cache."""
        self._cache: Dict[str, Any] = {}
    
    def get(self, key: str) -> Any:
        """Get value from cache."""
        return self._cache.get(key)
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        self._cache[key] = value


class UserRepository:
    """User repository with dependencies."""
    
    def __init__(self, logger: ILogger, cache: ICache) -> None:
        """
        Initialize repository.
        
        Args:
            logger: Logger service
            cache: Cache service
        """
        self.logger = logger
        self.cache = cache
        self._users = {}
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID."""
        cache_key = f"user:{user_id}"
        
        # Try cache first
        cached = self.cache.get(cache_key)
        if cached:
            self.logger.log(f"User {user_id} from cache")
            return cached
        
        # Get from storage
        user = self._users.get(user_id)
        if user:
            self.cache.set(cache_key, user)
            self.logger.log(f"User {user_id} from storage")
        
        return user
    
    def save_user(self, user_id: int, user_data: Dict) -> None:
        """Save user."""
        self._users[user_id] = user_data
        self.cache.set(f"user:{user_id}", user_data)
        self.logger.log(f"User {user_id} saved")


class UserService:
    """User service with dependencies."""
    
    def __init__(self, repository: UserRepository, logger: ILogger) -> None:
        """
        Initialize service.
        
        Args:
            repository: User repository
            logger: Logger service
        """
        self.repository = repository
        self.logger = logger
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user."""
        self.logger.log(f"Fetching user {user_id}")
        return self.repository.get_user(user_id)
    
    def create_user(self, user_id: int, name: str) -> Dict:
        """Create user."""
        user_data = {"id": user_id, "name": name}
        self.repository.save_user(user_id, user_data)
        self.logger.log(f"User {name} created")
        return user_data


def main() -> None:
    """Demonstrate dependency injection."""
    
    print("=== Dependency Injection Container ===")
    
    # Create container
    container = ServiceContainer()
    
    # Register services
    container.register_singleton(ILogger, ConsoleLogger)
    container.register_singleton(ICache, MemoryCache)
    container.register_transient(UserRepository)
    container.register_transient(UserService)
    
    # Resolve service
    user_service = container.resolve(UserService)
    
    # Use service
    user_service.create_user(1, "Alice")
    user_service.create_user(2, "Bob")
    
    user1 = user_service.get_user(1)
    user2 = user_service.get_user(2)
    
    print(f"User 1: {user1}")
    print(f"User 2: {user2}")
    
    print("\n=== Singleton vs Transient ===")
    logger1 = container.resolve(ILogger)
    logger2 = container.resolve(ILogger)
    
    repo1 = container.resolve(UserRepository)
    repo2 = container.resolve(UserRepository)
    
    print(f"Logger instances same: {logger1 is logger2}")  # True (singleton)
    print(f"Repository instances same: {repo1 is repo2}")  # False (transient)
    
    print("\n=== Scoped Lifetime ===")
    container.register_scoped(ILogger, FileLogger)
    
    with container.begin_scope():
        logger1 = container.resolve(ILogger)
        logger1.log("Message in scope 1")
        
        with container.begin_scope():
            logger2 = container.resolve(ILogger)
            logger2.log("Message in scope 2")
    
    print("\n=== Factory Registration ===")
    def create_special_logger() -> ILogger:
        """Factory for special logger."""
        class SpecialLogger(ILogger):
            def log(self, message: str) -> None:
                print(f"[SPECIAL] {message}")
        return SpecialLogger()
    
    container.register_factory(ILogger, create_special_logger)
    
    logger = container.resolve(ILogger)
    logger.log("Using factory-created logger")
    
    print("\n=== Instance Registration ===")
    custom_logger = ConsoleLogger()
    container.register_instance(ILogger, custom_logger)
    
    logger = container.resolve(ILogger)
    logger.log("Using registered instance")


if __name__ == "__main__":
    main()
