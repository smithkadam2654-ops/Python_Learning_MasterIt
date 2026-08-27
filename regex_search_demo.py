import re

def demonstrate_regex():
    """Demonstrate basic regular expression search and replace."""
    text = "Contact us at support@example.com or sales-info@company.org. Phone: (123) 456-7890."
    
    # 1. Searching for an email pattern
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    print(f"Finding all emails in:\n'{text}'\n")
    
    emails = re.findall(email_pattern, text)
    print(f"Found emails: {emails}")
    
    # 2. Extracting a phone number
    phone_pattern = r'\(\d{3}\) \d{3}-\d{4}'
    match = re.search(phone_pattern, text)
    if match:
        print(f"\nFound phone number: {match.group()}")
        
    # 3. Replacing text
    redacted_text = re.sub(email_pattern, "[REDACTED_EMAIL]", text)
    print(f"\nRedacted text:\n{redacted_text}")

if __name__ == "__main__":
    demonstrate_regex()
