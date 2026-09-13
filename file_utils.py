"""
File Operations - File system operations and utilities.
Features: File I/O, directory operations, file searching, and path manipulation.
"""

import os
import shutil
import glob
from typing import List, Optional
from pathlib import Path


class FileUtils:
    """File operation utilities."""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Read entire file content.
        
        Args:
            file_path: Path to file
            
        Returns:
            File content as string
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """
        Write content to file.
        
        Args:
            file_path: Path to file
            content: Content to write
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def append_file(file_path: str, content: str) -> None:
        """
        Append content to file.
        
        Args:
            file_path: Path to file
            content: Content to append
        """
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def read_lines(file_path: str) -> List[str]:
        """
        Read file lines.
        
        Args:
            file_path: Path to file
            
        Returns:
            List of lines
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    
    @staticmethod
    def write_lines(file_path: str, lines: List[str]) -> None:
        """
        Write lines to file.
        
        Args:
            file_path: Path to file
            lines: List of lines to write
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """
        Check if file exists.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file exists
        """
        return os.path.isfile(file_path)
    
    @staticmethod
    def directory_exists(dir_path: str) -> bool:
        """
        Check if directory exists.
        
        Args:
            dir_path: Path to directory
            
        Returns:
            True if directory exists
        """
        return os.path.isdir(dir_path)
    
    @staticmethod
    def create_directory(dir_path: str) -> None:
        """
        Create directory (including parents).
        
        Args:
            dir_path: Path to directory
        """
        os.makedirs(dir_path, exist_ok=True)
    
    @staticmethod
    def delete_file(file_path: str) -> None:
        """
        Delete file.
        
        Args:
            file_path: Path to file
        """
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    @staticmethod
    def delete_directory(dir_path: str) -> None:
        """
        Delete directory and contents.
        
        Args:
            dir_path: Path to directory
        """
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
    
    @staticmethod
    def copy_file(src: str, dst: str) -> None:
        """
        Copy file.
        
        Args:
            src: Source path
            dst: Destination path
        """
        shutil.copy2(src, dst)
    
    @staticmethod
    def copy_directory(src: str, dst: str) -> None:
        """
        Copy directory.
        
        Args:
            src: Source path
            dst: Destination path
        """
        shutil.copytree(src, dst)
    
    @staticmethod
    def move_file(src: str, dst: str) -> None:
        """
        Move file.
        
        Args:
            src: Source path
            dst: Destination path
        """
        shutil.move(src, dst)
    
    @staticmethod
    def rename_file(old_path: str, new_path: str) -> None:
        """
        Rename file.
        
        Args:
            old_path: Old path
            new_path: New path
        """
        os.rename(old_path, new_path)
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to file
            
        Returns:
            File size in bytes
        """
        return os.path.getsize(file_path)
    
    @staticmethod
    def list_directory(dir_path: str) -> List[str]:
        """
        List directory contents.
        
        Args:
            dir_path: Path to directory
            
        Returns:
            List of file/directory names
        """
        return os.listdir(dir_path)
    
    @staticmethod
    def list_files(dir_path: str, recursive: bool = False) -> List[str]:
        """
        List all files in directory.
        
        Args:
            dir_path: Path to directory
            recursive: Include subdirectories
            
        Returns:
            List of file paths
        """
        if recursive:
            files = []
            for root, _, filenames in os.walk(dir_path):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
            return files
        else:
            return [os.path.join(dir_path, f) for f in os.listdir(dir_path) 
                   if os.path.isfile(os.path.join(dir_path, f))]
    
    @staticmethod
    def list_directories(dir_path: str, recursive: bool = False) -> List[str]:
        """
        List all directories.
        
        Args:
            dir_path: Path to directory
            recursive: Include subdirectories
            
        Returns:
            List of directory paths
        """
        if recursive:
            dirs = []
            for root, dirnames, _ in os.walk(dir_path):
                for dirname in dirnames:
                    dirs.append(os.path.join(root, dirname))
            return dirs
        else:
            return [os.path.join(dir_path, d) for d in os.listdir(dir_path) 
                   if os.path.isdir(os.path.join(dir_path, d))]
    
    @staticmethod
    def find_files(pattern: str, dir_path: str = ".") -> List[str]:
        """
        Find files matching pattern.
        
        Args:
            pattern: Glob pattern
            dir_path: Directory to search
            
        Returns:
            List of matching file paths
        """
        return glob.glob(os.path.join(dir_path, pattern))
    
    @staticmethod
    def get文件扩展名(file_path: str) -> str:
        """
        Get file extension.
        
        Args:
            file_path: Path to file
            
        Returns:
            File extension (including dot)
        """
        return os.path.splitext(file_path)[1]
    
    @staticmethod
    def get_filename(file_path: str) -> str:
        """
        Get filename without path.
        
        Args:
            file_path: Path to file
            
        Returns:
            Filename
        """
        return os.path.basename(file_path)
    
    @staticmethod
    def get_directory(file_path: str) -> str:
        """
        Get directory from file path.
        
        Args:
            file_path: Path to file
            
        Returns:
            Directory path
        """
        return os.path.dirname(file_path)
    
    @staticmethod
    def join_paths(*paths: str) -> str:
        """
        Join path components.
        
        Args:
            *paths: Path components
            
        Returns:
            Joined path
        """
        return os.path.join(*paths)
    
    @staticmethod
    def normalize_path(path: str) -> str:
        """
        Normalize path.
        
        Args:
            path: Path to normalize
            
        Returns:
            Normalized path
        """
        return os.path.normpath(path)
    
    @staticmethod
    def absolute_path(path: str) -> str:
        """
        Get absolute path.
        
        Args:
            path: Path to convert
            
        Returns:
            Absolute path
        """
        return os.path.abspath(path)
    
    @staticmethod
    def get_current_directory() -> str:
        """
        Get current working directory.
        
        Returns:
            Current directory path
        """
        return os.getcwd()
    
    @staticmethod
    def change_directory(dir_path: str) -> None:
        """
        Change current directory.
        
        Args:
            dir_path: New directory path
        """
        os.chdir(dir_path)
    
    @staticmethod
    def create_temp_file(suffix: str = ".tmp") -> str:
        """
        Create temporary file.
        
        Args:
            suffix: File suffix
            
        Returns:
            Path to temporary file
        """
        import tempfile
        fd, path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        return path
    
    @staticmethod
    def create_temp_directory() -> str:
        """
        Create temporary directory.
        
        Returns:
            Path to temporary directory
        """
        import tempfile
        return tempfile.mkdtemp()
    
    @staticmethod
    def get_file_mtime(file_path: str) -> float:
        """
        Get file modification time.
        
        Args:
            file_path: Path to file
            
        Returns:
            Modification timestamp
        """
        return os.path.getmtime(file_path)
    
    @staticmethod
    def get_file_ctime(file_path: str) -> float:
        """
        Get file creation time.
        
        Args:
            file_path: Path to file
            
        Returns:
            Creation timestamp
        """
        return os.path.getctime(file_path)
    
    @staticmethod
    def is_file_empty(file_path: str) -> bool:
        """
        Check if file is empty.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file is empty
        """
        return os.path.getsize(file_path) == 0
    
    @staticmethod
    def count_lines(file_path: str) -> int:
        """
        Count lines in file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Number of lines
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    
    @staticmethod
    def count_words(file_path: str) -> int:
        """
        Count words in file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Number of words
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.read().split())
    
    @staticmethod
    def search_in_file(file_path: str, pattern: str) -> List[int]:
        """
        Search for pattern in file.
        
        Args:
            file_path: Path to file
            pattern: Pattern to search
            
        Returns:
            List of line numbers where pattern found
        """
        lines = FileUtils.read_lines(file_path)
        matching_lines = []
        
        for i, line in enumerate(lines):
            if pattern in line:
                matching_lines.append(i + 1)
        
        return matching_lines
    
    @staticmethod
    def replace_in_file(file_path: str, old: str, new: str) -> int:
        """
        Replace pattern in file.
        
        Args:
            file_path: Path to file
            old: Pattern to replace
            new: Replacement pattern
            
        Returns:
            Number of replacements
        """
        content = FileUtils.read_file(file_path)
        count = content.count(old)
        content = content.replace(old, new)
        FileUtils.write_file(file_path, content)
        return count


