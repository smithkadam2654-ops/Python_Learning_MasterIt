"""
Math Algorithms - Mathematical algorithms and number theory.
Features: Prime numbers, GCD, LCM, modular arithmetic, and numerical methods.
"""

import math
from typing import List, Tuple, Optional


def gcd(a: int, b: int) -> int:
    """
    Calculate Greatest Common Divisor using Euclidean algorithm.
    
    Time Complexity: O(log(min(a,b)))
    Space Complexity: O(1)
    
    Args:
        a: First integer
        b: Second integer
        
    Returns:
        GCD of a and b
    """
    a, b = abs(a), abs(b)
    
    while b:
        a, b = b, a % b
    
    return a


def lcm(a: int, b: int) -> int:
    """
    Calculate Least Common Multiple.
    
    Time Complexity: O(log(min(a,b)))
    Space Complexity: O(1)
    
    Args:
        a: First integer
        b: Second integer
        
    Returns:
        LCM of a and b
    """
    if a == 0 or b == 0:
        return 0
    
    return abs(a * b) // gcd(a, b)


def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    
    Time Complexity: O(sqrt(n))
    Space Complexity: O(1)
    
    Args:
        n: Integer to check
        
    Returns:
        True if prime, False otherwise
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True


def sieve_of_eratosthenes(n: int) -> List[int]:
    """
    Generate all primes up to n using Sieve of Eratosthenes.
    
    Time Complexity: O(n log log n)
    Space Complexity: O(n)
    
    Args:
        n: Upper bound (inclusive)
        
    Returns:
        List of primes up to n
    """
    if n < 2:
        return []
    
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(math.sqrt(n)) + 1):
        if sieve[i]:
            sieve[i*i:n+1:i] = [False] * len(sieve[i*i:n+1:i])
    
    return [i for i, is_prime in enumerate(sieve) if is_prime]


def prime_factors(n: int) -> List[int]:
    """
    Find prime factors of a number.
    
    Time Complexity: O(sqrt(n))
    Space Complexity: O(log n)
    
    Args:
        n: Integer to factorize
        
    Returns:
        List of prime factors
    """
    factors = []
    
    # Handle 2s
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # Handle odd factors
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    
    # If n is still > 1, it's a prime factor
    if n > 1:
        factors.append(n)
    
    return factors


def is_power_of_two(n: int) -> bool:
    """
    Check if number is a power of two.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Args:
        n: Integer to check
        
    Returns:
        True if power of two, False otherwise
    """
    return n > 0 and (n & (n - 1)) == 0


def factorial(n: int) -> int:
    """
    Calculate factorial iteratively.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        n: Non-negative integer
        
    Returns:
        Factorial of n
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


def fibonacci(n: int) -> int:
    """
    Calculate nth Fibonacci number iteratively.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        nth Fibonacci number
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def power(base: float, exponent: int) -> float:
    """
    Calculate base^exponent using fast exponentiation.
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Args:
        base: Base number
        exponent: Non-negative integer
        
    Returns:
        base raised to exponent
    """
    if exponent < 0:
        return 1 / power(base, -exponent)
    
    result = 1.0
    current = base
    
    while exponent > 0:
        if exponent % 2 == 1:
            result *= current
        current *= current
        exponent //= 2
    
    return result


def modular_exponentiation(base: int, exponent: int, modulus: int) -> int:
    """
    Calculate (base^exponent) % modulus efficiently.
    
    Time Complexity: O(log exponent)
    Space Complexity: O(1)
    
    Args:
        base: Base number
        exponent: Non-negative integer
        modulus: Modulus
        
    Returns:
        (base^exponent) % modulus
    """
    if modulus == 1:
        return 0
    
    result = 1
    base = base % modulus
    
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    
    return result


def is_perfect_square(n: int) -> bool:
    """
    Check if number is a perfect square.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Args:
        n: Integer to check
        
    Returns:
        True if perfect square, False otherwise
    """
    if n < 0:
        return False
    
    root = int(math.sqrt(n))
    return root * root == n


def is_perfect_cube(n: int) -> bool:
    """
    Check if number is a perfect cube.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Args:
        n: Integer to check
        
    Returns:
        True if perfect cube, False otherwise
    """
    if n < 0:
        return False
    
    root = round(n ** (1/3))
    return root ** 3 == n


def sum_of_digits(n: int) -> int:
    """
    Calculate sum of digits of a number.
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Args:
        n: Integer
        
    Returns:
        Sum of digits
    """
    n = abs(n)
    total = 0
    
    while n > 0:
        total += n % 10
        n //= 10
    
    return total


def reverse_number(n: int) -> int:
    """
    Reverse digits of a number.
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Args:
        n: Integer
        
    Returns:
        Reversed number
    """
    n = abs(n)
    reversed_num = 0
    
    while n > 0:
        reversed_num = reversed_num * 10 + n % 10
        n //= 10
    
    return reversed_num


def is_armstrong_number(n: int) -> bool:
    """
    Check if number is an Armstrong number (narcissistic number).
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Args:
        n: Integer to check
        
    Returns:
        True if Armstrong number, False otherwise
    """
    if n < 0:
        return False
    
    original = n
    num_digits = len(str(n))
    total = 0
    
    while n > 0:
        digit = n % 10
        total += digit ** num_digits
        n //= 10
    
    return total == original


