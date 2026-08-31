import logging

def setup_logging():
    # Configure the logging system
    # This replaces print() for professional applications
    logging.basicConfig(
        level=logging.DEBUG, # Set the minimum level to display (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def perform_operation(x, y):
    logging.info(f"Starting operation with {x} and {y}")
    
    try:
        logging.debug("Attempting to divide the numbers.")
        result = x / y
        logging.info(f"Operation successful. Result: {result}")
        return result
        
    except ZeroDivisionError:
        # Use logging.error to record problems
        # exc_info=True prints the stack trace for debugging
        logging.error("Attempted to divide by zero!", exc_info=False)
        return None
        
    except Exception as e:
        logging.critical(f"An unexpected critical error occurred: {e}")
        return None

if __name__ == "__main__":
    setup_logging()
    
    logging.debug("Program started.")
    
    perform_operation(10, 2)
    print("-" * 50) # Just a separator for readability in the console
    perform_operation(10, 0)
    
    logging.debug("Program finished.")
