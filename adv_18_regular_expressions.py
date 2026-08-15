"""
Advanced Python - Lesson 18: Regular Expressions (re module)
=============================================================
Regular expressions (regex) are powerful pattern-matching tools
for searching, extracting, and transforming text.

Topics Covered:
- Basic regex syntax recap
- Groups and named groups
- Lookahead and lookbehind assertions
- Greedy vs lazy quantifiers
- re.compile and pattern objects
- findall, finditer, sub, split
- Real-world patterns: emails, URLs, dates, IP addresses
- Verbose mode and inline flags
"""

import re
from typing import Generator


# ============================================================
# 1. BASIC PATTERNS AND SEARCH
# ============================================================
def demonstrate_basics():
    """Fundamental regex operations."""
    
    text = "The price is $49.99 and the discount is 20% off."
    
    # search: find first match
    match = re.search(r'\$(\d+\.\d+)', text)
    if match:
        print(f"Found price: {match.group(0)} -> value: {match.group(1)}")
    
    # match: match at beginning only
    m = re.match(r'The', text)
    print(f"match('The'): {m.group() if m else 'No match'}")
    
    # fullmatch: entire string must match
    m = re.fullmatch(r'The.*off\.', text)
    print(f"fullmatch: {bool(m)}")
    
    # findall: all non-overlapping matches
    prices = re.findall(r'\d+\.?\d*', text)
    print(f"All numbers: {prices}")


# ============================================================
# 2. GROUPS AND NAMED GROUPS
# ============================================================
def demonstrate_groups():
    """Groups capture parts of a match for extraction."""
    
    # Numbered groups
    date_pattern = r'(\d{4})-(\d{2})-(\d{2})'
    text = "Dates: 2024-06-15, 2024-12-25, 2025-01-01"
    
    for match in re.finditer(date_pattern, text):
        year, month, day = match.groups()
        print(f"  {match.group(0)} -> Year={year}, Month={month}, Day={day}")
    
    # Named groups (?P<name>pattern)
    print("\nNamed groups:")
    named_date = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
    match = re.search(named_date, "Born on 1990-03-15")
    if match:
        print(f"  {match.groupdict()}")
        print(f"  Year: {match.group('year')}, Month: {match.group('month')}")
    
    # Non-capturing group (?:pattern)
    print("\nNon-capturing groups:")
    pattern = r'(?:https?://)(?:www\.)?(\w+\.\w+)'
    urls = "Visit https://www.google.com or http://example.org"
    domains = re.findall(pattern, urls)
    print(f"  Domains only: {domains}")
    
    # Backreferences
    print("\nBackreferences (find repeated words):")
    text = "the the quick brown fox fox jumps over over the lazy dog"
    duplicates = re.findall(r'\b(\w+)\s+\1\b', text)
    print(f"  Repeated words: {duplicates}")


# ============================================================
# 3. LOOKAHEAD AND LOOKBEHIND
# ============================================================
def demonstrate_assertions():
    """Zero-width assertions match positions, not characters."""
    
    # Positive lookahead (?=...)
    text = "password123 admin456 user789 test"
    matches = re.findall(r'\w+(?=\d)', text)
    print(f"Words followed by digits: {matches}")
    
    # Negative lookahead (?!...)
    matches = re.findall(r'\w+(?!\d)', text)
    print(f"Words NOT followed by digits: {matches}")
    
    # Positive lookbehind (?<=...)
    text = "$100 €85 £50 200yen"
    matches = re.findall(r'(?<=\$)\d+', text)
    print(f"Amounts after $: {matches}")
    
    # Negative lookbehind (?<!...)
    matches = re.findall(r'(?<!\$)\b\d+\b', text)
    print(f"Amounts NOT after $: {matches}")
    
    # Complex: password validation
    print("\nPassword validation (lookahead):")
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%]).{8,}$'
    passwords = ["Str0ng!Pass", "weak", "NoDigit!A", "nodigit1a", "Str0ng!"]
    for pw in passwords:
        valid = bool(re.match(pattern, pw))
        print(f"  '{pw}': {'VALID' if valid else 'INVALID'}")


