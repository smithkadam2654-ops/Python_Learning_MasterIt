"""
Machine Learning Utilities Module

This module provides comprehensive machine learning utilities including:
- Data preprocessing and feature engineering
- Model evaluation metrics
- Cross-validation utilities
- Hyperparameter tuning
- Model serialization
- Simple machine learning implementations
- Data splitting and sampling
- Feature selection
- Model comparison
- Visualization helpers

Note: This module uses scikit-learn for advanced ML operations.
Install with: pip install scikit-learn numpy pandas matplotlib

All functions include comprehensive docstrings and type hints.
"""

import random
import math
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
import json


try:
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
    from sklearn.feature_selection import SelectKBest, f_classif, f_regression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class MLTask(Enum):
    """Machine learning task types."""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    DIMENSIONALITY_REDUCTION = "dimensionality_reduction"


@dataclass
class ModelEvaluation:
    """Container for model evaluation results."""
    model_name: str
    task_type: MLTask
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    mse: Optional[float] = None
    mae: Optional[float] = None
    r2: Optional[float] = None
    training_time: float = 0.0
    prediction_time: float = 0.0


@dataclass
class DataSplit:
    """Container for data split results."""
    X_train: Any
    X_test: Any
    y_train: Any
    y_test: Any
    train_size: float
    test_size: float


