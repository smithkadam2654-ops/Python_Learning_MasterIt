"""
Cryptography Basics - Basic cryptographic operations and concepts.
Features: Caesar cipher, Vigenère cipher, and hash functions.
"""

import hashlib
import base64
from typing import List, Optional


class CaesarCipher:
    """Caesar cipher implementation."""
    
    def __init__(self, shift: int = 3) -> None:
        """
        Initialize Caesar cipher.
        
        Args:
            shift: Number of positions to shift
        """
        self.shift = shift % 26
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using Caesar cipher.
        
        Args:
            plaintext: Text to encrypt
            
        Returns:
            Encrypted text
        """
        result = []
        
        for char in plaintext:
            if char.isupper():
                shifted = chr((ord(char) - 65 + self.shift) % 26 + 65)
                result.append(shifted)
            elif char.islower():
                shifted = chr((ord(char) - 97 + self.shift) % 26 + 97)
                result.append(shifted)
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext using Caesar cipher.
        
        Args:
            ciphertext: Text to decrypt
            
        Returns:
            Decrypted text
        """
        # Decrypt is just encrypt with negative shift
        reverse_cipher = CaesarCipher(-self.shift)
        return reverse_cipher.encrypt(ciphertext)
    
    def brute_force(self, ciphertext: str) -> List[str]:
        """
        Try all possible shifts to decrypt.
        
        Args:
            ciphertext: Text to decrypt
            
        Returns:
            List of all possible decryptions
        """
        results = []
        for shift in range(26):
            cipher = CaesarCipher(shift)
            decrypted = cipher.decrypt(ciphertext)
            results.append(f"Shift {shift}: {decrypted}")
        return results


class VigenereCipher:
    """Vigenère cipher implementation."""
    
    def __init__(self, key: str) -> None:
        """
        Initialize Vigenère cipher.
        
        Args:
            key: Encryption key
        """
        self.key = key.lower()
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using Vigenère cipher.
        
        Args:
            plaintext: Text to encrypt
            
        Returns:
            Encrypted text
        """
        result = []
        key_index = 0
        
        for char in plaintext:
            if char.isalpha():
                key_shift = ord(self.key[key_index % len(self.key)]) - 97
                
                if char.isupper():
                    shifted = chr((ord(char) - 65 + key_shift) % 26 + 65)
                    result.append(shifted)
                else:
                    shifted = chr((ord(char) - 97 + key_shift) % 26 + 97)
                    result.append(shifted)
                
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext using Vigenère cipher.
        
        Args:
            ciphertext: Text to decrypt
            
        Returns:
            Decrypted text
        """
        result = []
        key_index = 0
        
        for char in ciphertext:
            if char.isalpha():
                key_shift = ord(self.key[key_index % len(self.key)]) - 97
                
                if char.isupper():
                    shifted = chr((ord(char) - 65 - key_shift) % 26 + 65)
                    result.append(shifted)
                else:
                    shifted = chr((ord(char) - 97 - key_shift) % 26 + 97)
                    result.append(shifted)
                
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)


class HashUtils:
    """Utility functions for hashing."""
    
    @staticmethod
    def md5_hash(text: str) -> str:
        """
        Calculate MD5 hash of text.
        
        Args:
            text: Text to hash
            
        Returns:
            MD5 hash as hexadecimal string
        """
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def sha1_hash(text: str) -> str:
        """
        Calculate SHA-1 hash of text.
        
        Args:
            text: Text to hash
            
        Returns:
            SHA-1 hash as hexadecimal string
        """
        return hashlib.sha1(text.encode()).hexdigest()
    
    @staticmethod
    def sha256_hash(text: str) -> str:
        """
        Calculate SHA-256 hash of text.
        
        Args:
            text: Text to hash
            
        Returns:
            SHA-256 hash as hexadecimal string
        """
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def sha512_hash(text: str) -> str:
        """
        Calculate SHA-512 hash of text.
        
        Args:
            text: Text to hash
            
        Returns:
            SHA-512 hash as hexadecimal string
        """
        return hashlib.sha512(text.encode()).hexdigest()
    
    @staticmethod
    def file_hash(filepath: str, algorithm: str = "sha256") -> Optional[str]:
        """
        Calculate hash of a file.
        
        Args:
            filepath: Path to file
            algorithm: Hash algorithm to use
            
        Returns:
            Hash as hexadecimal string, or None if error
        """
        try:
            hash_func = hashlib.new(algorithm)
            
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
        except (IOError, ValueError):
            return None


class Base64Utils:
    """Base64 encoding and decoding utilities."""
    
    @staticmethod
    def encode(text: str) -> str:
        """
        Encode text to Base64.
        
        Args:
            text: Text to encode
            
        Returns:
            Base64 encoded string
        """
        return base64.b64encode(text.encode()).decode()
    
    @staticmethod
    def decode(encoded: str) -> str:
        """
        Decode Base64 string.
        
        Args:
            encoded: Base64 encoded string
            
        Returns:
            Decoded text
        """
        return base64.b64decode(encoded).decode()
    
    @staticmethod
    def encode_bytes(data: bytes) -> str:
        """
        Encode bytes to Base64.
        
        Args:
            data: Bytes to encode
            
        Returns:
            Base64 encoded string
        """
        return base64.b64encode(data).decode()
    
    @staticmethod
    def decode_bytes(encoded: str) -> bytes:
        """
        Decode Base64 string to bytes.
        
        Args:
            encoded: Base64 encoded string
            
        Returns:
            Decoded bytes
        """
        return base64.b64decode(encoded)


