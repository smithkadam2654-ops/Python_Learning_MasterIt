import os
import hashlib
from collections import defaultdict

def hash_file(filepath):
    """
    Returns the SHA-256 hash of a file. 
    It reads in chunks so it doesn't crash on huge files!
    """
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            # Read and update hash in 8KB chunks
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        # Ignore files we don't have permission to read
        return None

def find_duplicates(directory):
    print(f"Scanning directory: {directory}")
    print("This might take a moment depending on the number of files...\n")
    
    # Dictionary to map file hashes to a list of file paths
    hashes = defaultdict(list)
    
    # Walk through the directory tree
    for root, _, files in os.walk(directory):
        # Skip git folders and python cache to be safe
        if '.git' in root or '__pycache__' in root:
            continue
            
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = hash_file(filepath)
            
            if file_hash:
                hashes[file_hash].append(filepath)
                
    # Filter the dictionary to only keep hashes that have MORE than 1 file
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    
    if not duplicates:
        print("✅ No duplicate files found!")
    else:
        print(f"⚠️ Found {len(duplicates)} sets of duplicates:")
        print("-" * 50)
        for i, (file_hash, paths) in enumerate(duplicates.items(), 1):
            print(f"Set {i} (Hash: {file_hash[:8]}...):")
            for path in paths:
                print(f"  - {path}")
            print()

if __name__ == "__main__":
    print("--- 🔍 Duplicate File Finder ---")
    target_dir = input("Enter directory path to scan (or press Enter for current folder): ").strip()
    
    if not target_dir:
        target_dir = os.getcwd()
        
    find_duplicates(target_dir)
