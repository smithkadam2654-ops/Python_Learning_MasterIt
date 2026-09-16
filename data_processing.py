"""
Data Processing Module

This module provides comprehensive data processing and analysis utilities including:
- Data cleaning and preprocessing
- Statistical analysis
- Data transformation
- CSV/JSON data handling
- Data aggregation and grouping
- Filtering and sorting
- Data validation
- Text processing utilities
- Data visualization helpers
- Machine learning preprocessing

All functions include comprehensive docstrings and type hints.
"""

import csv
import json
import re
import statistics
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from collections import Counter, defaultdict
from datetime import datetime
import math


@dataclass
class DataPoint:
    """Represents a single data point with metadata."""
    value: Any
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StatisticsResult:
    """Container for statistical analysis results."""
    mean: float
    median: float
    mode: Any
    std_dev: float
    variance: float
    min: float
    max: float
    range: float
    sum: float
    count: int


class DataCleaner:
    """Data cleaning and preprocessing utilities."""
    
    @staticmethod
    def remove_nulls(data: List[Any]) -> List[Any]:
        """Remove null/None values from a list."""
        return [item for item in data if item is not None]
    
    @staticmethod
    def remove_duplicates(data: List[Any]) -> List[Any]:
        """Remove duplicate values while preserving order."""
        seen = set()
        result = []
        for item in data:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    @staticmethod
    def fill_nulls(data: List[Optional[Any]], fill_value: Any = 0) -> List[Any]:
        """Replace null values with a specified value."""
        return [fill_value if item is None else item for item in data]
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace in text."""
        return " ".join(text.split())
    
    @staticmethod
    def clean_string(text: str) -> str:
        """Clean string by removing special characters and extra spaces."""
        text = re.sub(r'[^\w\s]', '', text)
        return DataCleaner.normalize_whitespace(text)
    
    @staticmethod
    def standardize_case(text: str, case: str = "lower") -> str:
        """Standardize text case."""
        if case == "lower":
            return text.lower()
        elif case == "upper":
            return text.upper()
        elif case == "title":
            return text.title()
        return text
    
    @staticmethod
    def remove_outliers(data: List[float], method: str = "iqr", multiplier: float = 1.5) -> List[float]:
        """Remove outliers using specified method."""
        if not data:
            return data
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        if method == "iqr":
            q1 = sorted_data[n // 4]
            q3 = sorted_data[3 * n // 4]
            iqr = q3 - q1
            lower_bound = q1 - multiplier * iqr
            upper_bound = q3 + multiplier * iqr
            return [x for x in data if lower_bound <= x <= upper_bound]
        
        elif method == "zscore":
            mean = statistics.mean(data)
            std_dev = statistics.stdev(data) if len(data) > 1 else 0
            threshold = multiplier
            return [x for x in data if abs((x - mean) / std_dev) <= threshold] if std_dev > 0 else data
        
        return data
    
    @staticmethod
    def round_values(data: List[float], decimals: int = 2) -> List[float]:
        """Round all values to specified decimal places."""
        return [round(x, decimals) for x in data]


class DataTransformer:
    """Data transformation utilities."""
    
    @staticmethod
    def normalize_min_max(data: List[float]) -> List[float]:
        """Normalize data to 0-1 range using min-max normalization."""
        if not data:
            return data
        
        min_val = min(data)
        max_val = max(data)
        
        if max_val == min_val:
            return [0.0] * len(data)
        
        return [(x - min_val) / (max_val - min_val) for x in data]
    
    @staticmethod
    def normalize_z_score(data: List[float]) -> List[float]:
        """Normalize data using z-score standardization."""
        if len(data) < 2:
            return [0.0] * len(data)
        
        mean = statistics.mean(data)
        std_dev = statistics.stdev(data)
        
        if std_dev == 0:
            return [0.0] * len(data)
        
        return [(x - mean) / std_dev for x in data]
    
    @staticmethod
    def log_transform(data: List[float]) -> List[float]:
        """Apply logarithmic transformation."""
        return [math.log(x) if x > 0 else 0 for x in data]
    
    @staticmethod
    def encode_categorical(data: List[str]) -> Dict[str, List[int]]:
        """One-hot encode categorical data."""
        unique_values = list(set(data))
        encoding = {}
        
        for value in unique_values:
            encoding[value] = [1 if item == value else 0 for item in data]
        
        return encoding
    
    @staticmethod
    def label_encode(data: List[Any]) -> List[int]:
        """Label encode categorical data."""
        unique_values = list(set(data))
        mapping = {value: idx for idx, value in enumerate(unique_values)}
        return [mapping[item] for item in data]
    
    @staticmethod
    def bin_data(data: List[float], num_bins: int = 5) -> List[int]:
        """Bin continuous data into discrete intervals."""
        if not data:
            return []
        
        min_val = min(data)
        max_val = max(data)
        
        if max_val == min_val:
            return [0] * len(data)
        
        bin_width = (max_val - min_val) / num_bins
        return [int((x - min_val) / bin_width) for x in data]
    
    @staticmethod
    def apply_function(data: List[Any], func: Callable) -> List[Any]:
        """Apply a function to all elements in the data."""
        return [func(item) for item in data]


class StatisticalAnalyzer:
    """Statistical analysis utilities."""
    
    @staticmethod
    def calculate_statistics(data: List[float]) -> StatisticsResult:
        """Calculate comprehensive statistics for numeric data."""
        if not data:
            raise ValueError("Data cannot be empty")
        
        sorted_data = sorted(data)
        n = len(data)
        
        mean = statistics.mean(data)
        median = statistics.median(data)
        
        try:
            mode = statistics.mode(data)
        except statistics.StatisticsError:
            mode = None
        
        variance = statistics.variance(data) if n > 1 else 0
        std_dev = statistics.stdev(data) if n > 1 else 0
        
        return StatisticsResult(
            mean=mean,
            median=median,
            mode=mode,
            std_dev=std_dev,
            variance=variance,
            min=min(data),
            max=max(data),
            range=max(data) - min(data),
            sum=sum(data),
            count=n
        )
    
    @staticmethod
    def correlation(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient between two datasets."""
        if len(x) != len(y) or len(x) < 2:
            raise ValueError("Datasets must have same length and at least 2 elements")
        
        n = len(x)
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        
        return numerator / denominator if denominator != 0 else 0
    
    @staticmethod
    def percentile(data: List[float], percentile: float) -> float:
        """Calculate the value at a given percentile."""
        if not data:
            raise ValueError("Data cannot be empty")
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        index = (percentile / 100) * (n - 1)
        
        lower = int(index)
        upper = lower + 1
        
        if upper >= n:
            return sorted_data[-1]
        
        weight = index - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight
    
    @staticmethod
    def moving_average(data: List[float], window: int) -> List[float]:
        """Calculate moving average with specified window size."""
        if window <= 0 or window > len(data):
            raise ValueError("Window size must be positive and not exceed data length")
        
        return [statistics.mean(data[i:i+window]) for i in range(len(data) - window + 1)]
    
    @staticmethod
    def cumulative_sum(data: List[float]) -> List[float]:
        """Calculate cumulative sum."""
        result = []
        total = 0
        for value in data:
            total += value
            result.append(total)
        return result
    
    @staticmethod
    def frequency_distribution(data: List[Any]) -> Dict[Any, int]:
        """Calculate frequency distribution of values."""
        return dict(Counter(data))


