"""
Advanced Python - Lesson 09: Functional Programming
=====================================================
Functional programming treats computation as the evaluation of
mathematical functions, avoiding state and mutable data.

Topics Covered:
- Lambda functions
- map, filter, reduce
- Higher-order functions
- Closures
- Partial functions (functools.partial)
- Composing functions
- Currying
- Immutability patterns
"""

from functools import reduce, partial
from typing import Callable, TypeVar, Any
import operator

T = TypeVar("T")
U = TypeVar("U")


# ============================================================
# 1. LAMBDA FUNCTIONS
# ============================================================
def demonstrate_lambdas():
    """Lambda functions are anonymous, inline functions."""
    
    # Simple lambda
    square = lambda x: x ** 2
    print(f"square(5) = {square(5)}")

    # Multi-argument lambda
    add = lambda a, b: a + b
    print(f"add(3, 7) = {add(3, 7)}")

    # Lambda with conditional
    absolute = lambda x: x if x >= 0 else -x
    print(f"absolute(-42) = {absolute(-42)}")

    # Lambda for sorting
    students = [
        {"name": "Alice", "grade": 92},
        {"name": "Bob", "grade": 85},
        {"name": "Charlie", "grade": 95},
    ]
    by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
    print(f"Sorted by grade: {[s['name'] for s in by_grade]}")

    # Lambda with default arguments
    power = lambda base, exp=2: base ** exp
    print(f"power(5) = {power(5)}, power(2, 10) = {power(2, 10)}")


# ============================================================
# 2. MAP, FILTER, REDUCE
# ============================================================
def demonstrate_map_filter_reduce():
    """The three pillars of functional data transformation."""
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Original: {numbers}")

    # MAP: transform each element
    squared = list(map(lambda x: x ** 2, numbers))
    print(f"Mapped (squared): {squared}")

    # FILTER: keep elements matching a condition
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Filtered (evens): {evens}")

    # REDUCE: combine all elements into one result
    total = reduce(operator.add, numbers)
    product = reduce(operator.mul, numbers)
    print(f"Reduced (sum):     {total}")
    print(f"Reduced (product): {product}")

    # Chaining: filter then map
    result = list(
        map(
            lambda x: x ** 2,
            filter(lambda x: x % 2 != 0, numbers)
        )
    )
    print(f"Odd squares: {result}")

    # Reduce to find max
    max_val = reduce(lambda a, b: a if a > b else b, numbers)
    print(f"Reduced (max): {max_val}")

    # Reduce to build a dictionary
    pairs = [("a", 1), ("b", 2), ("c", 3)]
    as_dict = reduce(lambda d, pair: {**d, pair[0]: pair[1]}, pairs, {})
    print(f"Reduced (to dict): {as_dict}")


# ============================================================
# 3. HIGHER-ORDER FUNCTIONS
# ============================================================
def apply_twice(func: Callable[[int], int], value: int) -> int:
    """A function that takes another function as an argument."""
    return func(func(value))


def apply_n_times(func: Callable[[T], T], n: int) -> Callable[[T], T]:
    """Return a function that applies func n times."""
    def repeated(value: T) -> T:
        result = value
        for _ in range(n):
            result = func(result)
        return result
    return repeated


def map_custom(func: Callable[[T], U], items: list[T]) -> list[U]:
    """Custom implementation of map."""
    return [func(item) for item in items]


def filter_custom(func: Callable[[T], bool], items: list[T]) -> list[T]:
    """Custom implementation of filter."""
    return [item for item in items if func(item)]


def demonstrate_higher_order():
    """Functions that operate on other functions."""
    
    double = lambda x: x * 2
    increment = lambda x: x + 1

    print(f"apply_twice(double, 3) = {apply_twice(double, 3)}")
    print(f"apply_twice(increment, 10) = {apply_twice(increment, 10)}")

    # Create a function that quadruples a number
    quadruple = apply_n_times(double, 2)
    print(f"quadruple(5) = {quadruple(5)}")

    # Create a function that adds 5
    add_five = apply_n_times(increment, 5)
    print(f"add_five(10) = {add_five(10)}")

    # Custom map/filter
    nums = [1, 2, 3, 4, 5]
    print(f"map_custom(square, {nums}) = {map_custom(lambda x: x**2, nums)}")
    print(f"filter_custom(>3, {nums}) = {filter_custom(lambda x: x > 3, nums)}")


# ============================================================
# 4. CLOSURES
# ============================================================
def make_multiplier(factor: int) -> Callable[[int], int]:
    """Create a multiplier function using a closure.
    
    The inner function 'remembers' the 'factor' variable
    even after make_multiplier has returned.
    """
    def multiplier(value: int) -> int:
        return value * factor
    return multiplier


def make_counter(start: int = 0) -> dict:
    """Create a counter using closures (encapsulated state).
    
    Returns a dict of functions that share the same 'count' variable.
    """
    count = [start]  # Use list for mutability in closure

    def increment():
        count[0] += 1
        return count[0]

    def decrement():
        count[0] -= 1
        return count[0]

    def get_value():
        return count[0]

    def reset():
        count[0] = start
        return count[0]

    return {
        "increment": increment,
        "decrement": decrement,
        "get": get_value,
        "reset": reset,
    }


def make_validator(min_val: float = None, max_val: float = None):
    """Create a validator function with configurable bounds."""
    def validate(value: float) -> bool:
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
        return True
    return validate


