"""
Natural Language Processing Module

This module provides comprehensive NLP utilities including:
- Text preprocessing and tokenization
- Sentiment analysis
- Text classification
- Named entity recognition
- Text similarity and distance
- Keyword extraction
- Text summarization
- Language detection
- Text generation helpers
- Feature extraction for ML

Note: This module uses NLTK and spaCy for advanced NLP operations.
Install with: pip install nltk spacy textblob

All functions include comprehensive docstrings and type hints.
"""

import re
import math
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from collections import Counter, defaultdict


try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    from nltk.tag import pos_tag
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False


try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False


class Language(Enum):
    """Supported languages."""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"
    JAPANESE = "ja"


@dataclass
class SentimentResult:
    """Container for sentiment analysis results."""
    polarity: float  # -1 to 1 (negative to positive)
    subjectivity: float  # 0 to 1 (objective to subjective)
    label: str  # "positive", "negative", "neutral"
    confidence: float


@dataclass
class TextClassification:
    """Container for text classification results."""
    label: str
    confidence: float
    probabilities: Dict[str, float]


class TextPreprocessor:
    """Text preprocessing utilities."""
    
    def __init__(self, language: Language = Language.ENGLISH):
        """Initialize text preprocessor."""
        self.language = language
        self.stemmer = PorterStemmer() if NLTK_AVAILABLE else None
        self.lemmatizer = WordNetLemmatizer() if NLTK_AVAILABLE else None
        self.stop_words = self._get_stop_words()
    
    def _get_stop_words(self) -> set:
        """Get stop words for the language."""
        if NLTK_AVAILABLE:
            try:
                return set(stopwords.words(self.language.value))
            except:
                return set()
        return set()
    
    def clean_text(self, text: str) -> str:
        """Clean text by removing special characters and extra spaces."""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,!?;:]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        if NLTK_AVAILABLE:
            try:
                return word_tokenize(text)
            except:
                pass
        
        # Fallback to simple tokenization
        return re.findall(r'\b\w+\b', text.lower())
    
    def sentence_tokenize(self, text: str) -> List[str]:
        """Tokenize text into sentences."""
        if NLTK_AVAILABLE:
            try:
                return sent_tokenize(text)
            except:
                pass
        
        # Fallback to simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        """Remove stop words from tokens."""
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Apply stemming to tokens."""
        if self.stemmer:
            return [self.stemmer.stem(token) for token in tokens]
        return tokens
    
    def lemmatize_tokens(self, tokens: List[str]) -> List[str]:
        """Apply lemmatization to tokens."""
        if self.lemmatizer:
            return [self.lemmatizer.lemmatize(token) for token in tokens]
        return tokens
    
    def preprocess_pipeline(self, text: str, 
                          clean: bool = True,
                          tokenize: bool = True,
                          remove_stopwords: bool = True,
                          stem: bool = False,
                          lemmatize: bool = True) -> Union[str, List[str]]:
        """Apply complete preprocessing pipeline."""
        if clean:
            text = self.clean_text(text)
        
        if tokenize:
            tokens = self.tokenize(text)
            
            if remove_stopwords:
                tokens = self.remove_stop_words(tokens)
            
            if stem:
                tokens = self.stem_tokens(tokens)
            
            if lemmatize:
                tokens = self.lemmatize_tokens(tokens)
            
            return tokens
        
        return text


class SentimentAnalyzer:
    """Sentiment analysis utilities."""
    
    def __init__(self):
        """Initialize sentiment analyzer."""
        self.positive_words = {
            "good", "great", "excellent", "amazing", "wonderful", "fantastic",
            "positive", "happy", "joy", "love", "like", "best", "beautiful",
            "awesome", "brilliant", "perfect", "superb", "outstanding"
        }
        
        self.negative_words = {
            "bad", "terrible", "awful", "horrible", "poor", "negative",
            "sad", "hate", "dislike", "worst", "ugly", "awful", "dreadful",
            "disappointing", "disappointed", "frustrating", "frustrated"
        }
    
    def analyze_sentiment(self, text: str) -> SentimentResult:
        """Analyze sentiment of text."""
        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity
                
                if polarity > 0.1:
                    label = "positive"
                elif polarity < -0.1:
                    label = "negative"
                else:
                    label = "neutral"
                
                confidence = abs(polarity)
                
                return SentimentResult(
                    polarity=polarity,
                    subjectivity=subjectivity,
                    label=label,
                    confidence=confidence
                )
            except:
                pass
        
        # Fallback to word-based analysis
        return self._word_based_sentiment(text)
    
    def _word_based_sentiment(self, text: str) -> SentimentResult:
        """Word-based sentiment analysis (fallback)."""
        tokens = re.findall(r'\b\w+\b', text.lower())
        
        positive_count = sum(1 for token in tokens if token in self.positive_words)
        negative_count = sum(1 for token in tokens if token in self.negative_words)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            polarity = 0.0
            label = "neutral"
            confidence = 0.0
        else:
            polarity = (positive_count - negative_count) / total_sentiment_words
            confidence = total_sentiment_words / len(tokens) if tokens else 0
            
            if polarity > 0.1:
                label = "positive"
            elif polarity < -0.1:
                label = "negative"
            else:
                label = "neutral"
        
        return SentimentResult(
            polarity=polarity,
            subjectivity=0.5,  # Placeholder
            label=label,
            confidence=confidence
        )
    
    def batch_analyze(self, texts: List[str]) -> List[SentimentResult]:
        """Analyze sentiment for multiple texts."""
        return [self.analyze_sentiment(text) for text in texts]


class TextClassifier:
    """Simple text classification using keyword matching."""
    
    def __init__(self):
        """Initialize text classifier."""
        self.categories: Dict[str, set] = {}
    
    def add_category(self, category: str, keywords: List[str]) -> None:
        """Add category with keywords."""
        self.categories[category] = set(keyword.lower() for keyword in keywords)
    
    def classify(self, text: str) -> TextClassification:
        """Classify text into categories."""
        tokens = set(re.findall(r'\b\w+\b', text.lower()))
        
        scores = {}
        for category, keywords in self.categories.items():
            matches = len(tokens & keywords)
            scores[category] = matches
        
        if not scores:
            return TextClassification(
                label="unknown",
                confidence=0.0,
                probabilities={}
            )
        
        # Find best match
        max_score = max(scores.values())
        best_category = max(scores, key=scores.get)
        
        # Calculate confidence
        total_tokens = len(tokens)
        confidence = max_score / total_tokens if total_tokens > 0 else 0
        
        # Calculate probabilities
        total_matches = sum(scores.values())
        probabilities = {
            cat: (score / total_matches if total_matches > 0 else 0)
            for cat, score in scores.items()
        }
        
        return TextClassification(
            label=best_category,
            confidence=confidence,
            probabilities=probabilities
        )


class TextSimilarity:
    """Text similarity and distance metrics."""
    
    @staticmethod
    def jaccard_similarity(text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two texts."""
        tokens1 = set(re.findall(r'\b\w+\b', text1.lower()))
        tokens2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        
        return intersection / union if union > 0 else 0
    
    @staticmethod
    def cosine_similarity(text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts."""
        tokens1 = re.findall(r'\b\w+\b', text1.lower())
        tokens2 = re.findall(r'\b\w+\b', text2.lower())
        
        # Create term frequency vectors
        all_tokens = set(tokens1 + tokens2)
        
        vec1 = [tokens1.count(token) for token in all_tokens]
        vec2 = [tokens2.count(token) for token in all_tokens]
        
        # Calculate cosine similarity
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        return dot_product / (magnitude1 * magnitude2)
    
    @staticmethod
    def levenshtein_distance(text1: str, text2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        m, n = len(text1), len(text2)
        
        # Create distance matrix
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Initialize first row and column
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Fill the matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # deletion
                        dp[i][j - 1],      # insertion
                        dp[i - 1][j - 1]   # substitution
                    )
        
        return dp[m][n]
    
    @staticmethod
    def similarity_score(text1: str, text2: str) -> float:
        """Calculate overall similarity score (0-1)."""
        # Combine multiple similarity metrics
        jaccard = TextSimilarity.jaccard_similarity(text1, text2)
        cosine = TextSimilarity.cosine_similarity(text1, text2)
        
        # Normalize Levenshtein distance
        lev_distance = TextSimilarity.levenshtein_distance(text1, text2)
        max_length = max(len(text1), len(text2))
        lev_similarity = 1 - (lev_distance / max_length) if max_length > 0 else 1
        
        # Weighted average
        return (jaccard * 0.3 + cosine * 0.4 + lev_similarity * 0.3)


class KeywordExtractor:
    """Keyword extraction utilities."""
    
    @staticmethod
    def extract_keywords(text: str, 
                       top_n: int = 10,
                       min_length: int = 3) -> List[Tuple[str, float]]:
        """Extract top keywords using TF-IDF-like scoring."""
        # Tokenize and filter
        tokens = re.findall(r'\b\w+\b', text.lower())
        tokens = [token for token in tokens if len(token) >= min_length]
        
        if not tokens:
            return []
        
        # Calculate term frequency
        tf = Counter(tokens)
        
        # Calculate simple IDF (inverse document frequency)
        # Here we use document length as proxy
        doc_length = len(tokens)
        idf = {term: math.log(doc_length / (count + 1)) for term, count in tf.items()}
        
        # Calculate TF-IDF scores
        tfidf_scores = {term: tf[term] * idf[term] for term in tf}
        
        # Sort by score and return top N
        sorted_keywords = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_keywords[:top_n]
    
    @staticmethod
    def extract_keyphrases(text: str, 
                         n_gram_size: int = 2,
                         top_n: int = 5) -> List[Tuple[str, float]]:
        """Extract key phrases using n-gram analysis."""
        # Tokenize
        tokens = re.findall(r'\b\w+\b', text.lower())
        
        if len(tokens) < n_gram_size:
            return []
        
        # Generate n-grams
        ngrams = []
        for i in range(len(tokens) - n_gram_size + 1):
            ngram = ' '.join(tokens[i:i + n_gram_size])
            ngrams.append(ngram)
        
        # Count n-gram frequencies
        ngram_freq = Counter(ngrams)
        
        # Calculate scores (frequency + length bonus)
        scores = {}
        for ngram, freq in ngram_freq.items():
            scores[ngram] = freq * len(ngram.split())
        
        # Sort and return top N
        sorted_phrases = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_phrases[:top_n]


class TextSummarizer:
    """Text summarization utilities."""
    
    @staticmethod
    def extractive_summary(text: str, 
                          num_sentences: int = 3,
                          min_sentence_length: int = 10) -> str:
        """Generate extractive summary using sentence scoring."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentences = [s for s in sentences if len(s) >= min_sentence_length]
        
        if len(sentences) <= num_sentences:
            return '. '.join(sentences)
        
        # Score sentences based on position and length
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            # Position score (favor beginning and end)
            position_score = 1.0 - abs(i - len(sentences) / 2) / (len(sentences) / 2)
            
            # Length score (favor medium length)
            length = len(sentence.split())
            length_score = 1.0 - abs(length - 20) / 20
            length_score = max(0, length_score)
            
            # Combined score
            score = position_score * 0.6 + length_score * 0.4
            scored_sentences.append((sentence, score))
        
        # Sort by score and select top N
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in scored_sentences[:num_sentences]]
        
        # Reorder by original position
        original_order = []
        for sentence in sentences:
            if sentence in top_sentences:
                original_order.append(sentence)
                top_sentences.remove(sentence)
                if not top_sentences:
                    break
        
        return '. '.join(original_order)
    
    @staticmethod
    def keyword_summary(text: str, 
                       num_keywords: int = 5) -> str:
        """Generate summary based on keywords."""
        keywords = KeywordExtractor.extract_keywords(text, num_keywords)
        keyword_list = [kw[0] for kw in keywords]
        
        return f"Key topics: {', '.join(keyword_list)}"