class DataAggregator:
    """Data aggregation and grouping utilities."""
    
    @staticmethod
    def group_by(data: List[Dict], key: str) -> Dict[Any, List[Dict]]:
        """Group list of dictionaries by a key."""
        groups = defaultdict(list)
        for item in data:
            groups[item.get(key)].append(item)
        return dict(groups)
    
    @staticmethod
    def aggregate_groups(groups: Dict[Any, List[Dict]], 
                        aggregations: Dict[str, Callable]) -> Dict[Any, Dict]:
        """Apply aggregation functions to grouped data."""
        results = {}
        for key, items in groups.items():
            result = {}
            for field, func in aggregations.items():
                values = [item.get(field) for item in items if item.get(field) is not None]
                if values:
                    result[field] = func(values)
            results[key] = result
        return results
    
    @staticmethod
    def pivot_table(data: List[Dict], index: str, columns: str, 
                    values: str, aggfunc: Callable = sum) -> Dict[Any, Dict[Any, Any]]:
        """Create a pivot table from list of dictionaries."""
        result = defaultdict(lambda: defaultdict(list))
        
        for item in data:
            idx = item.get(index)
            col = item.get(columns)
            val = item.get(values)
            
            if idx is not None and col is not None and val is not None:
                result[idx][col].append(val)
        
        # Apply aggregation function
        pivot = {}
        for idx, cols in result.items():
            pivot[idx] = {col: aggfunc(vals) for col, vals in cols.items()}
        
        return pivot
    
    @staticmethod
    def sum_by_group(data: List[Dict], group_key: str, sum_key: str) -> Dict[Any, float]:
        """Sum values by group."""
        groups = DataAggregator.group_by(data, group_key)
        return {key: sum(item.get(sum_key, 0) for item in items) 
                for key, items in groups.items()}
    
    @staticmethod
    def count_by_group(data: List[Dict], group_key: str) -> Dict[Any, int]:
        """Count items by group."""
        groups = DataAggregator.group_by(data, group_key)
        return {key: len(items) for key, items in groups.items()}


