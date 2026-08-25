def display_menu():
    print("\n--- Expense Tracker ---")
    print("1. Add an expense")
    print("2. View all expenses")
    print("3. View total expenses")
    print("4. Exit")

def main():
    expenses = []
    
    while True:
        display_menu()
        choice = input("Choose an option: ")
        
        if choice == '1':
            item = input("Enter the expense item description: ")
            try:
                amount = float(input("Enter the amount: $"))
                expenses.append({"item": item, "amount": amount})
                print("Expense added successfully!")
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
                
        elif choice == '2':
            if not expenses:
                print("\nNo expenses recorded yet.")
            else:
                print("\nList of Expenses:")
                for i, exp in enumerate(expenses, 1):
                    print(f"{i}. {exp['item']}: ${exp['amount']:.2f}")
                    
        elif choice == '3':
            total = sum(exp['amount'] for exp in expenses)
            print(f"\nTotal Expenses: ${total:.2f}")
            
        elif choice == '4':
            print("Exiting Expense Tracker.")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
