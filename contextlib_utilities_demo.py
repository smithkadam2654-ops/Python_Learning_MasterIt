import contextlib
import os

@contextlib.contextmanager
def change_dir(destination):
    """A context manager to temporarily change the working directory."""
    try:
        # Save the original directory
        cwd = os.getcwd()
        # Change to the new directory
        os.chdir(destination)
        yield
    finally:
        # Always change back, even if an exception occurs
        os.chdir(cwd)

def demonstrate_contextlib():
    print("--- Custom Context Manager using @contextmanager ---")
    print(f"Original directory: {os.getcwd()}")
    
    # We use '..' to temporarily go up one directory
    with change_dir(".."):
        print(f"Temporarily in: {os.getcwd()}")
        
    print(f"Back to original directory: {os.getcwd()}")
    
    print("\n--- Using contextlib.suppress ---")
    # contextlib.suppress allows you to explicitly ignore specific exceptions
    # instead of writing a full try/except/pass block.
    
    # Let's try to remove a file that doesn't exist
    fake_file = "this_file_does_not_exist.txt"
    
    with contextlib.suppress(FileNotFoundError):
        os.remove(fake_file)
        
    print("Execution continued successfully because the FileNotFoundError was suppressed!")

if __name__ == "__main__":
    demonstrate_contextlib()
