"""
File Processor - A robust file processing utility with error handling.
Features: File validation, batch processing, progress tracking, and logging.
"""

import os
from pathlib import Path
from typing import List, Callable, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import time


class FileType(Enum):
    """Supported file types for processing."""
    TEXT = "txt"
    CSV = "csv"
    JSON = "json"
    LOG = "log"


class ProcessingStatus(Enum):
    """Status of file processing operations."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ProcessingResult:
    """Result of a file processing operation."""
    file_path: str
    status: ProcessingStatus
    lines_processed: int = 0
    error_message: Optional[str] = None
    processing_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class FileProcessor:
    """Process files with validation and error handling."""

    def __init__(self, base_directory: str) -> None:
        """
        Initialize the file processor.
        
        Args:
            base_directory: Base directory for file operations
        """
        self.base_directory = Path(base_directory)
        self.results: List[ProcessingResult] = []
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """Create base directory if it doesn't exist."""
        self.base_directory.mkdir(parents=True, exist_ok=True)

    def validate_file(self, file_path: Path) -> bool:
        """
        Validate that a file exists and is readable.
        
        Args:
            file_path: Path to the file to validate
        """
        return file_path.exists() and file_path.is_file()

    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """
        Get metadata about a file.
        
        Args:
            file_path: Path to the file
        """
        stat = file_path.stat()
        return {
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "created": stat.st_ctime,
            "extension": file_path.suffix,
        }

    def process_file(
        self,
        file_path: Path,
        processor: Callable[[List[str]], Any],
    ) -> ProcessingResult:
        """
        Process a single file with error handling.
        
        Args:
            file_path: Path to the file to process
            processor: Function to process the file lines
            
        Returns:
            ProcessingResult with operation details
        """
        result = ProcessingResult(
            file_path=str(file_path),
            status=ProcessingStatus.PROCESSING,
        )
        
        start_time = time.time()
        
        try:
            if not self.validate_file(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                result.lines_processed = len(lines)
                result.metadata = processor(lines)
            
            result.status = ProcessingStatus.COMPLETED
            
        except Exception as e:
            result.status = ProcessingStatus.FAILED
            result.error_message = str(e)
        
        result.processing_time = time.time() - start_time
        return result

    def process_directory(
        self,
        pattern: str = "*",
        processor: Optional[Callable[[List[str]], Any]] = None,
    ) -> List[ProcessingResult]:
        """
        Process all files matching a pattern in the directory.
        
        Args:
            pattern: Glob pattern for file matching
            processor: Optional custom processor function
        """
        if processor is None:
            processor = self._default_processor
        
        files = list(self.base_directory.glob(pattern))
        results = []
        
        for file_path in files:
            if file_path.is_file():
                result = self.process_file(file_path, processor)
                results.append(result)
        
        self.results.extend(results)
        return results

    def _default_processor(self, lines: List[str]) -> Dict[str, Any]:
        """Default processor that counts lines and characters."""
        return {
            "total_lines": len(lines),
            "total_chars": sum(len(line) for line in lines),
            "empty_lines": sum(1 for line in lines if not line.strip()),
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics from all results."""
        if not self.results:
            return {}
        
        total = len(self.results)
        completed = sum(1 for r in self.results if r.status == ProcessingStatus.COMPLETED)
        failed = sum(1 for r in self.results if r.status == ProcessingStatus.FAILED)
        total_lines = sum(r.lines_processed for r in self.results)
        total_time = sum(r.processing_time for r in self.results)
        
        return {
            "total_files": total,
            "completed": completed,
            "failed": failed,
            "success_rate": (completed / total * 100) if total > 0 else 0,
            "total_lines": total_lines,
            "total_time": total_time,
            "avg_time_per_file": total_time / total if total > 0 else 0,
        }

    def write_sample_file(self, filename: str, content: str) -> Path:
        """Write a sample file for testing."""
        file_path = self.base_directory / filename
        file_path.write_text(content, encoding="utf-8")
        return file_path


def main() -> None:
    """Demonstrate FileProcessor functionality."""
    # Create processor instance
    processor = FileProcessor("sample_files")
    
    # Write sample files
    processor.write_sample_file("sample1.txt", "Line 1\nLine 2\nLine 3\n")
    processor.write_sample_file("sample2.txt", "Hello\nWorld\nPython\n")
    processor.write_sample_file("sample3.txt", "Data\nAnalysis\nProcessing\n")
    
    # Process all text files
    print("Processing files...")
    results = processor.process_directory("*.txt")
    
    # Display results
    for result in results:
        print(f"\n{Path(result.file_path).name}:")
        print(f"  Status: {result.status.value}")
        print(f"  Lines: {result.lines_processed}")
        print(f"  Time: {result.processing_time:.3f}s")
        if result.error_message:
            print(f"  Error: {result.error_message}")
    
    # Display statistics
    print("\n=== Statistics ===")
    stats = processor.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
