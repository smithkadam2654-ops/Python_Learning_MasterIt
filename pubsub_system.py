import threading
import queue
import time
from typing import Callable, Dict, List, Any

class EventBus:
    """A simple thread-safe publish-subscribe event bus."""
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.RLock()
        self._event_queue = queue.Queue()
        
        # Start the dispatch thread
        self._dispatch_thread = threading.Thread(target=self._dispatch_loop, daemon=True)
        self._dispatch_thread.start()

    def subscribe(self, event_type: str, callback: Callable[[Any], None]):
        """Subscribe a callback to a specific event type."""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
            print(f"Subscribed {callback.__name__} to '{event_type}'")

    def publish(self, event_type: str, data: Any = None):
        """Publish an event asynchronously."""
        self._event_queue.put((event_type, data))
        
    def _dispatch_loop(self):
        """Continuously processes events from the queue."""
        while True:
            event_type, data = self._event_queue.get()
            with self._lock:
                callbacks = self._subscribers.get(event_type, []).copy()
                
            for callback in callbacks:
                try:
                    # In a production system, these might run in a thread pool
                    # so that slow callbacks don't block the event loop
                    callback(data)
                except Exception as e:
                    print(f"Error in subscriber {callback.__name__}: {e}")
            self._event_queue.task_done()

# --- Example Usage ---

def email_notification_handler(data):
    print(f"[Email Service] Sending welcome email to {data['username']}")
    time.sleep(0.5)

def metrics_handler(data):
    print(f"[Metrics Service] Recording new user registration: {data['username']}")

def main():
    bus = EventBus()
    
    # Register handlers
    bus.subscribe("user_registered", email_notification_handler)
    bus.subscribe("user_registered", metrics_handler)
    
    print("\nSimulating user registrations...")
    bus.publish("user_registered", {"username": "alice", "email": "alice@example.com"})
    bus.publish("user_registered", {"username": "bob", "email": "bob@example.com"})
    
    # Wait for the event queue to drain
    time.sleep(2)
    print("Finished.")

if __name__ == "__main__":
    main()
