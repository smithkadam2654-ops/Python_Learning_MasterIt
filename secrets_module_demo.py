import secrets
import string

def demonstrate_secrets():
    """Demonstrate generating cryptographically strong random numbers/tokens."""
    
    print("WARNING: The standard 'random' module is NOT secure for passwords or tokens!")
    print("Always use the 'secrets' module for security-sensitive applications.\n")
    
    print("--- 1. Secure Random Tokens ---")
    # Generate a secure URL-safe text string (great for password resets or API keys)
    url_token = secrets.token_urlsafe(32)
    print(f"URL-Safe Token: {url_token}")
    
    # Generate a secure hexadecimal string (great for session IDs)
    hex_token = secrets.token_hex(32)
    print(f"Hex Token:      {hex_token}")
    
    print("\n--- 2. Secure Random Selection ---")
    # Generate a secure random password
    alphabet = string.ascii_letters + string.digits + string.punctuation
    
    # We use secrets.choice instead of random.choice
    # We create a 16-character password by choosing randomly from the alphabet 16 times
    secure_password = ''.join(secrets.choice(alphabet) for i in range(16))
    
    print(f"Secure randomly generated password: {secure_password}")

if __name__ == "__main__":
    demonstrate_secrets()
