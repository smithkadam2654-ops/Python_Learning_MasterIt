import os

def demonstrate_os_module():
    """Demonstrate basic interactions with the operating system."""
    
    print("--- Environment Variables ---")
    # Get a specific environment variable
    user = os.getenv("USER") or os.getenv("USERNAME") or "Unknown"
    print(f"Current User: {user}")
    
    print("\n--- Working Directory & Paths ---")
    # Get current working directory
    cwd = os.getcwd()
    print(f"Current Working Directory: {cwd}")
    
    # Join paths safely (cross-platform)
    test_dir = os.path.join(cwd, "test_folder_demo")
    print(f"Path to test directory: {test_dir}")
    
    print("\n--- Directory Operations ---")
    # Create a directory if it doesn't exist
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
        print(f"Created directory: {test_dir}")
    else:
        print(f"Directory already exists: {test_dir}")
        
    # List contents of a directory
    print("\nContents of current directory (first 5 items):")
    contents = os.listdir(cwd)
    for item in contents[:5]:
        print(f"- {item}")
        
    # Clean up (Remove the directory we just created)
    if os.path.exists(test_dir):
        os.rmdir(test_dir)
        print(f"\nCleaned up: removed {test_dir}")

if __name__ == "__main__":
    demonstrate_os_module()
