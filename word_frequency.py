import string
from collections import Counter

def count_word_frequency(text):
    """Count the frequency of each word in a given text."""
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Split the text into words
    words = text.split()
    
    # Count the frequencies
    word_counts = Counter(words)
    
    return word_counts

# Example usage
if __name__ == "__main__":
    sample_text = """
    Python is an interpreted, high-level and general-purpose programming language. 
    Python's design philosophy emphasizes code readability!
    """

    frequencies = count_word_frequency(sample_text)

    print("Top 3 most common words:")
    for word, count in frequencies.most_common(3):
        print(f"'{word}': {count} times")
