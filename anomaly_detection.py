"""
Anomaly Detection Module

This module provides comprehensive anomaly detection utilities including:
- Statistical anomaly detection
- Z-score based detection
- IQR (Interquartile Range) method
- Isolation Forest concepts
- One-Class SVM concepts
- DBSCAN clustering for anomaly detection
- Autoencoder concepts
- Time series anomaly detection
- Multivariate anomaly detection
- Anomaly scoring and thresholding

Note: This module uses numpy and scikit-learn for advanced features.
Install with: pip install numpy scikit-learn

All functions include comprehensive docstrings and type hints.
"""

import math
import random
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from collections import Counter


try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from sklearn.ensemble import IsolationForest
    from sklearn.svm import OneClassSVM
    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class AnomalyType(Enum):
    """Types of anomalies."""
    POINT = "point"
    CONTEXTUAL = "contextual"
    COLLECTIVE = "collective"


class DetectionMethod(Enum):
    """Detection methods."""
    Z_SCORE = "z_score"
    IQR = "iqr"
    ISOLATION_FOREST = "isolation_forest"
    ONE_CLASS_SVM = "one_class_svm"
    DBSCAN = "dbscan"
    MOVING_AVERAGE = "moving_average"
    AUTOENCODER = "autoencoder"


@dataclass
class Anomaly:
    """Anomaly data structure."""
    index: int
    value: float
    score: float
    method: DetectionMethod
    timestamp: Optional[float] = None
    context: Optional[Dict] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}


class StatisticalAnomalyDetector:
    """Statistical anomaly detection methods."""
    
    @staticmethod
    def calculate_z_score(value: float, mean: float, std: float) -> float:
        """Calculate Z-score for value."""
        if std == 0:
            return 0.0
        return (value - mean) / std
    
    @staticmethod
    def detect_anomalies_z_score(data: List[float], threshold: float = 3.0) -> List[Anomaly]:
        """Detect anomalies using Z-score method."""
        if not data:
            return []
        
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        std = math.sqrt(variance)
        
        anomalies = []
        
        for i, value in enumerate(data):
            z_score = StatisticalAnomalyDetector.calculate_z_score(value, mean, std)
            
            if abs(z_score) > threshold:
                anomalies.append(Anomaly(
                    index=i,
                    value=value,
                    score=abs(z_score),
                    method=DetectionMethod.Z_SCORE
                ))
        
        return anomalies
    
    @staticmethod
    def detect_anomalies_iqr(data: List[float], multiplier: float = 1.5) -> List[Anomaly]:
        """Detect anomalies using IQR method."""
        if not data:
            return []
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        q1_index = n // 4
        q3_index = 3 * n // 4
        
        q1 = sorted_data[q1_index]
        q3 = sorted_data[q3_index]
        
        iqr = q3 - q1
        
        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr
        
        anomalies = []
        
        for i, value in enumerate(data):
            if value < lower_bound or value > upper_bound:
                # Calculate anomaly score based on distance from bounds
                if value < lower_bound:
                    score = (lower_bound - value) / iqr
                else:
                    score = (value - upper_bound) / iqr
                
                anomalies.append(Anomaly(
                    index=i,
                    value=value,
                    score=score,
                    method=DetectionMethod.IQR
                ))
        
        return anomalies
    
    @staticmethod
    def detect_anomalies_moving_average(data: List[float], window_size: int = 5,
                                        threshold: float = 2.0) -> List[Anomaly]:
        """Detect anomalies using moving average."""
        if len(data) < window_size:
            return []
        
        anomalies = []
        
        for i in range(window_size, len(data)):
            window = data[i - window_size:i]
            mean = sum(window) / len(window)
            std = math.sqrt(sum((x - mean) ** 2 for x in window) / len(window))
            
            if std > 0:
                z_score = abs((data[i] - mean) / std)
                
                if z_score > threshold:
                    anomalies.append(Anomaly(
                        index=i,
                        value=data[i],
                        score=z_score,
                        method=DetectionMethod.MOVING_AVERAGE
                    ))
        
        return anomalies


