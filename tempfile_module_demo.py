import tempfile
import os

def demonstrate_tempfile():
    """Demonstrate creating temporary files and directories that clean up after themselves."""
    
    print("--- 1. Temporary Files ---")
    # Create a temporary file that is automatically deleted when closed
    # We use mode 'w+t' to read and write text instead of bytes
    with tempfile.TemporaryFile(mode='w+t') as temp_file:
        print(f"Created a temporary file.")
        
        # Write to it
        temp_file.write("This is some highly sensitive temporary data.\n")
        temp_file.write("It will vanish as soon as the block ends.")
        
        # Seek back to the beginning to read it
        temp_file.seek(0)
        print("Reading back from the temp file:")
        print(temp_file.read())
        
    print("Temp file is now deleted.")
    
    print("\n--- 2. Named Temporary Files ---")
    # Sometimes you need the file to have a name in the filesystem (e.g., to pass to another program)
    with tempfile.NamedTemporaryFile(mode='w+t', delete=True) as named_temp:
        print(f"Created Named Temp File at: {named_temp.name}")
        named_temp.write("Data in a named file.")
        
        # The file exists in the OS right now!
        print(f"Does it exist in OS? {os.path.exists(named_temp.name)}")
        
    print(f"Does it exist after closing? {os.path.exists(named_temp.name)}")
    
    print("\n--- 3. Temporary Directories ---")
    # Create an entire temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temporary directory at: {temp_dir}")
        # You can create files inside here, and the WHOLE directory gets wiped when done!
        
    print("Temp directory is now deleted.")

if __name__ == "__main__":
    demonstrate_tempfile()
