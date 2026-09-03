"""
Pub-Sub System - Publish-Subscribe messaging system.
Features: Topic-based messaging, subscriber management, and message filtering.
"""

import threading
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3


@dataclass
class Message:
    """Message in pub-sub system."""
    topic: str
    payload: Any
    priority: MessagePriority = MessagePriority.NORMAL
    headers: Dict[str, str] = None
    
    def __post_init__(self):
        if self.headers is None:
            self.headers = {}


class Subscription:
    """Subscription to a topic."""
    
    def __init__(self, topic: str, callback: Callable, filter_func: Optional[Callable] = None) -> None:
        """
        Initialize subscription.
        
        Args:
            topic: Topic to subscribe to
            callback: Function to call when message is published
            filter_func: Optional function to filter messages
        """
        self.topic = topic
        self.callback = callback
        self.filter_func = filter_func
        self.id = id(self)
    
    def matches(self, message: Message) -> bool:
        """
        Check if subscription matches message.
        
        Args:
            message: Message to check
            
        Returns:
            True if message should be delivered to this subscription
        """
        if self.filter_func:
            return self.filter_func(message)
        return True


class Topic:
    """Topic in pub-sub system."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize topic.
        
        Args:
            name: Topic name
        """
        self.name = name
        self.subscriptions: List[Subscription] = []
        self._lock = threading.RLock()
    
    def subscribe(self, subscription: Subscription) -> None:
        """
        Add subscription to topic.
        
        Args:
            subscription: Subscription to add
        """
        with self._lock:
            self.subscriptions.append(subscription)
    
    def unsubscribe(self, subscription_id: int) -> bool:
        """
        Remove subscription from topic.
        
        Args:
            subscription_id: ID of subscription to remove
            
        Returns:
            True if subscription was removed
        """
        with self._lock:
            for i, sub in enumerate(self.subscriptions):
                if sub.id == subscription_id:
                    self.subscriptions.pop(i)
                    return True
        return False
    
    def publish(self, message: Message) -> int:
        """
        Publish message to all matching subscriptions.
        
        Args:
            message: Message to publish
            
        Returns:
            Number of subscriptions that received the message
        """
        delivered_count = 0
        
        with self._lock:
            for subscription in self.subscriptions:
                if subscription.matches(message):
                    try:
                        subscription.callback(message)
                        delivered_count += 1
                    except Exception as e:
                        print(f"Error in subscription callback: {e}")
        
        return delivered_count
    
    def get_subscriber_count(self) -> int:
        """Get number of subscriptions."""
        with self._lock:
            return len(self.subscriptions)


class PubSubSystem:
    """Publish-Subscribe system."""
    
    def __init__(self) -> None:
        """Initialize pub-sub system."""
        self.topics: Dict[str, Topic] = {}
        self._lock = threading.RLock()
    
    def create_topic(self, name: str) -> Topic:
        """
        Create a new topic.
        
        Args:
            name: Topic name
            
        Returns:
            Created topic
        """
        with self._lock:
            if name not in self.topics:
                self.topics[name] = Topic(name)
        return self.topics[name]
    
    def get_topic(self, name: str) -> Optional[Topic]:
        """
        Get topic by name.
        
        Args:
            name: Topic name
            
        Returns:
            Topic or None if not found
        """
        with self._lock:
            return self.topics.get(name)
    
    def subscribe(self, topic_name: str, callback: Callable, 
                filter_func: Optional[Callable] = None) -> Subscription:
        """
        Subscribe to a topic.
        
        Args:
            topic_name: Topic to subscribe to
            callback: Function to call when message is published
            filter_func: Optional function to filter messages
            
        Returns:
            Subscription object
        """
        topic = self.create_topic(topic_name)
        subscription = Subscription(topic_name, callback, filter_func)
        topic.subscribe(subscription)
        return subscription
    
    def unsubscribe(self, subscription_id: int) -> bool:
        """
        Unsubscribe by subscription ID.
        
        Args:
            subscription_id: ID of subscription to remove
            
        Returns:
            True if subscription was removed
        """
        with self._lock:
            for topic in self.topics.values():
                if topic.unsubscribe(subscription_id):
                    return True
        return False
    
    def publish(self, topic_name: str, payload: Any, 
               priority: MessagePriority = MessagePriority.NORMAL,
               headers: Optional[Dict[str, str]] = None) -> int:
        """
        Publish message to topic.
        
        Args:
            topic_name: Topic to publish to
            payload: Message payload
            priority: Message priority
            headers: Optional message headers
            
        Returns:
            Number of subscribers that received the message
        """
        topic = self.get_topic(topic_name)
        if not topic:
            return 0
        
        message = Message(topic_name, payload, priority, headers)
        return topic.publish(message)
    
    def get_topic_count(self) -> int:
        """Get number of topics."""
        with self._lock:
            return len(self.topics)
    
    def get_total_subscriber_count(self) -> int:
        """Get total number of subscriptions across all topics."""
        with self._lock:
            return sum(topic.get_subscriber_count() for topic in self.topics.values())


