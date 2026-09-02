"""
Beginner Project 49: Simple Interest Calculator
Calculates the simple interest earned over a period of time.
Formula: A = P(1 + rt) where P=Principal, r=rate, t=time
"""

def calculate_simple_interest(principal, rate, time_years):
    return principal * (rate / 100) * time_years

def main():
    print("Simple Interest Calculator")
    
    try:
        p = float(input("Enter the principal amount ($): "))
        r = float(input("Enter the annual interest rate (in %): "))
        t = float(input("Enter the time in years: "))
        
        if p < 0 or r < 0 or t < 0:
            print("Please enter positive values.")
            return
            
        interest = calculate_simple_interest(p, r, t)
        total_amount = p + interest
        
        print(f"\nInterest Earned: ${interest:.2f}")
        print(f"Total Amount after {t} years: ${total_amount:.2f}")
        
    except ValueError:
        print("Invalid input! Please enter numerical values.")

if __name__ == "__main__":
    main()
