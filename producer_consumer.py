"""
Producer-Consumer - Producer-Consumer pattern with thread-safe queue.
Features: Bounded queue, multiple producers/consumers, and graceful shutdown.
"""

import threading
import queue
import time
import random
from typing import Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum


class QueueStatus(Enum):
    """Queue status."""
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


@dataclass
class Task:
    """Task for producer-consumer pattern."""
    id: int
    data: Any
    priority: int = 0
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


class BoundedQueue:
    """Thread-safe bounded queue."""
    
    def __init__(self, max_size: int = 10) -> None:
        """
        Initialize bounded queue.
        
        Args:
            max_size: Maximum queue size
        """
        self.max_size = max_size
        self.queue = queue.PriorityQueue(maxsize=max_size)
        self._lock = threading.RLock()
        self._status = QueueStatus.RUNNING
    
    def put(self, item: Task, timeout: Optional[float] = None) -> bool:
        """
        Put item in queue.
        
        Args:
            item: Item to add
            timeout: Maximum time to wait
            
        Returns:
            True if item was added, False otherwise
        """
        if self._status != QueueStatus.RUNNING:
            return False
        
        try:
            self.queue.put((-item.priority, item.created_at, item), timeout=timeout)
            return True
        except queue.Full:
            return False
    
    def get(self, timeout: Optional[float] = None) -> Optional[Task]:
        """
        Get item from queue.
        
        Args:
            timeout: Maximum time to wait
            
        Returns:
            Item or None if queue is empty
        """
        if self._status != QueueStatus.RUNNING:
            return None
        
        try:
            _, _, item = self.queue.get(timeout=timeout)
            return item
        except queue.Empty:
            return None
    
    def size(self) -> int:
        """Get current queue size."""
        return self.queue.qsize()
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self.queue.empty()
    
    def is_full(self) -> bool:
        """Check if queue is full."""
        return self.queue.full()
    
    def pause(self) -> None:
        """Pause the queue."""
        with self._lock:
            self._status = QueueStatus.PAUSED
    
    def resume(self) -> None:
        """Resume the queue."""
        with self._lock:
            self._status = QueueStatus.RUNNING
    
    def stop(self) -> None:
        """Stop the queue."""
        with self._lock:
            self._status = QueueStatus.STOPPED
    
    def get_status(self) -> QueueStatus:
        """Get queue status."""
        return self._status


class Producer(threading.Thread):
    """Producer thread."""
    
    def __init__(self, queue: BoundedQueue, producer_id: int, 
                 produce_rate: float = 1.0) -> None:
        """
        Initialize producer.
        
        Args:
            queue: Queue to produce to
            producer_id: Producer identifier
            produce_rate: Items per second
        """
        super().__init__(daemon=True)
        self.queue = queue
        self.producer_id = producer_id
        self.produce_rate = produce_rate
        self.running = True
        self.items_produced = 0
    
    def run(self) -> None:
        """Main producer loop."""
        task_id = 0
        
        while self.running:
            # Check queue status
            if self.queue.get_status() == QueueStatus.STOPPED:
                break
            
            # Wait based on produce rate
            time.sleep(1.0 / self.produce_rate)
            
            # Create task
            task = Task(
                id=task_id,
                data=f"Item from Producer {self.producer_id}",
                priority=random.randint(0, 5)
            )
            task_id += 1
            
            # Try to put in queue
            if self.queue.put(task, timeout=0.1):
                self.items_produced += 1
                print(f"Producer {self.producer_id}: Produced Task {task.id}")
            else:
                print(f"Producer {self.producer_id}: Queue full, waiting...")
    
    def stop(self) -> None:
        """Stop the producer."""
        self.running = False


class Consumer(threading.Thread):
    """Consumer thread."""
    
    def __init__(self, queue: BoundedQueue, consumer_id: int, 
                 consume_rate: float = 1.0) -> None:
        """
        Initialize consumer.
        
        Args:
            queue: Queue to consume from
            consumer_id: Consumer identifier
            consume_rate: Items per second
        """
        super().__init__(daemon=True)
        self.queue = queue
        self.consumer_id = consumer_id
        self.consume_rate = consume_rate
        self.running = True
        self.items_consumed = 0
    
    def run(self) -> None:
        """Main consumer loop."""
        while self.running:
            # Check queue status
            if self.queue.get_status() == QueueStatus.STOPPED:
                if self.queue.is_empty():
                    break
            
            # Wait based on consume rate
            time.sleep(1.0 / self.consume_rate)
            
            # Try to get from queue
            task = self.queue.get(timeout=0.1)
            
            if task:
                self.items_consumed += 1
                print(f"Consumer {self.consumer_id}: Consumed Task {task.id} (priority {task.priority})")
                
                # Simulate processing
                time.sleep(0.1)
    
    def stop(self) -> None:
        """Stop the consumer."""
        self.running = False


