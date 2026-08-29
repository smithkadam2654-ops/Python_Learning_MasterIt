import hashlib

def demonstrate_hashlib():
    """Demonstrate cryptographic hashing using the hashlib module."""
    
    # The message we want to hash
    # Note: hashlib requires bytes, not strings, so we must encode it!
    message = "This is a highly confidential message.".encode('utf-8')
    
    print("--- Cryptographic Hashing ---")
    print(f"Original message: {message.decode('utf-8')}")
    
    # 1. SHA-256 (Highly recommended for general secure hashing)
    sha256_hash = hashlib.sha256(message).hexdigest()
    print(f"\nSHA-256 Hash: {sha256_hash}")
    
    # 2. SHA-512 (More secure, longer hash)
    sha512_hash = hashlib.sha512(message).hexdigest()
    print(f"SHA-512 Hash: {sha512_hash}")
    
    # 3. MD5 (Warning: Consider broken for security purposes, but fast for checksums)
    md5_hash = hashlib.md5(message).hexdigest()
    print(f"MD5 Hash:     {md5_hash}")
    
    print("\n--- Why Hashes are Useful ---")
    # Hashes are deterministic but unpredictable
    slightly_changed_message = "This is a highly confidential message!".encode('utf-8')
    new_hash = hashlib.sha256(slightly_changed_message).hexdigest()
    
    print("Notice how changing one character completely changes the hash:")
    print(f"Old Hash: {sha256_hash}")
    print(f"New Hash: {new_hash}")

if __name__ == "__main__":
    demonstrate_hashlib()
