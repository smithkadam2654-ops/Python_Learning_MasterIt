"""
Testing Utilities Module

This module provides comprehensive testing and quality assurance utilities including:
- Unit test helpers and assertions
- Test data generation
- Mock and stub utilities
- Test fixtures and setup/teardown
- Performance testing helpers
- Property-based testing
- Test coverage helpers
- Test runners and reporters
- Assertion utilities
- Test environment management

All functions include comprehensive docstrings and type hints.
"""

import time
import random
import string
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
import json


@dataclass
class TestResult:
    """Container for test results."""
    test_name: str
    passed: bool
    duration: float
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None


@dataclass
class TestSuite:
    """Container for test suite information."""
    name: str
    tests: List[TestResult]
    total_tests: int
    passed_tests: int
    failed_tests: int
    total_duration: float


class AssertionHelper:
    """Custom assertion utilities for testing."""
    
    @staticmethod
    def assert_equal(actual: Any, expected: Any, message: str = "") -> None:
        """Assert that two values are equal."""
        if actual != expected:
            error_msg = f"Expected {expected}, but got {actual}"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_not_equal(actual: Any, expected: Any, message: str = "") -> None:
        """Assert that two values are not equal."""
        if actual == expected:
            error_msg = f"Expected {actual} to be different from {expected}"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_true(value: Any, message: str = "") -> None:
        """Assert that value is truthy."""
        if not value:
            error_msg = f"Expected {value} to be truthy"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_false(value: Any, message: str = "") -> None:
        """Assert that value is falsy."""
        if value:
            error_msg = f"Expected {value} to be falsy"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_in(item: Any, container: Any, message: str = "") -> None:
        """Assert that item is in container."""
        if item not in container:
            error_msg = f"Expected {item} to be in {container}"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_not_in(item: Any, container: Any, message: str = "") -> None:
        """Assert that item is not in container."""
        if item in container:
            error_msg = f"Expected {item} to not be in {container}"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_is_none(value: Any, message: str = "") -> None:
        """Assert that value is None."""
        if value is not None:
            error_msg = f"Expected {value} to be None"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_is_not_none(value: Any, message: str = "") -> None:
        """Assert that value is not None."""
        if value is None:
            error_msg = f"Expected value to not be None"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_raises(exception_type: type, func: Callable, *args, **kwargs) -> Exception:
        """Assert that function raises specific exception."""
        try:
            func(*args, **kwargs)
            raise AssertionError(f"Expected {exception_type.__name__} to be raised")
        except exception_type as e:
            return e
        except Exception as e:
            raise AssertionError(f"Expected {exception_type.__name__}, but got {type(e).__name__}")
    
    @staticmethod
    def assert_almost_equal(a: float, b: float, tolerance: float = 1e-7, message: str = "") -> None:
        """Assert that two floats are almost equal within tolerance."""
        if abs(a - b) > tolerance:
            error_msg = f"Expected {a} to be almost equal to {b} (tolerance: {tolerance})"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_greater(a: Any, b: Any, message: str = "") -> None:
        """Assert that a > b."""
        if not a > b:
            error_msg = f"Expected {a} to be greater than {b}"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_less(a: Any, b: Any, message: str = "") -> None:
        """Assert that a < b."""
        if not a < b:
            error_msg = f"Expected {a} to be less than {b}"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_type(value: Any, expected_type: type, message: str = "") -> None:
        """Assert that value is of expected type."""
        if not isinstance(value, expected_type):
            error_msg = f"Expected {value} to be of type {expected_type.__name__}, got {type(value).__name__}"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_length(container: Any, expected_length: int, message: str = "") -> None:
        """Assert that container has expected length."""
        actual_length = len(container)
        if actual_length != expected_length:
            error_msg = f"Expected length {expected_length}, but got {actual_length}"
            if message:
                error_msg = f"{message}: {error_msg}"
            raise AssertionError(error_msg)


