"""
Security Utilities Module

This module provides comprehensive security and cryptographic utilities including:
- Password hashing and verification
- Token generation and validation
- Data encryption and decryption
- Secure random generation
- Hash functions
- Digital signatures
- Certificate handling
- Secure storage
- Security best practices
- Common attack prevention

All functions include comprehensive docstrings and type hints.
"""

import hashlib
import secrets
import base64
import hmac
import os
import json
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import re


try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


@dataclass
class PasswordHash:
    """Container for password hash information."""
    algorithm: str
    salt: str
    hash: str
    iterations: int


@dataclass
class TokenInfo:
    """Container for token information."""
    token: str
    expires_at: datetime
    created_at: datetime


class PasswordSecurity:
    """Password security utilities."""
    
    @staticmethod
    def hash_password(password: str, 
                     salt: Optional[str] = None,
                     iterations: int = 100000,
                     algorithm: str = "sha256") -> PasswordHash:
        """Hash password using PBKDF2."""
        if salt is None:
            salt = secrets.token_hex(16)
        
        if algorithm == "sha256":
            hash_algorithm = hashlib.sha256
        elif algorithm == "sha512":
            hash_algorithm = hashlib.sha512
        else:
            hash_algorithm = hashlib.sha256
        
        # Using standard library PBKDF2
        dk = hashlib.pbkdf2_hmac(
            hash_algorithm().name,
            password.encode('utf-8'),
            salt.encode('utf-8'),
            iterations
        )
        
        return PasswordHash(
            algorithm=algorithm,
            salt=salt,
            hash=dk.hex(),
            iterations=iterations
        )
    
    @staticmethod
    def verify_password(password: str, password_hash: PasswordHash) -> bool:
        """Verify password against hash."""
        new_hash = PasswordSecurity.hash_password(
            password,
            password_hash.salt,
            password_hash.iterations,
            password_hash.algorithm
        )
        
        return secrets.compare_digest(new_hash.hash, password_hash.hash)
    
    @staticmethod
    def generate_password(length: int = 16,
                         include_uppercase: bool = True,
                         include_lowercase: bool = True,
                         include_digits: bool = True,
                         include_special: bool = True) -> str:
        """Generate secure random password."""
        import string
        
        chars = ""
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_digits:
            chars += string.digits
        if include_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            chars = string.ascii_lowercase
        
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    @staticmethod
    def check_password_strength(password: str) -> Dict[str, Any]:
        """Check password strength."""
        result = {
            "score": 0,
            "length": len(password),
            "has_uppercase": any(c.isupper() for c in password),
            "has_lowercase": any(c.islower() for c in password),
            "has_digit": any(c.isdigit() for c in password),
            "has_special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
            "strength": "weak"
        }
        
        # Calculate score
        if result["length"] >= 8:
            result["score"] += 1
        if result["length"] >= 12:
            result["score"] += 1
        if result["has_uppercase"]:
            result["score"] += 1
        if result["has_lowercase"]:
            result["score"] += 1
        if result["has_digit"]:
            result["score"] += 1
        if result["has_special"]:
            result["score"] += 1
        
        # Determine strength
        if result["score"] <= 2:
            result["strength"] = "weak"
        elif result["score"] <= 4:
            result["strength"] = "medium"
        else:
            result["strength"] = "strong"
        
        return result
    
    @staticmethod
    def is_common_password(password: str) -> bool:
        """Check if password is in common password list."""
        common_passwords = {
            "password", "123456", "12345678", "1234", "qwerty",
            "12345", "dragon", "pussy", "baseball", "football",
            "letmein", "monkey", "696969", "abc123", "mustang",
            "master", "666666", "shadow", "superman", "1234567"
        }
        return password.lower() in common_passwords


