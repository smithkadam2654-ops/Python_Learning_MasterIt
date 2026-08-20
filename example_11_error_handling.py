class InsufficientFundsError(Exception):
    """A custom exception raised for invalid banking operations."""
    pass

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        print(f"\nAttempting to withdraw ${amount}...")
        
        try:
            # Validate input type
            if not isinstance(amount, (int, float)):
                raise TypeError("Withdrawal amount must be a number.")
            
            # Validate business logic
            if amount < 0:
                raise ValueError("Cannot withdraw a negative amount.")
            
            if amount > self.balance:
                raise InsufficientFundsError(
                    f"Insufficient funds. Balance is ${self.balance}, tried to withdraw ${amount}."
                )
                
            # Perform withdrawal
            self.balance -= amount
            
        except (TypeError, ValueError) as e:
            print(f"Validation Error: {e}")
        except InsufficientFundsError as e:
            print(f"Transaction Failed: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
        else:
            # Executes ONLY if the try block succeeds (no exceptions raised)
            print(f"Success! New balance is ${self.balance}")
        finally:
            # Executes NO MATTER WHAT (success or failure)
            print("Transaction log updated.")

if __name__ == "__main__":
    account = BankAccount(100)
    
    # 1. Success case
    account.withdraw(40)
    
    # 2. Custom Exception case
    account.withdraw(200)
    
    # 3. Built-in Exception case
    account.withdraw(-10)
