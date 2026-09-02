"""
Beginner Project 47: Multiplication Table Generator
A script that generates a multiplication table for any given number.
"""

def generate_table(number, up_to=10):
    print(f"\nMultiplication Table for {number}:")
    print("-" * 25)
    for i in range(1, up_to + 1):
        print(f"{number} x {i:2} = {number * i}")
    print("-" * 25)

def main():
    print("Multiplication Table Generator")
    
    try:
        number = int(input("Enter a number to see its multiplication table: "))
        limit = input("How many rows? (Press ENTER for default 10): ").strip()
        
        if limit:
            limit = int(limit)
        else:
            limit = 10
            
        generate_table(number, limit)
            
    except ValueError:
        print("Invalid input! Please enter integers only.")

if __name__ == "__main__":
    main()
