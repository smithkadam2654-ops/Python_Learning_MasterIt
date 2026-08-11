#!/usr/bin/env python3
"""
Data Validation Library
Provides comprehensive data validation utilities
"""

import re
from typing import List, Dict, Any

class DataValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number (US format)."""
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_not_empty(value: Any, field_name: str) -> List[str]:
        """Validate that a value is not empty."""
        errors = []
        if not value or (isinstance(value, str) and not value.strip()):
            errors.append(f"{field_name} cannot be empty")
        return errors
    
    @staticmethod
    def validate_length(value: str, max_length: int, field_name: str) -> List[str]:
        """Validate string length."""
        errors = []
        if len(value) > max_length:
            errors.append(f"{field_name} must be {max_length} characters or less")
        return errors
    
    @staticmethod
    def validate_range(value: float, min_val: float, max_val: float, field_name: str) -> List[str]:
        """Validate numeric range."""
        errors = []
        if value < min_val or value > max_val:
            errors.append(f"{field_name} must be between {min_val} and {max_val}")
        return errors

def validate_user_data(data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate user registration data."""
    errors = {}
    
    email_error = []
    if not DataValidator.validate_email(data.get('email', '')):
        email_error.append('Invalid email format')
    if DataValidator.validate_not_empty(data.get('email'), 'Email'):
        email_error.append('Email cannot be empty')
    if DataValidator.validate_length(data.get('email', ''), 254, 'Email'):
        email_error.append('Email must be 254 characters or less')
    
    errors['email'] = email_error
    
    age_error = []
    if DataValidator.validate_range(data.get('age', 0), 13, 120, 'Age'):
        age_error.append('Age must be between 13 and 120')
    errors['age'] = age_error
    
    return {k: v for k, v in errors.items() if v}

if __name__ == "__main__":
    # Test the validator
    test_data = {
        'email': 'test@example.com',
        'age': 25
    }
    
    validation_errors = validate_user_data(test_data)
    print("Validation errors:", validation_errors)
    
    # Test with invalid data
    invalid_data = {
        'email': '',
        'age': 10
    }
    
    invalid_errors = validate_user_data(invalid_data)
    print("Invalid data errors:", invalid_errors)