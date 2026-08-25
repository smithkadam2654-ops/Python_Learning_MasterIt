import random

def main():
    choices = ['rock', 'paper', 'scissors']
    print("Welcome to Rock, Paper, Scissors!")
    print("Type 'quit' to exit the game.")
    
    while True:
        user_choice = input("\nEnter rock, paper, or scissors: ").lower()
        
        if user_choice == 'quit':
            print("Thanks for playing!")
            break
            
        if user_choice not in choices:
            print("Invalid choice. Please try again.")
            continue
            
        computer_choice = random.choice(choices)
        print(f"Computer chose: {computer_choice}")
        
        if user_choice == computer_choice:
            print("It's a tie!")
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'paper' and computer_choice == 'rock') or \
             (user_choice == 'scissors' and computer_choice == 'paper'):
            print("You win!")
        else:
            print("Computer wins!")

if __name__ == "__main__":
    main()
