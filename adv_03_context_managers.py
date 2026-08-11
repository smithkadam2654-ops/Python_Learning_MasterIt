"""
Advanced Python - Lesson 03: Context Managers
===============================================
Context managers handle setup and teardown of resources automatically.
They ensure proper cleanup even when exceptions occur.

Topics Covered:
- with statement recap
- Custom context managers (class-based)
- Custom context managers (generator-based with @contextmanager)
- Nested context managers
- Async context managers
- Real-world patterns: file locking, database connections, timers
"""

import time
import tempfile
import os
from contextlib import contextmanager, ExitStack
from typing import Generator, Any


# ============================================================
# 1. CLASS-BASED CONTEXT MANAGER
# ============================================================
class Timer:
    """Context manager that measures elapsed time of a code block."""
    
    def __init__(self, label: str = "Block"):
        self.label = label
        self.start_time: float = 0
        self.elapsed: float = 0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self  # Return self so we can access elapsed time

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start_time
        print(f"[{self.label}] Elapsed: {self.elapsed:.6f}s")
        return False  # Don't suppress exceptions


class FileLock:
    """Context manager for file locking (simulated).
    
    Demonstrates resource acquisition and release patterns.
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.lock_file = filename + ".lock"
        self.acquired = False

    def __enter__(self):
        if os.path.exists(self.lock_file):
            raise RuntimeError(f"Lock already held: {self.lock_file}")
        # Create lock file
        with open(self.lock_file, "w") as f:
            f.write(str(os.getpid()))
        self.acquired = True
        print(f"Lock acquired: {self.filename}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.acquired and os.path.exists(self.lock_file):
            os.remove(self.lock_file)
            self.acquired = False
            print(f"Lock released: {self.filename}")
        return False


class DatabaseConnection:
    """Simulated database connection context manager.
    
    Shows proper connection lifecycle management.
    """
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False
        self.transaction_active = False

    def __enter__(self):
        print(f"Connecting to: {self.connection_string}")
        self.connected = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.transaction_active:
            if exc_type is not None:
                self.rollback()
            else:
                self.commit()
        print(f"Disconnecting from: {self.connection_string}")
        self.connected = False
        return False  # Let exceptions propagate

    def execute(self, query: str) -> str:
        if not self.connected:
            raise RuntimeError("Not connected")
        print(f"  Executing: {query}")
        return f"Result of: {query}"

    def begin_transaction(self):
        self.transaction_active = True
        print("  Transaction started")

    def commit(self):
        self.transaction_active = False
        print("  Transaction COMMITTED")

    def rollback(self):
        self.transaction_active = False
        print("  Transaction ROLLED BACK")


# ============================================================
# 2. GENERATOR-BASED CONTEXT MANAGERS (@contextmanager)
# ============================================================
@contextmanager
def temporary_file(suffix: str = ".txt"):
    """Context manager for temporary files with automatic cleanup.
    
    The yield value becomes the 'as' variable in the with statement.
    Code after yield runs during cleanup (like __exit__).
    """
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=suffix, delete=False
    )
    try:
        print(f"Created temp file: {tmp.name}")
        yield tmp  # Hand control to the with block
    finally:
        tmp.close()
        os.unlink(tmp.name)
        print(f"Cleaned up temp file: {tmp.name}")


@contextmanager
def suppressed_exceptions(*exception_types):
    """Context manager that suppresses specific exception types.
    
    Similar to contextlib.suppress but custom-built.
    """
    try:
        yield
    except exception_types as e:
        print(f"Suppressed {type(e).__name__}: {e}")


@contextmanager
def working_directory(path: str):
    """Temporarily change the working directory, then restore it."""
    original_dir = os.getcwd()
    try:
        os.chdir(path)
        print(f"Changed directory to: {path}")
        yield path
    finally:
        os.chdir(original_dir)
        print(f"Restored directory to: {original_dir}")


@contextmanager
def tag(name: str, **attrs):
    """Context manager that wraps output in an HTML-like tag."""
    attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    if attr_str:
        print(f"<{name} {attr_str}>")
    else:
        print(f"<{name}>")
    yield
    print(f"</{name}>")


# ============================================================
# 3. NESTED CONTEXT MANAGERS WITH EXITSTACK
# ============================================================
@contextmanager
def managed_resource(name: str):
    """Generic resource with setup/teardown logging."""
    print(f"  [SETUP] {name}")
    yield name
    print(f"  [TEARDOWN] {name}")


def demonstrate_exit_stack():
    """ExitStack manages a dynamic number of context managers.
    
    Useful when the number of resources is not known at compile time.
    """
    resources = ["Database", "Cache", "MessageQueue", "FileHandle"]

    print("Opening all resources with ExitStack:")
    with ExitStack() as stack:
        handles = [
            stack.enter_context(managed_resource(r)) for r in resources
        ]
        print(f"\n  Active resources: {handles}")
        print("  ... doing work with all resources ...\n")
    print("\nAll resources cleaned up!")


# ============================================================
# 4. ASYNC CONTEXT MANAGERS
# ============================================================
import asyncio


class AsyncDatabase:
    """Async context manager for simulated database operations.
    
    Uses __aenter__ and __aexit__ for async setup/teardown.
    """
    def __init__(self, host: str):
        self.host = host

    async def __aenter__(self):
        print(f"Async connecting to {self.host}...")
        await asyncio.sleep(0.1)  # Simulate network delay
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"Async disconnecting from {self.host}...")
        await asyncio.sleep(0.05)
        return False

    async def query(self, sql: str) -> list:
        print(f"  Async executing: {sql}")
        await asyncio.sleep(0.05)
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


@contextmanager
def async_timer(label: str) -> Generator:
    """Sync context manager that can be used in async code."""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"[{label}] Async elapsed: {elapsed:.4f}s")


async def async_demo():
    """Demonstrate async context managers."""
    async with AsyncDatabase("localhost:5432") as db:
        results = await db.query("SELECT * FROM users")
        print(f"  Query results: {results}")


# ============================================================
# 5. REAL-WORLD PATTERN: RESOURCE POOL
# ============================================================
class ResourcePool:
    """A simple resource pool context manager.
    
    Manages a pool of reusable resources (e.g., connections).
    """
    def __init__(self, size: int = 3):
        self.size = size
        self._pool: list[str] = [f"Resource-{i+1}" for i in range(size)]
        self._in_use: set[str] = set()

    @contextmanager
    def acquire(self):
        """Acquire a resource from the pool, return it when done."""
        if not self._pool:
            raise RuntimeError("No resources available in pool")
        resource = self._pool.pop()
        self._in_use.add(resource)
        print(f"  Acquired: {resource} (available: {len(self._pool)})")
        try:
            yield resource
        finally:
            self._pool.append(resource)
            self._in_use.discard(resource)
            print(f"  Released: {resource} (available: {len(self._pool)})")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Timer Context Manager")
    with Timer("Sum 1M numbers") as t:
        total = sum(range(1_000_000))
    print(f"Sum = {total:,} (took {t.elapsed:.6f}s)")

    separator("2. Database Connection")
    # Successful transaction
    with DatabaseConnection("postgres://localhost/mydb") as db:
        db.begin_transaction()
        db.execute("INSERT INTO users VALUES ('Alice')")
        db.execute("UPDATE accounts SET balance = 100")

    print()
    # Failed transaction (rollback)
    try:
        with DatabaseConnection("postgres://localhost/mydb") as db:
            db.begin_transaction()
            db.execute("INSERT INTO users VALUES ('Bob')")
            raise ValueError("Something went wrong!")
    except ValueError:
        print("  Caught the error after rollback")

    separator("3. Temporary File")
    with temporary_file(".csv") as tmp:
        tmp.write("name,age\nAlice,30\nBob,25\n")
        tmp.flush()
        print(f"Wrote data to: {tmp.name}")

    separator("4. Exception Suppression")
    with suppressed_exceptions(ValueError, TypeError):
        int("not a number")
    print("Program continues after suppressed exception")

    separator("5. HTML Tag Wrapper")
    with tag("div", class_="container", id="main"):
        with tag("h1"):
            print("  Hello, World!")
        with tag("p"):
            print("  This is a paragraph.")

    separator("6. ExitStack (Dynamic Resources)")
    demonstrate_exit_stack()

    separator("7. Resource Pool")
    pool = ResourcePool(size=3)
    with pool.acquire() as r1:
        print(f"  Using: {r1}")
        with pool.acquire() as r2:
            print(f"  Using: {r2}")
    print("All resources returned to pool")

    separator("8. Async Context Manager")
    asyncio.run(async_demo())


if __name__ == "__main__":
    main()
