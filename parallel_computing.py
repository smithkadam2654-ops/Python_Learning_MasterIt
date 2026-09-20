"""
Parallel Computing Module

This module provides comprehensive parallel computing utilities including:
- Multiprocessing with ProcessPoolExecutor
- Multithreading with ThreadPoolExecutor
- Async/await patterns with asyncio
- Concurrent data structures
- Parallel map/reduce operations
- Shared memory management
- Process synchronization
- Task queues and job distribution
- Parallel file processing
- Performance monitoring

All functions include comprehensive docstrings and type hints.
"""

import time
import threading
import queue
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import multiprocessing


try:
    import asyncio
    ASYNCIO_AVAILABLE = True
except ImportError:
    ASYNCIO_AVAILABLE = False


class ParallelBackend(Enum):
    """Parallel processing backends."""
    MULTIPROCESSING = "multiprocessing"
    THREADING = "threading"
    ASYNCIO = "asyncio"
    CONCURRENT_FUTURES = "concurrent_futures"


@dataclass
class ParallelResult:
    """Container for parallel task results."""
    task_id: str
    result: Any
    success: bool
    execution_time: float
    worker_id: Optional[int] = None
    error_message: Optional[str] = None


@dataclass
class WorkerStats:
    """Worker statistics."""
    worker_id: int
    tasks_completed: int
    total_execution_time: float
    average_time: float
    errors: int


