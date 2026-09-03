"""
Object Pool - Object pooling pattern for resource management.
Features: Generic object pool, automatic resource recycling, and pool statistics.
"""

import threading
from typing import TypeVar, Generic, Callable, Optional, List
from dataclasses import dataclass
from enum import Enum


T = TypeVar('T')


class PoolStatus(Enum):
    """Pool status."""
    AVAILABLE = "available"
    EXHAUSTED = "exhausted"
    CLOSED = "closed"


@dataclass
class PoolConfig:
    """Configuration for object pool."""
    min_size: int = 2
    max_size: int = 10
    create_timeout: float = 5.0


class PooledObject(Generic[T]):
    """Wrapper for pooled objects."""
    
    def __init__(self, obj: T, pool: 'ObjectPool') -> None:
        """
        Initialize pooled object wrapper.
        
        Args:
            obj: The actual object
            pool: Reference to the pool
        """
        self.obj = obj
        self.pool = pool
        self.in_use = False
        self.last_used = None
    
    def release(self) -> None:
        """Release object back to pool."""
        self.pool.release(self)


class ObjectPool(Generic[T]):
    """Generic object pool implementation."""
    
    def __init__(self, factory: Callable[[], T], 
                 config: Optional[PoolConfig] = None) -> None:
        """
        Initialize object pool.
        
        Args:
            factory: Function to create new objects
            config: Pool configuration
        """
        self.factory = factory
        self.config = config or PoolConfig()
        self.available: List[PooledObject[T]] = []
        self.in_use: List[PooledObject[T]] = []
        self._lock = threading.RLock()
        self._status = PoolStatus.AVAILABLE
        
        # Initialize with minimum pool size
        self._initialize_pool()
    
    def _initialize_pool(self) -> None:
        """Initialize pool with minimum number of objects."""
        for _ in range(self.config.min_size):
            obj = self.factory()
            self.available.append(PooledObject(obj, self))
    
    def acquire(self, timeout: Optional[float] = None) -> Optional[PooledObject[T]]:
        """
        Acquire an object from the pool.
        
        Args:
            timeout: Maximum time to wait (None = no timeout)
            
        Returns:
            Pooled object or None if pool is exhausted
        """
        if self._status == PoolStatus.CLOSED:
            return None
        
        with self._lock:
            if self.available:
                pooled_obj = self.available.pop()
                self.in_use.append(pooled_obj)
                pooled_obj.in_use = True
                return pooled_obj
            
            # Try to create new object if under max size
            if len(self.in_use) + len(self.available) < self.config.max_size:
                obj = self.factory()
                pooled_obj = PooledObject(obj, self)
                self.in_use.append(pooled_obj)
                pooled_obj.in_use = True
                return pooled_obj
            
            self._status = PoolStatus.EXHAUSTED
            return None
    
    def release(self, pooled_obj: PooledObject[T]) -> None:
        """
        Release an object back to the pool.
        
        Args:
            pooled_obj: Pooled object to release
        """
        with self._lock:
            if pooled_obj in self.in_use:
                self.in_use.remove(pooled_obj)
                pooled_obj.in_use = False
                
                # Reset object if needed
                if hasattr(pooled_obj.obj, 'reset'):
                    pooled_obj.obj.reset()
                
                self.available.append(pooled_obj)
                self._status = PoolStatus.AVAILABLE
    
    def close(self) -> None:
        """Close the pool and release all resources."""
        with self._lock:
            self._status = PoolStatus.CLOSED
            
            # Call cleanup on all objects
            for pooled_obj in self.available + self.in_use:
                if hasattr(pooled_obj.obj, 'close'):
                    try:
                        pooled_obj.obj.close()
                    except Exception as e:
                        print(f"Error closing object: {e}")
            
            self.available.clear()
            self.in_use.clear()
    
    def get_status(self) -> PoolStatus:
        """Get current pool status."""
        return self._status
    
    def get_available_count(self) -> int:
        """Get number of available objects."""
        with self._lock:
            return len(self.available)
    
    def get_in_use_count(self) -> int:
        """Get number of objects in use."""
        with self._lock:
            return len(self.in_use)
    
    def get_total_count(self) -> int:
        """Get total number of objects in pool."""
        return self.get_available_count() + self.get_in_use_count()


