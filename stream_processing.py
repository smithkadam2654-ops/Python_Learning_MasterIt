"""
Stream Processing Module

This module provides comprehensive stream processing utilities including:
- Stream data structures
- Windowing operations (tumbling, sliding, session)
- Stream aggregation
- Stream filtering and transformation
- Stream joins
- Stream partitioning
- Time-based operations
- Event time processing
- Watermark handling
- Stream state management

All functions include comprehensive docstrings and type hints.
"""

import time
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
from collections import deque, defaultdict
from datetime import datetime, timedelta


class WindowType(Enum):
    """Types of stream windows."""
    TUMBLING = "tumbling"
    SLIDING = "sliding"
    SESSION = "session"


class StreamEventType(Enum):
    """Types of stream events."""
    DATA = "data"
    WATERMARK = "watermark"
    CONTROL = "control"


@dataclass
class StreamEvent:
    """Stream event data structure."""
    data: Any
    timestamp: datetime
    event_type: StreamEventType = StreamEventType.DATA
    key: Optional[str] = None
    metadata: Optional[Dict] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class Stream:
    """Basic stream data structure."""
    
    def __init__(self, name: str = "stream"):
        """Initialize stream."""
        self.name = name
        self.events: deque = deque()
        self.max_size = 10000
    
    def add_event(self, event: StreamEvent) -> None:
        """Add event to stream."""
        self.events.append(event)
        
        # Maintain max size
        if len(self.events) > self.max_size:
            self.events.popleft()
    
    def get_events(self, count: Optional[int] = None) -> List[StreamEvent]:
        """Get events from stream."""
        if count is None:
            return list(self.events)
        return list(self.events)[-count:]
    
    def clear(self) -> None:
        """Clear stream events."""
        self.events.clear()
    
    def size(self) -> int:
        """Get stream size."""
        return len(self.events)


class Window:
    """Window for stream processing."""
    
    def __init__(self, window_type: WindowType, size: timedelta,
                 slide: Optional[timedelta] = None):
        """Initialize window."""
        self.window_type = window_type
        self.size = size
        self.slide = slide if slide else size
        self.events: List[StreamEvent] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def add_event(self, event: StreamEvent) -> bool:
        """Add event to window if within bounds."""
        if self.start_time is None:
            self.start_time = event.timestamp
            self.end_time = self.start_time + self.size
        
        if self.start_time <= event.timestamp <= self.end_time:
            self.events.append(event)
            return True
        return False
    
    def is_expired(self, current_time: datetime) -> bool:
        """Check if window is expired."""
        if self.end_time is None:
            return False
        return current_time > self.end_time
    
    def get_events(self) -> List[StreamEvent]:
        """Get events in window."""
        return self.events.copy()
    
    def clear(self) -> None:
        """Clear window events."""
        self.events.clear()
        self.start_time = None
        self.end_time = None


class StreamFilter:
    """Stream filtering operations."""
    
    @staticmethod
    def filter_by_key(stream: Stream, key: str) -> Stream:
        """Filter stream by key."""
        filtered = Stream(f"{stream.name}_filtered")
        
        for event in stream.get_events():
            if event.key == key:
                filtered.add_event(event)
        
        return filtered
    
    @staticmethod
    def filter_by_predicate(stream: Stream, predicate: Callable[[StreamEvent], bool]) -> Stream:
        """Filter stream by predicate function."""
        filtered = Stream(f"{stream.name}_filtered")
        
        for event in stream.get_events():
            if predicate(event):
                filtered.add_event(event)
        
        return filtered
    
    @staticmethod
    def filter_by_time_range(stream: Stream, start: datetime, end: datetime) -> Stream:
        """Filter stream by time range."""
        filtered = Stream(f"{stream.name}_filtered")
        
        for event in stream.get_events():
            if start <= event.timestamp <= end:
                filtered.add_event(event)
        
        return filtered