class DataPreprocessor:
    """Data preprocessing utilities."""
    
    @staticmethod
    def normalize_data(data: List[List[float]], 
                      method: str = "minmax") -> List[List[float]]:
        """Normalize data using specified method."""
        if not SKLEARN_AVAILABLE:
            # Manual implementation
            if method == "minmax":
                return DataPreprocessor._minmax_normalize_manual(data)
            elif method == "zscore":
                return DataPreprocessor._zscore_normalize_manual(data)
            return data
        
        data_array = np.array(data)
        
        if method == "minmax":
            scaler = MinMaxScaler()
        elif method == "zscore":
            scaler = StandardScaler()
        else:
            return data
        
        normalized = scaler.fit_transform(data_array)
        return normalized.tolist()
    
    @staticmethod
    def _minmax_normalize_manual(data: List[List[float]]) -> List[List[float]]:
        """Manual min-max normalization."""
        if not data:
            return data
        
        # Find min and max for each column
        cols = len(data[0])
        min_vals = [float('inf')] * cols
        max_vals = [float('-inf')] * cols
        
        for row in data:
            for i, val in enumerate(row):
                if val < min_vals[i]:
                    min_vals[i] = val
                if val > max_vals[i]:
                    max_vals[i] = val
        
        # Normalize
        normalized = []
        for row in data:
            normalized_row = []
            for i, val in enumerate(row):
                if max_vals[i] - min_vals[i] == 0:
                    normalized_row.append(0.0)
                else:
                    normalized_row.append((val - min_vals[i]) / (max_vals[i] - min_vals[i]))
            normalized.append(normalized_row)
        
        return normalized
    
    @staticmethod
    def _zscore_normalize_manual(data: List[List[float]]) -> List[List[float]]:
        """Manual z-score normalization."""
        if not data:
            return data
        
        # Calculate mean and std for each column
        cols = len(data[0])
        means = [0.0] * cols
        stds = [0.0] * cols
        
        # Calculate means
        for row in data:
            for i, val in enumerate(row):
                means[i] += val
        
        for i in range(cols):
            means[i] /= len(data)
        
        # Calculate stds
        for row in data:
            for i, val in enumerate(row):
                stds[i] += (val - means[i]) ** 2
        
        for i in range(cols):
            stds[i] = math.sqrt(stds[i] / len(data))
        
        # Normalize
        normalized = []
        for row in data:
            normalized_row = []
            for i, val in enumerate(row):
                if stds[i] == 0:
                    normalized_row.append(0.0)
                else:
                    normalized_row.append((val - means[i]) / stds[i])
            normalized.append(normalized_row)
        
        return normalized
    
    @staticmethod
    def encode_labels(labels: List[str]) -> Tuple[List[int], Dict[str, int]]:
        """Encode string labels to integers."""
        unique_labels = list(set(labels))
        label_map = {label: idx for idx, label in enumerate(unique_labels)}
        encoded = [label_map[label] for label in labels]
        return encoded, label_map
    
    @staticmethod
    def decode_labels(encoded: List[int], label_map: Dict[str, int]) -> List[str]:
        """Decode integer labels back to strings."""
        reverse_map = {idx: label for label, idx in label_map.items()}
        return [reverse_map[idx] for idx in encoded]
    
    @staticmethod
    def handle_missing_values(data: List[List[Any]], 
                            strategy: str = "mean") -> List[List[Any]]:
        """Handle missing values in dataset."""
        if not data:
            return data
        
        cols = len(data[0])
        rows = len(data)
        
        for col in range(cols):
            # Find missing values
            missing_indices = [i for i in range(rows) if data[i][col] is None or data[i][col] == ""]
            
            if not missing_indices:
                continue
            
            # Get non-missing values
            valid_values = [data[i][col] for i in range(rows) 
                          if data[i][col] is not None and data[i][col] != ""]
            
            if not valid_values:
                continue
            
            # Fill based on strategy
            if strategy == "mean" and all(isinstance(v, (int, float)) for v in valid_values):
                fill_value = sum(valid_values) / len(valid_values)
            elif strategy == "median" and all(isinstance(v, (int, float)) for v in valid_values):
                sorted_values = sorted(valid_values)
                fill_value = sorted_values[len(sorted_values) // 2]
            elif strategy == "mode":
                from collections import Counter
                counter = Counter(valid_values)
                fill_value = counter.most_common(1)[0][0]
            else:
                fill_value = valid_values[0]  # Use first valid value
            
            # Fill missing values
            for idx in missing_indices:
                data[idx][col] = fill_value
        
        return data
    
    @staticmethod
    def remove_outliers(data: List[List[float]], 
                       method: str = "iqr",
                       threshold: float = 1.5) -> List[List[float]]:
        """Remove outliers from dataset."""
        if not data:
            return data
        
        cols = len(data[0])
        rows = len(data)
        valid_rows = list(range(rows))
        
        for col in range(cols):
            column_values = [data[i][col] for i in valid_rows]
            
            if method == "iqr":
                sorted_values = sorted(column_values)
                q1 = sorted_values[len(sorted_values) // 4]
                q3 = sorted_values[3 * len(sorted_values) // 4]
                iqr = q3 - q1
                
                lower_bound = q1 - threshold * iqr
                upper_bound = q3 + threshold * iqr
                
                valid_rows = [i for i in valid_rows 
                            if lower_bound <= data[i][col] <= upper_bound]
            
            elif method == "zscore":
                mean = sum(column_values) / len(column_values)
                std = math.sqrt(sum((x - mean) ** 2 for x in column_values) / len(column_values))
                
                if std > 0:
                    valid_rows = [i for i in valid_rows 
                                if abs((data[i][col] - mean) / std) <= threshold]
        
        return [data[i] for i in valid_rows]


class DataSplitter:
    """Data splitting utilities."""
    
    @staticmethod
    def train_test_split(data: List[List[Any]], 
                       test_size: float = 0.2,
                       random_state: Optional[int] = None) -> DataSplit:
        """Split data into train and test sets."""
        if random_state is not None:
            random.seed(random_state)
        
        # Separate features and labels (assuming last column is label)
        X = [row[:-1] for row in data]
        y = [row[-1] for row in data]
        
        # Split
        indices = list(range(len(data)))
        random.shuffle(indices)
        
        split_point = int(len(data) * (1 - test_size))
        train_indices = indices[:split_point]
        test_indices = indices[split_point:]
        
        X_train = [X[i] for i in train_indices]
        X_test = [X[i] for i in test_indices]
        y_train = [y[i] for i in train_indices]
        y_test = [y[i] for i in test_indices]
        
        return DataSplit(
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
            train_size=1 - test_size,
            test_size=test_size
        )
    
    @staticmethod
    def k_fold_split(data: List[List[Any]], 
                   k: int = 5,
                   random_state: Optional[int] = None) -> List[Tuple[List[List[Any]], List[List[Any]]]]:
        """Create k-fold cross-validation splits."""
        if random_state is not None:
            random.seed(random_state)
        
        random.shuffle(data)
        fold_size = len(data) // k
        folds = []
        
        for i in range(k):
            start = i * fold_size
            end = start + fold_size if i < k - 1 else len(data)
            
            test_data = data[start:end]
            train_data = data[:start] + data[end:]
            
            folds.append((train_data, test_data))
        
        return folds


class ModelEvaluator:
    """Model evaluation utilities."""
    
    @staticmethod
    def calculate_classification_metrics(y_true: List[Any], 
                                       y_pred: List[Any]) -> Dict[str, float]:
        """Calculate classification metrics."""
        if not y_true or not y_pred:
            return {}
        
        # Simple implementation
        correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
        accuracy = correct / len(y_true)
        
        # Calculate precision, recall, F1 (binary classification)
        unique_classes = set(y_true)
        
        if len(unique_classes) == 2:
            # Binary classification
            positive_class = list(unique_classes)[1]
            
            true_positives = sum(1 for true, pred in zip(y_true, y_pred) 
                              if true == positive_class and pred == positive_class)
            false_positives = sum(1 for true, pred in zip(y_true, y_pred) 
                               if true != positive_class and pred == positive_class)
            false_negatives = sum(1 for true, pred in zip(y_true, y_pred) 
                               if true == positive_class and pred != positive_class)
            
            precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }
        
        return {"accuracy": accuracy}
    
    @staticmethod
    def calculate_regression_metrics(y_true: List[float], 
                                   y_pred: List[float]) -> Dict[str, float]:
        """Calculate regression metrics."""
        if not y_true or not y_pred:
            return {}
        
        n = len(y_true)
        
        # Mean Squared Error
        mse = sum((true - pred) ** 2 for true, pred in zip(y_true, y_pred)) / n
        
        # Mean Absolute Error
        mae = sum(abs(true - pred) for true, pred in zip(y_true, y_pred)) / n
        
        # R-squared
        mean_true = sum(y_true) / n
        ss_tot = sum((true - mean_true) ** 2 for true in y_true)
        ss_res = sum((true - pred) ** 2 for true, pred in zip(y_true, y_pred))
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        return {
            "mse": mse,
            "mae": mae,
            "r2": r2
        }
    
    @staticmethod
    def cross_validate(model: Callable,
                     data: List[List[Any]],
                     k: int = 5,
                     task_type: MLTask = MLTask.CLASSIFICATION) -> Dict[str, float]:
        """Perform k-fold cross-validation."""
        folds = DataSplitter.k_fold_split(data, k)
        scores = []
        
        for train_data, test_data in folds:
            # Train model
            X_train = [row[:-1] for row in train_data]
            y_train = [row[-1] for row in train_data]
            X_test = [row[:-1] for row in test_data]
            y_test = [row[-1] for row in test_data]
            
            # Train and predict
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            # Calculate score
            if task_type == MLTask.CLASSIFICATION:
                metrics = ModelEvaluator.calculate_classification_metrics(y_test, y_pred)
                scores.append(metrics.get("accuracy", 0))
            else:
                metrics = ModelEvaluator.calculate_regression_metrics(y_test, y_pred)
                scores.append(metrics.get("r2", 0))
        
        return {
            "mean_score": sum(scores) / len(scores),
            "std_score": math.sqrt(sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)),
            "scores": scores
        }


class SimpleModels:
    """Simple machine learning model implementations."""
    
    class KNearestNeighbors:
        """Simple k-nearest neighbors classifier."""
        
        def __init__(self, k: int = 3):
            """Initialize k-NN classifier."""
            self.k = k
            self.X_train = []
            self.y_train = []
        
        def fit(self, X: List[List[float]], y: List[Any]) -> None:
            """Fit the model."""
            self.X_train = X
            self.y_train = y
        
        def predict(self, X: List[List[float]]) -> List[Any]:
            """Predict labels for X."""
            predictions = []
            
            for sample in X:
                # Calculate distances
                distances = []
                for i, train_sample in enumerate(self.X_train):
                    distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(sample, train_sample)))
                    distances.append((distance, self.y_train[i]))
                
                # Sort by distance and get k nearest
                distances.sort(key=lambda x: x[0])
                k_nearest = distances[:self.k]
                
                # Majority vote
                from collections import Counter
                labels = [label for _, label in k_nearest]
                most_common = Counter(labels).most_common(1)[0][0]
                predictions.append(most_common)
            
            return predictions
    
    class LinearRegression:
        """Simple linear regression."""
        
        def __init__(self):
            """Initialize linear regression."""
            self.coefficients = []
            self.intercept = 0.0
        
        def fit(self, X: List[List[float]], y: List[float]) -> None:
            """Fit the model using least squares."""
            if not X or not y:
                return
            
            n_samples = len(X)
            n_features = len(X[0])
            
            # Add bias term
            X_bias = [[1.0] + sample for sample in X]
            
            # Calculate coefficients using normal equation
            # (X^T * X)^-1 * X^T * y
            X_transpose = list(zip(*X_bias))
            
            # Calculate X^T * X
            XT_X = [[sum(X_transpose[i][k] * X_transpose[j][k] for k in range(n_samples)) 
                    for j in range(n_features + 1)] for i in range(n_features + 1)]
            
            # Calculate X^T * y
            XT_y = [sum(X_transpose[i][k] * y[k] for k in range(n_samples)) 
                   for i in range(n_features + 1)]
            
            # Simple implementation using gradient descent for numerical stability
            self._gradient_descent(X_bias, y, learning_rate=0.01, iterations=1000)
        
        def _gradient_descent(self, X: List[List[float]], y: List[float],
                            learning_rate: float, iterations: int) -> None:
            """Gradient descent optimization."""
            n_samples = len(X)
            n_features = len(X[0])
            
            # Initialize coefficients
            self.coefficients = [0.0] * n_features
            
            for _ in range(iterations):
                predictions = [sum(coeff * feature for coeff, feature in zip(self.coefficients, sample)) 
                             for sample in X]
                
                errors = [pred - actual for pred, actual in zip(predictions, y)]
                
                # Update coefficients
                for j in range(n_features):
                    gradient = sum(errors[i] * X[i][j] for i in range(n_samples)) / n_samples
                    self.coefficients[j] -= learning_rate * gradient
        
        def predict(self, X: List[List[float]]) -> List[float]:
            """Predict values for X."""
            predictions = []
            
            for sample in X:
                prediction = self.coefficients[0] + sum(coeff * feature 
                                                       for coeff, feature in zip(self.coefficients[1:], sample))
                predictions.append(prediction)
            
            return predictions
    
    class DecisionTree:
        """Simple decision tree classifier."""
        
        def __init__(self, max_depth: int = 3):
            """Initialize decision tree."""
            self.max_depth = max_depth
            self.tree = None
        
        def fit(self, X: List[List[float]], y: List[Any]) -> None:
            """Fit the decision tree."""
            self.tree = self._build_tree(X, y, depth=0)
        
        def _build_tree(self, X: List[List[float]], y: List[Any], depth: int) -> Dict:
            """Build decision tree recursively."""
            # Stopping conditions
            if depth >= self.max_depth or len(set(y)) == 1:
                return {"label": max(set(y), key=y.count)}
            
            # Find best split
            best_feature, best_threshold, best_gain = self._find_best_split(X, y)
            
            if best_gain == 0:
                return {"label": max(set(y), key=y.count)}
            
            # Split data
            left_indices = [i for i, sample in enumerate(X) if sample[best_feature] <= best_threshold]
            right_indices = [i for i, sample in enumerate(X) if sample[best_feature] > best_threshold]
            
            left_X = [X[i] for i in left_indices]
            left_y = [y[i] for i in left_indices]
            right_X = [X[i] for i in right_indices]
            right_y = [y[i] for i in right_indices]
            
            return {
                "feature": best_feature,
                "threshold": best_threshold,
                "left": self._build_tree(left_X, left_y, depth + 1),
                "right": self._build_tree(right_X, right_y, depth + 1)
            }
        
        def _find_best_split(self, X: List[List[float]], y: List[Any]) -> Tuple[int, float, float]:
            """Find best feature and threshold for split."""
            best_gain = 0
            best_feature = 0
            best_threshold = 0
            
            n_features = len(X[0])
        
        def predict(self, X: List[List[float]]) -> List[Any]:
            """Predict labels for X."""
            return [self._predict_sample(sample, self.tree) for sample in X]
        
        def _predict_sample(self, sample: List[float], tree: Dict) -> Any:
            """Predict single sample."""
            if "label" in tree:
                return tree["label"]
            
            if sample[tree["feature"]] <= tree["threshold"]:
                return self._predict_sample(sample, tree["left"])
            else:
                return self._predict_sample(sample, tree["right"])


