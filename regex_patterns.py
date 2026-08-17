"""
Regular Expressions - Common regex patterns and applications.
Features: Pattern matching, validation, extraction, and replacement.
"""

import re
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class RegexMatch:
    """Container for regex match results."""
    pattern: str
    text: str
    matches: List[str]
    groups: List[Tuple[str, ...]]
    positions: List[Tuple[int, int]]


class RegexUtils:
    """Utility class for common regex operations."""
    
    @staticmethod
    def find_all(pattern: str, text: str) -> List[str]:
        """
        Find all non-overlapping matches of pattern in text.
        
        Args:
            pattern: Regular expression pattern
            text: Text to search
            
        Returns:
            List of matched strings
        """
        return re.findall(pattern, text)
    
    @staticmethod
    def find_first(pattern: str, text: str) -> Optional[str]:
        """
        Find first match of pattern in text.
        
        Args:
            pattern: Regular expression pattern
            text: Text to search
            
        Returns:
            First matched string, or None if no match
        """
        match = re.search(pattern, text)
        return match.group() if match else None
    
    @staticmethod
    def find_with_groups(pattern: str, text: str) -> List[Tuple[str, ...]]:
        """
        Find all matches with captured groups.
        
        Args:
            pattern: Regular expression pattern with groups
            text: Text to search
            
        Returns:
            List of tuples containing captured groups
        """
        return re.findall(pattern, text)
    
    @staticmethod
    def replace(pattern: str, text: str, replacement: str, count: int = 0) -> str:
        """
        Replace all occurrences of pattern with replacement.
        
        Args:
            pattern: Regular expression pattern
            text: Text to process
            replacement: Replacement string (can use backreferences)
            count: Maximum number of replacements (0 = all)
            
        Returns:
            Text with replacements applied
        """
        return re.sub(pattern, replacement, text, count=count)
    
    @staticmethod
    def split(pattern: str, text: str, maxsplit: int = 0) -> List[str]:
        """
        Split text by pattern.
        
        Args:
            pattern: Regular expression pattern
            text: Text to split
            maxsplit: Maximum number of splits (0 = no limit)
            
        Returns:
            List of split parts
        """
        return re.split(pattern, text, maxsplit=maxsplit)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number format (US format).
        
        Args:
            phone: Phone number to validate
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """
        Extract all email addresses from text.
        
        Args:
            text: Text to search
            
        Returns:
            List of email addresses found
        """
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        Extract all URLs from text.
        
        Args:
            text: Text to search
            
        Returns:
            List of URLs found
        """
        pattern = r'https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_numbers(text: str) -> List[str]:
        """
        Extract all numbers (integers and decimals) from text.
        
        Args:
            text: Text to search
            
        Returns:
            List of number strings found
        """
        pattern = r'-?\d+\.?\d*'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_dates(text: str) -> List[str]:
        """
        Extract dates in various formats (MM/DD/YYYY, YYYY-MM-DD, etc.).
        
        Args:
            text: Text to search
            
        Returns:
            List of date strings found
        """
        # Match MM/DD/YYYY, YYYY-MM-DD, DD-MM-YYYY
        pattern = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b|\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """
        Extract all hashtags from text.
        
        Args:
            text: Text to search
            
        Returns:
            List of hashtags found
        """
        pattern = r'#\w+'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_mentions(text: str) -> List[str]:
        """
        Extract all @mentions from text.
        
        Args:
            text: Text to search
            
        Returns:
            List of mentions found
        """
        pattern = r'@\w+'
        return re.findall(pattern, text)
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """
        Remove HTML tags from text.
        
        Args:
            text: Text with HTML tags
            
        Returns:
            Text without HTML tags
        """
        pattern = r'<[^>]+>'
        return re.sub(pattern, '', text)
    
    @staticmethod
    def remove_extra_whitespace(text: str) -> str:
        """
        Remove extra whitespace from text.
        
        Args:
            text: Text with extra whitespace
            
        Returns:
            Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        # Trim leading/trailing whitespace
        return text.strip()
    
    @staticmethod
    def mask_sensitive_data(text: str) -> str:
        """
        Mask sensitive data (emails, phone numbers, credit cards).
        
        Args:
            text: Text containing sensitive data
            
        Returns:
            Text with sensitive data masked
        """
        # Mask emails
        text = re.sub(r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r'***@\2', text)
        # Mask phone numbers
        text = re.sub(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', '***-***-****', text)
        # Mask credit card numbers (simplified)
        text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '****-****-****-****', text)
        return text
    
    @staticmethod
    def word_count(text: str) -> Dict[str, int]:
        """
        Count word frequencies in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary mapping words to their counts
        """
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = {}
        
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        return word_freq


def main() -> None:
    """Demonstrate regex utilities."""
    
    utils = RegexUtils()
    
    print("=== Pattern Matching ===")
    text = "The quick brown fox jumps over the lazy dog. The fox was quick."
    pattern = r'\bq\w+'
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    print(f"Find all: {utils.find_all(pattern, text)}")
    print(f"Find first: {utils.find_first(pattern, text)}")
    
    print("\n=== Group Extraction ===")
    text = "John: 25, Jane: 30, Bob: 35"
    pattern = r'(\w+):\s*(\d+)'
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    print(f"Groups: {utils.find_with_groups(pattern, text)}")
    
    print("\n=== Validation ===")
    test_cases = [
        ("Email", "user@example.com", utils.validate_email),
        ("Email invalid", "invalid.email", utils.validate_email),
        ("Phone", "123-456-7890", utils.validate_phone),
        ("Phone invalid", "123", utils.validate_phone),
        ("URL", "https://www.example.com", utils.validate_url),
        ("URL invalid", "not-a-url", utils.validate_url),
    ]
    
    for name, value, func in test_cases:
        result = func(value)
        print(f"{name}: {value} -> {result}")
    
    print("\n=== Extraction ===")
    text = """
    Contact us at info@example.com or support@company.com.
    Visit https://www.example.com or http://company.org.
    Call us at 123-456-7890 or (555) 123-4567.
    Order #12345 for $99.99 and #67890 for $149.99.
    """
    
    print(f"Text: {text.strip()}")
    print(f"Emails: {utils.extract_emails(text)}")
    print(f"URLs: {utils.extract_urls(text)}")
    print(f"Numbers: {utils.extract_numbers(text)}")
    
    print("\n=== Social Media Extraction ===")
    text = "Check out #Python and #Programming! @developer @coding"
    print(f"Text: {text}")
    print(f"Hashtags: {utils.extract_hashtags(text)}")
    print(f"Mentions: {utils.extract_mentions(text)}")
    
    print("\n=== Text Cleaning ===")
    html_text = "<p>Hello   <b>World</b>!</p>   This is   <i>test</i> text."
    print(f"Original: {html_text}")
    print(f"Remove HTML: {utils.remove_html_tags(html_text)}")
    print(f"Clean whitespace: {utils.remove_extra_whitespace(utils.remove_html_tags(html_text))}")
    
    print("\n=== Sensitive Data Masking ===")
    sensitive = "_contact: john@example.com, phone: 123-456-7890, card: 1234-5678-9012-3456"
    print(f"Original: {sensitive}")
    print(f"Masked: {utils.mask_sensitive_data(sensitive)}")
    
    print("\n=== Word Count ===")
    text = "The quick brown fox jumps over the lazy dog. The fox was quick and the dog was lazy."
    print(f"Text: {text}")
    word_counts = utils.word_count(text)
    print("Word frequencies:")
    for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {word}: {count}")


if __name__ == "__main__":
    main()
