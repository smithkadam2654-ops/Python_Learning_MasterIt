"""
Rate Limiter - Rate limiting algorithms for API throttling.
Features: Token bucket, sliding window, and leaky bucket implementations.
"""

import time
from typing import Optional, Dict
from dataclasses import dataclass
from collections import deque
import threading


@dataclass
class RateLimitResult:
    """Result of rate limit check."""
    allowed: bool
    remaining: int
    reset_time: float
    retry_after: Optional[float] = None


class TokenBucket:
    """Token bucket rate limiter."""
    
    def __init__(self, capacity: int, refill_rate: float) -> None:
        """
        Initialize token bucket.
        
        Args:
            capacity: Maximum number of tokens
            refill_rate: Tokens per second to add
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self._lock = threading.Lock()
    
    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> RateLimitResult:
        """
        Try to consume tokens.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            RateLimitResult indicating if request is allowed
        """
        with self._lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return RateLimitResult(
                    allowed=True,
                    remaining=int(self.tokens),
                    reset_time=self.last_refill + (self.capacity - self.tokens) / self.refill_rate
                )
            else:
                retry_after = (tokens - self.tokens) / self.refill_rate
                return RateLimitResult(
                    allowed=False,
                    remaining=int(self.tokens),
                    reset_time=self.last_refill + (self.capacity - self.tokens) / self.refill_rate,
                    retry_after=retry_after
                )
    
    def get_available_tokens(self) -> int:
        """Get current number of available tokens."""
        with self._lock:
            self._refill()
            return int(self.tokens)


class SlidingWindowLog:
    """Sliding window log rate limiter."""
    
    def __init__(self, window_size: float, max_requests: int) -> None:
        """
        Initialize sliding window log.
        
        Args:
            window_size: Window size in seconds
            max_requests: Maximum requests per window
        """
        self.window_size = window_size
        self.max_requests = max_requests
        self.requests = deque()
        self._lock = threading.Lock()
    
    def allow(self) -> RateLimitResult:
        """
        Check if request is allowed.
        
        Returns:
            RateLimitResult indicating if request is allowed
        """
        with self._lock:
            now = time.time()
            
            # Remove requests outside the window
            while self.requests and self.requests[0] <= now - self.window_size:
                self.requests.popleft()
            
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return RateLimitResult(
                    allowed=True,
                    remaining=self.max_requests - len(self.requests),
                    reset_time=now + self.window_size
                )
            else:
                # Time until oldest request expires
                retry_after = self.requests[0] + self.window_size - now
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=self.requests[0] + self.window_size,
                    retry_after=retry_after
                )
    
    def get_request_count(self) -> int:
        """Get current request count in window."""
        with self._lock:
            now = time.time()
            while self.requests and self.requests[0] <= now - self.window_size:
                self.requests.popleft()
            return len(self.requests)


class SlidingWindowCounter:
    """Sliding window counter rate limiter (optimized)."""
    
    def __init__(self, window_size: float, max_requests: int) -> None:
        """
        Initialize sliding window counter.
        
        Args:
            window_size: Window size in seconds
            max_requests: Maximum requests per window
        """
        self.window_size = window_size
        self.max_requests = max_requests
        self.windows: Dict[int, int] = {}
        self._lock = threading.Lock()
    
    def _get_window_index(self, timestamp: float) -> int:
        """Get window index for a timestamp."""
        return int(timestamp / self.window_size)
    
    def allow(self) -> RateLimitResult:
        """
        Check if request is allowed.
        
        Returns:
            RateLimitResult indicating if request is allowed
        """
        with self._lock:
            now = time.time()
            current_window = self._get_window_index(now)
            
            # Clean up old windows
            old_windows = [w for w in self.windows if w < current_window - 1]
            for w in old_windows:
                del self.windows[w]
            
            # Calculate request count
            prev_window_count = self.windows.get(current_window - 1, 0)
            current_window_count = self.windows.get(current_window, 0)
            
            # Weight of previous window (how much of it is still in the sliding window)
            elapsed_in_current = now % self.window_size
            weight = 1 - (elapsed_in_current / self.window_size)
            
            weighted_count = prev_window_count * weight + current_window_count
            
            if weighted_count < self.max_requests:
                self.windows[current_window] = current_window_count + 1
                return RateLimitResult(
                    allowed=True,
                    remaining=int(self.max_requests - weighted_count),
                    reset_time=now + self.window_size
                )
            else:
                retry_after = self.window_size - elapsed_in_current
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=now + retry_after,
                    retry_after=retry_after
                )


class LeakyBucket:
    """Leaky bucket rate limiter."""
    
    def __init__(self, capacity: int, leak_rate: float) -> None:
        """
        Initialize leaky bucket.
        
        Args:
            capacity: Maximum bucket capacity
            leak_rate: Requests per second to leak
        """
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.volume = 0.0
        self.last_leak = time.time()
        self._lock = threading.Lock()
    
    def _leak(self) -> None:
        """Leak requests from bucket based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_leak
        leaked = elapsed * self.leak_rate
        
        self.volume = max(0, self.volume - leaked)
        self.last_leak = now
    
    def allow(self) -> RateLimitResult:
        """
        Check if request is allowed.
        
        Returns:
            RateLimitResult indicating if request is allowed
        """
        with self._lock:
            self._leak()
            
            if self.volume < self.capacity:
                self.volume += 1
                return RateLimitResult(
                    allowed=True,
                    remaining=int(self.capacity - self.volume),
                    reset_time=self.last_leak + self.volume / self.leak_rate
                )
            else:
                retry_after = (self.volume - self.capacity + 1) / self.leak_rate
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=self.last_leak + self.volume / self.leak_rate,
                    retry_after=retry_after
                )
    
    def get_volume(self) -> float:
        """Get current bucket volume."""
        with self._lock:
            self._leak()
            return self.volume


