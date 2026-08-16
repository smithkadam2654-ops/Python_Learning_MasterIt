"""
String Manipulation Functions
Features: Palindrome checking and vowel reversal.
"""


def is_palindrome(s: str) -> bool:
    """
    Check if a given string is a palindrome (case-sensitive).
    
    A palindrome reads the same forwards and backwards.
    
    Args:
        s: The string to check
        
    Returns:
        True if the string is a palindrome, False otherwise
        
    Examples:
        >>> is_palindrome("level")
        True
        >>> is_palindrome("noon")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome("a")
        True
        >>> is_palindrome("Aba")
        False
    """
    return s == s[::-1]


def reverse_vowels(s: str) -> str:
    """
    Reverse only the vowels in a given string while maintaining other character positions.
    
    Vowels considered: a, e, i, o, u, A, E, I, O, U
    
    Args:
        s: The input string
        
    Returns:
        String with vowels reversed, other characters in original positions
        
    Examples:
        >>> reverse_vowels("hello")
        'holle'
        >>> reverse_vowels("OPE1")
        'EPO1'
        >>> reverse_vowels("aeiou")
        'uoiea'
        >>> reverse_vowels("Hello wOrld")
        'Hollo wErld'
        >>> reverse_vowels("python")
        'python'
    """
    vowels = "aeiouAEIOU"
    
    # Extract all vowels from the string in order
    vowel_list = [char for char in s if char in vowels]
    
    # Reverse the extracted vowels
    reversed_vowels = vowel_list[::-1]
    
    # Build the result string
    result = []
    vowel_index = 0
    
    for char in s:
        if char in vowels:
            result.append(reversed_vowels[vowel_index])
            vowel_index += 1
        else:
            result.append(char)
    
    return "".join(result)


def main() -> None:
    """Demonstrate the string manipulation functions."""
    
    # Test is_palindrome
    print("=== Palindrome Checker ===")
    test_cases = ["level", "noon", "hello", "a", "Aba"]
    for test in test_cases:
        result = is_palindrome(test)
        print(f'is_palindrome("{test}") -> {result}')
    
    # Test reverse_vowels
    print("\n=== Reverse Vowels ===")
    test_cases = ["hello", "OPE1", "aeiou", "Hello wOrld", "python"]
    for test in test_cases:
        result = reverse_vowels(test)
        print(f'reverse_vowels("{test}") -> "{result}"')


if __name__ == "__main__":
    main()
