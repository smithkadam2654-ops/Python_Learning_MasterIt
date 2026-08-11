#!/usr/bin/env python3
"""
Simple Bank System
Basic banking operations: deposit, withdraw, check balance
"""

class BankAccount:
    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transaction_history = []
    
    def deposit(self, amount):
        """Deposit money into account."""
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: ${amount:.2f}")
            return True, f"Deposited ${amount:.2f} successfully"
        else:
            return False, "Deposit amount must be positive"
    
    def withdraw(self, amount):
        """Withdraw money from account."""
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                self.transaction_history.append(f"Withdrew: ${amount:.2f}")
                return True, f"Withdrew ${amount:.2f} successfully"
            else:
                return False, f"Insufficient funds. Current balance: ${self.balance:.2f}"
        else:
            return False, "Withdrawal amount must be positive"
    
    def check_balance(self):
        """Check current balance."""
        return self.balance, f"Current balance: ${self.balance:.2f}"
    
    def show_history(self):
        """Show transaction history."""
        if not self.transaction_history:
            return "No transactions yet."
        
        history_text = "Transaction History:\n"
        for i, transaction in enumerate(self.transaction_history, 1):
            history_text += f"{i}. {transaction}\n"
        return history_text
    
    def __str__(self):
        return f"Account Holder: {self.account_holder}, Balance: ${self.balance:.2f}"

def get_valid_amount(prompt):
    """Get valid positive amount from user."""
    while True:
        try:
            amount = float(input(prompt))
            if amount > 0:
                return amount
            else:
                print("Amount must be positive!")
        except ValueError:
            print("Please enter a valid number!")

def main():
    print("=== Simple Bank System ===")
    
    # Get account holder name
    account_holder = input("Enter account holder name: ").strip()
    if not account_holder:
        account_holder = "Customer"
    
    # Create account with optional initial deposit
    print("Would you like to make an initial deposit?")
    initial_deposit = input("Enter amount (or press Enter to skip): ")
    
    if initial_deposit:
        try:
            initial_balance = float(initial_deposit)
            if initial_balance > 0:
                account = BankAccount(account_holder, initial_balance)
            else:
                account = BankAccount(account_holder)
        except ValueError:
            account = BankAccount(account_holder)
    else:
        account = BankAccount(account_holder)
    
    print(f"\nWelcome, {account_holder}!")
    print(f"Your account has been created with balance: ${account.balance:.2f}")
    
    while True:
        print(f"\n=== Menu ===")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transaction History")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            balance, message = account.check_balance()
            print(message)
        
        elif choice == '2':
            amount = get_valid_amount("Enter deposit amount: $")
            success, message = account.deposit(amount)
            print(message)
        
        elif choice == '3':
            amount = get_valid_amount("Enter withdrawal amount: $")
            success, message = account.withdraw(amount)
            print(message)
        
        elif choice == '4':
            print(account.show_history())
        
        elif choice == '5':
            print("Thank you for using our banking service!")
            break
        
        else:
            print("Invalid choice! Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()