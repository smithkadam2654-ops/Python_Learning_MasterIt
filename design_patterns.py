"""
Design Patterns - Implementation of common software design patterns.
Features: Singleton, Factory, Observer, Strategy, and Decorator patterns.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import threading


# ==================== SINGLETON PATTERN ====================

class SingletonMeta(type):
    """Metaclass for implementing Singleton pattern."""
    
    _instances: Dict = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    """Singleton database connection class."""
    
    def __init__(self):
        self.connection_string = "postgresql://localhost/mydb"
        self.is_connected = False
    
    def connect(self) -> None:
        """Establish database connection."""
        if not self.is_connected:
            print(f"Connecting to {self.connection_string}...")
            self.is_connected = True
            print("Connected!")
    
    def disconnect(self) -> None:
        """Close database connection."""
        if self.is_connected:
            print("Disconnecting from database...")
            self.is_connected = False


# ==================== FACTORY PATTERN ====================

class PaymentType(Enum):
    """Types of payment methods."""
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"


class PaymentProcessor(ABC):
    """Abstract base class for payment processors."""
    
    @abstractmethod
    def process(self, amount: float) -> bool:
        """Process payment of given amount."""
        pass


class CreditCardProcessor(PaymentProcessor):
    """Credit card payment processor."""
    
    def process(self, amount: float) -> bool:
        print(f"Processing credit card payment of ${amount:.2f}")
        return True


class PayPalProcessor(PaymentProcessor):
    """PayPal payment processor."""
    
    def process(self, amount: float) -> bool:
        print(f"Processing PayPal payment of ${amount:.2f}")
        return True


class BankTransferProcessor(PaymentProcessor):
    """Bank transfer payment processor."""
    
    def process(self, amount: float) -> bool:
        print(f"Processing bank transfer of ${amount:.2f}")
        return True


class PaymentFactory:
    """Factory for creating payment processors."""
    
    @staticmethod
    def create_processor(payment_type: PaymentType) -> PaymentProcessor:
        """Create appropriate payment processor based on type."""
        processors = {
            PaymentType.CREDIT_CARD: CreditCardProcessor(),
            PaymentType.PAYPAL: PayPalProcessor(),
            PaymentType.BANK_TRANSFER: BankTransferProcessor(),
        }
        
        processor = processors.get(payment_type)
        if processor is None:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return processor


# ==================== OBSERVER PATTERN ====================

class Observer(ABC):
    """Observer interface for the Observer pattern."""
    
    @abstractmethod
    def update(self, message: str) -> None:
        """Receive update notification."""
        pass


class Subject(ABC):
    """Subject interface for the Observer pattern."""
    
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Attach an observer to the subject."""
        pass
    
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Detach an observer from the subject."""
        pass
    
    @abstractmethod
    def notify(self, message: str) -> None:
        """Notify all observers of a change."""
        pass


class NewsPublisher(Subject):
    """News publisher that notifies subscribers."""
    
    def __init__(self) -> None:
        self._subscribers: List[Observer] = []
        self._latest_news: str = ""
    
    def attach(self, observer: Observer) -> None:
        """Add a new subscriber."""
        if observer not in self._subscribers:
            self._subscribers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Remove a subscriber."""
        if observer in self._subscribers:
            self._subscribers.remove(observer)
    
    def notify(self, message: str) -> None:
        """Notify all subscribers of new news."""
        for subscriber in self._subscribers:
            subscriber.update(message)
    
    def publish_news(self, news: str) -> None:
        """Publish new news item."""
        self._latest_news = news
        print(f"\nPublishing: {news}")
        self.notify(news)


class EmailSubscriber(Observer):
    """Subscriber that receives news via email."""
    
    def __init__(self, email: str) -> None:
        self.email = email
    
    def update(self, message: str) -> None:
        print(f"Email sent to {self.email}: {message}")


class SMSSubscriber(Observer):
    """Subscriber that receives news via SMS."""
    
    def __init__(self, phone: str) -> None:
        self.phone = phone
    
    def update(self, message: str) -> None:
        print(f"SMS sent to {self.phone}: {message}")


# ==================== STRATEGY PATTERN ====================

