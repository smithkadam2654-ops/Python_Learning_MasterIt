"""
Bit Manipulation - Common bit manipulation operations and algorithms.
Features: Bit operations, bit tricks, and practical applications.
"""

from typing import List


class BitUtils:
    """Utility class for bit manipulation operations."""
    
    @staticmethod
    def get_bit(num: int, position: int) -> bool:
        """
        Get bit at specific position (0-indexed from right).
        
        Args:
            num: Integer to check
            position: Bit position (0 = LSB)
            
        Returns:
            True if bit is 1, False if bit is 0
        """
        return (num >> position) & 1 == 1
    
    @staticmethod
    def set_bit(num: int, position: int) -> int:
        """
        Set bit at specific position to 1.
        
        Args:
            num: Integer to modify
            position: Bit position (0 = LSB)
            
        Returns:
            Modified integer
        """
        return num | (1 << position)
    
    @staticmethod
    def clear_bit(num: int, position: int) -> int:
        """
        Clear bit at specific position (set to 0).
        
        Args:
            num: Integer to modify
            position: Bit position (0 = LSB)
            
        Returns:
            Modified integer
        """
        return num & ~(1 << position)
    
    @staticmethod
    def toggle_bit(num: int, position: int) -> int:
        """
        Toggle bit at specific position.
        
        Args:
            num: Integer to modify
            position: Bit position (0 = LSB)
            
        Returns:
            Modified integer
        """
        return num ^ (1 << position)
    
    @staticmethod
    def is_power_of_two(num: int) -> bool:
        """
        Check if number is a power of two.
        
        Args:
            num: Integer to check
            
        Returns:
            True if power of two, False otherwise
        """
        return num > 0 and (num & (num - 1)) == 0
    
    @staticmethod
    def count_set_bits(num: int) -> int:
        """
        Count number of set bits (1s) in binary representation.
        
        Args:
            num: Integer to count bits in
            
        Returns:
            Number of set bits
        """
        count = 0
        while num:
            count += num & 1
            num >>= 1
        return count
    
    @staticmethod
    def count_set_bits_optimized(num: int) -> int:
        """
        Count set bits using Brian Kernighan's algorithm.
        
        Args:
            num: Integer to count bits in
            
        Returns:
            Number of set bits
        """
        count = 0
        while num:
            num &= num - 1  # Clear the least significant set bit
            count += 1
        return count
    
    @staticmethod
    def get_most_significant_bit(num: int) -> int:
        """
        Get position of most significant set bit.
        
        Args:
            num: Integer to check
            
        Returns:
            Position of MSB (0-indexed)
        """
        if num == 0:
            return -1
        
        position = 0
        while num > 1:
            num >>= 1
            position += 1
        return position
    
    @staticmethod
    def is_even(num: int) -> bool:
        """
        Check if number is even using bit operation.
        
        Args:
            num: Integer to check
            
        Returns:
            True if even, False if odd
        """
        return (num & 1) == 0
    
    @staticmethod
    def is_odd(num: int) -> bool:
        """
        Check if number is odd using bit operation.
        
        Args:
            num: Integer to check
            
        Returns:
            True if odd, False if even
        """
        return (num & 1) == 1
    
    @staticmethod
    def swap_numbers(a: int, b: int) -> tuple[int, int]:
        """
        Swap two numbers using XOR without temporary variable.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Tuple of (b, a) - swapped values
        """
        a = a ^ b
        b = a ^ b
        a = a ^ b
        return a, b
    
    @staticmethod
    def absolute_value(num: int) -> int:
        """
        Get absolute value without branching.
        
        Args:
            num: Integer to get absolute value of
            
        Returns:
            Absolute value
        """
        mask = num >> (num.bit_length() - 1) if num != 0 else 0
        return (num + mask) ^ mask
    
    @staticmethod
    def find_single_number(nums: List[int]) -> int:
        """
        Find the number that appears only once (others appear twice).
        
        Args:
            nums: List of integers where all but one appear twice
            
        Returns:
            The single number
        """
        result = 0
        for num in nums:
            result ^= num
        return result
    
    @staticmethod
    def find_single_number_triple(nums: List[int]) -> int:
        """
        Find the number that appears only once (others appear three times).
        
        Args:
            nums: List of integers where all but one appear three times
            
        Returns:
            The single number
        """
        ones = 0
        twos = 0
        
        for num in nums:
            twos |= ones & num
            ones ^= num
            common_mask = ~(ones & twos)
            ones &= common_mask
            twos &= common_mask
        
        return ones
    
    @staticmethod
    def reverse_bits(num: int, bits: int = 32) -> int:
        """
        Reverse bits of a number.
        
        Args:
            num: Integer to reverse bits of
            bits: Number of bits to consider
            
        Returns:
            Integer with reversed bits
        """
        result = 0
        for _ in range(bits):
            result = (result << 1) | (num & 1)
            num >>= 1
        return result
    
    @staticmethod
    def is_palindrome(num: int) -> bool:
        """
        Check if binary representation is a palindrome.
        
        Args:
            num: Integer to check
            
        Returns:
            True if binary palindrome, False otherwise
        """
        if num < 0:
            return False
        
        original = num
        reversed_num = 0
        
        while num > 0:
            reversed_num = (reversed_num << 1) | (num & 1)
            num >>= 1
        
        return original == reversed_num
    
    @staticmethod
    def add_without_operator(a: int, b: int) -> int:
        """
        Add two numbers without using + operator.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
        """
        while b != 0:
            carry = a & b
            a = a ^ b
            b = carry << 1
        return a
    
    @staticmethod
    def multiply_without_operator(a: int, b: int) -> int:
        """
        Multiply two numbers without using * operator.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a and b
        """
        result = 0
        while b > 0:
            if b & 1:
                result = BitUtils.add_without_operator(result, a)
            a <<= 1
            b >>= 1
        return result
    
    @staticmethod
    def divide_without_operator(dividend: int, divisor: int) -> int:
        """
        Divide two numbers without using / operator.
        
        Args:
            dividend: Number to divide
            divisor: Number to divide by
            
        Returns:
            Quotient (integer division)
        """
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        
        sign = -1 if (dividend < 0) ^ (divisor < 0) else 1
        dividend = abs(dividend)
        divisor = abs(divisor)
        
        quotient = 0
        temp = 0
        
        for i in range(dividend.bit_length() - 1, -1, -1):
            if temp + (divisor << i) <= dividend:
                temp += divisor << i
                quotient |= 1 << i
        
        return sign * quotient
    
    @staticmethod
    def next_power_of_two(num: int) -> int:
        """
        Find next power of two greater than or equal to num.
        
        Args:
            num: Integer to find next power of two for
            
        Returns:
            Next power of two
        """
        if num <= 1:
            return 1
        
        num -= 1
        num |= num >> 1
        num |= num >> 2
        num |= num >> 4
        num |= num >> 8
        num |= num >> 16
        num |= num >> 32
        return num + 1
    
    @staticmethod
    def to_binary_string(num: int, bits: int = 32) -> str:
        """
        Convert integer to binary string representation.
        
        Args:
            num: Integer to convert
            bits: Number of bits to show
            
        Returns:
            Binary string
        """
        return format(num & ((1 << bits) - 1), f'0{bits}b')


