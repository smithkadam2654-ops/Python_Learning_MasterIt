"""
Simple Encryption - Basic encryption and decryption utilities.
Features: Caesar cipher, Vigenère cipher, and simple XOR encryption.
"""

import base64
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class CipherType(Enum):
    """Cipher types."""
    CAESAR = "caesar"
    VIGENERE = "vigenere"
    XOR = "xor"
    BASE64 = "base64"


@dataclass
class EncryptionResult:
    """Encryption/decryption result."""
    success: bool
    data: str
    error: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation."""
        if self.success:
            return f"Success: {self.data}"
        return f"Error: {self.error}"


class SimpleEncryption:
    """Simple encryption utilities."""
    
    @staticmethod
    def caesar_encrypt(text: str, shift: int) -> EncryptionResult:
        """
        Encrypt text using Caesar cipher.
        
        Args:
            text: Text to encrypt
            shift: Shift amount
            
        Returns:
            Encryption result
        """
        try:
            result = ""
            for char in text:
                if char.isalpha():
                    shift_amount = shift % 26
                    if char.islower():
                        result += chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a'))
                    else:
                        result += chr((ord(char) - ord('A') + shift_amount) % 26 + ord('A'))
                else:
                    result += char
            return EncryptionResult(True, result)
        except Exception as e:
            return EncryptionResult(False, "", str(e))
    
    @staticmethod
    def caesar_decrypt(text: str, shift: int) -> EncryptionResult:
        """
        Decrypt text using Caesar cipher.
        
        Args:
            text: Text to decrypt
            shift: Shift amount
            
        Returns:
            Decryption result
        """
        return SimpleEncryption.caesar_encrypt(text, -shift)
    
    @staticmethod
    def vigenere_encrypt(text: str, key: str) -> EncryptionResult:
        """
        Encrypt text using Vigenère cipher.
        
        Args:
            text: Text to encrypt
            key: Encryption key
            
        Returns:
            Encryption result
        """
        try:
            if not key:
                return EncryptionResult(False, "", "Key cannot be empty")
            
            result = ""
            key_index = 0
            
            for char in text:
                if char.isalpha():
                    shift = ord(key[key_index % len(key)].lower()) - ord('a')
                    if char.islower():
                        result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                    else:
                        result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                    key_index += 1
                else:
                    result += char
            
            return EncryptionResult(True, result)
        except Exception as e:
            return EncryptionResult(False, "", str(e))
    
    @staticmethod
    def vigenere_decrypt(text: str, key: str) -> EncryptionResult:
        """
        Decrypt text using Vigenère cipher.
        
        Args:
            text: Text to decrypt
            key: Decryption key
            
        Returns:
            Decryption result
        """
        try:
            if not key:
                return EncryptionResult(False, "", "Key cannot be empty")
            
            result = ""
            key_index = 0
            
            for char in text:
                if char.isalpha():
                    shift = ord(key[key_index % len(key)].lower()) - ord('a')
                    if char.islower():
                        result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                    else:
                        result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                    key_index += 1
                else:
                    result += char
            
            return EncryptionResult(True, result)
        except Exception as e:
            return EncryptionResult(False, "", str(e))
    
    @staticmethod
    def xor_encrypt(text: str, key: str) -> EncryptionResult:
        """
        Encrypt text using XOR cipher.
        
        Args:
            text: Text to encrypt
            key: Encryption key
            
        Returns:
            Encryption result
        """
        try:
            if not key:
                return EncryptionResult(False, "", "Key cannot be empty")
            
            result = ""
            for i, char in enumerate(text):
                xor_char = chr(ord(char) ^ ord(key[i % len(key)]))
                result += xor_char
            
            # Encode as base64 for safe display
            encoded = base64.b64encode(result.encode()).decode()
            return EncryptionResult(True, encoded)
        except Exception as e:
            return EncryptionResult(False, "", str(e))
    
    @staticmethod
    def xor_decrypt(encoded_text: str, key: str) -> EncryptionResult:
        """
        Decrypt text using XOR cipher.
        
        Args:
            encoded_text: Encoded text (base64)
            key: Decryption key
            
        Returns:
            Decryption result
        """
        try:
            if not key:
                return EncryptionResult(False, "", "Key cannot be empty")
            
            # Decode from base64
            decoded = base64.b64decode(encoded_text).decode()
            
            result = ""
            for i, char in enumerate(decoded):
                xor_char = chr(ord(char) ^ ord(key[i % len(key)]))
                result += xor_char
            
            return EncryptionResult(True, result)
        except Exception as e:
            return EncryptionResult(False, "", str(e))
    
    @staticmethod
    def base64_encode(text: str) -> EncryptionResult:
        """
        Encode text using Base64.
        
        Args:
            text: Text to encode
            
        Returns:
            Encoding result
        """
        try:
            encoded = base64.b64encode(text.encode()).decode()
            return EncryptionResult(True, encoded)
        except Exception as e:
            return EncryptionResult(False, "", str(e))
    
    @staticmethod
    def base64_decode(encoded_text: str) -> EncryptionResult:
        """
        Decode text using Base64.
        
        Args:
            encoded_text: Encoded text
            
        Returns:
            Decoding result
        """
        try:
            decoded = base64.b64decode(encoded_text).decode()
            return EncryptionResult(True, decoded)
        except Exception as e:
            return EncryptionResult(False, "", str(e))
    
    @staticmethod
    def rot13(text: str) -> EncryptionResult:
        """
        ROT13 encoding (special case of Caesar with shift 13).
        
        Args:
            text: Text to encode
            
        Returns:
            Encoding result
        """
        return SimpleEncryption.caesar_encrypt(text, 13)
    
    @staticmethod
    def analyze_frequency(text: str) -> dict:
        """
        Analyze character frequency.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of character frequencies
        """
        frequency = {}
        for char in text.lower():
            if char.isalpha():
                frequency[char] = frequency.get(char, 0) + 1
        return frequency


class PasswordHasher:
    """Simple password hashing (for demonstration only)."""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple:
        """
        Hash password with salt.
        
        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)
            
        Returns:
            Tuple of (salt, hashed_password)
        """
        import hashlib
        
        if salt is None:
            import random
            salt = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
        
        salted = password + salt
        hashed = hashlib.sha256(salted.encode()).hexdigest()
        
        return salt, hashed
    
    @staticmethod
    def verify_password(password: str, salt: str, hashed: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password: Password to verify
            salt: Salt used for hashing
            hashed: Hashed password
            
        Returns:
            True if password matches
        """
        _, new_hash = PasswordHasher.hash_password(password, salt)
        return new_hash == hashed