class MachineLearningAnomalyDetector:
    """Machine learning-based anomaly detection."""
    
    def __init__(self):
        """Initialize ML detector."""
        self.model = None
        self.scaler = None
        self.is_fitted = False
    
    def fit_isolation_forest(self, data: List[List[float]], contamination: float = 0.1) -> None:
        """Fit Isolation Forest model."""
        if not SKLEARN_AVAILABLE:
            print("scikit-learn not available")
            return
        
        self.scaler = StandardScaler()
        scaled_data = self.scaler.fit_transform(data)
        
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.model.fit(scaled_data)
        self.is_fitted = True
    
    def fit_one_class_svm(self, data: List[List[float]], nu: float = 0.1) -> None:
        """Fit One-Class SVM model."""
        if not SKLEARN_AVAILABLE:
            print("scikit-learn not available")
            return
        
        self.scaler = StandardScaler()
        scaled_data = self.scaler.fit_transform(data)
        
        self.model = OneClassSVM(nu=nu, kernel='rbf')
        self.model.fit(scaled_data)
        self.is_fitted = True
    
    def predict(self, data: List[List[float]]) -> List[Anomaly]:
        """Predict anomalies."""
        if not self.is_fitted or not SKLEARN_AVAILABLE:
            return []
        
        scaled_data = self.scaler.transform(data)
        predictions = self.model.predict(scaled_data)
        
        anomalies = []
        
        for i, prediction in enumerate(predictions):
            if prediction == -1:  # Anomaly
                # Calculate anomaly score
                if hasattr(self.model, 'score_samples'):
                    scores = self.model.score_samples(scaled_data)
                    anomaly_score = -scores[i]  # Convert to positive
                else:
                    anomaly_score = 1.0
                
                anomalies.append(Anomaly(
                    index=i,
                    value=0.0,  # For multivariate, use 0 or first dimension
                    score=anomaly_score,
                    method=DetectionMethod.ISOLATION_FOREST if isinstance(self.model, IsolationForest) else DetectionMethod.ONE_CLASS_SVM
                ))
        
        return anomalies


class ClusteringAnomalyDetector:
    """Clustering-based anomaly detection."""
    
    @staticmethod
    def detect_anomalies_dbscan(data: List[List[float]], eps: float = 0.5,
                               min_samples: int = 5) -> List[Anomaly]:
        """Detect anomalies using DBSCAN clustering."""
        if not SKLEARN_AVAILABLE:
            return []
        
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(scaled_data)
        
        anomalies = []
        
        for i, label in enumerate(labels):
            if label == -1:  # Noise point = anomaly
                anomalies.append(Anomaly(
                    index=i,
                    value=0.0,
                    score=1.0,
                    method=DetectionMethod.DBSCAN
                ))
        
        return anomalies


class TimeSeriesAnomalyDetector:
    """Time series specific anomaly detection."""
    
    @staticmethod
    def detect_seasonal_anomalies(data: List[float], period: int,
                                  threshold: float = 2.0) -> List[Anomaly]:
        """Detect seasonal anomalies using decomposition."""
        if len(data) < period * 2:
            return []
        
        anomalies = []
        
        # Calculate seasonal baseline
        seasonal_means = {}
        
        for i in range(len(data)):
            season = i % period
            if season not in seasonal_means:
                seasonal_means[season] = []
            seasonal_means[season].append(data[i])
        
        # Calculate mean and std for each season
        seasonal_stats = {}
        for season, values in seasonal_means.items():
            mean = sum(values) / len(values)
            std = math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
            seasonal_stats[season] = (mean, std)
        
        # Detect anomalies
        for i, value in enumerate(data):
            season = i % period
            mean, std = seasonal_stats[season]
            
            if std > 0:
                z_score = abs((value - mean) / std)
                
                if z_score > threshold:
                    anomalies.append(Anomaly(
                        index=i,
                        value=value,
                        score=z_score,
                        method=DetectionMethod.MOVING_AVERAGE
                    ))
        
        return anomalies
    
    @staticmethod
    def detect_trend_anomalies(data: List[float], window_size: int = 10,
                              threshold: float = 2.0) -> List[Anomaly]:
        """Detect trend anomalies."""
        if len(data) < window_size * 2:
            return []
        
        anomalies = []
        
        # Calculate moving average
        moving_avg = []
        for i in range(window_size, len(data)):
            window = data[i - window_size:i]
            moving_avg.append(sum(window) / len(window))
        
        # Detect sudden changes
        for i in range(1, len(moving_avg)):
            change = abs(moving_avg[i] - moving_avg[i - 1])
            
            # Calculate expected change based on history
            if i > 1:
                expected_change = abs(moving_avg[i - 1] - moving_avg[i - 2])
                
                if expected_change > 0:
                    anomaly_score = change / expected_change
                    
                    if anomaly_score > threshold:
                        anomalies.append(Anomaly(
                            index=i + window_size,
                            value=data[i + window_size],
                            score=anomaly_score,
                            method=DetectionMethod.MOVING_AVERAGE
                        ))
        
        return anomalies


