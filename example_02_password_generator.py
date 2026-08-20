import random
import string

def generate_password(length=12, include_special=True):
    """Generates a strong, random password."""
    # Define character sets
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation if include_special else ""
    
    # Combine all allowed characters
    all_chars = letters + digits + special_chars
    
    # Ensure at least one of each type is included to meet basic strength requirements
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits)
    ]
    
    if include_special:
        password.append(random.choice(string.punctuation))
        
    # Fill the rest of the password length
    password += [random.choice(all_chars) for _ in range(length - len(password))]
    
    # Shuffle the characters to ensure randomness
    random.shuffle(password)
    
    return "".join(password)

if __name__ == "__main__":
    print(f"Generated Password (12 chars): {generate_password(12)}")
    print(f"Generated Password (16 chars): {generate_password(16)}")
    print(f"Generated Password (no special chars): {generate_password(12, include_special=False)}")