class FixedWindowCounter:
    """Fixed window counter rate limiter."""
    
    def __init__(self, window_size: float, max_requests: int) -> None:
        """
        Initialize fixed window counter.
        
        Args:
            window_size: Window size in seconds
            max_requests: Maximum requests per window
        """
        self.window_size = window_size
        self.max_requests = max_requests
        self.count = 0
        self.window_start = time.time()
        self._lock = threading.Lock()
    
    def allow(self) -> RateLimitResult:
        """
        Check if request is allowed.
        
        Returns:
            RateLimitResult indicating if request is allowed
        """
        with self._lock:
            now = time.time()
            
            # Reset window if expired
            if now - self.window_start >= self.window_size:
                self.count = 0
                self.window_start = now
            
            if self.count < self.max_requests:
                self.count += 1
                return RateLimitResult(
                    allowed=True,
                    remaining=self.max_requests - self.count,
                    reset_time=self.window_start + self.window_size
                )
            else:
                retry_after = self.window_start + self.window_size - now
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=self.window_start + self.window_size,
                    retry_after=retry_after
                )


class RateLimiterFactory:
    """Factory for creating rate limiters."""
    
    @staticmethod
    def create_token_bucket(capacity: int, refill_rate: float) -> TokenBucket:
        """Create token bucket rate limiter."""
        return TokenBucket(capacity, refill_rate)
    
    @staticmethod
    def create_sliding_window_log(window_size: float, max_requests: int) -> SlidingWindowLog:
        """Create sliding window log rate limiter."""
        return SlidingWindowLog(window_size, max_requests)
    
    @staticmethod
    def create_sliding_window_counter(window_size: float, max_requests: int) -> SlidingWindowCounter:
        """Create sliding window counter rate limiter."""
        return SlidingWindowCounter(window_size, max_requests)
    
    @staticmethod
    def create_leaky_bucket(capacity: int, leak_rate: float) -> LeakyBucket:
        """Create leaky bucket rate limiter."""
        return LeakyBucket(capacity, leak_rate)
    
    @staticmethod
    def create_fixed_window(window_size: float, max_requests: int) -> FixedWindowCounter:
        """Create fixed window counter rate limiter."""
        return FixedWindowCounter(window_size, max_requests)


def simulate_requests(limiter, num_requests: int, delay: float = 0.1) -> None:
    """
    Simulate requests against a rate limiter.
    
    Args:
        limiter: Rate limiter instance
        num_requests: Number of requests to simulate
        delay: Delay between requests
    """
    for i in range(num_requests):
        result = limiter.allow()
        status = "ALLOWED" if result.allowed else "BLOCKED"
        print(f"Request {i+1}: {status} (Remaining: {result.remaining})")
        
        if result.retry_after:
            print(f"  Retry after: {result.retry_after:.2f}s")
        
        time.sleep(delay)


def main() -> None:
    """Demonstrate rate limiting algorithms."""
    
    print("=== Token Bucket ===")
    token_bucket = TokenBucket(capacity=5, refill_rate=1.0)
    
    for i in range(7):
        result = token_bucket.consume()
        status = "ALLOWED" if result.allowed else "BLOCKED"
        print(f"Request {i+1}: {status} (Tokens: {token_bucket.get_available_tokens()})")
        
        if result.retry_after:
            print(f"  Retry after: {result.retry_after:.2f}s")
    
    time.sleep(2)
    print(f"After 2s, tokens: {token_bucket.get_available_tokens()}")
    
    print("\n=== Sliding Window Log ===")
    sliding_window = SlidingWindowLog(window_size=1.0, max_requests=3)
    
    for i in range(5):
        result = sliding_window.allow()
        status = "ALLOWED" if result.allowed else "BLOCKED"
        print(f"Request {i+1}: {status} (Count: {sliding_window.get_request_count()})")
        time.sleep(0.3)
    
    print("\n=== Sliding Window Counter ===")
    sliding_counter = SlidingWindowCounter(window_size=1.0, max_requests=3)
    
    for i in range(5):
        result = sliding_counter.allow()
        status = "ALLOWED" if result.allowed else "BLOCKED"
        print(f"Request {i+1}: {status}")
        time.sleep(0.3)
    
    print("\n=== Leaky Bucket ===")
    leaky_bucket = LeakyBucket(capacity=5, leak_rate=2.0)
    
    for i in range(7):
        result = leaky_bucket.allow()
        status = "ALLOWED" if result.allowed else "BLOCKED"
        print(f"Request {i+1}: {status} (Volume: {leaky_bucket.get_volume():.1f})")
        time.sleep(0.2)
    
    print("\n=== Fixed Window Counter ===")
    fixed_window = FixedWindowCounter(window_size=1.0, max_requests=3)
    
    for i in range(5):
        result = fixed_window.allow()
        status = "ALLOWED" if result.allowed else "BLOCKED"
        print(f"Request {i+1}: {status}")
        time.sleep(0.3)
    
    print("\n=== Comparison: Burst Traffic ===")
    print("Token Bucket (capacity=10, rate=2/s):")
    tb = TokenBucket(capacity=10, refill_rate=2.0)
    simulate_requests(tb, num_requests=15, delay=0.05)
    
    print("\nFixed Window (window=1s, max=3):")
    fw = FixedWindowCounter(window_size=1.0, max_requests=3)
    simulate_requests(fw, num_requests=8, delay=0.1)


if __name__ == "__main__":
    main()