class Connection:
    """Example database connection class."""
    
    def __init__(self, connection_string: str) -> None:
        """
        Initialize connection.
        
        Args:
            connection_string: Database connection string
        """
        self.connection_string = connection_string
        self.is_connected = True
        print(f"Created connection to {connection_string}")
    
    def execute(self, query: str) -> str:
        """
        Execute a query.
        
        Args:
            query: SQL query
            
        Returns:
            Query result
        """
        return f"Result for: {query}"
    
    def reset(self) -> None:
        """Reset connection state."""
        self.is_connected = True
    
    def close(self) -> None:
        """Close connection."""
        self.is_connected = False
        print(f"Closed connection to {self.connection_string}")


class ConnectionPool(ObjectPool[Connection]):
    """Specialized pool for database connections."""
    
    def __init__(self, connection_string: str, config: Optional[PoolConfig] = None) -> None:
        """
        Initialize connection pool.
        
        Args:
            connection_string: Database connection string
            config: Pool configuration
        """
        self.connection_string = connection_string
        super().__init__(
            lambda: Connection(connection_string),
            config
        )
    
    def get_connection(self) -> Optional[PooledObject[Connection]]:
        """
        Get a connection from the pool.
        
        Returns:
            Pooled connection or None if exhausted
        """
        return self.acquire()


class Worker:
    """Example worker class."""
    
    def __init__(self, worker_id: int) -> None:
        """
        Initialize worker.
        
        Args:
            worker_id: Worker identifier
        """
        self.worker_id = worker_id
        self.busy = False
        print(f"Created worker {worker_id}")
    
    def process(self, task: str) -> str:
        """
        Process a task.
        
        Args:
            task: Task to process
            
        Returns:
            Processing result
        """
        self.busy = True
        result = f"Worker {self.worker_id} processed: {task}"
        self.busy = False
        return result
    
    def reset(self) -> None:
        """Reset worker state."""
        self.busy = False
    
    def close(self) -> None:
        """Close worker."""
        print(f"Worker {self.worker_id} shutting down")


class WorkerPool(ObjectPool[Worker]):
    """Specialized pool for workers."""
    
    def __init__(self, num_workers: int = 4) -> None:
        """
        Initialize worker pool.
        
        Args:
            num_workers: Number of workers
        """
        config = PoolConfig(min_size=num_workers, max_size=num_workers)
        super().__init__(
            lambda: Worker(len(self.available) + len(self.in_use) + 1),
            config
        )
    
    def get_worker(self) -> Optional[PooledObject[Worker]]:
        """
        Get a worker from the pool.
        
        Returns:
            Pooled worker or None if exhausted
        """
        return self.acquire()


def main() -> None:
    """Demonstrate object pool functionality."""
    
    print("=== Connection Pool ===")
    pool = ConnectionPool("postgresql://localhost/mydb", PoolConfig(min_size=2, max_size=5))
    
    # Acquire connections
    conn1 = pool.get_connection()
    conn2 = pool.get_connection()
    conn3 = pool.get_connection()
    
    print(f"Available: {pool.get_available_count()}")
    print(f"In use: {pool.get_in_use_count()}")
    
    # Use connections
    if conn1:
        result = conn1.obj.execute("SELECT * FROM users")
        print(f"Query result: {result}")
    
    # Release connections
    if conn1:
        pool.release(conn1)
    
    print(f"After release - Available: {pool.get_available_count()}")
    
    # Close pool
    pool.close()
    print(f"Pool status: {pool.get_status()}")
    
    print("\n=== Worker Pool ===")
    worker_pool = WorkerPool(num_workers=3)
    
    # Get workers and process tasks
    tasks = ["Task A", "Task B", "Task C", "Task D"]
    
    for task in tasks:
        worker = worker_pool.get_worker()
        if worker:
            result = worker.obj.process(task)
            print(result)
            worker_pool.release(worker)
    
    print(f"Final pool stats:")
    print(f"  Available: {worker_pool.get_available_count()}")
    print(f"  In use: {worker_pool.get_in_use_count()}")
    
    worker_pool.close()
    
    print("\n=== Pool Exhaustion ===")
    small_pool = ConnectionPool("localhost/test", PoolConfig(min_size=1, max_size=2))
    
    # Try to acquire more than max size
    conn1 = small_pool.get_connection()
    conn2 = small_pool.get_connection()
    conn3 = small_pool.get_connection()  # Should return None
    
    print(f"Available: {small_pool.get_available_count()}")
    print(f"In use: {small_pool.get_in_use_count()}")
    print(f"Status: {small_pool.get_status()}")
    
    if conn3 is None:
        print("Pool exhausted - could not acquire connection")
    
    small_pool.close()


if __name__ == "__main__":
    main()
