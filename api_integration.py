"""
API Integration Module

This module provides comprehensive API integration utilities including:
- REST API client with authentication
- GraphQL client
- WebSocket client
- Rate limiting and retry logic
- Request/response logging
- Error handling and validation
- Pagination handling
- Webhook handling
- API testing utilities
- Mock API server

All functions include comprehensive docstrings and type hints.
"""

import json
import time
import hashlib
import hmac
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import urllib.parse


try:
    import requests
    from requests.adapters import HTTPAdapter
    from requests.exceptions import RequestException
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False


class HTTPMethod(Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class AuthType(Enum):
    """Authentication types."""
    NONE = "none"
    BASIC = "basic"
    BEARER = "bearer"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    CUSTOM = "custom"


@dataclass
class APIResponse:
    """Container for API response."""
    status_code: int
    data: Any
    headers: Dict[str, str]
    elapsed_time: float
    success: bool
    error_message: Optional[str] = None


@dataclass
class APIConfig:
    """API configuration."""
    base_url: str
    timeout: int = 30
    auth_type: AuthType = AuthType.NONE
    api_key: Optional[str] = None
    api_key_header: str = "X-API-Key"
    username: Optional[str] = None
    password: Optional[str] = None
    bearer_token: Optional[str] = None
    default_headers: Dict[str, str] = None
    verify_ssl: bool = True
    max_retries: int = 3
    retry_delay: float = 1.0


class RateLimiter:
    """Rate limiting for API requests."""
    
    def __init__(self, max_requests: int, time_window: float):
        """Initialize rate limiter."""
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def wait_if_needed(self) -> None:
        """Wait if rate limit would be exceeded."""
        now = time.time()
        
        # Remove old requests outside time window
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < self.time_window]
        
        # Wait if we've hit the limit
        if len(self.requests) >= self.max_requests:
            oldest_request = min(self.requests)
            wait_time = self.time_window - (now - oldest_request)
            if wait_time > 0:
                time.sleep(wait_time)
    
    def record_request(self) -> None:
        """Record a request."""
        self.requests.append(time.time())


