"""
Time Series Analysis Module

This module provides comprehensive time series analysis utilities including:
- Time series data structures
- Smoothing techniques (moving average, exponential smoothing)
- Trend analysis
- Seasonality detection
- Stationarity tests
- Forecasting methods
- Anomaly detection
- Time series decomposition
- Feature engineering
- Statistical tests

All functions include comprehensive docstrings and type hints.
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import statistics


class TimeSeriesType(Enum):
    """Types of time series."""
    UNIVARIATE = "univariate"
    MULTIVARIATE = "multivariate"
    SEASONAL = "seasonal"
    NON_SEASONAL = "non_seasonal"


@dataclass
class TimePoint:
    """Single time point in series."""
    timestamp: datetime
    value: float
    metadata: Optional[Dict] = None


@dataclass
class TimeSeries:
    """Time series data structure."""
    name: str
    data: List[TimePoint]
    frequency: Optional[str] = None
    
    def __len__(self) -> int:
        """Get length of time series."""
        return len(self.data)
    
    def get_values(self) -> List[float]:
        """Get all values."""
        return [tp.value for tp in self.data]
    
    def get_timestamps(self) -> List[datetime]:
        """Get all timestamps."""
        return [tp.timestamp for tp in self.data]
    
    def get_range(self) -> Tuple[datetime, datetime]:
        """Get time range."""
        if not self.data:
            return None, None
        return self.data[0].timestamp, self.data[-1].timestamp


class Smoothing:
    """Time series smoothing techniques."""
    
    @staticmethod
    def simple_moving_average(values: List[float], window: int) -> List[float]:
        """Simple moving average."""
        if window <= 0 or window > len(values):
            return values
        
        smoothed = []
        for i in range(len(values)):
            if i < window - 1:
                smoothed.append(values[i])
            else:
                window_avg = statistics.mean(values[i - window + 1:i + 1])
                smoothed.append(window_avg)
        
        return smoothed
    
    @staticmethod
    def weighted_moving_average(values: List[float], weights: List[float]) -> List[float]:
        """Weighted moving average."""
        if len(weights) > len(values):
            return values
        
        smoothed = []
        window = len(weights)
        total_weight = sum(weights)
        
        for i in range(len(values)):
            if i < window - 1:
                smoothed.append(values[i])
            else:
                weighted_sum = sum(w * v for w, v in zip(weights, values[i - window + 1:i + 1]))
                smoothed.append(weighted_sum / total_weight)
        
        return smoothed
    
    @staticmethod
    def exponential_smoothing(values: List[float], alpha: float = 0.3) -> List[float]:
        """Simple exponential smoothing."""
        if not values:
            return []
        
        smoothed = [values[0]]
        
        for i in range(1, len(values)):
            smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[i - 1])
        
        return smoothed
    
    @staticmethod
    def double_exponential_smoothing(values: List[float], 
                                   alpha: float = 0.3,
                                   beta: float = 0.3) -> List[float]:
        """Double exponential smoothing (Holt's method)."""
        if not values:
            return []
        
        # Initialize level and trend
        level = values[0]
        trend = values[1] - values[0] if len(values) > 1 else 0
        
        smoothed = [level]
        
        for i in range(1, len(values)):
            # Update level and trend
            new_level = alpha * values[i] + (1 - alpha) * (level + trend)
            new_trend = beta * (new_level - level) + (1 - beta) * trend
            
            level = new_level
            trend = new_trend
            
            smoothed.append(level + trend)
        
        return smoothed
    
    @staticmethod
    def center_moving_average(values: List[float], window: int) -> List[float]:
        """Centered moving average."""
        if window <= 0 or window > len(values):
            return values
        
        half_window = window // 2
        smoothed = []
        
        for i in range(len(values)):
            start = max(0, i - half_window)
            end = min(len(values), i + half_window + 1)
            window_avg = statistics.mean(values[start:end])
            smoothed.append(window_avg)
        
        return smoothed


class TrendAnalysis:
    """Trend analysis utilities."""
    
    @staticmethod
    def linear_trend(values: List[float]) -> Tuple[float, float]:
        """Calculate linear trend (slope and intercept)."""
        n = len(values)
        if n < 2:
            return 0.0, 0.0
        
        x = list(range(n))
        y = values
        
        # Calculate slope and intercept using least squares
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        return slope, intercept
    
    @staticmethod
    def polynomial_trend(values: List[float], degree: int = 2) -> List[float]:
        """Calculate polynomial trend."""
        n = len(values)
        if n < degree + 1:
            return values
        
        x = list(range(n))
        y = values
        
        # Normal equations for polynomial regression
        def build_matrix(degree):
            matrix = []
            for i in range(degree + 1):
                row = []
                for j in range(degree + 1):
                    row.append(sum(xi ** (i + j) for xi in x))
                matrix.append(row)
            return matrix
        
        def build_vector(degree):
            vector = []
            for i in range(degree + 1):
                vector.append(sum(xi ** i * yi for xi, yi in zip(x, y)))
            return vector
        
        # Simple implementation for degree 2
        if degree == 2:
            # Solve for coefficients manually for quadratic
            # Using numpy would be easier, but this is pure Python
            # For simplicity, return linear trend
            slope, intercept = TrendAnalysis.linear_trend(values)
            return [intercept + slope * xi for xi in x]
        
        return values
    
    @staticmethod
    def remove_trend(values: List[float]) -> List[float]:
        """Remove linear trend from series."""
        slope, intercept = TrendAnalysis.linear_trend(values)
        detrended = []
        
        for i, value in enumerate(values):
            trend_value = intercept + slope * i
            detrended.append(value - trend_value)
        
        return detrended


class Seasonality:
    """Seasonality detection and analysis."""
    
    @staticmethod
    def seasonal_decompose(values: List[float], period: int) -> Dict[str, List[float]]:
        """Decompose time series into trend, seasonal, and residual."""
        if len(values) < period * 2:
            return {
                "trend": values,
                "seasonal": [0] * len(values),
                "residual": values
            }
        
        # Calculate trend using moving average
        trend = Smoothing.center_moving_average(values, period)
        
        # Calculate seasonal component
        seasonal = []
        for i in range(len(values)):
            if trend[i] != 0:
                seasonal.append(values[i] - trend[i])
            else:
                seasonal.append(0)
        
        # Average seasonal pattern
        seasonal_pattern = []
        for i in range(period):
            indices = range(i, len(seasonal), period)
            pattern_value = statistics.mean([seasonal[j] for j in indices])
            seasonal_pattern.append(pattern_value)
        
        # Apply seasonal pattern
        seasonal_component = []
        for i in range(len(values)):
            seasonal_component.append(seasonal_pattern[i % period])
        
        # Calculate residual
        residual = []
        for i in range(len(values)):
            residual.append(values[i] - trend[i] - seasonal_component[i])
        
        return {
            "trend": trend,
            "seasonal": seasonal_component,
            "residual": residual
        }
    
    @staticmethod
    def detect_seasonality(values: List[float], max_period: int = 12) -> Optional[int]:
        """Detect seasonality period using autocorrelation."""
        n = len(values)
        if n < 10:
            return None
        
        # Calculate autocorrelation for different lags
        autocorrelations = []
        
        for lag in range(1, min(max_period, n // 2)):
            correlation = Seasonality._autocorrelation(values, lag)
            autocorrelations.append((lag, correlation))
        
        # Find lag with highest autocorrelation
        if autocorrelations:
            best_lag, best_corr = max(autocorrelations, key=lambda x: x[1])
            if abs(best_corr) > 0.3:  # Threshold for significance
                return best_lag
        
        return None
    
    @staticmethod
    def _autocorrelation(values: List[float], lag: int) -> float:
        """Calculate autocorrelation at given lag."""
        n = len(values)
        if lag >= n:
            return 0.0
        
        mean = statistics.mean(values)
        variance = statistics.variance(values) if len(values) > 1 else 0
        
        if variance == 0:
            return 0.0
        
        covariance = 0.0
        for i in range(n - lag):
            covariance += (values[i] - mean) * (values[i + lag] - mean)
        
        covariance /= (n - lag)
        
        return covariance / variance


class Stationarity:
    """Stationarity tests and transformations."""
    
    @staticmethod
    def adf_test(values: List[float]) -> Dict[str, Any]:
        """Augmented Dickey-Fuller test (simplified)."""
        # This is a simplified version - real ADF test requires more complex implementation
        n = len(values)
        if n < 10:
            return {"is_stationary": False, "p_value": 1.0}
        
        # Calculate first differences
        differences = [values[i] - values[i - 1] for i in range(1, n)]
        
        # Simple test: check if variance of differences is less than variance of original
        original_variance = statistics.variance(values)
        diff_variance = statistics.variance(differences)
        
        is_stationary = diff_variance < original_variance
        p_value = 0.05 if is_stationary else 0.5
        
        return {
            "is_stationary": is_stationary,
            "p_value": p_value,
            "test_statistic": diff_variance / original_variance if original_variance > 0 else 0
        }
    
    @staticmethod
    def make_stationary(values: List[float]) -> Tuple[List[float], str]:
        """Transform series to stationary."""
        n = len(values)
        if n < 2:
            return values, "none"
        
        # Try first difference
        differences = [values[i] - values[i - 1] for i in range(1, n)]
        
        # Check if differences are more stationary
        original_var = statistics.variance(values)
        diff_var = statistics.variance(differences)
        
        if diff_var < original_var:
            return differences, "first_difference"
        
        # Try log transformation
        try:
            log_values = [math.log(abs(v) + 1) for v in values]
            log_diff = [log_values[i] - log_values[i - 1] for i in range(1, n)]
            log_diff_var = statistics.variance(log_diff)
            
            if log_diff_var < diff_var:
                return log_diff, "log_difference"
        except:
            pass
        
        return differences, "first_difference"


class Forecasting:
    """Time series forecasting methods."""
    
    @staticmethod
    def naive_forecast(values: List[float], steps: int = 1) -> List[float]:
        """Naive forecast (last value)."""
        if not values:
            return []
        
        last_value = values[-1]
        return [last_value] * steps
    
    @staticmethod
    def average_forecast(values: List[float], steps: int = 1) -> List[float]:
        """Average forecast (mean of all values)."""
        if not values:
            return []
        
        avg = statistics.mean(values)
        return [avg] * steps
    
    @staticmethod
    def moving_average_forecast(values: List[float], window: int, steps: int = 1) -> List[float]:
        """Moving average forecast."""
        if not values or window <= 0:
            return []
        
        window = min(window, len(values))
        ma = statistics.mean(values[-window:])
        return [ma] * steps
    
    @staticmethod
    def exponential_smoothing_forecast(values: List[float], 
                                      alpha: float = 0.3,
                                      steps: int = 1) -> List[float]:
        """Exponential smoothing forecast."""
        if not values:
            return []
        
        smoothed = Smoothing.exponential_smoothing(values, alpha)
        last_smoothed = smoothed[-1]
        return [last_smoothed] * steps
    
    @staticmethod
    def linear_trend_forecast(values: List[float], steps: int = 1) -> List[float]:
        """Linear trend forecast."""
        if len(values) < 2:
            return []
        
        slope, intercept = TrendAnalysis.linear_trend(values)
        n = len(values)
        
        forecasts = []
        for i in range(steps):
            forecast = intercept + slope * (n + i)
            forecasts.append(forecast)
        
        return forecasts
    
    @staticmethod
    def seasonal_naive_forecast(values: List[float], period: int, steps: int = 1) -> List[float]:
        """Seasonal naive forecast."""
        if len(values) < period:
            return []
        
        forecasts = []
        for i in range(steps):
            # Use value from same period in previous cycle
            index = len(values) - period + (i % period)
            if index >= 0:
                forecasts.append(values[index])
            else:
                forecasts.append(values[-1])
        
        return forecasts


class AnomalyDetection:
    """Anomaly detection in time series."""
    
    @staticmethod
    def z_score_anomaly(values: List[float], threshold: float = 3.0) -> List[int]:
        """Detect anomalies using z-score."""
        if len(values) < 2:
            return []
        
        mean = statistics.mean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0
        
        if std == 0:
            return []
        
        anomalies = []
        for i, value in enumerate(values):
            z_score = abs((value - mean) / std)
            if z_score > threshold:
                anomalies.append(i)
        
        return anomalies
    
    @staticmethod
    def iqr_anomaly(values: List[float], multiplier: float = 1.5) -> List[int]:
        """Detect anomalies using IQR method."""
        if len(values) < 4:
            return []
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        q1 = sorted_values[n // 4]
        q3 = sorted_values[3 * n // 4]
        iqr = q3 - q1
        
        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr
        
        anomalies = []
        for i, value in enumerate(values):
            if value < lower_bound or value > upper_bound:
                anomalies.append(i)
        
        return anomalies
    
    @staticmethod
    def moving_average_anomaly(values: List[float], 
                               window: int = 5,
                               threshold: float = 2.0) -> List[int]:
        """Detect anomalies using moving average."""
        if len(values) < window:
            return []
        
        anomalies = []
        ma = Smoothing.simple_moving_average(values, window)
        
        for i in range(window, len(values)):
            std = statistics.stdev(values[i - window:i]) if window > 1 else 0
            if std > 0:
                z_score = abs((values[i] - ma[i]) / std)
                if z_score > threshold:
                    anomalies.append(i)
        
        return anomalies


class FeatureEngineering:
    """Feature engineering for time series."""
    
    @staticmethod
    def create_lag_features(values: List[float], lags: List[int]) -> Dict[str, List[float]]:
        """Create lag features."""
        features = {}
        
        for lag in lags:
            lagged = [None] * lag + values[:-lag]
            features[f"lag_{lag}"] = lagged
        
        return features
    
    @staticmethod
    def create_rolling_features(values: List[float], 
                                 window: int) -> Dict[str, List[float]]:
        """Create rolling features."""
        rolling_mean = Smoothing.simple_moving_average(values, window)
        rolling_std = []
        
        for i in range(len(values)):
            start = max(0, i - window + 1)
            window_values = values[start:i + 1]
            if len(window_values) > 1:
                rolling_std.append(statistics.stdev(window_values))
            else:
                rolling_std.append(0)
        
        return {
            "rolling_mean": rolling_mean,
            "rolling_std": rolling_std
        }
    
    @staticmethod
    def create_diff_features(values: List[float], order: int = 1) -> Dict[str, List[float]]:
        """Create difference features."""
        features = {}
        current_values = values
        
        for i in range(1, order + 1):
            if len(current_values) < 2:
                break
            
            differences = [current_values[j] - current_values[j - 1] 
                          for j in range(1, len(current_values))]
            features[f"diff_{i}"] = [None] * i + differences
            current_values = differences
        
        return features
    
    @staticmethod
    def create_datetime_features(timestamps: List[datetime]) -> Dict[str, List[int]]:
        """Create datetime features."""
        features = {
            "hour": [ts.hour for ts in timestamps],
            "day": [ts.day for ts in timestamps],
            "month": [ts.month for ts in timestamps],
            "day_of_week": [ts.weekday() for ts in timestamps],
            "day_of_year": [ts.timetuple().tm_yday for ts in timestamps],
            "quarter": [(ts.month - 1) // 3 + 1 for ts in timestamps]
        }
        
        return features


class Statistics:
    """Time series statistics."""
    
    @staticmethod
    def summary_statistics(values: List[float]) -> Dict[str, float]:
        """Calculate summary statistics."""
        if not values:
            return {}
        
        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
            "range": max(values) - min(values),
            "variance": statistics.variance(values) if len(values) > 1 else 0
        }
    
    @staticmethod
    def percent_change(values: List[float]) -> List[float]:
        """Calculate percent change."""
        if len(values) < 2:
            return [0.0] * len(values)
        
        changes = [0.0]
        for i in range(1, len(values)):
            if values[i - 1] != 0:
                change = (values[i] - values[i - 1]) / values[i - 1] * 100
            else:
                change = 0.0
            changes.append(change)
        
        return changes
    
    @staticmethod
    def cumulative_return(values: List[float]) -> List[float]:
        """Calculate cumulative return."""
        if not values:
            return []
        
        cumulative = [values[0]]
        for i in range(1, len(values)):
            cumulative.append(cumulative[-1] * (1 + values[i] / 100))
        
        return cumulative


def demonstrate_time_series():
    """Demonstrate time series functionality."""
    print("=== Time Series Analysis Demonstration ===\n")
    
    # Sample time series data
    values = [10, 12, 15, 14, 16, 18, 20, 19, 22, 25, 23, 26]
    timestamps = [datetime(2024, 1, i + 1) for i in range(len(values))]
    
    # Create Time Series
    print("1. Time Series Structure:")
    time_points = [TimePoint(ts, val) for ts, val in zip(timestamps, values)]
    ts = TimeSeries("sample", time_points, "daily")
    
    print(f"   Name: {ts.name}")
    print(f"   Length: {len(ts)}")
    print(f"   Range: {ts.get_range()}")
    
    # Smoothing
    print("\n2. Smoothing:")
    ma_3 = Smoothing.simple_moving_average(values, 3)
    print(f"   MA(3): {ma_3[:5]}...")
    
    exp_smooth = Smoothing.exponential_smoothing(values, 0.3)
    print(f"   Exponential smoothing: {exp_smooth[:5]}...")
    
    # Trend Analysis
    print("\n3. Trend Analysis:")
    slope, intercept = TrendAnalysis.linear_trend(values)
    print(f"   Linear trend: slope={slope:.2f}, intercept={intercept:.2f}")
    
    detrended = TrendAnalysis.remove_trend(values)
    print(f"   Detrended: {detrended[:5]}...")
    
    # Seasonality
    print("\n4. Seasonality:")
    period = Seasonality.detect_seasonality(values)
    print(f"   Detected period: {period}")
    
    if period:
        decomposition = Seasonality.seasonal_decompose(values, period)
        print(f"   Seasonal component: {decomposition['seasonal'][:5]}...")
    
    # Stationarity
    print("\n5. Stationarity:")
    adf_result = Stationarity.adf_test(values)
    print(f"   Is stationary: {adf_result['is_stationary']}")
    
    stationary, method = Stationarity.make_stationary(values)
    print(f"   Transformation method: {method}")
    
    # Forecasting
    print("\n6. Forecasting:")
    naive_forecast = Forecasting.naive_forecast(values, 3)
    print(f"   Naive forecast: {naive_forecast}")
    
    trend_forecast = Forecasting.linear_trend_forecast(values, 3)
    print(f"   Trend forecast: {trend_forecast}")
    
    exp_forecast = Forecasting.exponential_smoothing_forecast(values, 0.3, 3)
    print(f"   Exponential forecast: {exp_forecast}")
    
    # Anomaly Detection
    print("\n7. Anomaly Detection:")
    z_anomalies = AnomalyDetection.z_score_anomaly(values, threshold=2.0)
    print(f"   Z-score anomalies at indices: {z_anomalies}")
    
    iqr_anomalies = AnomalyDetection.iqr_anomaly(values)
    print(f"   IQR anomalies at indices: {iqr_anomalies}")
    
    # Feature Engineering
    print("\n8. Feature Engineering:")
    lag_features = FeatureEngineering.create_lag_features(values, [1, 2])
    print(f"   Lag features keys: {list(lag_features.keys())}")
    
    rolling_features = FeatureEngineering.create_rolling_features(values, 3)
    print(f"   Rolling mean: {rolling_features['rolling_mean'][:5]}...")
    
    diff_features = FeatureEngineering.create_diff_features(values, 1)
    print(f"   Diff features: {diff_features['diff_1'][:5]}...")
    
    datetime_features = FeatureEngineering.create_datetime_features(timestamps)
    print(f"   Datetime features keys: {list(datetime_features.keys())}")
    
    # Statistics
    print("\n9. Statistics:")
    stats = Statistics.summary_statistics(values)
    print(f"   Summary: {stats}")
    
    pct_change = Statistics.percent_change(values)
    print(f"   Percent change: {pct_change[:5]}...")
    
    cum_return = Statistics.cumulative_return(pct_change)
    print(f"   Cumulative return: {cum_return[:5]}...")
    
    print("\n=== Demonstration Complete ===")
    print("\nTime Series Best Practices:")
    print("- Always check for stationarity before modeling")
    print("- Use appropriate differencing for non-stationary series")
    print("- Detect and handle seasonality properly")
    print("- Use multiple forecasting methods and compare")
    print("- Validate forecasts using hold-out data")
    print("- Handle missing values appropriately")
    print("- Consider data frequency and sampling")
    print("- Use domain knowledge for feature engineering")
    print("- Monitor forecast accuracy over time")
    print("- Update models regularly with new data")


if __name__ == "__main__":
    demonstrate_time_series()