class ParallelProcessor:
    """Parallel processing with multiprocessing."""
    
    def __init__(self, max_workers: Optional[int] = None):
        """Initialize parallel processor."""
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.executor: Optional[ProcessPoolExecutor] = None
        self.results: List[ParallelResult] = []
        self.worker_stats: Dict[int, WorkerStats] = {}
    
    def __enter__(self):
        """Context manager entry."""
        self.executor = ProcessPoolExecutor(max_workers=self.max_workers)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.executor:
            self.executor.shutdown(wait=True)
    
    def map(self, func: Callable, iterable: List[Any]) -> List[Any]:
        """Parallel map operation."""
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(func, iterable))
        return results
    
    def map_async(self, func: Callable, iterable: List[Any]) -> List[Any]:
        """Parallel map operation (async)."""
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(func, item) for item in iterable]
            results = [future.result() for future in as_completed(futures)]
        return results
    
    def starmap(self, func: Callable, iterable: List[Tuple]) -> List[Any]:
        """Parallel starmap operation (for functions with multiple arguments)."""
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.starmap(func, iterable))
        return results
    
    def submit_task(self, func: Callable, *args, **kwargs) -> ParallelResult:
        """Submit single task for parallel execution."""
        task_id = f"task_{int(time.time() * 1000)}"
        start_time = time.time()
        
        try:
            with ProcessPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                result = future.result()
            
            return ParallelResult(
                task_id=task_id,
                result=result,
                success=True,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ParallelResult(
                task_id=task_id,
                result=None,
                success=False,
                execution_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def batch_process(self, func: Callable, data: List[Any],
                     batch_size: int = 10) -> List[Any]:
        """Process data in batches."""
        results = []
        
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            batch_results = self.map(func, batch)
            results.extend(batch_results)
        
        return results


class ThreadProcessor:
    """Parallel processing with threading."""
    
    def __init__(self, max_workers: Optional[int] = None):
        """Initialize thread processor."""
        self.max_workers = max_workers or multiprocessing.cpu_count() * 2
        self.executor: Optional[ThreadPoolExecutor] = None
    
    def __enter__(self):
        """Context manager entry."""
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.executor:
            self.executor.shutdown(wait=True)
    
    def map(self, func: Callable, iterable: List[Any]) -> List[Any]:
        """Parallel map with threads."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(func, iterable))
        return results
    
    def submit_tasks(self, func: Callable, tasks: List[Tuple]) -> List[ParallelResult]:
        """Submit multiple tasks for thread execution."""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(func, *task) for task in tasks]
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(ParallelResult(
                        task_id=str(id(future)),
                        result=result,
                        success=True,
                        execution_time=0.0
                    ))
                except Exception as e:
                    results.append(ParallelResult(
                        task_id=str(id(future)),
                        result=None,
                        success=False,
                        execution_time=0.0,
                        error_message=str(e)
                    ))
        
        return results


class AsyncProcessor:
    """Async/await pattern utilities."""
    
    def __init__(self):
        """Initialize async processor."""
        if not ASYNCIO_AVAILABLE:
            raise ImportError("asyncio library is required")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    async def run_async(self, func: Callable, *args, **kwargs) -> Any:
        """Run async function."""
        return await func(*args, **kwargs)
    
    async def gather_tasks(self, coroutines: List) -> List[Any]:
        """Gather multiple async tasks."""
        return await asyncio.gather(*coroutines)
    
    async def run_concurrent(self, coroutines: List, max_concurrent: int = 10) -> List[Any]:
        """Run tasks with concurrency limit."""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def limited_coro(coro):
            async with semaphore:
                return await coro
        
        limited_coros = [limited_coro(coro) for coro in coroutines]
        return await asyncio.gather(*limited_coros)
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute async function synchronously."""
        return self.loop.run_until_complete(self.run_async(func, *args, **kwargs))
    
    def execute_batch(self, func: Callable, items: List[Any]) -> List[Any]:
        """Execute async function on batch of items."""
        coroutines = [func(item) for item in items]
        return self.loop.run_until_complete(self.gather_tasks(coroutines))


class ConcurrentDataStructure:
    """Thread-safe data structures."""
    
    @staticmethod
    def thread_safe_list() -> list:
        """Create thread-safe list wrapper."""
        class ThreadSafeList:
            def __init__(self):
                self._list = []
                self._lock = threading.Lock()
            
            def append(self, item):
                with self._lock:
                    self._list.append(item)
            
            def get(self):
                with self._lock:
                    return self._list.copy()
            
            def extend(self, items):
                with self._lock:
                    self._list.extend(items)
        
        return ThreadSafeList()
    
    @staticmethod
    def thread_safe_dict() -> dict:
        """Create thread-safe dict wrapper."""
        class ThreadSafeDict:
            def __init__(self):
                self._dict = {}
                self._lock = threading.Lock()
            
            def get(self, key, default=None):
                with self._lock:
                    return self._dict.get(key, default)
            
            def set(self, key, value):
                with self._lock:
                    self._dict[key] = value
            
            def get_copy(self):
                with self._lock:
                    return self._dict.copy()
        
        return ThreadSafeDict()
    
    @staticmethod
    def thread_safe_queue(maxsize: int = 0) -> queue.Queue:
        """Create thread-safe queue."""
        return queue.Queue(maxsize=maxsize)
    
    @staticmethod
    def thread_safe_counter(initial_value: int = 0) -> Any:
        """Create thread-safe counter."""
        class ThreadSafeCounter:
            def __init__(self, initial_value=0):
                self._value = initial_value
                self._lock = threading.Lock()
            
            def increment(self):
                with self._lock:
                    self._value += 1
                    return self._value
            
            def decrement(self):
                with self._lock:
                    self._value -= 1
                    return self._value
            
            def get(self):
                with self._lock:
                    return self._value
        
        return ThreadSafeCounter(initial_value)


class ParallelMapReduce:
    """Parallel map-reduce operations."""
    
    @staticmethod
    def map_reduce(data: List[Any], map_func: Callable, 
                  reduce_func: Callable, workers: int = 4) -> Any:
        """Parallel map-reduce operation."""
        with ProcessPoolExecutor(max_workers=workers) as executor:
            # Map phase
            mapped = list(executor.map(map_func, data))
            
            # Reduce phase (can be parallel for associative operations)
            result = reduce_func(mapped)
        
        return result
    
    @staticmethod
    def parallel_filter(data: List[Any], predicate: Callable,
                       workers: int = 4) -> List[Any]:
        """Parallel filter operation."""
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(predicate, item) for item in data]
            results = []
            
            for future, item in zip(as_completed(futures), data):
                if future.result():
                    results.append(item)
        
        return results
    
    @staticmethod
    def parallel_sort(data: List[Any], key_func: Optional[Callable] = None,
                     workers: int = 4) -> List[Any]:
        """Parallel sort using merge sort."""
        if len(data) <= 1:
            return data
        
        # Simple parallel merge sort
        mid = len(data) // 2
        left = data[:mid]
        right = data[mid:]
        
        with ProcessPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(ParallelMapReduce.parallel_sort, left, key_func, 2)
            future2 = executor.submit(ParallelMapReduce.parallel_sort, right, key_func, 2)
            
            sorted_left = future1.result()
            sorted_right = future2.result()
        
        # Merge
        return ParallelMapReduce._merge(sorted_left, sorted_right, key_func)
    
    @staticmethod
    def _merge(left: List[Any], right: List[Any], 
               key_func: Optional[Callable] = None) -> List[Any]:
        """Merge two sorted lists."""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            left_key = key_func(left[i]) if key_func else left[i]
            right_key = key_func(right[j]) if key_func else right[j]
            
            if left_key <= right_key:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result


class SharedMemoryManager:
    """Shared memory management for multiprocessing."""
    
    @staticmethod
    def create_shared_value(typecode: str, initial_value: Any) -> Any:
        """Create shared value for multiprocessing."""
        return multiprocessing.Value(typecode, initial_value)
    
    @staticmethod
    def create_shared_array(typecode: str, size: int) -> Any:
        """Create shared array for multiprocessing."""
        return multiprocessing.Array(typecode, size)
    
    @staticmethod
    def shared_counter(initial_value: int = 0) -> Any:
        """Create shared counter."""
        return SharedMemoryManager.create_shared_value('i', initial_value)
    
    @staticmethod
    def shared_list(max_size: int = 100) -> Any:
        """Create shared list using manager."""
        manager = multiprocessing.Manager()
        return manager.list()


class ProcessSynchronization:
    """Process synchronization primitives."""
    
    @staticmethod
    def create_lock() -> Any:
        """Create process lock."""
        return multiprocessing.Lock()
    
    @staticmethod
    def create_semaphore(value: int = 1) -> Any:
        """Create process semaphore."""
        return multiprocessing.Semaphore(value)
    
    @staticmethod
    def create_event() -> Any:
        """Create process event."""
        return multiprocessing.Event()
    
    @staticmethod
    def create_barrier(parties: int) -> Any:
        """Create process barrier."""
        return multiprocessing.Barrier(parties)
    
    @staticmethod
    def create_queue(maxsize: int = 0) -> Any:
        """Create process queue."""
        return multiprocessing.Queue(maxsize)


class TaskQueue:
    """Task queue for job distribution."""
    
    def __init__(self, max_size: int = 0):
        """Initialize task queue."""
        self.queue = multiprocessing.Queue(maxsize=max_size)
        self.result_queue = multiprocessing.Queue()
        self.workers: List[multiprocessing.Process] = []
        self.running = False
    
    def add_task(self, task: Dict) -> bool:
        """Add task to queue."""
        try:
            self.queue.put(task, timeout=1.0)
            return True
        except:
            return False
    
    def get_task(self, timeout: float = 1.0) -> Optional[Dict]:
        """Get task from queue."""
        try:
            return self.queue.get(timeout=timeout)
        except:
            return None
    
    def add_result(self, result: Dict) -> None:
        """Add result to result queue."""
        self.result_queue.put(result)
    
    def get_result(self, timeout: float = 1.0) -> Optional[Dict]:
        """Get result from result queue."""
        try:
            return self.result_queue.get(timeout=timeout)
        except:
            return None
    
    def start_workers(self, worker_func: Callable, num_workers: int = 4) -> None:
        """Start worker processes."""
        self.running = True
        
        for i in range(num_workers):
            worker = multiprocessing.Process(target=worker_func, args=(self, i))
            worker.start()
            self.workers.append(worker)
    
    def stop_workers(self) -> None:
        """Stop all workers."""
        self.running = False
        
        for worker in self.workers:
            worker.join(timeout=5)
        
        self.workers.clear()


class ParallelFileProcessor:
    """Parallel file processing utilities."""
    
    @staticmethod
    def process_files(file_paths: List[str], 
                      process_func: Callable,
                      workers: int = 4) -> List[ParallelResult]:
        """Process multiple files in parallel."""
        results = []
        
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(process_func, path): path for path in file_paths}
            
            for future in as_completed(futures):
                file_path = futures[future]
                start_time = time.time()
                
                try:
                    result = future.result()
                    results.append(ParallelResult(
                        task_id=file_path,
                        result=result,
                        success=True,
                        execution_time=time.time() - start_time
                    ))
                except Exception as e:
                    results.append(ParallelResult(
                        task_id=file_path,
                        result=None,
                        success=False,
                        execution_time=time.time() - start_time,
                        error_message=str(e)
                    ))
        
        return results
    
    @staticmethod
    def process_directory(directory: str,
                          process_func: Callable,
                          pattern: str = "*",
                          workers: int = 4) -> List[ParallelResult]:
        """Process all files in directory matching pattern."""
        import glob
        import os
        
        file_paths = glob.glob(os.path.join(directory, pattern))
        return ParallelFileProcessor.process_files(file_paths, process_func, workers)
    
    @staticmethod
    def parallel_read_files(file_paths: List[str], workers: int = 4) -> Dict[str, str]:
        """Read multiple files in parallel."""
        def read_file(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(read_file, path): path for path in file_paths}
            results = {}
            
            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    results[file_path] = future.result()
                except Exception as e:
                    results[file_path] = f"Error: {e}"
        
        return results
    
    @staticmethod
    def parallel_write_files(file_data: Dict[str, str], workers: int = 4) -> Dict[str, bool]:
        """Write multiple files in parallel."""
        def write_file(data):
            path, content = data
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(write_file, (path, content)): path 
                       for path, content in file_data.items()}
            results = {}
            
            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    results[file_path] = future.result()
                except Exception as e:
                    results[file_path] = False
        
        return results


