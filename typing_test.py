import time
import random

def typing_test():
    sentences = [
        "The quick brown fox jumps over the lazy dog.",
        "Programming is the art of algorithm design and the craft of debugging errant code.",
        "Python is a clear and powerful object-oriented programming language.",
        "Practice makes perfect, but nobody is perfect, so why practice?"
    ]
    
    print("--- ⌨️ Terminal Typing Speed Test ---")
    print("Get ready to type! Press Enter when you are ready to begin.")
    input()
    
    sentence = random.choice(sentences)
    print("\nType this exactly:")
    # Using simple ANSI escape codes to make the sentence cyan
    print(f"\033[1;36m{sentence}\033[0m\n") 
    
    start_time = time.time()
    user_input = input("Start typing: ")
    end_time = time.time()
    
    time_taken = end_time - start_time
    
    # Calculate words per minute (WPM)
    # Average word length is generally considered to be 5 characters
    words_typed = len(user_input) / 5
    wpm = (words_typed / time_taken) * 60
    
    # Calculate accuracy
    correct_chars = sum(1 for i, c in enumerate(user_input) if i < len(sentence) and c == sentence[i])
    accuracy = (correct_chars / len(sentence)) * 100
    
    print(f"\nTime taken: {time_taken:.2f} seconds")
    print(f"Speed     : {wpm:.2f} WPM")
    print(f"Accuracy  : {accuracy:.2f}%")

if __name__ == "__main__":
    typing_test()
