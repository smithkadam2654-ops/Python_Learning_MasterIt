def count_words(text):
    # Split text by whitespace and count the resulting list elements
    words = text.split()
    return len(words)

def main():
    print("Word Counter")
    print("------------")
    
    user_text = input("Enter a sentence or paragraph:\n")
    
    if not user_text.strip():
        print("You entered an empty text.")
    else:
        word_count = count_words(user_text)
        character_count = len(user_text)
        char_no_spaces = len(user_text.replace(" ", ""))
        
        print("\n--- Statistics ---")
        print(f"Words: {word_count}")
        print(f"Characters (with spaces): {character_count}")
        print(f"Characters (without spaces): {char_no_spaces}")

if __name__ == "__main__":
    main()