def main() -> None:
    """Demonstrate encryption utilities."""
    
    print("=== Simple Encryption Demo ===")
    
    crypto = SimpleEncryption()
    
    # Caesar cipher
    text = "Hello, World!"
    shift = 3
    
    print(f"\nOriginal: {text}")
    
    encrypted = crypto.caesar_encrypt(text, shift)
    print(f"Caesar encrypted (shift={shift}): {encrypted}")
    
    decrypted = crypto.caesar_decrypt(encrypted.data, shift)
    print(f"Caesar decrypted: {decrypted}")
    
    # Vigenère cipher
    key = "KEY"
    print(f"\nOriginal: {text}")
    
    encrypted = crypto.vigenere_encrypt(text, key)
    print(f"Vigenère encrypted (key={key}): {encrypted}")
    
    decrypted = crypto.vigenere_decrypt(encrypted.data, key)
    print(f"Vigenère decrypted: {decrypted}")
    
    # XOR cipher
    xor_key = "SECRET"
    print(f"\nOriginal: {text}")
    
    encrypted = crypto.xor_encrypt(text, xor_key)
    print(f"XOR encrypted (key={xor_key}): {encrypted}")
    
    decrypted = crypto.xor_decrypt(encrypted.data, xor_key)
    print(f"XOR decrypted: {decrypted}")
    
    # Base64
    print(f"\nOriginal: {text}")
    
    encoded = crypto.base64_encode(text)
    print(f"Base64 encoded: {encoded}")
    
    decoded = crypto.base64_decode(encoded.data)
    print(f"Base64 decoded: {decoded}")
    
    # ROT13
    print(f"\nOriginal: {text}")
    
    rot13 = crypto.rot13(text)
    print(f"ROT13: {rot13}")
    
    # Frequency analysis
    print(f"\nFrequency analysis of: '{text}'")
    freq = crypto.analyze_frequency(text)
    for char, count in sorted(freq.items()):
        print(f"  {char}: {count}")
    
    # Password hashing
    print("\n=== Password Hashing ===")
    
    password = "mypassword123"
    salt, hashed = PasswordHasher.hash_password(password)
    print(f"Password: {password}")
    print(f"Salt: {salt}")
    print(f"Hash: {hashed}")
    
    verified = PasswordHasher.verify_password(password, salt, hashed)
    print(f"Verification (correct): {verified}")
    
    verified = PasswordHasher.verify_password("wrongpassword", salt, hashed)
    print(f"Verification (wrong): {verified}")
    
    print("\n⚠️  Note: These are simple encryption methods for educational purposes.")
    print("For production use, use established cryptographic libraries like cryptography.")


if __name__ == "__main__":
    main()
