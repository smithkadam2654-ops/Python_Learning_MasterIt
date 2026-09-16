"""
String Utilities Module

This module provides comprehensive string manipulation and processing utilities including:
- String cleaning and normalization
- String formatting and templating
- String searching and matching
- String transformation and conversion
- Text analysis and statistics
- String validation
- Encoding and decoding
- String manipulation utilities
- Pattern matching
- Text generation

All functions include comprehensive docstrings and type hints.
"""

import re
import random
import string
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from collections import Counter
import unicodedata


@dataclass
class TextAnalysis:
    """Container for text analysis results."""
    character_count: int
    word_count: int
    sentence_count: int
    paragraph_count: int
    average_word_length: float
    average_sentence_length: float
    most_common_words: List[Tuple[str, int]]
    readability_score: float


class StringCleaner:
    """String cleaning and normalization utilities."""
    
    @staticmethod
    def remove_whitespace(text: str) -> str:
        """Remove all whitespace from string."""
        return re.sub(r'\s+', '', text)
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace to single spaces."""
        return ' '.join(text.split())
    
    @staticmethod
    def remove_extra_spaces(text: str) -> str:
        """Remove extra spaces but preserve newlines."""
        return re.sub(r' +', ' ', text)
    
    @staticmethod
    def remove_newlines(text: str) -> str:
        """Remove newline characters."""
        return text.replace('\n', ' ').replace('\r', '')
    
    @staticmethod
    def remove_special_chars(text: str, keep_spaces: bool = True) -> str:
        """Remove special characters, optionally keeping spaces."""
        if keep_spaces:
            return re.sub(r'[^\w\s]', '', text)
        return re.sub(r'[^\w]', '', text)
    
    @staticmethod
    def remove_numbers(text: str) -> str:
        """Remove all numbers from string."""
        return re.sub(r'\d+', '', text)
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """Remove HTML tags from string."""
        return re.sub(r'<[^>]+>', '', text)
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from string."""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)
    
    @staticmethod
    def remove_emails(text: str) -> str:
        """Remove email addresses from string."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.sub(email_pattern, '', text)
    
    @staticmethod
    def normalize_unicode(text: str) -> str:
        """Normalize unicode characters."""
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    
    @staticmethod
    def clean_text(text: str, 
                   lowercase: bool = True,
                   remove_punctuation: bool = True,
                   remove_numbers: bool = False,
                   normalize_whitespace: bool = True) -> str:
        """Comprehensive text cleaning with multiple options."""
        if lowercase:
            text = text.lower()
        
        if remove_punctuation:
            text = StringCleaner.remove_special_chars(text)
        
        if remove_numbers:
            text = StringCleaner.remove_numbers(text)
        
        if normalize_whitespace:
            text = StringCleaner.normalize_whitespace(text)
        
        return text.strip()


class StringFormatter:
    """String formatting and templating utilities."""
    
    @staticmethod
    def format_currency(amount: float, currency: str = "$", 
                       decimals: int = 2, thousands_sep: bool = True) -> str:
        """Format amount as currency."""
        formatted = f"{amount:.{decimals}f}"
        
        if thousands_sep:
            parts = formatted.split('.')
            integer_part = parts[0]
            decimal_part = parts[1] if len(parts) > 1 else ""
            
            # Add thousands separator
            if len(integer_part) > 3:
                formatted_integer = "{:,}".format(int(integer_part))
                formatted = f"{formatted_integer}.{decimal_part}" if decimal_part else formatted_integer
        
        return f"{currency}{formatted}"
    
    @staticmethod
    def format_phone_number(phone: str, format: str = "(XXX) XXX-XXXX") -> str:
        """Format phone number according to specified format."""
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) == 10:
            return format.replace('X', '{}').format(*digits)
        elif len(digits) == 11:
            return format.replace('X', '{}').format(*digits[1:])
        else:
            return phone
    
    @staticmethod
    def format_ssn(ssn: str) -> str:
        """Format SSN as XXX-XX-XXXX."""
        digits = re.sub(r'\D', '', ssn)
        if len(digits) == 9:
            return f"{digits[:3]}-{digits[3:5]}-{digits[5:]}"
        return ssn
    
    @staticmethod
    def format_credit_card(card: str, mask: bool = True) -> str:
        """Format credit card number, optionally masking most digits."""
        digits = re.sub(r'\D', '', card)
        
        if len(digits) == 16:
            if mask:
                return f"XXXX-XXXX-XXXX-{digits[-4:]}"
            return f"{digits[:4]}-{digits[4:8]}-{digits[8:12]}-{digits[12:]}"
        return card
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to maximum length with suffix."""
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def truncate_words(text: str, max_words: int, suffix: str = "...") -> str:
        """Truncate text to maximum number of words."""
        words = text.split()
        
        if len(words) <= max_words:
            return text
        
        return ' '.join(words[:max_words]) + suffix
    
    @staticmethod
    def capitalize_words(text: str) -> str:
        """Capitalize first letter of each word."""
        return ' '.join(word.capitalize() for word in text.split())
    
    @staticmethod
    def title_case(text: str) -> str:
        """Convert string to title case."""
        return text.title()
    
    @staticmethod
    def camel_case(text: str) -> str:
        """Convert string to camelCase."""
        words = text.split()
        if not words:
            return ""
        
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    
    @staticmethod
    def pascal_case(text: str) -> str:
        """Convert string to PascalCase."""
        words = text.split()
        return ''.join(word.capitalize() for word in words)
    
    @staticmethod
    def snake_case(text: str) -> str:
        """Convert string to snake_case."""
        # Remove special characters and replace spaces with underscores
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', '_', text.lower())
        return text
    
    @staticmethod
    def kebab_case(text: str) -> str:
        """Convert string to kebab-case."""
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', '-', text.lower())
        return text


