import os

def demonstrate_file_operations():
    """Demonstrate basic file writing and reading."""
    file_name = "sample_data.txt"
    
    # 1. Writing to a file
    print("Writing to file...")
    with open(file_name, 'w') as file:
        file.write("Hello, this is the first line.\n")
        file.write("Here is a second line with some more text.\n")
        file.write("And a final third line.\n")
    
    # 2. Reading from a file
    print("\nReading from file:")
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            content = file.read()
            print("--- Start of file ---")
            print(content, end='')
            print("--- End of file ---")
            
        # Clean up by removing the file after we're done
        os.remove(file_name)
        print(f"\nRemoved '{file_name}' to clean up.")
    else:
        print("File was not found!")

# Example usage
if __name__ == "__main__":
    demonstrate_file_operations()
