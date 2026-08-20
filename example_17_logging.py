import logging
import sys

def setup_logger():
    """Configures a custom logger that outputs to both console and file."""
    
    # Create a custom logger
    logger = logging.getLogger("MyApp_Logger")
    
    # Set the base logging level (DEBUG catches everything)
    logger.setLevel(logging.DEBUG)
    
    # Define the format of our log messages
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
    )
    
    # 1. Console Handler (outputs to terminal)
    # Let's only output INFO and above to the console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # 2. File Handler (outputs to a file)
    # We'll save ALL logs (DEBUG and above) to this file
    file_handler = logging.FileHandler("app_debug.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Add both handlers to our logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def perform_operation(logger, x, y):
    """A sample function that logs different events."""
    logger.info("Starting operation perform_operation()")
    logger.debug(f"Input values received: x={x}, y={y}")
    
    try:
        if x < 0 or y < 0:
            logger.warning("One of the inputs is negative. This might lead to unexpected results.")
            
        result = x / y
        logger.debug(f"Computation successful. Result is {result}")
        return result
        
    except ZeroDivisionError:
        # exc_info=True automatically attaches the full traceback to the log!
        logger.error("Attempted to divide by zero!", exc_info=True)
        return None
    except Exception as e:
        logger.critical(f"A critical unexpected error occurred: {e}", exc_info=True)
        return None

if __name__ == "__main__":
    app_logger = setup_logger()
    
    print("Running operations... (check 'app_debug.log' for detailed logs!)")
    
    # 1. Normal operation
    perform_operation(app_logger, 10, 2)
    
    # 2. Operation triggering a warning
    perform_operation(app_logger, -5, 2)
    
    # 3. Operation triggering an error (division by zero)
    perform_operation(app_logger, 10, 0)
    
    app_logger.info("Application finished.")