class SortingStrategy(ABC):
    """Abstract strategy for sorting algorithms."""
    
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        """Sort the data using the strategy."""
        pass


class BubbleSort(SortingStrategy):
    """Bubble sort strategy."""
    
    def sort(self, data: List[int]) -> List[int]:
        data = data.copy()
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data


class QuickSort(SortingStrategy):
    """Quick sort strategy."""
    
    def sort(self, data: List[int]) -> List[int]:
        data = data.copy()
        
        def quicksort(arr: List[int]) -> List[int]:
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return quicksort(left) + middle + quicksort(right)
        
        return quicksort(data)


class Sorter:
    """Context class that uses sorting strategies."""
    
    def __init__(self, strategy: SortingStrategy) -> None:
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortingStrategy) -> None:
        """Change the sorting strategy."""
        self._strategy = strategy
    
    def sort_data(self, data: List[int]) -> List[int]:
        """Sort data using the current strategy."""
        return self._strategy.sort(data)


# ==================== DECORATOR PATTERN ====================

class TextComponent(ABC):
    """Abstract component for text processing."""
    
    @abstractmethod
    def get_text(self) -> str:
        """Get the processed text."""
        pass


class PlainText(TextComponent):
    """Plain text component."""
    
    def __init__(self, text: str) -> None:
        self._text = text
    
    def get_text(self) -> str:
        return self._text


class TextDecorator(TextComponent):
    """Base decorator for text components."""
    
    def __init__(self, component: TextComponent) -> None:
        self._component = component
    
    def get_text(self) -> str:
        return self._component.get_text()


class BoldDecorator(TextDecorator):
    """Decorator that adds bold formatting."""
    
    def get_text(self) -> str:
        return f"**{self._component.get_text()}**"


class ItalicDecorator(TextDecorator):
    """Decorator that adds italic formatting."""
    
    def get_text(self) -> str:
        return f"*{self._component.get_text()}*"


class UpperCaseDecorator(TextDecorator):
    """Decorator that converts to uppercase."""
    
    def get_text(self) -> str:
        return self._component.get_text().upper()


def main() -> None:
    """Demonstrate design patterns."""
    
    # Singleton Pattern
    print("=== SINGLETON PATTERN ===")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"Same instance: {db1 is db2}")
    db1.connect()
    db2.connect()  # Won't connect again
    
    # Factory Pattern
    print("\n=== FACTORY PATTERN ===")
    credit_processor = PaymentFactory.create_processor(PaymentType.CREDIT_CARD)
    paypal_processor = CreditCardProcessor = PaymentFactory.create_processor(PaymentType.PAYPAL)
    credit_processor.process(100.0)
    paypal_processor.process(50.0)
    
    # Observer Pattern
    print("\n=== OBSERVER PATTERN ===")
    publisher = NewsPublisher()
    
    email_sub = EmailSubscriber("user@example.com")
    sms_sub = SMSSubscriber("+1234567890")
    
    publisher.attach(email_sub)
    publisher.attach(sms_sub)
    
    publisher.publish_news("Breaking: Python 4.0 released!")
    
    publisher.detach(sms_sub)
    publisher.publish_news("Update: Bug fixes in Python 4.0")
    
    # Strategy Pattern
    print("\n=== STRATEGY PATTERN ===")
    data = [64, 34, 25, 12, 22, 11, 90]
    
    sorter = Sorter(BubbleSort())
    print(f"Bubble sort: {sorter.sort_data(data)}")
    
    sorter.set_strategy(QuickSort())
    print(f"Quick sort: {sorter.sort_data(data)}")
    
    # Decorator Pattern
    print("\n=== DECORATOR PATTERN ===")
    text = PlainText("Hello World")
    
    bold_text = BoldDecorator(text)
    italic_bold = ItalicDecorator(bold_text)
    uppercase_italic_bold = UpperCaseDecorator(italic_bold)
    
    print(f"Plain: {text.get_text()}")
    print(f"Bold: {bold_text.get_text()}")
    print(f"Italic Bold: {italic_bold.get_text()}")
    print(f"Uppercase Italic Bold: {uppercase_italic_bold.get_text()}")


if __name__ == "__main__":
    main()
