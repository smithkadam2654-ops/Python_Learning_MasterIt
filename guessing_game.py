import random

def guess_number():
    number_to_guess = random.randint(1, 100)
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

    # Limited to 5 attempts for a quick run
    attempts = 5
    
    for i in range(attempts):
        try:
            # For demonstration, we'll just simulate a guess if running unattended
            # In a real game, you would use input()
            # guess = int(input(f"Attempt {i+1}/{attempts} - Enter your guess: "))
            guess = random.randint(1, 100)
            print(f"Attempt {i+1}: Guessing {guess}...")
            
            if guess < number_to_guess:
                print("Too low!")
            elif guess > number_to_guess:
                print("Too high!")
            else:
                print(f"Congratulations! You guessed the number in {i+1} attempts.")
                return
        except ValueError:
            print("Please enter a valid integer.")
            
    print(f"Game over! The number was {number_to_guess}.")

if __name__ == "__main__":
    guess_number()
