"""
Advanced Python - Lesson 21: Logging & Profiling
==================================================
Proper logging and profiling are essential for debugging,
monitoring, and optimizing production applications.

Topics Covered:
- logging module: levels, handlers, formatters
- Structured logging (JSON)
- Log filters and custom handlers
- Profiling with cProfile and timeit
- Memory profiling
- Custom performance monitoring
- Tracing function calls
"""

import logging
import sys
import time
import io
import json
import functools
import cProfile
import pstats
import tracemalloc
from typing import Any, Callable
from datetime import datetime
from collections import defaultdict


# ============================================================
# 1. BASIC LOGGING SETUP
# ============================================================
def demonstrate_basic_logging():
    """Set up logging with different levels and handlers."""
    
    # Create a logger (not the root logger)
    logger = logging.getLogger("myapp")
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Console handler — shows INFO and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        "%(levelname)-8s | %(name)s | %(message)s"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # String handler (capture to variable for demo)
    log_capture = io.StringIO()
    file_handler = logging.StreamHandler(log_capture)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%H:%M:%S",
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    # Log at different levels
    logger.debug("Database connection pool initialized")
    logger.info("Application started on port 8080")
    logger.warning("Disk usage at 85%")
    logger.error("Failed to connect to cache server")
    logger.critical("Database is unreachable!")
    
    # Log with extra data
    logger.info("User login", extra={"user": "alice", "ip": "192.168.1.1"})
    
    # Show captured logs
    logger.removeHandler(file_handler)
    captured = log_capture.getvalue()
    print(f"\nCaptured {captured.count(chr(10))} log entries:")
    for line in captured.strip().split("\n")[:3]:
        print(f"  {line}")


# ============================================================
# 2. STRUCTURED LOGGING (JSON)
# ============================================================
class JsonFormatter(logging.Formatter):
    """Format log records as JSON for machine parsing."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        # Include any extra fields
        for key in ("user", "request_id", "duration_ms", "status_code"):
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)
        
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)


class StructuredLogger:
    """Logger that produces JSON-formatted log entries."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        self.logger.addHandler(handler)
        
        # Store captured entries for demo
        self._capture = io.StringIO()
        capture_handler = logging.StreamHandler(self._capture)
        capture_handler.setFormatter(JsonFormatter())
        self.logger.addHandler(capture_handler)

    def _log(self, level: int, msg: str, **extra):
        self.logger.log(level, msg, extra=extra)

    def info(self, msg: str, **extra):
        self._log(logging.INFO, msg, **extra)

    def error(self, msg: str, **extra):
        self._log(logging.ERROR, msg, **extra)

    def warning(self, msg: str, **extra):
        self._log(logging.WARNING, msg, **extra)

    def get_captured(self) -> list[dict]:
        entries = []
        for line in self._capture.getvalue().strip().split("\n"):
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return entries


def demonstrate_structured_logging():
    """JSON logging for production environments."""
    
    slog = StructuredLogger("api")
    
    slog.info("Request received", request_id="abc-123", status_code=200)
    slog.info("User authenticated", user="alice", request_id="abc-123")
    slog.warning("Slow query detected", duration_ms=2500, request_id="abc-123")
    slog.error("Payment failed", request_id="abc-124", status_code=500)
    
    print("\nParsed structured logs:")
    for entry in slog.get_captured()[:2]:
        print(f"  {json.dumps(entry, indent=4)}")


