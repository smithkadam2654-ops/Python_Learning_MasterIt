"""
Thread Pool - Thread pool executor for concurrent task execution.
Features: Task submission, result handling, and worker pool management.
"""

import threading
import queue
import time
from typing import Callable, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """Task to be executed by thread pool."""
    func: Callable
    args: tuple = ()
    kwargs: dict = None
    callback: Optional[Callable] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[Exception] = None
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}


class Worker(threading.Thread):
    """Worker thread for executing tasks."""
    
    def __init__(self, task_queue: queue.Queue, worker_id: int) -> None:
        """
        Initialize worker thread.
        
        Args:
            task_queue: Queue to get tasks from
            worker_id: Worker identifier
        """
        super().__init__(daemon=True)
        self.task_queue = task_queue
        self.worker_id = worker_id
        self.running = True
    
    def run(self) -> None:
        """Main worker loop."""
        while self.running:
            try:
                task = self.task_queue.get(timeout=1.0)
                
                if task is None:  # Poison pill
                    self.running = False
                    break
                
                task.status = TaskStatus.RUNNING
                
                try:
                    result = task.func(*task.args, **task.kwargs)
                    task.result = result
                    task.status = TaskStatus.COMPLETED
                    
                    if task.callback:
                        task.callback(result)
                        
                except Exception as e:
                    task.error = e
                    task.status = TaskStatus.FAILED
                
                self.task_queue.task_done()
                
            except queue.Empty:
                continue


class ThreadPool:
    """Thread pool for concurrent task execution."""
    
    def __init__(self, num_workers: int = 4) -> None:
        """
        Initialize thread pool.
        
        Args:
            num_workers: Number of worker threads
        """
        self.num_workers = num_workers
        self.task_queue = queue.Queue()
        self.workers: List[Worker] = []
        self.running = False
        self._lock = threading.Lock()
    
    def start(self) -> None:
        """Start the thread pool."""
        with self._lock:
            if self.running:
                return
            
            self.running = True
            self.workers = [
                Worker(self.task_queue, i)
                for i in range(self.num_workers)
            ]
            
            for worker in self.workers:
                worker.start()
    
    def submit(self, func: Callable, args: tuple = (), 
              kwargs: dict = None, callback: Optional[Callable] = None) -> Task:
        """
        Submit a task to the thread pool.
        
        Args:
            func: Function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            callback: Callback function for result
            
        Returns:
            Task object
        """
        if not self.running:
            self.start()
        
        task = Task(func, args, kwargs, callback)
        self.task_queue.put(task)
        return task
    
    def submitAndWait(self, func: Callable, args: tuple = None, 
                     kwargs: dict = None) -> Any:
        """
        Submit task and wait for result.
        
        Args:
            func: Function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            Task result
        """
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        
        task = self.submit(func, args, kwargs)
        
        # Wait for task completion
        while task.status == TaskStatus.PENDING or task.status == TaskStatus.RUNNING:
            time.sleep(0.01)
        
        if task.status == TaskStatus.FAILED:
            raise task.error
        
        return task.result
    
    def shutdown(self, wait: bool = True) -> None:
        """
        Shutdown the thread pool.
        
        Args:
            wait: Whether to wait for tasks to complete
        """
        with self._lock:
            if not self.running:
                return
            
            self.running = False
            
            # Send poison pills to workers
            for _ in range(self.num_workers):
                self.task_queue.put(None)
        
        if wait:
            for worker in self.workers:
                worker.join(timeout=5.0)
    
    def get_pending_count(self) -> int:
        """Get number of pending tasks."""
        return self.task_queue.qsize()
    
    def get_worker_count(self) -> int:
        """Get number of workers."""
        return len(self.workers)


class AsyncTask:
    """Async task with future-like behavior."""
    
    def __init__(self, task: Task) -> None:
        """
        Initialize async task.
        
        Args:
            task: Task to wrap
        """
        self.task = task
        self._completed = threading.Event()
    
    def get(self, timeout: Optional[float] = None) -> Any:
        """
        Get task result, blocking until complete.
        
        Args:
            timeout: Maximum time to wait
            
        Returns:
            Task result
        """
        if self._completed.wait(timeout):
            if self.task.status == TaskStatus.FAILED:
                raise self.task.error
            return self.task.result
        raise TimeoutError("Task did not complete in time")
    
    def is_done(self) -> bool:
        """Check if task is complete."""
        return self.task.status in (TaskStatus.COMPLETED, TaskStatus.FAILED)
    
    def is_successful(self) -> bool:
        """Check if task completed successfully."""
        return self.task.status == TaskStatus.COMPLETED


