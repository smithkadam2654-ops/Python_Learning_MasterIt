"""
Recommender Systems Module

This module provides comprehensive recommender system utilities including:
- User-based collaborative filtering
- Item-based collaborative filtering
- Matrix factorization
- Content-based filtering
- Hybrid recommendation
- Similarity metrics (cosine, Pearson, Jaccard)
- Recommendation evaluation
- Cold start handling
- Rating prediction
- Top-N recommendations

Note: This module uses numpy for numerical operations.
Install with: pip install numpy

All functions include comprehensive docstrings and type hints.
"""

import math
import random
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict


try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class RecommendationMethod(Enum):
    """Types of recommendation methods."""
    USER_BASED = "user_based"
    ITEM_BASED = "item_based"
    MATRIX_FACTORIZATION = "matrix_factorization"
    CONTENT_BASED = "content_based"
    HYBRID = "hybrid"


class SimilarityMetric(Enum):
    """Similarity metrics."""
    COSINE = "cosine"
    PEARSON = "pearson"
    JACCARD = "jaccard"
    EUCLIDEAN = "euclidean"


@dataclass
class Rating:
    """Rating data structure."""
    user_id: str
    item_id: str
    rating: float
    timestamp: float = 0.0
    
    def __post_init__(self):
        """Normalize rating."""
        self.rating = max(1.0, min(5.0, self.rating))


@dataclass
class Recommendation:
    """Recommendation data structure."""
    item_id: str
    predicted_rating: float
    confidence: float = 0.0
    reason: str = ""