class DataFilter:
    """Data filtering and sorting utilities."""
    
    @staticmethod
    def filter_by_condition(data: List[Dict], condition: Callable[[Dict], bool]) -> List[Dict]:
        """Filter data based on a condition function."""
        return [item for item in data if condition(item)]
    
    @staticmethod
    def filter_by_value(data: List[Dict], key: str, value: Any) -> List[Dict]:
        """Filter data where key equals value."""
        return [item for item in data if item.get(key) == value]
    
    @staticmethod
    def filter_by_range(data: List[Dict], key: str, min_val: Any, max_val: Any) -> List[Dict]:
        """Filter data where key is within range."""
        return [item for item in data if min_val <= item.get(key) <= max_val]
    
    @staticmethod
    def filter_by_pattern(data: List[Dict], key: str, pattern: str) -> List[Dict]:
        """Filter data where key matches regex pattern."""
        regex = re.compile(pattern)
        return [item for item in data if regex.search(str(item.get(key, "")))]
    
    @staticmethod
    def sort_by_key(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
        """Sort data by key."""
        return sorted(data, key=lambda x: x.get(key, ""), reverse=reverse)
    
    @staticmethod
    def sort_by_multiple_keys(data: List[Dict], keys: List[Tuple[str, bool]]) -> List[Dict]:
        """Sort data by multiple keys with direction."""
        return sorted(data, key=lambda x: tuple(x.get(k) for k, _ in keys), 
                     reverse=keys[0][1] if keys else False)
    
    @staticmethod
    def get_top_n(data: List[Dict], key: str, n: int) -> List[Dict]:
        """Get top N items by key value."""
        return sorted(data, key=lambda x: x.get(key, 0), reverse=True)[:n]
    
    @staticmethod
    def get_bottom_n(data: List[Dict], key: str, n: int) -> List[Dict]:
        """Get bottom N items by key value."""
        return sorted(data, key=lambda x: x.get(key, 0))[:n]


class CSVProcessor:
    """CSV file processing utilities."""
    
    @staticmethod
    def read_csv(file_path: str, delimiter: str = ",") -> List[Dict]:
        """Read CSV file and return list of dictionaries."""
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            return list(reader)
    
    @staticmethod
    def write_csv(data: List[Dict], file_path: str, delimiter: str = ",") -> None:
        """Write list of dictionaries to CSV file."""
        if not data:
            return
        
        fieldnames = data[0].keys()
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)
    
    @staticmethod
    def filter_csv(input_path: str, output_path: str, 
                   condition: Callable[[Dict], bool]) -> int:
        """Filter CSV file based on condition and write to output."""
        data = CSVProcessor.read_csv(input_path)
        filtered = [item for item in data if condition(item)]
        CSVProcessor.write_csv(filtered, output_path)
        return len(filtered)
    
    @staticmethod
    def merge_csv_files(file_paths: List[str], output_path: str) -> int:
        """Merge multiple CSV files into one."""
        merged_data = []
        for file_path in file_paths:
            merged_data.extend(CSVProcessor.read_csv(file_path))
        CSVProcessor.write_csv(merged_data, output_path)
        return len(merged_data)


