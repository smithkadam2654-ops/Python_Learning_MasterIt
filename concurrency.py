"""
Concurrency Patterns - Concurrent and parallel programming techniques.
Features: Threading, multiprocessing, async/await, and synchronization primitives.
"""

from typing import List, Optional
import threading
import multiprocessing
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


class ConcurrencyPatterns:
    """Concurrency pattern implementations."""
    
    @staticmethod
    def run_with_threads(func, args_list: List[tuple], max_workers: int = 4) -> List:
        """
        Run function with multiple threads.
        
        Args:
            func: Function to run
            args_list: List of argument tuples
            max_workers: Maximum number of threads
            
        Returns:
            List of results
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(func, *args) for args in args_list]
            results = [future.result() for future in futures]
        
        return results
    
    @staticmethod
    def run_with_processes(func, args_list: List[tuple], max_workers: int = 4) -> List:
        """
        Run function with multiple processes.
        
        Args:
            func: Function to run
            args_list: List of argument tuples
            max_workers: Maximum number of processes
            
        Returns:
            List of results
        """
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(func, *args) for args in args_list]
            results = [future.result() for future in futures]
        
        return results
    
    @staticmethod
    def async_gather(coro_list: List) -> List:
        """
        Run multiple coroutines concurrently.
        
        Args:
            coro_list: List of coroutines
            
        Returns:
            List of results
        """
        async def run_all():
            return await asyncio.gather(*coro_list)
        
        return asyncio.run(run_all())
    
    @staticmethod
    def producer_consumer(buffer_size: int = 5) -> None:
        """
        Producer-consumer pattern using threading.
        
        Args:
            buffer_size: Size of shared buffer
        """
        buffer = []
        buffer_lock = threading.Lock()
        not_empty = threading.Condition(buffer_lock)
        not_full = threading.Condition(buffer_lock)
        
        def producer():
            for i in range(10):
                with not_full:
                    while len(buffer) >= buffer_size:
                        not_full.wait()
                    buffer.append(f"item_{i}")
                    print(f"Produced: item_{i}")
                    not_empty.notify()
                time.sleep(0.1)
        
        def consumer():
            for _ in range(10):
                with not_empty:
                    while len(buffer) == 0:
                        not_empty.wait()
                    item = buffer.pop(0)
                    print(f"Consumed: {item}")
                    not_full.notify()
                time.sleep(0.15)
        
        producer_thread = threading.Thread(target=producer)
        consumer_thread = threading.Thread(target=consumer)
        
        producer_thread.start()
        consumer_thread.start()
        
        producer_thread.join()
        consumer_thread.join()
    
    @staticmethod
    def thread_safe_counter() -> int:
        """
        Thread-safe counter using lock.
        
        Returns:
            Final counter value
        """
        counter = 0
        lock = threading.Lock()
        
        def increment():
            nonlocal counter
            for _ in range(10000):
                with lock:
                    counter += 1
        
        threads = [threading.Thread(target=increment) for _ in range(10)]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        return counter
    
    @staticmethod
    def parallel_map(func, items: List, chunksize: int = 1) -> List:
        """
        Parallel map using multiprocessing.
        
        Args:
            func: Function to apply
            items: List of items
            chunksize: Chunk size for processing
            
        Returns:
            List of results
        """
        with multiprocessing.Pool() as pool:
            results = pool.map(func, items, chunksize=chunksize)
        
        return results
    
    @staticmethod
    def async_semaphore_example(max_concurrent: int = 3) -> List:
        """
        Async semaphore to limit concurrent operations.
        
        Args:
            max_concurrent: Maximum concurrent operations
            
        Returns:
            List of results
        """
        async def task(name: str, semaphore: asyncio.Semaphore):
            async with semaphore:
                print(f"Starting {name}")
                await asyncio.sleep(1)
                print(f"Finished {name}")
                return name
        
        async def run_all():
            semaphore = asyncio.Semaphore(max_concurrent)
            tasks = [task(f"task_{i}", semaphore) for i in range(10)]
            return await asyncio.gather(*tasks)
        
        return asyncio.run(run_all())
    
    @staticmethod
    def barrier_example(num_threads: int = 5) -> None:
        """
        Barrier synchronization example.
        
        Args:
            num_threads: Number of threads
        """
        barrier = threading.Barrier(num_threads)
        
        def worker(worker_id: int):
            print(f"Worker {worker_id} waiting")
            barrier.wait()
            print(f"Worker {worker_id} released")
        
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(num_threads)]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
    
    @staticmethod
    def read_write_lock_example() -> None:
        """
        Read-write lock pattern (simplified).
        
        Note: Python doesn't have built-in RLock for read-write,
        this is a simplified demonstration.
        """
        data = []
        lock = threading.Lock()
        readers = 0
        readers_lock = threading.Lock()
        
        def reader(reader_id: int):
            nonlocal readers
            with readers_lock:
                readers += 1
                if readers == 1:
                    lock.acquire()
            
            print(f"Reader {reader_id} reading: {data}")
            time.sleep(0.1)
            
            with readers_lock:
                readers -= 1
                if readers == 0:
                    lock.release()
            
            print(f"Reader {reader_id} finished")
        
        def writer(writer_id: int):
            with lock:
                print(f"Writer {writer_id} writing")
                data.append(f"item_{writer_id}")
                time.sleep(0.2)
                print(f"Writer {writer_id} finished")
        
        # Start readers and writers
        threads = []
        
        for i in range(3):
            threads.append(threading.Thread(target=reader, args=(i,)))
        
        for i in range(2):
            threads.append(threading.Thread(target=writer, args=(i,)))
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
    
    @staticmethod
    def pipeline_stages(data: List) -> List:
        """
        Pipeline pattern using queues.
        
        Args:
            data: Input data
            
        Returns:
            Processed data
        """
        from queue import Queue
        
        def stage1(input_queue: Queue, output_queue: Queue):
            while True:
                item = input_queue.get()
                if item is None:
                    break
                output_queue.put(item * 2)
        
        def stage2(input_queue: Queue, output_queue: Queue):
            while True:
                item = input_queue.get()
                if item is None:
                    break
                output_queue.put(item + 10)
        
        input_q = Queue()
        mid_q = Queue()
        output_q = Queue()
        
        # Start stages
        t1 = threading.Thread(target=stage1, args=(input_q, mid_q))
        t2 = threading.Thread(target=stage2, args=(mid_q, output_q))
        
        t1.start()
        t2.start()
        
        # Feed data
        for item in data:
            input_q.put(item)
        
        # Signal end
        input_q.put(None)
        mid_q.put(None)
        
        t1.join()
        t2.join()
        
        # Collect results
        results = []
        while not output_q.empty():
            results.append(output_q.get())
        
        return results


class AsyncPatterns:
    """Async/await pattern implementations."""
    
    @staticmethod
    async def fetch_url(url: str, delay: float = 1.0) -> str:
        """
        Simulate async URL fetch.
        
        Args:
            url: URL to fetch
            delay: Simulated delay
            
        Returns:
            Response string
        """
        await asyncio.sleep(delay)
        return f"Response from {url}"
    
    @staticmethod
    async def fetch_multiple_urls(urls: List[str]) -> List[str]:
        """
        Fetch multiple URLs concurrently.
        
        Args:
            urls: List of URLs
            
        Returns:
            List of responses
        """
        tasks = [AsyncPatterns.fetch_url(url) for url in urls]
        return await asyncio.gather(*tasks)
    
    @staticmethod
    async def timeout_example(coro, timeout: float = 2.0):
        """
        Async operation with timeout.
        
        Args:
            coro: Coroutine to run
            timeout: Timeout in seconds
            
        Returns:
            Result or None if timeout
        """
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            return None
    
    @staticmethod
    async def retry_example(coro, max_retries: int = 3, delay: float = 1.0):
        """
        Async operation with retry logic.
        
        Args:
            coro: Coroutine to run
            max_retries: Maximum retry attempts
            delay: Delay between retries
            
        Returns:
            Result or None if all retries fail
        """
        for attempt in range(max_retries):
            try:
                return await coro
            except Exception:
                if attempt < max_retries - 1:
                    await asyncio.sleep(delay)
                else:
                    return None


def square(x: int) -> int:
    """Helper function for parallel processing."""
    return x * x


def main() -> None:
    """Demonstrate concurrency patterns."""
    
    print("=== Concurrency Patterns Demo ===")
    
    # Thread pool
    print("\n--- Thread Pool ---")
    def task(x: int) -> int:
        time.sleep(0.1)
        return x * x
    
    args_list = [(i,) for i in range(5)]
    results = ConcurrencyPatterns.run_with_threads(task, args_list)
    print(f"Results: {results}")
    
    # Process pool
    print("\n--- Process Pool ---")
    results = ConcurrencyPatterns.run_with_processes(square, args_list)
    print(f"Results: {results}")
    
    # Thread-safe counter
    print("\n--- Thread-Safe Counter ---")
    counter = ConcurrencyPatterns.thread_safe_counter()
    print(f"Final counter: {counter}")
    
    # Parallel map
    print("\n--- Parallel Map ---")
    items = list(range(10))
    results = ConcurrencyPatterns.parallel_map(square, items)
    print(f"Results: {results}")
    
    # Barrier
    print("\n--- Barrier ---")
    ConcurrencyPatterns.barrier_example(3)
    
    # Pipeline
    print("\n--- Pipeline ---")
    data = [1, 2, 3, 4, 5]
    results = ConcurrencyPatterns.pipeline_stages(data)
    print(f"Input: {data}")
    print(f"Output: {results}")
    
    # Async patterns
    print("\n--- Async Fetch Multiple ---")
    urls = ["url1", "url2", "url3"]
    results = asyncio.run(AsyncPatterns.fetch_multiple_urls(urls))
    print(f"Results: {results}")


if __name__ == "__main__":
    main()
