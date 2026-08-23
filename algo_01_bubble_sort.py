def bubble_sort(arr):
    """
    Sorts a list in ascending order using the Bubble Sort algorithm.
    """
    n = len(arr)
    for i in range(n):
        # Track if any swaps were made in this pass
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # Swap elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no elements were swapped, the array is sorted
        if not swapped:
            break
    return arr

if __name__ == "__main__":
    sample_list = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original list: {sample_list}")
    sorted_list = bubble_sort(sample_list.copy())
    print(f"Sorted list:   {sorted_list}")