class PathUtils:
    """Path manipulation utilities using pathlib."""
    
    @staticmethod
    def join(*paths: str) -> Path:
        """
        Join paths using pathlib.
        
        Args:
            *paths: Path components
            
        Returns:
            Joined Path object
        """
        return Path(paths[0]).joinpath(*paths[1:])
    
    @staticmethod
    def get_parent(path: str) -> Path:
        """
        Get parent directory.
        
        Args:
            path: Path to file/directory
            
        Returns:
            Parent Path object
        """
        return Path(path).parent
    
    @staticmethod
    def get_stem(path: str) -> str:
        """
        Get filename without extension.
        
        Args:
            path: Path to file
            
        Returns:
            Filename stem
        """
        return Path(path).stem
    
    @staticmethod
    def get_suffix(path: str) -> str:
        """
        Get file extension.
        
        Args:
            path: Path to file
            
        Returns:
            File extension
        """
        return Path(path).suffix
    
    @staticmethod
    def resolve(path: str) -> Path:
        """
        Resolve absolute path.
        
        Args:
            path: Path to resolve
            
        Returns:
            Resolved Path object
        """
        return Path(path).resolve()
    
    @staticmethod
    def mkdir_p(path: str) -> None:
        """
        Create directory and parents.
        
        Args:
            path: Path to create
        """
        Path(path).mkdir(parents=True, exist_ok=True)