class LanguageDetector:
    """Language detection utilities."""
    
    @staticmethod
    def detect_language(text: str) -> Language:
        """Detect language of text (simplified)."""
        # Common character patterns for different languages
        language_patterns = {
            Language.CHINESE: r'[\u4e00-\u9fff]',
            Language.JAPANESE: r'[\u3040-\u309f\u30a0-\u30ff]',
            Language.FRENCH: r'[àâäéèêëïîôùûüÿç]',
            Language.GERMAN: r'[äöüß]',
            Language.SPANISH: r'[ñáéíóúü]',
        }
        
        # Check for language-specific characters
        for language, pattern in language_patterns.items():
            if re.search(pattern, text):
                return language
        
        # Default to English
        return Language.ENGLISH
    
    @staticmethod
    def get_language_stats(text: str) -> Dict[str, Any]:
        """Get language statistics for text."""
        detected_language = LanguageDetector.detect_language(text)
        
        # Character analysis
        total_chars = len(text)
        alpha_chars = sum(1 for c in text if c.isalpha())
        digit_chars = sum(1 for c in text if c.isdigit())
        space_chars = sum(1 for c in text if c.isspace())
        punctuation_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
        
        return {
            "detected_language": detected_language.value,
            "total_characters": total_chars,
            "alpha_characters": alpha_chars,
            "digit_characters": digit_chars,
            "space_characters": space_chars,
            "punctuation_characters": punctuation_chars,
            "alpha_ratio": alpha_chars / total_chars if total_chars > 0 else 0
        }


