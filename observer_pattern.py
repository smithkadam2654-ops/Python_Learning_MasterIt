"""
Observer Pattern - Implementation of the Observer design pattern.
Features: Subject-observer relationship, event notification, and decoupled communication.
"""

from typing import List, Callable, Any, Dict
from abc import ABC, abstractmethod
from dataclasses import dataclass
import threading


class Observer(ABC):
    """Observer interface."""
    
    @abstractmethod
    def update(self, subject: 'Subject', data: Any = None) -> None:
        """Receive update from subject."""
        pass


class Subject(ABC):
    """Subject interface."""
    
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        pass
    
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        pass
    
    @abstractmethod
    def notify(self, data: Any = None) -> None:
        """Notify all observers."""
        pass


class ConcreteSubject(Subject):
    """Concrete subject implementation."""
    
    def __init__(self) -> None:
        """Initialize subject."""
        self._observers: List[Observer] = []
        self._state: Any = None
        self._lock = threading.RLock()
    
    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)
    
    def notify(self, data: Any = None) -> None:
        """Notify all observers."""
        with self._lock:
            for observer in self._observers:
                observer.update(self, data)
    
    def get_state(self) -> Any:
        """Get current state."""
        return self._state
    
    def set_state(self, state: Any) -> None:
        """Set state and notify observers."""
        self._state = state
        self.notify(state)


