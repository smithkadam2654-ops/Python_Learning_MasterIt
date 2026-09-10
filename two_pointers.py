"""
Two Pointers Technique - Pattern for array/string problems.
Features: Fast/slow pointers, left/right pointers, and collision detection.
"""

from typing import List, Optional


class TwoPointers:
    """Two pointers technique implementations."""
    
    @staticmethod
    def two_sum_sorted(nums: List[int], target: int) -> Optional[List[int]]:
        """
        Find two numbers that sum to target in sorted array.
        
        Args:
            nums: Sorted array
            target: Target sum
            
        Returns:
            Indices of two numbers or None
        """
        left, right = 0, len(nums) - 1
        
        while left < right:
            current_sum = nums[left] + nums[right]
            
            if current_sum == target:
                return [left, right]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        
        return None
    
    @staticmethod
    def three_sum(nums: List[int]) -> List[List[int]]:
        """
        Find all unique triplets that sum to zero.
        
        Args:
            nums: Unsorted array
            
        Returns:
            List of triplets
        """
        nums.sort()
        result = []
        
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue  # Skip duplicates
            
            left, right = i + 1, len(nums) - 1
            
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                
                if total == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    
                    # Skip duplicates
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif total < 0:
                    left += 1
                else:
                    right -= 1
        
        return result
    
    @staticmethod
    def four_sum(nums: List[int], target: int) -> List[List[int]]:
        """
        Find all unique quadruplets that sum to target.
        
        Args:
            nums: Unsorted array
            target: Target sum
            
        Returns:
            List of quadruplets
        """
        nums.sort()
        result = []
        n = len(nums)
        
        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            for j in range(i + 1, n - 2):
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue
                
                left, right = j + 1, n - 1
                
                while left < right:
                    total = nums[i] + nums[j] + nums[left] + nums[right]
                    
                    if total == target:
                        result.append([nums[i], nums[j], nums[left], nums[right]])
                        left += 1
                        right -= 1
                        
                        while left < right and nums[left] == nums[left - 1]:
                            left += 1
                        while left < right and nums[right] == nums[right + 1]:
                            right -= 1
                    elif total < target:
                        left += 1
                    else:
                        right -= 1
        
        return result
    
    @staticmethod
    def is_palindrome(s: str) -> bool:
        """
        Check if string is palindrome (ignoring case and non-alphanumeric).
        
        Args:
            s: Input string
            
        Returns:
            True if palindrome
        """
        left, right = 0, len(s) - 1
        
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            
            if s[left].lower() != s[right].lower():
                return False
            
            left += 1
            right -= 1
        
        return True
    
    @staticmethod
    def is_palindrome_array(nums: List[int]) -> bool:
        """
        Check if array is palindrome.
        
        Args:
            nums: Input array
            
        Returns:
            True if palindrome
        """
        left, right = 0, len(nums) - 1
        
        while left < right:
            if nums[left] != nums[right]:
                return False
            left += 1
            right -= 1
        
        return True
    
    @staticmethod
    def remove_duplicates_sorted(nums: List[int]) -> int:
        """
        Remove duplicates from sorted array in-place.
        
        Args:
            nums: Sorted array
            
        Returns:
            New length
        """
        if not nums:
            return 0
        
        write_index = 1
        
        for i in range(1, len(nums)):
            if nums[i] != nums[write_index - 1]:
                nums[write_index] = nums[i]
                write_index += 1
        
        return write_index
    
    @staticmethod
    def remove_element(nums: List[int], val: int) -> int:
        """
        Remove all instances of val in-place.
        
        Args:
            nums: Array
            val: Value to remove
            
        Returns:
            New length
        """
        write_index = 0
        
        for num in nums:
            if num != val:
                nums[write_index] = num
                write_index += 1
        
        return write_index
    
    @staticmethod
    def move_zeros(nums: List[int]) -> None:
        """
        Move all zeros to end while maintaining order.
        
        Args:
            nums: Array (modified in-place)
        """
        write_index = 0
        
        for num in nums:
            if num != 0:
                nums[write_index] = num
                write_index += 1
        
        # Fill remaining with zeros
        for i in range(write_index, len(nums)):
            nums[i] = 0
    
    @staticmethod
    def sort_colors(nums: List[int]) -> None:
        """
        Sort array of 0s, 1s, and 2s (Dutch national flag).
        
        Args:
            nums: Array (modified in-place)
        """
        low, mid, high = 0, 0, len(nums) - 1
        
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
    
    @staticmethod
    def trap_rain_water(height: List[int]) -> int:
        """
        Calculate trapped rain water between bars.
        
        Args:
            height: Array of bar heights
            
        Returns:
            Total trapped water
        """
        if not height:
            return 0
        
        left, right = 0, len(height) - 1
        left_max, right_max = height[left], height[right]
        water = 0
        
        while left < right:
            if left_max < right_max:
                left += 1
                left_max = max(left_max, height[left])
                water += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                water += right_max - height[right]
        
        return water
    
    @staticmethod
    def container_with_most_water(height: List[int]) -> int:
        """
        Find maximum area between two vertical lines.
        
        Args:
            height: Array of heights
            
        Returns:
            Maximum area
        """
        left, right = 0, len(height) - 1
        max_area = 0
        
        while left < right:
            area = min(height[left], height[right]) * (right - left)
            max_area = max(max_area, area)
            
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        
        return max_area
    
    @staticmethod
    def has_cycle(head) -> bool:
        """
        Detect cycle in linked list using slow/fast pointers.
        
        Args:
            head: Linked list head node
            
        Returns:
            True if cycle exists
        """
        if not head or not head.next:
            return False
        
        slow = head
        fast = head.next
        
        while fast and fast.next:
            if slow == fast:
                return True
            slow = slow.next
            fast = fast.next.next
        
        return False
    
    @staticmethod
    def find_cycle_start(head):
        """
        Find start node of cycle in linked list.
        
        Args:
            head: Linked list head node
            
        Returns:
            Start node of cycle or None
        """
        if not head or not head.next:
            return None
        
        # Find meeting point
        slow = head
        fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        
        if slow != fast:
            return None
        
        # Find cycle start
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        
        return slow
    
    @staticmethod
    def find_middle(head):
        """
        Find middle node of linked list.
        
        Args:
            head: Linked list head node
            
        Returns:
            Middle node
        """
        if not head:
            return None
        
        slow = head
        fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        return slow
    
    @staticmethod
    def is_palindrome_linked_list(head) -> bool:
        """
        Check if linked list is palindrome.
        
        Args:
            head: Linked list head node
            
        Returns:
            True if palindrome
        """
        if not head or not head.next:
            return True
        
        # Find middle
        slow = head
        fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Reverse second half
        prev = None
        current = slow
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        # Compare
        left = head
        right = prev
        
        while right:
            if left.val != right.val:
                return False
            left = left.next
            right = right.next
        
        return True
    
    @staticmethod
    def merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
        """
        Merge two sorted arrays.
        
        Args:
            arr1: First sorted array
            arr2: Second sorted array
            
        Returns:
            Merged sorted array
        """
        result = []
        i, j = 0, 0
        
        while i < len(arr1) and j < len(arr2):
            if arr1[i] <= arr2[j]:
                result.append(arr1[i])
                i += 1
            else:
                result.append(arr2[j])
                j += 1
        
        result.extend(arr1[i:])
        result.extend(arr2[j:])
        
        return result
    
    @staticmethod
    def intersect_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
        """
        Find intersection of two sorted arrays.
        
        Args:
            arr1: First sorted array
            arr2: Second sorted array
            
        Returns:
            Intersection
        """
        result = []
        i, j = 0, 0
        
        while i < len(arr1) and j < len(arr2):
            if arr1[i] == arr2[j]:
                result.append(arr1[i])
                i += 1
                j += 1
            elif arr1[i] < arr2[j]:
                i += 1
            else:
                j += 1
        
        return result


