"""
API Client - A robust HTTP client with retry logic and error handling.
Features: Request timeout, exponential backoff, response validation, logging.
"""

import time
import json
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum


class HTTPMethod(Enum):
    """HTTP request methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class HTTPError(Exception):
    """Base exception for HTTP-related errors."""
    pass


class TimeoutError(HTTPError):
    """Exception raised when request times out."""
    pass


class ConnectionError(HTTPError):
    """Exception raised when connection fails."""
    pass


class ValidationError(HTTPError):
    """Exception raised when response validation fails."""
    pass


@dataclass
class Response:
    """Represents an HTTP response."""
    status_code: int
    data: Dict[str, Any]
    headers: Dict[str, str]
    elapsed_time: float

    def is_success(self) -> bool:
        """Check if response indicates success (2xx status code)."""
        return 200 <= self.status_code < 300

    def json(self) -> str:
        """Return response data as JSON string."""
        return json.dumps(self.data, indent=2)


class APIClient:
    """
    A robust API client with retry logic and error handling.
    Simulates HTTP requests for demonstration purposes.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for all requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries (exponential backoff)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.session_headers: Dict[str, str] = {}

    def set_header(self, key: str, value: str) -> None:
        """Set a default header for all requests."""
        self.session_headers[key] = value

    def set_auth_token(self, token: str) -> None:
        """Set authorization token header."""
        self.set_header("Authorization", f"Bearer {token}")

    def _simulate_request(
        self,
        method: HTTPMethod,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Response:
        """
        Simulate an HTTP request (for demonstration).
        In production, replace with requests library or httpx.
        """
        start_time = time.time()
        
        # Simulate network delay
        time.sleep(0.1)
        
        # Simulate response
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Mock response data
        mock_data = {
            "url": url,
            "method": method.value,
            "status": "success",
            "data": data or {},
        }
        
        elapsed = time.time() - start_time
        
        return Response(
            status_code=200,
            data=mock_data,
            headers={"Content-Type": "application/json"},
            elapsed_time=elapsed,
        )

    def _validate_response(
        self,
        response: Response,
        validator: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> None:
        """
        Validate the response data.
        
        Args:
            response: The response to validate
            validator: Optional custom validation function
        """
        if not response.is_success():
            raise ValidationError(f"Request failed with status {response.status_code}")
        
        if validator and not validator(response.data):
            raise ValidationError("Response data validation failed")

    def request(
        self,
        method: HTTPMethod,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        validator: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> Response:
        """
        Make an HTTP request with retry logic.
        
        Args:
            method: HTTP method to use
            endpoint: API endpoint path
            data: Request body data
            validator: Optional response validation function
            
        Returns:
            Response object with the result
            
        Raises:
            HTTPError: If all retry attempts fail
        """
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self._simulate_request(method, endpoint, data)
                self._validate_response(response, validator)
                return response
                
            except (TimeoutError, ConnectionError) as e:
                last_error = e
                if attempt < self.max_retries:
                    delay = self.retry_delay * (2 ** attempt)
                    time.sleep(delay)
                    continue
                raise
                
            except ValidationError as e:
                # Validation errors should not be retried
                raise

        raise HTTPError(f"Request failed after {self.max_retries} retries: {last_error}")

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        validator: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> Response:
        """Make a GET request."""
        return self.request(HTTPMethod.GET, endpoint, params, validator)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        validator: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> Response:
        """Make a POST request."""
        return self.request(HTTPMethod.POST, endpoint, data, validator)


def validate_user_data(data: Dict[str, Any]) -> bool:
    """Example validator for user data responses."""
    required_fields = {"id", "name", "email"}
    return required_fields.issubset(data.keys())


def main() -> None:
    """Demonstrate APIClient functionality."""
    # Initialize client
    client = APIClient(
        base_url="https://api.example.com",
        timeout=10.0,
        max_retries=3,
    )
    
    # Set authentication
    client.set_auth_token("your-api-token-here")
    
    # Make a GET request
    print("Making GET request...")
    response = client.get("/users/123")
    print(f"Status: {response.status_code}")
    print(f"Time: {response.elapsed_time:.3f}s")
    print(f"Data: {response.json()}")
    
    # Make a POST request with validation
    print("\nMaking POST request...")
    user_data = {"name": "John Doe", "email": "john@example.com"}
    response = client.post("/users", data=user_data)
    print(f"Status: {response.status_code}")
    print(f"Data: {response.json()}")


if __name__ == "__main__":
    main()
