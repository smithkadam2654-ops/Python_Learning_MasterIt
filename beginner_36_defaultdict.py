from collections import defaultdict

def main():
    # A standard dictionary throws a KeyError if you access a missing key.
    # A defaultdict automatically creates a default value for missing keys!
    
    # Let's group words by their starting letter
    words = ["apple", "banana", "avocado", "blueberry", "cherry"]
    
    # We pass 'list' to defaultdict, so missing keys default to an empty list []
    grouped_words = defaultdict(list)
    
    for word in words:
        first_letter = word[0]
        # No need to check if first_letter is in grouped_words!
        grouped_words[first_letter].append(word)
        
    print("Grouped words:")
    for letter, word_list in sorted(grouped_words.items()):
        print(f"{letter}: {word_list}")
        
    # Another example: counting with defaultdict(int) (defaults to 0)
    scores = defaultdict(int)
    scores["Alice"] += 10
    scores["Bob"] += 5
    scores["Alice"] += 20
    
    print(f"\nAlice's score: {scores['Alice']}")
    print(f"Bob's score: {scores['Bob']}")
    print(f"Charlie's score (never added): {scores['Charlie']}") # Prints 0!

if __name__ == "__main__":
    main()
