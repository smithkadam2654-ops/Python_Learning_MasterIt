from collections import Counter

def main():
    # Counter is a special dictionary for counting hashable objects
    
    # 1. Counting items in a list
    fruits = ["apple", "banana", "apple", "orange", "banana", "apple"]
    fruit_counts = Counter(fruits)
    print("Fruit counts:", fruit_counts)
    print(f"How many apples? {fruit_counts['apple']}")
    
    # 2. Counting characters in a string
    word = "mississippi"
    char_counts = Counter(word)
    print("\nCharacter counts in 'mississippi':")
    print(char_counts)
    
    # 3. Finding the most common elements
    print("\nTop 2 most common characters:")
    for char, count in char_counts.most_common(2):
        print(f"'{char}' appears {count} times")

if __name__ == "__main__":
    main()
