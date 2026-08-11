"""
Advanced Python - Lesson 12: Multithreading & Multiprocessing
==============================================================
Concurrency allows multiple operations to happen simultaneously.
Python offers threading (I/O-bound) and multiprocessing (CPU-bound).

Topics Covered:
- threading.Thread basics
- ThreadPoolExecutor (concurrent.futures)
- ProcessPoolExecutor for CPU-bound tasks
- Thread synchronization (Lock, Event, Barrier)
- Producer-consumer with queues
- Daemon threads
- GIL (Global Interpreter Lock) awareness
"""

import threading
import time
import concurrent.futures
import queue
import random
import os
from typing import Any


# ============================================================
# 1. BASIC THREADING
# ============================================================
def worker(name: str, duration: float):
    """A simple worker function that simulates work."""
    print(f"  [{name}] Starting (thread: {threading.current_thread().name})")
    time.sleep(duration)
    print(f"  [{name}] Finished after {duration}s")


def demonstrate_basic_threading():
    """Create and manage threads manually."""
    
    threads = []
    for i in range(3):
        t = threading.Thread(
            target=worker,
            args=(f"Worker-{i+1}", random.uniform(0.2, 0.5)),
            name=f"Thread-{i+1}",
        )
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print("  All threads completed!")


# ============================================================
# 2. THREAD POOL EXECUTOR
# ============================================================
def fetch_url(url: str) -> dict:
    """Simulate fetching a URL (I/O-bound task)."""
    delay = random.uniform(0.1, 0.4)
    time.sleep(delay)
    return {"url": url, "status": 200, "time": f"{delay:.2f}s"}


def demonstrate_thread_pool():
    """ThreadPoolExecutor manages a pool of worker threads."""
    
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/posts",
        "https://api.example.com/comments",
        "https://api.example.com/likes",
        "https://api.example.com/shares",
    ]
    
    print(f"Fetching {len(urls)} URLs with thread pool:")
    start = time.perf_counter()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        future_to_url = {
            executor.submit(fetch_url, url): url for url in urls
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                print(f"  {result}")
            except Exception as e:
                print(f"  {url} failed: {e}")
    
    elapsed = time.perf_counter() - start
    print(f"\n  Total time: {elapsed:.2f}s (parallel!)")


def demonstrate_map():
    """executor.map is like the built-in map but parallel."""
    
    def square(x: int) -> int:
        time.sleep(0.05)
        return x ** 2
    
    numbers = list(range(1, 11))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(square, numbers))
    
    print(f"Input:  {numbers}")
    print(f"Squared: {results}")


# ============================================================
# 3. MULTIPROCESSING (CPU-BOUND TASKS)
# ============================================================
def cpu_intensive_task(n: int) -> int:
    """A CPU-heavy computation (not affected by GIL)."""
    result = 0
    for i in range(n):
        result += i * i
    return result


def demonstrate_multiprocessing():
    """ProcessPoolExecutor uses separate processes (bypasses GIL).
    
    Use for CPU-bound tasks: math, image processing, data analysis.
    Use ThreadPoolExecutor for I/O-bound tasks: network, file I/O.
    """
    
    task_sizes = [2_000_000, 2_000_000, 2_000_000, 2_000_000]
    
    # Sequential
    start = time.perf_counter()
    seq_results = [cpu_intensive_task(n) for n in task_sizes]
    seq_time = time.perf_counter() - start
    print(f"Sequential: {seq_time:.2f}s")
    
    # Parallel (multiprocessing)
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        par_results = list(executor.map(cpu_intensive_task, task_sizes))
    par_time = time.perf_counter() - start
    print(f"Parallel:   {par_time:.2f}s")
    
    print(f"Speedup:    {seq_time / par_time:.1f}x")
    print(f"Results match: {seq_results == par_results}")


# ============================================================
# 4. THREAD SYNCHRONIZATION - LOCK
# ============================================================
class SharedCounter:
    """Thread-safe counter using a lock."""
    
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:  # Acquire and release automatically
            self._value += 1

    def decrement(self):
        with self._lock:
            self._value -= 1

    @property
    def value(self) -> int:
        with self._lock:
            return self._value


def demonstrate_lock():
    """Locks prevent race conditions in shared mutable state."""
    
    counter = SharedCounter()
    
    def increment_many(times: int):
        for _ in range(times):
            counter.increment()
    
    threads = [
        threading.Thread(target=increment_many, args=(10_000,))
        for _ in range(10)
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"Expected: 100000, Actual: {counter.value}")
    print(f"Thread-safe: {counter.value == 100000}")