def main() -> None:
    """Demonstrate bit manipulation operations."""
    
    utils = BitUtils()
    
    print("=== Basic Bit Operations ===")
    num = 13  # Binary: 1101
    print(f"Number: {num} ({utils.to_binary_string(num, 8)})")
    print(f"Get bit at position 2: {utils.get_bit(num, 2)}")
    print(f"Set bit at position 1: {utils.set_bit(num, 1)} ({utils.to_binary_string(utils.set_bit(num, 1), 8)})")
    print(f"Clear bit at position 3: {utils.clear_bit(num, 3)} ({utils.to_binary_string(utils.clear_bit(num, 3), 8)})")
    print(f"Toggle bit at position 0: {utils.toggle_bit(num, 0)} ({utils.to_binary_string(utils.toggle_bit(num, 0), 8)})")
    
    print("\n=== Number Properties ===")
    numbers = [1, 2, 3, 4, 5, 8, 16, 17]
    for n in numbers:
        print(f"{n:2d}: Power of 2: {utils.is_power_of_two(n):5s}, Even: {utils.is_even(n):5s}, Odd: {utils.is_odd(n):5s}")
    
    print("\n=== Count Set Bits ===")
    test_nums = [5, 7, 15, 31, 32]
    for n in test_nums:
        print(f"{n} ({utils.to_binary_string(n, 8)}): {utils.count_set_bits(n)} set bits (optimized: {utils.count_set_bits_optimized(n)})")
    
    print("\n=== Bit Tricks ===")
    a, b = 5, 10
    print(f"Before swap: a={a}, b={b}")
    a, b = utils.swap_numbers(a, b)
    print(f"After swap: a={a}, b={b}")
    
    print(f"\nAbsolute of -5: {utils.absolute_value(-5)}")
    print(f"Absolute of 5: {utils.absolute_value(5)}")
    
    print("\n=== Find Single Number ===")
    nums1 = [1, 2, 3, 2, 1]
    print(f"Array: {nums1}")
    print(f"Single (appears once): {utils.find_single_number(nums1)}")
    
    nums2 = [1, 1, 1, 2, 2, 2, 3]
    print(f"Array: {nums2}")
    print(f"Single (appears once, others thrice): {utils.find_single_number_triple(nums2)}")
    
    print("\n=== Reverse Bits ===")
    num = 0b1101
    print(f"Original: {utils.to_binary_string(num, 8)}")
    print(f"Reversed: {utils.to_binary_string(utils.reverse_bits(num, 8), 8)}")
    
    print("\n=== Binary Palindrome ===")
    test_nums = [5, 9, 10]
    for n in test_nums:
        print(f"{n} ({utils.to_binary_string(n, 8)}): Palindrome: {utils.is_palindrome(n)}")
    
    print("\n=== Arithmetic Without Operators ===")
    a, b = 7, 5
    print(f"{a} + {b} = {utils.add_without_operator(a, b)}")
    print(f"{a} * {b} = {utils.multiply_without_operator(a, b)}")
    print(f"{a} / {b} = {utils.divide_without_operator(a, b)}")
    
    print("\n=== Next Power of Two ===")
    for n in range(1, 20):
        print(f"{n:2d} -> {utils.next_power_of_two(n)}")


if __name__ == "__main__":
    main()