def main() -> None:
    """Demonstrate pub-sub system."""
    
    print("=== Basic Pub-Sub ===")
    pubsub = PubSubSystem()
    
    # Define subscribers
    def on_news(message: Message):
        print(f"News subscriber received: {message.payload}")
    
    def on_weather(message: Message):
        print(f"Weather subscriber received: {message.payload}")
    
    # Subscribe to topics
    pubsub.subscribe("news", on_news)
    pubsub.subscribe("weather", on_weather)
    
    # Publish messages
    pubsub.publish("news", "Breaking: Python 4.0 Released!")
    pubsub.publish("weather", "Sunny, 25°C")
    
    print(f"\nTotal topics: {pubsub.get_topic_count()}")
    print(f"Total subscribers: {pubsub.get_total_subscriber_count()}")
    
    print("\n=== Message Filtering ===")
    def high_priority_filter(message: Message) -> bool:
        """Filter for high priority messages only."""
        return message.priority == MessagePriority.HIGH
    
    def on_urgent(message: Message):
        print(f"🚨 URGENT: {message.payload}")
    
    # Subscribe with filter
    pubsub.subscribe("alerts", on_urgent, high_priority_filter)
    
    # Publish with different priorities
    pubsub.publish("alerts", "Low priority issue", MessagePriority.LOW)
    pubsub.publish("alerts", "Normal update", MessagePriority.NORMAL)
    pubsub.publish("alerts", "Critical failure!", MessagePriority.HIGH)
    
    print("\n=== Multiple Subscribers ===")
    messages_received = []
    
    def subscriber1(message: Message):
        messages_received.append(f"Sub1: {message.payload}")
    
    def subscriber2(message: Message):
        messages_received.append(f"Sub2: {message.payload}")
    
    def subscriber3(message: Message):
        messages_received.append(f"Sub3: {message.payload}")
    
    pubsub.subscribe("updates", subscriber1)
    pubsub.subscribe("updates", subscriber2)
    pubsub.subscribe("updates", subscriber3)
    
    pubsub.publish("updates", "System update available")
    
    print(f"Messages received: {messages_received}")
    
    print("\n=== Topic Management ===")
    topic = pubsub.get_topic("updates")
    print(f"Updates topic subscribers: {topic.get_subscriber_count()}")
    
    # Unsubscribe one subscriber
    sub = pubsub.subscribe("test", lambda m: None)
    pubsub.unsubscribe(sub.id)
    
    print(f"After unsubscribe: {pubsub.get_total_subscriber_count()}")
    
    print("\n=== Message Headers ===")
    def header_subscriber(message: Message):
        print(f"Headers: {message.headers}")
        print(f"Payload: {message.payload}")
    
    pubsub.subscribe("events", header_subscriber)
    
    pubsub.publish("events", "User logged in", headers={"event_type": "login", "user_id": "123"})


if __name__ == "__main__":
    main()
