"""
Regular Expressions Utilities Module

This module provides comprehensive regex utilities including:
- Common regex patterns
- Pattern validation
- Text extraction and replacement
- Pattern matching utilities
- Email, URL, phone validation
- Data sanitization
- Log parsing
- File path operations
- Custom pattern building
- Performance optimization

All functions include comprehensive docstrings and type hints.
"""

import re
from typing import Any, Dict, List, Optional, Tuple, Union, Pattern
from dataclasses import dataclass
from enum import Enum
import unicodedata


class RegexPattern(Enum):
    """Common regex patterns."""
    EMAIL = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    URL = r"https?://(?:[-\w.]|(?:%[0-9a-fA-F]{2}))+"
    PHONE_US = r"\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    PHONE_INTL = r"\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}"
    IP_ADDRESS = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    MAC_ADDRESS = r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
    DATE_ISO = r"\d{4}-\d{2}-\d{2}"
    DATE_US = r"\d{2}/\d{2}/\d{4}"
    TIME = r"\d{2}:\d{2}:\d{2}"
    CREDIT_CARD = r"\b(?:\d[ -]*?){13,16}\b"
    SSN = r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b"
    ZIP_CODE_US = r"\b\d{5}(?:-\d{4})?\b"
    UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    HEX_COLOR = r"#[0-9A-Fa-f]{6}"
    USERNAME = r"[a-zA-Z0-9_]{3,20}"
    PASSWORD = r".{8,}"
    HTML_TAG = r"<([a-zA-Z][a-zA-Z0-9]*)(?:\s[^>]*)?>|</([a-zA-Z][a-zA-Z0-9]*)>"


@dataclass
class MatchResult:
    """Container for regex match results."""
    matched: bool
    match: Optional[str]
    groups: Tuple
    start: int
    end: int
    span: Tuple[int, int]


