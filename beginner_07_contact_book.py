def display_menu():
    print("\n--- Contact Book ---")
    print("1. Add a contact")
    print("2. View all contacts")
    print("3. Search for a contact")
    print("4. Delete a contact")
    print("5. Exit")

def main():
    contacts = {}
    
    while True:
        display_menu()
        choice = input("Choose an option: ")
        
        if choice == '1':
            name = input("Enter contact name: ")
            phone = input("Enter phone number: ")
            contacts[name] = phone
            print(f"Contact {name} added successfully!")
            
        elif choice == '2':
            if not contacts:
                print("\nContact book is empty.")
            else:
                print("\nContacts:")
                for name, phone in contacts.items():
                    print(f"- {name}: {phone}")
                    
        elif choice == '3':
            search_name = input("Enter name to search: ")
            if search_name in contacts:
                print(f"Found: {search_name} - {contacts[search_name]}")
            else:
                print("Contact not found.")
                
        elif choice == '4':
            del_name = input("Enter name to delete: ")
            if del_name in contacts:
                del contacts[del_name]
                print(f"Contact {del_name} deleted.")
            else:
                print("Contact not found.")
                
        elif choice == '5':
            print("Exiting Contact Book.")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
