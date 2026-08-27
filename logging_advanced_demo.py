import logging
import sys

def configure_logger():
    """Configure a custom logger with handlers for console and file."""
    # Create a custom logger
    logger = logging.getLogger("AppLogger")
    logger.setLevel(logging.DEBUG)
    
    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler("app_demo.log")
    
    # Set levels for handlers
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)
    
    # Create formatters and add it to handlers
    console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)
    
    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def demonstrate_logging():
    """Demonstrate the custom logger."""
    logger = configure_logger()
    
    logger.debug("This is a debug message. (Only goes to the file)")
    logger.info("This is an info message. (Goes to console and file)")
    logger.warning("This is a warning message.")
    
    try:
        result = 10 / 0
    except ZeroDivisionError:
        logger.error("An error occurred during division", exc_info=True)
        
    print("\nCheck 'app_demo.log' to see the detailed file logs!")

if __name__ == "__main__":
    demonstrate_logging()