class StringSearcher:
    """String searching and matching utilities."""
    
    @staticmethod
    def find_all(text: str, pattern: str, case_sensitive: bool = True) -> List[int]:
        """Find all occurrences of pattern in text."""
        if not case_sensitive:
            text = text.lower()
            pattern = pattern.lower()
        
        indices = []
        start = 0
        
        while True:
            index = text.find(pattern, start)
            if index == -1:
                break
            indices.append(index)
            start = index + 1
        
        return indices
    
    @staticmethod
    def find_words(text: str, word: str, case_sensitive: bool = True) -> List[int]:
        """Find all occurrences of a whole word."""
        pattern = r'\b' + re.escape(word) + r'\b'
        flags = 0 if case_sensitive else re.IGNORECASE
        
        matches = list(re.finditer(pattern, text, flags))
        return [match.start() for match in matches]
    
    @staticmethod
    def find_regex(text: str, pattern: str, flags: int = 0) -> List[Tuple[int, int, str]]:
        """Find all regex matches with positions."""
        matches = list(re.finditer(pattern, text, flags))
        return [(match.start(), match.end(), match.group()) for match in matches]
    
    @staticmethod
    def contains_all(text: str, substrings: List[str], case_sensitive: bool = True) -> bool:
        """Check if text contains all substrings."""
        search_text = text if case_sensitive else text.lower()
        
        for substring in substrings:
            search_substring = substring if case_sensitive else substring.lower()
            if search_substring not in search_text:
                return False
        
        return True
    
    @staticmethod
    def contains_any(text: str, substrings: List[str], case_sensitive: bool = True) -> bool:
        """Check if text contains any of the substrings."""
        search_text = text if case_sensitive else text.lower()
        
        for substring in substrings:
            search_substring = substring if case_sensitive else substring.lower()
            if search_substring in search_text:
                return True
        
        return False
    
    @staticmethod
    def starts_with_any(text: str, prefixes: List[str], case_sensitive: bool = True) -> bool:
        """Check if text starts with any of the prefixes."""
        search_text = text if case_sensitive else text.lower()
        
        for prefix in prefixes:
            search_prefix = prefix if case_sensitive else prefix.lower()
            if search_text.startswith(search_prefix):
                return True
        
        return False
    
    @staticmethod
    def ends_with_any(text: str, suffixes: List[str], case_sensitive: bool = True) -> bool:
        """Check if text ends with any of the suffixes."""
        search_text = text if case_sensitive else text.lower()
        
        for suffix in suffixes:
            search_suffix = suffix if case_sensitive else suffix.lower()
            if search_text.endswith(search_suffix):
                return True
        
        return False
    
    @staticmethod
    def find_longest_common_substring(str1: str, str2: str) -> str:
        """Find the longest common substring between two strings."""
        m = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
        longest = 0
        lcs_end = 0
        
        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                if str1[i-1] == str2[j-1]:
                    m[i][j] = m[i-1][j-1] + 1
                    if m[i][j] > longest:
                        longest = m[i][j]
                        lcs_end = i
                else:
                    m[i][j] = 0
        
        return str1[lcs_end - longest:lcs_end]


