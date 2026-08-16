"""
Data Analyzer - A statistical analysis tool for numerical data.
Features: Mean, median, mode, standard deviation, and data visualization.
"""

from typing import List, Tuple, Dict, Optional
from collections import Counter
import math
from statistics import median as stat_median


class DataAnalyzer:
    """Perform statistical analysis on numerical datasets."""

    def __init__(self, data: List[float]) -> None:
        """
        Initialize analyzer with numerical data.
        
        Args:
            data: List of numerical values for analysis
        """
        if not data:
            raise ValueError("Data cannot be empty")
        self.data = data
        self.sorted_data = sorted(data)

    def mean(self) -> float:
        """Calculate arithmetic mean of the data."""
        return sum(self.data) / len(self.data)

    def median(self) -> float:
        """Calculate median value of the data."""
        return stat_median(self.data)

    def mode(self) -> Optional[float]:
        """
        Find the most frequent value(s).
        Returns None if no value repeats.
        """
        counts = Counter(self.data)
        max_count = max(counts.values())
        
        if max_count == 1:
            return None
        
        modes = [value for value, count in counts.items() if count == max_count]
        return modes[0] if len(modes) == 1 else None

    def standard_deviation(self) -> float:
        """Calculate population standard deviation."""
        mean_val = self.mean()
        variance = sum((x - mean_val) ** 2 for x in self.data) / len(self.data)
        return math.sqrt(variance)

    def variance(self) -> float:
        """Calculate population variance."""
        return self.standard_deviation() ** 2

    def percentile(self, percentile: float) -> float:
        """
        Calculate the value at a given percentile.
        
        Args:
            percentile: Percentile value between 0 and 100
        """
        if not 0 <= percentile <= 100:
            raise ValueError("Percentile must be between 0 and 100")
        
        index = (percentile / 100) * (len(self.sorted_data) - 1)
        lower_index = int(index)
        upper_index = min(lower_index + 1, len(self.sorted_data) - 1)
        
        if lower_index == upper_index:
            return self.sorted_data[lower_index]
        
        # Linear interpolation
        weight = index - lower_index
        return (self.sorted_data[lower_index] * (1 - weight) + 
                self.sorted_data[upper_index] * weight)

    def quartiles(self) -> Tuple[float, float, float]:
        """Calculate Q1 (25%), Q2 (50%), and Q3 (75%) quartiles."""
        return (self.percentile(25), self.percentile(50), self.percentile(75))

    def outliers(self, multiplier: float = 1.5) -> List[float]:
        """
        Identify outliers using IQR method.
        
        Args:
            multiplier: IQR multiplier for outlier threshold (default: 1.5)
        """
        q1, q2, q3 = self.quartiles()
        iqr = q3 - q1
        lower_bound = q1 - (multiplier * iqr)
        upper_bound = q3 + (multiplier * iqr)
        
        return [x for x in self.data if x < lower_bound or x > upper_bound]

    def summary(self) -> Dict[str, float]:
        """Generate a comprehensive statistical summary."""
        return {
            "count": len(self.data),
            "mean": self.mean(),
            "median": self.median(),
            "std_dev": self.standard_deviation(),
            "variance": self.variance(),
            "min": min(self.data),
            "max": max(self.data),
            "q1": self.quartiles()[0],
            "q3": self.quartiles()[2],
        }

    def __str__(self) -> str:
        """String representation of the analysis summary."""
        summary = self.summary()
        lines = [
            "=== Statistical Summary ===",
            f"Count: {summary['count']}",
            f"Mean: {summary['mean']:.2f}",
            f"Median: {summary['median']:.2f}",
            f"Std Dev: {summary['std_dev']:.2f}",
            f"Min: {summary['min']:.2f}",
            f"Max: {summary['max']:.2f}",
            f"Q1: {summary['q1']:.2f}",
            f"Q3: {summary['q3']:.2f}",
        ]
        return "\n".join(lines)


def main() -> None:
    """Demonstrate DataAnalyzer functionality."""
    # Sample dataset
    data = [23, 45, 67, 89, 12, 34, 56, 78, 90, 100, 45, 67, 23, 200]
    
    analyzer = DataAnalyzer(data)
    
    print(analyzer)
    print(f"\nMode: {analyzer.mode()}")
    print(f"Outliers: {analyzer.outliers()}")
    print(f"90th Percentile: {analyzer.percentile(90):.2f}")


if __name__ == "__main__":
    main()