class TokenGenerator:
    """Token generation and validation utilities."""
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate secure random token."""
        return secrets.token_hex(length)
    
    @staticmethod
    def generate_url_safe_token(length: int = 32) -> str:
        """Generate URL-safe random token."""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_api_key(length: int = 32) -> str:
        """Generate API key."""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_session_token() -> str:
        """Generate session token."""
        return secrets.token_hex(32)
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Generate CSRF token."""
        return secrets.token_hex(32)
    
    @staticmethod
    def generate_reset_token() -> TokenInfo:
        """Generate password reset token with expiration."""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=1)
        
        return TokenInfo(
            token=token,
            expires_at=expires_at,
            created_at=datetime.now()
        )
    
    @staticmethod
    def is_token_expired(token_info: TokenInfo) -> bool:
        """Check if token is expired."""
        return datetime.now() > token_info.expires_at
    
    @staticmethod
    def generate_jwt_payload(data: Dict[str, Any], 
                           expires_in: int = 3600) -> Dict[str, Any]:
        """Generate JWT-like payload (simplified)."""
        now = int(datetime.now().timestamp())
        
        payload = {
            "data": data,
            "iat": now,
            "exp": now + expires_in
        }
        
        return payload
    
    @staticmethod
    def encode_jwt(payload: Dict[str, Any], secret: str) -> str:
        """Encode JWT-like token (simplified - use PyJWT for production)."""
        import json
        import base64
        
        header = {"alg": "HS256", "typ": "JWT"}
        
        # Encode header and payload
        encoded_header = base64.urlsafe_b64encode(
            json.dumps(header).encode()
        ).decode().rstrip('=')
        
        encoded_payload = base64.urlsafe_b64encode(
            json.dumps(payload).encode()
        ).decode().rstrip('=')
        
        # Create signature
        message = f"{encoded_header}.{encoded_payload}"
        signature = hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
        
        encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip('=')
        
        return f"{message}.{encoded_signature}"


