"""
API Client - HTTP API client utilities.
Features: REST API client, authentication, retry logic, and response handling.
"""

from typing import Optional, Dict, Any, List
import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class APIClient:
    """Simple REST API client."""
    
    def __init__(self, base_url: str, default_headers: Dict[str, str] = None) -> None:
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API
            default_headers: Default headers for all requests
        """
        self.base_url = base_url.rstrip('/')
        self.default_headers = default_headers or {}
        self.session_headers = {}
    
    def set_auth(self, auth_type: str, credentials: str) -> None:
        """
        Set authentication credentials.
        
        Args:
            auth_type: Type of auth ('bearer', 'basic')
            credentials: Credentials string
        """
        if auth_type == 'bearer':
            self.session_headers['Authorization'] = f'Bearer {credentials}'
        elif auth_type == 'basic':
            self.session_headers['Authorization'] = f'Basic {credentials}'
    
    def set_header(self, key: str, value: str) -> None:
        """
        Set session header.
        
        Args:
            key: Header name
            value: Header value
        """
        self.session_headers[key] = value
    
    def _make_request(self, method: str, endpoint: str, 
                     data: Any = None, params: Dict[str, str] = None,
                     headers: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response dictionary or None
        """
        # Build URL
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        if params:
            from urllib.parse import urlencode
            url += '?' + urlencode(params)
        
        # Prepare headers
        request_headers = {**self.default_headers, **self.session_headers}
        if headers:
            request_headers.update(headers)
        
        # Prepare body
        body = None
        if data:
            body = json.dumps(data).encode('utf-8')
            request_headers['Content-Type'] = 'application/json'
        
        # Make request
        try:
            req = Request(url, data=body, headers=request_headers, method=method)
            with urlopen(req) as response:
                response_data = response.read().decode('utf-8')
                
                try:
                    body = json.loads(response_data)
                except json.JSONDecodeError:
                    body = response_data
                
                return {
                    'status': response.status,
                    'headers': dict(response.headers),
                    'body': body
                }
        except HTTPError as e:
            return {
                'status': e.code,
                'error': str(e),
                'body': e.read().decode('utf-8') if e.read() else None
            }
        except URLError as e:
            return {
                'status': None,
                'error': str(e),
                'body': None
            }
    
    def get(self, endpoint: str, params: Dict[str, str] = None,
            headers: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """
        Perform GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response dictionary
        """
        return self._make_request('GET', endpoint, params=params, headers=headers)
    
    def post(self, endpoint: str, data: Any = None,
             headers: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """
        Perform POST request.
        
        Args:
            endpoint: API endpoint
            data: Request body data
            headers: Additional headers
            
        Returns:
            Response dictionary
        """
        return self._make_request('POST', endpoint, data=data, headers=headers)
    
    def put(self, endpoint: str, data: Any = None,
            headers: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """
        Perform PUT request.
        
        Args:
            endpoint: API endpoint
            data: Request body data
            headers: Additional headers
            
        Returns:
            Response dictionary
        """
        return self._make_request('PUT', endpoint, data=data, headers=headers)
    
    def delete(self, endpoint: str, headers: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """
        Perform DELETE request.
        
        Args:
            endpoint: API endpoint
            headers: Additional headers
            
        Returns:
            Response dictionary
        """
        return self._make_request('DELETE', endpoint, headers=headers)
    
    def patch(self, endpoint: str, data: Any = None,
              headers: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """
        Perform PATCH request.
        
        Args:
            endpoint: API endpoint
            data: Request body data
            headers: Additional headers
            
        Returns:
            Response dictionary
        """
        return self._make_request('PATCH', endpoint, data=data, headers=headers)


class RetryableAPIClient(APIClient):
    """API client with retry logic."""
    
    def __init__(self, base_url: str, max_retries: int = 3,
                 retry_delay: float = 1.0, backoff_factor: float = 2.0,
                 default_headers: Dict[str, str] = None) -> None:
        """
        Initialize retryable API client.
        
        Args:
            base_url: Base URL for API
            max_retries: Maximum number of retries
            retry_delay: Initial delay between retries
            backoff_factor: Multiplier for exponential backoff
            default_headers: Default headers
        """
        super().__init__(base_url, default_headers)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.backoff_factor = backoff_factor
    
    def _make_request(self, method: str, endpoint: str,
                     data: Any = None, params: Dict[str, str] = None,
                     headers: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request with retry logic.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response dictionary or None
        """
        last_error = None
        delay = self.retry_delay
        
        for attempt in range(self.max_retries + 1):
            response = super()._make_request(method, endpoint, data, params, headers)
            
            # Check if request succeeded
            if response and response.get('status') and 200 <= response['status'] < 300:
                return response
            
            # Check if error is retryable
            if response and response.get('status'):
                status = response['status']
                if status not in [429, 500, 502, 503, 504]:
                    return response  # Don't retry client errors
            
            last_error = response
            if attempt < self.max_retries:
                time.sleep(delay)
                delay *= self.backoff_factor
        
        return last_error


class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, calls_per_second: float) -> None:
        """
        Initialize rate limiter.
        
        Args:
            calls_per_second: Maximum calls per second
        """
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0
    
    def wait(self) -> None:
        """Wait if necessary to respect rate limit."""
        now = time.time()
        elapsed = now - self.last_call
        
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        
        self.last_call = time.time()


class RateLimitedAPIClient(APIClient):
    """API client with rate limiting."""
    
    def __init__(self, base_url: str, calls_per_second: float = 10.0,
                 default_headers: Dict[str, str] = None) -> None:
        """
        Initialize rate-limited API client.
        
        Args:
            base_url: Base URL for API
            calls_per_second: Maximum calls per second
            default_headers: Default headers
        """
        super().__init__(base_url, default_headers)
        self.rate_limiter = RateLimiter(calls_per_second)
    
    def _make_request(self, method: str, endpoint: str,
                     data: Any = None, params: Dict[str, str] = None,
                     headers: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request with rate limiting.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response dictionary or None
        """
        self.rate_limiter.wait()
        return super()._make_request(method, endpoint, data, params, headers)


class ResponseParser:
    """Response parsing utilities."""
    
    @staticmethod
    def extract_field(response: Dict[str, Any], field_path: str) -> Any:
        """
        Extract field from response using dot notation.
        
        Args:
            response: Response dictionary
            field_path: Dot-separated field path
            
        Returns:
            Field value or None
        """
        if not response:
            return None
        
        body = response.get('body')
        if not body or not isinstance(body, dict):
            return None
        
        fields = field_path.split('.')
        value = body
        
        for field in fields:
            if isinstance(value, dict) and field in value:
                value = value[field]
            else:
                return None
        
        return value
    
    @staticmethod
    def extract_list(response: Dict[str, Any], field_path: str) -> List:
        """
        Extract list from response.
        
        Args:
            response: Response dictionary
            field_path: Dot-separated field path
            
        Returns:
            List or empty list
        """
        value = ResponseParser.extract_field(response, field_path)
        return value if isinstance(value, list) else []
    
    @staticmethod
    def is_success(response: Dict[str, Any]) -> bool:
        """
        Check if response indicates success.
        
        Args:
            response: Response dictionary
            
        Returns:
            True if successful
        """
        if not response:
            return False
        
        status = response.get('status')
        return status and 200 <= status < 300
    
    @staticmethod
    def get_error_message(response: Dict[str, Any]) -> Optional[str]:
        """
        Extract error message from response.
        
        Args:
            response: Response dictionary
            
        Returns:
            Error message or None
        """
        if not response:
            return None
        
        # Try common error fields
        body = response.get('body')
        if isinstance(body, dict):
            for field in ['error', 'message', 'detail', 'error_message']:
                if field in body:
                    return str(body[field])
        
        # Fallback to error field
        if 'error' in response:
            return str(response['error'])
        
        return None


class APIUtils:
    """General API utility functions."""
    
    @staticmethod
    def build_query_string(params: Dict[str, Any]) -> str:
        """
        Build query string from parameters.
        
        Args:
            params: Parameter dictionary
            
        Returns:
            Query string
        """
        from urllib.parse import urlencode
        return urlencode({k: v for k, v in params.items() if v is not None})
    
    @staticmethod
    def parse_query_string(query: str) -> Dict[str, str]:
        """
        Parse query string into dictionary.
        
        Args:
            query: Query string
            
        Returns:
            Parameter dictionary
        """
        from urllib.parse import parse_qs
        parsed = parse_qs(query)
        return {k: v[0] if v else '' for k, v in parsed.items()}
    
    @staticmethod
    def join_url(base: str, *parts: str) -> str:
        """
        Join URL parts.
        
        Args:
            base: Base URL
            *parts: URL parts to join
            
        Returns:
            Complete URL
        """
        from urllib.parse import urljoin
        url = base.rstrip('/')
        
        for part in parts:
            url = urljoin(url + '/', part.lstrip('/'))
        
        return url


def main() -> None:
    """Demonstrate API client utilities."""
    
    print("=== API Client Demo ===")
    
    # Basic API client
    print("\n--- Basic API Client ---")
    client = APIClient("https://api.example.com")
    client.set_header("User-Agent", "MyApp/1.0")
    
    print(f"Base URL: {client.base_url}")
    print(f"Headers: {client.session_headers}")
    
    # Retryable client
    print("\n--- Retryable Client ---")
    retry_client = RetryableAPIClient(
        "https://api.example.com",
        max_retries=3,
        retry_delay=1.0
    )
    print(f"Max retries: {retry_client.max_retries}")
    print(f"Retry delay: {retry_client.retry_delay}")
    
    # Rate-limited client
    print("\n--- Rate-Limited Client ---")
    rate_client = RateLimitedAPIClient(
        "https://api.example.com",
        calls_per_second=5.0
    )
    print(f"Calls per second: {1.0 / rate_client.rate_limiter.min_interval}")
    
    # Response parsing
    print("\n--- Response Parsing ---")
    response = {
        'status': 200,
        'body': {
            'data': {
                'user': {
                    'name': 'John',
                    'email': 'john@example.com'
                }
            }
        }
    }
    
    print(f"Is success: {ResponseParser.is_success(response)}")
    print(f"Extract name: {ResponseParser.extract_field(response, 'data.user.name')}")
    print(f"Extract list: {ResponseParser.extract_list(response, 'data')}")
    
    # Query string
    print("\n--- Query String ---")
    params = {'page': 1, 'limit': 10, 'sort': 'name'}
    query = APIUtils.build_query_string(params)
    print(f"Query string: {query}")
    
    parsed = APIUtils.parse_query_string(query)
    print(f"Parsed: {parsed}")
    
    # URL joining
    print("\n--- URL Joining ---")
    url = APIUtils.join_url("https://api.example.com", "v1", "users", "123")
    print(f"Joined URL: {url}")


if __name__ == "__main__":
    main()
