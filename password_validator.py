#!/usr/bin/env python3
"""
Password Validator Program
Validates passwords and checks their strength
"""

import re

def contains_uppercase(password):
    return any(char.isupper() for char in password)

def contains_lowercase(password):
    return any(char.islower() for char in password)

def contains_digit(password):
    return any(char.isdigit() for char in password)

def contains_special_char(password):
    special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
    return any(char in special_chars for char in password)

def check_password_strength(password):
    """Check password strength and return score and feedback."""
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")
    
    if len(password) >= 12:
        score += 1
    
    if contains_uppercase(password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    if contains_lowercase(password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    if contains_digit(password):
        score += 1
    else:
        feedback.append("Add numbers")
    
    if contains_special_char(password):
        score += 1
    else:
        feedback.append("Add special characters")
    
    return score, feedback

def is_common_password(password):
    """Check against common passwords."""
    common_passwords = [
        'password', '123456', 'qwerty', 'admin', 'welcome',
        '12345678', 'abc123', 'password123', 'letmein', 'monkey'
    ]
    return password.lower() in common_passwords

def main():
    print("=== Password Validator ===")
    
    while True:
        password = input("Enter a password (or press Enter to quit): ")
        
        if not password:
            print("Goodbye!")
            break
        
        if len(password) == 0:
            print("Please enter a password!")
            continue
        
        if is_common_password(password):
            print("❌ This is a common password! Choose a stronger one.")
            continue
        
        score, feedback = check_password_strength(password)
        
        print(f"\nPassword Analysis:")
        print(f"Length: {len(password)} characters")
        
        strength_levels = {
            6: "Very Strong",
            5: "Strong",
            4: "Good",
            3: "Fair",
            2: "Weak",
            1: "Very Weak",
            0: "Very Weak"
        }
        
        strength = strength_levels.get(score, "Very Weak")
        print(f"Strength: {strength}")
        
        if feedback:
            print("\nSuggestions:")
            for suggestion in feedback:
                print(f"  • {suggestion}")
        else:
            print("✅ Password is strong!")
        
        print("-" * 40)

if __name__ == "__main__":
    main()