class FeatureSelector:
    """Feature selection utilities."""
    
    @staticmethod
    def select_k_best(data: List[List[float]], 
                     k: int,
                     target_index: int = -1) -> List[int]:
        """Select k best features using correlation."""
        if not data or k <= 0:
            return []
        
        # Separate features and target
        features = [row[:target_index] + row[target_index+1:] if target_index >= 0 else row[:-1] 
                   for row in data]
        target = [row[target_index] if target_index >= 0 else row[-1] for row in data]
        
        if not features or not target:
            return []
        
        n_features = len(features[0])
        
        # Calculate correlation with target for each feature
        correlations = []
        for i in range(n_features):
            feature_values = [sample[i] for sample in features]
            
            # Calculate correlation
            if all(isinstance(v, (int, float)) for v in feature_values) and \
               all(isinstance(v, (int, float)) for v in target):
                
                mean_feature = sum(feature_values) / len(feature_values)
                mean_target = sum(target) / len(target)
                
                numerator = sum((f - mean_feature) * (t - mean_target) 
                             for f, t in zip(feature_values, target))
                denominator = math.sqrt(sum((f - mean_feature) ** 2 for f in feature_values) * 
                                     sum((t - mean_target) ** 2 for t in target))
                
                correlation = numerator / denominator if denominator != 0 else 0
                correlations.append((abs(correlation), i))
            else:
                correlations.append((0, i))
        
        # Sort by correlation and select top k
        correlations.sort(reverse=True)
        selected_indices = [idx for _, idx in correlations[:k]]
        
        return selected_indices