class ProducerConsumerSystem:
    """Producer-Consumer system manager."""
    
    def __init__(self, queue_size: int = 10, num_producers: int = 2, 
                 num_consumers: int = 2) -> None:
        """
        Initialize producer-consumer system.
        
        Args:
            queue_size: Maximum queue size
            num_producers: Number of producer threads
            num_consumers: Number of consumer threads
        """
        self.queue = BoundedQueue(queue_size)
        self.producers: List[Producer] = []
        self.consumers: List[Consumer] = []
        
        for i in range(num_producers):
            producer = Producer(self.queue, i, produce_rate=2.0)
            self.producers.append(producer)
        
        for i in range(num_consumers):
            consumer = Consumer(self.queue, i, consume_rate=1.5)
            self.consumers.append(consumer)
    
    def start(self) -> None:
        """Start all producers and consumers."""
        for producer in self.producers:
            producer.start()
        
        for consumer in self.consumers:
            consumer.start()
    
    def stop(self) -> None:
        """Stop all producers and consumers."""
        self.queue.stop()
        
        for producer in self.producers:
            producer.stop()
        
        for consumer in self.consumers:
            consumer.stop()
        
        # Wait for threads to finish
        for producer in self.producers:
            producer.join(timeout=1.0)
        
        for consumer in self.consumers:
            consumer.join(timeout=1.0)
    
    def get_stats(self) -> dict:
        """Get system statistics."""
        return {
            "queue_size": self.queue.size(),
            "queue_status": self.queue.get_status().value,
            "total_produced": sum(p.items_produced for p in self.producers),
            "total_consumed": sum(c.items_consumed for c in self.consumers),
        }


class WorkProcessor:
    """Example work processor for consumer."""
    
    @staticmethod
    def process_task(task: Task) -> str:
        """
        Process a task.
        
        Args:
            task: Task to process
            
        Returns:
            Processing result
        """
        time.sleep(0.2)  # Simulate work
        return f"Processed: {task.data}"


def main() -> None:
    """Demonstrate producer-consumer pattern."""
    
    print("=== Basic Producer-Consumer ===")
    system = ProducerConsumerSystem(queue_size=5, num_producers=2, num_consumers=2)
    
    print("Starting system...")
    system.start()
    
    # Let it run for a while
    time.sleep(3.0)
    
    print("\nStopping system...")
    system.stop()
    
    stats = system.get_stats()
    print(f"\nFinal stats: {stats}")
    
    print("\n=== Queue Control ===")
    queue = BoundedQueue(max_size=3)
    
    # Fill queue
    for i in range(3):
        task = Task(id=i, data=f"Item {i}")
        queue.put(task)
        print(f"Added Task {i}")
    
    print(f"Queue size: {queue.size()}")
    print(f"Queue full: {queue.is_full()}")
    
    # Try to add when full
    extra_task = Task(id=99, data="Extra")
    success = queue.put(extra_task, timeout=0.1)
    print(f"Add to full queue: {success}")
    
    # Consume items
    while not queue.is_empty():
        task = queue.get()
        print(f"Consumed Task {task.id}")
    
    print(f"Queue empty: {queue.is_empty()}")
    
    print("\n=== Priority Queue ===")
    priority_queue = BoundedQueue(max_size=10)
    
    # Add tasks with different priorities
    tasks = [
        Task(id=1, data="Low priority", priority=5),
        Task(id=2, data="High priority", priority=0),
        Task(id=3, data="Medium priority", priority=3),
        Task(id=4, data="Urgent", priority=1),
    ]
    
    for task in tasks:
        priority_queue.put(task)
        print(f"Added Task {task.id} with priority {task.priority}")
    
    # Consume - should come out in priority order
    print("\nConsuming (priority order):")
    while not priority_queue.is_empty():
        task = priority_queue.get()
        print(f"Task {task.id}: {task.data} (priority {task.priority})")
    
    print("\n=== Pause/Resume ===")
    queue = BoundedQueue(max_size=5)
    queue.pause()
    
    print(f"Queue status: {queue.get_status().value}")
    
    success = queue.put(Task(id=1, data="Test"))
    print(f"Put while paused: {success}")
    
    queue.resume()
    print(f"Queue status after resume: {queue.get_status().value}")
    
    success = queue.put(Task(id=2, data="Test"))
    print(f"Put while running: {success}")


if __name__ == "__main__":
    main()