class PerformanceMonitor:
    """Performance monitoring for parallel operations."""
    
    def __init__(self):
        """Initialize performance monitor."""
        self.metrics: Dict[str, List[float]] = {}
        self.lock = threading.Lock()
    
    def record_metric(self, metric_name: str, value: float) -> None:
        """Record performance metric."""
        with self.lock:
            if metric_name not in self.metrics:
                self.metrics[metric_name] = []
            self.metrics[metric_name].append(value)
    
    def get_metric_stats(self, metric_name: str) -> Dict[str, float]:
        """Get statistics for a metric."""
        with self.lock:
            if metric_name not in self.metrics or not self.metrics[metric_name]:
                return {}
            
            values = self.metrics[metric_name]
            
            return {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "mean": sum(values) / len(values),
                "sum": sum(values)
            }
    
    def get_all_metrics(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all metrics."""
        with self.lock:
            return {name: self.get_metric_stats(name) for name in self.metrics}
    
    def reset(self) -> None:
        """Reset all metrics."""
        with self.lock:
            self.metrics.clear()


class ParallelSort:
    """Parallel sorting algorithms."""
    
    @staticmethod
    def parallel_quick_sort(data: List[Any], workers: int = 4) -> List[Any]:
        """Parallel quicksort implementation."""
        if len(data) <= 1:
            return data
        
        # Choose pivot
        pivot = data[len(data) // 2]
        
        # Partition
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        
        # Parallel sort partitions
        with ProcessPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(ParallelSort.parallel_quick_sort, left, workers)
            future2 = executor.submit(ParallelSort.parallel_quick_sort, right, workers)
            
            sorted_left = future1.result()
            sorted_right = future2.result()
        
        return sorted_left + middle + sorted_right
    
    @staticmethod
    def parallel_merge_sort(data: List[Any], workers: int = 4) -> List[Any]:
        """Parallel merge sort implementation."""
        return ParallelMapReduce.parallel_sort(data, workers=workers)


class LoadBalancer:
    """Load balancing for parallel tasks."""
    
    @staticmethod
    def round_robin(tasks: List[Any], num_workers: int) -> List[List[Any]]:
        """Distribute tasks using round-robin."""
        worker_tasks = [[] for _ in range(num_workers)]
        
        for i, task in enumerate(tasks):
            worker_tasks[i % num_workers].append(task)
        
        return worker_tasks
    
    @staticmethod
    def least_loaded(tasks: List[Tuple[Any, float]], num_workers: int) -> List[List[Any]]:
        """Distribute tasks by estimated load."""
        worker_tasks = [[] for _ in range(num_workers)]
        worker_loads = [0.0] * num_workers
        
        for task, load in tasks:
            # Find least loaded worker
            min_load_index = worker_loads.index(min(worker_loads))
            worker_tasks[min_load_index].append(task)
            worker_loads[min_load_index] += load
        
        return worker_tasks
    
    @staticmethod
    def work_stealing(worker_tasks: List[List[Any]], idle_worker: int) -> Optional[Any]:
        """Work stealing - steal task from busy worker."""
        if idle_worker >= len(worker_tasks):
            return None
        
        # Find worker with most tasks
        max_tasks_index = max(range(len(worker_tasks)), 
                             key=lambda i: len(worker_tasks[i]))
        
        if len(worker_tasks[max_tasks_index]) > 1:
            stolen_task = worker_tasks[max_tasks_index].pop()
            return stolen_task
        
        return None


def demonstrate_parallel_computing():
    """Demonstrate parallel computing functionality."""
    print("=== Parallel Computing Demonstration ===\n")
    
    # Parallel Map
    print("1. Parallel Map:")
    processor = ParallelProcessor(max_workers=4)
    
    def square(x):
        return x * x
    
    numbers = list(range(1, 11))
    squared = processor.map(square, numbers)
    print(f"   Parallel map: {squared}")
    
    # Thread Pool
    print("\n2. Thread Pool:")
    thread_processor = ThreadProcessor(max_workers=4)
    
    def slow_operation(x):
        time.sleep(0.1)
        return x * 2
    
    thread_results = thread_processor.map(slow_operation, [1, 2, 3, 4])
    print(f"   Thread map: {thread_results}")
    
    # Map-Reduce
    print("\n3. Map-Reduce:")
    data = list(range(1, 11))
    
    def map_func(x):
        return x * x
    
    def reduce_func(results):
        return sum(results)
    
    total = ParallelMapReduce.map_reduce(data, map_func, reduce_func)
    print(f"   Map-reduce sum of squares: {total}")
    
    # Parallel Filter
    print("\n4. Parallel Filter:")
    def is_even(x):
        return x % 2 == 0
    
    evens = ParallelMapReduce.parallel_filter(data, is_even)
    print(f"   Parallel filter evens: {evens}")
    
    # Concurrent Data Structures
    print("\n5. Concurrent Data Structures:")
    safe_list = ConcurrentDataStructure.thread_safe_list()
    safe_list.append(1)
    safe_list.append(2)
    print(f"   Thread-safe list: {safe_list.get()}")
    
    safe_dict = ConcurrentDataStructure.thread_safe_dict()
    safe_dict.set("key1", "value1")
    safe_dict.set("key2", "value2")
    print(f"   Thread-safe dict: {safe_dict.get_copy()}")
    
    # Shared Memory
    print("\n6. Shared Memory:")
    counter = SharedMemoryManager.shared_counter(0)
    print(f"   Shared counter: {counter.value}")
    
    # Task Queue
    print("\n7. Task Queue:")
    task_queue = TaskQueue(max_size=10)
    task_queue.add_task({"task": "process", "data": "test"})
    task = task_queue.get_task()
    print(f"   Task from queue: {task}")
    
    # Parallel File Processing
    print("\n8. Parallel File Processing:")
    import os
    import tempfile
    
    # Create test files
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(3):
            file_path = os.path.join(tmpdir, f"test_{i}.txt")
            with open(file_path, 'w') as f:
                f.write(f"Content {i}")
        
        def process_file(path):
            with open(path, 'r') as f:
                return f.read()
        
        results = ParallelFileProcessor.process_directory(tmpdir, process_file, "test_*.txt")
        print(f"   Processed {len(results)} files")
    
    # Performance Monitoring
    print("\n9. Performance Monitoring:")
    monitor = PerformanceMonitor()
    
    for i in range(5):
        monitor.record_metric("task_time", 0.1 + i * 0.05)
    
    stats = monitor.get_metric_stats("task_time")
    print(f"   Task time stats: {stats}")
    
    # Load Balancing
    print("\n10. Load Balancing:")
    tasks = list(range(10))
    
    round_robin = LoadBalancer.round_robin(tasks, 3)
    print(f"   Round-robin distribution: {[len(tasks) for tasks in round_robin]}")
    
    weighted_tasks = [(i, i * 0.1) for i in range(10)]
    least_loaded = LoadBalancer.least_loaded(weighted_tasks, 3)
    print(f"   Least loaded distribution: {[len(tasks) for tasks in least_loaded]}")
    
    # Async Processing
    print("\n11. Async Processing:")
    if ASYNCIO_AVAILABLE:
        async def async_task(x):
            await asyncio.sleep(0.1)
            return x * 2
        
        async_processor = AsyncProcessor()
        async_result = async_processor.execute(async_task, 5)
        print(f"   Async result: {async_result}")
    else:
        print("   asyncio not available")
    
    # Parallel Sort
    print("\n12. Parallel Sort:")
    unsorted = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    
    sorted_data = ParallelSort.parallel_merge_sort(unsorted)
    print(f"   Parallel sort: {sorted_data}")
    
    print("\n=== Demonstration Complete ===")
    print("\nParallel Computing Best Practices:")
    print("- Use multiprocessing for CPU-bound tasks")
    print("- Use threading for I/O-bound tasks")
    print("- Use asyncio for concurrent I/O operations")
    print("- Be aware of GIL limitations with threading")
    print("- Use process pools for expensive operations")
    print("- Implement proper synchronization for shared resources")
    print("- Consider task granularity and overhead")
    print("- Monitor performance and adjust worker count")
    print("- Handle exceptions and timeouts properly")
    print("- Use concurrent data structures when sharing data")


if __name__ == "__main__":
    demonstrate_parallel_computing()