class ThreadPoolWithFutures:
    """Thread pool with future-like task objects."""
    
    def __init__(self, num_workers: int = 4) -> None:
        """
        Initialize thread pool with futures.
        
        Args:
            num_workers: Number of worker threads
        """
        self.pool = ThreadPool(num_workers)
        self.tasks: List[AsyncTask] = []
    
    def submit(self, func: Callable, args: tuple = None, 
              kwargs: dict = None) -> AsyncTask:
        """
        Submit task and return async task.
        
        Args:
            func: Function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            AsyncTask object
        """
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        
        task = self.pool.submit(func, args, kwargs)
        async_task = AsyncTask(task)
        self.tasks.append(async_task)
        return async_task
    
    def map(self, func: Callable, items: list) -> List[Any]:
        """
        Apply function to all items concurrently.
        
        Args:
            func: Function to apply
            items: Items to process
            
        Returns:
            List of results in order
        """
        async_tasks = [self.submit(func, (item,)) for item in items]
        return [task.get() for task in async_tasks]
    
    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the thread pool."""
        self.pool.shutdown(wait)


def main() -> None:
    """Demonstrate thread pool functionality."""
    
    print("=== Basic Thread Pool ===")
    pool = ThreadPool(num_workers=3)
    
    def worker_task(name: str, duration: float) -> str:
        """Sample worker task."""
        print(f"Task {name} started")
        time.sleep(duration)
        print(f"Task {name} completed")
        return f"Result from {name}"
    
    # Submit tasks
    tasks = [
        pool.submit(worker_task, ("Task 1", 1.0)),
        pool.submit(worker_task, ("Task 2", 0.5)),
        pool.submit(worker_task, ("Task 3", 0.8)),
        pool.submit(worker_task, ("Task 4", 0.3)),
    ]
    
    # Wait for all tasks
    for task in tasks:
        while task.status == TaskStatus.PENDING or task.status == TaskStatus.RUNNING:
            time.sleep(0.1)
        
        if task.status == TaskStatus.COMPLETED:
            print(f"Task result: {task.result}")
        else:
            print(f"Task failed: {task.error}")
    
    pool.shutdown()
    
    print("\n=== Submit and Wait ===")
    pool2 = ThreadPool(num_workers=2)
    
    def compute_task(x: int) -> int:
        """Compute task."""
        time.sleep(0.5)
        return x * 2
    
    result = pool2.submitAndWait(compute_task, (5,))
    print(f"Result: {result}")
    
    pool2.shutdown()
    
    print("\n=== Thread Pool with Futures ===")
    future_pool = ThreadPoolWithFutures(num_workers=3)
    
    def download_task(url: str) -> str:
        """Simulate download task."""
        time.sleep(0.3)
        return f"Content from {url}"
    
    urls = ["http://example.com/1", "http://example.com/2", "http://example.com/3"]
    
    async_tasks = [future_pool.submit(download_task, (url,)) for url in urls]
    
    for task in async_tasks:
        result = task.get(timeout=5.0)
        print(f"Downloaded: {result}")
    
    print("\n=== Map Operation ===")
    def process_item(item: int) -> int:
        """Process single item."""
        time.sleep(0.2)
        return item ** 2
    
    items = [1, 2, 3, 4, 5]
    results = future_pool.map(process_item, items)
    print(f"Input: {items}")
    print(f"Results: {results}")
    
    future_pool.shutdown()
    
    print("\n=== Task with Callback ===")
    pool3 = ThreadPool(num_workers=2)
    
    results = []
    
    def callback(result: str) -> None:
        """Callback for task completion."""
        results.append(result)
        print(f"Callback received: {result}")
    
    def callback_task(value: str) -> str:
        """Task with callback."""
        time.sleep(0.3)
        return f"Processed: {value}"
    
    pool3.submit(callback_task, ("Hello",), callback=callback)
    pool3.submit(callback_task, ("World",), callback=callback)
    
    time.sleep(1.0)
    print(f"All results: {results}")
    
    pool3.shutdown()


if __name__ == "__main__":
    main()
