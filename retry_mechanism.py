"""
Retry Mechanism - Retry logic with exponential backoff and jitter.
Features: Configurable retry attempts, backoff strategies, and error handling.
"""

import time
import random
from typing import Callable, Optional, List, Type, Tuple
from dataclasses import dataclass
from enum import Enum
import functools


class BackoffStrategy(Enum):
    """Backoff strategies for retry logic."""
    FIXED = "fixed"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    EXPONENTIAL_WITH_JITTER = "exponential_with_jitter"


@dataclass
class RetryConfig:
    """Configuration for retry mechanism."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    backoff_multiplier: float = 2.0
    strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL
    jitter: bool = True
    retry_on: Tuple[Type[Exception], ...] = (Exception,)


class RetryResult:
    """Result of retry operation."""
    
    def __init__(self, success: bool, attempts: int, 
                 total_time: float, last_error: Optional[Exception] = None) -> None:
        """
        Initialize retry result.
        
        Args:
            success: Whether operation succeeded
            attempts: Number of attempts made
            total_time: Total time spent retrying
            last_error: Last error if failed
        """
        self.success = success
        self.attempts = attempts
        self.total_time = total_time
        self.last_error = last_error
    
    def __str__(self) -> str:
        """String representation."""
        status = "SUCCESS" if self.success else "FAILED"
        return f"RetryResult({status}, attempts={self.attempts}, time={self.total_time:.2f}s)"


class RetryMechanism:
    """Retry mechanism with configurable backoff."""
    
    def __init__(self, config: Optional[RetryConfig] = None) -> None:
        """
        Initialize retry mechanism.
        
        Args:
            config: Retry configuration
        """
        self.config = config or RetryConfig()
    
    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for given attempt.
        
        Args:
            attempt: Attempt number (1-indexed)
            
        Returns:
            Delay in seconds
        """
        strategy = self.config.strategy
        
        if strategy == BackoffStrategy.FIXED:
            delay = self.config.base_delay
        
        elif strategy == BackoffStrategy.LINEAR:
            delay = self.config.base_delay * attempt
        
        elif strategy == BackoffStrategy.EXPONENTIAL:
            delay = self.config.base_delay * (self.config.backoff_multiplier ** (attempt - 1))
        
        elif strategy == BackoffStrategy.EXPONENTIAL_WITH_JITTER:
            base_delay = self.config.base_delay * (self.config.backoff_multiplier ** (attempt - 1))
            # Add jitter: ±25% of base delay
            jitter_amount = base_delay * 0.25
            delay = base_delay + random.uniform(-jitter_amount, jitter_amount)
        
        else:
            delay = self.config.base_delay
        
        return min(delay, self.config.max_delay)
    
    def execute(self, func: Callable, *args, **kwargs) -> RetryResult:
        """
        Execute function with retry logic.
        
        Args:
            func: Function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            RetryResult with execution details
        """
        start_time = time.time()
        last_error = None
        
        for attempt in range(1, self.config.max_attempts + 1):
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                return RetryResult(success=True, attempts=attempt, total_time=elapsed)
                
            except Exception as e:
                last_error = e
                
                # Check if error should trigger retry
                if not isinstance(e, self.config.retry_on):
                    elapsed = time.time() - start_time
                    return RetryResult(success=False, attempts=attempt, total_time=elapsed, last_error=e)
                
                # Don't delay after last attempt
                if attempt < self.config.max_attempts:
                    delay = self.calculate_delay(attempt)
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay:.2f}s...")
                    time.sleep(delay)
        
        elapsed = time.time() - start_time
        return RetryResult(success=False, attempts=self.config.max_attempts, total_time=elapsed, last_error=last_error)


