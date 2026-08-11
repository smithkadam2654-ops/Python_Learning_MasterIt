#!/usr/bin/env python3
"""
File Backup Script
Performs backup of directories with timestamping and compression
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_backup(source_dir, backup_dir='backups'):
    """Create a timestamped backup of a directory."""
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory '{source_dir}' not found")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"backup_{timestamp}"
    backup_path = os.path.join(backup_dir, backup_name)
    
    # Create backup directory
    os.makedirs(backup_path, exist_ok=True)
    
    # Copy files recursively
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(backup_path, item)
        
        if os.path.isdir(source_item):
            shutil.copytree(source_item, dest_item)
        else:
            shutil.copy2(source_item, dest_item)
    
    # Create zip archive
    zip_path = f"{backup_path}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, backup_path)
                zipf.write(file_path, arcname)
    
    # Remove uncompressed directory
    shutil.rmtree(backup_path)
    
    print(f"Backup created: {zip_path}")
    return zip_path

def backup_multiple_dirs(directories):
    """Create backups for multiple directories."""
    backups = []
    for source_dir in directories:
        try:
            backup_path = create_backup(source_dir)
            backups.append(backup_path)
        except Exception as e:
            print(f"Error backing up {source_dir}: {e}")
    
    return backups

if __name__ == "__main__":
    # Example usage
    print("=== File Backup Script ===")
    
    # Create backups directory if it doesn't exist
    if not os.path.exists('backups'):
        os.makedirs('backups')
    
    # Test with current directory
    current_backup = create_backup('.', 'backups')
    print(f"Backup created: {current_backup}")