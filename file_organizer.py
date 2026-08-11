#!/usr/bin/env python3
"""
File Organizer
Organize files in a directory by file type into categorized subfolders
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List

class FileOrganizer:
    def __init__(self, source_dir: str):
        self.source_dir = Path(source_dir)
        self.file_categories = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf', '.odt'],
            'spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
            'presentations': ['.ppt', '.pptx', '.odp'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php'],
            'fonts': ['.ttf', '.otf', '.woff', '.woff2'],
            'others': []  # Catch-all category
        }
    
    def organize_files(self, dry_run: bool = False) -> Dict[str, List[str]]:
        """Organize files by type."""
        organized_files = {category: [] for category in self.file_categories}
        
        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                file_extension = file_path.suffix.lower()
                
                # Find the appropriate category
                target_category = 'others'
                for category, extensions in self.file_categories.items():
                    if file_extension in extensions:
                        target_category = category
                        break
                
                # Create target directory if it doesn't exist
                target_dir = self.source_dir / target_category
                if not target_dir.exists():
                    target_dir.mkdir(exist_ok=True)
                
                # Move the file
                target_path = target_dir / file_path.name
                if dry_run:
                    print(f"Would move: {file_path} -> {target_path}")
                else:
                    shutil.move(str(file_path), str(target_path))
                    print(f"Moved: {file_path} -> {target_path}")
                
                organized_files[target_category].append(file_path.name)
        
        return organized_files
    
    def preview_organization(self) -> Dict[str, List[str]]:
        """Preview how files would be organized without moving them."""
        organized_files = {category: [] for category in self.file_categories}
        
        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                file_extension = file_path.suffix.lower()
                
                target_category = 'others'
                for category, extensions in self.file_categories.items():
                    if file_extension in extensions:
                        target_category = category
                        break
                
                organized_files[target_category].append(file_path.name)
        
        return organized_files

def main():
    print("=== File Organizer ===")
    
    source_dir = input("Enter directory path to organize: ").strip()
    
    if not os.path.exists(source_dir):
        print("Directory does not exist!")
        return
    
    organizer = FileOrganizer(source_dir)
    
    # Show preview
    print("\nPreview of organization:")
    preview = organizer.preview_organization()
    for category, files in preview.items():
        if files:
            print(f"\n{category.upper()} ({len(files)} files):")
            for file in files[:5]:  # Show first 5 files
                print(f"  - {file}")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more")
    
    # Ask for confirmation
    confirm = input(f"\nOrganize files in {source_dir}? (y/n): ").lower().strip()
    
    if confirm == 'y':
        organized = organizer.organize_files()
        print("\nOrganization complete!")
        for category, files in organized.items():
            if files:
                print(f"Moved {len(files)} files to {category}/")
    else:
        print("Organization cancelled.")

if __name__ == "__main__":
    main()