class MultivariateAnomalyDetector:
    """Multivariate anomaly detection."""
    
    @staticmethod
    def calculate_mahalanobis_distance(point: List[float], 
                                        mean: List[float],
                                        cov_matrix: List[List[float]]) -> float:
        """Calculate Mahalanobis distance."""
        if not NUMPY_AVAILABLE:
            return 0.0
        
        point_arr = np.array(point)
        mean_arr = np.array(mean)
        cov_arr = np.array(cov_matrix)
        
        try:
            inv_cov = np.linalg.inv(cov_arr)
            diff = point_arr - mean_arr
            distance = np.sqrt(diff.T @ inv_cov @ diff)
            return float(distance)
        except:
            return 0.0
    
    @staticmethod
    def detect_anomalies_mahalanobis(data: List[List[float]],
                                      threshold: float = 3.0) -> List[Anomaly]:
        """Detect anomalies using Mahalanobis distance."""
        if not NUMPY_AVAILABLE:
            return []
        
        data_arr = np.array(data)
        mean = np.mean(data_arr, axis=0).tolist()
        cov_matrix = np.cov(data_arr.T).tolist()
        
        anomalies = []
        
        for i, point in enumerate(data):
            distance = MultivariateAnomalyDetector.calculate_mahalanobis_distance(
                point, mean, cov_matrix
            )
            
            if distance > threshold:
                anomalies.append(Anomaly(
                    index=i,
                    value=point[0],  # Use first dimension
                    score=distance,
                    method=DetectionMethod.Z_SCORE
                ))
        
        return anomalies


class AutoencoderAnomalyDetector:
    """Autoencoder-based anomaly detection concepts."""
    
    def __init__(self, input_dim: int, encoding_dim: int = 2):
        """Initialize autoencoder detector."""
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        self.is_trained = False
    
    def train(self, data: List[List[float]], epochs: int = 100) -> None:
        """Train autoencoder (simplified - would use neural network in real implementation)."""
        # In real implementation, this would use Keras/PyTorch
        # For demonstration, we'll just mark as trained
        self.is_trained = True
    
    def detect_anomalies(self, data: List[List[float]], threshold: float = 0.5) -> List[Anomaly]:
        """Detect anomalies using reconstruction error."""
        if not self.is_trained:
            return []
        
        # In real implementation, this would calculate reconstruction error
        # For demonstration, we'll use a simple heuristic
        anomalies = []
        
        for i, point in enumerate(data):
            # Simplified reconstruction error calculation
            error = sum(abs(x) for x in point) / len(point)
            
            if error > threshold:
                anomalies.append(Anomaly(
                    index=i,
                    value=point[0],
                    score=error,
                    method=DetectionMethod.AUTOENCODER
                ))
        
        return anomalies


class AnomalyScorer:
    """Anomaly scoring and thresholding."""
    
    @staticmethod
    def normalize_scores(anomalies: List[Anomaly]) -> List[Anomaly]:
        """Normalize anomaly scores to [0, 1]."""
        if not anomalies:
            return anomalies
        
        scores = [a.score for a in anomalies]
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            return anomalies
        
        for anomaly in anomalies:
            anomaly.score = (anomaly.score - min_score) / (max_score - min_score)
        
        return anomalies
    
    @staticmethod
    def select_top_k(anomalies: List[Anomaly], k: int) -> List[Anomaly]:
        """Select top K anomalies by score."""
        sorted_anomalies = sorted(anomalies, key=lambda a: a.score, reverse=True)
        return sorted_anomalies[:k]
    
    @staticmethod
    def threshold_by_percentile(anomalies: List[Anomaly], percentile: float = 95.0) -> List[Anomaly]:
        """Select anomalies above percentile threshold."""
        if not anomalies:
            return []
        
        scores = [a.score for a in anomalies]
        threshold_score = np.percentile(scores, percentile) if NUMPY_AVAILABLE else sorted(scores)[int(len(scores) * percentile / 100)]
        
        return [a for a in anomalies if a.score >= threshold_score]