# ============================================================
# 5. THREAD EVENT (Signal between threads)
# ============================================================
def demonstrate_event():
    """Event allows one thread to signal others."""
    
    data_ready = threading.Event()
    results = []
    
    def producer():
        print("  [Producer] Loading data...")
        time.sleep(0.3)
        results.extend([1, 2, 3, 4, 5])
        print("  [Producer] Data ready! Signaling consumers.")
        data_ready.set()
    
    def consumer(name: str):
        print(f"  [{name}] Waiting for data...")
        data_ready.wait()  # Block until event is set
        print(f"  [{name}] Got data: {results}")
    
    prod = threading.Thread(target=producer)
    consumers = [
        threading.Thread(target=consumer, args=(f"Consumer-{i}",))
        for i in range(1, 4)
    ]
    
    # Start consumers first (they'll wait)
    for c in consumers:
        c.start()
    
    time.sleep(0.1)  # Let consumers start waiting
    prod.start()
    
    prod.join()
    for c in consumers:
        c.join()


# ============================================================
# 6. PRODUCER-CONSUMER WITH QUEUE
# ============================================================
def demonstrate_queue():
    """Thread-safe queue for producer-consumer pattern."""
    
    task_queue: queue.Queue = queue.Queue(maxsize=5)
    results: list = []
    results_lock = threading.Lock()
    
    def producer(name: str, count: int):
        for i in range(count):
            item = f"{name}-task-{i+1}"
            task_queue.put(item)
            print(f"  [{name}] Produced: {item}")
            time.sleep(0.05)
    
    def consumer(name: str):
        while True:
            item = task_queue.get()
            if item is None:  # Sentinel: stop signal
                task_queue.task_done()
                break
            # Process the item
            processed = f"Processed({item})"
            with results_lock:
                results.append(processed)
            print(f"  [{name}] {processed}")
            task_queue.task_done()
            time.sleep(0.08)
    
    # Start consumers
    consumers = [
        threading.Thread(target=consumer, args=(f"Worker-{i}",))
        for i in range(1, 3)
    ]
    for c in consumers:
        c.start()
    
    # Start producers
    producers = [
        threading.Thread(target=producer, args=(f"Producer-{i}", 4))
        for i in range(1, 3)
    ]
    for p in producers:
        p.start()
    
    # Wait for producers to finish
    for p in producers:
        p.join()
    
    # Send stop signals
    for _ in consumers:
        task_queue.put(None)
    
    # Wait for consumers
    for c in consumers:
        c.join()
    
    print(f"\n  Total processed: {len(results)} items")


# ============================================================
# 7. BARRIER (Synchronization Point)
# ============================================================
def demonstrate_barrier():
    """Barrier makes threads wait for each other at a point."""
    
    num_threads = 3
    barrier = threading.Barrier(num_threads)
    
    def phase_worker(name: str, phase: int):
        print(f"  [{name}] Phase {phase}: working...")
        time.sleep(random.uniform(0.1, 0.3))
        print(f"  [{name}] Phase {phase}: done, waiting at barrier")
        barrier.wait()  # Wait for all threads
        print(f"  [{name}] Phase {phase}: barrier passed!")
    
    print("Phase 1:")
    threads = [
        threading.Thread(target=phase_worker, args=(f"W-{i}", 1))
        for i in range(1, num_threads + 1)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# ============================================================
# 8. DAEMON THREADS
# ============================================================
def demonstrate_daemon():
    """Daemon threads run in the background and die with the main thread."""
    
    def background_monitor():
        count = 0
        while True:
            count += 1
            print(f"  [Monitor] Heartbeat #{count}")
            time.sleep(0.2)
    
    monitor = threading.Thread(target=background_monitor, daemon=True)
    monitor.start()
    
    # Main thread does some work
    print("  [Main] Doing work...")
    time.sleep(0.5)
    print("  [Main] Work done. Daemon will be killed when main exits.")
    print(f"  Monitor is daemon: {monitor.daemon}")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Basic Threading")
    demonstrate_basic_threading()

    separator("2. Thread Pool Executor")
    demonstrate_thread_pool()
    print()
    demonstrate_map()

    separator("3. Multiprocessing (CPU-Bound)")
    demonstrate_multiprocessing()

    separator("4. Thread Lock (Race Condition Prevention)")
    demonstrate_lock()

    separator("5. Thread Event (Signaling)")
    demonstrate_event()

    separator("6. Producer-Consumer Queue")
    demonstrate_queue()

    separator("7. Barrier (Sync Point)")
    demonstrate_barrier()

    separator("8. Daemon Threads")
    demonstrate_daemon()

    print(f"\n{'='*60}")
    print("  Key Takeaways:")
    print("  - Use THREADS for I/O-bound tasks (network, files)")
    print("  - Use PROCESSES for CPU-bound tasks (math, data)")
    print("  - Always use locks for shared mutable state")
    print("  - GIL prevents true parallel threads in CPython")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
