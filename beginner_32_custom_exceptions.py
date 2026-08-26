# Create a custom exception by inheriting from the base Exception class
class InsufficientFundsError(Exception):
    """Exception raised when an account has insufficient funds for a withdrawal."""
    def __init__(self, balance, amount):
        super().__init__(f"Attempted to withdraw ${amount} with a balance of only ${balance}")
        self.balance = balance
        self.amount = amount

def withdraw(balance, amount):
    print(f"\nAttempting to withdraw ${amount} from a balance of ${balance}...")
    if amount > balance:
        # We manually trigger (raise) our custom exception
        raise InsufficientFundsError(balance, amount)
    
    new_balance = balance - amount
    print(f"Success! New balance is ${new_balance}")
    return new_balance

def main():
    current_balance = 100

    try:
        current_balance = withdraw(current_balance, 50)
        current_balance = withdraw(current_balance, 75)
    except InsufficientFundsError as e:
        print("Transaction Failed!")
        print(f"Error Message: {e}")

if __name__ == "__main__":
    main()
