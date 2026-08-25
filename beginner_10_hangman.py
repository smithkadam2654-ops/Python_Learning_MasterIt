import random

def play_hangman():
    words = ['python', 'programming', 'computer', 'science', 'learning', 'algorithm']
    word_to_guess = random.choice(words)
    guessed_letters = []
    attempts_left = 6
    
    print("Welcome to Hangman!")
    
    while attempts_left > 0:
        display_word = ""
        for letter in word_to_guess:
            if letter in guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
                
        print(f"\nWord: {display_word}")
        print(f"Attempts left: {attempts_left}")
        print(f"Guessed letters: {', '.join(guessed_letters)}")
        
        if "_" not in display_word:
            print(f"\nCongratulations! You guessed the word '{word_to_guess}' correctly!")
            return
            
        guess = input("Guess a letter: ").lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single valid letter.")
            continue
            
        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue
            
        guessed_letters.append(guess)
        
        if guess in word_to_guess:
            print("Good guess!")
        else:
            print("Incorrect guess!")
            attempts_left -= 1
            
    print(f"\nGame Over! The word was '{word_to_guess}'.")

if __name__ == "__main__":
    play_hangman()