class StreamTransform:
    """Stream transformation operations."""
    
    @staticmethod
    def map(stream: Stream, transform_func: Callable[[Any], Any]) -> Stream:
        """Apply map transformation to stream."""
        transformed = Stream(f"{stream.name}_mapped")
        
        for event in stream.get_events():
            new_data = transform_func(event.data)
            new_event = StreamEvent(
                data=new_data,
                timestamp=event.timestamp,
                event_type=event.event_type,
                key=event.key,
                metadata=event.metadata
            )
            transformed.add_event(new_event)
        
        return transformed
    
    @staticmethod
    def flat_map(stream: Stream, flat_map_func: Callable[[Any], List[Any]]) -> Stream:
        """Apply flat map transformation to stream."""
        transformed = Stream(f"{stream.name}_flat_mapped")
        
        for event in stream.get_events():
            flat_data = flat_map_func(event.data)
            
            for item in flat_data:
                new_event = StreamEvent(
                    data=item,
                    timestamp=event.timestamp,
                    event_type=event.event_type,
                    key=event.key,
                    metadata=event.metadata
                )
                transformed.add_event(new_event)
        
        return transformed
    
    @staticmethod
    def extract_key(stream: Stream, key_func: Callable[[Any], str]) -> Stream:
        """Extract key from event data."""
        keyed = Stream(f"{stream.name}_keyed")
        
        for event in stream.get_events():
            key = key_func(event.data)
            new_event = StreamEvent(
                data=event.data,
                timestamp=event.timestamp,
                event_type=event.event_type,
                key=key,
                metadata=event.metadata
            )
            keyed.add_event(new_event)
        
        return keyed


class StreamAggregator:
    """Stream aggregation operations."""
    
    @staticmethod
    def count(stream: Stream) -> int:
        """Count events in stream."""
        return len(stream.get_events())
    
    @staticmethod
    def sum(stream: Stream, value_func: Callable[[Any], float]) -> float:
        """Sum values in stream."""
        total = 0.0
        
        for event in stream.get_events():
            total += value_func(event.data)
        
        return total
    
    @staticmethod
    def average(stream: Stream, value_func: Callable[[Any], float]) -> float:
        """Calculate average of values in stream."""
        events = stream.get_events()
        
        if not events:
            return 0.0
        
        total = StreamAggregator.sum(stream, value_func)
        return total / len(events)
    
    @staticmethod
    def min(stream: Stream, value_func: Callable[[Any], float]) -> float:
        """Find minimum value in stream."""
        values = [value_func(event.data) for event in stream.get_events()]
        return min(values) if values else 0.0
    
    @staticmethod
    def max(stream: Stream, value_func: Callable[[Any], float]) -> float:
        """Find maximum value in stream."""
        values = [value_func(event.data) for event in stream.get_events()]
        return max(values) if values else 0.0
    
    @staticmethod
    def group_by(stream: Stream, key_func: Callable[[Any], str]) -> Dict[str, Stream]:
        """Group stream events by key."""
        groups = defaultdict(list)
        
        for event in stream.get_events():
            key = key_func(event.data)
            groups[key].append(event)
        
        grouped_streams = {}
        for key, events in groups.items():
            grouped_stream = Stream(f"{stream.name}_{key}")
            for event in events:
                grouped_stream.add_event(event)
            grouped_streams[key] = grouped_stream
        
        return grouped_streams


class StreamJoin:
    """Stream join operations."""
    
    @staticmethod
    def inner_join(stream1: Stream, stream2: Stream,
                  key_func1: Callable[[Any], str],
                  key_func2: Callable[[Any], str]) -> Stream:
        """Inner join two streams."""
        joined = Stream(f"{stream1.name}_join_{stream2.name}")
        
        # Build index for stream2
        index = defaultdict(list)
        for event in stream2.get_events():
            key = key_func2(event.data)
            index[key].append(event)
        
        # Join
        for event1 in stream1.get_events():
            key = key_func1(event1.data)
            
            if key in index:
                for event2 in index[key]:
                    joined_event = StreamEvent(
                        data=(event1.data, event2.data),
                        timestamp=max(event1.timestamp, event2.timestamp),
                        event_type=StreamEventType.DATA,
                        key=key
                    )
                    joined.add_event(joined_event)
        
        return joined
    
    @staticmethod
    def left_join(stream1: Stream, stream2: Stream,
                 key_func1: Callable[[Any], str],
                 key_func2: Callable[[Any], str]) -> Stream:
        """Left join two streams."""
        joined = Stream(f"{stream1.name}_left_join_{stream2.name}")
        
        # Build index for stream2
        index = defaultdict(list)
        for event in stream2.get_events():
            key = key_func2(event.data)
            index[key].append(event)
        
        # Join
        for event1 in stream1.get_events():
            key = key_func1(event1.data)
            
            if key in index:
                for event2 in index[key]:
                    joined_event = StreamEvent(
                        data=(event1.data, event2.data),
                        timestamp=max(event1.timestamp, event2.timestamp),
                        event_type=StreamEventType.DATA,
                        key=key
                    )
                    joined.add_event(joined_event)
            else:
                joined_event = StreamEvent(
                    data=(event1.data, None),
                    timestamp=event1.timestamp,
                    event_type=StreamEventType.DATA,
                    key=key
                )
                joined.add_event(joined_event)
        
        return joined


