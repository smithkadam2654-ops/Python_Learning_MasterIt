"""
Advanced Python - Lesson 06: Async/Await & Asyncio
====================================================
Asynchronous programming allows concurrent execution of I/O-bound tasks
without the overhead of threads or processes.

Topics Covered:
- async/await basics
- Running coroutines with asyncio.run()
- Concurrent execution with asyncio.gather()
- asyncio.create_task for background work
- Async iterators and generators
- Async context managers
- Timeouts and cancellation
- Semaphore for rate limiting
"""

import asyncio
import time
import random
from typing import AsyncGenerator


# ============================================================
# 1. BASIC ASYNC FUNCTIONS
# ============================================================
async def greet_async(name: str) -> str:
    """A simple async function (coroutine).
    
    'async def' defines a coroutine.
    'await' pauses execution until the awaited coroutine completes.
    """
    await asyncio.sleep(0.1)  # Simulate I/O delay
    return f"Hello, {name}!"


async def fetch_data(url: str, delay: float = 0.5) -> dict:
    """Simulate fetching data from a URL."""
    print(f"  Fetching {url}...")
    await asyncio.sleep(delay)  # Simulate network delay
    return {"url": url, "status": 200, "data": f"Content from {url}"}


# ============================================================
# 2. CONCURRENT EXECUTION WITH GATHER
# ============================================================
async def sequential_fetch():
    """Fetch data sequentially — one at a time (slow)."""
    start = time.perf_counter()
    
    result1 = await fetch_data("https://api.example.com/users", 0.3)
    result2 = await fetch_data("https://api.example.com/posts", 0.3)
    result3 = await fetch_data("https://api.example.com/comments", 0.3)
    
    elapsed = time.perf_counter() - start
    print(f"  Sequential: {elapsed:.2f}s for 3 requests")
    return [result1, result2, result3]


async def concurrent_fetch():
    """Fetch data concurrently — all at once (fast).
    
    asyncio.gather() runs multiple coroutines concurrently
    and collects their results.
    """
    start = time.perf_counter()
    
    results = await asyncio.gather(
        fetch_data("https://api.example.com/users", 0.3),
        fetch_data("https://api.example.com/posts", 0.3),
        fetch_data("https://api.example.com/comments", 0.3),
    )
    
    elapsed = time.perf_counter() - start
    print(f"  Concurrent: {elapsed:.2f}s for 3 requests")
    return results


# ============================================================
# 3. TASKS AND BACKGROUND WORK
# ============================================================
async def background_logger(interval: float, max_count: int):
    """A coroutine that logs periodically (background task)."""
    for i in range(max_count):
        print(f"  [LOG] Background task tick #{i + 1}")
        await asyncio.sleep(interval)


async def demonstrate_tasks():
    """Show how to create and manage async tasks."""
    
    # Create a background task
    task = asyncio.create_task(background_logger(0.2, 3))
    
    # Do other work while the task runs in the background
    print("  Main task: doing work...")
    await asyncio.sleep(0.3)
    print("  Main task: more work...")
    
    # Wait for the background task to finish
    await task
    print("  Background task completed!")


# ============================================================
# 4. ASYNC ITERATOR AND GENERATOR
# ============================================================
async def async_range(start: int, stop: int, delay: float = 0.05) -> AsyncGenerator[int, None]:
    """Async generator that yields numbers with a delay between each.
    
    Use 'async for' to consume async generators.
    """
    for i in range(start, stop):
        await asyncio.sleep(delay)
        yield i


async def async_data_stream(count: int) -> AsyncGenerator[dict, None]:
    """Simulate an async data stream (e.g., websocket, SSE)."""
    for i in range(count):
        await asyncio.sleep(0.1)
        yield {
            "id": i + 1,
            "timestamp": time.time(),
            "value": random.randint(1, 100),
        }


async def consume_stream():
    """Consume an async data stream."""
    print("  Consuming async data stream:")
    async for item in async_data_stream(5):
        print(f"    Received: {item}")


# ============================================================
# 5. TIMEOUTS AND CANCELLATION
# ============================================================
async def slow_operation() -> str:
    """An operation that takes too long."""
    await asyncio.sleep(5)
    return "Done (but too late)"


async def demonstrate_timeout():
    """Use asyncio.wait_for to add timeouts to coroutines."""
    
    print("  Attempting operation with 1s timeout...")
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=1.0)
        print(f"  Result: {result}")
    except asyncio.TimeoutError:
        print("  Operation timed out! (as expected)")


