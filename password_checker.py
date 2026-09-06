"""
Password Strength Checker - Password validation and strength analysis.
Features: Complexity checking, common password detection, and suggestions.
"""

import re
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class PasswordStrength(Enum):
    """Password strength levels."""
    VERY_WEAK = "Very Weak"
    WEAK = "Weak"
    FAIR = "Fair"
    GOOD = "Good"
    STRONG = "Strong"
    VERY_STRONG = "Very Strong"


@dataclass
class PasswordResult:
    """Password check result."""
    strength: PasswordStrength
    score: int
    issues: List[str]
    suggestions: List[str]
    
    def __str__(self) -> str:
        """String representation."""
        return f"Strength: {self.strength.value} (Score: {self.score}/100)"


class PasswordChecker:
    """Password strength checker."""
    
    # Common weak passwords
    COMMON_PASSWORDS = {
        "password", "123456", "12345678", "qwerty", "abc123",
        "monkey", "letmein", "dragon", "111111", "baseball",
        "iloveyou", "trustno1", "sunshine", "master", "hello",
        "football", "princess", "admin", "welcome", "shadow",
        "ashley", "football", "jesus", "michael", "ninja",
        "mustang", "password1", "123456789", "adobe123"
    }
    
    def __init__(self) -> None:
        """Initialize password checker."""
        self.min_length = 8
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_numbers = True
        self.require_special = True
    
    def check_password(self, password: str) -> PasswordResult:
        """
        Check password strength.
        
        Args:
            password: Password to check
            
        Returns:
            Password check result
        """
        issues = []
        suggestions = []
        score = 100
        
        # Check for common passwords
        if password.lower() in self.COMMON_PASSWORDS:
            issues.append("Password is too common")
            suggestions.append("Choose a more unique password")
            score -= 50
            return PasswordResult(PasswordStrength.VERY_WEAK, max(0, score), issues, suggestions)
        
        # Check length
        if len(password) < self.min_length:
            issues.append(f"Password must be at least {self.min_length} characters")
            suggestions.append(f"Add {self.min_length - len(password)} more characters")
            score -= 20
        elif len(password) < 12:
            suggestions.append("Consider using 12+ characters for better security")
        elif len(password) >= 16:
            score += 10
        
        # Check character types
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_number = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        if self.require_uppercase and not has_upper:
            issues.append("Password must contain uppercase letters")
            suggestions.append("Add uppercase letters (A-Z)")
            score -= 15
        
        if self.require_lowercase and not has_lower:
            issues.append("Password must contain lowercase letters")
            suggestions.append("Add lowercase letters (a-z)")
            score -= 15
        
        if self.require_numbers and not has_number:
            issues.append("Password must contain numbers")
            suggestions.append("Add numbers (0-9)")
            score -= 15
        
        if self.require_special and not has_special:
            issues.append("Password must contain special characters")
            suggestions.append("Add special characters (!@#$%^&*)")
            score -= 15
        
        # Check for repeated characters
        if self._has_repeated_chars(password):
            issues.append("Password contains repeated characters")
            suggestions.append("Avoid repeating characters")
            score -= 10
        
        # Check for sequential characters
        if self._has_sequential_chars(password):
            issues.append("Password contains sequential characters")
            suggestions.append("Avoid sequential characters (123, abc)")
            score -= 10
        
        # Check for patterns
        if self._has_keyboard_patterns(password):
            issues.append("Password contains keyboard patterns")
            suggestions.append("Avoid keyboard patterns (qwerty, asdf)")
            score -= 10
        
        # Bonus for variety
        variety_count = sum([has_upper, has_lower, has_number, has_special])
        if variety_count == 4:
            score += 10
        elif variety_count == 3:
            score += 5
        
        # Determine strength
        strength = self._determine_strength(score)
        
        # Add suggestions if no issues
        if not issues and strength in (PasswordStrength.WEAK, PasswordStrength.FAIR):
            suggestions.append("Add more character types for stronger password")
        
        return PasswordResult(strength, max(0, score), issues, suggestions)
    
    def _has_repeated_chars(self, password: str) -> bool:
        """Check for repeated characters."""
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
    
    def _has_sequential_chars(self, password: str) -> bool:
        """Check for sequential characters."""
        for i in range(len(password) - 2):
            if (ord(password[i+1]) == ord(password[i]) + 1 and
                ord(password[i+2]) == ord(password[i]) + 2):
                return True
        return False
    
    def _has_keyboard_patterns(self, password: str) -> bool:
        """Check for keyboard patterns."""
        patterns = ['qwerty', 'asdfgh', 'zxcvbn', '123456', 'qwertyuiop']
        password_lower = password.lower()
        for pattern in patterns:
            if pattern in password_lower:
                return True
        return False
    
    def _determine_strength(self, score: int) -> PasswordStrength:
        """Determine strength from score."""
        if score >= 90:
            return PasswordStrength.VERY_STRONG
        elif score >= 75:
            return PasswordStrength.STRONG
        elif score >= 60:
            return PasswordStrength.GOOD
        elif score >= 45:
            return PasswordStrength.FAIR
        elif score >= 30:
            return PasswordStrength.WEAK
        else:
            return PasswordStrength.VERY_WEAK
    
    def generate_suggestions(self, password: str) -> List[str]:
        """
        Generate password improvement suggestions.
        
        Args:
            password: Current password
            
        Returns:
            List of suggestions
        """
        result = self.check_password(password)
        return result.suggestions
    
    def is_acceptable(self, password: str) -> bool:
        """
        Check if password meets minimum requirements.
        
        Args:
            password: Password to check
            
        Returns:
            True if acceptable
        """
        result = self.check_password(password)
        return len(result.issues) == 0


