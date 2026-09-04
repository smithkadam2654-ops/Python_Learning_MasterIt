"""
File Watcher - File system monitoring with event handling.
Features: Directory monitoring, event callbacks, and pattern filtering.
"""

import os
import time
import threading
from typing import Callable, Optional, List, Set
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class FileEventType(Enum):
    """File system event types."""
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    MOVED = "moved"


@dataclass
class FileEvent:
    """File system event."""
    event_type: FileEventType
    path: str
    timestamp: float = None
    old_path: Optional[str] = None  # For move events
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class FileEventHandler:
    """Base class for file event handlers."""
    
    def on_created(self, event: FileEvent) -> None:
        """Handle file creation event."""
        pass
    
    def on_modified(self, event: FileEvent) -> None:
        """Handle file modification event."""
        pass
    
    def on_deleted(self, event: FileEvent) -> None:
        """Handle file deletion event."""
        pass
    
    def on_moved(self, event: FileEvent) -> None:
        """Handle file move event."""
        pass
    
    def handle(self, event: FileEvent) -> None:
        """Route event to appropriate handler."""
        if event.event_type == FileEventType.CREATED:
            self.on_created(event)
        elif event.event_type == FileEventType.MODIFIED:
            self.on_modified(event)
        elif event.event_type == FileEventType.DELETED:
            self.on_deleted(event)
        elif event.event_type == FileEventType.MOVED:
            self.on_moved(event)


