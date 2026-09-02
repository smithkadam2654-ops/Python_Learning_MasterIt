"""
Beginner Project 60: Even and Odd Sorter
Takes a comma-separated string of numbers, and sorts them into even and odd lists.
"""

def main():
    print("Even and Odd Number Sorter")
    
    user_input = input("Enter a list of numbers separated by commas (e.g., 5, 2, 8, 11): ")
    
    try:
        # Split by comma, strip spaces, and convert to integers
        numbers = [int(num.strip()) for num in user_input.split(',')]
        
        even_nums = []
        odd_nums = []
        
        for num in numbers:
            if num % 2 == 0:
                even_nums.append(num)
            else:
                odd_nums.append(num)
                
        print("\nSorting Results:")
        print(f"Even numbers: {even_nums}")
        print(f"Odd numbers: {odd_nums}")
        
    except ValueError:
        print("Invalid input! Please make sure to enter only numbers separated by commas.")

if __name__ == "__main__":
    main()
