def main():
    numbers = [5, 2, 8, 1, 9]
    print(f"Original list: {numbers}")
    
    # Appending adds an element to the end of the list
    numbers.append(4)
    print(f"After appending 4: {numbers}")
    
    # Sorting modifies the list to be in ascending order
    numbers.sort()
    print(f"After sorting: {numbers}")
    
    # Popping removes and returns the last element
    last_item = numbers.pop()
    print(f"Popped item: {last_item}")
    print(f"List after popping: {numbers}")

if __name__ == "__main__":
    main()
