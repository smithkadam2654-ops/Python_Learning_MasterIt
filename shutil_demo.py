import shutil
import os

def demonstrate_shutil():
    """Demonstrate high-level file and directory operations with shutil."""
    
    # Create a dummy file for us to work with
    source_file = "dummy_source.txt"
    with open(source_file, 'w') as f:
        f.write("This is some dummy data.")
        
    print("--- 1. Copying Files ---")
    destination_file = "dummy_destination.txt"
    
    # copy2 copies the file AND its metadata (timestamps, permissions)
    shutil.copy2(source_file, destination_file)
    print(f"Copied '{source_file}' to '{destination_file}'")
    
    print("\n--- 2. Moving / Renaming Files ---")
    moved_file = "moved_dummy_data.txt"
    shutil.move(destination_file, moved_file)
    print(f"Moved/Renamed '{destination_file}' to '{moved_file}'")
    
    print("\n--- 3. Creating Archives (Zips) ---")
    # Let's create a temporary directory and put our files inside
    test_dir = "archive_test_dir"
    os.makedirs(test_dir, exist_ok=True)
    shutil.move(source_file, os.path.join(test_dir, source_file))
    shutil.move(moved_file, os.path.join(test_dir, moved_file))
    
    # Now we zip the entire directory
    archive_name = "my_archive"
    shutil.make_archive(archive_name, 'zip', test_dir)
    print(f"Created archive: {archive_name}.zip containing '{test_dir}'")
    
    print("\n--- 4. Cleanup ---")
    # shutil.rmtree recursively deletes a directory and everything inside it
    shutil.rmtree(test_dir)
    os.remove(f"{archive_name}.zip")
    print("Cleaned up the test directory and zip file.")

if __name__ == "__main__":
    demonstrate_shutil()
