def linear_search(arr, target):
    """
    Searches for a target value within a list using Linear Search.
    Returns the index if found, else -1.
    """
    for index, element in enumerate(arr):
        if element == target:
            return index
    return -1

if __name__ == "__main__":
    sample_list = [5, 12, 45, 7, 10, 89, 23]
    target_value = 10
    
    print(f"Searching for {target_value} in {sample_list}")
    result = linear_search(sample_list, target_value)
    
    if result != -1:
        print(f"Element {target_value} found at index {result}.")
    else:
        print(f"Element {target_value} not found in the list.")
