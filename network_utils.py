"""
Network Utilities - Network programming and HTTP operations.
Features: HTTP requests, URL parsing, and network utilities.
"""

import socket
import urllib.parse
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
import json


@dataclass
class URLComponents:
    """Parsed URL components."""
    scheme: str
    netloc: str
    path: str
    params: str
    query: str
    fragment: str


class NetworkUtils:
    """Utility class for network operations."""
    
    @staticmethod
    def parse_url(url: str) -> URLComponents:
        """
        Parse URL into components.
        
        Args:
            url: URL string to parse
            
        Returns:
            URLComponents object with parsed data
        """
        parsed = urllib.parse.urlparse(url)
        return URLComponents(
            scheme=parsed.scheme,
            netloc=parsed.netloc,
            path=parsed.path,
            params=parsed.params,
            query=parsed.query,
            fragment=parsed.fragment
        )
    
    @staticmethod
    def build_url(scheme: str, netloc: str, path: str = "", 
                  params: str = "", query: str = "", fragment: str = "") -> str:
        """
        Build URL from components.
        
        Args:
            scheme: URL scheme (http, https, etc.)
            netloc: Network location (domain)
            path: URL path
            params: URL parameters
            query: Query string
            fragment: Fragment identifier
            
        Returns:
            Complete URL string
        """
        return urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))
    
    @staticmethod
    def encode_query(params: Dict[str, str]) -> str:
        """
        Encode dictionary to query string.
        
        Args:
            params: Dictionary of query parameters
            
        Returns:
            Encoded query string
        """
        return urllib.parse.urlencode(params)
    
    @staticmethod
    def decode_query(query_string: str) -> Dict[str, str]:
        """
        Decode query string to dictionary.
        
        Args:
            query_string: Query string to decode
            
        Returns:
            Dictionary of parameters
        """
        return dict(urllib.parse.parse_qsl(query_string))
    
    @staticmethod
    def get_host_by_ip(ip: str) -> Optional[str]:
        """
        Get hostname from IP address.
        
        Args:
            ip: IP address string
            
        Returns:
            Hostname, or None if lookup fails
        """
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return None
    
    @staticmethod
    def get_ip_by_host(hostname: str) -> Optional[str]:
        """
        Get IP address from hostname.
        
        Args:
            hostname: Hostname to resolve
            
        Returns:
            IP address, or None if resolution fails
        """
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None
    
    @staticmethod
    def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
        """
        Check if a port is open on a host.
        
        Args:
            host: Host address
            port: Port number to check
            timeout: Connection timeout in seconds
            
        Returns:
            True if port is open, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except (socket.error, socket.timeout):
            return False
    
    @staticmethod
    def get_local_ip() -> Optional[str]:
        """
        Get local IP address.
        
        Returns:
            Local IP address, or None if unable to determine
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except socket.error:
            return None
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """
        Validate IP address format.
        
        Args:
            ip: IP address string to validate
            
        Returns:
            True if valid IP, False otherwise
        """
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
    
    @staticmethod
    def is_valid_ipv6(ip: str) -> bool:
        """
        Validate IPv6 address format.
        
        Args:
            ip: IPv6 address string to validate
            
        Returns:
            True if valid IPv6, False otherwise
        """
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            return True
        except socket.error:
            return False
    
    @staticmethod
    def ping_host(host: str, timeout: float = 2.0) -> bool:
        """
        Simulate ping by attempting to connect to port 80.
        Note: This is not a true ICMP ping.
        
        Args:
            host: Host to ping
            timeout: Timeout in seconds
            
        Returns:
            True if host is reachable, False otherwise
        """
        return NetworkUtils.check_port(host, 80, timeout)


class HTTPRequestBuilder:
    """Builder for HTTP requests."""
    
    def __init__(self) -> None:
        """Initialize HTTP request builder."""
        self.method = "GET"
        self.headers: Dict[str, str] = {}
        self.body: Optional[str] = None
    
    def set_method(self, method: str) -> 'HTTPRequestBuilder':
        """Set HTTP method."""
        self.method = method
        return self
    
    def set_header(self, key: str, value: str) -> 'HTTPRequestBuilder':
        """Set HTTP header."""
        self.headers[key] = value
        return self
    
    def set_headers(self, headers: Dict[str, str]) -> 'HTTPRequestBuilder':
        """Set multiple HTTP headers."""
        self.headers.update(headers)
        return self
    
    def set_body(self, body: str) -> 'HTTPRequestBuilder':
        """Set request body."""
        self.body = body
        return self
    
    def set_json_body(self, data: Dict) -> 'HTTPRequestBuilder':
        """Set JSON body from dictionary."""
        self.body = json.dumps(data)
        self.headers["Content-Type"] = "application/json"
        return self
    
    def build(self) -> str:
        """Build HTTP request string."""
        request_lines = [f"{self.method} / HTTP/1.1"]
        
        for key, value in self.headers.items():
            request_lines.append(f"{key}: {value}")
        
        request_lines.append("")  # Empty line before body
        
        if self.body:
            request_lines.append(self.body)
        
        return "\r\n".join(request_lines)


