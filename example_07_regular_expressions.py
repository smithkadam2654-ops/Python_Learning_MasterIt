import re

def extract_emails(text):
    """Extracts all valid email addresses from a given text."""
    # A basic regex pattern for matching email addresses
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # re.findall returns a list of all non-overlapping matches
    return re.findall(pattern, text)

if __name__ == "__main__":
    sample_text = """
    Please contact us at support@example.com for assistance.
    You can also reach our sales team at sales.department@company.co.uk.
    Invalid emails like user@domain or @missingusername.com will be ignored.
    My personal email is john_doe123@gmail.com!
    """
    
    found_emails = extract_emails(sample_text)
    
    print("Extracted Email Addresses:")
    for i, email in enumerate(found_emails, 1):
        print(f"{i}. {email}")