class StreamPartitioner:
    """Stream partitioning operations."""
    
    @staticmethod
    def partition_by_key(stream: Stream, num_partitions: int,
                       key_func: Callable[[Any], str]) -> List[Stream]:
        """Partition stream by key hash."""
        partitions = [Stream(f"{stream.name}_partition_{i}") for i in range(num_partitions)]
        
        for event in stream.get_events():
            key = key_func(event.data)
            partition_idx = hash(key) % num_partitions
            partitions[partition_idx].add_event(event)
        
        return partitions
    
    @staticmethod
    def partition_by_round_robin(stream: Stream, num_partitions: int) -> List[Stream]:
        """Partition stream by round-robin."""
        partitions = [Stream(f"{stream.name}_partition_{i}") for i in range(num_partitions)]
        
        for i, event in enumerate(stream.get_events()):
            partition_idx = i % num_partitions
            partitions[partition_idx].add_event(event)
        
        return partitions
    
    @staticmethod
    def partition_by_range(stream: Stream, num_partitions: int,
                          value_func: Callable[[Any], float]) -> List[Stream]:
        """Partition stream by value range."""
        partitions = [Stream(f"{stream.name}_partition_{i}") for i in range(num_partitions)]
        
        # Find min and max
        values = [value_func(event.data) for event in stream.get_events()]
        min_val = min(values) if values else 0
        max_val = max(values) if values else 0
        
        range_size = (max_val - min_val) / num_partitions if max_val > min_val else 1
        
        for event in stream.get_events():
            value = value_func(event.data)
            partition_idx = int((value - min_val) / range_size)
            partition_idx = min(partition_idx, num_partitions - 1)
            partitions[partition_idx].add_event(event)
        
        return partitions


class WindowedStream:
    """Windowed stream processing."""
    
    def __init__(self, stream: Stream, window: Window):
        """Initialize windowed stream."""
        self.stream = stream
        self.window = window
        self.current_windows: List[Window] = []
    
    def process(self, current_time: datetime) -> List[List[StreamEvent]]:
        """Process stream with windowing."""
        results = []
        
        # Check for expired windows
        active_windows = []
        
        for window in self.current_windows:
            if window.is_expired(current_time):
                results.append(window.get_events())
            else:
                active_windows.append(window)
        
        self.current_windows = active_windows
        
        # Process new events
        for event in self.stream.get_events():
            added = False
            
            for window in self.current_windows:
                if window.add_event(event):
                    added = True
            
            # Create new window if needed
            if not added:
                new_window = Window(self.window.window_type, self.window.size, self.window.slide)
                new_window.add_event(event)
                self.current_windows.append(new_window)
        
        return results


