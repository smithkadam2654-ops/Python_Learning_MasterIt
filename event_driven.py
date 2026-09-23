"""
Event-Driven Architecture Module

This module provides comprehensive event-driven architecture utilities including:
- Event bus implementation
- Event handlers and subscribers
- Event queuing
- Async event processing
- Event filtering and routing
- Event replay and persistence
- Event aggregation
- Circuit breaker pattern
- Event sourcing
- Dead letter queue

All functions include comprehensive docstrings and type hints.
"""

import time
import json
import threading
import queue
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import hashlib


class EventPriority(Enum):
    """Event priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class EventStatus(Enum):
    """Event processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"


@dataclass
class Event:
    """Event data structure."""
    event_id: str
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime
    priority: EventPriority = EventPriority.NORMAL
    source: Optional[str] = None
    correlation_id: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    status: EventStatus = EventStatus.PENDING
    metadata: Optional[Dict] = None
    
    def __post_init__(self):
        """Generate event ID if not provided."""
        if not self.event_id:
            self.event_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique event ID."""
        timestamp = str(time.time())
        content = f"{self.event_type}{timestamp}{self.data}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict:
        """Convert event to dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority.value,
            "source": self.source,
            "correlation_id": self.correlation_id,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "status": self.status.value,
            "metadata": self.metadata
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Event':
        """Create event from dictionary."""
        return Event(
            event_id=data["event_id"],
            event_type=data["event_type"],
            data=data["data"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            priority=EventPriority(data.get("priority", "normal")),
            source=data.get("source"),
            correlation_id=data.get("correlation_id"),
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            status=EventStatus(data.get("status", "pending")),
            metadata=data.get("metadata")
        )


class EventHandler:
    """Event handler interface."""
    
    def __init__(self, name: str, handler_func: Callable[[Event], Any]):
        """Initialize event handler."""
        self.name = name
        self.handler_func = handler_func
        self.event_types: List[str] = []
        self.enabled = True
        self.execution_count = 0
        self.execution_time = 0.0
    
    def can_handle(self, event: Event) -> bool:
        """Check if handler can handle event."""
        return self.enabled and event.event_type in self.event_types
    
    def handle(self, event: Event) -> Any:
        """Handle event."""
        start_time = time.time()
        
        try:
            result = self.handler_func(event)
            self.execution_count += 1
            self.execution_time += time.time() - start_time
            return result
        except Exception as e:
            raise Exception(f"Handler {self.name} failed: {e}")
    
    def add_event_type(self, event_type: str) -> None:
        """Add event type to handler."""
        if event_type not in self.event_types:
            self.event_types.append(event_type)
    
    def get_stats(self) -> Dict:
        """Get handler statistics."""
        avg_time = self.execution_time / self.execution_count if self.execution_count > 0 else 0
        return {
            "name": self.name,
            "execution_count": self.execution_count,
            "total_time": self.execution_time,
            "average_time": avg_time,
            "enabled": self.enabled
        }


class EventBus:
    """Central event bus for event distribution."""
    
    def __init__(self):
        """Initialize event bus."""
        self.handlers: Dict[str, List[EventHandler]] = {}
        self.lock = threading.RLock()
        self.event_log: List[Event] = []
        self.max_log_size = 1000
    
    def subscribe(self, handler: EventHandler) -> None:
        """Subscribe handler to event types."""
        with self.lock:
            for event_type in handler.event_types:
                if event_type not in self.handlers:
                    self.handlers[event_type] = []
                self.handlers[event_type].append(handler)
    
    def unsubscribe(self, handler: EventHandler) -> None:
        """Unsubscribe handler from all event types."""
        with self.lock:
            for event_type in handler.event_types:
                if event_type in self.handlers:
                    self.handlers[event_type] = [
                        h for h in self.handlers[event_type] if h != handler
                    ]
    
    def publish(self, event: Event) -> int:
        """Publish event to subscribers."""
        with self.lock:
            event.status = EventStatus.PROCESSING
            self._log_event(event)
            
            handlers = self.handlers.get(event.event_type, [])
            handled_count = 0
            
            for handler in handlers:
                if handler.can_handle(event):
                    try:
                        handler.handle(event)
                        handled_count += 1
                    except Exception as e:
                        print(f"Handler error: {e}")
            
            event.status = EventStatus.COMPLETED if handled_count > 0 else EventStatus.FAILED
            return handled_count
    
    def publish_async(self, event: Event) -> None:
        """Publish event asynchronously."""
        def async_publish():
            self.publish(event)
        
        thread = threading.Thread(target=async_publish)
        thread.start()
    
    def _log_event(self, event: Event) -> None:
        """Log event."""
        self.event_log.append(event)
        
        # Maintain log size
        if len(self.event_log) > self.max_log_size:
            self.event_log = self.event_log[-self.max_log_size:]
    
    def get_event_log(self, event_type: Optional[str] = None) -> List[Event]:
        """Get event log."""
        if event_type:
            return [e for e in self.event_log if e.event_type == event_type]
        return self.event_log.copy()
    
    def get_handler_stats(self) -> Dict[str, Dict]:
        """Get statistics for all handlers."""
        stats = {}
        
        with self.lock:
            for event_type, handlers in self.handlers.items():
                for handler in handlers:
                    stats[handler.name] = handler.get_stats()
        
        return stats


class EventQueue:
    """Event queue for processing events."""
    
    def __init__(self, max_size: int = 1000):
        """Initialize event queue."""
        self.queue = queue.PriorityQueue(maxsize=max_size)
        self.priority_map = {
            EventPriority.CRITICAL: 0,
            EventPriority.HIGH: 1,
            EventPriority.NORMAL: 2,
            EventPriority.LOW: 3
        }
    
    def enqueue(self, event: Event) -> bool:
        """Add event to queue."""
        priority = self.priority_map.get(event.priority, 2)
        try:
            self.queue.put((priority, time.time(), event))
            return True
        except queue.Full:
            return False
    
    def dequeue(self, timeout: float = 1.0) -> Optional[Event]:
        """Get event from queue."""
        try:
            priority, timestamp, event = self.queue.get(timeout=timeout)
            return event
        except queue.Empty:
            return None
    
    def size(self) -> int:
        """Get queue size."""
        return self.queue.qsize()
    
    def empty(self) -> bool:
        """Check if queue is empty."""
        return self.queue.empty()


class EventProcessor:
    """Process events from queue."""
    
    def __init__(self, event_queue: EventQueue, event_bus: EventBus):
        """Initialize event processor."""
        self.event_queue = event_queue
        self.event_bus = event_bus
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None
        self.processed_count = 0
        self.failed_count = 0
    
    def start(self) -> None:
        """Start event processor."""
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_loop)
        self.worker_thread.start()
    
    def stop(self) -> None:
        """Stop event processor."""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
    
    def _process_loop(self) -> None:
        """Process events in loop."""
        while self.running:
            event = self.event_queue.dequeue()
            
            if event:
                try:
                    self.event_bus.publish(event)
                    self.processed_count += 1
                except Exception as e:
                    print(f"Processing error: {e}")
                    self.failed_count += 1
                    
                    # Retry logic
                    if event.retry_count < event.max_retries:
                        event.retry_count += 1
                        event.status = EventStatus.RETRY
                        self.event_queue.enqueue(event)
            else:
                time.sleep(0.1)
    
    def get_stats(self) -> Dict:
        """Get processor statistics."""
        return {
            "running": self.running,
            "processed": self.processed_count,
            "failed": self.failed_count,
            "queue_size": self.event_queue.size()
        }


