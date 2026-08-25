def is_palindrome(text):
    # Remove spaces and convert to lowercase for accurate checking
    clean_text = text.replace(" ", "").lower()
    # Check if the text is the same forwards and backwards
    return clean_text == clean_text[::-1]

def main():
    print("--- Palindrome Checker ---")
    print("A palindrome is a word or phrase that reads the same backwards as forwards.")
    
    while True:
        user_input = input("\nEnter a word or phrase (or type 'quit' to exit): ")
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
            
        if not user_input.strip():
            print("Please enter some text.")
            continue
            
        if is_palindrome(user_input):
            print(f"Yes! '{user_input}' is a palindrome.")
        else:
            print(f"No. '{user_input}' is not a palindrome.")

if __name__ == "__main__":
    main()
