import unittest

# --- Code to be tested ---
def add(x, y):
    """Add two numbers together."""
    return x + y

def divide(x, y):
    """Divide x by y, raising an error if y is 0."""
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y

# --- Unit Tests ---
class TestMathFunctions(unittest.TestCase):
    """Test suite for our math functions."""
    
    # This runs BEFORE every single test method
    def setUp(self):
        self.test_var = 10
        
    # This runs AFTER every single test method
    def tearDown(self):
        pass 

    def test_add(self):
        # assertEqual checks if two values are equal
        self.assertEqual(add(10, 5), 15)
        self.assertEqual(add(-1, 1), 0)
        
    def test_add_with_setup_var(self):
        self.assertEqual(add(self.test_var, 5), 15)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertAlmostEqual(divide(10, 3), 3.3333333, places=6)
        
    def test_divide_by_zero(self):
        # assertRaises checks if a specific exception is raised
        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == "__main__":
    # This runs all the tests in the file
    # We use verbosity=2 to get detailed output
    print("Running Unit Tests...\n")
    unittest.main(verbosity=2)
