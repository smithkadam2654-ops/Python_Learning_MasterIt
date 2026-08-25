def display_currencies(rates):
    print("\nAvailable Currencies:")
    for currency in rates.keys():
        print(f"- {currency}")
    print()

def main():
    # Base currency is USD
    exchange_rates = {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "JPY": 150.25,
        "AUD": 1.53,
        "CAD": 1.35,
        "INR": 83.12
    }
    
    print("--- Static Currency Converter ---")
    display_currencies(exchange_rates)
    
    while True:
        try:
            amount = float(input("Enter amount to convert: "))
        except ValueError:
            print("Please enter a valid numeric amount.")
            continue
            
        from_curr = input("From currency (e.g., USD): ").upper()
        if from_curr not in exchange_rates:
            print("Invalid source currency.")
            continue
            
        to_curr = input("To currency (e.g., EUR): ").upper()
        if to_curr not in exchange_rates:
            print("Invalid target currency.")
            continue
            
        # Convert to USD first (base), then to target
        amount_in_usd = amount / exchange_rates[from_curr]
        final_amount = amount_in_usd * exchange_rates[to_curr]
        
        print(f"\n{amount:.2f} {from_curr} = {final_amount:.2f} {to_curr}\n")
        
        cont = input("Convert another? (y/n): ").lower()
        if cont != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