class EventFilter:
    """Filter events based on criteria."""
    
    @staticmethod
    def by_type(event: Event, event_types: List[str]) -> bool:
        """Filter by event type."""
        return event.event_type in event_types
    
    @staticmethod
    def by_priority(event: Event, min_priority: EventPriority) -> bool:
        """Filter by minimum priority."""
        priority_order = {
            EventPriority.CRITICAL: 4,
            EventPriority.HIGH: 3,
            EventPriority.NORMAL: 2,
            EventPriority.LOW: 1
        }
        return priority_order.get(event.priority, 0) >= priority_order.get(min_priority, 0)
    
    @staticmethod
    def by_source(event: Event, sources: List[str]) -> bool:
        """Filter by source."""
        return event.source in sources if event.source else False
    
    @staticmethod
    def by_data(event: Event, key: str, value: Any) -> bool:
        """Filter by data key-value."""
        return event.data.get(key) == value
    
    @staticmethod
    def custom(event: Event, filter_func: Callable[[Event], bool]) -> bool:
        """Custom filter function."""
        return filter_func(event)


class EventRouter:
    """Route events to different handlers based on rules."""
    
    def __init__(self):
        """Initialize event router."""
        self.routes: List[Tuple[Callable[[Event], bool], EventHandler]] = []
    
    def add_route(self, filter_func: Callable[[Event], bool], 
                  handler: EventHandler) -> None:
        """Add routing rule."""
        self.routes.append((filter_func, handler))
    
    def route(self, event: Event) -> List[EventHandler]:
        """Find matching handlers for event."""
        matching_handlers = []
        
        for filter_func, handler in self.routes:
            if filter_func(event):
                matching_handlers.append(handler)
        
        return matching_handlers


