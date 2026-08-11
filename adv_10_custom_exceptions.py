"""
Advanced Python - Lesson 10: Custom Exceptions & Error Handling
================================================================
Robust error handling is critical for production code. Custom exceptions
provide meaningful error information and enable precise error recovery.

Topics Covered:
- Exception hierarchy
- Creating custom exception classes
- Exception chaining (raise from)
- Custom exception groups
- Try/except/else/finally patterns
- Contextual error handling
- Retry patterns with exceptions
"""

import traceback
import sys
from typing import Any


# ============================================================
# 1. CUSTOM EXCEPTION HIERARCHY
# ============================================================
class AppError(Exception):
    """Base exception for the application.
    
    All custom exceptions should inherit from this base.
    """
    def __init__(self, message: str, code: str = "UNKNOWN"):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


class ValidationError(AppError):
    """Raised when input validation fails."""
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"Validation failed for '{field}': {message}", "VALIDATION")


class NotFoundError(AppError):
    """Raised when a requested resource is not found."""
    def __init__(self, resource: str, identifier: Any):
        self.resource = resource
        self.identifier = identifier
        super().__init__(
            f"{resource} with id '{identifier}' not found", "NOT_FOUND"
        )


class AuthenticationError(AppError):
    """Raised when authentication fails."""
    def __init__(self, reason: str = "Invalid credentials"):
        super().__init__(reason, "AUTH_FAILED")


class PermissionDeniedError(AppError):
    """Raised when a user lacks permission."""
    def __init__(self, action: str, resource: str):
        self.action = action
        self.resource = resource
        super().__init__(
            f"Permission denied: cannot '{action}' on '{resource}'",
            "PERMISSION_DENIED",
        )


class RateLimitError(AppError):
    """Raised when rate limit is exceeded."""
    def __init__(self, limit: int, window: str):
        self.limit = limit
        self.window = window
        self.retry_after: int = 60
        super().__init__(
            f"Rate limit exceeded: {limit} requests per {window}",
            "RATE_LIMITED",
        )


# ============================================================
# 2. EXCEPTION CHAINING (raise from)
# ============================================================
class DatabaseError(AppError):
    """Raised for database-related errors."""
    def __init__(self, message: str, query: str = ""):
        self.query = query
        super().__init__(message, "DATABASE")


class ServiceError(AppError):
    """Raised when a service operation fails."""
    pass


def simulate_db_query(query: str) -> None:
    """Simulate a database error."""
    raise ConnectionError("Connection refused: PostgreSQL at localhost:5432")


def get_user_by_id(user_id: int) -> dict:
    """Service layer that catches low-level errors and re-raises with context."""
    try:
        simulate_db_query(f"SELECT * FROM users WHERE id = {user_id}")
    except ConnectionError as e:
        # Chain the exception: preserves original traceback
        raise DatabaseError(
            f"Failed to fetch user #{user_id}",
            query=f"SELECT * FROM users WHERE id = {user_id}",
        ) from e


def demonstrate_chaining():
    """Show exception chaining with 'raise from'."""
    
    try:
        get_user_by_id(42)
    except DatabaseError as e:
        print(f"Caught: {e}")
        print(f"\n  Cause: {e.__cause__}")
        print(f"  Cause type: {type(e.__cause__).__name__}")
        
    print()
    
    # Show the full chained traceback
    try:
        get_user_by_id(42)
    except DatabaseError:
        print("Full chained traceback:")
        traceback.print_exc()


# ============================================================
# 3. TRY / EXCEPT / ELSE / FINALLY
# ============================================================
def process_order(order_id: int, items: list[dict]) -> dict:
    """Demonstrate all four clauses of exception handling.
    
    try:     Code that might raise an exception
    except:  Handle the exception
    else:    Runs if NO exception was raised
    finally: Always runs (cleanup)
    """
    print(f"\nProcessing order #{order_id}:")
    
    try:
        # Risky operations
        if not items:
            raise ValidationError("items", "Order must contain at least one item")
        
        total = sum(item.get("price", 0) * item.get("qty", 1) for item in items)
        
        if total <= 0:
            raise ValidationError("total", f"Order total must be positive, got {total}")
        
        # Simulate potential DB error
        if order_id == 999:
            raise DatabaseError("Simulated DB failure")
        
        result = {"order_id": order_id, "total": total, "status": "confirmed"}

    except ValidationError as e:
        print(f"  Validation error: {e}")
        result = {"order_id": order_id, "status": "rejected", "error": str(e)}

    except DatabaseError as e:
        print(f"  Database error: {e}")
        result = {"order_id": order_id, "status": "error", "error": "DB failure"}

    except Exception as e:
        # Catch-all for unexpected errors
        print(f"  Unexpected error: {type(e).__name__}: {e}")
        result = {"order_id": order_id, "status": "error", "error": "unknown"}

    else:
        # Only runs if NO exception occurred
        print(f"  Order confirmed! Total: ${total:.2f}")

    finally:
        # Always runs — cleanup resources
        print(f"  Cleanup: logging order #{order_id} attempt")

    return result


