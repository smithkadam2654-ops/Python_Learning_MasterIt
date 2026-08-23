def binary_search(arr, target):
    """
    Searches for a target value within a sorted list using Binary Search.
    Returns the index if found, else -1.
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1

if __name__ == "__main__":
    # Binary search requires a sorted list
    sample_list = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target_value = 23
    
    print(f"Searching for {target_value} in {sample_list}")
    result = binary_search(sample_list, target_value)
    
    if result != -1:
        print(f"Element {target_value} found at index {result}.")
    else:
        print(f"Element {target_value} not found in the list.")