class RESTClient:
    """REST API client with authentication and retry logic."""
    
    def __init__(self, config: APIConfig):
        """Initialize REST client."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required. Install with: pip install requests")
        
        self.config = config
        self.session = requests.Session()
        self.rate_limiter: Optional[RateLimiter] = None
        
        # Configure session
        if config.max_retries > 0:
            adapter = HTTPAdapter(max_retries=config.max_retries)
            self.session.mount('http://', adapter)
            self.session.mount('https://', adapter)
        
        # Set default headers
        if config.default_headers:
            self.session.headers.update(config.default_headers)
        
        # Configure authentication
        self._configure_auth()
    
    def _configure_auth(self) -> None:
        """Configure authentication based on config."""
        if self.config.auth_type == AuthType.BASIC:
            if self.config.username and self.config.password:
                self.session.auth = (self.config.username, self.config.password)
        
        elif self.config.auth_type == AuthType.BEARER:
            if self.config.bearer_token:
                self.session.headers['Authorization'] = f"Bearer {self.config.bearer_token}"
        
        elif self.config.auth_type == AuthType.API_KEY:
            if self.config.api_key:
                self.session.headers[self.config.api_key_header] = self.config.api_key
    
    def set_rate_limiter(self, max_requests: int, time_window: float) -> None:
        """Set rate limiter."""
        self.rate_limiter = RateLimiter(max_requests, time_window)
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        base_url = self.config.base_url.rstrip('/')
        endpoint = endpoint.lstrip('/')
        return f"{base_url}/{endpoint}"
    
    def _make_request(self, method: HTTPMethod, endpoint: str,
                     params: Optional[Dict] = None,
                     data: Optional[Dict] = None,
                     json_data: Optional[Dict] = None,
                     headers: Optional[Dict] = None) -> APIResponse:
        """Make HTTP request with retry logic."""
        if self.rate_limiter:
            self.rate_limiter.wait_if_needed()
        
        url = self._build_url(endpoint)
        request_headers = self.session.headers.copy()
        
        if headers:
            request_headers.update(headers)
        
        start_time = time.time()
        
        try:
            response = self.session.request(
                method=method.value,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=request_headers,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            elapsed_time = time.time() - start_time
            
            if self.rate_limiter:
                self.rate_limiter.record_request()
            
            # Parse response
            try:
                response_data = response.json()
            except:
                response_data = response.text
            
            return APIResponse(
                status_code=response.status_code,
                data=response_data,
                headers=dict(response.headers),
                elapsed_time=elapsed_time,
                success=response.status_code < 400
            )
            
        except RequestException as e:
            elapsed_time = time.time() - start_time
            return APIResponse(
                status_code=0,
                data=None,
                headers={},
                elapsed_time=elapsed_time,
                success=False,
                error_message=str(e)
            )
    
    def get(self, endpoint: str, params: Optional[Dict] = None,
           headers: Optional[Dict] = None) -> APIResponse:
        """Make GET request."""
        return self._make_request(HTTPMethod.GET, endpoint, params=params, headers=headers)
    
    def post(self, endpoint: str, data: Optional[Dict] = None,
            json_data: Optional[Dict] = None,
            headers: Optional[Dict] = None) -> APIResponse:
        """Make POST request."""
        return self._make_request(HTTPMethod.POST, endpoint, data=data, 
                                 json_data=json_data, headers=headers)
    
    def put(self, endpoint: str, data: Optional[Dict] = None,
           json_data: Optional[Dict] = None,
           headers: Optional[Dict] = None) -> APIResponse:
        """Make PUT request."""
        return self._make_request(HTTPMethod.PUT, endpoint, data=data,
                                 json_data=json_data, headers=headers)
    
    def delete(self, endpoint: str, params: Optional[Dict] = None,
              headers: Optional[Dict] = None) -> APIResponse:
        """Make DELETE request."""
        return self._make_request(HTTPMethod.DELETE, endpoint, params=params, headers=headers)
    
    def patch(self, endpoint: str, data: Optional[Dict] = None,
             json_data: Optional[Dict] = None,
             headers: Optional[Dict] = None) -> APIResponse:
        """Make PATCH request."""
        return self._make_request(HTTPMethod.PATCH, endpoint, data=data,
                                 json_data=json_data, headers=headers)
    
    def close(self) -> None:
        """Close the session."""
        self.session.close()


class GraphQLClient:
    """GraphQL client for API integration."""
    
    def __init__(self, base_url: str, headers: Optional[Dict] = None):
        """Initialize GraphQL client."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required. Install with: pip install requests")
        
        self.base_url = base_url
        self.headers = headers or {}
        self.session = requests.Session()
    
    def query(self, query: str, variables: Optional[Dict] = None,
             operation_name: Optional[str] = None) -> APIResponse:
        """Execute GraphQL query."""
        payload = {
            "query": query,
            "variables": variables or {}
        }
        
        if operation_name:
            payload["operationName"] = operation_name
        
        start_time = time.time()
        
        try:
            response = self.session.post(
                self.base_url,
                json=payload,
                headers=self.headers
            )
            
            elapsed_time = time.time() - start_time
            
            response_data = response.json()
            
            # Check for GraphQL errors
            if "errors" in response_data:
                return APIResponse(
                    status_code=response.status_code,
                    data=response_data,
                    headers=dict(response.headers),
                    elapsed_time=elapsed_time,
                    success=False,
                    error_message=str(response_data["errors"])
                )
            
            return APIResponse(
                status_code=response.status_code,
                data=response_data,
                headers=dict(response.headers),
                elapsed_time=elapsed_time,
                success=response.status_code < 400
            )
            
        except RequestException as e:
            elapsed_time = time.time() - start_time
            return APIResponse(
                status_code=0,
                data=None,
                headers={},
                elapsed_time=elapsed_time,
                success=False,
                error_message=str(e)
            )
    
    def mutate(self, mutation: str, variables: Optional[Dict] = None) -> APIResponse:
        """Execute GraphQL mutation."""
        return self.query(mutation, variables)
    
    def close(self) -> None:
        """Close the session."""
        self.session.close()


