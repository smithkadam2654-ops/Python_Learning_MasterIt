"""
Beginner Project 61: Simple Shopping List
A small menu-based application to add, remove, and view items in a shopping list.
"""

def show_menu():
    print("\n--- Shopping List Menu ---")
    print("1. View list")
    print("2. Add item")
    print("3. Remove item")
    print("4. Clear list")
    print("5. Quit")

def main():
    shopping_list = []
    print("Welcome to your Shopping List app!")
    
    while True:
        show_menu()
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            if not shopping_list:
                print("\nYour list is empty.")
            else:
                print("\nYour Shopping List:")
                for index, item in enumerate(shopping_list, 1):
                    print(f"{index}. {item}")
                    
        elif choice == '2':
            item = input("What would you like to add? ").strip()
            if item:
                shopping_list.append(item)
                print(f"'{item}' added to the list.")
                
        elif choice == '3':
            item = input("What would you like to remove? ").strip()
            if item in shopping_list:
                shopping_list.remove(item)
                print(f"'{item}' removed from the list.")
            else:
                print(f"'{item}' was not found in the list.")
                
        elif choice == '4':
            shopping_list.clear()
            print("Your shopping list has been cleared.")
            
        elif choice == '5':
            print("Goodbye! Happy shopping!")
            break
            
        else:
            print("Invalid option. Please choose a number from 1 to 5.")

if __name__ == "__main__":
    main()
