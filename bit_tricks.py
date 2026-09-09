"""
Bit Tricks - Advanced bit manipulation techniques.
Features: Bit manipulation patterns, bit hacks, and optimization techniques.
"""

from typing import List


class BitTricks:
    """Advanced bit manipulation tricks and patterns."""
    
    @staticmethod
    def next_power_of_two(n: int) -> int:
        """
        Find next power of two greater than or equal to n.
        
        Args:
            n: Number
            
        Returns:
            Next power of two
        """
        if n <= 0:
            return 1
        
        n -= 1
        n |= n >> 1
        n |= n >> 2
        n |= n >> 4
        n |= n >> 8
        n |= n >> 16
        n |= n >> 32
        return n + 1
    
    @staticmethod
    def previous_power_of_two(n: int) -> int:
        """
        Find previous power of two less than or equal to n.
        
        Args:
            n: Number
            
        Returns:
            Previous power of two
        """
        if n <= 0:
            return 0
        
        n |= n >> 1
        n |= n >> 2
        n |= n >> 4
        n |= n >> 8
        n |= n >> 16
        n |= n >> 32
        return n - (n >> 1)
    
    @staticmethod
    def is_palindrome(n: int) -> bool:
        """
        Check if binary representation is palindrome.
        
        Args:
            n: Number
            
        Returns:
            True if binary palindrome
        """
        if n < 0:
            return False
        
        original = n
        reversed_n = 0
        
        while n > 0:
            reversed_n = (reversed_n << 1) | (n & 1)
            n >>= 1
        
        return original == reversed_n
    
    @staticmethod
    def add_without_plus(a: int, b: int) -> int:
        """
        Add two numbers without using + operator.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum
        """
        while b != 0:
            carry = a & b
            a = a ^ b
            b = carry << 1
        return a
    
    @staticmethod
    def subtract_without_minus(a: int, b: int) -> int:
        """
        Subtract two numbers without using - operator.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Difference
        """
        while b != 0:
            borrow = (~a) & b
            a = a ^ b
            b = borrow << 1
        return a
    
    @staticmethod
    def multiply_without_multiply(a: int, b: int) -> int:
        """
        Multiply two numbers without using * operator.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product
        """
        result = 0
        while b > 0:
            if b & 1:
                result = BitTricks.add_without_plus(result, a)
            a <<= 1
            b >>= 1
        return result
    
    @staticmethod
    def divide_without_divide(dividend: int, divisor: int) -> int:
        """
        Divide two numbers without using / operator.
        
        Args:
            dividend: Dividend
            divisor: Divisor
            
        Returns:
            Quotient
        """
        if divisor == 0:
            raise ZeroDivisionError("division by zero")
        
        sign = -1 if ((dividend < 0) ^ (divisor < 0)) else 1
        dividend = abs(dividend)
        divisor = abs(divisor)
        
        quotient = 0
        temp = 0
        
        for i in range(31, -1, -1):
            if temp + (divisor << i) <= dividend:
                temp += divisor << i
                quotient |= 1 << i
        
        return sign * quotient
    
    @staticmethod
    def find_missing_number(nums: List[int]) -> int:
        """
        Find missing number in range [0, n] using XOR.
        
        Args:
            nums: List of n numbers with one missing
            
        Returns:
            Missing number
        """
        n = len(nums)
        xor_all = 0
        xor_nums = 0
        
        for i in range(n + 1):
            xor_all ^= i
        
        for num in nums:
            xor_nums ^= num
        
        return xor_all ^ xor_nums
    
    @staticmethod
    def find_two_missing_numbers(nums: List[int]) -> tuple:
        """
        Find two missing numbers in range [1, n+2].
        
        Args:
            nums: List of n numbers with two missing
            
        Returns:
            Tuple of two missing numbers
        """
        n = len(nums) + 2
        xor_all = 0
        xor_nums = 0
        
        for i in range(1, n + 1):
            xor_all ^= i
        
        for num in nums:
            xor_nums ^= num
        
        xor = xor_all ^ xor_nums
        
        # Find rightmost set bit
        rightmost_set_bit = xor & -xor
        
        x = 0
        y = 0
        
        for i in range(1, n + 1):
            if i & rightmost_set_bit:
                x ^= i
            else:
                y ^= i
        
        for num in nums:
            if num & rightmost_set_bit:
                x ^= num
            else:
                y ^= num
        
        return (x, y)
    
    @staticmethod
    def count_bits_from_zero_to_n(n: int) -> int:
        """
        Count total set bits from 0 to n.
        
        Args:
            n: Upper bound
            
        Returns:
            Total count of set bits
        """
        n += 1
        count = 0
        power_of_two = 2
        
        while power_of_two <= n:
            count += (n // power_of_two) * (power_of_two // 2)
            count += max(0, n % power_of_two - power_of_two // 2)
            power_of_two <<= 1
        
        return count
    
    @staticmethod
    def rotate_left(n: int, d: int, bits: int = 32) -> int:
        """
        Rotate bits left by d positions.
        
        Args:
            n: Number
            d: Rotation amount
            bits: Number of bits (default 32)
            
        Returns:
            Rotated number
        """
        d = d % bits
        return ((n << d) | (n >> (bits - d))) & ((1 << bits) - 1)
    
    @staticmethod
    def rotate_right(n: int, d: int, bits: int = 32) -> int:
        """
        Rotate bits right by d positions.
        
        Args:
            n: Number
            d: Rotation amount
            bits: Number of bits (default 32)
            
        Returns:
            Rotated number
        """
        d = d % bits
        return ((n >> d) | (n << (bits - d))) & ((1 << bits) - 1)
    
    @staticmethod
    def swap_nibbles(n: int) -> int:
        """
        Swap nibbles in a byte.
        
        Args:
            n: Number (byte)
            
        Returns:
            Number with swapped nibbles
        """
        return ((n & 0x0F) << 4) | ((n & 0xF0) >> 4)
    
    @staticmethod
    def is_subset_sum_possible(nums: List[int], target: int) -> bool:
        """
        Check if subset sum is possible using bitmask.
        
        Args:
            nums: List of positive integers
            target: Target sum
            
        Returns:
            True if subset sum possible
        """
        n = len(nums)
        for mask in range(1 << n):
            current_sum = 0
            for i in range(n):
                if mask & (1 << i):
                    current_sum += nums[i]
            if current_sum == target:
                return True
        return False


def main() -> None:
    """Demonstrate bit tricks."""
    
    print("=== Bit Tricks Demo ===")
    
    # Next/Previous power of two
    print("\n--- Power of Two ---")
    for n in [5, 10, 17, 32, 33]:
        print(f"{n}: next={BitTricks.next_power_of_two(n)}, prev={BitTricks.previous_power_of_two(n)}")
    
    # Binary palindrome
    print("\n--- Binary Palindrome ---")
    for n in [5, 9, 10, 15]:
        print(f"{n} (binary: {bin(n)[2:]}): {BitTricks.is_palindrome(n)}")
    
    # Arithmetic without operators
    print("\n--- Arithmetic Without Operators ---")
    a, b = 5, 3
    print(f"{a} + {b} = {BitTricks.add_without_plus(a, b)}")
    print(f"{a} - {b} = {BitTricks.subtract_without_minus(a, b)}")
    print(f"{a} * {b} = {BitTricks.multiply_without_multiply(a, b)}")
    print(f"{a} / {b} = {BitTricks.divide_without_divide(a, b)}")
    
    # Missing number
    print("\n--- Missing Number ---")
    nums = [0, 1, 2, 4, 5]
    print(f"Array: {nums}")
    print(f"Missing: {BitTricks.find_missing_number(nums)}")
    
    # Two missing numbers
    print("\n--- Two Missing Numbers ---")
    nums_two = [1, 2, 4, 5, 6]
    print(f"Array: {nums_two}")
    print(f"Missing: {BitTricks.find_two_missing_numbers(nums_two)}")
    
    # Count bits from 0 to n
    print("\n--- Count Bits from 0 to n ---")
    for n in [5, 10, 15]:
        print(f"0 to {n}: {BitTricks.count_bits_from_zero_to(n)}")
    
    # Rotate bits
    print("\n--- Rotate Bits ---")
    n = 0b1101
    print(f"Original: {bin(n)}")
    print(f"Rotate left 2: {bin(BitTricks.rotate_left(n, 2, 4))}")
    print(f"Rotate right 2: {bin(BitTricks.rotate_right(n, 2, 4))}")
    
    # Swap nibbles
    print("\n--- Swap Nibbles ---")
    for n in [0b10011010, 0b10101010]:
        print(f"{bin(n)} -> {bin(BitTricks.swap_nibbles(n))}")
    
    # Subset sum
    print("\n--- Subset Sum ---")
    nums = [1, 2, 3, 4]
    target = 7
    print(f"Array: {nums}, target: {target}")
    print(f"Possible: {BitTricks.is_subset_sum_possible(nums, target)}")


if __name__ == "__main__":
    main()