class FeatureExtractor:
    """Feature extraction for ML models."""
    
    @staticmethod
    def bag_of_words(text: str, vocabulary: Optional[List[str]] = None) -> Dict[str, int]:
        """Extract bag of words features."""
        tokens = re.findall(r'\b\w+\b', text.lower())
        
        if vocabulary is None:
            vocabulary = list(set(tokens))
        
        bow = {}
        for word in vocabulary:
            bow[word] = tokens.count(word)
        
        return bow
    
    @staticmethod
    def tf_idf(texts: List[str]) -> Dict[str, Dict[str, float]]:
        """Calculate TF-IDF features for multiple texts."""
        # Tokenize all texts
        all_tokens = []
        tokenized_texts = []
        
        for text in texts:
            tokens = re.findall(r'\b\w+\b', text.lower())
            tokenized_texts.append(tokens)
            all_tokens.extend(tokens)
        
        # Build vocabulary
        vocabulary = list(set(all_tokens))
        
        # Calculate TF-IDF
        tfidf_results = {}
        
        for i, tokens in enumerate(tokenized_texts):
            tfidf_scores = {}
            
            for term in vocabulary:
                # Term frequency
                tf = tokens.count(term) / len(tokens) if tokens else 0
                
                # Document frequency
                df = sum(1 for doc_tokens in tokenized_texts if term in doc_tokens)
                
                # Inverse document frequency
                idf = math.log(len(texts) / df) if df > 0 else 0
                
                # TF-IDF
                tfidf_scores[term] = tf * idf
            
            tfidf_results[f"doc_{i}"] = tfidf_scores
        
        return tfidf_results
    
    @staticmethod
    def ngram_features(text: str, n: int = 2) -> Counter:
        """Extract n-gram features."""
        tokens = re.findall(r'\b\w+\b', text.lower())
        
        if len(tokens) < n:
            return Counter()
        
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i + n])
            ngrams.append(ngram)
        
        return Counter(ngrams)
    
    @staticmethod
    def char_ngrams(text: str, n: int = 3) -> Counter:
        """Extract character n-gram features."""
        text = text.lower().replace(' ', '')
        
        if len(text) < n:
            return Counter()
        
        ngrams = []
        for i in range(len(text) - n + 1):
            ngram = text[i:i + n]
            ngrams.append(ngram)
        
        return Counter(ngrams)


