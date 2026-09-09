"""
Bit Manipulation Operations - Common bit manipulation techniques.
Features: Bit tricks, parity checks, and bit manipulation utilities.
"""

from typing import List


class BitOperations:
    """Common bit manipulation operations."""
    
    @staticmethod
    def get_bit(n: int, i: int) -> int:
        """
        Get i-th bit of n (0-indexed from right).
        
        Args:
            n: Number
            i: Bit position
            
        Returns:
            Bit value (0 or 1)
        """
        return (n >> i) & 1
    
    @staticmethod
    def set_bit(n: int, i: int) -> int:
        """
        Set i-th bit of n to 1.
        
        Args:
            n: Number
            i: Bit position
            
        Returns:
            Number with bit set
        """
        return n | (1 << i)
    
    @staticmethod
    def clear_bit(n: int, i: int) -> int:
        """
        Clear i-th bit of n (set to 0).
        
        Args:
            n: Number
            i: Bit position
            
        Returns:
            Number with bit cleared
        """
        return n & ~(1 << i)
    
    @staticmethod
    def toggle_bit(n: int, i: int) -> int:
        """
        Toggle i-th bit of n.
        
        Args:
            n: Number
            i: Bit position
            
        Returns:
            Number with bit toggled
        """
        return n ^ (1 << i)
    
    @staticmethod
    def is_power_of_two(n: int) -> bool:
        """
        Check if n is a power of two.
        
        Args:
            n: Number
            
        Returns:
            True if power of two
        """
        return n > 0 and (n & (n - 1)) == 0
    
    @staticmethod
    def count_set_bits(n: int) -> int:
        """
        Count number of set bits (Brian Kernighan's algorithm).
        
        Args:
            n: Number
            
        Returns:
            Count of set bits
        """
        count = 0
        while n:
            n &= n - 1
            count += 1
        return count
    
    @staticmethod
    def count_set_bits_builtin(n: int) -> int:
        """
        Count set bits using built-in function.
        
        Args:
            n: Number
            
        Returns:
            Count of set bits
        """
        return bin(n).count('1')
    
    @staticmethod
    def is_even(n: int) -> bool:
        """
        Check if n is even using bitwise operation.
        
        Args:
            n: Number
            
        Returns:
            True if even
        """
        return (n & 1) == 0
    
    @staticmethod
    def is_odd(n: int) -> bool:
        """
        Check if n is odd using bitwise operation.
        
        Args:
            n: Number
            
        Returns:
            True if odd
        """
        return (n & 1) == 1
    
    @staticmethod
    def swap_numbers(a: int, b: int) -> tuple:
        """
        Swap two numbers using XOR (without temporary variable).
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Tuple of (swapped_a, swapped_b)
        """
        a = a ^ b
        b = a ^ b
        a = a ^ b
        return (a, b)
    
    @staticmethod
    def absolute_value(n: int) -> int:
        """
        Get absolute value without branching.
        
        Args:
            n: Number
            
        Returns:
            Absolute value
        """
        mask = n >> (n.bit_length() - 1) if n != 0 else 0
        return (n + mask) ^ mask
    
    @staticmethod
    def max_of_two(a: int, b: int) -> int:
        """
        Get maximum of two numbers without comparison.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Maximum value
        """
        return a - ((a - b) & ((a - b) >> (a - b).bit_length() - 1))
    
    @staticmethod
    def min_of_two(a: int, b: int) -> int:
        """
        Get minimum of two numbers without comparison.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Minimum value
        """
        return b - ((a - b) & ((a - b) >> (a - b).bit_length() - 1))
    
    @staticmethod
    def multiply_by_two(n: int) -> int:
        """
        Multiply by 2 using left shift.
        
        Args:
            n: Number
            
        Returns:
            n * 2
        """
        return n << 1
    
    @staticmethod
    def divide_by_two(n: int) -> int:
        """
        Divide by 2 using right shift.
        
        Args:
            n: Number
            
        Returns:
            n // 2
        """
        return n >> 1
    
    @staticmethod
    def is_power_of_four(n: int) -> bool:
        """
        Check if n is a power of four.
        
        Args:
            n: Number
            
        Returns:
            True if power of four
        """
        return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0
    
    @staticmethod
    def reverse_bits(n: int) -> int:
        """
        Reverse bits of a 32-bit unsigned integer.
        
        Args:
            n: Number
            
        Returns:
            Number with reversed bits
        """
        result = 0
        for _ in range(32):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result
    
    @staticmethod
    def find_single_number(nums: List[int]) -> int:
        """
        Find the single number in array where every other appears twice.
        
        Args:
            nums: List of numbers
            
        Returns:
            Single number
        """
        result = 0
        for num in nums:
            result ^= num
        return result
    
    @staticmethod
    def find_single_number_triple(nums: List[int]) -> int:
        """
        Find the single number in array where every other appears three times.
        
        Args:
            nums: List of numbers
            
        Returns:
            Single number
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
    def gray_code(n: int) -> List[int]:
        """
        Generate n-bit Gray code sequence.
        
        Args:
            n: Number of bits
            
        Returns:
            List of Gray code values
        """
        result = []
        for i in range(1 << n):
            result.append(i ^ (i >> 1))
        return result


def main() -> None:
    """Demonstrate bit operations."""
    
    print("=== Bit Operations Demo ===")
    
    n = 13  # Binary: 1101
    
    print(f"Number: {n} (binary: {bin(n)})")
    
    # Get bit
    print(f"\n--- Get Bit ---")
    for i in range(4):
        print(f"Bit {i}: {BitOperations.get_bit(n, i)}")
    
    # Set bit
    print(f"\n--- Set Bit ---")
    print(f"Set bit 1: {BitOperations.set_bit(n, 1)} (binary: {bin(BitOperations.set_bit(n, 1))})")
    
    # Clear bit
    print(f"\n--- Clear Bit ---")
    print(f"Clear bit 3: {BitOperations.clear_bit(n, 3)} (binary: {bin(BitOperations.clear_bit(n, 3))})")
    
    # Toggle bit
    print(f"\n--- Toggle Bit ---")
    print(f"Toggle bit 2: {BitOperations.toggle_bit(n, 2)} (binary: {bin(BitOperations.toggle_bit(n, 2))})")
    
    # Power of two
    print(f"\n--- Power of Two ---")
    for num in [1, 2, 4, 8, 16, 3, 5, 6]:
        print(f"{num}: {BitOperations.is_power_of_two(num)}")
    
    # Count set bits
    print(f"\n--- Count Set Bits ---")
    for num in [5, 7, 15, 16]:
        print(f"{num}: {BitOperations.count_set_bits(num)} (builtin: {BitOperations.count_set_bits_builtin(num)})")
    
    # Even/Odd
    print(f"\n--- Even/Odd ---")
    for num in [1, 2, 3, 4, 5, 6]:
        print(f"{num}: even={BitOperations.is_even(num)}, odd={BitOperations.is_odd(num)}")
    
    # Swap numbers
    print(f"\n--- Swap Numbers ---")
    a, b = 5, 10
    print(f"Before: a={a}, b={b}")
    a, b = BitOperations.swap_numbers(a, b)
    print(f"After: a={a}, b={b}")
    
    # Absolute value
    print(f"\n--- Absolute Value ---")
    for num in [-5, 5, -10, 10]:
        print(f"abs({num}) = {BitOperations.absolute_value(num)}")
    
    # Max/Min
    print(f"\n--- Max/Min ---")
    print(f"max(5, 10) = {BitOperations.max_of_two(5, 10)}")
    print(f"min(5, 10) = {BitOperations.min_of_two(5, 10)}")
    
    # Multiply/Divide by two
    print(f"\n--- Multiply/Divide by Two ---")
    for num in [5, 10, 15]:
        print(f"{num} * 2 = {BitOperations.multiply_by_two(num)}")
        print(f"{num} // 2 = {BitOperations.divide_by_two(num)}")
    
    # Power of four
    print(f"\n--- Power of Four ---")
    for num in [1, 4, 16, 64, 2, 8, 32]:
        print(f"{num}: {BitOperations.is_power_of_four(num)}")
    
    # Reverse bits
    print(f"\n--- Reverse Bits ---")
    for num in [1, 2, 3, 4, 5]:
        print(f"{num} (binary: {bin(num)[2:].zfill(8)}) -> {BitOperations.reverse_bits(num)}")
    
    # Find single number
    print(f"\n--- Find Single Number ---")
    nums = [2, 3, 5, 4, 5, 3, 4]
    print(f"Array: {nums}")
    print(f"Single: {BitOperations.find_single_number(nums)}")
    
    # Find single number (three times)
    print(f"\n--- Find Single Number (Three Times) ---")
    nums_triple = [2, 2, 3, 2]
    print(f"Array: {nums_triple}")
    print(f"Single: {BitOperations.find_single_number_triple(nums_triple)}")
    
    # Gray code
    print(f"\n--- Gray Code ---")
    for n in range(1, 4):
        gray = BitOperations.gray_code(n)
        print(f"{n}-bit Gray code: {gray}")


if __name__ == "__main__":
    main()
