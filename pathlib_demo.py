from pathlib import Path
import os

def demonstrate_pathlib():
    """Demonstrate modern object-oriented file paths with pathlib."""
    
    print("--- 1. Creating and Inspecting Paths ---")
    # Get the current directory
    current_dir = Path.cwd()
    print(f"Current Directory: {current_dir}")
    
    # Get the parent directory
    print(f"Parent Directory: {current_dir.parent}")
    
    # Build a path gracefully (no need for os.path.join!)
    test_folder = current_dir / "my_test_folder"
    test_file = test_folder / "hello.txt"
    print(f"Target File Path: {test_file}")
    
    print("\n--- 2. File and Directory Operations ---")
    # Create the directory (parents=True acts like 'mkdir -p', exist_ok ignores errors if it exists)
    test_folder.mkdir(parents=True, exist_ok=True)
    
    # Write text to the file directly
    test_file.write_text("Hello, Pathlib is amazing!")
    
    # Check if it exists and read it back
    if test_file.exists() and test_file.is_file():
        content = test_file.read_text()
        print(f"File Content: '{content}'")
        
        # Get metadata
        print(f"File Name: {test_file.name}")
        print(f"File Extension: {test_file.suffix}")
        print(f"File Size (bytes): {test_file.stat().st_size}")
        
    print("\n--- 3. Cleanup ---")
    # Clean up the file and folder
    test_file.unlink() # Deletes the file
    test_folder.rmdir() # Deletes the empty directory
    print("Cleaned up the test file and folder.")

if __name__ == "__main__":
    demonstrate_pathlib()