class PasswordGenerator:
    """Password generator."""
    
    def __init__(self) -> None:
        """Initialize password generator."""
        import random
        self.random = random
    
    def generate(self, length: int = 16, include_upper: bool = True,
                 include_lower: bool = True, include_numbers: bool = True,
                 include_special: bool = True) -> str:
        """
        Generate random password.
        
        Args:
            length: Password length
            include_upper: Include uppercase
            include_lower: Include lowercase
            include_numbers: Include numbers
            include_special: Include special characters
            
        Returns:
            Generated password
        """
        import string
        
        chars = ""
        if include_lower:
            chars += string.ascii_lowercase
        if include_upper:
            chars += string.ascii_uppercase
        if include_numbers:
            chars += string.digits
        if include_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            chars = string.ascii_letters
        
        password = ''.join(self.random.choice(chars) for _ in range(length))
        return password
    
    def generate_passphrase(self, word_count: int = 4, separator: str = "-") -> str:
        """
        Generate passphrase from random words.
        
        Args:
            word_count: Number of words
            separator: Word separator
            
        Returns:
            Generated passphrase
        """
        words = [
            "correct", "horse", "battery", "staple", "purple", "elephant",
            "guitar", "planet", "coffee", "window", "dragon", "mountain",
            "river", "forest", "ocean", "thunder", "crystal", "diamond",
            "shadow", "whisper", "breeze", "autumn", "winter", "summer"
        ]
        
        selected = self.random.sample(words, min(word_count, len(words)))
        return separator.join(selected)


def main() -> None:
    """Demonstrate password checker."""
    
    print("=== Password Strength Checker Demo ===")
    
    checker = PasswordChecker()
    
    # Test passwords
    test_passwords = [
        "password",
        "12345678",
        "Password1",
        "MyP@ssw0rd!",
        "Correct-Horse-Battery-Staple",
        "Th1s!s@Str0ng#P@ssw0rd",
        "qwerty123",
        "aaa111"
    ]
    
    for password in test_passwords:
        print(f"\nPassword: '{password}'")
        result = checker.check_password(password)
        print(result)
        
        if result.issues:
            print("Issues:")
            for issue in result.issues:
                print(f"  - {issue}")
        
        if result.suggestions:
            print("Suggestions:")
            for suggestion in result.suggestions:
                print(f"  - {suggestion}")
    
    print("\n=== Password Generator ===")
    
    generator = PasswordGenerator()
    
    print("\nRandom passwords:")
    for i in range(5):
        password = generator.generate(16)
        result = checker.check_password(password)
        print(f"{password} - {result.strength.value}")
    
    print("\nPassphrases:")
    for i in range(3):
        passphrase = generator.generate_passphrase()
        result = checker.check_password(passphrase)
        print(f"{passphrase} - {result.strength.value}")


if __name__ == "__main__":
    main()
