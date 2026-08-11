"""
Advanced Python - Lesson 05: OOP Design Patterns
==================================================
Design patterns are reusable solutions to common software design problems.
This module demonstrates several key patterns in Python.

Patterns Covered:
- Factory Method
- Abstract Factory
- Observer (Publish-Subscribe)
- Strategy
- Adapter
- Composite
- Builder
"""

from abc import ABC, abstractmethod
from typing import Any
import math


# ============================================================
# 1. FACTORY METHOD PATTERN
# ============================================================
class Notification(ABC):
    """Abstract product: a notification that can be sent."""
    
    @abstractmethod
    def send(self, message: str) -> str:
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass


class EmailNotification(Notification):
    def send(self, message: str) -> str:
        return f"[EMAIL] Sending: {message}"

    def get_type(self) -> str:
        return "email"


class SMSNotification(Notification):
    def send(self, message: str) -> str:
        return f"[SMS] Sending: {message}"

    def get_type(self) -> str:
        return "sms"


class PushNotification(Notification):
    def send(self, message: str) -> str:
        return f"[PUSH] Sending: {message}"

    def get_type(self) -> str:
        return "push"


class NotificationFactory:
    """Factory that creates notification objects based on type."""

    _registry: dict[str, type[Notification]] = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    @classmethod
    def create(cls, notification_type: str) -> Notification:
        """Create a notification instance by type name."""
        cls_name = cls._registry.get(notification_type.lower())
        if cls_name is None:
            raise ValueError(f"Unknown notification type: {notification_type}")
        return cls_name()

    @classmethod
    def register_type(cls, name: str, notification_class: type[Notification]):
        """Register a new notification type."""
        cls._registry[name.lower()] = notification_class


# ============================================================
# 2. OBSERVER PATTERN (Publish-Subscribe)
# ============================================================
class Event:
    """Simple event with a name and data payload."""
    def __init__(self, name: str, data: dict | None = None):
        self.name = name
        self.data = data or {}

    def __repr__(self):
        return f"Event({self.name!r}, {self.data})"


class Observer(ABC):
    """Abstract observer that reacts to events."""
    
    @abstractmethod
    def on_event(self, event: Event) -> None:
        pass


class EventBus:
    """Central event bus that manages subscriptions and event dispatch.
    
    Publishers emit events, subscribers receive them — decoupled.
    """
    def __init__(self):
        self._subscribers: dict[str, list[Observer]] = {}

    def subscribe(self, event_name: str, observer: Observer):
        """Subscribe an observer to a specific event."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(observer)
        print(f"  Subscribed {type(observer).__name__} to '{event_name}'")

    def unsubscribe(self, event_name: str, observer: Observer):
        """Remove an observer from an event."""
        if event_name in self._subscribers:
            self._subscribers[event_name].remove(observer)

    def publish(self, event: Event):
        """Publish an event to all subscribers."""
        observers = self._subscribers.get(event.name, [])
        for observer in observers:
            observer.on_event(event)


class Logger(Observer):
    def on_event(self, event: Event) -> None:
        print(f"  [LOG] {event.name}: {event.data}")


class AlertService(Observer):
    def on_event(self, event: Event) -> None:
        if event.data.get("severity") == "high":
            print(f"  [ALERT] Critical event: {event.name}!")


class MetricsCollector(Observer):
    def __init__(self):
        self.event_counts: dict[str, int] = {}

    def on_event(self, event: Event) -> None:
        self.event_counts[event.name] = self.event_counts.get(event.name, 0) + 1


# ============================================================
# 3. STRATEGY PATTERN
# ============================================================
class SortStrategy(ABC):
    """Abstract sorting strategy."""
    
    @abstractmethod
    def sort(self, data: list) -> list:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def name(self) -> str:
        return "Bubble Sort"


class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

    def name(self) -> str:
        return "Quick Sort"


class BuiltInSort(SortStrategy):
    def sort(self, data: list) -> list:
        return sorted(data)

    def name(self) -> str:
        return "Python Built-in Sort"


class Sorter:
    """Context class that uses a pluggable sorting strategy."""

    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data: list) -> list:
        print(f"  Using strategy: {self._strategy.name()}")
        return self._strategy.sort(data)


# ============================================================
# 4. ADAPTER PATTERN
# ============================================================
class OldPaymentGateway:
    """Legacy payment system with an outdated interface."""

    def process_payment(self, amount_cents: int, merchant_id: str) -> dict:
        return {
            "success": True,
            "transaction_id": f"TXN-{merchant_id}-{amount_cents}",
            "charged_cents": amount_cents,
        }


class ModernPaymentInterface(ABC):
    """Modern payment interface that all new gateways must implement."""

    @abstractmethod
    def charge(self, amount: float, currency: str = "USD") -> dict:
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> dict:
        pass


class LegacyGatewayAdapter(ModernPaymentInterface):
    """Adapter that makes the old gateway conform to the new interface."""

    def __init__(self, legacy_gateway: OldPaymentGateway, merchant_id: str):
        self._gateway = legacy_gateway
        self._merchant_id = merchant_id

    def charge(self, amount: float, currency: str = "USD") -> dict:
        amount_cents = int(amount * 100)
        result = self._gateway.process_payment(amount_cents, self._merchant_id)
        return {
            "success": result["success"],
            "transaction_id": result["transaction_id"],
            "amount": amount,
            "currency": currency,
        }

    def refund(self, transaction_id: str) -> dict:
        return {"success": True, "refunded": transaction_id}


# ============================================================
# 5. COMPOSITE PATTERN
# ============================================================
class FileSystemItem(ABC):
    """Abstract component in the file system composite."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> None:
        pass