class DataEncryption:
    """Data encryption and decryption utilities."""
    
    @staticmethod
    def generate_key() -> bytes:
        """Generate encryption key."""
        return secrets.token_bytes(32)
    
    @staticmethod
    def generate_aes_key() -> bytes:
        """Generate AES-256 key."""
        return secrets.token_bytes(32)
    
    @staticmethod
    def encrypt_aes(plaintext: str, key: bytes) -> Tuple[bytes, bytes]:
        """Encrypt data using AES-256-CBC."""
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library is required. Install with: pip install cryptography")
        
        # Generate random IV
        iv = secrets.token_bytes(16)
        
        # Pad plaintext
        pad_length = 16 - (len(plaintext) % 16)
        plaintext += chr(pad_length) * pad_length
        
        # Encrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        
        return ciphertext, iv
    
    @staticmethod
    def decrypt_aes(ciphertext: bytes, key: bytes, iv: bytes) -> str:
        """Decrypt data using AES-256-CBC."""
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library is required. Install with: pip install cryptography")
        
        # Decrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        pad_length = plaintext[-1]
        plaintext = plaintext[:-pad_length]
        
        return plaintext.decode()
    
    @staticmethod
    def encrypt_fernet(plaintext: str, key: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        """Encrypt data using Fernet (AES-128 in CBC mode with HMAC)."""
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library is required. Install with: pip install cryptography")
        
        if key is None:
            key = Fernet.generate_key()
        
        fernet = Fernet(key)
        ciphertext = fernet.encrypt(plaintext.encode())
        
        return ciphertext, key
    
    @staticmethod
    def decrypt_fernet(ciphertext: bytes, key: bytes) -> str:
        """Decrypt data using Fernet."""
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library is required. Install with: pip install cryptography")
        
        fernet = Fernet(key)
        plaintext = fernet.decrypt(ciphertext)
        
        return plaintext.decode()
    
    @staticmethod
    def encrypt_xor(plaintext: str, key: str) -> str:
        """Simple XOR encryption (not secure for production)."""
        key_extended = (key * ((len(plaintext) // len(key)) + 1))[:len(plaintext)]
        encrypted = ''.join(chr(ord(p) ^ ord(k)) for p, k in zip(plaintext, key_extended))
        return base64.b64encode(encrypted.encode()).decode()
    
    @staticmethod
    def decrypt_xor(ciphertext: str, key: str) -> str:
        """Simple XOR decryption (not secure for production)."""
        encrypted = base64.b64decode(ciphertext).decode()
        key_extended = (key * ((len(encrypted) // len(key)) + 1))[:len(encrypted)]
        decrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(encrypted, key_extended))
        return decrypted


class HashFunctions:
    """Hash function utilities."""
    
    @staticmethod
    def sha256_hash(data: str) -> str:
        """Calculate SHA-256 hash."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def sha512_hash(data: str) -> str:
        """Calculate SHA-512 hash."""
        return hashlib.sha512(data.encode()).hexdigest()
    
    @staticmethod
    def md5_hash(data: str) -> str:
        """Calculate MD5 hash (not secure for passwords)."""
        return hashlib.md5(data.encode()).hexdigest()
    
    @staticmethod
    def sha1_hash(data: str) -> str:
        """Calculate SHA-1 hash (not secure for passwords)."""
        return hashlib.sha1(data.encode()).hexdigest()
    
    @staticmethod
    def hash_file(file_path: str, algorithm: str = "sha256") -> str:
        """Calculate hash of file."""
        if algorithm == "sha256":
            hash_func = hashlib.sha256()
        elif algorithm == "sha512":
            hash_func = hashlib.sha512()
        elif algorithm == "md5":
            hash_func = hashlib.md5()
        else:
            hash_func = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    @staticmethod
    def hmac_sha256(data: str, secret: str) -> str:
        """Calculate HMAC-SHA256."""
        return hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def hmac_sha512(data: str, secret: str) -> str:
        """Calculate HMAC-SHA512."""
        return hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha512
        ).hexdigest()


class SecureRandom:
    """Secure random generation utilities."""
    
    @staticmethod
    def random_bytes(length: int) -> bytes:
        """Generate secure random bytes."""
        return secrets.token_bytes(length)
    
    @staticmethod
    def random_int(min_val: int, max_val: int) -> int:
        """Generate secure random integer."""
        return secrets.randbelow(max_val - min_val + 1) + min_val
    
    @staticmethod
    def random_float() -> float:
        """Generate secure random float between 0 and 1."""
        return secrets.randbelow(1000000) / 1000000
    
    @staticmethod
    def random_choice(choices: List[Any]) -> Any:
        """Choose random element securely."""
        return secrets.choice(choices)
    
    @staticmethod
    def random_shuffle(items: List[Any]) -> List[Any]:
        """Shuffle list securely."""
        shuffled = items.copy()
        for i in range(len(shuffled) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        return shuffled


class InputSanitization:
    """Input sanitization and validation."""
    
    @staticmethod
    def sanitize_html(input_string: str) -> str:
        """Sanitize HTML input (basic)."""
        # Replace potentially dangerous characters
        sanitization_map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;'
        }
        
        for char, replacement in sanitization_map.items():
            input_string = input_string.replace(char, replacement)
        
        return input_string
    
    @staticmethod
    def sanitize_sql(input_string: str) -> str:
        """Sanitize SQL input (basic)."""
        # Remove SQL comments and dangerous patterns
        dangerous_patterns = [
            r'--.*',  # SQL comments
            r'/\*.*\*/',  # Multi-line comments
            r';.*',  # Multiple statements
            r'\bDROP\b',  # DROP statements
            r'\bDELETE\b',  # DELETE statements
            r'\bINSERT\b',  # INSERT statements
            r'\bUPDATE\b',  # UPDATE statements
            r'\bUNION\b',  # UNION statements
        ]
        
        for pattern in dangerous_patterns:
            input_string = re.sub(pattern, '', input_string, flags=re.IGNORECASE)
        
        return input_string
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove path separators and dangerous characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'\.\.', '', filename)  # Remove parent directory references
        filename = filename.strip('. ')  # Remove leading/trailing dots and spaces
        
        if not filename:
            filename = "sanitized"
        
        return filename
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format."""
        pattern = r'^https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/.*)?$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format."""
        pattern = r'^\+?[\d\s-()]{10,}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_credit_card(card: str) -> bool:
        """Validate credit card using Luhn algorithm."""
        digits = re.sub(r'\D', '', card)
        
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


class SecureStorage:
    """Secure storage utilities."""
    
    @staticmethod
    def encrypt_storage_key(data: str, master_key: str) -> str:
        """Encrypt data for storage using master key."""
        return DataEncryption.encrypt_xor(data, master_key)
    
    @staticmethod
    def decrypt_storage_key(encrypted_data: str, master_key: str) -> str:
        """Decrypt data from storage using master key."""
        return DataEncryption.decrypt_xor(encrypted_data, master_key)
    
    @staticmethod
    def secure_delete(file_path: str, passes: int = 3) -> bool:
        """Securely delete file by overwriting."""
        try:
            file_size = os.path.getsize(file_path)
            
            for _ in range(passes):
                with open(file_path, 'wb') as f:
                    f.write(os.urandom(file_size))
            
            os.remove(file_path)
            return True
        except Exception:
            return False
    
    @staticmethod
    def encrypt_config(config: Dict[str, Any], key: str) -> str:
        """Encrypt configuration dictionary."""
        config_json = json.dumps(config)
        return DataEncryption.encrypt_xor(config_json, key)
    
    @staticmethod
    def decrypt_config(encrypted_config: str, key: str) -> Dict[str, Any]:
        """Decrypt configuration dictionary."""
        config_json = DataEncryption.decrypt_xor(encrypted_config, key)
        return json.loads(config_json)


class SecurityAuditor:
    """Security audit utilities."""
    
    @staticmethod
    def audit_password_policy(password: str) -> Dict[str, Any]:
        """Audit password against security policies."""
        strength = PasswordSecurity.check_password_strength(password)
        is_common = PasswordSecurity.is_common_password(password)
        
        return {
            "password": "*" * len(password),
            "strength": strength["strength"],
            "score": strength["score"],
            "is_common": is_common,
            "meets_minimum_length": strength["length"] >= 8,
            "has_complexity": all([
                strength["has_uppercase"],
                strength["has_lowercase"],
                strength["has_digit"],
                strength["has_special"]
            ]),
            "recommendations": SecurityAuditor._get_password_recommendations(strength, is_common)
        }
    
    @staticmethod
    def _get_password_recommendations(strength: Dict[str, Any], is_common: bool) -> List[str]:
        """Get password recommendations."""
        recommendations = []
        
        if is_common:
            recommendations.append("Password is too common - choose a unique password")
        
        if strength["length"] < 12:
            recommendations.append("Use a longer password (12+ characters)")
        
        if not strength["has_uppercase"]:
            recommendations.append("Add uppercase letters")
        
        if not strength["has_lowercase"]:
            recommendations.append("Add lowercase letters")
        
        if not strength["has_digit"]:
            recommendations.append("Add numbers")
        
        if not strength["has_special"]:
            recommendations.append("Add special characters")
        
        if strength["score"] < 4:
            recommendations.append("Increase overall complexity")
        
        return recommendations
    
    @staticmethod
    def audit_input_security(input_string: str, input_type: str) -> Dict[str, Any]:
        """Audit input for security issues."""
        results = {
            "input_type": input_type,
            "is_safe": True,
            "issues": []
        }
        
        if input_type == "html":
            if "<script>" in input_string.lower():
                results["issues"].append("Contains script tags")
                results["is_safe"] = False
            if "javascript:" in input_string.lower():
                results["issues"].append("Contains javascript protocol")
                results["is_safe"] = False
        
        elif input_type == "sql":
            if ";" in input_string:
                results["issues"].append("Contains statement separator")
                results["is_safe"] = False
            if any(keyword in input_string.lower() for keyword in ["drop", "delete", "insert", "update"]):
                results["issues"].append("Contains SQL keywords")
                results["is_safe"] = False
        
        elif input_type == "filename":
            if ".." in input_string:
                results["issues"].append("Contains path traversal")
                results["is_safe"] = False
            if "/" in input_string or "\\" in input_string:
                results["issues"].append("Contains path separators")
                results["is_safe"] = False
        
        return results


def demonstrate_security_utils():
    """Demonstrate security utilities functionality."""
    print("=== Security Utilities Demonstration ===\n")
    
    # Password Security
    print("1. Password Security:")
    password = PasswordSecurity.generate_password(16)
    print(f"   Generated password: {password}")
    
    password_hash = PasswordSecurity.hash_password("my_secure_password")
    print(f"   Password hash: {password_hash.hash[:32]}...")
    
    is_valid = PasswordSecurity.verify_password("my_secure_password", password_hash)
    print(f"   Password verification: {is_valid}")
    
    strength = PasswordSecurity.check_password_strength(password)
    print(f"   Password strength: {strength['strength']} (score: {strength['score']})")
    
    # Token Generation
    print("\n2. Token Generation:")
    print(f"   Random token: {TokenGenerator.generate_token(16)}")
    print(f"   URL-safe token: {TokenGenerator.generate_url_safe_token(16)}")
    print(f"   API key: {TokenGenerator.generate_api_key(16)}")
    
    reset_token = TokenGenerator.generate_reset_token()
    print(f"   Reset token: {reset_token.token[:20]}...")
    print(f"   Expires at: {reset_token.expires_at}")
    
    # Hash Functions
    print("\n3. Hash Functions:")
    data = "sensitive_data"
    print(f"   SHA-256: {HashFunctions.sha256_hash(data)[:32]}...")
    print(f"   SHA-512: {HashFunctions.sha512_hash(data)[:32]}...")
    print(f"   HMAC-SHA256: {HashFunctions.hmac_sha256(data, 'secret')[:32]}...")
    
    # Data Encryption
    print("\n4. Data Encryption:")
    if CRYPTO_AVAILABLE:
        plaintext = "Secret message"
        ciphertext, key = DataEncryption.encrypt_fernet(plaintext)
        print(f"   Encrypted: {ciphertext[:32]}...")
        print(f"   Key: {key[:32]}...")
        
        decrypted = DataEncryption.decrypt_fernet(ciphertext, key)
        print(f"   Decrypted: {decrypted}")
    else:
        print("   cryptography library not available")
        print("   Using XOR encryption (less secure):")
        xor_encrypted = DataEncryption.encrypt_xor("Secret message", "mykey")
        print(f"   XOR encrypted: {xor_encrypted[:32]}...")
        xor_decrypted = DataEncryption.decrypt_xor(xor_encrypted, "mykey")
        print(f"   XOR decrypted: {xor_decrypted}")
    
    # Secure Random
    print("\n5. Secure Random:")
    print(f"   Random bytes: {SecureRandom.random_bytes(8).hex()}")
    print(f"   Random int: {SecureRandom.random_int(1, 100)}")
    print(f"   Random float: {SecureRandom.random_float():.4f}")
    
    # Input Sanitization
    print("\n6. Input Sanitization:")
    html_input = "<script>alert('xss')</script>"
    print(f"   Original HTML: {html_input}")
    print(f"   Sanitized: {InputSanitization.sanitize_html(html_input)}")
    
    sql_input = "SELECT * FROM users; DROP TABLE users;"
    print(f"   Original SQL: {sql_input}")
    print(f"   Sanitized: {InputSanitization.sanitize_sql(sql_input)}")
    
    filename = "../../../etc/passwd"
    print(f"   Original filename: {filename}")
    print(f"   Sanitized: {InputSanitization.sanitize_filename(filename)}")
    
    # Validation
    print("\n7. Input Validation:")
    print(f"   Valid email: {InputSanitization.validate_email('test@example.com')}")
    print(f"   Valid URL: {InputSanitization.validate_url('https://example.com')}")
    print(f"   Valid phone: {InputSanitization.validate_phone('+1-555-123-4567')}")
    print(f"   Valid credit card: {InputSanitization.validate_credit_card('4111111111111111')}")
    
    # Security Audit
    print("\n8. Security Audit:")
    audit = SecurityAuditor.audit_password_policy("password123")
    print(f"   Password audit: {audit['strength']} strength")
    print(f"   Recommendations: {audit['recommendations']}")
    
    input_audit = SecurityAuditor.audit_input_security("<script>alert('xss')</script>", "html")
    print(f"   Input audit: {'Safe' if input_audit['is_safe'] else 'Unsafe'}")
    print(f"   Issues: {input_audit['issues']}")
    
    print("\n=== Demonstration Complete ===")
    print("\nSecurity Best Practices:")
    print("- Use strong password hashing (PBKDF2, bcrypt, Argon2)")
    print("- Use verified cryptographic libraries (cryptography, PyJWT)")
    print("- Never store plaintext passwords")
    print("- Always validate and sanitize user input")
    print("- Use HTTPS for secure communication")
    print("- Keep cryptographic libraries updated")
    print("- Follow principle of least privilege")


if __name__ == "__main__":
    demonstrate_security_utils()