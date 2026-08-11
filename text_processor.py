#!/usr/bin/env python3
"""
Text Processing Utilities
Provides comprehensive text analysis and processing functions
"""

import re
from collections import Counter
from typing import List, Tuple

class TextProcessor:
    @staticmethod
    def word_frequency(text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """Calculate word frequency and return top N most common words."""
        # Clean and tokenize
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Count frequencies
        word_counts = Counter(words)
        
        # Return top N
        return word_counts.most_common(top_n)
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """Extract all hashtags from text."""
        return re.findall(r'#[\w]+', text)
    
    @staticmethod
    def summarize_text(text: str, max_sentences: int = 3) -> str:
        """Simple text summarization by extracting key sentences."""
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Calculate word frequencies
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = Counter(words)
        
        # Score sentences
        sentence_scores = {}
        for sentence in sentences:
            words_in_sentence = re.findall(r'\b\w+\b', sentence.lower())
            score = sum(word_freq[word] for word in words_in_sentence)
            sentence_scores[sentence] = score
        
        # Get top scoring sentences
        top_sentences = sorted(sentence_scores.items(), 
                             key=lambda x: x[1], reverse=True)[:max_sentences]
        
        return ' '.join(sorted([sent for sent, score in top_sentences]))
    
    @staticmethod
    def create_word_cloud(text: str, width: int = 50, height: int = 20) -> str:
        """Create a simple ASCII word cloud."""
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = Counter(words)
        
        # Create word cloud
        cloud_lines = []
        max_freq = max(word_freq.values()) if word_freq else 1
        
        for line_num in range(height):
            line_words = []
            for word, freq in word_freq.most_common():
                if freq > (line_num * max_freq / height):
                    # Scale word size
                    word_length = int(freq * width / max_freq) + 1
                    line_words.append(word * min(word_length, 10))
                else:
                    break
            cloud_lines.append(' '.join(line_words))
        
        return '\n'.join(cloud_lines)

if __name__ == "__main__":
    # Test the text processor
    sample_text = "Python is a great programming language. Python is easy to learn. " \
                  "Many developers use Python for data science and web development. " \
                  "Python has a large community and extensive libraries."
    
    print("=== Word Frequency ===")
    freq = TextProcessor.word_frequency(sample_text, 5)
    for word, count in freq:
        print(f"{word}: {count}")
    
    print("\n=== Hashtags ===")
    hashtags = TextProcessor.extract_hashtags(sample_text + " #Python #Programming #DataScience")
    print(hashtags)
    
    print("\n=== Word Cloud ===")
    word_cloud = TextProcessor.create_word_cloud(sample_text)
    print(word_cloud)