class TestDataGenerator:
    """Generate test data for various types."""
    
    @staticmethod
    def random_string(length: int = 10, 
                     include_uppercase: bool = True,
                     include_lowercase: bool = True,
                     include_digits: bool = True,
                     include_special: bool = False) -> str:
        """Generate random string."""
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
    def random_int(min_val: int = 0, max_val: int = 100) -> int:
        """Generate random integer."""
        return random.randint(min_val, max_val)
    
    @staticmethod
    def random_float(min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Generate random float."""
        return random.uniform(min_val, max_val)
    
    @staticmethod
    def random_email() -> str:
        """Generate random email address."""
        username = TestDataGenerator.random_string(8, include_digits=False, include_special=False)
        domain = TestDataGenerator.random_string(6, include_digits=False, include_special=False)
        return f"{username}@{domain}.com"
    
    @staticmethod
    def random_phone() -> str:
        """Generate random phone number."""
        return f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    @staticmethod
    def random_url() -> str:
        """Generate random URL."""
        domain = TestDataGenerator.random_string(8, include_digits=False, include_special=False)
        path = TestDataGenerator.random_string(6, include_digits=False, include_special=False)
        return f"https://www.{domain}.com/{path}"
    
    @staticmethod
    def random_date(start_year: int = 2000, end_year: int = 2024) -> str:
        """Generate random date string."""
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year:04d}-{month:02d}-{day:02d}"
    
    @staticmethod
    def random_name() -> str:
        """Generate random name."""
        first_names = ["John", "Jane", "Bob", "Alice", "Charlie", "Diana", "Edward", "Fiona"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    @staticmethod
    def random_address() -> str:
        """Generate random address."""
        street_numbers = random.randint(1, 9999)
        street_names = ["Main", "Oak", "Maple", "Cedar", "Elm", "Pine", "Washington"]
        street_types = ["St", "Ave", "Blvd", "Ln", "Dr", "Rd"]
        cities = ["Springfield", "Riverdale", "Greenville", "Fairview", "Oakville"]
        states = ["CA", "NY", "TX", "FL", "IL"]
        
        return f"{street_numbers} {random.choice(street_names)} {random.choice(street_types)}, {random.choice(cities)}, {random.choice(states)}"
    
    @staticmethod
    def random_ipv4() -> str:
        """Generate random IPv4 address."""
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    
    @staticmethod
    def random_uuid() -> str:
        """Generate random UUID string."""
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def random_dict(keys: List[str], value_types: List[type]) -> Dict[str, Any]:
        """Generate random dictionary with specified keys and value types."""
        result = {}
        for key, value_type in zip(keys, value_types):
            if value_type == str:
                result[key] = TestDataGenerator.random_string(8)
            elif value_type == int:
                result[key] = TestDataGenerator.random_int()
            elif value_type == float:
                result[key] = TestDataGenerator.random_float()
            elif value_type == bool:
                result[key] = random.choice([True, False])
            else:
                result[key] = TestDataGenerator.random_string(8)
        return result
    
    @staticmethod
    def random_list(length: int, value_type: type = str) -> List[Any]:
        """Generate random list of specified type."""
        if value_type == str:
            return [TestDataGenerator.random_string(8) for _ in range(length)]
        elif value_type == int:
            return [TestDataGenerator.random_int() for _ in range(length)]
        elif value_type == float:
            return [TestDataGenerator.random_float() for _ in range(length)]
        elif value_type == bool:
            return [random.choice([True, False]) for _ in range(length)]
        else:
            return [TestDataGenerator.random_string(8) for _ in range(length)]


class MockObject:
    """Simple mock object for testing."""
    
    def __init__(self, **kwargs):
        """Initialize mock object with attributes."""
        self._call_history = []
        self._return_values = {}
        self._side_effects = {}
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __call__(self, *args, **kwargs):
        """Make mock object callable."""
        self._call_history.append((args, kwargs))
        
        method_name = kwargs.get('_method_name', '__call__')
        
        if method_name in self._side_effects:
            return self._side_effects[method_name](*args, **kwargs)
        
        if method_name in self._return_values:
            return self._return_values[method_name]
        
        return None
    
    def set_return_value(self, method_name: str, return_value: Any) -> None:
        """Set return value for a method."""
        self._return_values[method_name] = return_value
    
    def set_side_effect(self, method_name: str, side_effect: Callable) -> None:
        """Set side effect for a method."""
        self._side_effects[method_name] = side_effect
    
    def get_call_count(self, method_name: Optional[str] = None) -> int:
        """Get number of times method was called."""
        if method_name is None:
            return len(self._call_history)
        
        return sum(1 for call in self._call_history if call[1].get('_method_name') == method_name)
    
    def was_called(self, method_name: Optional[str] = None) -> bool:
        """Check if method was called."""
        return self.get_call_count(method_name) > 0
    
    def get_call_args(self, method_name: Optional[str] = None) -> List[Tuple]:
        """Get arguments from method calls."""
        if method_name is None:
            return [call[0] for call in self._call_history]
        
        return [call[0] for call in self._call_history if call[1].get('_method_name') == method_name]
    
    def reset_mock(self) -> None:
        """Reset call history."""
        self._call_history = []


class TestFixture:
    """Test fixture management."""
    
    def __init__(self):
        """Initialize test fixture."""
        self._setup_fixtures = []
        self._teardown_fixtures = []
        self._fixtures = {}
    
    def add_setup(self, func: Callable) -> None:
        """Add setup function."""
        self._setup_fixtures.append(func)
    
    def add_teardown(self, func: Callable) -> None:
        """Add teardown function."""
        self._teardown_fixtures.append(func)
    
    def add_fixture(self, name: str, value: Any) -> None:
        """Add fixture value."""
        self._fixtures[name] = value
    
    def get_fixture(self, name: str) -> Any:
        """Get fixture value."""
        return self._fixtures.get(name)
    
    def setup(self) -> None:
        """Run all setup functions."""
        for func in self._setup_fixtures:
            func()
    
    def teardown(self) -> None:
        """Run all teardown functions."""
        for func in reversed(self._teardown_fixtures):
            func()


class PerformanceTester:
    """Performance testing utilities."""
    
    @staticmethod
    def measure_time(func: Callable, *args, **kwargs) -> Tuple[Any, float]:
        """Measure execution time of function."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, end_time - start_time
    
    @staticmethod
    def benchmark(func: Callable, iterations: int = 100, *args, **kwargs) -> Dict[str, float]:
        """Benchmark function over multiple iterations."""
        times = []
        
        for _ in range(iterations):
            _, duration = PerformanceTester.measure_time(func, *args, **kwargs)
            times.append(duration)
        
        return {
            "total_time": sum(times),
            "average_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "iterations": iterations
        }
    
    @staticmethod
    def memory_usage(func: Callable, *args, **kwargs) -> Tuple[Any, Dict[str, float]]:
        """Measure memory usage of function."""
        try:
            import tracemalloc
            tracemalloc.start()
            
            result = func(*args, **kwargs)
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            return result, {
                "current_mb": current / (1024 * 1024),
                "peak_mb": peak / (1024 * 1024)
            }
        except ImportError:
            return func(*args, **kwargs), {"current_mb": 0, "peak_mb": 0}
    
    @staticmethod
    def assert_performance(func: Callable, max_time: float, *args, **kwargs) -> None:
        """Assert that function completes within max time."""
        _, duration = PerformanceTester.measure_time(func, *args, **kwargs)
        
        if duration > max_time:
            raise AssertionError(f"Function took {duration:.4f}s, expected max {max_time:.4f}s")


class PropertyTester:
    """Property-based testing utilities."""
    
    @staticmethod
    def for_all(generator: Callable, property_func: Callable, 
                iterations: int = 100) -> bool:
        """Test property for all generated values."""
        for _ in range(iterations):
            value = generator()
            if not property_func(value):
                return False
        return True
    
    @staticmethod
    def there_exists(generator: Callable, property_func: Callable,
                    iterations: int = 100) -> bool:
        """Test that property exists for at least one generated value."""
        for _ in range(iterations):
            value = generator()
            if property_func(value):
                return True
        return False
    
    @staticmethod
    def for_none(generator: Callable, property_func: Callable,
                iterations: int = 100) -> bool:
        """Test that property is false for all generated values."""
        for _ in range(iterations):
            value = generator()
            if property_func(value):
                return False
        return True


class TestRunner:
    """Simple test runner."""
    
    def __init__(self):
        """Initialize test runner."""
        self.test_results: List[TestResult] = []
        self.test_suites: List[TestSuite] = []
    
    def run_test(self, test_func: Callable, test_name: Optional[str] = None) -> TestResult:
        """Run a single test function."""
        if test_name is None:
            test_name = test_func.__name__
        
        start_time = time.time()
        
        try:
            test_func()
            duration = time.time() - start_time
            result = TestResult(test_name, True, duration)
        except AssertionError as e:
            duration = time.time() - start_time
            result = TestResult(test_name, False, duration, str(e))
        except Exception as e:
            duration = time.time() - start_time
            result = TestResult(test_name, False, duration, str(e), "Unexpected error")
        
        self.test_results.append(result)
        return result
    
    def run_tests(self, test_funcs: List[Callable]) -> List[TestResult]:
        """Run multiple test functions."""
        results = []
        for test_func in test_funcs:
            result = self.run_test(test_func)
            results.append(result)
        return results
    
    def create_suite(self, suite_name: str, test_results: List[TestResult]) -> TestSuite:
        """Create a test suite from results."""
        passed = sum(1 for r in test_results if r.passed)
        failed = len(test_results) - passed
        total_duration = sum(r.duration for r in test_results)
        
        suite = TestSuite(
            name=suite_name,
            tests=test_results,
            total_tests=len(test_results),
            passed_tests=passed,
            failed_tests=failed,
            total_duration=total_duration
        )
        
        self.test_suites.append(suite)
        return suite
    
    def print_results(self) -> None:
        """Print test results."""
        if not self.test_results:
            print("No tests run")
            return
        
        passed = sum(1 for r in self.test_results if r.passed)
        failed = len(self.test_results) - passed
        
        print(f"\n{'='*50}")
        print(f"Test Results: {passed}/{len(self.test_results)} passed")
        print(f"{'='*50}")
        
        for result in self.test_results:
            status = "✓ PASS" if result.passed else "✗ FAIL"
            print(f"{status}: {result.test_name} ({result.duration:.4f}s)")
            if not result.passed:
                print(f"  Error: {result.error_message}")
        
        print(f"\nTotal duration: {sum(r.duration for r in self.test_results):.4f}s")


class TestEnvironment:
    """Test environment management."""
    
    @staticmethod
    def set_env_var(key: str, value: str) -> None:
        """Set environment variable for testing."""
        os.environ[key] = value
    
    @staticmethod
    def get_env_var(key: str) -> Optional[str]:
        """Get environment variable."""
        return os.environ.get(key)
    
    @staticmethod
    def clear_env_var(key: str) -> None:
        """Clear environment variable."""
        if key in os.environ:
            del os.environ[key]
    
    @staticmethod
    def backup_env() -> Dict[str, str]:
        """Backup current environment."""
        return dict(os.environ)
    
    @staticmethod
    def restore_env(env_backup: Dict[str, str]) -> None:
        """Restore environment from backup."""
        os.environ.clear()
        os.environ.update(env_backup)
    
    @staticmethod
    def create_temp_dir() -> str:
        """Create temporary directory for testing."""
        import tempfile
        return tempfile.mkdtemp()
    
    @staticmethod
    def cleanup_temp_dir(temp_dir: str) -> None:
        """Clean up temporary directory."""
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_assertions():
    """Test assertion helpers."""
    AssertionHelper.assert_equal(1, 1)
    AssertionHelper.assert_true(True)
    AssertionHelper.assert_in(1, [1, 2, 3])
    AssertionHelper.assert_greater(5, 3)
    AssertionHelper.assert_almost_equal(1.0000001, 1.0, tolerance=1e-6)


def test_data_generation():
    """Test data generation."""
    assert len(TestDataGenerator.random_string(10)) == 10
    assert 0 <= TestDataGenerator.random_int(0, 100) <= 100
    assert "@" in TestDataGenerator.random_email()


def test_mock_object():
    """Test mock object."""
    mock = MockObject()
    mock.set_return_value("test_method", "test_value")
    assert mock.get_call_count() == 0


def demonstrate_testing_utils():
    """Demonstrate testing utilities functionality."""
    print("=== Testing Utilities Demonstration ===\n")
    
    # Test Data Generation
    print("1. Test Data Generation:")
    print(f"   Random string: {TestDataGenerator.random_string(8)}")
    print(f"   Random int: {TestDataGenerator.random_int(1, 100)}")
    print(f"   Random email: {TestDataGenerator.random_email()}")
    print(f"   Random phone: {TestDataGenerator.random_phone()}")
    print(f"   Random name: {TestDataGenerator.random_name()}")
    print(f"   Random address: {TestDataGenerator.random_address()}")
    print(f"   Random IPv4: {TestDataGenerator.random_ipv4()}")
    print(f"   Random UUID: {TestDataGenerator.random_uuid()}")
    
    # Assertions
    print("\n2. Assertion Helpers:")
    try:
        AssertionHelper.assert_equal(1, 1)
        print("   assert_equal(1, 1): ✓")
    except AssertionError:
        print("   assert_equal(1, 1): ✗")
    
    try:
        AssertionHelper.assert_greater(5, 3)
        print("   assert_greater(5, 3): ✓")
    except AssertionError:
        print("   assert_greater(5, 3): ✗")
    
    try:
        AssertionHelper.assert_almost_equal(1.0000001, 1.0, tolerance=1e-6)
        print("   assert_almost_equal: ✓")
    except AssertionError:
        print("   assert_almost_equal: ✗")
    
    # Mock Object
    print("\n3. Mock Object:")
    mock = MockObject()
    mock.set_return_value("get_data", "test_data")
    print(f"   Return value set: {mock._return_values}")
    print(f"   Call count: {mock.get_call_count()}")
    print(f"   Was called: {mock.was_called()}")
    
    # Performance Testing
    print("\n4. Performance Testing:")
    def sample_function():
        return sum(range(1000))
    
    result, duration = PerformanceTester.measure_time(sample_function)
    print(f"   Function execution time: {duration:.6f}s")
    
    benchmark = PerformanceTester.benchmark(sample_function, iterations=10)
    print(f"   Benchmark (10 iterations):")
    print(f"     Average: {benchmark['average_time']:.6f}s")
    print(f"     Min: {benchmark['min_time']:.6f}s")
    print(f"     Max: {benchmark['max_time']:.6f}s")
    
    # Test Runner
    print("\n5. Test Runner:")
    runner = TestRunner()
    runner.run_test(test_assertions, "test_assertions")
    runner.run_test(test_data_generation, "test_data_generation")
    runner.run_test(test_mock_object, "test_mock_object")
    runner.print_results()
    
    # Property Testing
    print("\n6. Property Testing:")
    def even_generator():
        return random.randint(0, 100) * 2
    
    def is_even_property(n):
        return n % 2 == 0
    
    result = PropertyTester.for_all(even_generator, is_even_property, iterations=10)
    print(f"   All generated numbers are even: {result}")
    
    # Test Environment
    print("\n7. Test Environment:")
    TestEnvironment.set_env_var("TEST_VAR", "test_value")
    print(f"   Set env var: {TestEnvironment.get_env_var('TEST_VAR')}")
    TestEnvironment.clear_env_var("TEST_VAR")
    print(f"   Cleared env var: {TestEnvironment.get_env_var('TEST_VAR')}")
    
    temp_dir = TestEnvironment.create_temp_dir()
    print(f"   Created temp dir: {temp_dir}")
    TestEnvironment.cleanup_temp_dir(temp_dir)
    print(f"   Cleaned up temp dir")
    
    print("\n=== Demonstration Complete ===")


if __name__ == "__main__":
    import os
    demonstrate_testing_utils()