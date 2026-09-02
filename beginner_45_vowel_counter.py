"""
Beginner Project 45: Vowel Counter
A script to count the number of vowels in a given string.
"""

def count_vowels(text):
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count

def main():
    print("Vowel Counter")
    user_input = input("Enter a word or sentence: ")
    
    vowel_count = count_vowels(user_input)
    
    print(f"\nThe text contains {vowel_count} vowel(s).")

if __name__ == "__main__":
    main()