def main() -> None:
    """Demonstrate two pointers technique."""
    
    print("=== Two Pointers Demo ===")
    
    # Two sum
    print("\n--- Two Sum (Sorted) ---")
    nums = [2, 7, 11, 15]
    target = 9
    print(f"Array: {nums}, target: {target}")
    print(f"Indices: {TwoPointers.two_sum_sorted(nums, target)}")
    
    # Three sum
    print("\n--- Three Sum ---")
    nums = [-1, 0, 1, 2, -1, -4]
    print(f"Array: {nums}")
    print(f"Triplets summing to 0: {TwoPointers.three_sum(nums)}")
    
    # Four sum
    print("\n--- Four Sum ---")
    nums = [1, 0, -1, 0, -2, 2]
    target = 0
    print(f"Array: {nums}, target: {target}")
    print(f"Quadruplets: {TwoPointers.four_sum(nums, target)}")
    
    # Palindrome string
    print("\n--- Palindrome String ---")
    s = "A man, a plan, a canal: Panama"
    print(f"'{s}': {TwoPointers.is_palindrome(s)}")
    
    # Palindrome array
    print("\n--- Palindrome Array ---")
    nums = [1, 2, 3, 2, 1]
    print(f"Array: {nums}")
    print(f"Is palindrome: {TwoPointers.is_palindrome_array(nums)}")
    
    # Remove duplicates
    print("\n--- Remove Duplicates (Sorted) ---")
    nums = [1, 1, 2, 2, 2, 3, 4, 4, 5]
    print(f"Original: {nums}")
    new_len = TwoPointers.remove_duplicates_sorted(nums)
    print(f"After: {nums[:new_len]}, length: {new_len}")
    
    # Remove element
    print("\n--- Remove Element ---")
    nums = [3, 2, 2, 3]
    val = 3
    print(f"Original: {nums}, val: {val}")
    new_len = TwoPointers.remove_element(nums, val)
    print(f"After: {nums[:new_len]}, length: {new_len}")
    
    # Move zeros
    print("\n--- Move Zeros ---")
    nums = [0, 1, 0, 3, 12]
    print(f"Original: {nums}")
    TwoPointers.move_zeros(nums)
    print(f"After: {nums}")
    
    # Sort colors
    print("\n--- Sort Colors ---")
    nums = [2, 0, 2, 1, 1, 0]
    print(f"Original: {nums}")
    TwoPointers.sort_colors(nums)
    print(f"After: {nums}")
    
    # Trap rain water
    print("\n--- Trap Rain Water ---")
    height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"Heights: {height}")
    print(f"Trapped water: {TwoPointers.trap_rain_water(height)}")
    
    # Container with most water
    print("\n--- Container with Most Water ---")
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"Heights: {height}")
    print(f"Max area: {TwoPointers.container_with_most_water(height)}")
    
    # Merge sorted arrays
    print("\n--- Merge Sorted Arrays ---")
    arr1 = [1, 3, 5, 7]
    arr2 = [2, 4, 6, 8]
    print(f"Array 1: {arr1}")
    print(f"Array 2: {arr2}")
    print(f"Merged: {TwoPointers.merge_sorted_arrays(arr1, arr2)}")
    
    # Intersect sorted arrays
    print("\n--- Intersect Sorted Arrays ---")
    arr1 = [1, 2, 3, 4, 5]
    arr2 = [2, 4, 6, 8]
    print(f"Array 1: {arr1}")
    print(f"Array 2: {arr2}")
    print(f"Intersection: {TwoPointers.intersect_sorted_arrays(arr1, arr2)}")


if __name__ == "__main__":
    main()
