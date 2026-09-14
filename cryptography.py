"""
Cryptography - Encryption, decryption, and hashing utilities.
Features: Symmetric encryption, hashing, digital signatures, and common crypto operations.
"""

from typing import Optional, Tuple
import hashlib
import hmac
import base64
from secrets import token_bytes, token_hex


class HashUtils:
    """Hash function utilities."""
    
    @staticmethod
    def md5(text: str) -> str:
        """
        Calculate MD5 hash (not recommended for security).
        
        Args:
            text: Input text
            
        Returns:
            MD5 hash hex string
        """
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def sha1(text: str) -> str:
        """
        Calculate SHA-1 hash (not recommended for security).
        
        Args:
            text: Input text
            
        Returns:
            SHA-1 hash hex string
        """
        return hashlib.sha1(text.encode()).hexdigest()
    
    @staticmethod
    def sha256(text: str) -> str:
        """
        Calculate SHA-256 hash.
        
        Args:
            text: Input text
            
        Returns:
            SHA-256 hash hex string
        """
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def sha512(text: str) -> str:
        """
        Calculate SHA-512 hash.
        
        Args:
            text: Input text
            
        Returns:
            SHA-512 hash hex string
        """
        return hashlib.sha512(text.encode()).hexdigest()
    
    @staticmethod
    def sha256_file(file_path: str) -> str:
        """
        Calculate SHA-256 hash of file.
        
        Args:
            file_path: Path to file
            
        Returns:
            SHA-256 hash hex string
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
    
    @staticmethod
    def hmac_sha256(key: str, message: str) -> str:
        """
        Calculate HMAC-SHA256.
        
        Args:
            key: Secret key
            message: Message to authenticate
            
        Returns:
            HMAC hex string
        """
        return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    @staticmethod
    def compare_hashes(hash1: str, hash2: str) -> bool:
        """
        Compare two hashes securely (timing attack resistant).
        
        Args:
            hash1: First hash
            hash2: Second hash
            
        Returns:
            True if hashes match
        """
        return hmac.compare_digest(hash1.encode(), hash2.encode())


class PasswordUtils:
    """Password hashing utilities."""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """
        Hash password using PBKDF2.
        
        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)
            
        Returns:
            Tuple of (salt, hashed_password)
        """
        if salt is None:
            salt = token_hex(16)
        
        # PBKDF2 with SHA-256, 100000 iterations
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000
        ).hex()
        
        return (salt, hashed)
    
    @staticmethod
    def verify_password(password: str, salt: str, hashed_password: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password: Password to verify
            salt: Salt used in hashing
            hashed_password: Hashed password to compare
            
        Returns:
            True if password matches
        """
        _, computed_hash = PasswordUtils.hash_password(password, salt)
        return HashUtils.compare_hashes(computed_hash, hashed_password)


class EncodingUtils:
    """Encoding and decoding utilities."""
    
    @staticmethod
    def base64_encode(text: str) -> str:
        """
        Encode text to base64.
        
        Args:
            text: Input text
            
        Returns:
            Base64 encoded string
        """
        return base64.b64encode(text.encode()).decode()
    
    @staticmethod
    def base64_decode(encoded: str) -> str:
        """
        Decode base64 string.
        
        Args:
            encoded: Base64 encoded string
            
        Returns:
            Decoded text
        """
        return base64.b64decode(encoded).decode()
    
    @staticmethod
    def base64_url_encode(text: str) -> str:
        """
        Encode text to URL-safe base64.
        
        Args:
            text: Input text
            
        Returns:
            URL-safe base64 encoded string
        """
        return base64.urlsafe_b64encode(text.encode()).decode()
    
    @staticmethod
    def base64_url_decode(encoded: str) -> str:
        """
        Decode URL-safe base64 string.
        
        Args:
            encoded: URL-safe base64 encoded string
            
        Returns:
            Decoded text
        """
        return base64.urlsafe_b64decode(encoded).decode()
    
    @staticmethod
    def hex_encode(text: str) -> str:
        """
        Encode text to hexadecimal.
        
        Args:
            text: Input text
            
        Returns:
            Hex encoded string
        """
        return text.encode().hex()
    
    @staticmethod
    def hex_decode(encoded: str) -> str:
        """
        Decode hexadecimal string.
        
        Args:
            encoded: Hex encoded string
            
        Returns:
            Decoded text
        """
        return bytes.fromhex(encoded).decode()


