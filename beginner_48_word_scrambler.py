"""
Beginner Project 48: Word Scrambler
A script that takes a word and scrambles its letters randomly.
"""
import random

def scramble_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    return "".join(word_list)

def main():
    print("Word Scrambler")
    word = input("Enter a word to scramble: ").strip()
    
    if not word:
        print("Please enter a valid word.")
        return
        
    scrambled = scramble_word(word)
    print(f"\nOriginal: {word}")
    print(f"Scrambled: {scrambled}")

if __name__ == "__main__":
    main()