async def demonstrate_cancellation():
    """Cancel a running task."""
    
    task = asyncio.create_task(slow_operation())
    
    await asyncio.sleep(0.2)
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("  Task was cancelled successfully")


# ============================================================
# 6. SEMAPHORE FOR RATE LIMITING
# ============================================================
async def fetch_with_limit(semaphore: asyncio.Semaphore, url: str) -> dict:
    """Fetch data with a concurrency limit using a semaphore."""
    async with semaphore:
        print(f"  Fetching {url} (slots available: {semaphore._value})")
        await asyncio.sleep(random.uniform(0.1, 0.3))
        return {"url": url, "status": 200}


async def demonstrate_semaphore():
    """Limit concurrent requests using a semaphore."""
    
    urls = [f"https://api.example.com/page/{i}" for i in range(1, 9)]
    
    # Allow at most 3 concurrent requests
    semaphore = asyncio.Semaphore(3)
    
    print(f"  Fetching {len(urls)} URLs with max 3 concurrent:")
    tasks = [fetch_with_limit(semaphore, url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(f"  All {len(results)} requests completed!")


# ============================================================
# 7. ASYNC PRODUCER-CONSUMER
# ============================================================
async def producer(queue: asyncio.Queue, count: int):
    """Produce items and put them in the queue."""
    for i in range(count):
        item = f"item-{i + 1}"
        await queue.put(item)
        print(f"  [PRODUCER] Produced: {item}")
        await asyncio.sleep(0.1)
    # Signal completion
    await queue.put(None)
    print("  [PRODUCER] Done producing")


async def consumer(queue: asyncio.Queue):
    """Consume items from the queue."""
    while True:
        item = await queue.get()
        if item is None:
            print("  [CONSUMER] Received stop signal")
            break
        print(f"  [CONSUMER] Processing: {item}")
        await asyncio.sleep(0.15)
        queue.task_done()
    print("  [CONSUMER] Done consuming")


async def demonstrate_producer_consumer():
    """Classic producer-consumer pattern with asyncio.Queue."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=3)
    
    prod = asyncio.create_task(producer(queue, 5))
    cons = asyncio.create_task(consumer(queue))
    
    await asyncio.gather(prod, cons)


# ============================================================
# 8. ERROR HANDLING IN ASYNC CODE
# ============================================================
async def risky_fetch(url: str) -> dict:
    """Simulate a fetch that might fail."""
    if "error" in url:
        raise ConnectionError(f"Failed to fetch {url}")
    await asyncio.sleep(0.1)
    return {"url": url, "status": 200}


async def safe_gather(*coros):
    """Run coroutines concurrently, catching individual failures.
    
    return_exceptions=True makes gather return exceptions
    instead of raising them.
    """
    results = await asyncio.gather(*coros, return_exceptions=True)
    
    successes = []
    failures = []
    
    for r in results:
        if isinstance(r, Exception):
            failures.append(r)
        else:
            successes.append(r)
    
    return successes, failures


async def demonstrate_error_handling():
    """Handle errors in concurrent async operations."""
    
    successes, failures = await safe_gather(
        risky_fetch("https://api.example.com/good1"),
        risky_fetch("https://api.example.com/error"),
        risky_fetch("https://api.example.com/good2"),
        risky_fetch("https://api.example.com/error2"),
    )
    
    print(f"  Successes: {len(successes)}")
    for s in successes:
        print(f"    {s}")
    print(f"  Failures:  {len(failures)}")
    for f in failures:
        print(f"    {type(f).__name__}: {f}")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


async def main():
    separator("1. Basic Async")
    greeting = await greet_async("Python")
    print(f"  {greeting}")

    separator("2. Sequential vs Concurrent")
    await sequential_fetch()
    await concurrent_fetch()

    separator("3. Tasks")
    await demonstrate_tasks()

    separator("4. Async Iterators")
    print("  Async range(1, 6):")
    async for num in async_range(1, 6):
        print(f"    {num}", end="")
    print()
    await consume_stream()

    separator("5. Timeouts & Cancellation")
    await demonstrate_timeout()
    await demonstrate_cancellation()

    separator("6. Semaphore (Rate Limiting)")
    await demonstrate_semaphore()

    separator("7. Producer-Consumer")
    await demonstrate_producer_consumer()

    separator("8. Error Handling")
    await demonstrate_error_handling()


if __name__ == "__main__":
    asyncio.run(main())
