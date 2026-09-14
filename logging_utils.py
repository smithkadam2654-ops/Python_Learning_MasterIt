"""
Logging Utilities - Logging configuration and utilities.
Features: Custom loggers, log formatting, file handlers, and log rotation.
"""

import logging
import sys
from typing import Optional
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime


class LoggerConfig:
    """Logger configuration utilities."""
    
    @staticmethod
    def setup_logger(name: str, level: int = logging.INFO,
                    log_file: Optional[str] = None,
                    format_string: str = None) -> logging.Logger:
        """
        Setup logger with console and optional file handler.
        
        Args:
            name: Logger name
            level: Logging level
            log_file: Optional log file path
            format_string: Custom format string
            
        Returns:
            Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Remove existing handlers
        logger.handlers.clear()
        
        # Default format
        if format_string is None:
            format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        formatter = logging.Formatter(format_string)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    @staticmethod
    def setup_rotating_logger(name: str, log_file: str,
                            max_bytes: int = 10 * 1024 * 1024,
                            backup_count: int = 5,
                            level: int = logging.INFO) -> logging.Logger:
        """
        Setup logger with rotating file handler.
        
        Args:
            name: Logger name
            log_file: Log file path
            max_bytes: Maximum file size before rotation
            backup_count: Number of backup files to keep
            level: Logging level
            
        Returns:
            Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.handlers.clear()
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Rotating file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    @staticmethod
    def setup_timed_rotating_logger(name: str, log_file: str,
                                   when: str = 'midnight',
                                   interval: int = 1,
                                   backup_count: int = 7,
                                   level: int = logging.INFO) -> logging.Logger:
        """
        Setup logger with time-based rotating file handler.
        
        Args:
            name: Logger name
            log_file: Log file path
            when: When to rotate ('S', 'M', 'H', 'D', 'midnight', etc.)
            interval: Rotation interval
            backup_count: Number of backup files to keep
            level: Logging level
            
        Returns:
            Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.handlers.clear()
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Timed rotating file handler
        file_handler = TimedRotatingFileHandler(
            log_file,
            when=when,
            interval=interval,
            backupCount=backup_count
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for console output."""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{log_color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


class StructuredLogger:
    """Structured logger with JSON-like output."""
    
    def __init__(self, name: str, level: int = logging.INFO) -> None:
        """
        Initialize structured logger.
        
        Args:
            name: Logger name
            level: Logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
    
    def log(self, level: str, message: str, **kwargs) -> None:
        """
        Log structured message.
        
        Args:
            level: Log level
            message: Log message
            **kwargs: Additional fields
        """
        import json
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'message': message,
            **kwargs
        }
        self.logger.log(getattr(logging, level.upper()), json.dumps(log_data))
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.log('DEBUG', message, **kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self.log('INFO', message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.log('WARNING', message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self.log('ERROR', message, **kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message."""
        self.log('CRITICAL', message, **kwargs)


class LogContext:
    """Context manager for logging with context."""
    
    def __init__(self, logger: logging.Logger, context: dict) -> None:
        """
        Initialize log context.
        
        Args:
            logger: Logger instance
            context: Context dictionary
        """
        self.logger = logger
        self.context = context
        self.old_factory = None
    
    def __enter__(self) -> 'LogContext':
        """Enter context."""
        self.old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            for key, value in self.context.items():
                setattr(record, key, value)
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context."""
        logging.setLogRecordFactory(self.old_factory)


class PerformanceLogger:
    """Logger for performance monitoring."""
    
    def __init__(self, logger: logging.Logger) -> None:
        """
        Initialize performance logger.
        
        Args:
            logger: Logger instance
        """
        self.logger = logger
        self.start_time = None
    
    def start(self) -> None:
        """Start timing."""
        self.start_time = datetime.utcnow()
        self.logger.info("Performance tracking started")
    
    def stop(self, operation: str) -> float:
        """
        Stop timing and log duration.
        
        Args:
            operation: Operation name
            
        Returns:
            Duration in seconds
        """
        if self.start_time is None:
            self.logger.warning("Performance tracking not started")
            return 0
        
        end_time = datetime.utcnow()
        duration = (end_time - self.start_time).total_seconds()
        
        self.logger.info(f"Operation '{operation}' completed in {duration:.3f}s")
        self.start_time = None
        
        return duration


class LogFilter:
    """Custom log filter."""
    
    def __init__(self, level: int) -> None:
        """
        Initialize log filter.
        
        Args:
            level: Minimum log level
        """
        self.level = level
    
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log record.
        
        Args:
            record: Log record
            
        Returns:
            True if record should be logged
        """
        return record.levelno >= self.level


def main() -> None:
    """Demonstrate logging utilities."""
    
    print("=== Logging Utilities Demo ===")
    
    # Basic logger
    print("\n--- Basic Logger ---")
    logger = LoggerConfig.setup_logger("demo", logging.INFO)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Colored formatter
    print("\n--- Colored Logger ---")
    logger = logging.getLogger("colored")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    
    logger.info("This should be green")
    logger.warning("This should be yellow")
    logger.error("This should be red")
    
    # Structured logger
    print("\n--- Structured Logger ---")
    struct_logger = StructuredLogger("structured")
    struct_logger.info("User logged in", user_id=123, ip="192.168.1.1")
    struct_logger.error("Database connection failed", error_code=500, retry=3)
    
    # Performance logger
    print("\n--- Performance Logger ---")
    perf_logger = LoggerConfig.setup_logger("perf", logging.INFO)
    perf = PerformanceLogger(perf_logger)
    
    perf.start()
    import time
    time.sleep(0.1)
    perf.stop("test operation")
    
    # Log context
    print("\n--- Log Context ---")
    logger = LoggerConfig.setup_logger("context", logging.INFO)
    
    with LogContext(logger, {'user_id': '123', 'session': 'abc'}):
        logger.info("Message with context")
    
    # Custom filter
    print("\n--- Custom Filter ---")
    logger = logging.getLogger("filtered")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    handler.addFilter(LogFilter(logging.WARNING))
    logger.addHandler(handler)
    
    logger.debug("This won't show")
    logger.info("This won't show")
    logger.warning("This will show")
    logger.error("This will show")


if __name__ == "__main__":
    main()