def is_palindrome_number(n: int) -> bool:
    """
    Check if number is a palindrome.
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Args:
        n: Integer to check
        
    Returns:
        True if palindrome, False otherwise
    """
    if n < 0:
        return False
    
    original = n
    reversed_num = 0
    
    while n > 0:
        reversed_num = reversed_num * 10 + n % 10
        n //= 10
    
    return original == reversed_num


def count_trailing_zeros(n: int) -> int:
    """
    Count trailing zeros in factorial of n.
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Args:
        n: Non-negative integer
        
    Returns:
        Number of trailing zeros in n!
    """
    count = 0
    i = 5
    
    while n // i > 0:
        count += n // i
        i *= 5
    
    return count


def euler_totient(n: int) -> int:
    """
    Calculate Euler's Totient function (count of numbers <= n coprime to n).
    
    Time Complexity: O(sqrt(n))
    Space Complexity: O(1)
    
    Args:
        n: Positive integer
        
    Returns:
        Euler's totient value
    """
    if n <= 0:
        return 0
    
    result = n
    p = 2
    
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    
    if n > 1:
        result -= result // n
    
    return result


def chinese_remainder_theorem(a: int, m: int, b: int, n: int) -> Optional[int]:
    """
    Solve x ≡ a (mod m) and x ≡ b (mod n) using CRT.
    
    Time Complexity: O(log(min(m,n)))
    Space Complexity: O(1)
    
    Args:
        a: First remainder
        m: First modulus
        b: Second remainder
        n: Second modulus
        
    Returns:
        Solution x, or None if no solution exists
    """
    # Check if solution exists
    if (a - b) % gcd(m, n) != 0:
        return None
    
    # Find solution using extended Euclidean algorithm
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if b == 0:
            return (a, 1, 0)
        g, x, y = extended_gcd(b, a % b)
        return (g, y, x - (a // b) * y)
    
    g, p, q = extended_gcd(m, n)
    lcm_mn = m // g * n
    
    x = (a * n * q + b * m * p) % lcm_mn
    
    return x if x >= 0 else x + lcm_mn


def binary_to_decimal(binary: str) -> int:
    """
    Convert binary string to decimal.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Args:
        binary: Binary string
        
    Returns:
        Decimal value
    """
    return int(binary, 2)


def decimal_to_binary(n: int) -> str:
    """
    Convert decimal to binary string.
    
    Time Complexity: O(log n)
    Space Complexity: O(log n)
    
    Args:
        n: Non-negative integer
        
    Returns:
        Binary string
    """
    if n == 0:
        return "0"
    
    binary = []
    
    while n > 0:
        binary.append(str(n % 2))
        n //= 2
    
    return ''.join(reversed(binary))


def main() -> None:
    """Demonstrate mathematical algorithms."""
    
    print("=== GCD and LCM ===")
    print(f"gcd(48, 18): {gcd(48, 18)}")
    print(f"lcm(48, 18): {lcm(48, 18)}")
    
    print("\n=== Prime Numbers ===")
    print(f"is_prime(17): {is_prime(17)}")
    print(f"is_prime(18): {is_prime(18)}")
    print(f"Primes up to 30: {sieve_of_eratosthenes(30)}")
    print(f"Prime factors of 84: {prime_factors(84)}")
    
    print("\n=== Powers and Factorials ===")
    print(f"is_power_of_two(16): {is_power_of_two(16)}")
    print(f"is_power_of_two(18): {is_power_of_two(18)}")
    print(f"factorial(5): {factorial(5)}")
    print(f"fibonacci(10): {fibonacci(10)}")
    print(f"power(2, 10): {power(2, 10)}")
    
    print("\n=== Modular Arithmetic ===")
    print(f"modular_exponentiation(2, 10, 1000): {modular_exponentiation(2, 10, 1000)}")
    
    print("\n=== Number Properties ===")
    print(f"is_perfect_square(16): {is_perfect_square(16)}")
    print(f"is_perfect_square(15): {is_perfect_square(15)}")
    print(f"is_perfect_cube(27): {is_perfect_cube(27)}")
    print(f"sum_of_digits(12345): {sum_of_digits(12345)}")
    print(f"reverse_number(12345): {reverse_number(12345)}")
    
    print("\n=== Special Numbers ===")
    print(f"is_armstrong_number(153): {is_armstrong_number(153)}")
    print(f"is_armstrong_number(154): {is_armstrong_number(154)}")
    print(f"is_palindrome_number(121): {is_palindrome_number(121)}")
    print(f"is_palindrome_number(123): {is_palindrome_number(123)}")
    
    print("\n=== Factorial Trailing Zeros ===")
    for n in [5, 10, 25, 100]:
        print(f"Trailing zeros in {n}!: {count_trailing_zeros(n)}")
    
    print("\n=== Euler's Totient ===")
    for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        print(f"φ({n}): {euler_totient(n)}")
    
    print("\n=== Chinese Remainder Theorem ===")
    result = chinese_remainder_theorem(2, 3, 3, 5)
    print(f"x ≡ 2 (mod 3), x ≡ 3 (mod 5): x = {result}")
    
    print("\n=== Number Base Conversion ===")
    print(f"binary_to_decimal('1010'): {binary_to_decimal('1010')}")
    print(f"decimal_to_binary(10): {decimal_to_binary(10)}")


if __name__ == "__main__":
    main()
