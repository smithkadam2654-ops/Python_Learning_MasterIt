def selection_sort(arr):
    """
    Sorts a list in ascending order using the Selection Sort algorithm.
    """
    n = len(arr)
    for i in range(n):
        # Find the minimum element in remaining unsorted array
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
                
        # Swap the found minimum element with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        
    return arr

if __name__ == "__main__":
    sample_list = [64, 25, 12, 22, 11]
    print(f"Original list: {sample_list}")
    sorted_list = selection_sort(sample_list.copy())
    print(f"Sorted list:   {sorted_list}")