class EventChannel:
    """Event channel for pub-sub pattern."""
    
    def __init__(self) -> None:
        """Initialize event channel."""
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.RLock()
    
    def subscribe(self, event: str, callback: Callable) -> None:
        """
        Subscribe to an event.
        
        Args:
            event: Event name
            callback: Function to call when event is published
        """
        with self._lock:
            if event not in self._subscribers:
                self._subscribers[event] = []
            self._subscribers[event].append(callback)
    
    def unsubscribe(self, event: str, callback: Callable) -> None:
        """
        Unsubscribe from an event.
        
        Args:
            event: Event name
            callback: Function to remove
        """
        with self._lock:
            if event in self._subscribers and callback in self._subscribers[event]:
                self._subscribers[event].remove(callback)
    
    def publish(self, event: str, data: Any = None) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event: Event name
            data: Data to pass to subscribers
        """
        with self._lock:
            if event in self._subscribers:
                for callback in self._subscribers[event]:
                    try:
                        callback(data)
                    except Exception as e:
                        print(f"Error in callback for {event}: {e}")
    
    def get_subscriber_count(self, event: str) -> int:
        """Get number of subscribers for an event."""
        with self._lock:
            return len(self._subscribers.get(event, []))


class NewsAgency(ConcreteSubject):
    """News agency that publishes news."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize news agency.
        
        Args:
            name: Agency name
        """
        super().__init__()
        self.name = name
    
    def publish_news(self, news: str) -> None:
        """
        Publish news article.
        
        Args:
            news: News content
        """
        print(f"\n{self.name} publishes: {news}")
        self.set_state(news)


class NewsSubscriber(Observer):
    """News subscriber."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize subscriber.
        
        Args:
            name: Subscriber name
        """
        self.name = name
        self.news_history: List[str] = []
    
    def update(self, subject: Subject, data: Any = None) -> None:
        """Receive news update."""
        if isinstance(subject, NewsAgency):
            news = data
            self.news_history.append(news)
            print(f"{self.name} received: {news}")


class StockMarket(ConcreteSubject):
    """Stock market that notifies of price changes."""
    
    def __init__(self) -> None:
        """Initialize stock market."""
        super().__init__()
        self._prices: Dict[str, float] = {}
    
    def update_price(self, symbol: str, price: float) -> None:
        """
        Update stock price.
        
        Args:
            symbol: Stock symbol
            price: New price
        """
        old_price = self._prices.get(symbol)
        self._prices[symbol] = price
        
        print(f"\nStock update: {symbol} = ${price:.2f}")
        
        if old_price is not None:
            change = price - old_price
            self.notify({"symbol": symbol, "price": price, "change": change})
        else:
            self.notify({"symbol": symbol, "price": price, "change": 0.0})
    
    def get_price(self, symbol: str) -> Optional[float]:
        """Get current stock price."""
        return self._prices.get(symbol)


class StockTrader(Observer):
    """Stock trader that reacts to price changes."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize trader.
        
        Args:
            name: Trader name
        """
        self.name = name
        self.portfolio: Dict[str, int] = {}
    
    def update(self, subject: Subject, data: Any = None) -> None:
        """React to price change."""
        if isinstance(subject, StockMarket) and data:
            symbol = data["symbol"]
            price = data["price"]
            change = data["change"]
            
            if change > 0:
                print(f"{self.name}: {symbol} went up ${change:.2f} - considering buy")
            else:
                print(f"{self.name}: {symbol} went down ${abs(change):.2f} - considering sell")


class WeatherStation(ConcreteSubject):
    """Weather station that reports weather changes."""
    
    def __init__(self) -> None:
        """Initialize weather station."""
        super().__init__()
        self._temperature = 0.0
        self._humidity = 0
        self._pressure = 0.0
    
    def set_measurements(self, temperature: float, humidity: int, pressure: float) -> None:
        """
        Update weather measurements.
        
        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            pressure: Pressure in hPa
        """
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        
        print(f"\nWeather update: {temperature}°C, {humidity}% humidity, {pressure} hPa")
        self.notify({
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure
        })
    
    def get_measurements(self) -> Dict[str, Any]:
        """Get current measurements."""
        return {
            "temperature": self._temperature,
            "humidity": self._humidity,
            "pressure": self._pressure
        }


class WeatherDisplay(Observer):
    """Weather display device."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize display.
        
        Args:
            name: Display name
        """
        self.name = name
    
    def update(self, subject: Subject, data: Any = None) -> None:
        """Update display with new weather data."""
        if isinstance(subject, WeatherStation) and data:
            temp = data["temperature"]
            humidity = data["humidity"]
            pressure = data["pressure"]
            
            print(f"{self.name}: Current conditions - {temp}°C, {humidity}% humidity, {pressure} hPa")


class SmartHome:
    """Smart home system using event channel."""
    
    def __init__(self) -> None:
        """Initialize smart home."""
        self.events = EventChannel()
        self._setup_events()
    
    def _setup_events(self) -> None:
        """Set up event subscriptions."""
        self.events.subscribe("motion_detected", self._on_motion)
        self.events.subscribe("door_opened", self._on_door_open)
        self.events.subscribe("temperature_change", self._on_temperature_change)
    
    def _on_motion(self, data: Any) -> None:
        """Handle motion detection."""
        room = data.get("room", "unknown")
        print(f"💡 Motion detected in {room} - turning on lights")
    
    def _on_door_open(self, data: Any) -> None:
        """Handle door opening."""
        door = data.get("door", "unknown")
        print(f"🚪 {door} opened - logging entry")
    
    def _on_temperature_change(self, data: Any) -> None:
        """Handle temperature change."""
        temp = data.get("temperature", 0)
        if temp > 25:
            print(f"❄️ Temperature {temp}°C - turning on AC")
        elif temp < 18:
            print(f"🔥 Temperature {temp}°C - turning on heater")
    
    def detect_motion(self, room: str) -> None:
        """Report motion detection."""
        self.events.publish("motion_detected", {"room": room})
    
    def open_door(self, door: str) -> None:
        """Report door opening."""
        self.events.publish("door_opened", {"door": door})
    
    def change_temperature(self, temperature: float) -> None:
        """Report temperature change."""
        self.events.publish("temperature_change", {"temperature": temperature})


def main() -> None:
    """Demonstrate observer pattern implementations."""
    
    print("=== News Agency ===")
    agency = NewsAgency("Breaking News")
    
    alice = NewsSubscriber("Alice")
    bob = NewsSubscriber("Bob")
    
    agency.attach(alice)
    agency.attach(bob)
    
    agency.publish_news("Python 4.0 Released!")
    agency.publish_news("New AI Breakthrough")
    
    agency.detach(bob)
    agency.publish_news("Final News Update")
    
    print(f"\nAlice's news history: {alice.news_history}")
    
    print("\n=== Stock Market ===")
    market = StockMarket()
    
    trader1 = StockTrader("Trader Joe")
    trader2 = StockTrader("Trader Jane")
    
    market.attach(trader1)
    market.attach(trader2)
    
    market.update_price("AAPL", 150.0)
    market.update_price("AAPL", 152.5)
    market.update_price("AAPL", 151.0)
    
    print(f"\nAAPL current price: ${market.get_price('AAPL'):.2f}")
    
    print("\n=== Weather Station ===")
    station = WeatherStation()
    
    display1 = WeatherDisplay("Living Room Display")
    display2 = WeatherDisplay("Mobile App")
    
    station.attach(display1)
    station.attach(display2)
    
    station.set_measurements(22.5, 65, 1013)
    station.set_measurements(24.0, 60, 1010)
    
    print("\n=== Smart Home ===")
    home = SmartHome()
    
    home.detect_motion("living room")
    home.open_door("front door")
    home.change_temperature(26.0)
    home.change_temperature(17.0)
    
    print(f"\nEvent subscribers for motion_detected: {home.events.get_subscriber_count('motion_detected')}")


if __name__ == "__main__":
    main()
