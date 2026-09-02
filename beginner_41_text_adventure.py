"""
Beginner Project 41: Text Adventure Game
A simple text-based adventure game using functions and conditional logic.
"""

def intro():
    print("Welcome to the Dark Forest Adventure!")
    print("You find yourself at a fork in the path.")
    print("To your left, the path looks dark and foreboding.")
    print("To your right, the path seems lighter but is covered in thorns.")
    
    choice = input("Which path do you choose? (left/right): ").lower().strip()
    
    if choice == 'left':
        dark_path()
    elif choice == 'right':
        thorn_path()
    else:
        print("Invalid choice. Please type 'left' or 'right'.")
        intro()

def dark_path():
    print("\nYou walk down the dark path. It's very hard to see.")
    print("Suddenly, you hear a growl.")
    choice = input("Do you run or stand your ground? (run/stand): ").lower().strip()
    
    if choice == 'run':
        print("\nYou ran back to safety. You survived, but the adventure is over.")
    elif choice == 'stand':
        print("\nA friendly dog emerges from the shadows! He leads you to a treasure chest. You win!")
    else:
        print("Invalid choice.")
        dark_path()

def thorn_path():
    print("\nYou carefully navigate the thorns. It's painful but you push through.")
    print("You reach a clearing and see a mysterious glowing stone.")
    choice = input("Do you touch the stone or ignore it? (touch/ignore): ").lower().strip()
    
    if choice == 'touch':
        print("\nThe stone gives you magical powers! You are now a wizard. You win!")
    elif choice == 'ignore':
        print("\nYou ignore the stone and walk home. A boring but safe end to your journey.")
    else:
        print("Invalid choice.")
        thorn_path()

if __name__ == "__main__":
    intro()
