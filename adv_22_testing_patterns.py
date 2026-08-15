"""
Advanced Python - Lesson 22: Testing & Mocking Patterns
========================================================
Testing ensures code correctness. This module demonstrates
testing patterns using unittest and mocking techniques.

Topics Covered:
- unittest.TestCase basics
- Assertions and custom assertions
- Test fixtures (setUp/tearDown)
- Mocking with unittest.mock
- Patching modules and classes
- Parameterized tests
- Test doubles: stubs, fakes, spies
- Testing async code
- Property-based testing concepts
"""

import unittest
from unittest.mock import (
    Mock, MagicMock, patch, PropertyMock,
    call, ANY, sentinel
)
from typing import Any
from datetime import datetime
import json
import os


# ============================================================
# CODE UNDER TEST
# ============================================================
class UserService:
    """Service class to demonstrate testing patterns."""
    
    def __init__(self, db, email_client, logger):
        self.db = db
        self.email_client = email_client
        self.logger = logger

    def create_user(self, name: str, email: str, age: int) -> dict:
        """Create a new user with validation."""
        # Validate inputs
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        if "@" not in email:
            raise ValueError(f"Invalid email: {email}")
        if age < 0 or age > 150:
            raise ValueError(f"Invalid age: {age}")
        
        # Check if user exists
        existing = self.db.find_by_email(email)
        if existing:
            raise ValueError(f"User with email {email} already exists")
        
        # Create user
        user = {
            "id": self.db.next_id(),
            "name": name.strip(),
            "email": email,
            "age": age,
            "created_at": datetime.now().isoformat(),
        }
        
        self.db.save(user)
        self.email_client.send_welcome(email, name)
        self.logger.info(f"User created: {name} ({email})")
        
        return user

    def get_user(self, user_id: int) -> dict | None:
        """Get user by ID."""
        user = self.db.find_by_id(user_id)
        if user:
            self.logger.info(f"User fetched: {user_id}")
        else:
            self.logger.warning(f"User not found: {user_id}")
        return user

    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        user = self.db.find_by_id(user_id)
        if not user:
            return False
        self.db.delete(user_id)
        self.email_client.send_goodbye(user["email"], user["name"])
        self.logger.info(f"User deleted: {user_id}")
        return True

    def update_age(self, user_id: int, new_age: int) -> dict:
        """Update user's age."""
        if new_age < 0 or new_age > 150:
            raise ValueError(f"Invalid age: {new_age}")
        user = self.db.find_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        user["age"] = new_age
        self.db.save(user)
        return user


class Calculator:
    """Simple calculator for testing demonstrations."""
    
    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    def factorial(self, n: int) -> int:
        if n < 0:
            raise ValueError("Factorial not defined for negative numbers")
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)


# ============================================================
# 1. BASIC TESTS
# ============================================================
class TestCalculator(unittest.TestCase):
    """Basic unit tests for Calculator."""
    
    def setUp(self):
        """Called before each test method."""
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(0, 5), -5)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 100), 0)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.3333, places=3)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_factorial(self):
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(1), 1)
        self.assertEqual(self.calc.factorial(5), 120)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            self.calc.factorial(-1)


# ============================================================
# 2. COMPREHENSIVE ASSERTIONS
# ============================================================
class TestAssertions(unittest.TestCase):
    """Demonstrate various assertion methods."""
    
    def test_equality_assertions(self):
        self.assertEqual(1 + 1, 2)
        self.assertNotEqual(1, 2)
        self.assertEqual([1, 2, 3], [1, 2, 3])
        self.assertEqual({"a": 1}, {"a": 1})

    def test_truth_assertions(self):
        self.assertTrue(1 > 0)
        self.assertFalse(1 < 0)
        self.assertTrue(bool("non-empty"))
        self.assertFalse(bool(""))

    def test_membership_assertions(self):
        self.assertIn("a", ["a", "b", "c"])
        self.assertNotIn("d", ["a", "b", "c"])
        self.assertIn("key", {"key": "value"})

    def test_type_assertions(self):
        self.assertIsInstance(42, int)
        self.assertIsInstance("hello", str)
        self.assertIsInstance([], list)
        self.assertNotIsInstance(42, str)

    def test_none_assertions(self):
        self.assertIsNone(None)
        self.assertIsNotNone(42)

    def test_comparison_assertions(self):
        self.assertGreater(5, 3)
        self.assertGreaterEqual(5, 5)
        self.assertLess(3, 5)
        self.assertLessEqual(5, 5)

    def test_string_assertions(self):
        self.assertRegex("hello123", r"\w+\d+")
        self.assertNotRegex("hello", r"\d+")

    def test_collection_assertions(self):
        self.assertCountEqual([1, 2, 3], [3, 1, 2])
        self.assertListEqual([1, 2], [1, 2])
        self.assertDictEqual({"a": 1}, {"a": 1})
        self.assertSetEqual({1, 2}, {2, 1})

    def test_custom_message(self):
        result = 42
        self.assertEqual(result, 42, f"Expected 42 but got {result}")


