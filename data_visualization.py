"""
Data Visualization Module

This module provides comprehensive data visualization utilities including:
- ASCII chart generation
- Terminal-based plotting
- Data format conversion for visualization
- Color schemes and palettes
- Chart configuration
- Data aggregation for plotting
- Simple graph representations
- Statistical visualization helpers
- Export utilities
- Interactive terminal displays

All functions include comprehensive docstrings and type hints.
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import json


class ChartType(Enum):
    """Chart types."""
    BAR = "bar"
    LINE = "line"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    PIE = "pie"
    AREA = "area"


class ColorScheme(Enum):
    """Color schemes for charts."""
    DEFAULT = "default"
    MONOCHROME = "monochrome"
    RAINBOW = "rainbow"
    HEATMAP = "heatmap"
    SEQUENTIAL = "sequential"


@dataclass
class ChartConfig:
    """Chart configuration."""
    width: int = 80
    height: int = 20
    title: str = ""
    x_label: str = ""
    y_label: str = ""
    show_grid: bool = True
    show_legend: bool = True
    color_scheme: ColorScheme = ColorScheme.DEFAULT
    padding: int = 2


class ASCIIChart:
    """ASCII chart generation for terminal display."""
    
    def __init__(self, config: Optional[ChartConfig] = None):
        """Initialize ASCII chart with configuration."""
        self.config = config or ChartConfig()
        self.colors = self._get_color_scheme()
    
    def _get_color_scheme(self) -> List[str]:
        """Get color scheme based on configuration."""
        schemes = {
            ColorScheme.DEFAULT: ["█", "▓", "▒", "░", " "],
            ColorScheme.MONOCHROME: ["█", "▓", "▒", "░", " "],
            ColorScheme.RAINBOW: ["█", "▓", "▒", "░", " "],
            ColorScheme.HEATMAP: ["█", "▓", "▒", "░", " "],
            ColorScheme.SEQUENTIAL: ["█", "▓", "▒", "░", " "]
        }
        return schemes.get(self.config.color_scheme, schemes[ColorScheme.DEFAULT])
    
    def bar_chart(self, data: Dict[str, float], 
                 max_value: Optional[float] = None) -> str:
        """Generate ASCII bar chart."""
        if not data:
            return "No data to display"
        
        labels = list(data.keys())
        values = list(data.values())
        
        if max_value is None:
            max_value = max(values) if values else 1
        
        # Calculate dimensions
        chart_width = self.config.width - self.config.padding * 2
        chart_height = self.config.height - self.config.padding * 2
        
        # Build chart
        lines = []
        
        # Add title
        if self.config.title:
            lines.append(self.config.title.center(self.config.width))
            lines.append("")
        
        # Calculate bar heights
        bar_heights = []
        max_label_length = max(len(str(label)) for label in labels) if labels else 0
        
        for value in values:
            if max_value > 0:
                height = int((value / max_value) * chart_height)
            else:
                height = 0
            bar_heights.append(max(1, height))
        
        # Draw bars from top to bottom
        for row in range(chart_height, 0, -1):
            line = " " * max_label_length + " │"
            
            for bar_height in bar_heights:
                if row <= bar_height:
                    line += "█"
                else:
                    line += " "
                line += " "
            
            lines.append(line)
        
        # Add x-axis
        x_axis = " " * max_label_length + " └"
        for _ in bar_heights:
            x_axis += "─"
        lines.append(x_axis)
        
        # Add labels
        label_line = " " * max_label_length + "  "
        for label in labels:
            label_str = str(label)[:3]  # Truncate to 3 chars
            label_line += label_str + " "
        lines.append(label_line)
        
        # Add axis labels
        if self.config.y_label:
            lines.insert(1, self.config.y_label.rjust(max_label_length + 1))
        
        if self.config.x_label:
            lines.append(self.config.x_label.center(self.config.width))
        
        return "\n".join(lines)
    
    def line_chart(self, data: List[Tuple[float, float]],
                 x_range: Optional[Tuple[float, float]] = None,
                 y_range: Optional[Tuple[float, float]] = None) -> str:
        """Generate ASCII line chart."""
        if not data:
            return "No data to display"
        
        # Sort data by x value
        sorted_data = sorted(data, key=lambda x: x[0])
        x_values = [point[0] for point in sorted_data]
        y_values = [point[1] for point in sorted_data]
        
        # Determine ranges
        if x_range is None:
            x_min, x_max = min(x_values), max(x_values)
        else:
            x_min, x_max = x_range
        
        if y_range is None:
            y_min, y_max = min(y_values), max(y_values)
        else:
            y_min, y_max = y_range
        
        # Calculate dimensions
        chart_width = self.config.width - self.config.padding * 2
        chart_height = self.config.height - self.config.padding * 2
        
        # Build chart
        lines = []
        
        # Add title
        if self.config.title:
            lines.append(self.config.title.center(self.config.width))
            lines.append("")
        
        # Create grid
        grid = [[" " for _ in range(chart_width)] for _ in range(chart_height)]
        
        # Plot points
        for x, y in sorted_data:
            # Normalize to chart coordinates
            if x_max - x_min > 0:
                chart_x = int(((x - x_min) / (x_max - x_min)) * (chart_width - 1))
            else:
                chart_x = chart_width // 2
            
            if y_max - y_min > 0:
                chart_y = int(((y - y_min) / (y_max - y_min)) * (chart_height - 1))
            else:
                chart_y = chart_height // 2
            
            # Ensure within bounds
            chart_x = max(0, min(chart_width - 1, chart_x))
            chart_y = max(0, min(chart_height - 1, chart_y))
            
            # Plot point (invert y for screen coordinates)
            grid[chart_height - 1 - chart_y][chart_x] = "●"
        
        # Draw lines connecting points
        for i in range(len(sorted_data) - 1):
            x1, y1 = sorted_data[i]
            x2, y2 = sorted_data[i + 1]
            
            # Normalize to chart coordinates
            if x_max - x_min > 0:
                chart_x1 = int(((x1 - x_min) / (x_max - x_min)) * (chart_width - 1))
                chart_x2 = int(((x2 - x_min) / (x_max - x_min)) * (chart_width - 1))
            else:
                chart_x1 = chart_x2 = chart_width // 2
            
            if y_max - y_min > 0:
                chart_y1 = int(((y1 - y_min) / (y_max - y_min)) * (chart_height - 1))
                chart_y2 = int(((y2 - y_min) / (y_max - y_min)) * (chart_height - 1))
            else:
                chart_y1 = chart_y2 = chart_height // 2
            
            # Ensure within bounds
            chart_x1 = max(0, min(chart_width - 1, chart_x1))
            chart_x2 = max(0, min(chart_width - 1, chart_x2))
            chart_y1 = max(0, min(chart_height - 1, chart_y1))
            chart_y2 = max(0, min(chart_height - 1, chart_y2))
            
            # Draw line using Bresenham's algorithm
            points = self._bresenham_line(chart_x1, chart_height - 1 - chart_y1,
                                        chart_x2, chart_height - 1 - chart_y2)
            
            for px, py in points:
                if 0 <= px < chart_width and 0 <= py < chart_height:
                    if grid[py][px] == " ":
                        grid[py][px] = "·"
        
        # Convert grid to strings
        for row in grid:
            lines.append("".join(row))
        
        # Add axis labels
        if self.config.y_label:
            for i, line in enumerate(lines):
                if i == len(lines) // 2:
                    lines[i] = self.config.y_label[:3] + " " + line
                    break
        
        if self.config.x_label:
            lines.append(self.config.x_label.center(self.config.width))
        
        return "\n".join(lines)
    
    def _bresenham_line(self, x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
        """Bresenham's line algorithm for drawing lines."""
        points = []
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            points.append((x0, y0))
            
            if x0 == x1 and y0 == y1:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        
        return points
    
    def scatter_plot(self, data: List[Tuple[float, float]],
                   x_range: Optional[Tuple[float, float]] = None,
                   y_range: Optional[Tuple[float, float]] = None) -> str:
        """Generate ASCII scatter plot."""
        if not data:
            return "No data to display"
        
        x_values = [point[0] for point in data]
        y_values = [point[1] for point in data]
        
        # Determine ranges
        if x_range is None:
            x_min, x_max = min(x_values), max(x_values)
        else:
            x_min, x_max = x_range
        
        if y_range is None:
            y_min, y_max = min(y_values), max(y_values)
        else:
            y_min, y_max = y_range
        
        # Calculate dimensions
        chart_width = self.config.width - self.config.padding * 2
        chart_height = self.config.height - self.config.padding * 2
        
        # Build chart
        lines = []
        
        # Add title
        if self.config.title:
            lines.append(self.config.title.center(self.config.width))
            lines.append("")
        
        # Create grid
        grid = [[" " for _ in range(chart_width)] for _ in range(chart_height)]
        
        # Plot points
        for x, y in data:
            # Normalize to chart coordinates
            if x_max - x_min > 0:
                chart_x = int(((x - x_min) / (x_max - x_min)) * (chart_width - 1))
            else:
                chart_x = chart_width // 2
            
            if y_max - y_min > 0:
                chart_y = int(((y - y_min) / (y_max - y_min)) * (chart_height - 1))
            else:
                chart_y = chart_height // 2
            
            # Ensure within bounds
            chart_x = max(0, min(chart_width - 1, chart_x))
            chart_y = max(0, min(chart_height - 1, chart_y))
            
            # Plot point (invert y for screen coordinates)
            grid[chart_height - 1 - chart_y][chart_x] = "●"
        
        # Convert grid to strings
        for row in grid:
            lines.append("".join(row))
        
        # Add axis labels
        if self.config.y_label:
            for i, line in enumerate(lines):
                if i == len(lines) // 2:
                    lines[i] = self.config.y_label[:3] + " " + line
                    break
        
        if self.config.x_label:
            lines.append(self.config.x_label.center(self.config.width))
        
        return "\n".join(lines)
    
    def histogram(self, data: List[float], bins: int = 10) -> str:
        """Generate ASCII histogram."""
        if not data:
            return "No data to display"
        
        # Calculate bin ranges
        min_val = min(data)
        max_val = max(data)
        bin_width = (max_val - min_val) / bins if bins > 0 else 1
        
        # Count values in each bin
        bin_counts = [0] * bins
        for value in data:
            bin_index = int((value - min_val) / bin_width)
            bin_index = min(bin_index, bins - 1)
            bin_counts[bin_index] += 1
        
        # Generate bar chart from bin counts
        bin_labels = [f"{min_val + i * bin_width:.1f}" for i in range(bins)]
        bin_data = dict(zip(bin_labels, bin_counts))
        
        return self.bar_chart(bin_data)
    
    def pie_chart(self, data: Dict[str, float]) -> str:
        """Generate ASCII pie chart (simplified representation)."""
        if not data:
            return "No data to display"
        
        total = sum(data.values())
        if total == 0:
            return "Total value is zero"
        
        lines = []
        
        # Add title
        if self.config.title:
            lines.append(self.config.title.center(self.config.width))
            lines.append("")
        
        # Calculate percentages
        percentages = {key: (value / total) * 100 for key, value in data.items()}
        
        # Display as legend with percentages
        lines.append("Pie Chart (Legend):")
        lines.append("")
        
        for label, percentage in percentages.items():
            bar_length = int(percentage / 5)  # 5% per character
            bar = "█" * bar_length
            lines.append(f"{label:15} {bar} {percentage:.1f}%")
        
        return "\n".join(lines)


