import random
import string

def generate_password(length=12, use_special=True):
    characters = string.ascii_letters + string.digits
    if use_special:
        characters += string.punctuation
        
    if length < 4:
        print("Password length should be at least 4 characters.")
        return None
        
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    print("Random Password Generator")
    try:
        length = int(input("Enter desired password length (default 12): ") or "12")
        use_special = input("Include special characters? (y/n): ").lower() != 'n'
        
        pwd = generate_password(length, use_special)
        if pwd:
            print(f"\nYour generated password is: {pwd}")
    except ValueError:
        print("Invalid input for length.")

if __name__ == "__main__":
    main()
