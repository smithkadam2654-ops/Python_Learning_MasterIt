def insertion_sort(arr):
    """
    Sorts a list in ascending order using the Insertion Sort algorithm.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        
    return arr

if __name__ == "__main__":
    sample_list = [12, 11, 13, 5, 6]
    print(f"Original list: {sample_list}")
    sorted_list = insertion_sort(sample_list.copy())
    print(f"Sorted list:   {sorted_list}")
