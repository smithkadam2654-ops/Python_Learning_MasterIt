"""
Math Utilities Module

This module provides comprehensive mathematical and scientific computing utilities including:
- Basic arithmetic operations
- Advanced mathematical functions
- Statistical calculations
- Linear algebra operations
- Geometry calculations
- Number theory utilities
- Probability and statistics
- Matrix operations
- Coordinate transformations
- Unit conversions

All functions include comprehensive docstrings and type hints.
"""

import math
import random
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import cmath


class RoundingMode(Enum):
    """Rounding modes for numerical operations."""
    ROUND = "round"
    FLOOR = "floor"
    CEIL = "ceil"
    TRUNCATE = "truncate"


@dataclass
class Point2D:
    """2D point representation."""
    x: float
    y: float
    
    def distance_to(self, other: 'Point2D') -> float:
        """Calculate distance to another point."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __add__(self, other: 'Point2D') -> 'Point2D':
        """Add two points."""
        return Point2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point2D') -> 'Point2D':
        """Subtract two points."""
        return Point2D(self.x - other.x, self.y - other.y)


@dataclass
class Point3D:
    """3D point representation."""
    x: float
    y: float
    z: float
    
    def distance_to(self, other: 'Point3D') -> float:
        """Calculate distance to another point."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)


@dataclass
class StatisticsResult:
    """Container for statistical results."""
    mean: float
    median: float
    mode: float
    std_dev: float
    variance: float
    min: float
    max: float
    range: float
    sum: float
    count: int
    quartiles: Tuple[float, float, float]


