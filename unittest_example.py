import unittest

# --- The Code We Want to Test ---
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# --- The Unit Tests ---
# We create a class that inherits from unittest.TestCase
class TestMathFunctions(unittest.TestCase):

    # Every test method MUST start with the word "test_"
    def test_add_positive_numbers(self):
        # We assert (expect) that add(2, 3) exactly equals 5
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-2, -3), -5)
        self.assertEqual(add(-2, 3), 1)

    def test_divide_normal(self):
        self.assertEqual(divide(10, 2), 5.0)
        
        # When dealing with floating point math (decimals), assertAlmostEqual is safer
        self.assertAlmostEqual(divide(5, 2), 2.5)

    def test_divide_by_zero(self):
        # We expect a ValueError to be raised if we try to divide by zero
        # The 'with' context manager captures the error so the test passes instead of crashing
        with self.assertRaises(ValueError):
            divide(10, 0)

# --- Running the Tests ---
if __name__ == "__main__":
    # This automatically finds and runs all methods starting with "test_" in this file
    print("Running Unit Tests...\n")
    unittest.main()
