import random
import string

def generate_password(length=12):
    # Define the characters to choose from
    letters = string.ascii_letters # a-z and A-Z
    numbers = string.digits        # 0-9
    symbols = string.punctuation   # !@#$%^&* etc.
    
    # Combine all characters
    all_characters = letters + numbers + symbols
    
    # Randomly select characters up to the requested length
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password

if __name__ == "__main__":
    print("--- Secure Password Generator ---")
    # Generate 3 different passwords
    for i in range(3):
        pwd = generate_password(length=16)
        print(f"Password {i+1}: {pwd}")