class RandomUtils:
    """Cryptographic random utilities."""
    
    @staticmethod
    def random_bytes(length: int) -> bytes:
        """
        Generate cryptographically secure random bytes.
        
        Args:
            length: Number of bytes
            
        Returns:
            Random bytes
        """
        return token_bytes(length)
    
    @staticmethod
    def random_hex(length: int) -> str:
        """
        Generate cryptographically secure random hex string.
        
        Args:
            length: Number of bytes (hex string will be 2x length)
            
        Returns:
            Random hex string
        """
        return token_hex(length)
    
    @staticmethod
    def random_token(length: int = 32) -> str:
        """
        Generate random token (URL-safe base64).
        
        Args:
            length: Number of bytes
            
        Returns:
            Random token
        """
        return base64.urlsafe_b64encode(token_bytes(length)).decode().rstrip('=')
    
    @staticmethod
    def generate_uuid() -> str:
        """
        Generate UUID4.
        
        Returns:
            UUID string
        """
        import uuid
        return str(uuid.uuid4())


class CipherUtils:
    """Simple cipher utilities (for educational purposes)."""
    
    @staticmethod
    def caesar_cipher(text: str, shift: int) -> str:
        """
        Caesar cipher (shift each letter).
        
        Args:
            text: Input text
            shift: Shift amount
            
        Returns:
            Encrypted text
        """
        result = []
        
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - base + shift) % 26
                result.append(chr(base + shifted))
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def caesar_decipher(text: str, shift: int) -> str:
        """
        Caesar cipher decryption.
        
        Args:
            text: Encrypted text
            shift: Shift amount
            
        Returns:
            Decrypted text
        """
        return CipherUtils.caesar_cipher(text, -shift)
    
    @staticmethod
    def vigenere_cipher(text: str, key: str) -> str:
        """
        Vigenère cipher.
        
        Args:
            text: Input text
            key: Encryption key
            
        Returns:
            Encrypted text
        """
        result = []
        key = key.lower()
        key_index = 0
        
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shift = ord(key[key_index % len(key)]) - ord('a')
                shifted = (ord(char) - base + shift) % 26
                result.append(chr(base + shifted))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def vigenere_decipher(text: str, key: str) -> str:
        """
        Vigenère cipher decryption.
        
        Args:
            text: Encrypted text
            key: Decryption key
            
        Returns:
            Decrypted text
        """
        result = []
        key = key.lower()
        key_index = 0
        
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shift = ord(key[key_index % len(key)]) - ord('a')
                shifted = (ord(char) - base - shift) % 26
                result.append(chr(base + shifted))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def xor_cipher(text: str, key: str) -> str:
        """
        XOR cipher.
        
        Args:
            text: Input text
            key: Encryption key
            
        Returns:
            Encrypted text (hex encoded)
        """
        result = []
        
        for i, char in enumerate(text):
            xor_char = chr(ord(char) ^ ord(key[i % len(key)]))
            result.append(xor_char)
        
        return ''.join(result).encode().hex()
    
    @staticmethod
    def xor_decipher(hex_text: str, key: str) -> str:
        """
        XOR cipher decryption.
        
        Args:
            hex_text: Encrypted text (hex encoded)
            key: Decryption key
            
        Returns:
            Decrypted text
        """
        encrypted = bytes.fromhex(hex_text).decode()
        return CipherUtils.xor_cipher(encrypted, key)


