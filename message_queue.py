"""
Message Queue Module

This module provides comprehensive message queue utilities including:
- Queue implementation (FIFO, LIFO, priority)
- Message routing
- Topic-based pub/sub
- Dead letter queue
- Message acknowledgment
- Queue monitoring
- Persistent storage
- Consumer groups
- Message filtering
- Queue statistics

All functions include comprehensive docstrings and type hints.
"""

import time
import json
import threading
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum
from collections import deque
import pickle


class QueueType(Enum):
    """Types of message queues."""
    FIFO = "fifo"
    LIFO = "lifo"
    PRIORITY = "priority"


class MessageStatus(Enum):
    """Message processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    ACKNOWLEDGED = "acknowledged"
    FAILED = "failed"
    REQUEUED = "requeued"


@dataclass
class Message:
    """Message data structure."""
    message_id: str
    body: Any
    headers: Dict[str, Any]
    timestamp: float
    priority: int = 0
    status: MessageStatus = MessageStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    metadata: Optional[Dict] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        """Convert message to dictionary."""
        return {
            "message_id": self.message_id,
            "body": self.body,
            "headers": self.headers,
            "timestamp": self.timestamp,
            "priority": self.priority,
            "status": self.status.value,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "metadata": self.metadata
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Message':
        """Create message from dictionary."""
        return Message(
            message_id=data["message_id"],
            body=data["body"],
            headers=data["headers"],
            timestamp=data["timestamp"],
            priority=data.get("priority", 0),
            status=MessageStatus(data.get("status", "pending")),
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            metadata=data.get("metadata")
        )


class MessageQueue:
    """Basic message queue implementation."""
    
    def __init__(self, name: str, queue_type: QueueType = QueueType.FIFO,
                 max_size: int = 1000):
        """Initialize message queue."""
        self.name = name
        self.queue_type = queue_type
        self.max_size = max_size
        self.lock = threading.Lock()
        
        if queue_type == QueueType.FIFO:
            self.queue = deque()
        elif queue_type == QueueType.LIFO:
            self.queue = deque()
        elif queue_type == QueueType.PRIORITY:
            self.queue = []
    
    def enqueue(self, message: Message) -> bool:
        """Add message to queue."""
        with self.lock:
            if len(self.queue) >= self.max_size:
                return False
            
            if self.queue_type == QueueType.PRIORITY:
                # Insert in priority order
                self.queue.append(message)
                self.queue.sort(key=lambda m: m.priority, reverse=True)
            elif self.queue_type == QueueType.LIFO:
                self.queue.appendleft(message)
            else:  # FIFO
                self.queue.append(message)
            
            return True
    
    def dequeue(self) -> Optional[Message]:
        """Remove message from queue."""
        with self.lock:
            if not self.queue:
                return None
            
            if self.queue_type == QueueType.LIFO:
                return self.queue.popleft()
            else:  # FIFO or PRIORITY
                return self.queue.popleft()
    
    def peek(self) -> Optional[Message]:
        """Peek at next message without removing."""
        with self.lock:
            if not self.queue:
                return None
            return self.queue[0]
    
    def size(self) -> int:
        """Get queue size."""
        with self.lock:
            return len(self.queue)
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self.size() == 0
    
    def is_full(self) -> bool:
        """Check if queue is full."""
        return self.size() >= self.max_size
    
    def clear(self) -> None:
        """Clear all messages."""
        with self.lock:
            self.queue.clear()


class Topic:
    """Topic for pub/sub messaging."""
    
    def __init__(self, name: str):
        """Initialize topic."""
        self.name = name
        self.subscribers: List[Callable] = []
        self.lock = threading.Lock()
        self.message_count = 0
    
    def subscribe(self, callback: Callable[[Message], None]) -> None:
        """Subscribe to topic."""
        with self.lock:
            self.subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable[[Message], None]) -> bool:
        """Unsubscribe from topic."""
        with self.lock:
            if callback in self.subscribers:
                self.subscribers.remove(callback)
                return True
            return False
    
    def publish(self, message: Message) -> int:
        """Publish message to topic."""
        with self.lock:
            self.message_count += 1
            subscribers = self.subscribers.copy()
        
        # Notify subscribers
        for callback in subscribers:
            try:
                callback(message)
            except Exception as e:
                print(f"Subscriber error: {e}")
        
        return len(subscribers)
    
    def subscriber_count(self) -> int:
        """Get number of subscribers."""
        with self.lock:
            return len(self.subscribers)


class MessageBroker:
    """Message broker for routing messages."""
    
    def __init__(self):
        """Initialize message broker."""
        self.queues: Dict[str, MessageQueue] = {}
        self.topics: Dict[str, Topic] = {}
        self.lock = threading.Lock()
    
    def create_queue(self, name: str, queue_type: QueueType = QueueType.FIFO,
                     max_size: int = 1000) -> MessageQueue:
        """Create new queue."""
        with self.lock:
            if name not in self.queues:
                self.queues[name] = MessageQueue(name, queue_type, max_size)
            return self.queues[name]
    
    def get_queue(self, name: str) -> Optional[MessageQueue]:
        """Get queue by name."""
        return self.queues.get(name)
    
    def delete_queue(self, name: str) -> bool:
        """Delete queue."""
        with self.lock:
            if name in self.queues:
                del self.queues[name]
                return True
            return False
    
    def create_topic(self, name: str) -> Topic:
        """Create new topic."""
        with self.lock:
            if name not in self.topics:
                self.topics[name] = Topic(name)
            return self.topics[name]
    
    def get_topic(self, name: str) -> Optional[Topic]:
        """Get topic by name."""
        return self.topics.get(name)
    
    def delete_topic(self, name: str) -> bool:
        """Delete topic."""
        with self.lock:
            if name in self.topics:
                del self.topics[name]
                return True
            return False
    
    def route_message(self, message: Message, destination: str,
                     destination_type: str = "queue") -> bool:
        """Route message to destination."""
        if destination_type == "queue":
            queue = self.get_queue(destination)
            if queue:
                return queue.enqueue(message)
        elif destination_type == "topic":
            topic = self.get_topic(destination)
            if topic:
                topic.publish(message)
                return True
        
        return False


class DeadLetterQueue:
    """Dead letter queue for failed messages."""
    
    def __init__(self, name: str = "dlq"):
        """Initialize dead letter queue."""
        self.name = name
        self.queue: List[Message] = []
        self.lock = threading.Lock()
    
    def add(self, message: Message, error: str) -> bool:
        """Add failed message to DLQ."""
        with self.lock:
            message.metadata = message.metadata or {}
            message.metadata["error"] = error
            message.metadata["failed_at"] = time.time()
            message.status = MessageStatus.FAILED
            
            self.queue.append(message)
            return True
    
    def get(self) -> Optional[Message]:
        """Get message from DLQ."""
        with self.lock:
            if self.queue:
                return self.queue.pop(0)
            return None
    
    def size(self) -> int:
        """Get DLQ size."""
        with self.lock:
            return len(self.queue)
    
    def clear(self) -> None:
        """Clear DLQ."""
        with self.lock:
            self.queue.clear()


class MessageConsumer:
    """Message consumer for processing messages."""
    
    def __init__(self, queue: MessageQueue, dlq: Optional[DeadLetterQueue] = None):
        """Initialize consumer."""
        self.queue = queue
        self.dlq = dlq
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None
        self.processed_count = 0
        self.failed_count = 0
        self.callback: Optional[Callable[[Message], bool]] = None
    
    def set_callback(self, callback: Callable[[Message], bool]) -> None:
        """Set message processing callback."""
        self.callback = callback
    
    def start(self) -> None:
        """Start consumer."""
        self.running = True
        self.worker_thread = threading.Thread(target=self._consume_loop)
        self.worker_thread.start()
    
    def stop(self) -> None:
        """Stop consumer."""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
    
    def _consume_loop(self) -> None:
        """Consume messages in loop."""
        while self.running:
            message = self.queue.dequeue()
            
            if message and self.callback:
                try:
                    message.status = MessageStatus.PROCESSING
                    success = self.callback(message)
                    
                    if success:
                        message.status = MessageStatus.ACKNOWLEDGED
                        self.processed_count += 1
                    else:
                        self._handle_failure(message)
                        self.failed_count += 1
                except Exception as e:
                    self._handle_failure(message, str(e))
                    self.failed_count += 1
            else:
                time.sleep(0.1)
    
    def _handle_failure(self, message: Message, error: str = "Processing failed") -> None:
        """Handle failed message."""
        message.retry_count += 1
        
        if message.retry_count < message.max_retries:
            message.status = MessageStatus.REQUEUED
            self.queue.enqueue(message)
        elif self.dlq:
            self.dlq.add(message, error)
        else:
            message.status = MessageStatus.FAILED
    
    def get_stats(self) -> Dict:
        """Get consumer statistics."""
        return {
            "running": self.running,
            "processed": self.processed_count,
            "failed": self.failed_count,
            "queue_size": self.queue.size()
        }


class MessageProducer:
    """Message producer for sending messages."""
    
    def __init__(self, queue: MessageQueue):
        """Initialize producer."""
        self.queue = queue
        self.message_count = 0
    
    def send(self, body: Any, headers: Optional[Dict] = None,
             priority: int = 0) -> bool:
        """Send message to queue."""
        import uuid
        
        message = Message(
            message_id=str(uuid.uuid4()),
            body=body,
            headers=headers or {},
            timestamp=time.time(),
            priority=priority
        )
        
        success = self.queue.enqueue(message)
        if success:
            self.message_count += 1
        
        return success
    
    def send_batch(self, messages: List[Dict]) -> int:
        """Send batch of messages."""
        sent = 0
        
        for msg_data in messages:
            if self.send(
                body=msg_data.get("body"),
                headers=msg_data.get("headers"),
                priority=msg_data.get("priority", 0)
            ):
                sent += 1
        
        return sent


class ConsumerGroup:
    """Consumer group for load balancing."""
    
    def __init__(self, name: str, queue: MessageQueue, num_consumers: int = 3):
        """Initialize consumer group."""
        self.name = name
        self.queue = queue
        self.consumers: List[MessageConsumer] = []
        self.dlq = DeadLetterQueue(f"{name}_dlq")
        
        for i in range(num_consumers):
            consumer = MessageConsumer(queue, self.dlq)
            consumer.name = f"{name}_consumer_{i}"
            self.consumers.append(consumer)
    
    def set_callback(self, callback: Callable[[Message], bool]) -> None:
        """Set callback for all consumers."""
        for consumer in self.consumers:
            consumer.set_callback(callback)
    
    def start(self) -> None:
        """Start all consumers."""
        for consumer in self.consumers:
            consumer.start()
    
    def stop(self) -> None:
        """Stop all consumers."""
        for consumer in self.consumers:
            consumer.stop()
    
    def get_stats(self) -> Dict:
        """Get group statistics."""
        total_processed = sum(c.processed_count for c in self.consumers)
        total_failed = sum(c.failed_count for c in self.consumers)
        
        return {
            "name": self.name,
            "num_consumers": len(self.consumers),
            "total_processed": total_processed,
            "total_failed": total_failed,
            "dlq_size": self.dlq.size()
        }


class MessageFilter:
    """Message filtering utilities."""
    
    @staticmethod
    def by_header(message: Message, header: str, value: Any) -> bool:
        """Filter by header value."""
        return message.headers.get(header) == value
    
    @staticmethod
    def by_priority(message: Message, min_priority: int) -> bool:
        """Filter by minimum priority."""
        return message.priority >= min_priority
    
    @staticmethod
    def by_status(message: Message, status: MessageStatus) -> bool:
        """Filter by status."""
        return message.status == status
    
    @staticmethod
    def custom(message: Message, filter_func: Callable[[Message], bool]) -> bool:
        """Custom filter function."""
        return filter_func(message)


class QueueMonitor:
    """Queue monitoring and statistics."""
    
    def __init__(self, broker: MessageBroker):
        """Initialize monitor."""
        self.broker = broker
        self.metrics: Dict[str, Dict] = {}
    
    def collect_metrics(self) -> Dict:
        """Collect metrics from all queues."""
        metrics = {}
        
        for name, queue in self.broker.queues.items():
            metrics[name] = {
                "size": queue.size(),
                "type": queue.queue_type.value,
                "max_size": queue.max_size,
                "is_empty": queue.is_empty(),
                "is_full": queue.is_full()
            }
        
        for name, topic in self.broker.topics.items():
            metrics[f"topic_{name}"] = {
                "subscribers": topic.subscriber_count(),
                "message_count": topic.message_count
            }
        
        self.metrics = metrics
        return metrics
    
    def get_queue_stats(self, queue_name: str) -> Optional[Dict]:
        """Get statistics for specific queue."""
        queue = self.broker.get_queue(queue_name)
        if queue:
            return {
                "size": queue.size(),
                "type": queue.queue_type.value,
                "max_size": queue.max_size
            }
        return None


class PersistentQueue:
    """Persistent queue with file storage."""
    
    def __init__(self, name: str, storage_path: str = "queue_storage"):
        """Initialize persistent queue."""
        self.name = name
        self.storage_path = storage_path
        self.queue = MessageQueue(name)
        self._load_from_storage()
    
    def _load_from_storage(self) -> None:
        """Load messages from storage."""
        import os
        
        file_path = f"{self.storage_path}/{self.name}.pkl"
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    messages = pickle.load(f)
                    for msg_data in messages:
                        message = Message.from_dict(msg_data)
                        self.queue.enqueue(message)
            except Exception as e:
                print(f"Load error: {e}")
    
    def _save_to_storage(self) -> bool:
        """Save messages to storage."""
        import os
        
        os.makedirs(self.storage_path, exist_ok=True)
        file_path = f"{self.storage_path}/{self.name}.pkl"
        
        try:
            messages = []
            temp_queue = MessageQueue("temp")
            
            while not self.queue.is_empty():
                message = self.queue.dequeue()
                messages.append(message.to_dict())
                temp_queue.enqueue(message)
            
            with open(file_path, 'wb') as f:
                pickle.dump(messages, f)
            
            # Restore queue
            while not temp_queue.is_empty():
                self.queue.enqueue(temp_queue.dequeue())
            
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False
    
    def enqueue(self, message: Message) -> bool:
        """Enqueue with persistence."""
        success = self.queue.enqueue(message)
        if success:
            self._save_to_storage()
        return success
    
    def dequeue(self) -> Optional[Message]:
        """Dequeue with persistence."""
        message = self.queue.dequeue()
        if message:
            self._save_to_storage()
        return message


def demonstrate_message_queue():
    """Demonstrate message queue functionality."""
    print("=== Message Queue Demonstration ===\n")
    
    # Message Queue
    print("1. Message Queue:")
    queue = MessageQueue("test_queue", QueueType.FIFO, max_size=10)
    
    for i in range(5):
        message = Message(
            message_id=f"msg_{i}",
            body=f"Message {i}",
            headers={"type": "test"},
            timestamp=time.time()
        )
        queue.enqueue(message)
    
    print(f"   Queue size: {queue.size()}")
    print(f"   Is full: {queue.is_full()}")
    
    msg = queue.dequeue()
    print(f"   Dequeued: {msg.body if msg else 'None'}")
    
    # Priority Queue
    print("\n2. Priority Queue:")
    priority_queue = MessageQueue("priority_queue", QueueType.PRIORITY)
    
    for i in range(5):
        message = Message(
            message_id=f"msg_{i}",
            body=f"Message {i}",
            headers={},
            timestamp=time.time(),
            priority=i
        )
        priority_queue.enqueue(message)
    
    print(f"   Queue size: {priority_queue.size()}")
    
    # Topic Pub/Sub
    print("\n3. Topic Pub/Sub:")
    topic = Topic("test_topic")
    
    def subscriber1(msg):
        print(f"   Subscriber 1 received: {msg.body}")
    
    def subscriber2(msg):
        print(f"   Subscriber 2 received: {msg.body}")
    
    topic.subscribe(subscriber1)
    topic.subscribe(subscriber2)
    
    message = Message(
        message_id="pub_msg",
        body="Published message",
        headers={},
        timestamp=time.time()
    )
    
    print(f"   Publishing message...")
    topic.publish(message)
    print(f"   Subscriber count: {topic.subscriber_count()}")
    
    # Message Broker
    print("\n4. Message Broker:")
    broker = MessageBroker()
    
    queue1 = broker.create_queue("queue1", QueueType.FIFO)
    queue2 = broker.create_queue("queue2", QueueType.LIFO)
    
    topic1 = broker.create_topic("topic1")
    
    print(f"   Queues: {list(broker.queues.keys())}")
    print(f"   Topics: {list(broker.topics.keys())}")
    
    # Dead Letter Queue
    print("\n5. Dead Letter Queue:")
    dlq = DeadLetterQueue("test_dlq")
    
    failed_message = Message(
        message_id="failed",
        body="Failed message",
        headers={},
        timestamp=time.time()
    )
    
    dlq.add(failed_message, "Simulated failure")
    print(f"   DLQ size: {dlq.size()}")
    
    # Message Consumer
    print("\n6. Message Consumer:")
    test_queue = MessageQueue("consumer_test")
    
    for i in range(3):
        message = Message(
            message_id=f"consumer_msg_{i}",
            body=f"Consumer message {i}",
            headers={},
            timestamp=time.time()
        )
        test_queue.enqueue(message)
    
    def process_message(msg):
        print(f"   Processing: {msg.body}")
        return True
    
    consumer = MessageConsumer(test_queue)
    consumer.set_callback(process_message)
    
    # Process messages synchronously
    for _ in range(3):
        msg = test_queue.dequeue()
        if msg:
            process_message(msg)
    
    stats = consumer.get_stats()
    print(f"   Stats: {stats}")
    
    # Message Producer
    print("\n7. Message Producer:")
    producer = MessageProducer(queue)
    
    producer.send("Hello", {"type": "greeting"}, priority=1)
    producer.send("World", {"type": "greeting"}, priority=2)
    
    print(f"   Messages sent: {producer.message_count}")
    print(f"   Queue size: {queue.size()}")
    
    # Consumer Group
    print("\n8. Consumer Group:")
    group_queue = MessageQueue("group_queue")
    
    for i in range(10):
        message = Message(
            message_id=f"group_msg_{i}",
            body=f"Group message {i}",
            headers={},
            timestamp=time.time()
        )
        group_queue.enqueue(message)
    
    group = ConsumerGroup("test_group", group_queue, num_consumers=2)
    group.set_callback(process_message)
    
    print(f"   Group consumers: {len(group.consumers)}")
    
    # Message Filter
    print("\n9. Message Filter:")
    test_msg = Message(
        message_id="filter_test",
        body="Test message",
        headers={"type": "important", "priority": "high"},
        timestamp=time.time(),
        priority=5
    )
    
    passes = MessageFilter.by_header(test_msg, "type", "important")
    print(f"   Header filter: {passes}")
    
    passes = MessageFilter.by_priority(test_msg, 3)
    print(f"   Priority filter: {passes}")
    
    # Queue Monitor
    print("\n10. Queue Monitor:")
    monitor = QueueMonitor(broker)
    metrics = monitor.collect_metrics()
    
    print(f"   Metrics: {list(metrics.keys())}")
    
    print("\n=== Demonstration Complete ===")
    print("\nMessage Queue Best Practices:")
    print("- Choose appropriate queue type for your use case")
    print("- Use priority queues for important messages")
    print("- Implement dead letter queues for failed messages")
    print("- Use consumer groups for load balancing")
    print("- Monitor queue sizes and consumer lag")
    print("- Use message acknowledgment for reliability")
    print("- Implement retry logic with exponential backoff")
    print("- Use persistent storage for critical messages")
    print("- Consider message ordering requirements")
    print("- Use filters for targeted message routing")
    print("- Implement proper error handling and logging")


if __name__ == "__main__":
    demonstrate_message_queue()
