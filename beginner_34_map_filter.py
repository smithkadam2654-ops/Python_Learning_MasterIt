def main():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # 1. Using map() to apply a function to all items
    # Let's square every number
    squared = list(map(lambda x: x**2, numbers))
    print(f"Original numbers: {numbers}")
    print(f"Squared (using map): {squared}")

    # 2. Using filter() to keep items that match a condition
    # Let's keep only the even numbers
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Evens (using filter): {evens}")

    # 3. Combining map() and filter()
    # Let's square only the even numbers
    squared_evens = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
    print(f"Squared Evens: {squared_evens}")

if __name__ == "__main__":
    main()
