"""
Logging System - Custom logging implementation with multiple handlers.
Features: Multiple log levels, file handlers, and formatted output.
"""

import sys
from typing import Optional, List, Callable
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class LogLevel(Enum):
    """Log severity levels."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


@dataclass
class LogRecord:
    """Log record containing log information."""
    timestamp: datetime
    level: LogLevel
    message: str
    logger_name: str
    extra: dict = None
    
    def __post_init__(self):
        if self.extra is None:
            self.extra = {}


class LogFormatter:
    """Base class for log formatters."""
    
    def format(self, record: LogRecord) -> str:
        """Format a log record."""
        raise NotImplementedError


class SimpleFormatter(LogFormatter):
    """Simple log formatter."""
    
    def format(self, record: LogRecord) -> str:
        """Format log record as simple string."""
        level_name = record.level.name
        return f"[{level_name}] {record.message}"


class DetailedFormatter(LogFormatter):
    """Detailed log formatter with timestamp and logger name."""
    
    def __init__(self, include_timestamp: bool = True, include_logger: bool = True) -> None:
        """
        Initialize detailed formatter.
        
        Args:
            include_timestamp: Whether to include timestamp
            include_logger: Whether to include logger name
        """
        self.include_timestamp = include_timestamp
        self.include_logger = include_logger
    
    def format(self, record: LogRecord) -> str:
        """Format log record with details."""
        parts = []
        
        if self.include_timestamp:
            timestamp = record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            parts.append(f"[{timestamp}]")
        
        level_name = record.level.name
        parts.append(f"[{level_name}]")
        
        if self.include_logger:
            parts.append(f"[{record.logger_name}]")
        
        parts.append(record.message)
        
        return " ".join(parts)


class ColoredFormatter(LogFormatter):
    """Colored log formatter for terminal output."""
    
    # ANSI color codes
    COLORS = {
        LogLevel.DEBUG: "\033[36m",      # Cyan
        LogLevel.INFO: "\033[32m",       # Green
        LogLevel.WARNING: "\033[33m",    # Yellow
        LogLevel.ERROR: "\033[31m",      # Red
        LogLevel.CRITICAL: "\033[35m",   # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.level, "")
        level_name = record.level.name
        
        timestamp = record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        message = f"{color}[{timestamp}] [{level_name}] {record.message}{self.RESET}"
        
        return message


class LogHandler:
    """Base class for log handlers."""
    
    def __init__(self, formatter: Optional[LogFormatter] = None) -> None:
        """
        Initialize log handler.
        
        Args:
            formatter: Formatter to use for output
        """
        self.formatter = formatter or SimpleFormatter()
        self.level = LogLevel.DEBUG
    
    def set_level(self, level: LogLevel) -> None:
        """Set minimum log level for this handler."""
        self.level = level
    
    def set_formatter(self, formatter: LogFormatter) -> None:
        """Set formatter for this handler."""
        self.formatter = formatter
    
    def emit(self, record: LogRecord) -> None:
        """Emit a log record."""
        if record.level.value >= self.level.value:
            self.write(self.formatter.format(record))
    
    def write(self, message: str) -> None:
        """Write formatted message."""
        raise NotImplementedError
    
    def close(self) -> None:
        """Close the handler."""
        pass


class ConsoleHandler(LogHandler):
    """Handler that writes to console (stdout/stderr)."""
    
    def __init__(self, use_stderr: bool = False, formatter: Optional[LogFormatter] = None) -> None:
        """
        Initialize console handler.
        
        Args:
            use_stderr: Whether to write to stderr instead of stdout
            formatter: Formatter to use
        """
        super().__init__(formatter)
        self.stream = sys.stderr if use_stderr else sys.stdout
    
    def write(self, message: str) -> None:
        """Write message to console."""
        self.stream.write(message + "\n")
        self.stream.flush()


class FileHandler(LogHandler):
    """Handler that writes to a file."""
    
    def __init__(self, filename: str, mode: str = "a", formatter: Optional[LogFormatter] = None) -> None:
        """
        Initialize file handler.
        
        Args:
            filename: Path to log file
            mode: File mode ('a' for append, 'w' for overwrite)
            formatter: Formatter to use
        """
        super().__init__(formatter)
        self.filename = filename
        self.mode = mode
        self.file = None
        self._open_file()
    
    def _open_file(self) -> None:
        """Open the log file."""
        # Create directory if it doesn't exist
        Path(self.filename).parent.mkdir(parents=True, exist_ok=True)
        self.file = open(self.filename, self.mode, encoding='utf-8')
    
    def write(self, message: str) -> None:
        """Write message to file."""
        if self.file:
            self.file.write(message + "\n")
            self.file.flush()
    
    def close(self) -> None:
        """Close the file."""
        if self.file:
            self.file.close()
            self.file = None


class CallbackHandler(LogHandler):
    """Handler that calls a callback function with log messages."""
    
    def __init__(self, callback: Callable[[str], None], formatter: Optional[LogFormatter] = None) -> None:
        """
        Initialize callback handler.
        
        Args:
            callback: Function to call with formatted message
            formatter: Formatter to use
        """
        super().__init__(formatter)
        self.callback = callback
    
    def write(self, message: str) -> None:
        """Call callback with message."""
        self.callback(message)


class Logger:
    """Logger class for logging messages."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize logger.
        
        Args:
            name: Logger name
        """
        self.name = name
        self.handlers: List[LogHandler] = []
        self.level = LogLevel.DEBUG
    
    def add_handler(self, handler: LogHandler) -> None:
        """Add a handler to this logger."""
        self.handlers.append(handler)
    
    def remove_handler(self, handler: LogHandler) -> None:
        """Remove a handler from this logger."""
        if handler in self.handlers:
            self.handlers.remove(handler)
    
    def set_level(self, level: LogLevel) -> None:
        """Set minimum log level for this logger."""
        self.level = level
    
    def _log(self, level: LogLevel, message: str, extra: Optional[dict] = None) -> None:
        """
        Internal logging method.
        
        Args:
            level: Log level
            message: Log message
            extra: Extra data to include
        """
        if level.value >= self.level.value:
            record = LogRecord(
                timestamp=datetime.now(),
                level=level,
                message=message,
                logger_name=self.name,
                extra=extra or {}
            )
            
            for handler in self.handlers:
                handler.emit(record)
    
    def debug(self, message: str, extra: Optional[dict] = None) -> None:
        """Log debug message."""
        self._log(LogLevel.DEBUG, message, extra)
    
    def info(self, message: str, extra: Optional[dict] = None) -> None:
        """Log info message."""
        self._log(LogLevel.INFO, message, extra)
    
    def warning(self, message: str, extra: Optional[dict] = None) -> None:
        """Log warning message."""
        self._log(LogLevel.WARNING, message, extra)
    
    def error(self, message: str, extra: Optional[dict] = None) -> None:
        """Log error message."""
        self._log(LogLevel.ERROR, message, extra)
    
    def critical(self, message: str, extra: Optional[dict] = None) -> None:
        """Log critical message."""
        self._log(LogLevel.CRITICAL, message, extra)


class LoggerFactory:
    """Factory for creating and managing loggers."""
    
    _loggers: dict = {}
    
    @classmethod
    def get_logger(cls, name: str) -> Logger:
        """
        Get or create a logger with the given name.
        
        Args:
            name: Logger name
            
        Returns:
            Logger instance
        """
        if name not in cls._loggers:
            cls._loggers[name] = Logger(name)
        return cls._loggers[name]
    
    @classmethod
    def configure_default(cls, level: LogLevel = LogLevel.INFO) -> Logger:
        """
        Configure default logger with console handler.
        
        Args:
            level: Minimum log level
            
        Returns:
            Configured logger
        """
        logger = cls.get_logger("default")
        logger.set_level(level)
        
        # Add colored console handler
        console_handler = ConsoleHandler(formatter=ColoredFormatter())
        console_handler.set_level(level)
        logger.add_handler(console_handler)
        
        return logger


def main() -> None:
    """Demonstrate logging system."""
    
    print("=== Simple Logger ===")
    logger = Logger("MyApp")
    
    # Add console handler
    console_handler = ConsoleHandler(formatter=DetailedFormatter())
    logger.add_handler(console_handler)
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    print("\n=== Colored Logger ===")
    colored_logger = Logger("ColoredApp")
    colored_handler = ConsoleHandler(formatter=ColoredFormatter())
    colored_logger.add_handler(colored_handler)
    
    colored_logger.debug("Debug message")
    colored_logger.info("Info message")
    colored_logger.warning("Warning message")
    colored_logger.error("Error message")
    colored_logger.critical("Critical message")
    
    print("\n=== File Logger ===")
    file_logger = Logger("FileApp")
    file_handler = FileHandler("logs/app.log", formatter=DetailedFormatter())
    file_logger.add_handler(file_handler)
    
    file_logger.info("Application started")
    file_logger.warning("Low memory warning")
    file_logger.error("Connection failed")
    
    print(f"Logs written to logs/app.log")
    
    print("\n=== Callback Logger ===")
    messages = []
    
    def callback(message: str):
        messages.append(message)
    
    callback_logger = Logger("CallbackApp")
    callback_handler = CallbackHandler(callback, formatter=SimpleFormatter())
    callback_logger.add_handler(callback_handler)
    
    callback_logger.info("Message 1")
    callback_logger.info("Message 2")
    
    print(f"Captured messages: {messages}")
    
    print("\n=== Logger Factory ===")
    default_logger = LoggerFactory.configure_default(LogLevel.INFO)
    default_logger.info("Using default logger")
    default_logger.debug("This won't show (below INFO level)")
    
    print("\n=== Multiple Handlers ===")
    multi_logger = Logger("MultiApp")
    multi_logger.add_handler(ConsoleHandler(formatter=ColoredFormatter()))
    multi_logger.add_handler(FileHandler("logs/multi.log", formatter=DetailedFormatter()))
    
    multi_logger.info("This goes to both console and file")
    print(f"Also written to logs/multi.log")


if __name__ == "__main__":
    main()