def main() -> None:
    """Demonstrate file operations."""
    
    print("=== File Operations Demo ===")
    
    # Create temp directory for demo
    temp_dir = FileUtils.create_temp_directory()
    print(f"Created temp directory: {temp_dir}")
    
    # Write and read
    test_file = FileUtils.join_paths(temp_dir, "test.txt")
    FileUtils.write_file(test_file, "Hello, World!\nThis is a test file.")
    print(f"Written to: {test_file}")
    
    content = FileUtils.read_file(test_file)
    print(f"Read content: {content}")
    
    # File info
    print(f"\n--- File Info ---")
    print(f"Exists: {FileUtils.file_exists(test_file)}")
    print(f"Size: {FileUtils.get_file_size(test_file)} bytes")
    print(f"Lines: {FileUtils.count_lines(test_file)}")
    print(f"Words: {FileUtils.count_words(test_file)}")
    
    # List directory
    print(f"\n--- Directory Listing ---")
    print(f"Files: {FileUtils.list_files(temp_dir)}")
    
    # Copy
    copy_file = FileUtils.join_paths(temp_dir, "copy.txt")
    FileUtils.copy_file(test_file, copy_file)
    print(f"Copied to: {copy_file}")
    
    # Search
    print(f"\n--- Search ---")
    pattern = "test"
    lines = FileUtils.search_in_file(test_file, pattern)
    print(f"'{pattern}' found on lines: {lines}")
    
    # Replace
    count = FileUtils.replace_in_file(copy_file, "test", "demo")
    print(f"Replaced {count} occurrences")
    
    # Path utilities
    print(f"\n--- Path Utilities ---")
    print(f"Filename: {FileUtils.get_filename(test_file)}")
    print(f"Extension: {FileUtils.get文件扩展名(test_file)}")
    print(f"Directory: {FileUtils.get_directory(test_file)}")
    
    # Cleanup
    FileUtils.delete_directory(temp_dir)
    print(f"\nCleaned up temp directory")


if __name__ == "__main__":
    main()