class DataAggregator:
    """Data aggregation for visualization."""
    
    @staticmethod
    def aggregate_by_category(data: List[Dict], 
                            category_field: str,
                            value_field: str,
                            aggregation: str = "sum") -> Dict[str, float]:
        """Aggregate data by category."""
        groups = {}
        
        for item in data:
            category = item.get(category_field)
            value = item.get(value_field, 0)
            
            if category not in groups:
                groups[category] = []
            
            groups[category].append(value)
        
        # Apply aggregation
        result = {}
        for category, values in groups.items():
            if aggregation == "sum":
                result[category] = sum(values)
            elif aggregation == "mean":
                result[category] = sum(values) / len(values) if values else 0
            elif aggregation == "count":
                result[category] = len(values)
            elif aggregation == "max":
                result[category] = max(values) if values else 0
            elif aggregation == "min":
                result[category] = min(values) if values else 0
            else:
                result[category] = sum(values)
        
        return result
    
    @staticmethod
    def time_series_aggregation(data: List[Tuple[str, float]],
                               interval: str = "day") -> Dict[str, float]:
        """Aggregate time series data by interval."""
        # Simplified implementation
        return dict(data)
    
    @staticmethod
    def moving_average(data: List[float], window: int = 3) -> List[float]:
        """Calculate moving average."""
        if not data or window <= 0:
            return []
        
        result = []
        for i in range(len(data)):
            start = max(0, i - window + 1)
            window_data = data[start:i + 1]
            result.append(sum(window_data) / len(window_data))
        
        return result
    
    @staticmethod
    def cumulative_sum(data: List[float]) -> List[float]:
        """Calculate cumulative sum."""
        result = []
        total = 0
        for value in data:
            total += value
            result.append(total)
        return result


