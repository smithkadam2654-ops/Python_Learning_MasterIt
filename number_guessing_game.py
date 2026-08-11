#!/usr/bin/env python3
"""
Number Guessing Game
A simple guessing game where the player tries to guess a random number
"""

import random

def generate_random_number(difficulty):
    """Generate random number based on difficulty level."""
    if difficulty == 'easy':
        return random.randint(1, 50)
    elif difficulty == 'medium':
        return random.randint(1, 100)
    elif difficulty == 'hard':
        return random.randint(1, 200)
    elif difficulty == 'expert':
        return random.randint(1, 500)
    else:
        return random.randint(1, 100)

def get_valid_input(prompt, min_val, max_val):
    """Get valid input from user within range."""
    while True:
        try:
            guess = int(input(prompt))
            if min_val <= guess <= max_val:
                return guess
            else:
                print(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("Please enter a valid number!")

def play_game():
    print("=== Number Guessing Game ===")
    
    # Difficulty selection
    difficulties = {
        'easy': (1, 50, 10),
        'medium': (1, 100, 10),
        'hard': (1, 200, 15),
        'expert': (1, 500, 20)
    }
    
    print("Choose difficulty:")
    print("1. Easy (1-50, 10 attempts)")
    print("2. Medium (1-100, 10 attempts)")
    print("3. Hard (1-200, 15 attempts)")
    print("4. Expert (1-500, 20 attempts)")
    
    while True:
        choice = input("Enter difficulty (1-4): ")
        if choice == '1':
            difficulty_name = 'easy'
            min_val, max_val, max_attempts = difficulties['easy']
            break
        elif choice == '2':
            difficulty_name = 'medium'
            min_val, max_val, max_attempts = difficulties['medium']
            break
        elif choice == '3':
            difficulty_name = 'hard'
            min_val, max_val, max_attempts = difficulties['hard']
            break
        elif choice == '4':
            difficulty_name = 'expert'
            min_val, max_val, max_attempts = difficulties['expert']
            break
        else:
            print("Please enter a number between 1 and 4")
    
    # Generate target number
    target_number = generate_random_number(difficulty_name)
    attempts = 0
    
    print(f"\nYou chose {difficulty_name} mode!")
    print(f"Guess a number between {min_val} and {max_val}")
    print(f"You have {max_attempts} attempts")
    
    while attempts < max_attempts:
        remaining_attempts = max_attempts - attempts
        guess = get_valid_input(
            f"Attempt {attempts + 1}/{max_attempts} (Remaining: {remaining_attempts}): ",
            min_val, max_val
        )
        attempts += 1
        
        if guess == target_number:
            print(f"\n🎉 Congratulations! You guessed the number {target_number} in {attempts} attempts!")
            return True
        elif guess < target_number:
            print("Too low! Try a higher number.")
        else:
            print("Too high! Try a lower number.")
    
    print(f"\n❌ Game Over! The number was {target_number}")
    return False

def main():
    print("=== Number Guessing Game ===")
    
    play_again = 'y'
    wins = 0
    games_played = 0
    
    while play_again.lower() == 'y':
        games_played += 1
        if play_game():
            wins += 1
        play_again = input("\nDo you want to play again? (y/n): ")
    
    if games_played > 0:
        win_rate = (wins / games_played) * 100
        print(f"\n=== Game Summary ===")
        print(f"Games played: {games_played}")
        print(f"Wins: {wins}")
        print(f"Win rate: {win_rate:.1f}%")

if __name__ == "__main__":
    main()