class BasicMath:
    """Basic mathematical operations."""
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtract two numbers."""
        return a - b
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    @staticmethod
    def power(base: float, exponent: float) -> float:
        """Calculate base raised to exponent."""
        return base ** exponent
    
    @staticmethod
    def square_root(n: float) -> float:
        """Calculate square root."""
        if n < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(n)
    
    @staticmethod
    def absolute_value(n: float) -> float:
        """Calculate absolute value."""
        return abs(n)
    
    @staticmethod
    def round_number(n: float, decimals: int = 0, 
                    mode: RoundingMode = RoundingMode.ROUND) -> float:
        """Round number with specified mode."""
        if mode == RoundingMode.ROUND:
            return round(n, decimals)
        elif mode == RoundingMode.FLOOR:
            return math.floor(n * (10 ** decimals)) / (10 ** decimals)
        elif mode == RoundingMode.CEIL:
            return math.ceil(n * (10 ** decimals)) / (10 ** decimals)
        elif mode == RoundingMode.TRUNCATE:
            return int(n * (10 ** decimals)) / (10 ** decimals)
        else:
            return round(n, decimals)


class AdvancedMath:
    """Advanced mathematical functions."""
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate factorial of n."""
        if n < 0:
            raise ValueError("Factorial of negative number")
        if n == 0 or n == 1:
            return 1
        return math.factorial(n)
    
    @staticmethod
    def fibonacci(n: int) -> int:
        """Calculate nth Fibonacci number."""
        if n < 0:
            raise ValueError("Fibonacci of negative number")
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculate greatest common divisor."""
        return math.gcd(a, b)
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Calculate least common multiple."""
        return abs(a * b) // math.gcd(a, b)
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if number is prime."""
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
    def prime_factors(n: int) -> List[int]:
        """Get prime factors of a number."""
        factors = []
        
        # Handle 2 separately
        while n % 2 == 0:
            factors.append(2)
            n = n // 2
        
        # Check odd factors
        i = 3
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n = n // i
            i += 2
        
        if n > 1:
            factors.append(n)
        
        return factors
    
    @staticmethod
    def logarithm(n: float, base: float = math.e) -> float:
        """Calculate logarithm with specified base."""
        if n <= 0:
            raise ValueError("Logarithm of non-positive number")
        if base <= 0 or base == 1:
            raise ValueError("Invalid logarithm base")
        
        return math.log(n, base)
    
    @staticmethod
    def natural_log(n: float) -> float:
        """Calculate natural logarithm."""
        if n <= 0:
            raise ValueError("Natural log of non-positive number")
        return math.log(n)
    
    @staticmethod
    def degrees_to_radians(degrees: float) -> float:
        """Convert degrees to radians."""
        return math.radians(degrees)
    
    @staticmethod
    def radians_to_degrees(radians: float) -> float:
        """Convert radians to degrees."""
        return math.degrees(radians)
    
    @staticmethod
    def sin(angle: float, degrees: bool = False) -> float:
        """Calculate sine of angle."""
        if degrees:
            angle = math.radians(angle)
        return math.sin(angle)
    
    @staticmethod
    def cos(angle: float, degrees: bool = False) -> float:
        """Calculate cosine of angle."""
        if degrees:
            angle = math.radians(angle)
        return math.cos(angle)
    
    @staticmethod
    def tan(angle: float, degrees: bool = False) -> float:
        """Calculate tangent of angle."""
        if degrees:
            angle = math.radians(angle)
        return math.tan(angle)


class Statistics:
    """Statistical calculations."""
    
    @staticmethod
    def mean(data: List[float]) -> float:
        """Calculate arithmetic mean."""
        if not data:
            raise ValueError("Cannot calculate mean of empty list")
        return sum(data) / len(data)
    
    @staticmethod
    def median(data: List[float]) -> float:
        """Calculate median."""
        if not data:
            raise ValueError("Cannot calculate median of empty list")
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        if n % 2 == 0:
            return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            return sorted_data[n//2]
    
    @staticmethod
    def mode(data: List[float]) -> float:
        """Calculate mode."""
        if not data:
            raise ValueError("Cannot calculate mode of empty list")
        
        from collections import Counter
        counts = Counter(data)
        max_count = max(counts.values())
        modes = [value for value, count in counts.items() if count == max_count]
        
        if len(modes) == 1:
            return modes[0]
        else:
            return Statistics.mean(modes)  # Return mean if multiple modes
    
    @staticmethod
    def variance(data: List[float], sample: bool = True) -> float:
        """Calculate variance."""
        if len(data) < 2:
            raise ValueError("Need at least 2 data points for variance")
        
        mean_val = Statistics.mean(data)
        squared_diffs = [(x - mean_val) ** 2 for x in data]
        
        if sample:
            return sum(squared_diffs) / (len(data) - 1)
        else:
            return sum(squared_diffs) / len(data)
    
    @staticmethod
    def std_dev(data: List[float], sample: bool = True) -> float:
        """Calculate standard deviation."""
        return math.sqrt(Statistics.variance(data, sample))
    
    @staticmethod
    def percentile(data: List[float], percentile: float) -> float:
        """Calculate value at given percentile."""
        if not data:
            raise ValueError("Cannot calculate percentile of empty list")
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        index = (percentile / 100) * (n - 1)
        
        lower = int(index)
        upper = lower + 1
        
        if upper >= n:
            return sorted_data[-1]
        
        weight = index - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight
    
    @staticmethod
    def quartiles(data: List[float]) -> Tuple[float, float, float]:
        """Calculate Q1, Q2, Q3 quartiles."""
        q1 = Statistics.percentile(data, 25)
        q2 = Statistics.percentile(data, 50)
        q3 = Statistics.percentile(data, 75)
        return (q1, q2, q3)
    
    @staticmethod
    def range(data: List[float]) -> float:
        """Calculate range (max - min)."""
        if not data:
            raise ValueError("Cannot calculate range of empty list")
        return max(data) - min(data)
    
    @staticmethod
    def iqr(data: List[float]) -> float:
        """Calculate interquartile range."""
        q1, q2, q3 = Statistics.quartiles(data)
        return q3 - q1
    
    @staticmethod
    def z_score(value: float, data: List[float]) -> float:
        """Calculate z-score for a value."""
        mean_val = Statistics.mean(data)
        std = Statistics.std_dev(data)
        
        if std == 0:
            return 0.0
        
        return (value - mean_val) / std
    
    @staticmethod
    def correlation(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y) or len(x) < 2:
            raise ValueError("Lists must have same length and at least 2 elements")
        
        n = len(x)
        mean_x = Statistics.mean(x)
        mean_y = Statistics.mean(y)
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * \
                     math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    @staticmethod
    def full_statistics(data: List[float]) -> StatisticsResult:
        """Calculate comprehensive statistics."""
        if not data:
            raise ValueError("Cannot calculate statistics of empty list")
        
        sorted_data = sorted(data)
        
        return StatisticsResult(
            mean=Statistics.mean(data),
            median=Statistics.median(data),
            mode=Statistics.mode(data),
            std_dev=Statistics.std_dev(data),
            variance=Statistics.variance(data),
            min=min(data),
            max=max(data),
            range=Statistics.range(data),
            sum=sum(data),
            count=len(data),
            quartiles=Statistics.quartiles(data)
        )


class Geometry:
    """Geometric calculations."""
    
    @staticmethod
    def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate distance between two 2D points."""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    @staticmethod
    def distance_3d(x1: float, y1: float, z1: float,
                   x2: float, y2: float, z2: float) -> float:
        """Calculate distance between two 3D points."""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    
    @staticmethod
    def midpoint_2d(x1: float, y1: float, x2: float, y2: float) -> Point2D:
        """Calculate midpoint between two 2D points."""
        return Point2D((x1 + x2) / 2, (y1 + y2) / 2)
    
    @staticmethod
    def circle_area(radius: float) -> float:
        """Calculate area of a circle."""
        return math.pi * radius ** 2
    
    @staticmethod
    def circle_circumference(radius: float) -> float:
        """Calculate circumference of a circle."""
        return 2 * math.pi * radius
    
    @staticmethod
    def rectangle_area(width: float, height: float) -> float:
        """Calculate area of a rectangle."""
        return width * height
    
    @staticmethod
    def rectangle_perimeter(width: float, height: float) -> float:
        """Calculate perimeter of a rectangle."""
        return 2 * (width + height)
    
    @staticmethod
    def triangle_area(base: float, height: float) -> float:
        """Calculate area of a triangle."""
        return 0.5 * base * height
    
    @staticmethod
    def triangle_perimeter(a: float, b: float, c: float) -> float:
        """Calculate perimeter of a triangle."""
        return a + b + c
    
    @staticmethod
    def sphere_volume(radius: float) -> float:
        """Calculate volume of a sphere."""
        return (4/3) * math.pi * radius ** 3
    
    @staticmethod
    def sphere_surface_area(radius: float) -> float:
        """Calculate surface area of a sphere."""
        return 4 * math.pi * radius ** 2
    
    @staticmethod
    def cube_volume(side: float) -> float:
        """Calculate volume of a cube."""
        return side ** 3
    
    @staticmethod
    def cube_surface_area(side: float) -> float:
        """Calculate surface area of a cube."""
        return 6 * side ** 2
    
    @staticmethod
    def cylinder_volume(radius: float, height: float) -> float:
        """Calculate volume of a cylinder."""
        return math.pi * radius ** 2 * height
    
    @staticmethod
    def cylinder_surface_area(radius: float, height: float) -> float:
        """Calculate surface area of a cylinder."""
        return 2 * math.pi * radius * (radius + height)
    
    @staticmethod
    def pythagorean_theorem(a: float, b: float) -> float:
        """Calculate hypotenuse using Pythagorean theorem."""
        return math.sqrt(a**2 + b**2)
    
    @staticmethod
    def slope(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate slope of line between two points."""
        if x2 == x1:
            raise ValueError("Vertical line has undefined slope")
        return (y2 - y1) / (x2 - x1)
    
    @staticmethod
    def angle_between_points(x1: float, y1: float, 
                            x2: float, y2: float, 
                            x3: float, y3: float) -> float:
        """Calculate angle between three points (in degrees)."""
        # Vectors from point 2 to points 1 and 3
        v1 = (x1 - x2, y1 - y2)
        v2 = (x3 - x2, y3 - y2)
        
        # Dot product
        dot = v1[0] * v2[0] + v1[1] * v2[1]
        
        # Magnitudes
        mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
        mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        # Calculate angle
        cos_angle = dot / (mag1 * mag2)
        cos_angle = max(-1, min(1, cos_angle))  # Clamp to [-1, 1]
        
        return math.degrees(math.acos(cos_angle))


class MatrixOperations:
    """Matrix operations."""
    
    @staticmethod
    def create_matrix(rows: int, cols: int, 
                     fill_value: float = 0.0) -> List[List[float]]:
        """Create a matrix with specified dimensions."""
        return [[fill_value for _ in range(cols)] for _ in range(rows)]
    
    @staticmethod
    def add_matrices(a: List[List[float]], 
                   b: List[List[float]]) -> List[List[float]]:
        """Add two matrices."""
        if len(a) != len(b) or len(a[0]) != len(b[0]):
            raise ValueError("Matrices must have same dimensions")
        
        result = MatrixOperations.create_matrix(len(a), len(a[0]))
        
        for i in range(len(a)):
            for j in range(len(a[0])):
                result[i][j] = a[i][j] + b[i][j]
        
        return result
    
    @staticmethod
    def subtract_matrices(a: List[List[float]], 
                        b: List[List[float]]) -> List[List[float]]:
        """Subtract two matrices."""
        if len(a) != len(b) or len(a[0]) != len(b[0]):
            raise ValueError("Matrices must have same dimensions")
        
        result = MatrixOperations.create_matrix(len(a), len(a[0]))
        
        for i in range(len(a)):
            for j in range(len(a[0])):
                result[i][j] = a[i][j] - b[i][j]
        
        return result
    
    @staticmethod
    def multiply_matrices(a: List[List[float]], 
                        b: List[List[float]]) -> List[List[float]]:
        """Multiply two matrices."""
        if len(a[0]) != len(b):
            raise ValueError("Number of columns in first matrix must equal rows in second")
        
        result = MatrixOperations.create_matrix(len(a), len(b[0]))
        
        for i in range(len(a)):
            for j in range(len(b[0])):
                for k in range(len(b)):
                    result[i][j] += a[i][k] * b[k][j]
        
        return result
    
    @staticmethod
    def transpose_matrix(matrix: List[List[float]]) -> List[List[float]]:
        """Transpose a matrix."""
        if not matrix:
            return []
        
        return [[matrix[j][i] for j in range(len(matrix))] 
                for i in range(len(matrix[0]))]
    
    @staticmethod
    def scalar_multiply(matrix: List[List[float]], 
                       scalar: float) -> List[List[float]]:
        """Multiply matrix by scalar."""
        result = MatrixOperations.create_matrix(len(matrix), len(matrix[0]))
        
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                result[i][j] = matrix[i][j] * scalar
        
        return result
    
    @staticmethod
    def determinant_2x2(matrix: List[List[float]]) -> float:
        """Calculate determinant of 2x2 matrix."""
        if len(matrix) != 2 or len(matrix[0]) != 2:
            raise ValueError("Matrix must be 2x2")
        
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    @staticmethod
    def determinant_3x3(matrix: List[List[float]]) -> float:
        """Calculate determinant of 3x3 matrix."""
        if len(matrix) != 3 or len(matrix[0]) != 3:
            raise ValueError("Matrix must be 3x3")
        
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        
        return (a * (e * i - f * h) - 
                b * (d * i - f * g) + 
                c * (d * h - e * g))


class Probability:
    """Probability calculations."""
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate factorial."""
        return AdvancedMath.factorial(n)
    
    @staticmethod
    def permutation(n: int, r: int) -> int:
        """Calculate permutation nPr."""
        if r > n:
            raise ValueError("r cannot be greater than n")
        return AdvancedMath.factorial(n) // AdvancedMath.factorial(n - r)
    
    @staticmethod
    def combination(n: int, r: int) -> int:
        """Calculate combination nCr."""
        if r > n:
            raise ValueError("r cannot be greater than n")
        return AdvancedMath.factorial(n) // (AdvancedMath.factorial(r) * AdvancedMath.factorial(n - r))
    
    @staticmethod
    def binomial_probability(n: int, k: int, p: float) -> float:
        """Calculate binomial probability."""
        if not (0 <= p <= 1):
            raise ValueError("Probability must be between 0 and 1")
        
        comb = Probability.combination(n, k)
        return comb * (p ** k) * ((1 - p) ** (n - k))
    
    @staticmethod
    def expected_value(values: List[float], 
                      probabilities: List[float]) -> float:
        """Calculate expected value."""
        if len(values) != len(probabilities):
            raise ValueError("Values and probabilities must have same length")
        
        if not math.isclose(sum(probabilities), 1.0, rel_tol=1e-9):
            raise ValueError("Probabilities must sum to 1")
        
        return sum(v * p for v, p in zip(values, probabilities))
    
    @staticmethod
    def variance(values: List[float], 
                probabilities: List[float]) -> float:
        """Calculate variance."""
        if len(values) != len(probabilities):
            raise ValueError("Values and probabilities must have same length")
        
        expected = Probability.expected_value(values, probabilities)
        return sum(p * (v - expected) ** 2 for v, p in zip(values, probabilities))
    
    @staticmethod
    def standard_deviation(values: List[float], 
                         probabilities: List[float]) -> float:
        """Calculate standard deviation."""
        return math.sqrt(Probability.variance(values, probabilities))


class UnitConverter:
    """Unit conversion utilities."""
    
    # Length conversions
    @staticmethod
    def meters_to_feet(meters: float) -> float:
        """Convert meters to feet."""
        return meters * 3.28084
    
    @staticmethod
    def feet_to_meters(feet: float) -> float:
        """Convert feet to meters."""
        return feet / 3.28084
    
    @staticmethod
    def kilometers_to_miles(km: float) -> float:
        """Convert kilometers to miles."""
        return km * 0.621371
    
    @staticmethod
    def miles_to_kilometers(miles: float) -> float:
        """Convert miles to kilometers."""
        return miles / 0.621371
    
    # Temperature conversions
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius."""
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        """Convert Celsius to Kelvin."""
        return celsius + 273.15
    
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """Convert Kelvin to Celsius."""
        return kelvin - 273.15
    
    # Weight conversions
    @staticmethod
    def kilograms_to_pounds(kg: float) -> float:
        """Convert kilograms to pounds."""
        return kg * 2.20462
    
    @staticmethod
    def pounds_to_kilograms(lbs: float) -> float:
        """Convert pounds to kilograms."""
        return lbs / 2.20462
    
    # Volume conversions
    @staticmethod
    def liters_to_gallons(liters: float) -> float:
        """Convert liters to gallons."""
        return liters * 0.264172
    
    @staticmethod
    def gallons_to_liters(gallons: float) -> float:
        """Convert gallons to liters."""
        return gallons / 0.264172
    
    # Area conversions
    @staticmethod
    def square_meters_to_square_feet(sq_meters: float) -> float:
        """Convert square meters to square feet."""
        return sq_meters * 10.7639
    
    @staticmethod
    def square_feet_to_square_meters(sq_feet: float) -> float:
        """Convert square feet to square meters."""
        return sq_feet / 10.7639
    
    # Time conversions
    @staticmethod
    def hours_to_minutes(hours: float) -> float:
        """Convert hours to minutes."""
        return hours * 60
    
    @staticmethod
    def minutes_to_seconds(minutes: float) -> float:
        """Convert minutes to seconds."""
        return minutes * 60
    
    @staticmethod
    def days_to_hours(days: float) -> float:
        """Convert days to hours."""
        return days * 24
    
    # Speed conversions
    @staticmethod
    def kmh_to_mph(kmh: float) -> float:
        """Convert km/h to mph."""
        return kmh * 0.621371
    
    @staticmethod
    def mph_to_kmh(mph: float) -> float:
        """Convert mph to km/h."""
        return mph / 0.621371


class NumberGenerator:
    """Random number generation utilities."""
    
    @staticmethod
    def random_int(min_val: int, max_val: int) -> int:
        """Generate random integer between min and max (inclusive)."""
        return random.randint(min_val, max_val)
    
    @staticmethod
    def random_float(min_val: float, max_val: float) -> float:
        """Generate random float between min and max."""
        return random.uniform(min_val, max_val)
    
    @staticmethod
    def random_choice(choices: List[Any]) -> Any:
        """Choose random element from list."""
        return random.choice(choices)
    
    @staticmethod
    def random_choices(choices: List[Any], k: int) -> List[Any]:
        """Choose k random elements from list (with replacement)."""
        return random.choices(choices, k=k)
    
    @staticmethod
    def random_sample(choices: List[Any], k: int) -> List[Any]:
        """Choose k random elements from list (without replacement)."""
        return random.sample(choices, k)
    
    @staticmethod
    def random_string(length: int, 
                     include_uppercase: bool = True,
                     include_lowercase: bool = True,
                     include_digits: bool = True,
                     include_special: bool = False) -> str:
        """Generate random string."""
        import string
        chars = ""
        
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_digits:
            chars += string.digits
        if include_special:
            chars += "!@#$%^&*"
        
        if not chars:
            chars = string.ascii_lowercase
        
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def normal_distribution(mean: float, std_dev: float) -> float:
        """Generate random number from normal distribution."""
        return random.gauss(mean, std_dev)
    
    @staticmethod
    def exponential_distribution(lambda_param: float) -> float:
        """Generate random number from exponential distribution."""
        return random.expovariate(lambda_param)


def demonstrate_math_utils():
    """Demonstrate math utilities functionality."""
    print("=== Math Utilities Demonstration ===\n")
    
    # Basic Math
    print("1. Basic Math:")
    print(f"   Addition: {BasicMath.add(5, 3)}")
    print(f"   Division: {BasicMath.divide(10, 2)}")
    print(f"   Power: {BasicMath.power(2, 3)}")
    print(f"   Square root: {BasicMath.square_root(16)}")
    print(f"   Absolute: {BasicMath.absolute_value(-5)}")
    
    # Advanced Math
    print("\n2. Advanced Math:")
    print(f"   Factorial(5): {AdvancedMath.factorial(5)}")
    print(f"   Fibonacci(10): {AdvancedMath.fibonacci(10)}")
    print(f"   GCD(12, 18): {AdvancedMath.gcd(12, 18)}")
    print(f"   LCM(12, 18): {AdvancedMath.lcm(12, 18)}")
    print(f"   Is prime(17): {AdvancedMath.is_prime(17)}")
    print(f"   Prime factors(12): {AdvancedMath.prime_factors(12)}")
    print(f"   Log(100, 10): {AdvancedMath.logarithm(100, 10)}")
    print(f"   Sin(90°): {AdvancedMath.sin(90, degrees=True)}")
    
    # Statistics
    print("\n3. Statistics:")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"   Data: {data}")
    print(f"   Mean: {Statistics.mean(data)}")
    print(f"   Median: {Statistics.median(data)}")
    print(f"   Std dev: {Statistics.std_dev(data):.2f}")
    print(f"   75th percentile: {Statistics.percentile(data, 75)}")
    print(f"   Correlation: {Statistics.correlation(data, [x*2 for x in data])}")
    
    # Full Statistics
    print("\n4. Full Statistics:")
    stats = Statistics.full_statistics(data)
    print(f"   Mean: {stats.mean}")
    print(f"   Median: {stats.median}")
    print(f"   Range: {stats.range}")
    print(f"   Quartiles: {stats.quartiles}")
    
    # Geometry
    print("\n5. Geometry:")
    print(f"   Circle area (r=5): {Geometry.circle_area(5):.2f}")
    print(f"   Rectangle area (3x4): {Geometry.rectangle_area(3, 4)}")
    print(f"   Triangle area (b=6, h=4): {Geometry.triangle_area(6, 4)}")
    print(f"   Sphere volume (r=3): {Geometry.sphere_volume(3):.2f}")
    print(f"   Distance 2D: {Geometry.distance_2d(0, 0, 3, 4)}")
    print(f"   Pythagorean: {Geometry.pythagorean_theorem(3, 4)}")
    
    # Matrix Operations
    print("\n6. Matrix Operations:")
    matrix_a = [[1, 2], [3, 4]]
    matrix_b = [[5, 6], [7, 8]]
    print(f"   Matrix A: {matrix_a}")
    print(f"   Matrix B: {matrix_b}")
    print(f"   Addition: {MatrixOperations.add_matrices(matrix_a, matrix_b)}")
    print(f"   Determinant 2x2: {MatrixOperations.determinant_2x2(matrix_a)}")
    
    # Probability
    print("\n7. Probability:")
    print(f"   Permutation(5, 3): {Probability.permutation(5, 3)}")
    print(f"   Combination(5, 3): {Probability.combination(5, 3)}")
    print(f"   Binomial P(5, 2, 0.5): {Probability.binomial_probability(5, 2, 0.5):.4f}")
    
    # Unit Conversions
    print("\n8. Unit Conversions:")
    print(f"   100m to feet: {UnitConverter.meters_to_feet(100):.2f}")
    print(f"   25°C to °F: {UnitConverter.celsius_to_fahrenheit(25):.1f}")
    print(f"   10km to miles: {UnitConverter.kilometers_to_miles(10):.2f}")
    print(f"   70kg to lbs: {UnitConverter.kilograms_to_pounds(70):.2f}")
    
    # Random Generation
    print("\n9. Random Generation:")
    print(f"   Random int (1-10): {NumberGenerator.random_int(1, 10)}")
    print(f"   Random float (0-1): {NumberGenerator.random_float(0, 1):.4f}")
    print(f"   Random string: {NumberGenerator.random_string(8)}")
    print(f"   Normal distribution: {NumberGenerator.normal_distribution(0, 1):.4f}")
    
    # 2D Points
    print("\n10. 2D Points:")
    point1 = Point2D(0, 0)
    point2 = Point2D(3, 4)
    print(f"   Point 1: ({point1.x}, {point1.y})")
    print(f"   Point 2: ({point2.x}, {point2.y})")
    print(f"   Distance: {point1.distance_to(point2)}")
    print(f"   Addition: {point1 + point2}")
    
    print("\n=== Demonstration Complete ===")


if __name__ == "__main__":
    demonstrate_math_utils()