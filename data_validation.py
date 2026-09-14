"""
Data Validation - Data validation and sanitization utilities.
Features: Type checking, format validation, range validation, and data cleaning.
"""

from typing import Any, List, Optional, Callable
import re
from datetime import datetime


class ValidationError(Exception):
    """Custom validation error."""
    pass


class Validator:
    """Data validator implementation."""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email string
            
        Returns:
            True if valid email format
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """
        Validate phone number format (US format).
        
        Args:
            phone: Phone string
            
        Returns:
            True if valid phone format
        """
        pattern = r'^\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url: URL string
            
        Returns:
            True if valid URL format
        """
        pattern = r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
        return re.match(pattern, url) is not None
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """
        Validate IPv4 address.
        
        Args:
            ip: IP address string
            
        Returns:
            True if valid IPv4
        """
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_credit_card(card: str) -> bool:
        """
        Validate credit card using Luhn algorithm.
        
        Args:
            card: Card number string
            
        Returns:
            True if valid card number
        """
        # Remove spaces and dashes
        card = re.sub(r'[\s-]', '', card)
        
        if not card.isdigit() or len(card) < 13 or len(card) > 19:
            return False
        
        # Luhn algorithm
        total = 0
        reverse_digits = card[::-1]
        
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        
        return total % 10 == 0
    
    @staticmethod
    def is_valid_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
        """
        Validate date string format.
        
        Args:
            date_str: Date string
            format: Date format string
            
        Returns:
            True if valid date
        """
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_username(username: str, min_len: int = 3, max_len: int = 20) -> bool:
        """
        Validate username (alphanumeric with underscores).
        
        Args:
            username: Username string
            min_len: Minimum length
            max_len: Maximum length
            
        Returns:
            True if valid username
        """
        pattern = f'^[a-zA-Z0-9_]+{{{min_len},{max_len}}}$'
        return re.match(pattern, username) is not None
    
    @staticmethod
    def is_valid_password(password: str, min_len: int = 8) -> bool:
        """
        Validate password strength.
        
        Args:
            password: Password string
            min_len: Minimum length
            
        Returns:
            True if meets requirements
        """
        if len(password) < min_len:
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        return has_upper and has_lower and has_digit and has_special
    
    @staticmethod
    def is_valid_json(json_str: str) -> bool:
        """
        Validate JSON string.
        
        Args:
            json_str: JSON string
            
        Returns:
            True if valid JSON
        """
        import json
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False
    
    @staticmethod
    def is_valid_uuid(uuid_str: str) -> bool:
        """
        Validate UUID format.
        
        Args:
            uuid_str: UUID string
            
        Returns:
            True if valid UUID
        """
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return re.match(pattern, uuid_str.lower()) is not None
    
    @staticmethod
    def is_valid_hex(hex_str: str) -> bool:
        """
        Validate hexadecimal string.
        
        Args:
            hex_str: Hex string
            
        Returns:
            True if valid hex
        """
        pattern = r'^0x[0-9a-fA-F]+$|^[0-9a-fA-F]+$'
        return re.match(pattern, hex_str) is not None
    
    @staticmethod
    def is_valid_base64(base64_str: str) -> bool:
        """
        Validate base64 string.
        
        Args:
            base64_str: Base64 string
            
        Returns:
            True if valid base64
        """
        import base64
        try:
            # Pad if necessary
            padding = 4 - len(base64_str) % 4
            if padding != 4:
                base64_str += '=' * padding
            
            base64.b64decode(base64_str)
            return True
        except Exception:
            return False


class DataSanitizer:
    """Data sanitization utilities."""
    
    @staticmethod
    def sanitize_string(s: str, allowed_chars: str = None) -> str:
        """
        Sanitize string by removing disallowed characters.
        
        Args:
            s: Input string
            allowed_chars: Allowed characters (default: alphanumeric and space)
            
        Returns:
            Sanitized string
        """
        if allowed_chars is None:
            allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
        
        return ''.join(c for c in s if c in allowed_chars)
    
    @staticmethod
    def sanitize_html(s: str) -> str:
        """
        Sanitize HTML by escaping special characters.
        
        Args:
            s: Input string
            
        Returns:
            Sanitized string
        """
        s = s.replace('&', '&amp;')
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
        s = s.replace('"', '&quot;')
        s = s.replace("'", '&#x27;')
        return s
    
    @staticmethod
    def sanitize_sql(s: str) -> str:
        """
        Sanitize SQL input (basic escaping).
        
        Args:
            s: Input string
            
        Returns:
            Sanitized string
            
        Note: This is basic sanitization. Use parameterized queries in production.
        """
        return s.replace("'", "''")
    
    @staticmethod
    def remove_whitespace(s: str) -> str:
        """
        Remove all whitespace from string.
        
        Args:
            s: Input string
            
        Returns:
            String without whitespace
        """
        return re.sub(r'\s+', '', s)
    
    @staticmethod
    def normalize_whitespace(s: str) -> str:
        """
        Normalize whitespace to single spaces.
        
        Args:
            s: Input string
            
        Returns:
            String with normalized whitespace
        """
        return ' '.join(s.split())
    
    @staticmethod
    def trim_string(s: str, max_length: int) -> str:
        """
        Trim string to maximum length.
        
        Args:
            s: Input string
            max_length: Maximum length
            
        Returns:
            Trimmed string
        """
        if len(s) <= max_length:
            return s
        return s[:max_length - 3] + '...'
    
    @staticmethod
    def mask_email(email: str) -> str:
        """
        Mask email for privacy.
        
        Args:
            email: Email string
            
        Returns:
            Masked email
        """
        parts = email.split('@')
        if len(parts) != 2:
            return email
        
        username, domain = parts
        if len(username) <= 2:
            masked = '*' * len(username)
        else:
            masked = username[0] + '*' * (len(username) - 2) + username[-1]
        
        return f"{masked}@{domain}"
    
    @staticmethod
    def mask_credit_card(card: str) -> str:
        """
        Mask credit card number.
        
        Args:
            card: Card number string
            
        Returns:
            Masked card number
        """
        card = re.sub(r'[\s-]', '', card)
        if len(card) < 4:
            return card
        
        return '*' * (len(card) - 4) + card[-4:]


class DataValidator:
    """Generic data validator with rules."""
    
    def __init__(self) -> None:
        """Initialize data validator."""
        self.rules: List[Callable] = []
        self.errors: List[str] = []
    
    def add_rule(self, rule: Callable, error_message: str) -> 'DataValidator':
        """
        Add validation rule.
        
        Args:
            rule: Validation function (returns bool)
            error_message: Error message if validation fails
            
        Returns:
            Self for chaining
        """
        self.rules.append((rule, error_message))
        return self
    
    def validate(self, data: Any) -> bool:
        """
        Validate data against all rules.
        
        Args:
            data: Data to validate
            
        Returns:
            True if all rules pass
        """
        self.errors = []
        
        for rule, error_message in self.rules:
            if not rule(data):
                self.errors.append(error_message)
        
        return len(self.errors) == 0
    
    def get_errors(self) -> List[str]:
        """Get validation errors."""
        return self.errors


class RangeValidator:
    """Range validation utilities."""
    
    @staticmethod
    def validate_range(value: int, min_val: int, max_val: int) -> bool:
        """
        Validate value is within range.
        
        Args:
            value: Value to check
            min_val: Minimum value
            max_val: Maximum value
            
        Returns:
            True if in range
        """
        return min_val <= value <= max_val
    
    @staticmethod
    def validate_length(value: str, min_len: int, max_len: int) -> bool:
        """
        Validate string length.
        
        Args:
            value: String to check
            min_len: Minimum length
            max_len: Maximum length
            
        Returns:
            True if length in range
        """
        return min_len <= len(value) <= max_len
    
    @staticmethod
    def validate_positive(value: int) -> bool:
        """
        Validate value is positive.
        
        Args:
            value: Value to check
            
        Returns:
            True if positive
        """
        return value > 0
    
    @staticmethod
    def validate_non_negative(value: int) -> bool:
        """
        Validate value is non-negative.
        
        Args:
            value: Value to check
            
        Returns:
            True if non-negative
        """
        return value >= 0


def main() -> None:
    """Demonstrate data validation."""
    
    print("=== Data Validation Demo ===")
    
    # Email validation
    print("\n--- Email Validation ---")
    emails = ["test@example.com", "invalid-email", "user@domain.co.uk"]
    for email in emails:
        print(f"'{email}': {Validator.is_valid_email(email)}")
    
    # Phone validation
    print("\n--- Phone Validation ---")
    phones = ["(123) 456-7890", "123-456-7890", "1234567890", "invalid"]
    for phone in phones:
        print(f"'{phone}': {Validator.is_valid_phone(phone)}")
    
    # Credit card validation
    print("\n--- Credit Card Validation ---")
    cards = ["4532015112830366", "1234567890123456"]  # First is valid test card
    for card in cards:
        print(f"'{card}': {Validator.is_valid_credit_card(card)}")
    
    # Password validation
    print("\n--- Password Validation ---")
    passwords = ["weak", "Strong123!", "StrongPass123"]
    for pwd in passwords:
        print(f"'{pwd}': {Validator.is_valid_password(pwd)}")
    
    # Sanitization
    print("\n--- Sanitization ---")
    html = "<script>alert('xss')</script>"
    print(f"HTML: '{html}'")
    print(f"Sanitized: '{DataSanitizer.sanitize_html(html)}'")
    
    email = "john.doe@example.com"
    print(f"\nEmail: '{email}'")
    print(f"Masked: '{DataSanitizer.mask_email(email)}'")
    
    card = "4532015112830366"
    print(f"\nCard: '{card}'")
    print(f"Masked: '{DataSanitizer.mask_credit_card(card)}'")
    
    # Custom validator
    print("\n--- Custom Validator ---")
    validator = DataValidator()
    validator.add_rule(lambda x: len(x) >= 8, "Password too short")
    validator.add_rule(lambda x: any(c.isdigit() for c in x), "Must contain digit")
    
    password = "password"
    result = validator.validate(password)
    print(f"Password: '{password}'")
    print(f"Valid: {result}")
    print(f"Errors: {validator.get_errors()}")
    
    # Range validation
    print("\n--- Range Validation ---")
    print(f"5 in range 1-10: {RangeValidator.validate_range(5, 1, 10)}")
    print(f"15 in range 1-10: {RangeValidator.validate_range(15, 1, 10)}")
    print(f"'hello' length 3-10: {RangeValidator.validate_length('hello', 3, 10)}")
    print(f"'hi' length 3-10: {RangeValidator.validate_length('hi', 3, 10)}")


if __name__ == "__main__":
    main()
