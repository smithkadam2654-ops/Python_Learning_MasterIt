"""
Pipeline Pattern - Data processing pipeline implementation.
Features: Stage-based processing, data transformation, and pipeline composition.
"""

from typing import Callable, Any, List, Optional, Generic, TypeVar
from dataclasses import dataclass
from enum import Enum
import concurrent.futures
import threading


T = TypeVar('T')
U = TypeVar('U')


class PipelineStatus(Enum):
    """Pipeline execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class PipelineResult:
    """Result of pipeline execution."""
    status: PipelineStatus
    data: Any = None
    error: Optional[Exception] = None
    stage_results: List[Any] = None
    
    def __post_init__(self):
        if self.stage_results is None:
            self.stage_results = []


class PipelineStage:
    """Single stage in a pipeline."""
    
    def __init__(self, name: str, processor: Callable, parallel: bool = False) -> None:
        """
        Initialize pipeline stage.
        
        Args:
            name: Stage name
            processor: Callable that processes data
            parallel: Whether this stage can run in parallel
        """
        self.name = name
        self.processor = processor
        self.parallel = parallel
    
    def execute(self, data: Any) -> Any:
        """
        Execute the stage processor.
        
        Args:
            data: Input data
            
        Returns:
            Processed data
        """
        return self.processor(data)


class Pipeline:
    """Data processing pipeline."""
    
    def __init__(self, name: str = "Pipeline") -> None:
        """
        Initialize pipeline.
        
        Args:
            name: Pipeline name
        """
        self.name = name
        self.stages: List[PipelineStage] = []
        self._status = PipelineStatus.PENDING
        self._lock = threading.Lock()
    
    def add_stage(self, stage: PipelineStage) -> 'Pipeline':
        """
        Add a stage to the pipeline.
        
        Args:
            stage: Stage to add
            
        Returns:
            Self for method chaining
        """
        self.stages.append(stage)
        return self
    
    def add_processor(self, name: str, processor: Callable, parallel: bool = False) -> 'Pipeline':
        """
        Add a processor as a stage.
        
        Args:
            name: Stage name
            processor: Callable processor
            parallel: Whether stage can run in parallel
            
        Returns:
            Self for method chaining
        """
        self.add_stage(PipelineStage(name, processor, parallel))
        return self
    
    def execute(self, data: Any) -> PipelineResult:
        """
        Execute the pipeline.
        
        Args:
            data: Input data
            
        Returns:
            PipelineResult with execution results
        """
        with self._lock:
            self._status = PipelineStatus.RUNNING
            result = PipelineResult(status=PipelineStatus.RUNNING, data=data)
            
            current_data = data
            result.stage_results = [data]
            
            try:
                for stage in self.stages:
                    current_data = stage.execute(current_data)
                    result.stage_results.append(current_data)
                
                result.data = current_data
                result.status = PipelineStatus.COMPLETED
                self._status = PipelineStatus.COMPLETED
                
            except Exception as e:
                result.error = e
                result.status = PipelineStatus.FAILED
                self._status = PipelineStatus.FAILED
            
            return result
    
    def execute_parallel(self, data: Any) -> PipelineResult:
        """
        Execute pipeline with parallel stages where possible.
        
        Args:
            data: Input data
            
        Returns:
            PipelineResult with execution results
        """
        with self._lock:
            self._status = PipelineStatus.RUNNING
            result = PipelineResult(status=PipelineStatus.RUNNING, data=data)
            result.stage_results = [data]
            
            current_data = data
            
            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = []
                    
                    for stage in self.stages:
                        if stage.parallel:
                            future = executor.submit(stage.execute, current_data)
                            futures.append(future)
                        else:
                            current_data = stage.execute(current_data)
                            result.stage_results.append(current_data)
                    
                    # Wait for parallel stages
                    for future in concurrent.futures.as_completed(futures):
                        current_data = future.result()
                        result.stage_results.append(current_data)
                
                result.data = current_data
                result.status = PipelineStatus.COMPLETED
                self._status = PipelineStatus.COMPLETED
                
            except Exception as e:
                result.error = e
                result.status = PipelineStatus.FAILED
                self._status = PipelineStatus.FAILED
            
            return result
    
    def get_status(self) -> PipelineStatus:
        """Get current pipeline status."""
        return self._status
    
    def clear(self) -> None:
        """Clear all stages from pipeline."""
        with self._lock:
            self.stages.clear()
            self._status = PipelineStatus.PENDING


class PipelineBuilder:
    """Builder for creating pipelines."""
    
    def __init__(self, name: str = "Pipeline") -> None:
        """
        Initialize pipeline builder.
        
        Args:
            name: Pipeline name
        """
        self.pipeline = Pipeline(name)
    
    def stage(self, name: str, processor: Callable, parallel: bool = False) -> 'PipelineBuilder':
        """
        Add a stage to the pipeline.
        
        Args:
            name: Stage name
            processor: Callable processor
            parallel: Whether stage can run in parallel
            
        Returns:
            Self for method chaining
        """
        self.pipeline.add_processor(name, processor, parallel)
        return self
    
    def build(self) -> Pipeline:
        """
        Build and return the pipeline.
        
        Returns:
            Configured Pipeline instance
        """
        return self.pipeline


class DataProcessor:
    """Common data processing functions."""
    
    @staticmethod
    def to_uppercase(text: str) -> str:
        """Convert text to uppercase."""
        return text.upper()
    
    @staticmethod
    def to_lowercase(text: str) -> str:
        """Convert text to lowercase."""
        return text.lower()
    
    @staticmethod
    def trim(text: str) -> str:
        """Trim whitespace from text."""
        return text.strip()
    
    @staticmethod
    def remove_duplicates(items: List) -> List:
        """Remove duplicates from list."""
        return list(dict.fromkeys(items))
    
    @staticmethod
    def filter_positive(numbers: List[int]) -> List[int]:
        """Filter positive numbers."""
        return [n for n in numbers if n > 0]
    
    @staticmethod
    def square(numbers: List[int]) -> List[int]:
        """Square all numbers."""
        return [n ** 2 for n in numbers]
    
    @staticmethod
    def sum(numbers: List[int]) -> int:
        """Sum all numbers."""
        return sum(numbers)
    
    @staticmethod
    def multiply_by_2(numbers: List[int]) -> List[int]:
        """Multiply all numbers by 2."""
        return [n * 2 for n in numbers]
    
    @staticmethod
    def reverse_list(items: List) -> List:
        """Reverse list."""
        return items[::-1]
    
    @staticmethod
    def sort_list(items: List) -> List:
        """Sort list."""
        return sorted(items)


class TextProcessingPipeline:
    """Specialized pipeline for text processing."""
    
    @staticmethod
    def create_cleaning_pipeline() -> Pipeline:
        """Create a text cleaning pipeline."""
        return (PipelineBuilder("Text Cleaning")
                .stage("trim", DataProcessor.trim)
                .stage("lowercase", DataProcessor.to_lowercase)
                .stage("remove_extra_spaces", lambda x: ' '.join(x.split()))
                .build())
    
    @staticmethod
    def create_analysis_pipeline() -> Pipeline:
        """Create a text analysis pipeline."""
        def word_count(text: str) -> int:
            return len(text.split())
        
        def char_count(text: str) -> int:
            return len(text)
        
        def avg_word_length(text: str) -> float:
            words = text.split()
            return sum(len(w) for w in words) / len(words) if words else 0
        
        return (PipelineBuilder("Text Analysis")
                .stage("word_count", word_count)
                .stage("char_count", char_count)
                .stage("avg_word_length", avg_word_length)
                .build())


class NumberProcessingPipeline:
    """Specialized pipeline for number processing."""
    
    @staticmethod
    def create_filter_pipeline() -> Pipeline:
        """Create a number filtering pipeline."""
        return (PipelineBuilder("Number Filter")
                .stage("filter_positive", DataProcessor.filter_positive)
                .stage("remove_duplicates", DataProcessor.remove_duplicates)
                .stage("sort", DataProcessor.sort_list)
                .build())
    
    @staticmethod
    def create_transform_pipeline() -> Pipeline:
        """Create a number transformation pipeline."""
        return (PipelineBuilder("Number Transform")
                .stage("multiply_by_2", DataProcessor.multiply_by_2)
                .stage("square", DataProcessor.square)
                .stage("sum", DataProcessor.sum)
                .build())


class ParallelProcessingPipeline:
    """Pipeline with parallel processing capabilities."""
    
    @staticmethod
    def create_parallel_pipeline() -> Pipeline:
        """Create a pipeline with parallel stages."""
        def slow_operation_1(x: int) -> int:
            import time
            time.sleep(0.1)
            return x * 2
        
        def slow_operation_2(x: int) -> int:
            import time
            time.sleep(0.1)
            return x + 10
        
        def slow_operation_3(x: int) -> int:
            import time
            time.sleep(0.1)
            return x ** 2
        
        return (PipelineBuilder("Parallel Processing")
                .stage("op1", slow_operation_1, parallel=True)
                .stage("op2", slow_operation_2, parallel=True)
                .stage("op3", slow_operation_3, parallel=True)
                .stage("sum", lambda x: sum(x) if isinstance(x, list) else x)
                .build())


def main() -> None:
    """Demonstrate pipeline pattern implementations."""
    
    print("=== Basic Pipeline ===")
    pipeline = (PipelineBuilder("Number Pipeline")
                .stage("multiply_by_2", DataProcessor.multiply_by_2)
                .stage("square", DataProcessor.square)
                .stage("sum", DataProcessor.sum)
                .build())
    
    numbers = [1, 2, 3, 4, 5]
    result = pipeline.execute(numbers)
    
    print(f"Input: {numbers}")
    print(f"Stage results: {result.stage_results}")
    print(f"Final result: {result.data}")
    print(f"Status: {result.status}")
    
    print("\n=== Text Cleaning Pipeline ===")
    text_pipeline = TextProcessingPipeline.create_cleaning_pipeline()
    
    text = "  Hello   World!  This is a TEST.  "
    result = text_pipeline.execute(text)
    
    print(f"Original: '{text}'")
    print(f"Cleaned: '{result.data}'")
    print(f"Stage results: {result.stage_results}")
    
    print("\n=== Text Analysis Pipeline ===")
    analysis_pipeline = TextProcessingPipeline.create_analysis_pipeline()
    
    text = "The quick brown fox jumps over the lazy dog"
    result = analysis_pipeline.execute(text)
    
    print(f"Text: '{text}'")
    print(f"Word count: {result.stage_results[0]}")
    print(f"Character count: {result.stage_results[1]}")
    print(f"Average word length: {result.stage_results[2]:.2f}")
    
    print("\n=== Number Filter Pipeline ===")
    filter_pipeline = NumberProcessingPipeline.create_filter_pipeline()
    
    numbers = [3, -1, 5, -2, 5, 3, 7, -3]
    result = filter_pipeline.execute(numbers)
    
    print(f"Input: {numbers}")
    print(f"Filtered: {result.data}")
    
    print("\n=== Number Transform Pipeline ===")
    transform_pipeline = NumberProcessingPipeline.create_transform_pipeline()
    
    numbers = [1, 2, 3]
    result = transform_pipeline.execute(numbers)
    
    print(f"Input: {numbers}")
    print(f"Transformed: {result.data}")
    
    print("\n=== Parallel Pipeline ===")
    parallel_pipeline = ParallelProcessingPipeline.create_parallel_pipeline()
    
    import time
    start = time.time()
    result = parallel_pipeline.execute_parallel(5)
    end = time.time()
    
    print(f"Input: 5")
    print(f"Result: {result.data}")
    print(f"Execution time: {end - start:.2f}s")
    
    # Compare with sequential
    start = time.time()
    result = parallel_pipeline.execute(5)
    end = time.time()
    
    print(f"Sequential execution time: {end - start:.2f}s")
    
    print("\n=== Pipeline with Error Handling ===")
    def failing_stage(x):
        raise ValueError("Intentional error")
    
    error_pipeline = (PipelineBuilder("Error Pipeline")
                     .stage("stage1", lambda x: x * 2)
                     .stage("stage2", failing_stage)
                     .stage("stage3", lambda x: x + 1)
                     .build())
    
    result = error_pipeline.execute(5)
    print(f"Status: {result.status}")
    print(f"Error: {result.error}")
    print(f"Stage results before error: {result.stage_results}")


if __name__ == "__main__":
    main()