class SimilarityCalculator:
    """Similarity calculation utilities."""
    
    @staticmethod
    def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two vectors."""
        # Get common items
        common_items = set(vec1.keys()) & set(vec2.keys())
        
        if not common_items:
            return 0.0
        
        # Calculate dot product
        dot_product = sum(vec1[item] * vec2[item] for item in common_items)
        
        # Calculate magnitudes
        mag1 = math.sqrt(sum(vec1[item] ** 2 for item in vec1))
        mag2 = math.sqrt(sum(vec2[item] ** 2 for item in vec2))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    @staticmethod
    def pearson_correlation(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate Pearson correlation coefficient."""
        common_items = set(vec1.keys()) & set(vec2.keys())
        
        if len(common_items) < 2:
            return 0.0
        
        # Calculate means
        mean1 = sum(vec1[item] for item in common_items) / len(common_items)
        mean2 = sum(vec2[item] for item in common_items) / len(common_items)
        
        # Calculate numerator and denominators
        numerator = sum((vec1[item] - mean1) * (vec2[item] - mean2) for item in common_items)
        
        sum1 = sum((vec1[item] - mean1) ** 2 for item in common_items)
        sum2 = sum((vec2[item] - mean2) ** 2 for item in common_items)
        
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    @staticmethod
    def jaccard_similarity(set1: set, set2: set) -> float:
        """Calculate Jaccard similarity between two sets."""
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    @staticmethod
    def euclidean_distance(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate Euclidean distance."""
        common_items = set(vec1.keys()) & set(vec2.keys())
        
        if not common_items:
            return float('inf')
        
        squared_diff = sum((vec1[item] - vec2[item]) ** 2 for item in common_items)
        return math.sqrt(squared_diff)


class UserBasedCollaborativeFiltering:
    """User-based collaborative filtering."""
    
    def __init__(self, similarity_metric: SimilarityMetric = SimilarityMetric.COSINE):
        """Initialize user-based CF."""
        self.similarity_metric = similarity_metric
        self.user_ratings: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.similarity_matrix: Dict[Tuple[str, str], float] = {}
    
    def add_rating(self, rating: Rating) -> None:
        """Add user rating."""
        self.user_ratings[rating.user_id][rating.item_id] = rating.rating
    
    def calculate_user_similarity(self, user1: str, user2: str) -> float:
        """Calculate similarity between two users."""
        key = (user1, user2)
        
        if key in self.similarity_matrix:
            return self.similarity_matrix[key]
        
        ratings1 = self.user_ratings.get(user1, {})
        ratings2 = self.user_ratings.get(user2, {})
        
        if self.similarity_metric == SimilarityMetric.COSINE:
            similarity = SimilarityCalculator.cosine_similarity(ratings1, ratings2)
        elif self.similarity_metric == SimilarityMetric.PEARSON:
            similarity = SimilarityCalculator.pearson_correlation(ratings1, ratings2)
        else:
            similarity = SimilarityCalculator.cosine_similarity(ratings1, ratings2)
        
        self.similarity_matrix[key] = similarity
        return similarity
    
    def find_similar_users(self, user_id: str, k: int = 10) -> List[Tuple[str, float]]:
        """Find k most similar users."""
        similarities = []
        
        for other_user in self.user_ratings:
            if other_user != user_id:
                similarity = self.calculate_user_similarity(user_id, other_user)
                similarities.append((other_user, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:k]
    
    def predict_rating(self, user_id: str, item_id: str, k: int = 10) -> float:
        """Predict rating for user-item pair."""
        # Get similar users who rated this item
        similar_users = self.find_similar_users(user_id, k)
        
        weighted_sum = 0.0
        similarity_sum = 0.0
        
        for similar_user, similarity in similar_users:
            if item_id in self.user_ratings.get(similar_user, {}):
                rating = self.user_ratings[similar_user][item_id]
                weighted_sum += similarity * rating
                similarity_sum += abs(similarity)
        
        if similarity_sum == 0:
            # Fallback to user's average rating
            user_ratings = self.user_ratings.get(user_id, {})
            if user_ratings:
                return sum(user_ratings.values()) / len(user_ratings)
            return 3.0  # Default rating
        
        return weighted_sum / similarity_sum
    
    def recommend(self, user_id: str, n: int = 10, k: int = 10) -> List[Recommendation]:
        """Generate top-N recommendations for user."""
        # Get items user hasn't rated
        user_rated_items = set(self.user_ratings.get(user_id, {}).keys())
        all_items = set()
        
        for ratings in self.user_ratings.values():
            all_items.update(ratings.keys())
        
        unrated_items = all_items - user_rated_items
        
        # Predict ratings for unrated items
        predictions = []
        
        for item_id in unrated_items:
            predicted_rating = self.predict_rating(user_id, item_id, k)
            predictions.append(Recommendation(
                item_id=item_id,
                predicted_rating=predicted_rating,
                confidence=0.5  # Simplified confidence
            ))
        
        # Sort by predicted rating
        predictions.sort(key=lambda x: x.predicted_rating, reverse=True)
        return predictions[:n]


class ItemBasedCollaborativeFiltering:
    """Item-based collaborative filtering."""
    
    def __init__(self, similarity_metric: SimilarityMetric = SimilarityMetric.COSINE):
        """Initialize item-based CF."""
        self.similarity_metric = similarity_metric
        self.item_ratings: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.similarity_matrix: Dict[Tuple[str, str], float] = {}
    
    def add_rating(self, rating: Rating) -> None:
        """Add user rating."""
        self.item_ratings[rating.item_id][rating.user_id] = rating.rating
    
    def calculate_item_similarity(self, item1: str, item2: str) -> float:
        """Calculate similarity between two items."""
        key = (item1, item2)
        
        if key in self.similarity_matrix:
            return self.similarity_matrix[key]
        
        ratings1 = self.item_ratings.get(item1, {})
        ratings2 = self.item_ratings.get(item2, {})
        
        if self.similarity_metric == SimilarityMetric.COSINE:
            similarity = SimilarityCalculator.cosine_similarity(ratings1, ratings2)
        elif self.similarity_metric == SimilarityMetric.PEARSON:
            similarity = SimilarityCalculator.pearson_correlation(ratings1, ratings2)
        else:
            similarity = SimilarityCalculator.cosine_similarity(ratings1, ratings2)
        
        self.similarity_matrix[key] = similarity
        return similarity
    
    def find_similar_items(self, item_id: str, k: int = 10) -> List[Tuple[str, float]]:
        """Find k most similar items."""
        similarities = []
        
        for other_item in self.item_ratings:
            if other_item != item_id:
                similarity = self.calculate_item_similarity(item_id, other_item)
                similarities.append((other_item, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:k]
    
    def predict_rating(self, user_id: str, item_id: str, k: int = 10) -> float:
        """Predict rating for user-item pair."""
        # Get user's ratings
        user_ratings = {}
        for item, ratings in self.item_ratings.items():
            if user_id in ratings:
                user_ratings[item] = ratings[user_id]
        
        if not user_ratings:
            return 3.0  # Default rating
        
        # Find similar items to target item
        similar_items = self.find_similar_items(item_id, k)
        
        weighted_sum = 0.0
        similarity_sum = 0.0
        
        for similar_item, similarity in similar_items:
            if similar_item in user_ratings:
                rating = user_ratings[similar_item]
                weighted_sum += similarity * rating
                similarity_sum += abs(similarity)
        
        if similarity_sum == 0:
            return sum(user_ratings.values()) / len(user_ratings)
        
        return weighted_sum / similarity_sum
    
    def recommend(self, user_id: str, n: int = 10, k: int = 10) -> List[Recommendation]:
        """Generate top-N recommendations for user."""
        # Get items user hasn't rated
        user_rated_items = set()
        for item, ratings in self.item_ratings.items():
            if user_id in ratings:
                user_rated_items.add(item)
        
        all_items = set(self.item_ratings.keys())
        unrated_items = all_items - user_rated_items
        
        # Predict ratings for unrated items
        predictions = []
        
        for item_id in unrated_items:
            predicted_rating = self.predict_rating(user_id, item_id, k)
            predictions.append(Recommendation(
                item_id=item_id,
                predicted_rating=predicted_rating,
                confidence=0.5
            ))
        
        predictions.sort(key=lambda x: x.predicted_rating, reverse=True)
        return predictions[:n]


class MatrixFactorization:
    """Matrix factorization using alternating least squares."""
    
    def __init__(self, num_factors: int = 10, learning_rate: float = 0.01,
                 regularization: float = 0.1, max_iterations: int = 100):
        """Initialize matrix factorization."""
        self.num_factors = num_factors
        self.learning_rate = learning_rate
        self.regularization = regularization
        self.max_iterations = max_iterations
        self.user_factors: Dict[str, List[float]] = {}
        self.item_factors: Dict[str, List[float]] = {}
        self.ratings: List[Rating] = []
    
    def add_rating(self, rating: Rating) -> None:
        """Add rating."""
        self.ratings.append(rating)
    
    def train(self) -> None:
        """Train matrix factorization model."""
        # Initialize factors
        users = set(r.user_id for r in self.ratings)
        items = set(r.item_id for r in self.ratings)
        
        for user_id in users:
            self.user_factors[user_id] = [random.random() for _ in range(self.num_factors)]
        
        for item_id in items:
            self.item_factors[item_id] = [random.random() for _ in range(self.num_factors)]
        
        # Alternating least squares
        for iteration in range(self.max_iterations):
            for rating in self.ratings:
                user_factors = self.user_factors[rating.user_id]
                item_factors = self.item_factors[rating.item_id]
                
                # Predict rating
                predicted = sum(u * i for u, i in zip(user_factors, item_factors))
                error = rating.rating - predicted
                
                # Update factors
                for i in range(self.num_factors):
                    self.user_factors[rating.user_id][i] += self.learning_rate * (
                        error * item_factors[i] - self.regularization * user_factors[i]
                    )
                    self.item_factors[rating.item_id][i] += self.learning_rate * (
                        error * user_factors[i] - self.regularization * item_factors[i]
                    )
    
    def predict_rating(self, user_id: str, item_id: str) -> float:
        """Predict rating."""
        if user_id not in self.user_factors or item_id not in self.item_factors:
            return 3.0  # Default rating
        
        user_factors = self.user_factors[user_id]
        item_factors = self.item_factors[item_id]
        
        predicted = sum(u * i for u, i in zip(user_factors, item_factors))
        return max(1.0, min(5.0, predicted))
    
    def recommend(self, user_id: str, n: int = 10) -> List[Recommendation]:
        """Generate top-N recommendations."""
        recommendations = []
        
        for item_id in self.item_factors:
            if item_id not in self.user_factors.get(user_id, {}):
                predicted = self.predict_rating(user_id, item_id)
                recommendations.append(Recommendation(
                    item_id=item_id,
                    predicted_rating=predicted,
                    confidence=0.5
                ))
        
        recommendations.sort(key=lambda x: x.predicted_rating, reverse=True)
        return recommendations[:n]


class ContentBasedFiltering:
    """Content-based filtering using item features."""
    
    def __init__(self):
        """Initialize content-based filtering."""
        self.item_features: Dict[str, Dict[str, float]] = {}
        self.user_profiles: Dict[str, Dict[str, float]] = {}
    
    def add_item_features(self, item_id: str, features: Dict[str, float]) -> None:
        """Add item features."""
        self.item_features[item_id] = features
    
    def add_rating(self, rating: Rating) -> None:
        """Add rating and update user profile."""
        # Update user profile based on item features
        if rating.item_id in self.item_features:
            features = self.item_features[rating.item_id]
            
            for feature, value in features.items():
                if feature not in self.user_profiles[rating.user_id]:
                    self.user_profiles[rating.user_id][feature] = 0.0
                
                # Weighted by rating
                self.user_profiles[rating.user_id][feature] += value * rating.rating
    
    def calculate_similarity(self, user_id: str, item_id: str) -> float:
        """Calculate similarity between user profile and item."""
        if user_id not in self.user_profiles or item_id not in self.item_features:
            return 0.0
        
        user_profile = self.user_profiles[user_id]
        item_features = self.item_features[item_id]
        
        return SimilarityCalculator.cosine_similarity(user_profile, item_features)
    
    def recommend(self, user_id: str, n: int = 10) -> List[Recommendation]:
        """Generate recommendations based on content."""
        recommendations = []
        
        for item_id in self.item_features:
            similarity = self.calculate_similarity(user_id, item_id)
            predicted_rating = 1.0 + similarity * 4.0  # Scale to 1-5
            
            recommendations.append(Recommendation(
                item_id=item_id,
                predicted_rating=predicted_rating,
                confidence=similarity
            ))
        
        recommendations.sort(key=lambda x: x.predicted_rating, reverse=True)
        return recommendations[:n]


class HybridRecommender:
    """Hybrid recommender combining multiple methods."""
    
    def __init__(self, methods: List[RecommendationMethod], weights: Optional[List[float]] = None):
        """Initialize hybrid recommender."""
        self.methods = methods
        self.weights = weights if weights else [1.0] * len(methods)
        
        self.user_cf = UserBasedCollaborativeFiltering()
        self.item_cf = ItemBasedCollaborativeFiltering()
        self.mf = MatrixFactorization()
        self.content_cf = ContentBasedFiltering()
    
    def add_rating(self, rating: Rating) -> None:
        """Add rating to all methods."""
        self.user_cf.add_rating(rating)
        self.item_cf.add_rating(rating)
        self.mf.add_rating(rating)
        self.content_cf.add_rating(rating)
    
    def train(self) -> None:
        """Train all methods."""
        self.mf.train()
    
    def recommend(self, user_id: str, n: int = 10) -> List[Recommendation]:
        """Generate hybrid recommendations."""
        all_recommendations = defaultdict(lambda: {"rating": 0.0, "confidence": 0.0, "count": 0})
        
        # Get recommendations from each method
        for method, weight in zip(self.methods, self.weights):
            if method == RecommendationMethod.USER_BASED:
                recs = self.user_cf.recommend(user_id, n)
            elif method == RecommendationMethod.ITEM_BASED:
                recs = self.item_cf.recommend(user_id, n)
            elif method == RecommendationMethod.MATRIX_FACTORIZATION:
                recs = self.mf.recommend(user_id, n)
            elif method == RecommendationMethod.CONTENT_BASED:
                recs = self.content_cf.recommend(user_id, n)
            else:
                continue
            
            for rec in recs:
                all_recommendations[rec.item_id]["rating"] += rec.predicted_rating * weight
                all_recommendations[rec.item_id]["confidence"] += rec.confidence * weight
                all_recommendations[rec.item_id]["count"] += 1
        
        # Average recommendations
        final_recommendations = []
        
        for item_id, data in all_recommendations.items():
            if data["count"] > 0:
                avg_rating = data["rating"] / data["count"]
                avg_confidence = data["confidence"] / data["count"]
                
                final_recommendations.append(Recommendation(
                    item_id=item_id,
                    predicted_rating=avg_rating,
                    confidence=avg_confidence
                ))
        
        final_recommendations.sort(key=lambda x: x.predicted_rating, reverse=True)
        return final_recommendations[:n]


class RecommendationEvaluator:
    """Recommendation evaluation utilities."""
    
    @staticmethod
    def calculate_mae(predictions: List[Tuple[float, float]]) -> float:
        """Calculate Mean Absolute Error."""
        if not predictions:
            return 0.0
        
        errors = [abs(pred - actual) for pred, actual in predictions]
        return sum(errors) / len(errors)
    
    @staticmethod
    def calculate_rmse(predictions: List[Tuple[float, float]]) -> float:
        """Calculate Root Mean Square Error."""
        if not predictions:
            return 0.0
        
        squared_errors = [(pred - actual) ** 2 for pred, actual in predictions]
        return math.sqrt(sum(squared_errors) / len(squared_errors))
    
    @staticmethod
    def calculate_precision_at_k(recommendations: List[str], relevant_items: set, k: int) -> float:
        """Calculate Precision@K."""
        if not recommendations:
            return 0.0
        
        top_k = recommendations[:k]
        relevant_in_top_k = len(set(top_k) & relevant_items)
        
        return relevant_in_top_k / k
    
    @staticmethod
    def calculate_recall_at_k(recommendations: List[str], relevant_items: set, k: int) -> float:
        """Calculate Recall@K."""
        if not relevant_items:
            return 0.0
        
        top_k = recommendations[:k]
        relevant_in_top_k = len(set(top_k) & relevant_items)
        
        return relevant_in_top_k / len(relevant_items)
    
    @staticmethod
    def calculate_ndcg(recommendations: List[str], relevant_items: set, k: int) -> float:
        """Calculate Normalized Discounted Cumulative Gain."""
        if not recommendations:
            return 0.0
        
        dcg = 0.0
        for i, item in enumerate(recommendations[:k]):
            if item in relevant_items:
                dcg += 1.0 / math.log2(i + 2)
        
        # Ideal DCG
        ideal_dcg = sum(1.0 / math.log2(i + 2) for i in range(min(k, len(relevant_items))))
        
        if ideal_dcg == 0:
            return 0.0
        
        return dcg / ideal_dcg


def demonstrate_recommender_systems():
    """Demonstrate recommender systems functionality."""
    print("=== Recommender Systems Demonstration ===\n")
    
    # Sample Data
    print("1. Sample Rating Data:")
    ratings = [
        Rating("user1", "item1", 5.0),
        Rating("user1", "item2", 3.0),
        Rating("user1", "item3", 4.0),
        Rating("user2", "item1", 4.0),
        Rating("user2", "item2", 5.0),
        Rating("user2", "item4", 2.0),
        Rating("user3", "item3", 5.0),
        Rating("user3", "item4", 4.0),
        Rating("user3", "item5", 3.0),
    ]
    
    print(f"   Total ratings: {len(ratings)}")
    
    # Similarity Calculation
    print("\n2. Similarity Calculation:")
    vec1 = {"item1": 5.0, "item2": 3.0, "item3": 4.0}
    vec2 = {"item1": 4.0, "item2": 5.0, "item4": 2.0}
    
    cosine_sim = SimilarityCalculator.cosine_similarity(vec1, vec2)
    pearson_sim = SimilarityCalculator.pearson_correlation(vec1, vec2)
    
    print(f"   Cosine similarity: {cosine_sim:.4f}")
    print(f"   Pearson correlation: {pearson_sim:.4f}")
    
    # User-Based CF
    print("\n3. User-Based Collaborative Filtering:")
    user_cf = UserBasedCollaborativeFiltering()
    
    for rating in ratings:
        user_cf.add_rating(rating)
    
    similar_users = user_cf.find_similar_users("user1", k=2)
    print(f"   Similar users to user1: {[(u, f'{s:.4f}') for u, s in similar_users]}")
    
    predicted = user_cf.predict_rating("user1", "item4")
    print(f"   Predicted rating for user1-item4: {predicted:.2f}")
    
    recommendations = user_cf.recommend("user1", n=3)
    print(f"   Recommendations: {[r.item_id for r in recommendations]}")
    
    # Item-Based CF
    print("\n4. Item-Based Collaborative Filtering:")
    item_cf = ItemBasedCollaborativeFiltering()
    
    for rating in ratings:
        item_cf.add_rating(rating)
    
    similar_items = item_cf.find_similar_items("item1", k=2)
    print(f"   Similar items to item1: {[(i, f'{s:.4f}') for i, s in similar_items]}")
    
    predicted = item_cf.predict_rating("user1", "item4")
    print(f"   Predicted rating for user1-item4: {predicted:.2f}")
    
    # Matrix Factorization
    print("\n5. Matrix Factorization:")
    mf = MatrixFactorization(num_factors=5, max_iterations=50)
    
    for rating in ratings:
        mf.add_rating(rating)
    
    mf.train()
    
    predicted = mf.predict_rating("user1", "item4")
    print(f"   Predicted rating for user1-item4: {predicted:.2f}")
    
    # Content-Based Filtering
    print("\n6. Content-Based Filtering:")
    content_cf = ContentBasedFiltering()
    
    content_cf.add_item_features("item1", {"action": 1.0, "drama": 0.5})
    content_cf.add_item_features("item2", {"comedy": 1.0, "romance": 0.8})
    content_cf.add_item_features("item3", {"action": 0.8, "thriller": 0.9})
    
    for rating in ratings:
        content_cf.add_rating(rating)
    
    similarity = content_cf.calculate_similarity("user1", "item1")
    print(f"   User-item similarity: {similarity:.4f}")
    
    # Hybrid Recommender
    print("\n7. Hybrid Recommender:")
    hybrid = HybridRecommender(
        [RecommendationMethod.USER_BASED, RecommendationMethod.ITEM_BASED],
        weights=[0.6, 0.4]
    )
    
    for rating in ratings:
        hybrid.add_rating(rating)
    
    hybrid_recommendations = hybrid.recommend("user1", n=3)
    print(f"   Hybrid recommendations: {[r.item_id for r in hybrid_recommendations]}")
    
    # Evaluation
    print("\n8. Recommendation Evaluation:")
    predictions = [(4.5, 5.0), (3.2, 3.0), (4.8, 4.0)]
    
    mae = RecommendationEvaluator.calculate_mae(predictions)
    rmse = RecommendationEvaluator.calculate_rmse(predictions)
    
    print(f"   MAE: {mae:.4f}")
    print(f"   RMSE: {rmse:.4f}")
    
    recommendations_list = ["item1", "item2", "item3", "item4"]
    relevant = {"item1", "item3"}
    
    precision = RecommendationEvaluator.calculate_precision_at_k(recommendations_list, relevant, 3)
    recall = RecommendationEvaluator.calculate_recall_at_k(recommendations_list, relevant, 3)
    ndcg = RecommendationEvaluator.calculate_ndcg(recommendations_list, relevant, 3)
    
    print(f"   Precision@3: {precision:.4f}")
    print(f"   Recall@3: {recall:.4f}")
    print(f"   NDCG@3: {ndcg:.4f}")
    
    print("\n=== Demonstration Complete ===")
    print("\nRecommender Systems Best Practices:")
    print("- Choose appropriate algorithm for your data")
    print("- Handle cold start problems carefully")
    print("- Use hybrid methods for better accuracy")
    print("- Consider scalability for large datasets")
    print("- Evaluate using multiple metrics")
    print("- Handle sparse data appropriately")
    print("- Consider real-time vs. batch recommendations")
    print("- Use appropriate similarity metrics")
    print("- Implement proper evaluation protocols")
    print("- Consider user feedback and implicit signals")
    print("- Handle diversity and novelty in recommendations")
    print("- Update models regularly with new data")
    print("- Consider A/B testing for algorithm selection")


if __name__ == "__main__":
    demonstrate_recommender_systems()