class SimpleEncryption:
    """Simple encryption using XOR (for educational purposes)."""
    
    @staticmethod
    def encrypt(text: str, key: str) -> str:
        """
        Encrypt text using XOR with key.
        
        Args:
            text: Plain text
            key: Encryption key
            
        Returns:
            Base64 encoded ciphertext
        """
        encrypted = []
        
        for i, char in enumerate(text):
            encrypted_char = chr(ord(char) ^ ord(key[i % len(key)]))
            encrypted.append(encrypted_char)
        
        return base64.b64encode(''.join(encrypted).encode()).decode()
    
    @staticmethod
    def decrypt(ciphertext: str, key: str) -> str:
        """
        Decrypt ciphertext using XOR with key.
        
        Args:
            ciphertext: Base64 encoded ciphertext
            key: Decryption key
            
        Returns:
            Plain text
        """
        encrypted = base64.b64decode(ciphertext).decode()
        decrypted = []
        
        for i, char in enumerate(encrypted):
            decrypted_char = chr(ord(char) ^ ord(key[i % len(key)]))
            decrypted.append(decrypted_char)
        
        return ''.join(decrypted)


def main() -> None:
    """Demonstrate cryptography utilities."""
    
    print("=== Cryptography Demo ===")
    
    # Hashing
    print("\n--- Hashing ---")
    text = "Hello, World!"
    print(f"Text: {text}")
    print(f"MD5: {HashUtils.md5(text)}")
    print(f"SHA-1: {HashUtils.sha1(text)}")
    print(f"SHA-256: {HashUtils.sha256(text)}")
    print(f"SHA-512: {HashUtils.sha512(text)}")
    
    # HMAC
    print("\n--- HMAC ---")
    key = "secret_key"
    message = "important_message"
    hmac_result = HashUtils.hmac_sha256(key, message)
    print(f"HMAC-SHA256: {hmac_result}")
    
    # Password hashing
    print("\n--- Password Hashing ---")
    password = "my_secure_password"
    salt, hashed = PasswordUtils.hash_password(password)
    print(f"Salt: {salt}")
    print(f"Hashed: {hashed}")
    print(f"Verified: {PasswordUtils.verify_password(password, salt, hashed)}")
    
    # Encoding
    print("\n--- Encoding ---")
    text = "Hello, World!"
    b64 = EncodingUtils.base64_encode(text)
    print(f"Base64: {b64}")
    print(f"Decoded: {EncodingUtils.base64_decode(b64)}")
    
    hex_encoded = EncodingUtils.hex_encode(text)
    print(f"Hex: {hex_encoded}")
    print(f"Decoded: {EncodingUtils.hex_decode(hex_encoded)}")
    
    # Random generation
    print("\n--- Random Generation ---")
    print(f"Random bytes (16): {RandomUtils.random_bytes(16).hex()}")
    print(f"Random hex (16): {RandomUtils.random_hex(16)}")
    print(f"Random token: {RandomUtils.random_token()}")
    print(f"UUID: {RandomUtils.generate_uuid()}")
    
    # Caesar cipher
    print("\n--- Caesar Cipher ---")
    text = "Hello, World!"
    shift = 3
    encrypted = CipherUtils.caesar_cipher(text, shift)
    decrypted = CipherUtils.caesar_decipher(encrypted, shift)
    print(f"Original: {text}")
    print(f"Encrypted (shift {shift}): {encrypted}")
    print(f"Decrypted: {decrypted}")
    
    # Vigenère cipher
    print("\n--- Vigenère Cipher ---")
    text = "Hello, World!"
    key = "KEY"
    encrypted = CipherUtils.vigenere_cipher(text, key)
    decrypted = CipherUtils.vigenere_decipher(encrypted, key)
    print(f"Original: {text}")
    print(f"Encrypted (key '{key}'): {encrypted}")
    print(f"Decrypted: {decrypted}")
    
    # Simple encryption
    print("\n--- Simple XOR Encryption ---")
    text = "Secret Message"
    key = "mykey"
    encrypted = SimpleEncryption.encrypt(text, key)
    decrypted = SimpleEncryption.decrypt(encrypted, key)
    print(f"Original: {text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")


if __name__ == "__main__":
    main()