# ============================================================
# 4. GREEDY VS LAZY QUANTIFIERS
# ============================================================
def demonstrate_quantifiers():
    """Greedy matches as much as possible; lazy matches as little as possible."""
    
    html = "<div>Hello</div> <div>World</div> <div>Python</div>"
    
    # Greedy (default): matches from first < to last >
    greedy = re.findall(r'<div>.*</div>', html)
    print(f"Greedy: {greedy}")
    
    # Lazy (with ?): matches shortest possible
    lazy = re.findall(r'<div>.*?</div>', html)
    print(f"Lazy:   {lazy}")
    
    # Greedy vs lazy with nested content
    text = "start [content1] middle [content2] end"
    greedy = re.findall(r'\[.*\]', text)
    lazy = re.findall(r'\[.*?\]', text)
    print(f"\nGreedy brackets: {greedy}")
    print(f"Lazy brackets:   {lazy}")
    
    # Possessive quantifiers (not directly supported in re, but via atomic groups)
    # Use workaround with lookaheads for performance
    print("\nPractical: extracting HTML attributes")
    tag = '<a href="https://example.com" class="link" id="main">'
    attrs = re.findall(r'(\w+)="([^"]*?)"', tag)
    print(f"  Attributes: {attrs}")


# ============================================================
# 5. COMPILED PATTERNS AND FLAGS
# ============================================================
def demonstrate_compiled_patterns():
    """Pre-compile patterns for reuse and performance."""
    
    # Compile once, use many times
    email_pattern = re.compile(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        re.IGNORECASE
    )
    
    texts = [
        "Contact: alice@example.com for info",
        "BOB@GMAIL.COM is valid too",
        "Invalid: @missing.com, also@bad",
        "Multiple: a@b.co and c@d.org here",
    ]
    
    for text in texts:
        emails = email_pattern.findall(text)
        print(f"  '{text}'")
        print(f"    Found: {emails}")
    
    # VERBOSE mode for readable complex patterns
    phone_pattern = re.compile(r"""
        ^                       # Start of string
        (?:\+?1[-.\s]?)?        # Optional country code
        \(?\d{3}\)?             # Area code (with optional parens)
        [-.\s]?                  # Separator
        \d{3}                    # First 3 digits
        [-.\s]?                  # Separator
        \d{4}                    # Last 4 digits
        $                       # End of string
    """, re.VERBOSE)
    
    print("\nPhone number validation (VERBOSE mode):")
    phones = [
        "(555) 123-4567",
        "555-123-4567",
        "555.123.4567",
        "+1-555-123-4567",
        "12345",
    ]
    for phone in phones:
        valid = bool(phone_pattern.match(phone))
        print(f"  '{phone}': {'VALID' if valid else 'INVALID'}")


# ============================================================
# 6. SUBSTITUTION AND SPLITTING
# ============================================================
def demonstrate_sub_and_split():
    """re.sub for replacements, re.split for splitting."""
    
    # Basic substitution
    text = "Hello   World   Python   Programming"
    cleaned = re.sub(r'\s+', ' ', text)
    print(f"Normalize spaces: '{cleaned}'")
    
    # Sub with backreferences
    text = "John Smith, Jane Doe, Bob Johnson"
    swapped = re.sub(r'(\w+)\s+(\w+)', r'\2, \1', text)
    print(f"Swap name order: '{swapped}'")
    
    # Sub with a function
    def censor(match):
        word = match.group(0)
        return word[0] + '*' * (len(word) - 1)
    
    text = "This damn code is freaking awesome"
    censored = re.sub(r'\b(damn|freaking)\b', censor, text)
    print(f"Censored: '{censored}'")
    
    # Conditional replacement
    def highlight_numbers(match):
        num = int(match.group(0))
        if num > 50:
            return f"[HIGH:{num}]"
        return f"[LOW:{num}]"
    
    text = "Scores: 85, 42, 91, 33, 67"
    result = re.sub(r'\d+', highlight_numbers, text)
    print(f"Conditional: '{result}'")
    
    # Split with regex
    text = "apple,banana;cherry|grape\torange"
    parts = re.split(r'[,;|\t]+', text)
    print(f"Split by delimiters: {parts}")
    
    # Split keeping delimiters
    text = "one1two2three3four"
    parts = re.split(r'(\d)', text)
    print(f"Split keeping digits: {parts}")