# ============================================================
# 4. CUSTOM VALIDATION WITH COLLECTED ERRORS
# ============================================================
class ValidationErrors(Exception):
    """Exception that collects multiple validation errors."""
    
    def __init__(self):
        self.errors: list[ValidationError] = []
        super().__init__("Multiple validation errors")

    def add(self, field: str, message: str):
        self.errors.append(ValidationError(field, message))

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __str__(self) -> str:
        lines = [f"{len(self.errors)} validation error(s):"]
        for err in self.errors:
            lines.append(f"  - {err.field}: {err.message}")
        return "\n".join(lines)


def validate_user(data: dict) -> dict:
    """Validate user data, collecting ALL errors at once."""
    errors = ValidationErrors()

    # Name validation
    name = data.get("name", "")
    if not name:
        errors.add("name", "Name is required")
    elif len(name) < 2:
        errors.add("name", "Name must be at least 2 characters")

    # Email validation
    email = data.get("email", "")
    if not email:
        errors.add("email", "Email is required")
    elif "@" not in email:
        errors.add("email", "Invalid email format")

    # Age validation
    age = data.get("age")
    if age is None:
        errors.add("age", "Age is required")
    elif not isinstance(age, int) or age < 0 or age > 150:
        errors.add("age", "Age must be between 0 and 150")

    # Password validation
    password = data.get("password", "")
    if len(password) < 8:
        errors.add("password", "Password must be at least 8 characters")
    elif not any(c.isupper() for c in password):
        errors.add("password", "Password must contain an uppercase letter")
    elif not any(c.isdigit() for c in password):
        errors.add("password", "Password must contain a digit")

    if errors.has_errors():
        raise errors

    return {"name": name, "email": email, "age": age}


# ============================================================
# 5. RETRY WITH EXPONENTIAL BACKOFF
# ============================================================
import time
import random


class RetryableError(AppError):
    """Error that can be retried."""
    pass


class MaxRetriesExceeded(AppError):
    """Raised when all retry attempts are exhausted."""
    def __init__(self, operation: str, attempts: int, last_error: Exception):
        self.operation = operation
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(
            f"Max retries ({attempts}) exceeded for '{operation}'",
            "MAX_RETRIES",
        )


def retry_with_backoff(
    func: callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
    max_delay: float = 2.0,
):
    """Execute a function with exponential backoff retry."""
    last_error = None
    
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except RetryableError as e:
            last_error = e
            if attempt == max_retries:
                break
            # Exponential backoff with jitter
            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            jitter = random.uniform(0, delay * 0.1)
            wait_time = delay + jitter
            print(f"  Attempt {attempt}/{max_retries} failed: {e}")
            print(f"  Retrying in {wait_time:.3f}s...")
            time.sleep(wait_time)
    
    raise MaxRetriesExceeded(func.__name__, max_retries, last_error)


# ============================================================
# 6. CONTEXTUAL ERROR HANDLING
# ============================================================
class ErrorContext:
    """Context manager that adds context to exceptions."""
    
    def __init__(self, context_message: str):
        self.context_message = context_message

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            # Add context to the exception
            if not hasattr(exc_val, "context"):
                exc_val.context = []
            exc_val.context.append(self.context_message)
        return False  # Don't suppress


def demonstrate_contextual_errors():
    """Add layers of context to exceptions."""
    
    try:
        with ErrorContext("Processing batch #123"):
            with ErrorContext("Handling record #45"):
                with ErrorContext("Validating email field"):
                    raise ValidationError("email", "Invalid format")
    except ValidationError as e:
        print(f"Error: {e}")
        print(f"Context chain:")
        for ctx in reversed(getattr(e, "context", [])):
            print(f"  -> {ctx}")


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. Custom Exception Hierarchy")
    for exc in [
        ValidationError("email", "Invalid format"),
        NotFoundError("User", 42),
        AuthenticationError("Token expired"),
        PermissionDeniedError("delete", "admin_panel"),
        RateLimitError(100, "1 minute"),
    ]:
        print(f"  {exc}")

    separator("2. Exception Chaining")
    demonstrate_chaining()

    separator("3. Try/Except/Else/Finally")
    process_order(1, [{"name": "Widget", "price": 29.99, "qty": 2}])
    process_order(2, [])
    process_order(3, [{"name": "Free Item", "price": 0, "qty": 1}])
    process_order(999, [{"name": "Widget", "price": 10, "qty": 1}])

    separator("4. Collected Validation Errors")
    # Bad data
    try:
        validate_user({"name": "", "email": "bad", "age": -5, "password": "abc"})
    except ValidationErrors as e:
        print(e)
    
    # Good data
    print()
    result = validate_user({
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "password": "Secure123",
    })
    print(f"Valid user: {result}")

    separator("5. Retry with Backoff")
    attempt_count = 0
    def flaky_operation():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise RetryableError(f"Temporary failure (attempt {attempt_count})")
        return "Success!"
    
    try:
        result = retry_with_backoff(flaky_operation, max_retries=5)
        print(f"  Result: {result}")
    except MaxRetriesExceeded as e:
        print(f"  Failed: {e}")

    separator("6. Contextual Errors")
    demonstrate_contextual_errors()


if __name__ == "__main__":
    main()
