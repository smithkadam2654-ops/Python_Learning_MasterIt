"""
Beginner Project 56: Sentence Word Reverser
Reverses the order of words in a given sentence.
Example: "Hello World" -> "World Hello"
"""

def reverse_words(sentence):
    # Split the sentence into a list of words, reverse it, and join it back
    words = sentence.split()
    words.reverse()
    return " ".join(words)

def main():
    print("Sentence Word Reverser")
    
    sentence = input("Enter a sentence to reverse: ").strip()
    
    if not sentence:
        print("Please enter a valid sentence.")
        return
        
    reversed_sentence = reverse_words(sentence)
    print(f"\nOriginal: {sentence}")
    print(f"Reversed: {reversed_sentence}")

if __name__ == "__main__":
    main()