class WebSocketClient:
    """WebSocket client for real-time communication."""
    
    def __init__(self, url: str):
        """Initialize WebSocket client."""
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError("websockets library is required. Install with: pip install websockets")
        
        self.url = url
        self.connection = None
    
    async def connect(self) -> bool:
        """Connect to WebSocket server."""
        try:
            self.connection = await websockets.connect(self.url)
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    async def send(self, message: Union[str, Dict]) -> bool:
        """Send message to WebSocket server."""
        if not self.connection:
            return False
        
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            
            await self.connection.send(message)
            return True
        except Exception as e:
            print(f"Send failed: {e}")
            return False
    
    async def receive(self) -> Optional[str]:
        """Receive message from WebSocket server."""
        if not self.connection:
            return None
        
        try:
            message = await self.connection.recv()
            return message
        except Exception as e:
            print(f"Receive failed: {e}")
            return None
    
    async def close(self) -> None:
        """Close WebSocket connection."""
        if self.connection:
            await self.connection.close()
            self.connection = None


class WebhookHandler:
    """Webhook handling utilities."""
    
    @staticmethod
    def verify_signature(payload: bytes, signature: str, 
                        secret: str, algorithm: str = "sha256") -> bool:
        """Verify webhook signature."""
        expected_signature = hmac.new(
            secret.encode(),
            payload,
            getattr(hashlib, algorithm)
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    
    @staticmethod
    def parse_webhook_data(raw_data: bytes) -> Dict[str, Any]:
        """Parse webhook data."""
        try:
            return json.loads(raw_data.decode())
        except json.JSONDecodeError:
            return {"raw_data": raw_data.decode()}
    
    @staticmethod
    def create_webhook_response(status_code: int = 200,
                               message: str = "OK") -> Dict[str, Any]:
        """Create webhook response."""
        return {
            "status": status_code,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }


class PaginationHandler:
    """Pagination handling for API responses."""
    
    @staticmethod
    def paginate_next(response: APIResponse, 
                     next_url_field: str = "next") -> Optional[str]:
        """Extract next page URL from response."""
        if response.success and isinstance(response.data, dict):
            return response.data.get(next_url_field)
        return None
    
    @staticmethod
    def paginate_offset(response: APIResponse,
                       offset_field: str = "offset",
                       limit_field: str = "limit") -> Tuple[int, int]:
        """Extract offset and limit from response."""
        if response.success and isinstance(response.data, dict):
            offset = response.data.get(offset_field, 0)
            limit = response.data.get(limit_field, 10)
            return offset, limit
        return 0, 10
    
    @staticmethod
    def paginate_cursor(response: APIResponse,
                       cursor_field: str = "cursor") -> Optional[str]:
        """Extract cursor from response."""
        if response.success and isinstance(response.data, dict):
            return response.data.get(cursor_field)
        return None


class APIValidator:
    """API response validation."""
    
    @staticmethod
    def validate_status_code(response: APIResponse, 
                            expected_codes: List[int]) -> bool:
        """Validate response status code."""
        return response.status_code in expected_codes
    
    @staticmethod
    def validate_response_structure(response: APIResponse,
                                    required_fields: List[str]) -> bool:
        """Validate response has required fields."""
        if not response.success or not isinstance(response.data, dict):
            return False
        
        return all(field in response.data for field in required_fields)
    
    @staticmethod
    def validate_data_type(response: APIResponse,
                          field: str,
                          expected_type: type) -> bool:
        """Validate field has expected type."""
        if not response.success or not isinstance(response.data, dict):
            return False
        
        if field not in response.data:
            return False
        
        return isinstance(response.data[field], expected_type)
    
    @staticmethod
    def validate_schema(response: APIResponse,
                       schema: Dict[str, type]) -> bool:
        """Validate response against schema."""
        if not response.success or not isinstance(response.data, dict):
            return False
        
        for field, expected_type in schema.items():
            if field not in response.data:
                return False
            if not isinstance(response.data[field], expected_type):
                return False
        
        return True


class APILogger:
    """API request/response logging."""
    
    def __init__(self, log_file: Optional[str] = None):
        """Initialize API logger."""
        self.log_file = log_file
        self.logs: List[Dict] = []
    
    def log_request(self, method: str, url: str, 
                    params: Optional[Dict] = None,
                    data: Optional[Dict] = None) -> None:
        """Log API request."""
        log_entry = {
            "type": "request",
            "method": method,
            "url": url,
            "params": params,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logs.append(log_entry)
        
        if self.log_file:
            self._write_to_file(log_entry)
    
    def log_response(self, response: APIResponse) -> None:
        """Log API response."""
        log_entry = {
            "type": "response",
            "status_code": response.status_code,
            "success": response.success,
            "elapsed_time": response.elapsed_time,
            "error_message": response.error_message,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logs.append(log_entry)
        
        if self.log_file:
            self._write_to_file(log_entry)
    
    def _write_to_file(self, log_entry: Dict) -> None:
        """Write log entry to file."""
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_logs(self, log_type: Optional[str] = None) -> List[Dict]:
        """Get logs, optionally filtered by type."""
        if log_type:
            return [log for log in self.logs if log["type"] == log_type]
        return self.logs


class MockAPIServer:
    """Mock API server for testing."""
    
    def __init__(self):
        """Initialize mock API server."""
        self.endpoints: Dict[str, Callable] = {}
        self.request_log: List[Dict] = []
    
    def add_endpoint(self, path: str, handler: Callable) -> None:
        """Add endpoint handler."""
        self.endpoints[path] = handler
    
    def handle_request(self, method: str, path: str,
                      params: Optional[Dict] = None,
                      data: Optional[Dict] = None) -> APIResponse:
        """Handle incoming request."""
        # Log request
        self.request_log.append({
            "method": method,
            "path": path,
            "params": params,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        
        # Find matching endpoint
        handler = self.endpoints.get(path)
        
        if handler:
            try:
                response_data = handler(method, params, data)
                return APIResponse(
                    status_code=200,
                    data=response_data,
                    headers={},
                    elapsed_time=0.0,
                    success=True
                )
            except Exception as e:
                return APIResponse(
                    status_code=500,
                    data={"error": str(e)},
                    headers={},
                    elapsed_time=0.0,
                    success=False,
                    error_message=str(e)
                )
        
        return APIResponse(
            status_code=404,
            data={"error": "Endpoint not found"},
            headers={},
            elapsed_time=0.0,
            success=False,
            error_message="Endpoint not found"
        )
    
    def get_request_log(self) -> List[Dict]:
        """Get request log."""
        return self.request_log
    
    def clear_log(self) -> None:
        """Clear request log."""
        self.request_log.clear()


class APIBuilder:
    """API URL and query builder utilities."""
    
    @staticmethod
    def build_url(base_url: str, path: str, 
                 params: Optional[Dict] = None) -> str:
        """Build complete URL with query parameters."""
        url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
        
        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"
        
        return url
    
    @staticmethod
    def build_query_string(params: Dict) -> str:
        """Build query string from parameters."""
        return urllib.parse.urlencode(params)
    
    @staticmethod
    def parse_query_string(query_string: str) -> Dict[str, str]:
        """Parse query string into dictionary."""
        return dict(urllib.parse.parse_qsl(query_string))
    
    @staticmethod
    def join_url(base_url: str, *parts: str) -> str:
        """Join URL parts safely."""
        url = base_url.rstrip('/')
        for part in parts:
            url = f"{url}/{part.lstrip('/')}"
        return url


def demonstrate_api_integration():
    """Demonstrate API integration functionality."""
    print("=== API Integration Demonstration ===\n")
    
    if not REQUESTS_AVAILABLE:
        print("requests library is required. Install with: pip install requests")
        return
    
    # API Configuration
    print("1. API Configuration:")
    config = APIConfig(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=10,
        auth_type=AuthType.NONE,
        max_retries=3
    )
    print(f"   Base URL: {config.base_url}")
    print(f"   Timeout: {config.timeout}s")
    print(f"   Max retries: {config.max_retries}")
    
    # REST Client
    print("\n2. REST Client:")
    client = RESTClient(config)
    
    # Make GET request
    print("   Making GET request to /posts/1...")
    response = client.get("/posts/1")
    print(f"   Status: {response.status_code}")
    print(f"   Success: {response.success}")
    print(f"   Time: {response.elapsed_time:.4f}s")
    if response.success:
        print(f"   Data keys: {list(response.data.keys()) if isinstance(response.data, dict) else 'N/A'}")
    
    # Rate Limiter
    print("\n3. Rate Limiting:")
    client.set_rate_limiter(max_requests=5, time_window=1.0)
    print("   Rate limiter set: 5 requests per second")
    
    # API Builder
    print("\n4. API URL Building:")
    url = APIBuilder.build_url("https://api.example.com", "users", 
                              {"page": 1, "limit": 10})
    print(f"   Built URL: {url}")
    
    query_string = APIBuilder.build_query_string({"search": "python", "sort": "desc"})
    print(f"   Query string: {query_string}")
    
    # GraphQL Client
    print("\n5. GraphQL Client:")
    graphql_client = GraphQLClient("https://api.example.com/graphql")
    print("   GraphQL client initialized")
    
    # Pagination Handler
    print("\n6. Pagination Handler:")
    mock_response = APIResponse(
        status_code=200,
        data={"next": "https://api.example.com/page2", "offset": 0, "limit": 10},
        headers={},
        elapsed_time=0.1,
        success=True
    )
    
    next_url = PaginationHandler.paginate_next(mock_response)
    print(f"   Next URL: {next_url}")
    
    offset, limit = PaginationHandler.paginate_offset(mock_response)
    print(f"   Offset: {offset}, Limit: {limit}")
    
    # API Validator
    print("\n7. API Validation:")
    is_valid = APIValidator.validate_status_code(mock_response, [200, 201])
    print(f"   Status code valid: {is_valid}")
    
    has_required = APIValidator.validate_response_structure(
        mock_response, ["next", "offset"]
    )
    print(f"   Has required fields: {has_required}")
    
    # Webhook Handler
    print("\n8. Webhook Handler:")
    payload = b'{"event": "user.created", "data": {"id": 123}}'
    signature = WebhookHandler.verify_signature(payload, "test_signature", "secret")
    print(f"   Signature verification: {signature}")
    
    webhook_data = WebhookHandler.parse_webhook_data(payload)
    print(f"   Parsed webhook data: {webhook_data}")
    
    # Mock API Server
    print("\n9. Mock API Server:")
    mock_server = MockAPIServer()
    
    def sample_handler(method, params, data):
        return {"message": "Hello from mock API", "method": method}
    
    mock_server.add_endpoint("/test", sample_handler)
    mock_response = mock_server.handle_request("GET", "/test")
    print(f"   Mock response: {mock_response.data}")
    
    print(f"   Request log count: {len(mock_server.get_request_log())}")
    
    # API Logger
    print("\n10. API Logger:")
    logger = APILogger()
    logger.log_request("GET", "https://api.example.com/users")
    logger.log_response(mock_response)
    
    print(f"   Log entries: {len(logger.get_logs())}")
    
    client.close()
    
    print("\n=== Demonstration Complete ===")
    print("\nAPI Integration Best Practices:")
    print("- Use rate limiting to avoid overwhelming APIs")
    print("- Implement proper error handling and retry logic")
    print("- Validate API responses before processing")
    print("- Use authentication headers properly")
    print("- Log API requests and responses for debugging")
    print("- Handle pagination for large datasets")
    print("- Use webhooks for real-time updates")
    print("- Test with mock servers during development")


if __name__ == "__main__":
    demonstrate_api_integration()