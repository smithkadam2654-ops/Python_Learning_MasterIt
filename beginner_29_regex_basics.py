import re

def main():
    text = "Please contact support at help@example.com for assistance. Alternate email: admin@test.org"

    # 1. Simple search
    if re.search(r"support", text):
        print("Found the word 'support'!")

    # 2. Find all email addresses using a regular expression pattern
    # Pattern explanation: 
    # [a-zA-Z0-9_.+-]+  -> matches the username
    # @                 -> matches the @ symbol
    # [a-zA-Z0-9-]+     -> matches the domain name
    # \.                -> matches the dot
    # [a-zA-Z0-9-.]+    -> matches the top-level domain (like com, org)
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    
    emails = re.findall(pattern, text)
    print("\nFound email addresses:")
    for email in emails:
        print(f"- {email}")

    # 3. Replacing text
    redacted_text = re.sub(pattern, "[REDACTED EMAIL]", text)
    print("\nRedacted Text:")
    print(redacted_text)

if __name__ == "__main__":
    main()