class TimeBasedOperations:
    """Time-based stream operations."""
    
    @staticmethod
    def delay(stream: Stream, delay_ms: int) -> Stream:
        """Delay stream by specified milliseconds."""
        delayed = Stream(f"{stream.name}_delayed")
        delay = timedelta(milliseconds=delay_ms)
        
        for event in stream.get_events():
            delayed_event = StreamEvent(
                data=event.data,
                timestamp=event.timestamp + delay,
                event_type=event.event_type,
                key=event.key,
                metadata=event.metadata
            )
            delayed.add_event(delayed_event)
        
        return delayed
    
    @staticmethod
    def throttle(stream: Stream, interval_ms: int) -> Stream:
        """Throttle stream to emit at most one event per interval."""
        throttled = Stream(f"{stream.name}_throttled")
        interval = timedelta(milliseconds=interval_ms)
        last_emit = None
        
        for event in stream.get_events():
            if last_emit is None or event.timestamp - last_emit >= interval:
                throttled.add_event(event)
                last_emit = event.timestamp
        
        return throttled
    
    @staticmethod
    def debounce(stream: Stream, delay_ms: int) -> Stream:
        """Debounce stream to emit only after quiet period."""
        debounced = Stream(f"{stream.name}_debounced")
        delay = timedelta(milliseconds=delay_ms)
        buffer = []
        
        for event in stream.get_events():
            buffer.append(event)
            
            # Check if quiet period elapsed
            if event.timestamp - buffer[0].timestamp >= delay:
                debounced.add_event(buffer[-1])
                buffer.clear()
        
        # Emit last event if buffer not empty
        if buffer:
            debounced.add_event(buffer[-1])
        
        return debounced


class WatermarkHandler:
    """Watermark handling for event time processing."""
    
    def __init__(self, allowed_lateness: timedelta = timedelta(seconds=5)):
        """Initialize watermark handler."""
        self.allowed_lateness = allowed_lateness
        self.current_watermark: Optional[datetime] = None
        self.late_events: List[StreamEvent] = []
    
    def update_watermark(self, event: StreamEvent) -> bool:
        """Update watermark based on event."""
        if self.current_watermark is None or event.timestamp > self.current_watermark:
            self.current_watermark = event.timestamp
            return True
        return False
    
    def is_late(self, event: StreamEvent) -> bool:
        """Check if event is late."""
        if self.current_watermark is None:
            return False
        return event.timestamp < self.current_watermark - self.allowed_lateness
    
    def get_late_events(self) -> List[StreamEvent]:
        """Get late events."""
        return self.late_events.copy()
    
    def clear_late_events(self) -> None:
        """Clear late events."""
        self.late_events.clear()


class StreamState:
    """Stream state management."""
    
    def __init__(self):
        """Initialize stream state."""
        self.keyed_state: Dict[str, Dict] = defaultdict(dict)
        self.operator_state: Dict = {}
    
    def update_keyed_state(self, key: str, state_key: str, value: Any) -> None:
        """Update state for key."""
        self.keyed_state[key][state_key] = value
    
    def get_keyed_state(self, key: str, state_key: str) -> Optional[Any]:
        """Get state for key."""
        return self.keyed_state[key].get(state_key)
    
    def update_operator_state(self, state_key: str, value: Any) -> None:
        """Update operator state."""
        self.operator_state[state_key] = value
    
    def get_operator_state(self, state_key: str) -> Optional[Any]:
        """Get operator state."""
        return self.operator_state.get(state_key)
    
    def clear_keyed_state(self, key: str) -> None:
        """Clear state for key."""
        if key in self.keyed_state:
            del self.keyed_state[key]
    
    def clear_all_state(self) -> None:
        """Clear all state."""
        self.keyed_state.clear()
        self.operator_state.clear()


class StreamProcessor:
    """High-level stream processor."""
    
    def __init__(self, stream: Stream):
        """Initialize stream processor."""
        self.stream = stream
        self.state = StreamState()
        self.watermark_handler = WatermarkHandler()
    
    def process(self, operations: List[Callable]) -> Stream:
        """Process stream through operations."""
        result = self.stream
        
        for operation in operations:
            result = operation(result)
        
        return result
    
    def add_event(self, data: Any, key: Optional[str] = None) -> None:
        """Add event to stream."""
        event = StreamEvent(
            data=data,
            timestamp=datetime.now(),
            event_type=StreamEventType.DATA,
            key=key
        )
        self.stream.add_event(event)


