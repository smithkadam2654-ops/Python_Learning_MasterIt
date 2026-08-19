def main():
    # A simple list of strings
    fruits = ["apple", "banana", "cherry", "date"]
    
    print("Printing fruits using a for loop:")
    for fruit in fruits:
        print(f"- {fruit}")
        
    print("\nPrinting squares from 1 to 5 using list comprehension:")
    # List comprehensions are a pythonic way to create lists
    squares = [x**2 for x in range(1, 6)]
    print(squares)

if __name__ == "__main__":
    main()