class AnomalyEnsemble:
    """Ensemble of multiple anomaly detection methods."""
    
    def __init__(self, methods: List[DetectionMethod]):
        """Initialize ensemble."""
        self.methods = methods
        self.detectors = {}
        
        for method in methods:
            if method == DetectionMethod.ISOLATION_FOREST:
                self.detectors[method] = MachineLearningAnomalyDetector()
            elif method == DetectionMethod.ONE_CLASS_SVM:
                self.detectors[method] = MachineLearningAnomalyDetector()
    
    def fit(self, data: List[List[float]]) -> None:
        """Fit all detectors."""
        for method, detector in self.detectors.items():
            if method == DetectionMethod.ISOLATION_FOREST:
                detector.fit_isolation_forest(data)
            elif method == DetectionMethod.ONE_CLASS_SVM:
                detector.fit_one_class_svm(data)
    
    def detect(self, data: List[List[float]]) -> List[Anomaly]:
        """Detect anomalies using ensemble."""
        all_anomalies = []
        
        for method in self.methods:
            if method == DetectionMethod.Z_SCORE:
                # Use first dimension for univariate methods
                univariate_data = [point[0] for point in data]
                anomalies = StatisticalAnomalyDetector.detect_anomalies_z_score(univariate_data)
                all_anomalies.extend(anomalies)
            
            elif method == DetectionMethod.IQR:
                univariate_data = [point[0] for point in data]
                anomalies = StatisticalAnomalyDetector.detect_anomalies_iqr(univariate_data)
                all_anomalies.extend(anomalies)
            
            elif method in self.detectors:
                detector = self.detectors[method]
                anomalies = detector.predict(data)
                all_anomalies.extend(anomalies)
        
        # Combine results (simplified - take union)
        return all_anomalies