def demonstrate_closures():
    """Closures capture variables from their enclosing scope."""
    
    # Multipliers
    triple = make_multiplier(3)
    quintuple = make_multiplier(5)
    print(f"triple(10) = {triple(10)}")
    print(f"quintuple(10) = {quintuple(10)}")

    # Counter
    counter = make_counter(0)
    counter["increment"]()
    counter["increment"]()
    counter["increment"]()
    print(f"Counter value: {counter['get']()}")
    counter["decrement"]()
    print(f"After decrement: {counter['get']()}")
    counter["reset"]()
    print(f"After reset: {counter['get']()}")

    # Validators
    is_positive = make_validator(min_val=0)
    is_percentage = make_validator(min_val=0, max_val=100)
    print(f"\nis_positive(5): {is_positive(5)}")
    print(f"is_positive(-1): {is_positive(-1)}")
    print(f"is_percentage(50): {is_percentage(50)}")
    print(f"is_percentage(150): {is_percentage(150)}")


# ============================================================
# 5. PARTIAL FUNCTIONS
# ============================================================
def demonstrate_partial():
    """functools.partial creates specialized versions of functions."""
    
    # Basic partial
    def power(base: int, exponent: int) -> int:
        return base ** exponent

    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)

    print(f"square(5) = {square(5)}")
    print(f"cube(5) = {cube(5)}")

    # Partial with map
    numbers = [1, 2, 3, 4, 5]
    cubes = list(map(cube, numbers))
    print(f"cubes: {cubes}")

    # Partial for string formatting
    def format_price(amount: float, currency: str, decimals: int = 2) -> str:
        return f"{currency}{amount:.{decimals}f}"

    usd_price = partial(format_price, currency="$")
    eur_price = partial(format_price, currency="€")

    print(f"USD: {usd_price(49.99)}")
    print(f"EUR: {eur_price(49.99)}")

    # Partial for creating filters
    def is_divisible_by(divisor: int, number: int) -> bool:
        return number % divisor == 0

    is_even = partial(is_divisible_by, 2)
    is_multiple_of_5 = partial(is_divisible_by, 5)

    nums = list(range(1, 21))
    print(f"Evens: {list(filter(is_even, nums))}")
    print(f"Multiples of 5: {list(filter(is_multiple_of_5, nums))}")


# ============================================================
# 6. FUNCTION COMPOSITION
# ============================================================
def compose(*functions: Callable) -> Callable:
    """Compose multiple functions into one.
    
    compose(f, g, h)(x) == f(g(h(x)))
    Functions are applied right to left.
    """
    def composed(value):
        result = value
        for func in reversed(functions):
            result = func(result)
        return result
    return composed


def pipe(*functions: Callable) -> Callable:
    """Pipe functions left to right.
    
    pipe(f, g, h)(x) == h(g(f(x)))
    """
    def piped(value):
        result = value
        for func in functions:
            result = func(result)
        return result
    return piped


def demonstrate_composition():
    """Function composition builds complex operations from simple ones."""
    
    # Simple functions
    double = lambda x: x * 2
    increment = lambda x: x + 1
    square = lambda x: x ** 2
    negate = lambda x: -x

    # Compose (right to left)
    transform = compose(negate, square, increment, double)
    # Result: negate(square(increment(double(3))))
    # = negate(square(increment(6)))
    # = negate(square(7))
    # = negate(49)
    # = -49
    print(f"compose(negate, square, inc, double)(3) = {transform(3)}")

    # Pipe (left to right, more intuitive)
    pipeline = pipe(double, increment, square, negate)
    print(f"pipe(double, inc, square, negate)(3) = {pipeline(3)}")

    # String processing pipeline
    strip_ws = str.strip
    to_lower = str.lower
    replace_spaces = lambda s: s.replace(" ", "_")
    
    slugify = pipe(strip_ws, to_lower, replace_spaces)
    result = slugify("  Hello World Python  ")
    print(f"slugify('  Hello World Python  ') = '{result}'")

    # Data transformation pipeline
    parse_int = lambda s: int(s)
    clamp = lambda x: max(0, min(100, x))
    to_grade = lambda x: "A" if x >= 90 else "B" if x >= 80 else "C" if x >= 70 else "F"

    process_score = pipe(parse_int, clamp, to_grade)
    
    scores = ["95", "82", "67", "150", "-10"]
    print(f"\nScore processing:")
    for s in scores:
        grade = process_score(s)
        print(f"  '{s}' -> {grade}")


# ============================================================
# 7. CURRYING
# ============================================================
def curry(func: Callable) -> Callable:
    """Convert a multi-argument function into curried form.
    
    curry(f)(a)(b)(c) == f(a, b, c)
    """
    import inspect
    sig = inspect.signature(func)
    num_params = len(sig.parameters)

    def curried(*args):
        if len(args) >= num_params:
            return func(*args)
        return lambda *more_args: curried(*(args + more_args))

    return curried


def demonstrate_currying():
    """Currying transforms multi-arg functions into single-arg chains."""
    
    @curry
    def add_three(a: int, b: int, c: int) -> int:
        return a + b + c

    print(f"add_three(1, 2, 3) = {add_three(1, 2, 3)}")
    print(f"add_three(1)(2)(3) = {add_three(1)(2)(3)}")
    print(f"add_three(1, 2)(3) = {add_three(1, 2)(3)}")

    add_10 = add_three(10)
    add_10_20 = add_10(20)
    print(f"add_10(20)(30) = {add_10_20(30)}")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Lambda Functions")
    demonstrate_lambdas()

    separator("2. Map, Filter, Reduce")
    demonstrate_map_filter_reduce()

    separator("3. Higher-Order Functions")
    demonstrate_higher_order()

    separator("4. Closures")
    demonstrate_closures()

    separator("5. Partial Functions")
    demonstrate_partial()

    separator("6. Function Composition")
    demonstrate_composition()

    separator("7. Currying")
    demonstrate_currying()


if __name__ == "__main__":
    main()