class CookieManager:
    """Simple cookie manager for HTTP requests."""
    
    def __init__(self) -> None:
        """Initialize cookie manager."""
        self.cookies: Dict[str, str] = {}
    
    def set_cookie(self, name: str, value: str) -> None:
        """Set a cookie."""
        self.cookies[name] = value
    
    def get_cookie(self, name: str) -> Optional[str]:
        """Get a cookie value."""
        return self.cookies.get(name)
    
    def delete_cookie(self, name: str) -> None:
        """Delete a cookie."""
        self.cookies.pop(name, None)
    
    def get_cookie_header(self) -> str:
        """Get Cookie header string."""
        return "; ".join(f"{k}={v}" for k, v in self.cookies.items())
    
    def parse_set_cookie(self, set_cookie_header: str) -> None:
        """Parse Set-Cookie header and store cookie."""
        # Simple parsing - extract name=value
        parts = set_cookie_header.split(";")
        if parts:
            name_value = parts[0].strip()
            if "=" in name_value:
                name, value = name_value.split("=", 1)
                self.set_cookie(name.strip(), value.strip())
    
    def clear_all(self) -> None:
        """Clear all cookies."""
        self.cookies.clear()


def main() -> None:
    """Demonstrate network utilities."""
    
    utils = NetworkUtils()
    
    print("=== URL Parsing ===")
    url = "https://example.com/path?param1=value1&param2=value2#section"
    components = utils.parse_url(url)
    print(f"URL: {url}")
    print(f"Scheme: {components.scheme}")
    print(f"Netloc: {components.netloc}")
    print(f"Path: {components.path}")
    print(f"Query: {components.query}")
    print(f"Fragment: {components.fragment}")
    
    print("\n=== URL Building ===")
    built_url = utils.build_url(
        scheme="https",
        netloc="api.example.com",
        path="/users",
        query="page=1&limit=10"
    )
    print(f"Built URL: {built_url}")
    
    print("\n=== Query Encoding/Decoding ===")
    params = {"name": "John Doe", "age": "30", "city": "New York"}
    encoded = utils.encode_query(params)
    print(f"Encoded: {encoded}")
    decoded = utils.decode_query(encoded)
    print(f"Decoded: {decoded}")
    
    print("\n=== IP/Host Resolution ===")
    host = "google.com"
    ip = utils.get_ip_by_host(host)
    print(f"IP of {host}: {ip}")
    
    if ip:
        hostname = utils.get_host_by_ip(ip)
        print(f"Hostname of {ip}: {hostname}")
    
    print(f"\nLocal IP: {utils.get_local_ip()}")
    
    print("\n=== IP Validation ===")
    test_ips = ["192.168.1.1", "256.1.1.1", "2001:0db8:85a3::8a2e:0370:7334"]
    for ip in test_ips:
        ipv4_valid = utils.is_valid_ip(ip)
        ipv6_valid = utils.is_valid_ipv6(ip)
        print(f"{ip}: IPv4={ipv4_valid}, IPv6={ipv6_valid}")
    
    print("\n=== HTTP Request Builder ===")
    request = (HTTPRequestBuilder()
               .set_method("POST")
               .set_header("Host", "api.example.com")
               .set_header("User-Agent", "MyApp/1.0")
               .set_json_body({"name": "Alice", "age": 25})
               .build())
    print("HTTP Request:")
    print(request)
    
    print("\n=== Cookie Manager ===")
    manager = CookieManager()
    manager.set_cookie("session_id", "abc123")
    manager.set_cookie("user_pref", "dark_mode")
    print(f"Cookie header: {manager.get_cookie_header()}")
    print(f"Session ID: {manager.get_cookie('session_id')}")
    
    manager.parse_set_cookie("token=xyz789; Path=/; HttpOnly")
    print(f"After parsing Set-Cookie: {manager.get_cookie_header()}")
    
    manager.delete_cookie("session_id")
    print(f"After deleting session_id: {manager.get_cookie_header()}")


if __name__ == "__main__":
    main()