class StringTransformer:
    """String transformation and conversion utilities."""
    
    @staticmethod
    def reverse(text: str) -> str:
        """Reverse the string."""
        return text[::-1]
    
    @staticmethod
    def shuffle(text: str) -> str:
        """Shuffle characters in the string."""
        chars = list(text)
        random.shuffle(chars)
        return ''.join(chars)
    
    @staticmethod
    def alternate_case(text: str) -> str:
        """Alternate between uppercase and lowercase."""
        result = []
        for i, char in enumerate(text):
            if i % 2 == 0:
                result.append(char.upper())
            else:
                result.append(char.lower())
        return ''.join(result)
    
    @staticmethod
    def swap_case(text: str) -> str:
        """Swap uppercase and lowercase."""
        return text.swapcase()
    
    @staticmethod
    def remove_duplicates(text: str) -> str:
        """Remove duplicate characters while preserving order."""
        seen = set()
        result = []
        for char in text:
            if char not in seen:
                seen.add(char)
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def replace_multiple(text: str, replacements: Dict[str, str]) -> str:
        """Replace multiple substrings at once."""
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    @staticmethod
    def insert_at(text: str, position: int, insertion: str) -> str:
        """Insert string at specified position."""
        return text[:position] + insertion + text[position:]
    
    @staticmethod
    def remove_at(text: str, start: int, end: int) -> str:
        """Remove characters from start to end position."""
        return text[:start] + text[end:]
    
    @staticmethod
    def repeat(text: str, times: int, separator: str = "") -> str:
        """Repeat text specified times with optional separator."""
        return separator.join([text] * times)
    
    @staticmethod
    def pad_left(text: str, length: int, char: str = " ") -> str:
        """Pad string on the left to reach specified length."""
        if len(text) >= length:
            return text
        return char * (length - len(text)) + text
    
    @staticmethod
    def pad_right(text: str, length: int, char: str = " ") -> str:
        """Pad string on the right to reach specified length."""
        if len(text) >= length:
            return text
        return text + char * (length - len(text))
    
    @staticmethod
    def center_text(text: str, length: int, char: str = " ") -> str:
        """Center string within specified length."""
        if len(text) >= length:
            return text
        
        total_padding = length - len(text)
        left_padding = total_padding // 2
        right_padding = total_padding - left_padding
        
        return char * left_padding + text + char * right_padding