class File(FileSystemItem):
    """Leaf node: a file with a size."""

    def __init__(self, name: str, size: int):
        super().__init__(name)
        self.size = size

    def get_size(self) -> int:
        return self.size

    def display(self, indent: int = 0) -> None:
        print(f"{'  ' * indent}- {self.name} ({self.size} bytes)")


class Directory(FileSystemItem):
    """Composite node: a directory containing files and subdirectories."""

    def __init__(self, name: str):
        super().__init__(name)
        self.children: list[FileSystemItem] = []

    def add(self, item: FileSystemItem):
        self.children.append(item)

    def remove(self, item: FileSystemItem):
        self.children.remove(item)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)

    def display(self, indent: int = 0) -> None:
        print(f"{'  ' * indent}+ {self.name}/ ({self.get_size()} bytes)")
        for child in self.children:
            child.display(indent + 1)


# ============================================================
# 6. BUILDER PATTERN
# ============================================================
class HttpRequest:
    """Complex object to be built step by step."""

    def __init__(self):
        self.method: str = "GET"
        self.url: str = ""
        self.headers: dict[str, str] = {}
        self.body: Any = None
        self.timeout: int = 30
        self.retries: int = 0

    def __repr__(self) -> str:
        return (
            f"HttpRequest(\n"
            f"  method={self.method},\n"
            f"  url={self.url!r},\n"
            f"  headers={self.headers},\n"
            f"  body={self.body!r},\n"
            f"  timeout={self.timeout},\n"
            f"  retries={self.retries}\n"
            f")"
        )


class HttpRequestBuilder:
    """Builder that constructs HttpRequest objects step by step."""

    def __init__(self):
        self._request = HttpRequest()

    def with_method(self, method: str) -> "HttpRequestBuilder":
        self._request.method = method.upper()
        return self

    def with_url(self, url: str) -> "HttpRequestBuilder":
        self._request.url = url
        return self

    def with_header(self, key: str, value: str) -> "HttpRequestBuilder":
        self._request.headers[key] = value
        return self

    def with_body(self, body: Any) -> "HttpRequestBuilder":
        self._request.body = body
        return self

    def with_timeout(self, seconds: int) -> "HttpRequestBuilder":
        self._request.timeout = seconds
        return self

    def with_retries(self, count: int) -> "HttpRequestBuilder":
        self._request.retries = count
        return self

    def build(self) -> HttpRequest:
        """Validate and return the constructed request."""
        if not self._request.url:
            raise ValueError("URL is required")
        if self._request.method in ("POST", "PUT", "PATCH") and self._request.body is None:
            print("  Warning: POST/PUT/PATCH without body")
        return self._request


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Factory Method")
    for ntype in ["email", "sms", "push"]:
        notification = NotificationFactory.create(ntype)
        print(f"  {notification.send('Hello, World!')}")

    separator("2. Observer Pattern")
    bus = EventBus()
    logger = Logger()
    alerts = AlertService()
    metrics = MetricsCollector()

    bus.subscribe("user.login", logger)
    bus.subscribe("user.login", metrics)
    bus.subscribe("system.error", logger)
    bus.subscribe("system.error", alerts)
    bus.subscribe("system.error", metrics)

    print()
    bus.publish(Event("user.login", {"user": "alice", "ip": "192.168.1.1"}))
    bus.publish(Event("system.error", {"severity": "high", "msg": "Disk full"}))
    bus.publish(Event("system.error", {"severity": "low", "msg": "Slow query"}))
    print(f"\n  Metrics: {metrics.event_counts}")

    separator("3. Strategy Pattern")
    data = [64, 34, 25, 12, 22, 11, 90]
    sorter = Sorter(BubbleSort())
    print(f"  Result: {sorter.sort(data)}")
    sorter.set_strategy(QuickSort())
    print(f"  Result: {sorter.sort(data)}")
    sorter.set_strategy(BuiltInSort())
    print(f"  Result: {sorter.sort(data)}")

    separator("4. Adapter Pattern")
    legacy = OldPaymentGateway()
    adapter = LegacyGatewayAdapter(legacy, merchant_id="SHOP001")
    result = adapter.charge(49.99, "USD")
    print(f"  Charge result: {result}")
    refund = adapter.refund(result["transaction_id"])
    print(f"  Refund result: {refund}")

    separator("5. Composite Pattern")
    root = Directory("project")
    src = Directory("src")
    src.add(File("main.py", 2048))
    src.add(File("utils.py", 1024))
    
    tests = Directory("tests")
    tests.add(File("test_main.py", 512))
    
    root.add(File("README.md", 256))
    root.add(src)
    root.add(tests)
    root.display()

    separator("6. Builder Pattern")
    request = (
        HttpRequestBuilder()
        .with_method("POST")
        .with_url("https://api.example.com/users")
        .with_header("Content-Type", "application/json")
        .with_header("Authorization", "Bearer token123")
        .with_body({"name": "Alice", "email": "alice@example.com"})
        .with_timeout(60)
        .with_retries(3)
        .build()
    )
    print(f"  {request}")


if __name__ == "__main__":
    main()
