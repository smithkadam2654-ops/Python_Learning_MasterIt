"""
Event System - Event-driven architecture with pub/sub pattern.
Features: Event bus, subscribers, and event handling.
"""

from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import threading
import queue


@dataclass
class Event:
    """Base event class."""
    name: str
    data: Any = None
    timestamp: datetime = None
    source: str = ""
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class EventBus:
    """Event bus for publishing and subscribing to events."""
    
    def __init__(self) -> None:
        """Initialize event bus."""
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_queue: queue.Queue = queue.Queue()
        self._running = False
        self._thread: Optional[threading.Thread] = None
    
    def subscribe(self, event_name: str, handler: Callable) -> None:
        """
        Subscribe to an event.
        
        Args:
            event_name: Name of the event to subscribe to
            handler: Function to call when event is published
        """
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)
    
    def unsubscribe(self, event_name: str, handler: Callable) -> bool:
        """
        Unsubscribe from an event.
        
        Args:
            event_name: Name of the event to unsubscribe from
            handler: Handler function to remove
            
        Returns:
            True if handler was removed, False otherwise
        """
        if event_name in self._subscribers:
            if handler in self._subscribers[event_name]:
                self._subscribers[event_name].remove(handler)
                return True
        return False
    
    def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event: Event to publish
        """
        self._event_queue.put(event)
    
    def publish_sync(self, event: Event) -> None:
        """
        Publish an event synchronously.
        
        Args:
            event: Event to publish
        """
        self._dispatch_event(event)
    
    def _dispatch_event(self, event: Event) -> None:
        """Dispatch event to all subscribers."""
        if event.name in self._subscribers:
            for handler in self._subscribers[event.name]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in event handler for {event.name}: {e}")
    
    def start(self) -> None:
        """Start the event processing thread."""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._process_events, daemon=True)
            self._thread.start()
    
    def stop(self) -> None:
        """Stop the event processing thread."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
    
    def _process_events(self) -> None:
        """Process events from the queue."""
        while self._running:
            try:
                event = self._event_queue.get(timeout=0.1)
                self._dispatch_event(event)
            except queue.Empty:
                continue
    
    def get_subscriber_count(self, event_name: str) -> int:
        """Get number of subscribers for an event."""
        return len(self._subscribers.get(event_name, []))
    
    def clear_subscribers(self, event_name: Optional[str] = None) -> None:
        """Clear subscribers for an event or all events."""
        if event_name:
            self._subscribers.pop(event_name, None)
        else:
            self._subscribers.clear()


class EventEmitter:
    """Mixin class for objects that can emit events."""
    
    def __init__(self):
        """Initialize event emitter."""
        self._event_bus: Optional[EventBus] = None
        self._event_prefix = ""
    
    def set_event_bus(self, event_bus: EventBus) -> None:
        """Set the event bus for this emitter."""
        self._event_bus = event_bus
    
    def set_event_prefix(self, prefix: str) -> None:
        """Set prefix for event names."""
        self._event_prefix = prefix
    
    def emit(self, event_name: str, data: Any = None) -> None:
        """Emit an event."""
        if self._event_bus:
            full_name = f"{self._event_prefix}.{event_name}" if self._event_prefix else event_name
            event = Event(name=full_name, data=data, source=self.__class__.__name__)
            self._event_bus.publish(event)
    
    def emit_sync(self, event_name: str, data: Any = None) -> None:
        """Emit an event synchronously."""
        if self._event_bus:
            full_name = f"{self._event_prefix}.{event_name}" if self._event_prefix else event_name
            event = Event(name=full_name, data=data, source=self.__class__.__name__)
            self._event_bus.publish_sync(event)


class EventHistory:
    """Track event history for debugging."""
    
    def __init__(self, max_size: int = 1000) -> None:
        """
        Initialize event history.
        
        Args:
            max_size: Maximum number of events to store
        """
        self._events: List[Event] = []
        self._max_size = max_size
    
    def record(self, event: Event) -> None:
        """Record an event."""
        self._events.append(event)
        if len(self._events) > self._max_size:
            self._events.pop(0)
    
    def get_events(self, event_name: Optional[str] = None, limit: int = 100) -> List[Event]:
        """Get events from history."""
        events = self._events
        if event_name:
            events = [e for e in events if e.name == event_name]
        return events[-limit:]
    
    def clear(self) -> None:
        """Clear event history."""
        self._events.clear()
    
    def get_count(self, event_name: Optional[str] = None) -> int:
        """Get count of events."""
        if event_name:
            return len([e for e in self._events if e.name == event_name])
        return len(self._events)


def main() -> None:
    """Demonstrate event system."""
    
    print("=== Basic Event Bus ===")
    bus = EventBus()
    
    # Define event handlers
    def on_user_created(event: Event):
        print(f"User created: {event.data}")
    
    def on_user_deleted(event: Event):
        print(f"User deleted: {event.data}")
    
    # Subscribe to events
    bus.subscribe("user.created", on_user_created)
    bus.subscribe("user.deleted", on_user_deleted)
    
    # Publish events
    bus.publish_sync(Event("user.created", data={"name": "Alice", "id": 1}))
    bus.publish_sync(Event("user.deleted", data={"name": "Bob", "id": 2}))
    
    print(f"\nSubscriber count for user.created: {bus.get_subscriber_count('user.created')}")
    
    print("\n=== Asynchronous Event Processing ===")
    async_bus = EventBus()
    
    def on_message(event: Event):
        print(f"Received message: {event.data}")
    
    def on_error(event: Event):
        print(f"Error occurred: {event.data}")
    
    async_bus.subscribe("message", on_message)
    async_bus.subscribe("error", on_error)
    
    async_bus.start()
    
    # Publish multiple events
    for i in range(3):
        async_bus.publish(Event("message", data=f"Message {i}"))
    
    async_bus.publish(Event("error", data="Something went wrong"))
    
    # Wait for processing
    import time
    time.sleep(0.5)
    
    async_bus.stop()
    
    print("\n=== Event Emitter ===")
    bus = EventBus()
    
    class User:
        def __init__(self, name: str):
            self.name = name
        
        def save(self):
            self.emit("saved", {"name": self.name})
    
    # Mix in EventEmitter
    User.__bases__ = (EventEmitter,) + User.__bases__
    
    def on_user_saved(event: Event):
        print(f"User saved event: {event.data}")
    
    bus.subscribe("saved", on_user_saved)
    
    user = User("Charlie")
    user.set_event_bus(bus)
    user.save()
    
    print("\n=== Event History ===")
    history = EventHistory(max_size=10)
    
    for i in range(5):
        event = Event("test", data=i)
        history.record(event)
    
    print(f"Total events: {history.get_count()}")
    print(f"Test events: {history.get_count('test')}")
    
    for event in history.get_events("test"):
        print(f"  Event: {event.name}, Data: {event.data}")


if __name__ == "__main__":
    main()
