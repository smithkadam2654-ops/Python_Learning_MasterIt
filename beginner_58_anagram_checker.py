"""
Beginner Project 58: Anagram Checker
Checks if two given words are anagrams of each other (contain the exact same letters).
"""

def is_anagram(word1, word2):
    # Remove spaces and convert to lowercase for accurate comparison
    w1 = word1.replace(" ", "").lower()
    w2 = word2.replace(" ", "").lower()
    
    # Sorting the letters allows us to compare them directly
    return sorted(w1) == sorted(w2)

def main():
    print("Anagram Checker")
    
    word1 = input("Enter the first word or phrase: ").strip()
    word2 = input("Enter the second word or phrase: ").strip()
    
    if not word1 or not word2:
        print("Please enter valid words.")
        return
        
    if is_anagram(word1, word2):
        print(f"\nYes! '{word1}' and '{word2}' are anagrams of each other.")
    else:
        print(f"\nNo, '{word1}' and '{word2}' are NOT anagrams.")

if __name__ == "__main__":
    main()