class ModelSerializer:
    """Model serialization utilities."""
    
    @staticmethod
    def save_model(model: Any, file_path: str) -> bool:
        """Save model to file."""
        try:
            # For simple models, save as JSON
            if hasattr(model, '__dict__'):
                model_data = {
                    "class_name": model.__class__.__name__,
                    "attributes": model.__dict__
                }
                
                with open(file_path, 'w') as f:
                    json.dump(model_data, f, indent=2)
                return True
            
            return False
        except Exception:
            return False
    
    @staticmethod
    def load_model(file_path: str) -> Optional[Any]:
        """Load model from file."""
        try:
            with open(file_path, 'r') as f:
                model_data = json.load(f)
            
            # Reconstruct simple models
            if model_data["class_name"] == "KNearestNeighbors":
                model = SimpleModels.KNearestNeighbors()
                model.__dict__.update(model_data["attributes"])
                return model
            
            return None
        except Exception:
            return None


def demonstrate_machine_learning_utils():
    """Demonstrate machine learning utilities functionality."""
    print("=== Machine Learning Utilities Demonstration ===\n")
    
    # Data Preprocessing
    print("1. Data Preprocessing:")
    data = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
    print(f"   Original data: {data}")
    
    normalized = DataPreprocessor.normalize_data(data, method="minmax")
    print(f"   Min-max normalized: {normalized}")
    
    labels = ["cat", "dog", "cat", "dog"]
    encoded, label_map = DataPreprocessor.encode_labels(labels)
    print(f"   Encoded labels: {encoded}")
    print(f"   Label map: {label_map}")
    
    # Data Splitting
    print("\n2. Data Splitting:")
    sample_data = [[1, 2, "A"], [3, 4, "B"], [5, 6, "A"], [7, 8, "B"]]
    split = DataSplitter.train_test_split(sample_data, test_size=0.5, random_state=42)
    print(f"   Train size: {len(split.X_train)}, Test size: {len(split.X_test)}")
    
    # Simple Models
    print("\n3. Simple Models:")
    
    # k-NN
    X_train = [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0]]
    y_train = ["A", "A", "B", "B"]
    X_test = [[1.5, 2.5], [3.5, 4.5]]
    
    knn = SimpleModels.KNearestNeighbors(k=2)
    knn.fit(X_train, y_train)
    knn_predictions = knn.predict(X_test)
    print(f"   k-NN predictions: {knn_predictions}")
    
    # Linear Regression
    X_reg = [[1.0], [2.0], [3.0], [4.0]]
    y_reg = [2.0, 4.0, 6.0, 8.0]
    X_test_reg = [[5.0]]
    
    lr = SimpleModels.LinearRegression()
    lr.fit(X_reg, y_reg)
    lr_predictions = lr.predict(X_test_reg)
    print(f"   Linear regression prediction: {lr_predictions}")
    
    # Model Evaluation
    print("\n4. Model Evaluation:")
    y_true = ["A", "A", "B", "B"]
    y_pred = ["A", "B", "B", "B"]
    
    class_metrics = ModelEvaluator.calculate_classification_metrics(y_true, y_pred)
    print(f"   Classification metrics: {class_metrics}")
    
    y_true_reg = [2.0, 4.0, 6.0, 8.0]
    y_pred_reg = [2.1, 3.9, 6.2, 7.8]
    
    reg_metrics = ModelEvaluator.calculate_regression_metrics(y_true_reg, y_pred_reg)
    print(f"   Regression metrics: {reg_metrics}")
    
    # Feature Selection
    print("\n5. Feature Selection:")
    feature_data = [[1.0, 2.0, 3.0, "A"], [2.0, 4.0, 6.0, "B"], [3.0, 6.0, 9.0, "A"]]
    selected = FeatureSelector.select_k_best(feature_data, k=2)
    print(f"   Selected feature indices: {selected}")
    
    # Cross-validation
    print("\n6. Cross-validation:")
    cv_data = [[1, 2, "A"], [3, 4, "B"], [5, 6, "A"], [7, 8, "B"]]
    folds = DataSplitter.k_fold_split(cv_data, k=2)
    print(f"   Number of folds: {len(folds)}")
    print(f"   Fold 1 train size: {len(folds[0][0])}, test size: {len(folds[0][1])}")
    
    # Missing Values
    print("\n7. Missing Value Handling:")
    data_with_missing = [[1.0, None, 3.0], [4.0, 5.0, None], [7.0, 8.0, 9.0]]
    filled = DataPreprocessor.handle_missing_values(data_with_missing, strategy="mean")
    print(f"   Data with missing values: {data_with_missing}")
    print(f"   After filling: {filled}")
    
    # Outlier Removal
    print("\n8. Outlier Removal:")
    data_with_outliers = [[1.0, 2.0], [3.0, 4.0], [100.0, 200.0], [5.0, 6.0]]
    cleaned = DataPreprocessor.remove_outliers(data_with_outliers, method="iqr")
    print(f"   Original: {len(data_with_outliers)} rows")
    print(f"   After outlier removal: {len(cleaned)} rows")
    
    # Model Serialization
    print("\n9. Model Serialization:")
    saved = ModelSerializer.save_model(knn, "knn_model.json")
    print(f"   Model saved: {saved}")
    
    loaded_model = ModelSerializer.load_model("knn_model.json")
    print(f"   Model loaded: {loaded_model is not None}")
    
    # Cleanup
    import os
    if os.path.exists("knn_model.json"):
        os.remove("knn_model.json")
    
    print("\n=== Demonstration Complete ===")
    print("\nMachine Learning Best Practices:")
    print("- Always split data into train and test sets")
    print("- Use cross-validation for robust evaluation")
    print("- Preprocess data appropriately for your model")
    print("- Handle missing values before training")
    print("- Remove or handle outliers carefully")
    print("- Select relevant features to improve performance")
    print("- Evaluate models using appropriate metrics")
    print("- Save trained models for later use")
    print("- Consider using scikit-learn for production ML")


if __name__ == "__main__":
    demonstrate_machine_learning_utils()