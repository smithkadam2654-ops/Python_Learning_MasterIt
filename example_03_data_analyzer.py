from collections import Counter

def analyze_text(text):
    """Analyzes a block of text and returns word statistics."""
    # Convert text to lowercase and split into words
    words = text.lower().split()
    
    # Remove basic punctuation from the ends of words
    words = [word.strip('.,!?()[]{}"\'') for word in words]
    words = [word for word in words if word] # Remove empty strings
    
    word_count = len(words)
    unique_words = len(set(words))
    
    # Get the 3 most common words using collections.Counter
    word_frequencies = Counter(words)
    top_3_words = word_frequencies.most_common(3)
    
    return {
        "total_words": word_count,
        "unique_words": unique_words,
        "top_3_words": top_3_words
    }

if __name__ == "__main__":
    sample_text = """
    Python is an amazing programming language. Python is used for web development, 
    data science, artificial intelligence, and more. Learning Python is fun!
    """
    
    stats = analyze_text(sample_text)
    print("Text Analysis Results:")
    print(f"Total Words: {stats['total_words']}")
    print(f"Unique Words: {stats['unique_words']}")
    print("Top 3 most common words:")
    for word, count in stats['top_3_words']:
        print(f" - '{word}': {count} times")