def demonstrate_anomaly_detection():
    """Demonstrate anomaly detection functionality."""
    print("=== Anomaly Detection Demonstration ===\n")
    
    # Generate sample data
    print("1. Sample Data Generation:")
    normal_data = [random.gauss(50, 5) for _ in range(100)]
    anomalous_data = normal_data + [100, 110, 5, -10, 120]  # Add anomalies
    
    print(f"   Normal data points: {len(normal_data)}")
    print(f"   Anomalous data points: {len(anomalous_data)}")
    print(f"   Data range: {min(anomalous_data):.2f} to {max(anomalous_data):.2f}")
    
    # Z-Score Detection
    print("\n2. Z-Score Anomaly Detection:")
    z_anomalies = StatisticalAnomalyDetector.detect_anomalies_z_score(anomalous_data, threshold=2.5)
    print(f"   Anomalies detected: {len(z_anomalies)}")
    print(f"   Anomaly indices: {[a.index for a in z_anomalies]}")
    print(f"   Anomaly values: {[f'{a.value:.2f}' for a in z_anomalies]}")
    
    # IQR Detection
    print("\n3. IQR Anomaly Detection:")
    iqr_anomalies = StatisticalAnomalyDetector.detect_anomalies_iqr(anomalous_data, multiplier=1.5)
    print(f"   Anomalies detected: {len(iqr_anomalies)}")
    print(f"   Anomaly indices: {[a.index for a in iqr_anomalies]}")
    
    # Moving Average Detection
    print("\n4. Moving Average Anomaly Detection:")
    ma_anomalies = StatisticalAnomalyDetector.detect_anomalies_moving_average(anomalous_data, window_size=10)
    print(f"   Anomalies detected: {len(ma_anomalies)}")
    
    # Machine Learning Detection
    print("\n5. Machine Learning Anomaly Detection:")
    ml_data = [[random.gauss(50, 5), random.gauss(30, 3)] for _ in range(100)]
    ml_data += [[100, 90], [5, 10], [120, 100]]  # Add anomalies
    
    if SKLEARN_AVAILABLE:
        ml_detector = MachineLearningAnomalyDetector()
        ml_detector.fit_isolation_forest(ml_data)
        ml_anomalies = ml_detector.predict(ml_data)
        print(f"   Isolation Forest anomalies: {len(ml_anomalies)}")
    else:
        print("   scikit-learn not available for ML methods")
    
    # DBSCAN Detection
    print("\n6. DBSCAN Clustering Anomaly Detection:")
    if SKLEARN_AVAILABLE:
        dbscan_anomalies = ClusteringAnomalyDetector.detect_anomalies_dbscan(ml_data)
        print(f"   DBSCAN anomalies: {len(dbscan_anomalies)}")
    else:
        print("   scikit-learn not available")
    
    # Time Series Detection
    print("\n7. Time Series Anomaly Detection:")
    ts_data = [math.sin(i * 0.1) * 10 + 50 for i in range(100)]
    ts_data[50] = 100  # Add anomaly
    ts_data[75] = 0   # Add anomaly
    
    seasonal_anomalies = TimeSeriesAnomalyDetector.detect_seasonal_anomalies(ts_data, period=20)
    print(f"   Seasonal anomalies: {len(seasonal_anomalies)}")
    
    trend_anomalies = TimeSeriesAnomalyDetector.detect_trend_anomalies(ts_data)
    print(f"   Trend anomalies: {len(trend_anomalies)}")
    
    # Multivariate Detection
    print("\n8. Multivariate Anomaly Detection:")
    mv_data = [[random.gauss(50, 5), random.gauss(30, 3)] for _ in range(100)]
    mv_data += [[100, 90], [5, 10]]
    
    if NUMPY_AVAILABLE:
        mv_anomalies = MultivariateAnomalyDetector.detect_anomalies_mahalanobis(mv_data)
        print(f"   Mahalanobis anomalies: {len(mv_anomalies)}")
    else:
        print("   numpy not available")
    
    # Autoencoder Detection
    print("\n9. Autoencoder Anomaly Detection:")
    ae_detector = AutoencoderAnomalyDetector(input_dim=2, encoding_dim=1)
    ae_detector.train(ml_data[:90])
    ae_anomalies = ae_detector.detect_anomalies(ml_data, threshold=15.0)
    print(f"   Autoencoder anomalies: {len(ae_anomalies)}")
    
    # Anomaly Scoring
    print("\n10. Anomaly Scoring:")
    if z_anomalies:
        normalized = AnomalyScorer.normalize_scores(z_anomalies)
        print(f"   Normalized scores: {[f'{a.score:.4f}' for a in normalized[:5]]}")
        
        top_k = AnomalyScorer.select_top_k(normalized, k=3)
        print(f"   Top 3 anomalies: {[a.index for a in top_k]}")
    
    # Ensemble Detection
    print("\n11. Ensemble Detection:")
    ensemble = AnomalyEnsemble([DetectionMethod.Z_SCORE, DetectionMethod.IQR])
    ensemble_anomalies = ensemble.detect(ml_data)
    print(f"   Ensemble anomalies: {len(ensemble_anomalies)}")
    
    print("\n=== Demonstration Complete ===")
    print("\nAnomaly Detection Best Practices:")
    print("- Choose appropriate method for your data type")
    print("- Normalize/standardize data before ML methods")
    print("- Use ensemble methods for robust detection")
    print("- Tune thresholds based on domain knowledge")
    print("- Consider false positive vs. false negative trade-offs")
    print("- Use time series methods for temporal data")
    print("- Consider multivariate methods for correlated features")
    print("- Validate anomalies with domain experts")
    print("- Monitor detection performance over time")
    print("- Use explainable AI for anomaly interpretation")
    print("- Handle concept drift in production")
    print("- Implement proper alerting and escalation")
    print("- Consider computational cost for real-time detection")


if __name__ == "__main__":
    demonstrate_anomaly_detection()