class XORCipher:
    """Simple XOR cipher for basic encryption."""
    
    @staticmethod
    def encrypt(plaintext: str, key: str) -> str:
        """
        Encrypt plaintext using XOR cipher.
        
        Args:
            plaintext: Text to encrypt
            key: Encryption key
            
        Returns:
            Encrypted text (hexadecimal)
        """
        encrypted = []
        key_len = len(key)
        
        for i, char in enumerate(plaintext):
            encrypted_char = chr(ord(char) ^ ord(key[i % key_len]))
            encrypted.append(encrypted_char)
        
        return Base64Utils.encode(''.join(encrypted))
    
    @staticmethod
    def decrypt(ciphertext: str, key: str) -> str:
        """
        Decrypt ciphertext using XOR cipher.
        
        Args:
            ciphertext: Encrypted text (hexadecimal)
            key: Decryption key
            
        Returns:
            Decrypted text
        """
        decoded = Base64Utils.decode(ciphertext)
        decrypted = []
        key_len = len(key)
        
        for i, char in enumerate(decoded):
            decrypted_char = chr(ord(char) ^ ord(key[i % key_len]))
            decrypted.append(decrypted_char)
        
        return ''.join(decrypted)


class PasswordUtils:
    """Password security utilities."""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """
        Hash password with salt.
        
        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)
            
        Returns:
            Tuple of (salt, hashed_password)
        """
        if salt is None:
            salt = HashUtils.sha256_hash(str(hash(password)))[:16]
        
        salted_password = password + salt
        hashed = HashUtils.sha256_hash(salted_password)
        
        return salt, hashed
    
    @staticmethod
    def verify_password(password: str, salt: str, hashed_password: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password: Password to verify
            salt: Salt used in hashing
            hashed_password: Hash to verify against
            
        Returns:
            True if password matches, False otherwise
        """
        _, computed_hash = PasswordUtils.hash_password(password, salt)
        return computed_hash == hashed_password
    
    @staticmethod
    def check_password_strength(password: str) -> dict:
        """
        Check password strength.
        
        Args:
            password: Password to check
            
        Returns:
            Dictionary with strength metrics
        """
        strength = {
            "length": len(password) >= 8,
            "uppercase": any(c.isupper() for c in password),
            "lowercase": any(c.islower() for c in password),
            "digit": any(c.isdigit() for c in password),
            "special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
        }
        
        strength["score"] = sum(strength.values())
        strength["strong"] = strength["score"] >= 4
        
        return strength


def main() -> None:
    """Demonstrate cryptography utilities."""
    
    print("=== Caesar Cipher ===")
    caesar = CaesarCipher(3)
    plaintext = "Hello, World!"
    encrypted = caesar.encrypt(plaintext)
    decrypted = caesar.decrypt(encrypted)
    
    print(f"Original: {plaintext}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    
    print("\nBrute force:")
    for attempt in caesar.brute_force(encrypted)[:5]:
        print(f"  {attempt}")
    
    print("\n=== Vigenère Cipher ===")
    vigenere = VigenereCipher("KEY")
    plaintext = "Hello, World!"
    encrypted = vigenere.encrypt(plaintext)
    decrypted = vigenere.decrypt(encrypted)
    
    print(f"Original: {plaintext}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    
    print("\n=== Hash Functions ===")
    text = "Hello, World!"
    print(f"MD5: {HashUtils.md5_hash(text)}")
    print(f"SHA-1: {HashUtils.sha1_hash(text)}")
    print(f"SHA-256: {HashUtils.sha256_hash(text)}")
    print(f"SHA-512: {HashUtils.sha512_hash(text)}")
    
    print("\n=== Base64 Encoding ===")
    text = "Hello, World!"
    encoded = Base64Utils.encode(text)
    decoded = Base64Utils.decode(encoded)
    
    print(f"Original: {text}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
    
    print("\n=== XOR Cipher ===")
    key = "SECRET"
    plaintext = "Secret Message"
    encrypted = XORCipher.encrypt(plaintext, key)
    decrypted = XORCipher.decrypt(encrypted, key)
    
    print(f"Original: {plaintext}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    
    print("\n=== Password Security ===")
    password = "MySecurePass123!"
    salt, hashed = PasswordUtils.hash_password(password)
    print(f"Password: {password}")
    print(f"Salt: {salt}")
    print(f"Hash: {hashed}")
    
    valid = PasswordUtils.verify_password(password, salt, hashed)
    print(f"Verification: {valid}")
    
    invalid = PasswordUtils.verify_password("WrongPass", salt, hashed)
    print(f"Wrong password verification: {invalid}")
    
    strength = PasswordUtils.check_password_strength(password)
    print(f"\nPassword strength: {strength}")


if __name__ == "__main__":
    main()