def demonstrate_natural_language_processing():
    """Demonstrate NLP functionality."""
    print("=== Natural Language Processing Demonstration ===\n")
    
    # Text Preprocessing
    print("1. Text Preprocessing:")
    preprocessor = TextPreprocessor()
    
    sample_text = "Hello World! This is a SAMPLE text with URLs https://example.com and emails test@test.com"
    print(f"   Original: {sample_text}")
    
    cleaned = preprocessor.clean_text(sample_text)
    print(f"   Cleaned: {cleaned}")
    
    tokens = preprocessor.tokenize(cleaned)
    print(f"   Tokens: {tokens}")
    
    no_stopwords = preprocessor.remove_stop_words(tokens)
    print(f"   Without stopwords: {no_stopwords}")
    
    # Sentiment Analysis
    print("\n2. Sentiment Analysis:")
    sentiment_analyzer = SentimentAnalyzer()
    
    positive_text = "I love this product! It's amazing and wonderful."
    negative_text = "This is terrible and awful. I hate it."
    neutral_text = "The product is okay, nothing special."
    
    print(f"   Positive: {sentiment_analyzer.analyze_sentiment(positive_text).label}")
    print(f"   Negative: {sentiment_analyzer.analyze_sentiment(negative_text).label}")
    print(f"   Neutral: {sentiment_analyzer.analyze_sentiment(neutral_text).label}")
    
    # Text Classification
    print("\n3. Text Classification:")
    classifier = TextClassifier()
    classifier.add_category("sports", ["game", "team", "player", "score", "win", "sport"])
    classifier.add_category("technology", ["computer", "software", "hardware", "digital", "tech"])
    classifier.add_category("food", ["cooking", "recipe", "ingredient", "meal", "taste"])
    
    sports_text = "The team won the game with a great score"
    tech_text = "The new computer software is amazing"
    food_text = "This cooking recipe has great ingredients"
    
    print(f"   Sports text: {classifier.classify(sports_text).label}")
    print(f"   Tech text: {classifier.classify(tech_text).label}")
    print(f"   Food text: {classifier.classify(food_text).label}")
    
    # Text Similarity
    print("\n4. Text Similarity:")
    text1 = "The quick brown fox jumps over the lazy dog"
    text2 = "The quick brown fox jumped over the lazy dog"
    text3 = "A completely different sentence about something else"
    
    jaccard = TextSimilarity.jaccard_similarity(text1, text2)
    cosine = TextSimilarity.cosine_similarity(text1, text2)
    overall = TextSimilarity.similarity_score(text1, text2)
    
    print(f"   Jaccard similarity (similar texts): {jaccard:.3f}")
    print(f"   Cosine similarity (similar texts): {cosine:.3f}")
    print(f"   Overall similarity (similar texts): {overall:.3f}")
    
    different = TextSimilarity.similarity_score(text1, text3)
    print(f"   Overall similarity (different texts): {different:.3f}")
    
    # Keyword Extraction
    print("\n5. Keyword Extraction:")
    long_text = """
    Machine learning is a subset of artificial intelligence that focuses on building systems 
    that learn from data. Python is a popular programming language for machine learning 
    due to its extensive libraries and community support. Data science involves analyzing 
    and interpreting complex data to help decision-making.
    """
    
    keywords = KeywordExtractor.extract_keywords(long_text, top_n=5)
    print(f"   Top keywords: {[kw[0] for kw in keywords]}")
    
    keyphrases = KeywordExtractor.extract_keyphrases(long_text, n_gram_size=2, top_n=3)
    print(f"   Key phrases: {[kp[0] for kp in keyphrases]}")
    
    # Text Summarization
    print("\n6. Text Summarization:")
    summary = TextSummarizer.extractive_summary(long_text, num_sentences=2)
    print(f"   Summary: {summary}")
    
    keyword_summary = TextSummarizer.keyword_summary(long_text, num_keywords=3)
    print(f"   Keyword summary: {keyword_summary}")
    
    # Language Detection
    print("\n7. Language Detection:")
    english_text = "This is English text"
    chinese_text = "这是中文文本"
    language_stats = LanguageDetector.get_language_stats(english_text)
    print(f"   English stats: {language_stats['detected_language']}")
    
    detected_chinese = LanguageDetector.detect_language(chinese_text)
    print(f"   Chinese detection: {detected_chinese.value}")
    
    # Feature Extraction
    print("\n8. Feature Extraction:")
    sample_texts = [
        "Machine learning is great",
        "Deep learning is powerful",
        "Natural language processing is interesting"
    ]
    
    bow = FeatureExtractor.bag_of_words(sample_texts[0])
    print(f"   Bag of words: {dict(list(bow.items())[:5])}")
    
    ngrams = FeatureExtractor.ngram_features(sample_texts[0], n=2)
    print(f"   2-grams: {list(ngrams.items())[:5]}")
    
    print("\n=== Demonstration Complete ===")
    print("\nNLP Best Practices:")
    print("- Always preprocess text before analysis")
    print("- Use appropriate tokenization for your language")
    print("- Consider context for accurate sentiment analysis")
    print("- Combine multiple similarity metrics for robustness")
    print("- Extract meaningful keywords and phrases")
    print("- Use domain-specific vocabularies for classification")
    print("- Consider using libraries like NLTK, spaCy for production")
    print("- Handle multilingual text with proper language detection")


if __name__ == "__main__":
    demonstrate_natural_language_processing()