class TextAnalyzer:
    """Text analysis and statistics utilities."""
    
    @staticmethod
    def count_characters(text: str, include_spaces: bool = True) -> int:
        """Count characters in text."""
        if include_spaces:
            return len(text)
        return len(text.replace(' ', ''))
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text."""
        words = text.split()
        return len(words)
    
    @staticmethod
    def count_sentences(text: str) -> int:
        """Count sentences in text."""
        sentences = re.split(r'[.!?]+', text)
        return len([s for s in sentences if s.strip()])
    
    @staticmethod
    def count_paragraphs(text: str) -> int:
        """Count paragraphs in text."""
        paragraphs = text.split('\n\n')
        return len([p for p in paragraphs if p.strip()])
    
    @staticmethod
    def average_word_length(text: str) -> float:
        """Calculate average word length."""
        words = text.split()
        if not words:
            return 0.0
        return sum(len(word) for word in words) / len(words)
    
    @staticmethod
    def average_sentence_length(text: str) -> float:
        """Calculate average sentence length in words."""
        sentences = re.split(r'[.!?]+', text)
        valid_sentences = [s for s in sentences if s.strip()]
        
        if not valid_sentences:
            return 0.0
        
        total_words = sum(TextAnalyzer.count_words(s) for s in valid_sentences)
        return total_words / len(valid_sentences)
    
    @staticmethod
    def most_common_words(text: str, n: int = 10, 
                         case_sensitive: bool = False) -> List[Tuple[str, int]]:
        """Get most common words in text."""
        if not case_sensitive:
            text = text.lower()
        
        words = re.findall(r'\b\w+\b', text)
        word_counts = Counter(words)
        
        return word_counts.most_common(n)
    
    @staticmethod
    def most_common_characters(text: str, n: int = 10,
                              case_sensitive: bool = False) -> List[Tuple[str, int]]:
        """Get most common characters in text."""
        if not case_sensitive:
            text = text.lower()
        
        char_counts = Counter(text)
        return char_counts.most_common(n)
    
    @staticmethod
    def vocabulary_richness(text: str) -> float:
        """Calculate vocabulary richness (unique words / total words)."""
        words = re.findall(r'\b\w+\b', text.lower())
        
        if not words:
            return 0.0
        
        unique_words = len(set(words))
        return unique_words / len(words)
    
    @staticmethod
    def readability_score(text: str) -> float:
        """Calculate basic readability score (simplified Flesch)."""
        words = re.findall(r'\b\w+\b', text)
        sentences = re.split(r'[.!?]+', text)
        valid_sentences = [s for s in sentences if s.strip()]
        
        if not words or not valid_sentences:
            return 0.0
        
        total_words = len(words)
        total_sentences = len(valid_sentences)
        total_syllables = sum(TextAnalyzer._count_syllables(word) for word in words)
        
        # Simplified Flesch Reading Ease
        score = 206.835 - (1.015 * total_words / total_sentences) - (84.6 * total_syllables / total_words)
        return max(0, min(100, score))
    
    @staticmethod
    def _count_syllables(word: str) -> int:
        """Count syllables in a word (simplified)."""
        word = word.lower()
        if len(word) <= 3:
            return 1
        
        vowels = 'aeiouy'
        syllable_count = 0
        prev_char_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_char_was_vowel:
                syllable_count += 1
            prev_char_was_vowel = is_vowel
        
        if word.endswith('e'):
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    @staticmethod
    def analyze_text(text: str) -> TextAnalysis:
        """Perform comprehensive text analysis."""
        return TextAnalysis(
            character_count=TextAnalyzer.count_characters(text),
            word_count=TextAnalyzer.count_words(text),
            sentence_count=TextAnalyzer.count_sentences(text),
            paragraph_count=TextAnalyzer.count_paragraphs(text),
            average_word_length=TextAnalyzer.average_word_length(text),
            average_sentence_length=TextAnalyzer.average_sentence_length(text),
            most_common_words=TextAnalyzer.most_common_words(text, 5),
            readability_score=TextAnalyzer.readability_score(text)
        )


class StringValidator:
    """String validation utilities."""
    
    @staticmethod
    def is_email(text: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, text))
    
    @staticmethod
    def is_url(text: str) -> bool:
        """Validate URL format."""
        pattern = r'^https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/.*)?$'
        return bool(re.match(pattern, text))
    
    @staticmethod
    def is_phone(text: str) -> bool:
        """Validate phone number format."""
        pattern = r'^\+?[\d\s-()]{10,}$'
        return bool(re.match(pattern, text))
    
    @staticmethod
    def is_ip_address(text: str) -> bool:
        """Validate IPv4 address format."""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, text):
            return False
        
        octets = text.split('.')
        return all(0 <= int(octet) <= 255 for octet in octets)
    
    @staticmethod
    def is_credit_card(text: str) -> bool:
        """Validate credit card number using Luhn algorithm."""
        digits = re.sub(r'\D', '', text)
        
        if len(digits) < 13 or len(digits) > 19:
            return False
        
        # Luhn algorithm
        total = 0
        reverse_digits = digits[::-1]
        
        for i, digit in enumerate(reverse_digits):
            num = int(digit)
            if i % 2 == 1:
                num *= 2
                if num > 9:
                    num -= 9
            total += num
        
        return total % 10 == 0
    
    @staticmethod
    def is_strong_password(text: str) -> bool:
        """Validate strong password (8+ chars, uppercase, lowercase, number, special)."""
        if len(text) < 8:
            return False
        
        has_upper = any(c.isupper() for c in text)
        has_lower = any(c.islower() for c in text)
        has_digit = any(c.isdigit() for c in text)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in text)
        
        return all([has_upper, has_lower, has_digit, has_special])
    
    @staticmethod
    def is_hex_color(text: str) -> bool:
        """Validate hex color code."""
        pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        return bool(re.match(pattern, text))
    
    @staticmethod
    def is_date(text: str, format: str = "%Y-%m-%d") -> bool:
        """Validate date format."""
        from datetime import datetime
        try:
            datetime.strptime(text, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_json(text: str) -> bool:
        """Validate JSON format."""
        import json
        try:
            json.loads(text)
            return True
        except:
            return False


class StringGenerator:
    """String generation utilities."""
    
    @staticmethod
    def random_string(length: int, 
                      include_uppercase: bool = True,
                      include_lowercase: bool = True,
                      include_digits: bool = True,
                      include_special: bool = False) -> str:
        """Generate random string with specified character types."""
        chars = ""
        
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_digits:
            chars += string.digits
        if include_special:
            chars += "!@#$%^&*"
        
        if not chars:
            chars = string.ascii_lowercase
        
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def random_password(length: int = 12) -> str:
        """Generate random strong password."""
        return StringGenerator.random_string(
            length,
            include_uppercase=True,
            include_lowercase=True,
            include_digits=True,
            include_special=True
        )
    
    @staticmethod
    def random_hex_color() -> str:
        """Generate random hex color."""
        return f"#{''.join(random.choices('0123456789ABCDEF', k=6))}"
    
    @staticmethod
    def random_uuid() -> str:
        """Generate random UUID string."""
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def random_lorem_ipsum(sentences: int = 5) -> str:
        """Generate random lorem ipsum text."""
        lorem_words = [
            "lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
            "adipiscing", "elit", "sed", "do", "eiusmod", "tempor",
            "incididunt", "ut", "labore", "et", "dolore", "magna",
            "aliqua", "enim", "ad", "minim", "veniam", "quis"
        ]
        
        sentences_list = []
        for _ in range(sentences):
            sentence_words = random.sample(lorem_words, random.randint(8, 15))
            sentence = ' '.join(sentence_words)
            sentence = sentence[0].upper() + sentence[1:] + '.'
            sentences_list.append(sentence)
        
        return ' '.join(sentences_list)
    
    @staticmethod
    def generate_slug(text: str) -> str:
        """Generate URL-friendly slug from text."""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'\s+', '-', text)
        text = re.sub(r'-+', '-', text)
        return text.strip('-')


def demonstrate_string_utils():
    """Demonstrate string utilities functionality."""
    print("=== String Utilities Demonstration ===\n")
    
    # String Cleaning
    print("1. String Cleaning:")
    dirty_text = "  Hello   World!  This is  a TEST.  "
    print(f"   Original: '{dirty_text}'")
    print(f"   Normalize whitespace: '{StringCleaner.normalize_whitespace(dirty_text)}'")
    print(f"   Remove special chars: '{StringCleaner.remove_special_chars(dirty_text)}'")
    print(f"   Clean text: '{StringCleaner.clean_text(dirty_text)}'")
    
    # String Formatting
    print("\n2. String Formatting:")
    print(f"   Currency: {StringFormatter.format_currency(1234.56)}")
    print(f"   Phone: {StringFormatter.format_phone_number('1234567890')}")
    print(f"   SSN: {StringFormatter.format_ssn('123456789')}")
    print(f"   Credit card: {StringFormatter.format_credit_card('1234567890123456')}")
    print(f"   Camel case: {StringFormatter.camel_case('hello world test')}")
    print(f"   Snake case: {StringFormatter.snake_case('Hello World Test')}")
    
    # String Searching
    print("\n3. String Searching:")
    text = "The quick brown fox jumps over the lazy dog"
    print(f"   Find 'the': {StringSearcher.find_words(text, 'the', case_sensitive=False)}")
    print(f"   Contains all: {StringSearcher.contains_all(text, ['quick', 'fox', 'dog'])}")
    print(f"   Contains any: {StringSearcher.contains_any(text, ['cat', 'dog'])}")
    
    # String Transformation
    print("\n4. String Transformation:")
    print(f"   Reverse: '{StringTransformer.reverse('hello')}'")
    print(f"   Alternate case: '{StringTransformer.alternate_case('hello')}'")
    print(f"   Swap case: '{StringTransformer.swap_case('HeLLo')}'")
    print(f"   Remove duplicates: '{StringTransformer.remove_duplicates('hello')}'")
    
    # Text Analysis
    print("\n5. Text Analysis:")
    sample_text = "The quick brown fox jumps over the lazy dog. The dog was not amused."
    analysis = TextAnalyzer.analyze_text(sample_text)
    print(f"   Character count: {analysis.character_count}")
    print(f"   Word count: {analysis.word_count}")
    print(f"   Sentence count: {analysis.sentence_count}")
    print(f"   Average word length: {analysis.average_word_length:.2f}")
    print(f"   Most common words: {analysis.most_common_words[:3]}")
    
    # String Validation
    print("\n6. String Validation:")
    print(f"   Email valid: {StringValidator.is_email('test@example.com')}")
    print(f"   URL valid: {StringValidator.is_url('https://example.com')}")
    print(f"   Phone valid: {StringValidator.is_phone('+1-555-123-4567')}")
    print(f"   IP valid: {StringValidator.is_ip_address('192.168.1.1')}")
    print(f"   Strong password: {StringValidator.is_strong_password('Pass123!')}")
    
    # String Generation
    print("\n7. String Generation:")
    print(f"   Random string: {StringGenerator.random_string(10)}")
    print(f"   Random password: {StringGenerator.random_password()}")
    print(f"   Random hex color: {StringGenerator.random_hex_color()}")
    print(f"   Random UUID: {StringGenerator.random_uuid()}")
    print(f"   Random slug: {StringGenerator.generate_slug('Hello World Test')}")
    
    # Longest Common Substring
    print("\n8. Advanced Operations:")
    str1 = "programming"
    str2 = "programmer"
    lcs = StringSearcher.find_longest_common_substring(str1, str2)
    print(f"   LCS of '{str1}' and '{str2}': '{lcs}'")
    
    print("\n=== Demonstration Complete ===")


if __name__ == "__main__":
    demonstrate_string_utils()