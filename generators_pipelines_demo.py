def read_data(filename):
    """Generator to simulate reading lines from a large file."""
    lines = [
        "ERROR: User login failed",
        "INFO: Application started",
        "WARNING: Low memory",
        "ERROR: Database connection timeout",
        "INFO: Data saved successfully"
    ]
    for line in lines:
        yield line

def filter_errors(lines):
    """Generator to filter only ERROR lines."""
    for line in lines:
        if "ERROR" in line:
            yield line

def extract_message(lines):
    """Generator to extract the message part from the line."""
    for line in lines:
        parts = line.split(":", 1)
        if len(parts) > 1:
            yield parts[1].strip()

def demonstrate_generator_pipeline():
    """Demonstrate chaining generators to form a pipeline."""
    print("--- Generator Pipeline ---")
    
    # 1. Start the pipeline
    lines = read_data("dummy_file.log")
    
    # 2. Add the filter stage
    error_lines = filter_errors(lines)
    
    # 3. Add the extraction stage
    error_messages = extract_message(error_lines)
    
    # The pipeline is fully lazy! No processing happens until we iterate
    print("Executing pipeline to find errors:")
    for msg in error_messages:
        print(f"- {msg}")

if __name__ == "__main__":
    demonstrate_generator_pipeline()