# ============================================================
# 3. LOG FILTERS
# ============================================================
class SensitiveDataFilter(logging.Filter):
    """Filter that redacts sensitive information from log messages."""
    
    SENSITIVE_PATTERNS = [
        "password", "secret", "token", "api_key", "ssn",
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for pattern in self.SENSITIVE_PATTERNS:
            if pattern in msg.lower():
                record.msg = f"[REDACTED: contains '{pattern}']"
                return True
        return True


class RateLimitFilter(logging.Filter):
    """Filter that rate-limits repeated log messages."""
    
    def __init__(self, max_per_minute: int = 10):
        super().__init__()
        self.max_per_minute = max_per_minute
        self.message_times: dict[str, list[float]] = defaultdict(list)

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        now = time.time()
        
        # Clean old entries
        self.message_times[msg] = [
            t for t in self.message_times[msg] if now - t < 60
        ]
        
        if len(self.message_times[msg]) >= self.max_per_minute:
            return False  # Suppress
        
        self.message_times[msg].append(now)
        return True


def demonstrate_filters():
    """Log filters control which messages get logged."""
    
    logger = logging.getLogger("secure_app")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    handler.addFilter(SensitiveDataFilter())
    logger.addHandler(handler)
    
    print("Sensitive data filter:")
    logger.info("User alice logged in")
    logger.info("User password is abc123")
    logger.info("API token: sk-12345")
    logger.info("Request completed successfully")


# ============================================================
# 4. PROFILING WITH cProfile
# ============================================================
def slow_function_a():
    """A deliberately slow function."""
    total = 0
    for i in range(500_000):
        total += i * i
    return total


def slow_function_b():
    """Another slow function."""
    data = [str(i) for i in range(100_000)]
    return len(data)


def slow_function_c():
    """Function with string operations."""
    result = ""
    for i in range(10_000):
        result += str(i)
    return len(result)


def profile_code():
    """Profile code using cProfile."""
    
    # Profile a set of functions
    profiler = cProfile.Profile()
    profiler.enable()
    
    slow_function_a()
    slow_function_b()
    slow_function_c()
    
    profiler.disable()
    
    # Print stats
    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    
    print("Top 10 functions by cumulative time:")
    stream = io.StringIO()
    stats_stream = pstats.Stats(profiler, stream=stream)
    stats_stream.sort_stats("cumulative")
    stats_stream.print_stats(10)
    
    for line in stream.getvalue().strip().split("\n")[:15]:
        print(f"  {line}")


# ============================================================
# 5. TIMING DECORATORS
# ============================================================
class TimingStats:
    """Collect timing statistics across function calls."""
    
    def __init__(self):
        self.call_times: dict[str, list[float]] = defaultdict(list)

    def record(self, func_name: str, elapsed: float):
        self.call_times[func_name].append(elapsed)

    def report(self) -> str:
        lines = ["Function Timing Report:"]
        lines.append(f"  {'Function':<25} {'Calls':>6} {'Avg (ms)':>10} {'Total (ms)':>12}")
        lines.append(f"  {'-'*55}")
        
        for name, times in sorted(self.call_times.items()):
            avg = sum(times) / len(times) * 1000
            total = sum(times) * 1000
            lines.append(f"  {name:<25} {len(times):>6} {avg:>10.2f} {total:>12.2f}")
        
        return "\n".join(lines)


# Global timing stats
_timing_stats = TimingStats()


def timed(func: Callable) -> Callable:
    """Decorator that times function execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        _timing_stats.record(func.__name__, elapsed)
        return result
    return wrapper


@timed
def compute_sum(n: int) -> int:
    """Sum using a loop."""
    total = 0
    for i in range(n):
        total += i
    return total


@timed
def compute_sum_formula(n: int) -> int:
    """Sum using Gauss formula."""
    return n * (n - 1) // 2


@timed
def compute_sum_builtin(n: int) -> int:
    """Sum using Python built-in."""
    return sum(range(n))


def demonstrate_timing():
    """Compare performance of different approaches."""
    
    n = 1_000_000
    
    for _ in range(5):
        compute_sum(n)
        compute_sum_formula(n)
        compute_sum_builtin(n)
    
    print(_timing_stats.report())


# ============================================================
# 6. MEMORY PROFILING
# ============================================================
def demonstrate_memory_profiling():
    """Use tracemalloc to track memory allocations."""
    
    tracemalloc.start()
    
    # Take initial snapshot
    snapshot1 = tracemalloc.take_snapshot()
    
    # Allocate some memory
    data1 = [i ** 2 for i in range(100_000)]
    data2 = {"key_" + str(i): f"value_{i}" for i in range(50_000)}
    data3 = [[j for j in range(100)] for i in range(1_000)]
    
    # Take second snapshot
    snapshot2 = tracemalloc.take_snapshot()
    
    # Compare snapshots
    stats = snapshot2.compare_to(snapshot1, "lineno")
    
    print("Top memory allocations:")
    for stat in stats[:5]:
        print(f"  {stat}")
    
    # Current memory usage
    current, peak = tracemalloc.get_traced_memory()
    print(f"\n  Current memory: {current / 1024 / 1024:.2f} MB")
    print(f"  Peak memory:    {peak / 1024 / 1024:.2f} MB")
    
    tracemalloc.stop()


# ============================================================
# 7. FUNCTION TRACING
# ============================================================
class FunctionTracer:
    """Trace function calls, arguments, and return values."""
    
    def __init__(self):
        self.call_log: list[dict] = []

    def trace(self, func: Callable) -> Callable:
        """Decorator that traces function calls."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            call_info = {
                "function": func.__name__,
                "args": args,
                "kwargs": kwargs,
                "timestamp": datetime.now().isoformat(),
            }
            
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                call_info["return"] = result
                call_info["status"] = "success"
            except Exception as e:
                call_info["error"] = str(e)
                call_info["status"] = "error"
                result = None
            finally:
                call_info["duration_ms"] = (time.perf_counter() - start) * 1000
                self.call_log.append(call_info)
            
            return result
        return wrapper

    def summary(self) -> str:
        lines = ["Call Trace Summary:"]
        for entry in self.call_log:
            status = entry["status"]
            icon = "OK" if status == "success" else "ERR"
            args_str = ", ".join(str(a) for a in entry["args"])
            ret = entry.get("return", entry.get("error", ""))
            lines.append(
                f"  [{icon}] {entry['function']}({args_str}) "
                f"-> {ret} ({entry['duration_ms']:.2f}ms)"
            )
        return "\n".join(lines)