class PatternValidator:
    """Regex pattern validation utilities."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address."""
        pattern = re.compile(RegexPattern.EMAIL.value)
        return bool(pattern.fullmatch(email))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL."""
        pattern = re.compile(RegexPattern.URL.value)
        return bool(pattern.fullmatch(url))
    
    @staticmethod
    def validate_phone_us(phone: str) -> bool:
        """Validate US phone number."""
        pattern = re.compile(RegexPattern.PHONE_US.value)
        return bool(pattern.fullmatch(phone))
    
    @staticmethod
    def validate_phone_intl(phone: str) -> bool:
        """Validate international phone number."""
        pattern = re.compile(RegexPattern.PHONE_INTL.value)
        return bool(pattern.fullmatch(phone))
    
    @staticmethod
    def validate_ip_address(ip: str) -> bool:
        """Validate IPv4 address."""
        pattern = re.compile(RegexPattern.IP_ADDRESS.value)
        return bool(pattern.fullmatch(ip))
    
    @staticmethod
    def validate_mac_address(mac: str) -> bool:
        """Validate MAC address."""
        pattern = re.compile(RegexPattern.MAC_ADDRESS.value)
        return bool(pattern.fullmatch(mac))
    
    @staticmethod
    def validate_date_iso(date_str: str) -> bool:
        """Validate ISO date format (YYYY-MM-DD)."""
        pattern = re.compile(RegexPattern.DATE_ISO.value)
        return bool(pattern.fullmatch(date_str))
    
    @staticmethod
    def validate_time(time_str: str) -> bool:
        """Validate time format (HH:MM:SS)."""
        pattern = re.compile(RegexPattern.TIME.value)
        return bool(pattern.fullmatch(time_str))
    
    @staticmethod
    def validate_credit_card(card_number: str) -> bool:
        """Validate credit card number format."""
        pattern = re.compile(RegexPattern.CREDIT_CARD.value)
        return bool(pattern.fullmatch(card_number.replace(" ", "").replace("-", "")))
    
    @staticmethod
    def validate_ssn(ssn: str) -> bool:
        """Validate US Social Security Number."""
        pattern = re.compile(RegexPattern.SSN.value)
        return bool(pattern.fullmatch(ssn))
    
    @staticmethod
    def validate_zip_code(zip_code: str) -> bool:
        """Validate US ZIP code."""
        pattern = re.compile(RegexPattern.ZIP_CODE_US.value)
        return bool(pattern.fullmatch(zip_code))
    
    @staticmethod
    def validate_uuid(uuid_str: str) -> bool:
        """Validate UUID format."""
        pattern = re.compile(RegexPattern.UUID.value)
        return bool(pattern.fullmatch(uuid_str))
    
    @staticmethod
    def validate_hex_color(color: str) -> bool:
        """Validate hex color code."""
        pattern = re.compile(RegexPattern.HEX_COLOR.value)
        return bool(pattern.fullmatch(color))
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format."""
        pattern = re.compile(RegexPattern.USERNAME.value)
        return bool(pattern.fullmatch(username))
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, bool]:
        """Validate password strength."""
        result = {
            "length": len(password) >= 8,
            "uppercase": bool(re.search(r'[A-Z]', password)),
            "lowercase": bool(re.search(r'[a-z]', password)),
            "number": bool(re.search(r'\d', password)),
            "special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }
        
        result["strong"] = all(result.values())
        return result


class TextExtractor:
    """Text extraction using regex."""
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """Extract all email addresses from text."""
        pattern = re.compile(RegexPattern.EMAIL.value)
        return pattern.findall(text)
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract all URLs from text."""
        pattern = re.compile(RegexPattern.URL.value)
        return pattern.findall(text)
    
    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """Extract all phone numbers from text."""
        pattern = re.compile(RegexPattern.PHONE_INTL.value)
        return pattern.findall(text)
    
    @staticmethod
    def extract_ip_addresses(text: str) -> List[str]:
        """Extract all IP addresses from text."""
        pattern = re.compile(RegexPattern.IP_ADDRESS.value)
        return pattern.findall(text)
    
    @staticmethod
    def extract_dates(text: str) -> List[str]:
        """Extract all dates in ISO format from text."""
        pattern = re.compile(RegexPattern.DATE_ISO.value)
        return pattern.findall(text)
    
    @staticmethod
    def extract_times(text: str) -> List[str]:
        """Extract all times from text."""
        pattern = re.compile(RegexPattern.TIME.value)
        return pattern.findall(text)
    
    @staticmethod
    def extract_numbers(text: str) -> List[str]:
        """Extract all numbers from text."""
        pattern = re.compile(r'\b\d+\.?\d*\b')
        return pattern.findall(text)
    
    @staticmethod
    def extract_emojis(text: str) -> List[str]:
        """Extract all emojis from text."""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.findall(text)
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """Extract all hashtags from text."""
        pattern = re.compile(r'#\w+')
        return pattern.findall(text)
    
    @staticmethod
    def extract_mentions(text: str) -> List[str]:
        """Extract all @mentions from text."""
        pattern = re.compile(r'@\w+')
        return pattern.findall(text)
    
    @staticmethod
    def extract_code_blocks(text: str, language: Optional[str] = None) -> List[str]:
        """Extract code blocks from text."""
        if language:
            pattern = re.compile(r'```' + language + r'\n(.*?)```', re.DOTALL)
        else:
            pattern = re.compile(r'```(.*?)```', re.DOTALL)
        
        return pattern.findall(text)


class TextReplacer:
    """Text replacement using regex."""
    
    @staticmethod
    def replace_emails(text: str, replacement: str = "[EMAIL]") -> str:
        """Replace all email addresses with placeholder."""
        pattern = re.compile(RegexPattern.EMAIL.value)
        return pattern.sub(replacement, text)
    
    @staticmethod
    def replace_urls(text: str, replacement: str = "[URL]") -> str:
        """Replace all URLs with placeholder."""
        pattern = re.compile(RegexPattern.URL.value)
        return pattern.sub(replacement, text)
    
    @staticmethod
    def replace_phone_numbers(text: str, replacement: str = "[PHONE]") -> str:
        """Replace all phone numbers with placeholder."""
        pattern = re.compile(RegexPattern.PHONE_INTL.value)
        return pattern.sub(replacement, text)
    
    @staticmethod
    def replace_ip_addresses(text: str, replacement: str = "[IP]") -> str:
        """Replace all IP addresses with placeholder."""
        pattern = re.compile(RegexPattern.IP_ADDRESS.value)
        return pattern.sub(replacement, text)
    
    @staticmethod
    def replace_special_chars(text: str, replacement: str = "") -> str:
        """Replace special characters."""
        pattern = re.compile(r'[^a-zA-Z0-9\s]')
        return pattern.sub(replacement, text)
    
    @staticmethod
    def replace_multiple_spaces(text: str, replacement: str = " ") -> str:
        """Replace multiple spaces with single space."""
        pattern = re.compile(r'\s+')
        return pattern.sub(replacement, text)
    
    @staticmethod
    def replace_newlines(text: str, replacement: str = " ") -> str:
        """Replace newlines with space."""
        pattern = re.compile(r'\n+')
        return pattern.sub(replacement, text)
    
    @staticmethod
    def replace_tabs(text: str, replacement: str = " ") -> str:
        """Replace tabs with spaces."""
        pattern = re.compile(r'\t')
        return pattern.sub(replacement, text)
    
    @staticmethod
    def replace_html_tags(text: str, replacement: str = "") -> str:
        """Remove HTML tags from text."""
        pattern = re.compile(r'<[^>]+>')
        return pattern.sub(replacement, text)
    
    @staticmethod
    def replace_bbcode(text: str, replacement: str = "") -> str:
        """Remove BBCode tags from text."""
        pattern = re.compile(r'\[/?[a-z]+\]')
        return pattern.sub(replacement, text)


class TextSanitizer:
    """Text sanitization utilities."""
    
    @staticmethod
    def sanitize_for_sql(text: str) -> str:
        """Sanitize text for SQL queries."""
        # Remove potentially dangerous SQL keywords
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', 'OR', 'AND']
        for keyword in sql_keywords:
            text = re.sub(keyword, '', text, flags=re.IGNORECASE)
        
        # Remove quotes
        text = text.replace("'", "").replace('"', "")
        
        return text
    
    @staticmethod
    def sanitize_for_html(text: str) -> str:
        """Sanitize text for HTML output."""
        # HTML entity encoding
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&#x27;")
        
        return text
    
    @staticmethod
    def sanitize_for_filename(text: str) -> str:
        """Sanitize text for use as filename."""
        # Remove invalid characters
        text = re.sub(r'[<>:"/\\|?*]', '', text)
        text = text.replace(' ', '_')
        
        # Remove leading/trailing dots and spaces
        text = text.strip('. ')
        
        # Limit length
        text = text[:255]
        
        return text
    
    @staticmethod
    def sanitize_whitespace(text: str) -> str:
        """Normalize whitespace in text."""
        # Normalize unicode whitespace
        text = unicodedata.normalize('NFKC', text)
        
        # Replace all whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Trim
        text = text.strip()
        
        return text
    
    @staticmethod
    def remove_accented_chars(text: str) -> str:
        """Remove accented characters."""
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()


class PatternMatcher:
    """Pattern matching utilities."""
    
    @staticmethod
    def find_pattern(text: str, pattern: str, 
                     case_sensitive: bool = True) -> List[MatchResult]:
        """Find all pattern matches in text."""
        flags = 0 if case_sensitive else re.IGNORECASE
        compiled_pattern = re.compile(pattern, flags)
        
        results = []
        for match in compiled_pattern.finditer(text):
            results.append(MatchResult(
                matched=True,
                match=match.group(),
                groups=match.groups(),
                start=match.start(),
                end=match.end(),
                span=match.span()
            ))
        
        return results
    
    @staticmethod
    def match_pattern(text: str, pattern: str,
                     case_sensitive: bool = True) -> Optional[MatchResult]:
        """Match pattern at start of text."""
        flags = 0 if case_sensitive else re.IGNORECASE
        compiled_pattern = re.compile(pattern, flags)
        
        match = compiled_pattern.match(text)
        if match:
            return MatchResult(
                matched=True,
                match=match.group(),
                groups=match.groups(),
                start=match.start(),
                end=match.end(),
                span=match.span()
            )
        
        return None
    
    @staticmethod
    def full_match(text: str, pattern: str,
                   case_sensitive: bool = True) -> Optional[MatchResult]:
        """Check if text fully matches pattern."""
        flags = 0 if case_sensitive else re.IGNORECASE
        compiled_pattern = re.compile(pattern, flags)
        
        match = compiled_pattern.fullmatch(text)
        if match:
            return MatchResult(
                matched=True,
                match=match.group(),
                groups=match.groups(),
                start=match.start(),
                end=match.end(),
                span=match.span()
            )
        
        return None
    
    @staticmethod
    def count_matches(text: str, pattern: str,
                      case_sensitive: bool = True) -> int:
        """Count number of pattern matches."""
        flags = 0 if case_sensitive else re.IGNORECASE
        compiled_pattern = re.compile(pattern, flags)
        return len(compiled_pattern.findall(text))
    
    @staticmethod
    def split_by_pattern(text: str, pattern: str,
                          case_sensitive: bool = True) -> List[str]:
        """Split text by pattern."""
        flags = 0 if case_sensitive else re.IGNORECASE
        compiled_pattern = re.compile(pattern, flags)
        return compiled_pattern.split(text)


class LogParser:
    """Log parsing utilities."""
    
    @staticmethod
    def parse_apache_log(log_line: str) -> Optional[Dict]:
        """Parse Apache log line."""
        # Common Apache log format
        pattern = r'(\S+) (\S+) (\S+) \[([\w:/]+\s\+\d+)\] "(\S+) (\S+) (\d+)" "([^"]*)" "([^"]*)"'
        match = re.match(pattern, log_line)
        
        if match:
            return {
                "ip": match.group(1),
                "identity": match.group(2),
                "user": match.group(3),
                "timestamp": match.group(4),
                "method": match.group(5),
                "path": match.group(6),
                "status": match.group(7),
                "size": match.group(8),
                "referer": match.group(9),
                "user_agent": match.group(10)
            }
        
        return None
    
    @staticmethod
    def parse_nginx_log(log_line: str) -> Optional[Dict]:
        """Parse Nginx log line."""
        pattern = r'(\S+) - (\S+) \[([\w:/]+\s\+\d+)\] "(\S+) (\S+) (\d+)" "([^"]*)" "([^"]*)"'
        match = re.match(pattern, log_line)
        
        if match:
            return {
                "ip": match.group(1),
                "identity": match.group(2),
                "timestamp": match.group(3),
                "method": match.group(4),
                "path": match.group(5),
                "status": match.group(6),
                "size": match.group(7),
                "referer": match.group(8),
                "user_agent": match.group(9)
            }
        
        return None
    
    @staticmethod
    def parse_syslog(log_line: str) -> Optional[Dict]:
        """Parse syslog line."""
        pattern = r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(.*)'
        match = re.match(pattern, log_line)
        
        if match:
            return {
                "timestamp": match.group(1),
                "hostname": match.group(2),
                "message": match.group(3)
            }
        
        return None
    
    @staticmethod
    def extract_log_level(log_line: str) -> Optional[str]:
        """Extract log level from log line."""
        pattern = r'\b(DEBUG|INFO|WARNING|ERROR|CRITICAL|FATAL)\b'
        match = re.search(pattern, log_line, re.IGNORECASE)
        return match.group().upper() if match else None
    
    @staticmethod
    def extract_timestamp(log_line: str) -> Optional[str]:
        """Extract timestamp from log line."""
        pattern = r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}'
        match = re.search(pattern, log_line)
        return match.group() if match else None


class FilePathParser:
    """File path parsing utilities."""
    
    @staticmethod
    def extract_filename(path: str) -> str:
        """Extract filename from path."""
        pattern = r'[^/\\]+$'
        match = re.search(pattern, path)
        return match.group() if match else ""
    
    @staticmethod
    def extract_extension(path: str) -> str:
        """Extract file extension from path."""
        pattern = r'\.([^.\\/]+)$'
        match = re.search(pattern, path)
        return match.group(1) if match else ""
    
    @staticmethod
    def extract_directory(path: str) -> str:
        """Extract directory from path."""
        pattern = r'^(.+)'
        if '/' in path:
            pattern = r'^(.*/)'
        elif '\\' in path:
            pattern = r'^(.+\\)'
        
        match = re.search(pattern, path)
        directory = match.group(1) if match else ""
        
        # Remove trailing separator
        directory = directory.rstrip('/\\')
        
        return directory
    
    @staticmethod
    def normalize_path(path: str) -> str:
        """Normalize file path separators."""
        return path.replace('\\', '/')
    
    @staticmethod
    def is_absolute_path(path: str) -> bool:
        """Check if path is absolute."""
        if re.match(r'^[A-Za-z]:', path):  # Windows
            return True
        if path.startswith('/') or path.startswith('\\'):  # Unix/Windows
            return True
        return False


class CustomPatternBuilder:
    """Custom regex pattern building utilities."""
    
    @staticmethod
    def build_email_pattern(domain_whitelist: List[str] = None) -> str:
        """Build email pattern with domain whitelist."""
        base_pattern = r"[a-zA-Z0-9._%+-]+@"
        
        if domain_whitelist:
            domains = "|".join(domain_whitelist)
            return base_pattern + r"(?:\." + domains + r")"
        
        return base_pattern + r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    
    @staticmethod
    def build_phone_pattern(country_code: str = None) -> str:
        """Build phone pattern for specific country."""
        if country_code:
            return rf"\+?{country_code}[-.\s]?\(?\d{{1,4}}\)?[-.\s]?\d{{1,4}}[-.\s]?\d{{1,9}}"
        return RegexPattern.PHONE_INTL.value
    
    @staticmethod
    def build_date_pattern(format: str = "iso") -> str:
        """Build date pattern for specific format."""
        patterns = {
            "iso": r"\d{4}-\d{2}-\d{2}",
            "us": r"\d{2}/\d{2}/\d{4}",
            "eu": r"\d{2}-\d{2}-\d{4}",
            "compact": r"\d{8}"
        }
        return patterns.get(format, patterns["iso"])
    
    @staticmethod
    def build_range_pattern(min_val: int, max_val: int, 
                           length: int = None) -> str:
        """Build pattern for numeric range."""
        if length is None:
            length = len(str(max_val))
        
        return rf"[0-9]{{{length}}}" if min_val == 0 else rf"[{min_val}-{max_val}]{{{length}}}"
    
    @staticmethod
    def build_word_pattern(min_length: int, max_length: int,
                           allowed_chars: str = None) -> str:
        """Build pattern for word with length constraints."""
        if allowed_chars:
            char_class = f"[{allowed_chars}]"
        else:
            char_class = r"\w"
        
        if min_length == max_length:
            return f"{char_class}{{{min_length}}}"
        else:
            return f"{char_class}{{{min_length},{max_length}}}"


class RegexOptimizer:
    """Regex optimization utilities."""
    
    @staticmethod
    def compile_pattern(pattern: str, flags: int = 0) -> Pattern:
        """Compile regex pattern for reuse."""
        return re.compile(pattern, flags)
    
    @staticmethod
    def escape_regex_chars(text: str) -> str:
        """Escape special regex characters."""
        return re.escape(text)
    
    @staticmethod
    def optimize_for_case_insensitive(pattern: str) -> str:
        """Optimize pattern for case-insensitive matching."""
        # Convert to character class for case-insensitive alternatives
        if '|'.join([c.lower() for c in pattern]) == pattern:
            # Already lowercase
            pattern = f"(?i){pattern}"
        
        return pattern
    
    @staticmethod
    def remove_backtracking(pattern: str) -> str:
        """Remove backtracking from pattern (atomic grouping)."""
        # Replace greedy quantifiers with atomic versions
        pattern = re.sub(r'\*+', '*', pattern)
        pattern = re.sub(r'\++', '+', pattern)
        pattern = re.sub(r'\?+', '?', pattern)
        
        return pattern


def demonstrate_regex_utils():
    """Demonstrate regex utilities functionality."""
    print("=== Regex Utilities Demonstration ===\n")
    
    # Pattern Validation
    print("1. Pattern Validation:")
    validator = PatternValidator()
    
    print(f"   Email valid: {validator.validate_email('test@example.com')}")
    print(f"   URL valid: {validator.validate_url('https://example.com')}")
    print(f"   Phone US valid: {validator.validate_phone_us('(123) 456-7890')}")
    print(f"   IP valid: {validator.validate_ip_address('192.168.1.1')}")
    print(f"   MAC valid: {validator.validate_mac_address('00:1A:2B:3C:4D:5E')}")
    print(f"   Date ISO valid: {validator.validate_date_iso('2024-01-01')}")
    print(f"   Time valid: {validator.validate_time('12:30:45')}")
    print(f"   UUID valid: {validator.validate_uuid('550e8400-e29b-41d4-a716-446655440000')}")
    
    password_strength = validator.validate_password_strength("MyPass123!")
    print(f"   Password strength: {password_strength}")
    
    # Text Extraction
    print("\n2. Text Extraction:")
    text = """
    Contact us at info@example.com or support@test.com
    Visit our website at https://example.com or http://test.org
    Call us at +1-555-123-4567 or 555-987-6543
    Our IP is 192.168.1.1 or 10.0.0.1
    """
    
    extractor = TextExtractor()
    print(f"   Emails: {extractor.extract_emails(text)}")
    print(f"   URLs: {extractor.extract_urls(text)}")
    print(f"   Phones: {extractor.extract_phone_numbers(text)}")
    print(f"   IPs: {extractor.extract_ip_addresses(text)}")
    
    # Text Replacement
    print("\n3. Text Replacement:")
    sample_text = "Email me at test@example.com or visit https://example.com"
    
    replacer = TextReplacer()
    masked = replacer.replace_emails(sample_text)
    print(f"   Masked emails: {masked}")
    
    no_special = replacer.replace_special_chars("Hello! How are you?")
    print(f"   No special chars: {no_special}")
    
    # Text Sanitization
    print("\n4. Text Sanitization:")
    sanitizer = TextSanitizer()
    
    sql_safe = sanitizer.sanitize_for_sql("admin' OR '1'='1")
    print(f"   SQL safe: {sql_safe}")
    
    html_safe = sanitizer.sanitize_for_html("<script>alert('XSS')</script>")
    print(f"   HTML safe: {html_safe}")
    
    filename_safe = sanitizer.sanitize_for_filename("my/file*.txt")
    print(f"   Filename safe: {filename_safe}")
    
    no_accents = sanitizer.remove_accented_chars("café naïve")
    print(f"   No accents: {no_accents}")
    
    # Pattern Matching
    print("\n5. Pattern Matching:")
    matcher = PatternMatcher()
    
    matches = matcher.find_pattern("The price is $50 and $100", r'\$\d+')
    print(f"   Find pattern: {[m.match for m in matches]}")
    
    count = matcher.count_matches("test test test", r'test')
    print(f"   Count matches: {count}")
    
    split_result = matcher.split_by_pattern("apple,banana,cherry", r',')
    print(f"   Split by pattern: {split_result}")
    
    # Log Parsing
    print("\n6. Log Parsing:")
    apache_log = '127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0"'
    
    parsed = LogParser.parse_apache_log(apache_log)
    print(f"   Parsed Apache log: {parsed['path'] if parsed else 'Failed'}")
    
    log_level = LogParser.extract_log_level("[ERROR] Failed to connect to database")
    print(f"   Log level: {log_level}")
    
    # File Path Parsing
    print("\n7. File Path Parsing:")
    path_parser = FilePathParser()
    
    path = "/home/user/documents/file.txt"
    print(f"   Filename: {path_parser.extract_filename(path)}")
    print(f"   Extension: {path_parser.extract_extension(path)}")
    print(f"   Directory: {path_parser.extract_directory(path)}")
    print(f"   Is absolute: {path_parser.is_absolute_path(path)}")
    
    # Custom Patterns
    print("\n8. Custom Pattern Building:")
    builder = CustomPatternBuilder()
    
    custom_email = builder.build_email_pattern(["example.com", "test.com"])
    print(f"   Custom email pattern: {custom_email}")
    
    date_pattern = builder.build_date_pattern("us")
    print(f"   US date pattern: {date_pattern}")
    
    range_pattern = builder.build_range_pattern(100, 999, 3)
    print(f"   Range pattern (100-999): {range_pattern}")
    
    word_pattern = builder.build_word_pattern(3, 10, "a-z")
    print(f"   Word pattern (3-10 lowercase): {word_pattern}")
    
    # Regex Optimization
    print("\n9. Regex Optimization:")
    optimizer = RegexOptimizer()
    
    compiled = optimizer.compile_pattern(r'\d+')
    print(f"   Compiled pattern matches: {len(compiled.findall('test 123 test 456'))}")
    
    escaped = optimizer.escape_regex_chars("test.example.com")
    print(f"   Escaped: {escaped}")
    
    # Social Media Extraction
    print("\n10. Social Media Extraction:")
    social_text = "Check out #python @python_dev for amazing #programming tips!"
    
    hashtags = extractor.extract_hashtags(social_text)
    mentions = extractor.extract_mentions(social_text)
    
    print(f"   Hashtags: {hashtags}")
    print(f"   Mentions: {mentions}")
    
    print("\n=== Demonstration Complete ===")
    print("\nRegex Best Practices:")
    print("- Use compiled patterns for repeated matching")
    print("- Use raw strings for regex patterns (r'pattern')")
    print("- Be specific with patterns to avoid false positives")
    print("- Use non-greedy quantifiers (*?, +?) when appropriate")
    print("- Consider atomic grouping for performance")
    print("- Use character classes [a-z] instead of a|b|c")
    print("- Validate input patterns before processing")
    print("- Escape user input before using in regex")
    print("- Test patterns thoroughly with edge cases")
    print("- Use re.VERBOSE for debugging complex patterns")


if __name__ == "__main__":
    demonstrate_regex_utils()