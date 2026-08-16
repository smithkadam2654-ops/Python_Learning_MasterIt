"""
Async Programming - Asynchronous programming patterns in Python.
Features: Async/await, coroutines, tasks, concurrent execution, and async context managers.
"""

import asyncio
import random
import time
from typing import List, AsyncGenerator
from dataclasses import dataclass
from contextlib import asynccontextmanager


# ==================== BASIC ASYNC FUNCTIONS ====================

async def fetch_data(url: str, delay: float) -> str:
    """
    Simulate fetching data from a URL with delay.
    
    Args:
        url: URL to fetch from
        delay: Simulated network delay in seconds
        
    Returns:
        Simulated response data
    """
    print(f"Fetching {url}...")
    await asyncio.sleep(delay)
    return f"Data from {url}"


async def process_data(data: str, processing_time: float) -> str:
    """
    Simulate processing data with delay.
    
    Args:
        data: Data to process
        processing_time: Simulated processing time
        
    Returns:
        Processed data
    """
    print(f"Processing {data}...")
    await asyncio.sleep(processing_time)
    return f"Processed: {data}"


# ==================== CONCURRENT EXECUTION ====================

async def fetch_multiple_urls(urls: List[str]) -> List[str]:
    """
    Fetch data from multiple URLs concurrently.
    
    Args:
        urls: List of URLs to fetch
        
    Returns:
        List of responses in order of completion
    """
    tasks = [fetch_data(url, random.uniform(0.5, 2.0)) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


async def fetch_with_timeout(url: str, timeout: float) -> Optional[str]:
    """
    Fetch data with a timeout limit.
    
    Args:
        url: URL to fetch
        timeout: Maximum time to wait
        
    Returns:
        Response data or None if timeout
    """
    try:
        return await asyncio.wait_for(fetch_data(url, 3.0), timeout=timeout)
    except asyncio.TimeoutError:
        print(f"Timeout fetching {url}")
        return None


# ==================== ASYNC GENERATORS ====================

async def number_generator(start: int, end: int, delay: float = 0.1) -> AsyncGenerator[int, None]:
    """
    Generate numbers asynchronously with delay.
    
    Args:
        start: Starting number
        end: Ending number
        delay: Delay between each number
        
    Yields:
        Numbers from start to end
    """
    for num in range(start, end + 1):
        await asyncio.sleep(delay)
        yield num


async def process_numbers() -> None:
    """Demonstrate async generator consumption."""
    print("Processing numbers:")
    async for num in number_generator(1, 5, 0.2):
        print(f"  Number: {num}")


# ==================== ASYNC CONTEXT MANAGERS ====================

@asynccontextmanager
async def async_timer(name: str):
    """
    Async context manager for timing operations.
    
    Args:
        name: Name of the operation being timed
    """
    start_time = time.time()
    print(f"[{name}] Starting...")
    try:
        yield
    finally:
        elapsed = time.time() - start_time
        print(f"[{name}] Completed in {elapsed:.2f}s")


@dataclass
class AsyncConnection:
    """Simulated async connection with context manager."""
    host: str
    port: int
    _connected: bool = False
    
    async def connect(self) -> None:
        """Establish connection."""
        print(f"Connecting to {self.host}:{self.port}...")
        await asyncio.sleep(0.5)
        self._connected = True
        print("Connected!")
    
    async def disconnect(self) -> None:
        """Close connection."""
        if self._connected:
            print("Disconnecting...")
            await asyncio.sleep(0.2)
            self._connected = False
            print("Disconnected!")
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()


# ==================== ASYNC QUEUES ====================

async def producer(queue: asyncio.Queue, items: List[str]) -> None:
    """
    Produce items for the queue.
    
    Args:
        queue: Async queue to put items in
        items: Items to produce
    """
    for item in items:
        await asyncio.sleep(random.uniform(0.1, 0.5))
        await queue.put(item)
        print(f"Produced: {item}")


async def consumer(queue: asyncio.Queue, name: str) -> None:
    """
    Consume items from the queue.
    
    Args:
        queue: Async queue to get items from
        name: Name of the consumer
    """
    while True:
        item = await queue.get()
        await asyncio.sleep(random.uniform(0.2, 0.8))
        print(f"{name} consumed: {item}")
        queue.task_done()


async def queue_demo() -> None:
    """Demonstrate async queue with producer-consumer pattern."""
    queue = asyncio.Queue(maxsize=5)
    
    items = [f"item-{i}" for i in range(1, 8)]
    
    # Start producer and consumers
    producer_task = asyncio.create_task(producer(queue, items))
    consumers = [
        asyncio.create_task(consumer(queue, f"Consumer-{i}"))
        for i in range(2)
    ]
    
    # Wait for producer to finish
    await producer_task
    
    # Wait for queue to be empty
    await queue.join()
    
    # Cancel consumers
    for consumer_task in consumers:
        consumer_task.cancel()


# ==================== RATE LIMITING ====================

class RateLimiter:
    """Rate limiter for async operations."""
    
    def __init__(self, rate_limit: float):
        """
        Initialize rate limiter.
        
        Args:
            rate_limit: Maximum requests per second
        """
        self.rate_limit = rate_limit
        self.min_interval = 1.0 / rate_limit
        self.last_call = 0.0
    
    async def acquire(self) -> None:
        """Wait until next request is allowed."""
        now = time.time()
        time_since_last = now - self.last_call
        
        if time_since_last < self.min_interval:
            await asyncio.sleep(self.min_interval - time_since_last)
        
        self.last_call = time.time()


async def rate_limited_request(
    url: str,
    limiter: RateLimiter,
) -> str:
    """
    Make a rate-limited request.
    
    Args:
        url: URL to request
        limiter: Rate limiter instance
        
    Returns:
        Response data
    """
    await limiter.acquire()
    return await fetch_data(url, 0.1)


# ==================== MAIN DEMO ====================

async def main() -> None:
    """Demonstrate async programming patterns."""
    
    # Basic async functions
    print("=== BASIC ASYNC ===")
    async with async_timer("Sequential operations"):
        data1 = await fetch_data("https://api1.com", 1.0)
        data2 = await fetch_data("https://api2.com", 1.0)
        print(f"Results: {data1}, {data2}")
    
    # Concurrent execution
    print("\n=== CONCURRENT EXECUTION ===")
    async with async_timer("Concurrent operations"):
        urls = ["https://api1.com", "https://api2.com", "https://api3.com"]
        results = await fetch_multiple_urls(urls)
        print(f"Concurrent results: {results}")
    
    # Timeout handling
    print("\n=== TIMEOUT HANDLING ===")
    result = await fetch_with_timeout("https://slow-api.com", timeout=0.5)
    print(f"Result with timeout: {result}")
    
    # Async generator
    print("\n=== ASYNC GENERATOR ===")
    await process_numbers()
    
    # Async context manager
    print("\n=== ASYNC CONTEXT MANAGER ===")
    async with AsyncConnection("localhost", 5432):
        print("Performing database operations...")
        await asyncio.sleep(0.3)
    
    # Queue demo
    print("\n=== QUEUE PRODUCER-CONSUMER ===")
    await queue_demo()
    
    # Rate limiting
    print("\n=== RATE LIMITING ===")
    limiter = RateLimiter(rate_limit=3.0)  # 3 requests per second
    urls = [f"https://api{i}.com" for i in range(5)]
    
    async with async_timer("Rate-limited requests"):
        tasks = [rate_limited_request(url, limiter) for url in urls]
        results = await asyncio.gather(*tasks)
        print(f"Rate-limited results: {len(results)} requests completed")


if __name__ == "__main__":
    asyncio.run(main())