def demonstrate_tracing():
    """Trace function execution for debugging."""
    
    tracer = FunctionTracer()
    
    @tracer.trace
    def add(a: int, b: int) -> int:
        return a + b
    
    @tracer.trace
    def divide(a: float, b: float) -> float:
        return a / b
    
    @tracer.trace
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    add(10, 20)
    add(100, 200)
    divide(10, 3)
    greet("Alice")
    
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass  # Expected
    
    print(tracer.summary())


# ============================================================
# 8. PERFORMANCE MONITOR
# ============================================================
class PerformanceMonitor:
    """Comprehensive performance monitoring context manager."""
    
    def __init__(self, label: str = "Block"):
        self.label = label
        self.start_time: float = 0
        self.elapsed: float = 0
        self.memory_before: int = 0
        self.memory_after: int = 0

    def __enter__(self):
        tracemalloc.start()
        self.memory_before = tracemalloc.get_traced_memory()[0]
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start_time
        self.memory_after = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()
        
        print(f"\n--- Performance: {self.label} ---")
        print(f"  Time:    {self.elapsed * 1000:.2f} ms")
        print(f"  Memory:  {(self.memory_after - self.memory_before) / 1024:.2f} KB")
        return False


def demonstrate_perf_monitor():
    """All-in-one performance monitoring."""
    
    with PerformanceMonitor("List comprehension"):
        data = [i ** 2 for i in range(500_000)]
    
    with PerformanceMonitor("Generator expression"):
        gen = (i ** 2 for i in range(500_000))
        total = sum(gen)
    
    with PerformanceMonitor("Dict creation"):
        d = {f"key_{i}": i * i for i in range(200_000)}
    
    with PerformanceMonitor("String concatenation"):
        result = ""
        for i in range(10_000):
            result += str(i)


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Basic Logging")
    demonstrate_basic_logging()

    separator("2. Structured (JSON) Logging")
    demonstrate_structured_logging()

    separator("3. Log Filters")
    demonstrate_filters()

    separator("4. Profiling with cProfile")
    profile_code()

    separator("5. Timing Decorators")
    demonstrate_timing()

    separator("6. Memory Profiling")
    demonstrate_memory_profiling()

    separator("7. Function Tracing")
    demonstrate_tracing()

    separator("8. Performance Monitor")
    demonstrate_perf_monitor()


if __name__ == "__main__":
    main()
