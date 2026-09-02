"""
Beginner Project 59: Random Name Picker
Allows the user to input a list of names and randomly picks a winner.
"""
import random

def main():
    print("Random Name Picker (Raffle Simulator)")
    print("Enter names one by one. Type 'done' when you are finished.")
    
    names = []
    
    while True:
        name = input("Enter a name: ").strip()
        if name.lower() == 'done':
            break
        if name:
            names.append(name)
            
    if not names:
        print("No names were entered. Nobody wins!")
        return
        
    print("\nPicking a random winner...")
    winner = random.choice(names)
    
    print("-" * 30)
    print(f"🎉 THE WINNER IS: {winner} 🎉")
    print("-" * 30)

if __name__ == "__main__":
    main()