class FileWatcher:
    """File system watcher."""
    
    def __init__(self, watch_path: str, recursive: bool = True) -> None:
        """
        Initialize file watcher.
        
        Args:
            watch_path: Path to watch
            recursive: Whether to watch subdirectories
        """
        self.watch_path = Path(watch_path)
        self.recursive = recursive
        self.handlers: List[FileEventHandler] = []
        self.patterns: List[str] = []  # File patterns to include
        self.exclude_patterns: List[str] = []  # Patterns to exclude
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._previous_state: Dict[str, float] = {}
    
    def add_handler(self, handler: FileEventHandler) -> None:
        """
        Add event handler.
        
        Args:
            handler: Handler to add
        """
        self.handlers.append(handler)
    
    def remove_handler(self, handler: FileEventHandler) -> None:
        """
        Remove event handler.
        
        Args:
            handler: Handler to remove
        """
        if handler in self.handlers:
            self.handlers.remove(handler)
    
    def add_pattern(self, pattern: str) -> None:
        """
        Add file pattern to watch (e.g., "*.txt").
        
        Args:
            pattern: File pattern
        """
        self.patterns.append(pattern)
    
    def add_exclude_pattern(self, pattern: str) -> None:
        """
        Add pattern to exclude.
        
        Args:
            pattern: Pattern to exclude
        """
        self.exclude_patterns.append(pattern)
    
    def _should_watch(self, path: Path) -> bool:
        """
        Check if path should be watched based on patterns.
        
        Args:
            path: Path to check
            
        Returns:
            True if path should be watched
        """
        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if path.match(pattern):
                return False
        
        # If no include patterns, watch everything
        if not self.patterns:
            return True
        
        # Check include patterns
        for pattern in self.patterns:
            if path.match(pattern):
                return True
        
        return False
    
    def _scan_directory(self) -> Dict[str, float]:
        """
        Scan directory and return file modification times.
        
        Returns:
            Dictionary mapping file paths to modification times
        """
        state = {}
        
        if self.recursive:
            for path in self.watch_path.rglob("*"):
                if path.is_file() and self._should_watch(path):
                    state[str(path)] = path.stat().st_mtime
        else:
            for path in self.watch_path.glob("*"):
                if path.is_file() and self._should_watch(path):
                    state[str(path)] = path.stat().st_mtime
        
        return state
    
    def _detect_changes(self, old_state: Dict[str, float], 
                       new_state: Dict[str, float]) -> List[FileEvent]:
        """
        Detect changes between two directory states.
        
        Args:
            old_state: Previous directory state
            new_state: Current directory state
            
        Returns:
            List of detected events
        """
        events = []
        old_files = set(old_state.keys())
        new_files = set(new_state.keys())
        
        # Detect new files
        for path in new_files - old_files:
            events.append(FileEvent(FileEventType.CREATED, path))
        
        # Detect deleted files
        for path in old_files - new_files:
            events.append(FileEvent(FileEventType.DELETED, path))
        
        # Detect modified files
        for path in old_files & new_files:
            if new_state[path] != old_state[path]:
                events.append(FileEvent(FileEventType.MODIFIED, path))
        
        return events
    
    def _watch_loop(self) -> None:
        """Main watch loop."""
        self._previous_state = self._scan_directory()
        
        while self._running:
            time.sleep(1.0)  # Polling interval
            
            if not self._running:
                break
            
            new_state = self._scan_directory()
            events = self._detect_changes(self._previous_state, new_state)
            
            for event in events:
                for handler in self.handlers:
                    try:
                        handler.handle(event)
                    except Exception as e:
                        print(f"Error in handler: {e}")
            
            self._previous_state = new_state
    
    def start(self) -> None:
        """Start watching."""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._watch_loop, daemon=True)
            self._thread.start()
    
    def stop(self) -> None:
        """Stop watching."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
    
    def is_running(self) -> bool:
        """Check if watcher is running."""
        return self._running


class LoggingHandler(FileEventHandler):
    """Handler that logs file events."""
    
    def __init__(self) -> None:
        """Initialize logging handler."""
        self.events: List[FileEvent] = []
    
    def on_created(self, event: FileEvent) -> None:
        """Log file creation."""
        print(f"[CREATED] {event.path}")
        self.events.append(event)
    
    def on_modified(self, event: FileEvent) -> None:
        """Log file modification."""
        print(f"[MODIFIED] {event.path}")
        self.events.append(event)
    
    def on_deleted(self, event: FileEvent) -> None:
        """Log file deletion."""
        print(f"[DELETED] {event.path}")
        self.events.append(event)
    
    def on_moved(self, event: FileEvent) -> None:
        """Log file move."""
        print(f"[MOVED] {event.old_path} -> {event.path}")
        self.events.append(event)


class StatisticsHandler(FileEventHandler):
    """Handler that tracks statistics."""
    
    def __init__(self) -> None:
        """Initialize statistics handler."""
        self.created_count = 0
        self.modified_count = 0
        self.deleted_count = 0
        self.moved_count = 0
    
    def on_created(self, event: FileEvent) -> None:
        """Increment created count."""
        self.created_count += 1
    
    def on_modified(self, event: FileEvent) -> None:
        """Increment modified count."""
        self.modified_count += 1
    
    def on_deleted(self, event: FileEvent) -> None:
        """Increment deleted count."""
        self.deleted_count += 1
    
    def on_moved(self, event: FileEvent) -> None:
        """Increment moved count."""
        self.moved_count += 1
    
    def get_stats(self) -> Dict[str, int]:
        """Get statistics."""
        return {
            "created": self.created_count,
            "modified": self.modified_count,
            "deleted": self.deleted_count,
            "moved": self.moved_count
        }


class CallbackHandler(FileEventHandler):
    """Handler that calls custom callbacks."""
    
    def __init__(self, on_created: Optional[Callable] = None,
                 on_modified: Optional[Callable] = None,
                 on_deleted: Optional[Callable] = None) -> None:
        """
        Initialize callback handler.
        
        Args:
            on_created: Callback for creation events
            on_modified: Callback for modification events
            on_deleted: Callback for deletion events
        """
        self.on_created_callback = on_created
        self.on_modified_callback = on_modified
        self.on_deleted_callback = on_deleted
    
    def on_created(self, event: FileEvent) -> None:
        """Call creation callback."""
        if self.on_created_callback:
            self.on_created_callback(event)
    
    def on_modified(self, event: FileEvent) -> None:
        """Call modification callback."""
        if self.on_modified_callback:
            self.on_modified_callback(event)
    
    def on_deleted(self, event: FileEvent) -> None:
        """Call deletion callback."""
        if self.on_deleted_callback:
            self.on_deleted_callback(event)


def main() -> None:
    """Demonstrate file watcher functionality."""
    
    print("=== File Watcher Demo ===")
    
    # Create a temporary directory for testing
    import tempfile
    temp_dir = tempfile.mkdtemp()
    print(f"Watching directory: {temp_dir}")
    
    # Create watcher
    watcher = FileWatcher(temp_dir, recursive=True)
    
    # Add handlers
    logging_handler = LoggingHandler()
    stats_handler = StatisticsHandler()
    
    watcher.add_handler(logging_handler)
    watcher.add_handler(stats_handler)
    
    # Only watch .txt files
    watcher.add_pattern("*.txt")
    
    # Start watching
    watcher.start()
    print("Watcher started")
    
    # Create some test files
    import time
    time.sleep(0.5)
    
    test_file1 = Path(temp_dir) / "test1.txt"
    test_file2 = Path(temp_dir) / "test2.txt"
    test_file3 = Path(temp_dir) / "test3.log"  # Should be ignored
    
    test_file1.write_text("Hello")
    test_file2.write_text("World")
    test_file3.write_text("Ignored")
    
    print("\nCreated files")
    time.sleep(1.5)
    
    # Modify a file
    test_file1.write_text("Hello, World!")
    print("\nModified test1.txt")
    time.sleep(1.5)
    
    # Delete a file
    test_file2.unlink()
    print("\nDeleted test2.txt")
    time.sleep(1.5)
    
    # Stop watcher
    watcher.stop()
    print("\nWatcher stopped")
    
    # Show statistics
    print(f"\nStatistics: {stats_handler.get_stats()}")
    print(f"Total events logged: {len(logging_handler.events)}")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
    print(f"\nCleaned up temporary directory")
    
    print("\n=== Callback Handler Demo ===")
    
    def on_file_created(event: FileEvent):
        print(f"📝 New file detected: {Path(event.path).name}")
    
    def on_file_modified(event: FileEvent):
        print(f"✏️ File changed: {Path(event.path).name}")
    
    callback_handler = CallbackHandler(on_created, on_file_modified)
    
    print("Callback handler configured")


if __name__ == "__main__":
    main()