# ============================================================
# 7. REAL-WORLD PATTERNS
# ============================================================
class RegexPatterns:
    """Collection of production-ready regex patterns."""
    
    # Email (simplified RFC 5322)
    EMAIL = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    # URL
    URL = re.compile(
        r'https?://(?:www\.)?[\w.-]+(?:\.[a-zA-Z]{2,})(?:/[^\s]*)?'
    )
    
    # IPv4 Address
    IPV4 = re.compile(
        r'^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}'
        r'(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$'
    )
    
    # ISO Date (YYYY-MM-DD)
    ISO_DATE = re.compile(
        r'^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$'
    )
    
    # Hex Color
    HEX_COLOR = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
    
    # Credit Card (basic Luhn-agnostic format check)
    CREDIT_CARD = re.compile(
        r'^(?:\d{4}[-\s]?){3}\d{4}$'
    )
    
    # Markdown bold
    MARKDOWN_BOLD = re.compile(r'\*\*(.+?)\*\*')
    
    # SQL Injection detection (basic)
    SQL_INJECTION = re.compile(
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)\b.*\b(FROM|INTO|TABLE|WHERE|SET)\b)',
        re.IGNORECASE
    )


def validate_patterns():
    """Test real-world regex patterns."""
    
    tests = [
        ("Email", RegexPatterns.EMAIL, [
            ("alice@example.com", True),
            ("bob@gmail.co.uk", True),
            ("@invalid.com", False),
            ("no-at-sign", False),
            ("spaces in@email.com", False),
        ]),
        ("IPv4", RegexPatterns.IPV4, [
            ("192.168.1.1", True),
            ("255.255.255.0", True),
            ("256.1.1.1", False),
            ("192.168.1", False),
            ("0.0.0.0", True),
        ]),
        ("ISO Date", RegexPatterns.ISO_DATE, [
            ("2024-06-15", True),
            ("2024-13-01", False),
            ("2024-02-30", False),
            ("24-06-15", False),
        ]),
        ("Hex Color", RegexPatterns.HEX_COLOR, [
            ("#fff", True),
            ("#FF0000", True),
            ("#abc123", True),
            ("#GGGGGG", False),
            ("red", False),
        ]),
    ]
    
    for name, pattern, cases in tests:
        print(f"\n{name} validation:")
        for value, expected in cases:
            result = bool(pattern.match(value))
            status = "✓" if result == expected else "✗ UNEXPECTED"
            print(f"  {status} '{value}': {result}")


# ============================================================
# 8. PRACTICAL: LOG PARSER
# ============================================================
def parse_log_entries():
    """Parse structured log entries with regex."""
    
    log_lines = [
        '2024-06-15 10:30:45 [INFO] User alice logged in from 192.168.1.100',
        '2024-06-15 10:31:02 [ERROR] Database connection failed: timeout after 30s',
        '2024-06-15 10:31:15 [WARNING] High memory usage: 85% of 16GB',
        '2024-06-15 10:32:00 [INFO] API request: GET /api/users (200 OK)',
        '2024-06-15 10:32:30 [ERROR] File not found: /var/log/app.log',
        '2024-06-15 10:33:00 [INFO] Cache hit ratio: 94.5%',
    ]
    
    pattern = re.compile(
        r'(?P<date>\d{4}-\d{2}-\d{2})\s+'
        r'(?P<time>\d{2}:\d{2}:\d{2})\s+'
        r'\[(?P<level>\w+)\]\s+'
        r'(?P<message>.+)'
    )
    
    print("Parsed log entries:")
    errors = []
    
    for line in log_lines:
        m = pattern.match(line)
        if m:
            entry = m.groupdict()
            icon = {"INFO": "ℹ", "ERROR": "✗", "WARNING": "⚠"}.get(entry["level"], "?")
            print(f"  {icon} [{entry['time']}] {entry['message']}")
            if entry["level"] == "ERROR":
                errors.append(entry)
    
    print(f"\n  Total errors: {len(errors)}")
    for err in errors:
        print(f"    {err['time']}: {err['message']}")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Basic Patterns")
    demonstrate_basics()

    separator("2. Groups and Named Groups")
    demonstrate_groups()

    separator("3. Lookahead and Lookbehind")
    demonstrate_assertions()

    separator("4. Greedy vs Lazy Quantifiers")
    demonstrate_quantifiers()

    separator("5. Compiled Patterns and Flags")
    demonstrate_compiled_patterns()

    separator("6. Substitution and Splitting")
    demonstrate_sub_and_split()

    separator("7. Real-World Pattern Validation")
    validate_patterns()

    separator("8. Log Parser")
    parse_log_entries()


if __name__ == "__main__":
    main()