class JSONProcessor:
    """JSON data processing utilities."""
    
    @staticmethod
    def read_json(file_path: str) -> Any:
        """Read JSON file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    @staticmethod
    def write_json(data: Any, file_path: str, indent: int = 2) -> None:
        """Write data to JSON file."""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=indent, default=str)
    
    @staticmethod
    def flatten_json(data: Dict, parent_key: str = "", sep: str = ".") -> Dict:
        """Flatten nested JSON structure."""
        items = []
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(JSONProcessor.flatten_json(value, new_key, sep).items())
            else:
                items.append((new_key, value))
        return dict(items)
    
    @staticmethod
    def extract_field(data: List[Dict], field: str) -> List[Any]:
        """Extract a specific field from list of dictionaries."""
        return [item.get(field) for item in data]
    
    @staticmethod
    def filter_json(data: List[Dict], field: str, value: Any) -> List[Dict]:
        """Filter JSON data by field value."""
        return [item for item in data if item.get(field) == value]


class TextProcessor:
    """Text processing utilities."""
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Tokenize text into words."""
        return re.findall(r'\b\w+\b', text.lower())
    
    @staticmethod
    def word_count(text: str) -> int:
        """Count words in text."""
        return len(TextProcessor.tokenize(text))
    
    @staticmethod
    def character_count(text: str, include_spaces: bool = True) -> int:
        """Count characters in text."""
        return len(text) if include_spaces else len(text.replace(" ", ""))
    
    @staticmethod
    def sentence_count(text: str) -> int:
        """Count sentences in text."""
        sentences = re.split(r'[.!?]+', text)
        return len([s for s in sentences if s.strip()])
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """Extract email addresses from text."""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract URLs from text."""
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """Extract phone numbers from text."""
        pattern = r'\+?[\d\s-()]{10,}'
        return re.findall(pattern, text)
    
    @staticmethod
    def ngrams(text: str, n: int) -> List[str]:
        """Generate n-grams from text."""
        tokens = TextProcessor.tokenize(text)
        return [' '.join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


class DataValidator:
    """Data validation utilities."""
    
    @staticmethod
    def validate_data_types(data: Dict[str, Any], schema: Dict[str, type]) -> bool:
        """Validate data against type schema."""
        for field, expected_type in schema.items():
            if field not in data or not isinstance(data[field], expected_type):
                return False
        return True
    
    @staticmethod
    def validate_range(value: float, min_val: float, max_val: float) -> bool:
        """Validate value is within range."""
        return min_val <= value <= max_val
    
    @staticmethod
    def validate_length(value: Any, min_len: int, max_len: int) -> bool:
        """Validate value length is within range."""
        return min_len <= len(value) <= max_len
    
    @staticmethod
    def validate_pattern(value: str, pattern: str) -> bool:
        """Validate value matches regex pattern."""
        return bool(re.match(pattern, value))
    
    @staticmethod
    def check_missing_values(data: List[Dict]) -> Dict[str, int]:
        """Check for missing values in dataset."""
        missing = defaultdict(int)
        for item in data:
            for key, value in item.items():
                if value is None or value == "":
                    missing[key] += 1
        return dict(missing)


def demonstrate_data_processing():
    """Demonstrate data processing functionality."""
    print("=== Data Processing Demonstration ===\n")
    
    # Sample data
    sample_data = [
        {"name": "John", "age": 30, "salary": 50000, "department": "Engineering"},
        {"name": "Jane", "age": 25, "salary": 45000, "department": "Marketing"},
        {"name": "Bob", "age": 35, "salary": 60000, "department": "Engineering"},
        {"name": "Alice", "age": 28, "salary": 55000, "department": "Sales"},
        {"name": "Charlie", "age": 32, "salary": 58000, "department": "Engineering"}
    ]
    
    # Data Cleaning
    print("1. Data Cleaning:")
    dirty_data = [1, 2, None, 4, 2, 5, None, 6]
    print(f"   Original: {dirty_data}")
    print(f"   Remove nulls: {DataCleaner.remove_nulls(dirty_data)}")
    print(f"   Remove duplicates: {DataCleaner.remove_duplicates([1, 2, 2, 3, 3, 3])}")
    print(f"   Clean string: '{DataCleaner.clean_string('  Hello, World!  ')}'")
    
    # Data Transformation
    print("\n2. Data Transformation:")
    numeric_data = [10, 20, 30, 40, 50]
    print(f"   Original: {numeric_data}")
    print(f"   Min-max normalized: {DataTransformer.normalize_min_max(numeric_data)}")
    print(f"   Z-score normalized: {DataTransformer.normalize_z_score(numeric_data)}")
    print(f"   Log transformed: {DataTransformer.log_transform([1, 10, 100, 1000])}")
    
    # Statistical Analysis
    print("\n3. Statistical Analysis:")
    stats = StatisticalAnalyzer.calculate_statistics([10, 20, 30, 40, 50])
    print(f"   Mean: {stats.mean}")
    print(f"   Median: {stats.median}")
    print(f"   Std Dev: {stats.std_dev:.2f}")
    print(f"   75th percentile: {StatisticalAnalyzer.percentile([10, 20, 30, 40, 50], 75)}")
    
    # Data Aggregation
    print("\n4. Data Aggregation:")
    groups = DataAggregator.group_by(sample_data, "department")
    print(f"   Groups by department: {list(groups.keys())}")
    sums = DataAggregator.sum_by_group(sample_data, "department", "salary")
    print(f"   Salary sums by department: {sums}")
    counts = DataAggregator.count_by_group(sample_data, "department")
    print(f"   Employee counts by department: {counts}")
    
    # Data Filtering
    print("\n5. Data Filtering:")
    filtered = DataFilter.filter_by_range(sample_data, "age", 28, 35)
    print(f"   Employees aged 28-35: {[d['name'] for d in filtered]}")
    sorted_data = DataFilter.sort_by_key(sample_data, "salary", reverse=True)
    print(f"   Top salary: {sorted_data[0]['name']} (${sorted_data[0]['salary']})")
    
    # Text Processing
    print("\n6. Text Processing:")
    text = "Hello world! This is a test. Contact us at test@example.com or visit https://example.com"
    print(f"   Word count: {TextProcessor.word_count(text)}")
    print(f"   Sentence count: {TextProcessor.sentence_count(text)}")
    print(f"   Emails found: {TextProcessor.extract_emails(text)}")
    print(f"   URLs found: {TextProcessor.extract_urls(text)}")
    
    # Data Validation
    print("\n7. Data Validation:")
    schema = {"name": str, "age": int, "salary": (int, float)}
    valid_data = {"name": "John", "age": 30, "salary": 50000}
    print(f"   Valid data check: {DataValidator.validate_data_types(valid_data, schema)}")
    print(f"   Range check (25, 30): {DataValidator.validate_range(30, 25, 35)}")
    
    # Frequency Distribution
    print("\n8. Frequency Distribution:")
    categories = ["A", "B", "A", "C", "B", "A", "A", "B"]
    freq = StatisticalAnalyzer.frequency_distribution(categories)
    print(f"   Category frequencies: {freq}")
    
    # Moving Average
    print("\n9. Moving Average:")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ma = StatisticalAnalyzer.moving_average(data, 3)
    print(f"   3-period moving average: {ma}")
    
    # Cumulative Sum
    print("\n10. Cumulative Sum:")
    cumsum = StatisticalAnalyzer.cumulative_sum([1, 2, 3, 4, 5])
    print(f"   Cumulative sum: {cumsum}")
    
    print("\n=== Demonstration Complete ===")


if __name__ == "__main__":
    demonstrate_data_processing()