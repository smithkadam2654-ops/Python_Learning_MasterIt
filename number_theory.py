"""
Number Theory Algorithms - Mathematical number operations.
Features: GCD, LCM, prime numbers, modular arithmetic, and factorization.
"""

from typing import List, Tuple
import math


class NumberTheory:
    """Number theory algorithm implementations."""
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Calculate greatest common divisor using Euclidean algorithm.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            GCD of a and b
        """
        while b:
            a, b = b, a % b
        return abs(a)
    
    @staticmethod
    def gcd_extended(a: int, b: int) -> Tuple[int, int, int]:
        """
        Extended Euclidean algorithm (finds x, y such that ax + by = gcd(a,b)).
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Tuple of (gcd, x, y)
        """
        if b == 0:
            return (a, 1, 0)
        
        gcd, x1, y1 = NumberTheory.gcd_extended(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        
        return (gcd, x, y)
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """
        Calculate least common multiple.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            LCM of a and b
        """
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // NumberTheory.gcd(a, b)
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """
        Check if number is prime using trial division.
        
        Args:
            n: Number to check
            
        Returns:
            True if prime
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        
        return True
    
    @staticmethod
    def sieve_of_eratosthenes(n: int) -> List[bool]:
        """
        Generate prime sieve up to n.
        
        Args:
            n: Upper bound
            
        Returns:
            Boolean array where index i is True if i is prime
        """
        if n < 2:
            return [False] * (n + 1)
        
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(math.sqrt(n)) + 1):
            if sieve[i]:
                for j in range(i * i, n + 1, i):
                    sieve[j] = False
        
        return sieve
    
    @staticmethod
    def get_primes(n: int) -> List[int]:
        """
        Get list of primes up to n.
        
        Args:
            n: Upper bound
            
        Returns:
            List of primes
        """
        sieve = NumberTheory.sieve_of_eratosthenes(n)
        return [i for i, is_prime in enumerate(sieve) if is_prime]
    
    @staticmethod
    def prime_factors(n: int) -> List[int]:
        """
        Get prime factors of n.
        
        Args:
            n: Number to factorize
            
        Returns:
            List of prime factors
        """
        factors = []
        
        # Handle 2
        while n % 2 == 0:
            factors.append(2)
            n //= 2
        
        # Handle odd factors
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            while n % i == 0:
                factors.append(i)
                n //= i
        
        # If n is still > 2, it's prime
        if n > 2:
            factors.append(n)
        
        return factors
    
    @staticmethod
    def prime_factors_with_count(n: int) -> dict:
        """
        Get prime factors with their counts.
        
        Args:
            n: Number to factorize
            
        Returns:
            Dictionary of prime factor to count
        """
        factors = NumberTheory.prime_factors(n)
        result = {}
        
        for factor in factors:
            result[factor] = result.get(factor, 0) + 1
        
        return result
    
    @staticmethod
    def modular_exponentiation(base: int, exponent: int, modulus: int) -> int:
        """
        Calculate (base^exponent) % modulus efficiently.
        
        Args:
            base: Base
            exponent: Exponent
            modulus: Modulus
            
        Returns:
            Result of modular exponentiation
        """
        if modulus == 1:
            return 0
        
        result = 1
        base = base % modulus
        
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            
            exponent = exponent >> 1
            base = (base * base) % modulus
        
        return result
    
    @staticmethod
    def modular_inverse(a: int, m: int) -> Optional[int]:
        """
        Find modular inverse of a modulo m (a and m must be coprime).
        
        Args:
            a: Number
            m: Modulus
            
        Returns:
            Modular inverse or None if doesn't exist
        """
        gcd, x, _ = NumberTheory.gcd_extended(a, m)
        
        if gcd != 1:
            return None  # Inverse doesn't exist
        
        return x % m
    
    @staticmethod
    def euler_totient(n: int) -> int:
        """
        Calculate Euler's totient function (count of numbers < n coprime to n).
        
        Args:
            n: Number
            
        Returns:
            Euler's totient
        """
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
    
    @staticmethod
    def is_coprime(a: int, b: int) -> bool:
        """
        Check if two numbers are coprime (gcd = 1).
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            True if coprime
        """
        return NumberTheory.gcd(a, b) == 1
    
    @staticmethod
    def chinese_remainder_theorem(equations: List[Tuple[int, int]]) -> Optional[int]:
        """
        Solve system of congruences using Chinese Remainder Theorem.
        
        Args:
            equations: List of (remainder, modulus) tuples
            
        Returns:
            Solution or None if no solution
        """
        if not equations:
            return None
        
        result = equations[0][0]
        mod_product = equations[0][1]
        
        for remainder, modulus in equations[1:]:
            # Solve: result + mod_product * k ≡ remainder (mod modulus)
            # mod_product * k ≡ remainder - result (mod modulus)
            
            diff = remainder - result
            gcd, x, _ = NumberTheory.gcd_extended(mod_product, modulus)
            
            if diff % gcd != 0:
                return None  # No solution
            
            # Find k
            k = (diff // gcd) * x % (modulus // gcd)
            
            result += mod_product * k
            mod_product = NumberTheory.lcm(mod_product, modulus)
            result %= mod_product
        
        return result
    
    @staticmethod
    def fibonacci(n: int) -> int:
        """
        Calculate nth Fibonacci number using matrix exponentiation.
        
        Args:
            n: Index (0-indexed)
            
        Returns:
            nth Fibonacci number
        """
        if n <= 1:
            return n
        
        def matrix_mult(a, b):
            return [
                [a[0][0] * b[0][0] + a[0][1] * b[1][0],
                 a[0][0] * b[0][1] + a[0][1] * b[1][1]],
                [a[1][0] * b[0][0] + a[1][1] * b[1][0],
                 a[1][0] * b[0][1] + a[1][1] * b[1][1]]
            ]
        
        def matrix_pow(mat, power):
            result = [[1, 0], [0, 1]]  # Identity matrix
            
            while power > 0:
                if power % 2 == 1:
                    result = matrix_mult(result, mat)
                mat = matrix_mult(mat, mat)
                power //= 2
            
            return result
        
        fib_matrix = [[1, 1], [1, 0]]
        result = matrix_pow(fib_matrix, n - 1)
        return result[0][0]
    
    @staticmethod
    def factorial(n: int) -> int:
        """
        Calculate factorial.
        
        Args:
            n: Number
            
        Returns:
            n!
        """
        if n < 0:
            return 0
        if n <= 1:
            return 1
        
        result = 1
        for i in range(2, n + 1):
            result *= i
        
        return result
    
    @staticmethod
    def factorial_mod(n: int, m: int) -> int:
        """
        Calculate factorial modulo m.
        
        Args:
            n: Number
            m: Modulus
            
        Returns:
            n! % m
        """
        if n < 0:
            return 0
        if n <= 1:
            return 1 % m
        
        result = 1
        for i in range(2, n + 1):
            result = (result * i) % m
        
        return result
    
    @staticmethod
    def binomial_coefficient(n: int, k: int) -> int:
        """
        Calculate binomial coefficient C(n, k).
        
        Args:
            n: Total items
            k: Items to choose
            
        Returns:
            C(n, k)
        """
        if k < 0 or k > n:
            return 0
        if k == 0 or k == n:
            return 1
        
        k = min(k, n - k)  # Use symmetry
        
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        
        return result


def main() -> None:
    """Demonstrate number theory algorithms."""
    
    print("=== Number Theory Demo ===")
    
    # GCD and LCM
    print("\n--- GCD and LCM ---")
    a, b = 48, 18
    print(f"GCD({a}, {b}) = {NumberTheory.gcd(a, b)}")
    print(f"LCM({a}, {b}) = {NumberTheory.lcm(a, b)}")
    
    # Extended GCD
    print("\n--- Extended GCD ---")
    a, b = 35, 15
    gcd, x, y = NumberTheory.gcd_extended(a, b)
    print(f"{a}*{x} + {b}*{y} = {gcd}")
    
    # Prime checking
    print("\n--- Prime Checking ---")
    for n in [2, 3, 4, 5, 17, 18, 19]:
        print(f"{n}: {NumberTheory.is_prime(n)}")
    
    # Sieve
    print("\n--- Sieve of Eratosthenes ---")
    n = 30
    primes = NumberTheory.get_primes(n)
    print(f"Primes up to {n}: {primes}")
    
    # Prime factors
    print("\n--- Prime Factorization ---")
    n = 84
    print(f"Prime factors of {n}: {NumberTheory.prime_factors(n)}")
    print(f"With counts: {NumberTheory.prime_factors_with_count(n)}")
    
    # Modular exponentiation
    print("\n--- Modular Exponentiation ---")
    base, exp, mod = 7, 3, 13
    print(f"{base}^{exp} mod {mod} = {NumberTheory.modular_exponentiation(base, exp, mod)}")
    
    # Modular inverse
    print("\n--- Modular Inverse ---")
    a, m = 3, 11
    inv = NumberTheory.modular_inverse(a, m)
    print(f"Inverse of {a} mod {m}: {inv}")
    
    # Euler's totient
    print("\n--- Euler's Totient ---")
    for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        print(f"φ({n}) = {NumberTheory.euler_totient(n)}")
    
    # Coprime check
    print("\n--- Coprime Check ---")
    pairs = [(14, 15), (21, 14)]
    for a, b in pairs:
        print(f"{a}, {b}: {NumberTheory.is_coprime(a, b)}")
    
    # Chinese Remainder Theorem
    print("\n--- Chinese Remainder Theorem ---")
    equations = [(2, 3), (3, 5), (2, 7)]
    result = NumberTheory.chinese_remainder_theorem(equations)
    print(f"Equations: {equations}")
    print(f"Solution: {result}")
    
    # Fibonacci
    print("\n--- Fibonacci ---")
    for n in [0, 1, 5, 10, 20]:
        print(f"F({n}) = {NumberTheory.fibonacci(n)}")
    
    # Factorial
    print("\n--- Factorial ---")
    for n in [0, 1, 5, 10]:
        print(f"{n}! = {NumberTheory.factorial(n)}")
    
    # Binomial coefficient
    print("\n--- Binomial Coefficient ---")
    for n in [5, 10]:
        for k in range(n + 1):
            print(f"C({n}, {k}) = {NumberTheory.binomial_coefficient(n, k)}", end="  ")
        print()


if __name__ == "__main__":
    main()
