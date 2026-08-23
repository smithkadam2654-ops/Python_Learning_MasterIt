def quick_sort(arr):
    """
    Sorts a list in ascending order using the Quick Sort algorithm.
    """
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return quick_sort(left) + middle + quick_sort(right)

if __name__ == "__main__":
    sample_list = [10, 7, 8, 9, 1, 5]
    print(f"Original list: {sample_list}")
    sorted_list = quick_sort(sample_list)
    print(f"Sorted list:   {sorted_list}")