class EventAggregator:
    """Aggregate multiple events into single event."""
    
    def __init__(self, event_type: str, window_size: int = 10, timeout: float = 5.0):
        """Initialize event aggregator."""
        self.event_type = event_type
        self.window_size = window_size
        self.timeout = timeout
        self.events: List[Event] = []
        self.lock = threading.Lock()
    
    def add_event(self, event: Event) -> Optional[Event]:
        """Add event to aggregator."""
        if event.event_type != self.event_type:
            return None
        
        with self.lock:
            self.events.append(event)
            
            if len(self.events) >= self.window_size:
                return self._aggregate()
        
        return None
    
    def _aggregate(self) -> Event:
        """Aggregate events into single event."""
        aggregated_data = {
            "count": len(self.events),
            "events": [e.data for e in self.events]
        }
        
        aggregated_event = Event(
            event_id="",
            event_type=f"{self.event_type}_aggregated",
            data=aggregated_data,
            timestamp=datetime.now()
        )
        
        self.events.clear()
        return aggregated_event


class CircuitBreaker:
    """Circuit breaker pattern for event processing."""
    
    def __init__(self, failure_threshold: int = 5, 
                 timeout: float = 60.0):
        """Initialize circuit breaker."""
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
        self.lock = threading.Lock()
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker."""
        with self.lock:
            if self.state == "open":
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = "half-open"
                else:
                    raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            
            with self.lock:
                if self.state == "half-open":
                    self.state = "closed"
                    self.failure_count = 0
            
            return result
        except Exception as e:
            with self.lock:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "open"
            
            raise e
    
    def get_state(self) -> Dict:
        """Get circuit breaker state."""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "last_failure_time": self.last_failure_time
        }


class EventStore:
    """Event sourcing - store and replay events."""
    
    def __init__(self, storage_path: str = "events.json"):
        """Initialize event store."""
        self.storage_path = storage_path
        self.events: List[Event] = []
        self.load_events()
    
    def store(self, event: Event) -> bool:
        """Store event."""
        self.events.append(event)
        return self._save_events()
    
    def load_events(self) -> List[Event]:
        """Load events from storage."""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                self.events = [Event.from_dict(e) for e in data]
        except FileNotFoundError:
            self.events = []
        
        return self.events
    
    def _save_events(self) -> bool:
        """Save events to storage."""
        try:
            with open(self.storage_path, 'w') as f:
                data = [e.to_dict() for e in self.events]
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False
    
    def get_events(self, event_type: Optional[str] = None,
                   start_time: Optional[datetime] = None,
                   end_time: Optional[datetime] = None) -> List[Event]:
        """Get events with filters."""
        events = self.events
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
        
        return events
    
    def replay(self, handler: Callable, event_type: Optional[str] = None) -> int:
        """Replay events to handler."""
        events = self.get_events(event_type)
        
        for event in events:
            try:
                handler(event)
            except Exception as e:
                print(f"Replay error: {e}")
        
        return len(events)


class DeadLetterQueue:
    """Dead letter queue for failed events."""
    
    def __init__(self, max_size: int = 100):
        """Initialize dead letter queue."""
        self.queue: List[Event] = []
        self.max_size = max_size
        self.lock = threading.Lock()
    
    def add(self, event: Event, error: str) -> bool:
        """Add failed event to DLQ."""
        with self.lock:
            if len(self.queue) >= self.max_size:
                return False
            
            event.metadata = event.metadata or {}
            event.metadata["error"] = error
            event.metadata["failed_at"] = datetime.now().isoformat()
            
            self.queue.append(event)
            return True
    
    def get(self) -> Optional[Event]:
        """Get event from DLQ."""
        with self.lock:
            if self.queue:
                return self.queue.pop(0)
            return None
    
    def size(self) -> int:
        """Get DLQ size."""
        return len(self.queue)
    
    def clear(self) -> None:
        """Clear DLQ."""
        with self.lock:
            self.queue.clear()


def demonstrate_event_driven():
    """Demonstrate event-driven architecture functionality."""
    print("=== Event-Driven Architecture Demonstration ===\n")
    
    # Event Bus
    print("1. Event Bus:")
    event_bus = EventBus()
    
    def user_created_handler(event: Event):
        print(f"   User created: {event.data}")
    
    def user_updated_handler(event: Event):
        print(f"   User updated: {event.data}")
    
    handler1 = EventHandler("user_created", user_created_handler)
    handler1.add_event_type("user.created")
    
    handler2 = EventHandler("user_updated", user_updated_handler)
    handler2.add_event_type("user.updated")
    
    event_bus.subscribe(handler1)
    event_bus.subscribe(handler2)
    
    event1 = Event("", "user.created", {"user_id": 1, "name": "John"}, datetime.now())
    event2 = Event("", "user.updated", {"user_id": 1, "name": "Jane"}, datetime.now())
    
    event_bus.publish(event1)
    event_bus.publish(event2)
    
    # Event Queue
    print("\n2. Event Queue:")
    event_queue = EventQueue(max_size=10)
    
    event_queue.enqueue(event1)
    event_queue.enqueue(event2)
    
    print(f"   Queue size: {event_queue.size()}")
    
    dequeued = event_queue.dequeue()
    print(f"   Dequeued: {dequeued.event_type if dequeued else 'None'}")
    
    # Event Processor
    print("\n3. Event Processor:")
    processor = EventProcessor(event_queue, event_bus)
    processor.start()
    
    time.sleep(0.5)
    
    stats = processor.get_stats()
    print(f"   Stats: {stats}")
    
    processor.stop()
    
    # Event Filter
    print("\n4. Event Filter:")
    critical_event = Event("", "alert", {"level": "critical"}, datetime.now(), EventPriority.CRITICAL)
    
    passes = EventFilter.by_priority(critical_event, EventPriority.HIGH)
    print(f"   Critical passes high filter: {passes}")
    
    # Event Router
    print("\n5. Event Router:")
    router = EventRouter()
    
    def alert_handler(event: Event):
        print(f"   Alert handled: {event.data}")
    
    alert_handler_obj = EventHandler("alert", alert_handler)
    alert_handler_obj.add_event_type("alert")
    
    router.add_route(lambda e: e.event_type == "alert", alert_handler_obj)
    
    routed = router.route(critical_event)
    print(f"   Routed handlers: {len(routed)}")
    
    # Event Aggregator
    print("\n6. Event Aggregator:")
    aggregator = EventAggregator("metric", window_size=3)
    
    for i in range(3):
        metric_event = Event("", "metric", {"value": i}, datetime.now())
        result = aggregator.add_event(metric_event)
    
    print(f"   Aggregated events: {len(aggregator.events)}")
    
    # Circuit Breaker
    print("\n7. Circuit Breaker:")
    circuit_breaker = CircuitBreaker(failure_threshold=2, timeout=1.0)
    
    def failing_function():
        raise Exception("Simulated failure")
    
    try:
        circuit_breaker.execute(failing_function)
    except:
        pass
    
    try:
        circuit_breaker.execute(failing_function)
    except:
        pass
    
    state = circuit_breaker.get_state()
    print(f"   Circuit breaker state: {state}")
    
    # Event Store
    print("\n8. Event Store:")
    event_store = EventStore("test_events.json")
    
    event_store.store(event1)
    event_store.store(event2)
    
    stored_events = event_store.get_events()
    print(f"   Stored events: {len(stored_events)}")
    
    # Dead Letter Queue
    print("\n9. Dead Letter Queue:")
    dlq = DeadLetterQueue(max_size=5)
    
    failed_event = Event("", "error", {"message": "test"}, datetime.now())
    dlq.add(failed_event, "Processing failed")
    
    print(f"   DLQ size: {dlq.size()}")
    
    # Event Stats
    print("\n10. Event Statistics:")
    handler_stats = event_bus.get_handler_stats()
    print(f"   Handler stats: {list(handler_stats.keys())}")
    
    # Cleanup
    import os
    if os.path.exists("test_events.json"):
        os.remove("test_events.json")
    
    print("\n11. Cleanup complete")
    
    print("\n=== Demonstration Complete ===")
    print("\nEvent-Driven Architecture Best Practices:")
    print("- Use event-driven architecture for loose coupling")
    print("- Implement proper error handling and retry logic")
    print("- Use circuit breakers to prevent cascading failures")
    print("- Monitor event processing performance")
    print("- Use dead letter queues for failed events")
    print("- Implement event replay for debugging")
    print("- Use appropriate event priority levels")
    print("- Aggregate events when appropriate")
    print("- Keep event schemas simple and versioned")
    print("- Consider event ordering requirements")
    print("- Use correlation IDs for tracking event chains")


if __name__ == "__main__":
    demonstrate_event_driven()