def demonstrate_stream_processing():
    """Demonstrate stream processing functionality."""
    print("=== Stream Processing Demonstration ===\n")
    
    # Basic Stream
    print("1. Basic Stream:")
    stream = Stream("test_stream")
    
    for i in range(5):
        event = StreamEvent(
            data=f"value_{i}",
            timestamp=datetime.now(),
            key=f"key_{i % 2}"
        )
        stream.add_event(event)
    
    print(f"   Stream size: {stream.size()}")
    print(f"   Events: {[e.data for e in stream.get_events()]}")
    
    # Filtering
    print("\n2. Stream Filtering:")
    filtered = StreamFilter.filter_by_key(stream, "key_0")
    print(f"   Filtered by key_0: {[e.data for e in filtered.get_events()]}")
    
    predicate = lambda e: int(e.data.split("_")[1]) > 2
    filtered_pred = StreamFilter.filter_by_predicate(stream, predicate)
    print(f"   Filtered by predicate: {[e.data for e in filtered_pred.get_events()]}")
    
    # Transformation
    print("\n3. Stream Transformation:")
    mapped = StreamTransform.map(stream, lambda x: x.upper())
    print(f"   Mapped to upper: {[e.data for e in mapped.get_events()]}")
    
    # Aggregation
    print("\n4. Stream Aggregation:")
    count = StreamAggregator.count(stream)
    print(f"   Count: {count}")
    
    value_func = lambda x: int(x.split("_")[1])
    total = StreamAggregator.sum(stream, value_func)
    print(f"   Sum: {total}")
    
    avg = StreamAggregator.average(stream, value_func)
    print(f"   Average: {avg:.2f}")
    
    max_val = StreamAggregator.max(stream, value_func)
    print(f"   Max: {max_val}")
    
    # Grouping
    print("\n5. Stream Grouping:")
    grouped = StreamAggregator.group_by(stream, lambda x: x.split("_")[0])
    print(f"   Groups: {list(grouped.keys())}")
    
    # Join
    print("\n6. Stream Join:")
    stream2 = Stream("stream2")
    for i in range(3):
        event = StreamEvent(
            data=f"item_{i}",
            timestamp=datetime.now(),
            key=f"key_{i % 2}"
        )
        stream2.add_event(event)
    
    joined = StreamJoin.inner_join(stream, stream2, lambda x: x.split("_")[1], lambda x: x.split("_")[1])
    print(f"   Joined events: {len(joined.get_events())}")
    
    # Partitioning
    print("\n7. Stream Partitioning:")
    partitions = StreamPartitioner.partition_by_key(stream, 2, lambda x: x.split("_")[1])
    print(f"   Partition sizes: {[p.size() for p in partitions]}")
    
    # Windowing
    print("\n8. Windowed Stream:")
    window = Window(WindowType.TUMBLING, timedelta(seconds=1))
    windowed = WindowedStream(stream, window)
    
    results = windowed.process(datetime.now())
    print(f"   Window results: {len(results)}")
    
    # Time-based operations
    print("\n9. Time-based Operations:")
    delayed = TimeBasedOperations.delay(stream, 100)
    print(f"   Delayed stream size: {delayed.size()}")
    
    throttled = TimeBasedOperations.throttle(stream, 50)
    print(f"   Throttled stream size: {throttled.size()}")
    
    # Watermark
    print("\n10. Watermark Handling:")
    watermark = WatermarkHandler(allowed_lateness=timedelta(seconds=1))
    
    for event in stream.get_events():
        watermark.update_watermark(event)
    
    print(f"   Current watermark: {watermark.current_watermark}")
    
    # State Management
    print("\n11. Stream State:")
    state = StreamState()
    state.update_keyed_state("key_0", "count", 5)
    state.update_keyed_state("key_1", "count", 3)
    
    print(f"   Key_0 count: {state.get_keyed_state('key_0', 'count')}")
    print(f"   Key_1 count: {state.get_keyed_state('key_1', 'count')}")
    
    print("\n=== Demonstration Complete ===")
    print("\nStream Processing Best Practices:")
    print("- Choose appropriate window types for your use case")
    print("- Use watermark handling for event time processing")
    print("- Manage state carefully for keyed operations")
    print("- Consider backpressure for high-throughput streams")
    print("- Use partitioning for parallel processing")
    print("- Monitor stream latency and throughput")
    print("- Handle late events appropriately")
    print("- Use idempotent operations for at-least-once semantics")
    print("- Consider fault tolerance and recovery")
    print("- Use checkpointing for stateful operations")
    print("- Design for exactly-once processing when possible")


if __name__ == "__main__":
    demonstrate_stream_processing()
