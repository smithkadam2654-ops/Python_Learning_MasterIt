import re

def validate_emails(text):
    print("--- Extracting Emails ---")
    # A regex pattern for matching standard email addresses
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Find all matches in the text
    emails = re.findall(pattern, text)
    
    if emails:
        print("Found the following emails:")
        for email in emails:
            print(f"- {email}")
    else:
        print("No emails found.")

def replace_phone_numbers(text):
    print("\n--- Redacting Phone Numbers ---")
    # Match patterns like 123-456-7890 or (123) 456-7890
    pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    # Replace the matches with a redacted string
    redacted_text = re.sub(pattern, "[REDACTED PHONE NUMBER]", text)
    print("Original text:")
    print(text)
    print("\nRedacted text:")
    print(redacted_text)

if __name__ == "__main__":
    sample_text = """
    Please contact our support team at support@example.com for assistance.
    You can also reach out to the manager, Jane Doe, at j.doe@company.org.
    For urgent inquiries, call us at (555) 123-4567 or 555-987-6543.
    """
    
    validate_emails(sample_text)
    replace_phone_numbers(sample_text)