class ChartExporter:
    """Chart export utilities."""
    
    @staticmethod
    def to_json(chart_data: Dict[str, Any], file_path: str) -> bool:
        """Export chart data to JSON."""
        try:
            with open(file_path, 'w') as f:
                json.dump(chart_data, f, indent=2)
            return True
        except Exception:
            return False
    
    @staticmethod
    def to_csv(data: List[Tuple[float, float]], file_path: str) -> bool:
        """Export data to CSV."""
        try:
            with open(file_path, 'w') as f:
                f.write("x,y\n")
                for x, y in data:
                    f.write(f"{x},{y}\n")
            return True
        except Exception:
            return False
    
    @staticmethod
    def to_html(chart_string: str, file_path: str) -> bool:
        """Export ASCII chart to HTML."""
        try:
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Chart</title>
    <style>
        body {{
            font-family: monospace;
            white-space: pre;
            background-color: #f0f0f0;
            padding: 20px;
        }}
    </style>
</head>
<body>
{chart_string}
</body>
</html>
"""
            with open(file_path, 'w') as f:
                f.write(html_content)
            return True
        except Exception:
            return False


class StatisticalVisualization:
    """Statistical visualization helpers."""
    
    @staticmethod
    def box_plot(data: List[float]) -> str:
        """Generate ASCII box plot."""
        if not data:
            return "No data to display"
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        # Calculate quartiles
        q1 = sorted_data[n // 4]
        median = sorted_data[n // 2]
        q3 = sorted_data[3 * n // 4]
        min_val = sorted_data[0]
        max_val = sorted_data[-1]
        
        # Generate representation
        lines = []
        lines.append("Box Plot:")
        lines.append(f"Min: {min_val}")
        lines.append(f"Q1:  {q1}")
        lines.append(f"Med: {median}")
        lines.append(f"Q3:  {q3}")
        lines.append(f"Max: {max_val}")
        
        # Visual representation
        range_val = max_val - min_val if max_val != min_val else 1
        
        # Scale to 50 characters
        scale = 50 / range_val
        
        def to_pos(value):
            return int((value - min_val) * scale)
        
        min_pos = to_pos(min_val)
        q1_pos = to_pos(q1)
        med_pos = to_pos(median)
        q3_pos = to_pos(q3)
        max_pos = to_pos(max_val)
        
        # Draw box plot
        line = " " * min_pos + "│"
        line += "─" * (q1_pos - min_pos) + "┐"
        line += "─" * (med_pos - q1_pos) + "│"
        line += "─" * (q3_pos - med_pos) + "┘"
        line += "─" * (max_pos - q3_pos) + "│"
        
        lines.append(line)
        lines.append(" " * min_pos + "0" + " " * (max_pos - min_pos) + str(int(max_val)))
        
        return "\n".join(lines)
    
    @staticmethod
    def correlation_matrix(data: Dict[str, List[float]]) -> str:
        """Generate ASCII correlation matrix."""
        if not data:
            return "No data to display"
        
        variables = list(data.keys())
        n = len(variables)
        
        # Calculate correlations
        correlations = {}
        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables):
                if i == j:
                    correlations[(var1, var2)] = 1.0
                elif (var2, var1) in correlations:
                    correlations[(var1, var2)] = correlations[(var2, var1)]
                else:
                    # Calculate correlation
                    values1 = data[var1]
                    values2 = data[var2]
                    
                    if len(values1) != len(values2):
                        correlations[(var1, var2)] = 0.0
                        continue
                    
                    mean1 = sum(values1) / len(values1)
                    mean2 = sum(values2) / len(values2)
                    
                    numerator = sum((v1 - mean1) * (v2 - mean2) for v1, v2 in zip(values1, values2))
                    denominator = math.sqrt(sum((v1 - mean1) ** 2 for v1 in values1) * 
                                         sum((v2 - mean2) ** 2 for v2 in values2))
                    
                    corr = numerator / denominator if denominator != 0 else 0
                    correlations[(var1, var2)] = corr
        
        # Generate matrix display
        lines = []
        lines.append("Correlation Matrix:")
        lines.append("")
        
        # Header
        header = "    " + " ".join(f"{var[:4]:>4}" for var in variables)
        lines.append(header)
        
        # Rows
        for i, var1 in enumerate(variables):
            row = f"{var1[:4]:>4} "
            for j, var2 in enumerate(variables):
                corr = correlations[(var1, var2)]
                # Format correlation with color indicator
                if corr >= 0.7:
                    symbol = "█"
                elif corr >= 0.3:
                    symbol = "▓"
                elif corr >= -0.3:
                    symbol = "░"
                elif corr >= -0.7:
                    symbol = "▒"
                else:
                    symbol = "█"
                
                row += f" {symbol}"
            lines.append(row)
        
        return "\n".join(lines)


def demonstrate_data_visualization():
    """Demonstrate data visualization functionality."""
    print("=== Data Visualization Demonstration ===\n")
    
    # ASCII Chart
    print("1. ASCII Bar Chart:")
    config = ChartConfig(title="Sales by Region", width=60, height=10)
    chart = ASCIIChart(config)
    
    sales_data = {
        "North": 120,
        "South": 80,
        "East": 95,
        "West": 110
    }
    
    print(chart.bar_chart(sales_data))
    
    # Line Chart
    print("\n2. Line Chart:")
    line_data = [(1, 10), (2, 25), (3, 15), (4, 30), (5, 20), (6, 35)]
    config = ChartConfig(title="Performance Over Time", width=50, height=12)
    line_chart = ASCIIChart(config)
    print(line_chart.line_chart(line_data))
    
    # Scatter Plot
    print("\n3. Scatter Plot:")
    scatter_data = [(1, 2), (2, 4), (3, 5), (4, 4), (5, 6), (6, 8)]
    config = ChartConfig(title="Correlation Plot", width=40, height=10)
    scatter_chart = ASCIIChart(config)
    print(scatter_chart.scatter_plot(scatter_data))
    
    # Histogram
    print("\n4. Histogram:")
    histogram_data = [1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5, 6, 7, 8, 9, 10]
    config = ChartConfig(title="Distribution", width=50, height=8)
    hist_chart = ASCIIChart(config)
    print(hist_chart.histogram(histogram_data, bins=5))
    
    # Pie Chart
    print("\n5. Pie Chart:")
    pie_data = {"Product A": 30, "Product B": 25, "Product C": 20, "Product D": 25}
    config = ChartConfig(title="Market Share", width=50)
    pie_chart = ASCIIChart(config)
    print(pie_chart.pie_chart(pie_data))
    
    # Data Aggregation
    print("\n6. Data Aggregation:")
    sample_data = [
        {"category": "A", "value": 10},
        {"category": "B", "value": 20},
        {"category": "A", "value": 15},
        {"category": "B", "value": 25},
        {"category": "C", "value": 30}
    ]
    
    aggregated = DataAggregator.aggregate_by_category(sample_data, "category", "value", "sum")
    print(f"   Aggregated by category: {aggregated}")
    
    moving_avg = DataAggregator.moving_average([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], window=3)
    print(f"   Moving average: {moving_avg}")
    
    cumsum = DataAggregator.cumulative_sum([1, 2, 3, 4, 5])
    print(f"   Cumulative sum: {cumsum}")
    
    # Statistical Visualization
    print("\n7. Statistical Visualization:")
    box_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(StatisticalVisualization.box_plot(box_data))
    
    correlation_data = {
        "A": [1, 2, 3, 4, 5],
        "B": [2, 4, 6, 8, 10],
        "C": [5, 4, 3, 2, 1]
    }
    print(StatisticalVisualization.correlation_matrix(correlation_data))
    
    # Export
    print("\n8. Export Utilities:")
    chart_data = {"type": "bar", "data": sales_data}
    exported = ChartExporter.to_json(chart_data, "chart_data.json")
    print(f"   JSON export: {exported}")
    
    exported_csv = ChartExporter.to_csv(line_data, "chart_data.csv")
    print(f"   CSV export: {exported_csv}")
    
    # Cleanup
    import os
    for file in ["chart_data.json", "chart_data.csv"]:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n=== Demonstration Complete ===")
    print("\nData Visualization Tips:")
    print("- Choose appropriate chart type for your data")
    print("- Use clear labels and titles")
    print("- Consider color schemes for accessibility")
    print("- Aggregate data appropriately for visualization")
    print("- Use statistical plots for data analysis")
    print("- Export charts for sharing and documentation")
    print("- For advanced plotting, consider matplotlib or plotly")


if __name__ == "__main__":
    demonstrate_data_visualization()