def retry(max_attempts: int = 3, base_delay: float = 1.0, 
          strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL,
          retry_on: Tuple[Type[Exception], ...] = (Exception,)) -> Callable:
    """
    Decorator for retry logic.
    
    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay between retries
        strategy: Backoff strategy
        retry_on: Tuple of exception types to retry on
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        config = RetryConfig(
            max_attempts=max_attempts,
            base_delay=base_delay,
            strategy=strategy,
            retry_on=retry_on
        )
        retry_mechanism = RetryMechanism(config)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = retry_mechanism.execute(func, *args, **kwargs)
            
            if not result.success:
                raise result.last_error
            
            return result.last_error if result.last_error else None
        
        return wrapper
    
    return decorator


class CircuitBreaker:
    """Circuit breaker pattern implementation."""
    
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0) -> None:
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening
            timeout: Time to wait before attempting recovery
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.
        
        Args:
            func: Function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            Function result
        """
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self) -> None:
        """Handle successful call."""
        self.failure_count = 0
        if self.state == "half-open":
            self.state = "closed"
    
    def _on_failure(self) -> None:
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset."""
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.timeout
    
    def get_state(self) -> str:
        """Get current circuit breaker state."""
        return self.state
    
    def reset(self) -> None:
        """Reset circuit breaker to closed state."""
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"


class Bulkhead:
    """Bulkhead pattern for limiting concurrent operations."""
    
    def __init__(self, max_concurrent: int = 10) -> None:
        """
        Initialize bulkhead.
        
        Args:
            max_concurrent: Maximum concurrent operations
        """
        self.max_concurrent = max_concurrent
        self.current_concurrent = 0
        self._semaphore = None
    
    def __enter__(self):
        """Enter bulkhead context."""
        if self._semaphore is None:
            import threading
            self._semaphore = threading.Semaphore(self.max_concurrent)
        
        self._semaphore.acquire()
        self.current_concurrent += 1
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit bulkhead context."""
        self.current_concurrent -= 1
        if self._semaphore:
            self._semaphore.release()
    
    def get_available_slots(self) -> int:
        """Get available concurrent slots."""
        return self.max_concurrent - self.current_concurrent


def main() -> None:
    """Demonstrate retry mechanism functionality."""
    
    print("=== Basic Retry ===")
    retry_config = RetryConfig(
        max_attempts=3,
        base_delay=0.5,
        strategy=BackoffStrategy.EXPONENTIAL
    )
    
    retry_mechanism = RetryMechanism(retry_config)
    
    def unreliable_function(attempt: int) -> str:
        """Function that fails first few times."""
        if attempt < 2:
            raise ValueError(f"Attempt {attempt} failed")
        return f"Success on attempt {attempt}"
    
    # Use a closure to track attempts
    attempt_count = [0]
    
    def wrapped_func():
        attempt_count[0] += 1
        return unreliable_function(attempt_count[0])
    
    result = retry_mechanism.execute(wrapped_func)
    print(f"Result: {result}")
    
    print("\n=== Retry Decorator ===")
    
    @retry(max_attempts=4, base_delay=0.3, strategy=BackoffStrategy.LINEAR)
    def fetch_data(url: str) -> str:
        """Simulate data fetching with failures."""
        if "fail" in url:
            raise ConnectionError("Connection failed")
        return f"Data from {url}"
    
    try:
        result = fetch_data("https://api.example.com/data")
        print(f"Success: {result}")
    except Exception as e:
        print(f"Failed: {e}")
    
    try:
        result = fetch_data("https://api.example.com/fail")
        print(f"Success: {result}")
    except Exception as e:
        print(f"Failed: {e}")
    
    print("\n=== Backoff Strategies ===")
    strategies = [
        BackoffStrategy.FIXED,
        BackoffStrategy.LINEAR,
        BackoffStrategy.EXPONENTIAL,
        BackoffStrategy.EXPONENTIAL_WITH_JITTER,
    ]
    
    for strategy in strategies:
        config = RetryConfig(max_attempts=3, base_delay=0.2, strategy=strategy)
        mechanism = RetryMechanism(config)
        
        print(f"\n{strategy.value}:")
        for i in range(1, 4):
            delay = mechanism.calculate_delay(i)
            print(f"  Attempt {i}: {delay:.3f}s delay")
    
    print("\n=== Circuit Breaker ===")
    circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=2.0)
    
    call_count = [0]
    
    def failing_service():
        """Service that fails."""
        call_count[0] += 1
        raise ValueError("Service unavailable")
    
    # Trigger failures
    for i in range(5):
        try:
            circuit_breaker.call(failing_service)
        except Exception as e:
            print(f"Call {i+1}: {e}, Circuit state: {circuit_breaker.get_state()}")
    
    print(f"\nWaiting for circuit breaker timeout...")
    time.sleep(2.5)
    
    print(f"Circuit state after timeout: {circuit_breaker.get_state()}")
    
    circuit_breaker.reset()
    print(f"After reset: {circuit_breaker.get_state()}")
    
    print("\n=== Bulkhead ===")
    bulkhead = Bulkhead(max_concurrent=3)
    
    print(f"Available slots: {bulkhead.get_available_slots()}")
    
    with bulkhead:
        print(f"Inside bulkhead, available: {bulkhead.get_available_slots()}")
    
    print(f"After exit, available: {bulkhead.get_available_slots()}")


if __name__ == "__main__":
    main()