# ============================================================
# 3. TEST FIXTURES
# ============================================================
class TestWithFixtures(unittest.TestCase):
    """Using setUp/tearDown for test isolation."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        self.mock_db = Mock()
        self.mock_email = Mock()
        self.mock_logger = Mock()
        self.service = UserService(
            self.mock_db, self.mock_email, self.mock_logger
        )
        
        # Configure mock behaviors
        self.mock_db.next_id.return_value = 1
        self.mock_db.find_by_email.return_value = None

    def tearDown(self):
        """Clean up after each test."""
        # Reset all mocks
        self.mock_db.reset_mock()
        self.mock_email.reset_mock()
        self.mock_logger.reset_mock()

    def test_create_user_success(self):
        user = self.service.create_user("Alice", "alice@test.com", 30)
        
        self.assertEqual(user["name"], "Alice")
        self.assertEqual(user["email"], "alice@test.com")
        self.assertEqual(user["age"], 30)
        self.assertEqual(user["id"], 1)
        
        # Verify DB was called
        self.mock_db.save.assert_called_once()
        self.mock_email.send_welcome.assert_called_once_with(
            "alice@test.com", "Alice"
        )
        self.mock_logger.info.assert_called_once()

    def test_create_user_invalid_name(self):
        with self.assertRaises(ValueError) as ctx:
            self.service.create_user("A", "a@test.com", 25)
        self.assertIn("2 characters", str(ctx.exception))

    def test_create_user_invalid_email(self):
        with self.assertRaises(ValueError):
            self.service.create_user("Alice", "invalid-email", 25)

    def test_create_user_duplicate_email(self):
        self.mock_db.find_by_email.return_value = {"id": 1, "name": "Existing"}
        
        with self.assertRaises(ValueError) as ctx:
            self.service.create_user("Alice", "dup@test.com", 30)
        self.assertIn("already exists", str(ctx.exception))

    def test_delete_user_success(self):
        self.mock_db.find_by_id.return_value = {
            "id": 1, "name": "Alice", "email": "alice@test.com"
        }
        
        result = self.service.delete_user(1)
        self.assertTrue(result)
        self.mock_db.delete.assert_called_once_with(1)
        self.mock_email.send_goodbye.assert_called_once_with(
            "alice@test.com", "Alice"
        )

    def test_delete_user_not_found(self):
        self.mock_db.find_by_id.return_value = None
        result = self.service.delete_user(999)
        self.assertFalse(result)
        self.mock_db.delete.assert_not_called()


# ============================================================
# 4. MOCKING TECHNIQUES
# ============================================================
class TestMocking(unittest.TestCase):
    """Advanced mocking patterns."""
    
    def test_mock_return_value(self):
        """Configure mock return values."""
        mock_api = Mock()
        mock_api.get_user.return_value = {"name": "Alice", "age": 30}
        
        result = mock_api.get_user(1)
        self.assertEqual(result["name"], "Alice")
        mock_api.get_user.assert_called_once_with(1)

    def test_mock_side_effect(self):
        """Use side_effect for dynamic responses or exceptions."""
        mock_api = Mock()
        mock_api.fetch.side_effect = [
            {"data": "first"},
            {"data": "second"},
            ConnectionError("Network error"),
        ]
        
        self.assertEqual(mock_api.fetch()["data"], "first")
        self.assertEqual(mock_api.fetch()["data"], "second")
        
        with self.assertRaises(ConnectionError):
            mock_api.fetch()

    def test_mock_call_verification(self):
        """Verify how mocks were called."""
        mock_fn = Mock()
        mock_fn(1, 2, key="value")
        mock_fn(3, 4)
        
        # Check call count
        self.assertEqual(mock_fn.call_count, 2)
        
        # Check specific calls
        mock_fn.assert_any_call(1, 2, key="value")
        
        # Check all calls
        expected = [call(1, 2, key="value"), call(3, 4)]
        self.assertEqual(mock_fn.call_args_list, expected)

    def test_magic_mock(self):
        """MagicMock supports magic methods."""
        mock_list = MagicMock()
        mock_list.__len__.return_value = 5
        mock_list.__iter__.return_value = iter([1, 2, 3])
        mock_list.__getitem__.side_effect = lambda i: [10, 20, 30][i]
        
        self.assertEqual(len(mock_list), 5)
        self.assertEqual(list(mock_list), [1, 2, 3])
        self.assertEqual(mock_list[0], 10)

    @patch("builtins.open")
    def test_patch_builtin(self, mock_open):
        """Patch built-in functions."""
        mock_open.return_value.__enter__ = Mock(
            return_value=Mock(read=Mock(return_value='{"key": "value"}'))
        )
        mock_open.return_value.__exit__ = Mock(return_value=False)
        
        with open("config.json", "r") as f:
            data = json.loads(f.read())
        
        self.assertEqual(data["key"], "value")
        mock_open.assert_called_once_with("config.json", "r")

    def test_sentinel_values(self):
        """Use sentinel for unique test values."""
        MISSING = sentinel.MISSING
        
        def get_or_default(key, default=MISSING):
            data = {"a": 1}
            if key in data:
                return data[key]
            if default is MISSING:
                raise KeyError(key)
            return default
        
        self.assertEqual(get_or_default("a"), 1)
        self.assertEqual(get_or_default("b", 42), 42)
        with self.assertRaises(KeyError):
            get_or_default("b")


# ============================================================
# 5. PARAMETERIZED TESTS
# ============================================================
class TestParameterized(unittest.TestCase):
    """Run the same test with multiple inputs."""
    
    def test_calculator_add_cases(self):
        """Parameterized addition tests."""
        calc = Calculator()
        test_cases = [
            # (a, b, expected)
            (1, 2, 3),
            (0, 0, 0),
            (-1, 1, 0),
            (100, -50, 50),
            (0.1, 0.2, 0.3),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                result = calc.add(a, b)
                self.assertAlmostEqual(result, expected, places=10)

    def test_email_validation(self):
        """Parameterized email validation."""
        valid_emails = [
            "alice@example.com",
            "bob.smith@gmail.com",
            "user+tag@domain.co.uk",
        ]
        invalid_emails = [
            "not-an-email",
            "@missing-user.com",
            "user@",
            "",
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertIn("@", email, f"'{email}' should be valid")
        
        for email in invalid_emails:
            with self.subTest(email=email):
                parts = email.split("@")
                is_valid = len(parts) == 2 and all(parts)
                self.assertFalse(is_valid, f"'{email}' should be invalid")

    def test_factorial_cases(self):
        """Parameterized factorial tests."""
        calc = Calculator()
        cases = [(0, 1), (1, 1), (5, 120), (10, 3628800)]
        for n, expected in cases:
            with self.subTest(n=n):
                self.assertEqual(calc.factorial(n), expected)


# ============================================================
# 6. TEST DOUBLES: STUBS, FAKES, SPIES
# ============================================================
class FakeDatabase:
    """Fake: in-memory implementation for testing."""
    
    def __init__(self):
        self._store: dict[int, dict] = {}
        self._next_id = 1

    def save(self, user: dict):
        if "id" not in user:
            user["id"] = self._next_id
            self._next_id += 1
        self._store[user["id"]] = user

    def find_by_id(self, user_id: int) -> dict | None:
        return self._store.get(user_id)

    def find_by_email(self, email: str) -> dict | None:
        for user in self._store.values():
            if user["email"] == email:
                return user
        return None

    def delete(self, user_id: int):
        self._store.pop(user_id, None)

    def next_id(self) -> int:
        return self._next_id


class SpyLogger:
    """Spy: records calls but also executes behavior."""
    
    def __init__(self):
        self.messages: list[tuple[str, str]] = []

    def info(self, msg: str):
        self.messages.append(("INFO", msg))

    def warning(self, msg: str):
        self.messages.append(("WARNING", msg))

    def error(self, msg: str):
        self.messages.append(("ERROR", msg))


class TestWithDoubles(unittest.TestCase):
    """Testing with fakes, stubs, and spies."""
    
    def setUp(self):
        self.fake_db = FakeDatabase()
        self.mock_email = Mock()
        self.spy_logger = SpyLogger()
        self.service = UserService(
            self.fake_db, self.mock_email, self.spy_logger
        )

    def test_create_and_retrieve(self):
        """Integration test with fake database."""
        user = self.service.create_user("Alice", "alice@test.com", 30)
        
        # Retrieve from fake DB
        found = self.service.get_user(user["id"])
        self.assertIsNotNone(found)
        self.assertEqual(found["name"], "Alice")
        
        # Check spy logger
        info_messages = [m for level, m in self.spy_logger.messages if level == "INFO"]
        self.assertTrue(any("Alice" in m for m in info_messages))

    def test_delete_removes_from_db(self):
        """Test delete with fake database."""
        user = self.service.create_user("Bob", "bob@test.com", 25)
        
        result = self.service.delete_user(user["id"])
        self.assertTrue(result)
        
        # Verify removed from fake DB
        found = self.service.get_user(user["id"])
        self.assertIsNone(found)

    def test_update_age(self):
        """Test update with fake database."""
        user = self.service.create_user("Charlie", "charlie@test.com", 20)
        updated = self.service.update_age(user["id"], 21)
        self.assertEqual(updated["age"], 21)


# ============================================================
# 7. PATCHING MODULES AND CLASSES
# ============================================================
class WeatherAPI:
    """Class that depends on external services."""
    
    def __init__(self):
        self.base_url = "https://api.weather.com"

    def fetch_weather(self, city: str) -> dict:
        """This would normally make an HTTP request."""
        # Simulated — in real code this would use requests
        import requests  # noqa: would be imported
        response = requests.get(f"{self.base_url}/weather?city={city}")
        return response.json()

    def get_forecast_summary(self, city: str) -> str:
        weather = self.fetch_weather(city)
        temp = weather.get("temperature", "unknown")
        condition = weather.get("condition", "unknown")
        return f"{city}: {temp}°C, {condition}"


class TestPatching(unittest.TestCase):
    """Patch external dependencies for isolated testing."""
    
    def test_get_forecast_with_mock(self):
        api = WeatherAPI()
        
        # Patch the method directly
        api.fetch_weather = Mock(return_value={
            "temperature": 22,
            "condition": "sunny",
            "humidity": 45,
        })
        
        summary = api.get_forecast_summary("London")
        self.assertEqual(summary, "London: 22°C, sunny")
        api.fetch_weather.assert_called_once_with("London")

    def test_multiple_scenarios(self):
        api = WeatherAPI()
        
        scenarios = [
            ({"temperature": 35, "condition": "hot"}, "Paris: 35°C, hot"),
            ({"temperature": -5, "condition": "snowy"}, "Moscow: -5°C, snowy"),
            ({}, "Tokyo: unknown°C, unknown"),
        ]
        
        for weather_data, expected in scenarios:
            api.fetch_weather = Mock(return_value=weather_data)
            city = expected.split(":")[0]
            result = api.get_forecast_summary(city)
            self.assertEqual(result, expected)


# ============================================================
# 8. TESTING EXCEPTIONS AND EDGE CASES
# ============================================================
class TestEdgeCases(unittest.TestCase):
    """Test error handling and edge cases."""
    
    def setUp(self):
        self.calc = Calculator()

    def test_division_error_message(self):
        with self.assertRaises(ZeroDivisionError) as ctx:
            self.calc.divide(10, 0)
        self.assertIn("zero", str(ctx.exception).lower())

    def test_factorial_negative_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.calc.factorial(-5)
        self.assertIn("negative", str(ctx.exception).lower())

    def test_large_factorial(self):
        result = self.calc.factorial(20)
        self.assertEqual(result, 2432902008176640000)

    def test_floating_point_precision(self):
        result = self.calc.add(0.1, 0.2)
        self.assertAlmostEqual(result, 0.3, places=10)

    def test_very_large_numbers(self):
        result = self.calc.multiply(10**100, 10**100)
        self.assertEqual(result, 10**200)


# ============================================================
# RUN ALL TESTS
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("Running All Test Suites")
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestCalculator,
        TestAssertions,
        TestWithFixtures,
        TestMocking,
        TestParameterized,
        TestWithDoubles,
        TestPatching,
        TestEdgeCases,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    separator("Test Summary")
    print(f"  Tests run:    {result.testsRun}")
    print(f"  Successes:    {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  Failures:     {len(result.failures)}")
    print(f"  Errors:       {len(result.errors)}")
    print(f"  Skipped:      {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n  All tests passed!")


if __name__ == "__main__":
    main()
