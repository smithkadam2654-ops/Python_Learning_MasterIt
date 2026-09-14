"""
Networking Utilities - Network operations and HTTP requests.
Features: HTTP requests, URL handling, socket operations, and network utilities.
"""

from typing import Optional, Dict, Any
import socket
import urllib.request
import urllib.parse
import json
from http.client import HTTPResponse


class HTTPClient:
    """Simple HTTP client implementation."""
    
    @staticmethod
    def get(url: str, headers: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """
        Perform HTTP GET request.
        
        Args:
            url: URL to request
            headers: Optional headers
            
        Returns:
            Response dictionary with status, headers, and body
        """
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req) as response:
                return HTTPClient._parse_response(response)
        except Exception as e:
            print(f"GET request failed: {e}")
            return None
    
    @staticmethod
    def post(url: str, data: Dict[str, Any] = None, 
             headers: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """
        Perform HTTP POST request.
        
        Args:
            url: URL to request
            data: Data to send
            headers: Optional headers
            
        Returns:
            Response dictionary
        """
        try:
            if data:
                data = json.dumps(data).encode('utf-8')
                if headers is None:
                    headers = {}
                headers['Content-Type'] = 'application/json'
            
            req = urllib.request.Request(url, data=data, headers=headers or {}, method='POST')
            with urllib.request.urlopen(req) as response:
                return HTTPClient._parse_response(response)
        except Exception as e:
            print(f"POST request failed: {e}")
            return None
    
    @staticmethod
    def _parse_response(response: HTTPResponse) -> Dict[str, Any]:
        """Parse HTTP response."""
        headers = dict(response.headers)
        
        try:
            body = response.read().decode('utf-8')
            # Try to parse as JSON
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass
        except:
            body = None
        
        return {
            'status': response.status,
            'headers': headers,
            'body': body
        }


class URLUtils:
    """URL manipulation utilities."""
    
    @staticmethod
    def parse_url(url: str) -> Dict[str, str]:
        """
        Parse URL into components.
        
        Args:
            url: URL string
            
        Returns:
            Dictionary with components (scheme, netloc, path, params, query, fragment)
        """
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'path': parsed.path,
            'params': parsed.params,
            'query': parsed.query,
            'fragment': parsed.fragment
        }
    
    @staticmethod
    def build_url(base: str, path: str = '', params: Dict[str, str] = None) -> str:
        """
        Build URL from components.
        
        Args:
            base: Base URL
            path: Path to append
            params: Query parameters
            
        Returns:
            Complete URL
        """
        from urllib.parse import urljoin, urlencode
        
        url = urljoin(base, path)
        
        if params:
            url += '?' + urlencode(params)
        
        return url
    
    @staticmethod
    def encode_url(url: str) -> str:
        """
        URL encode string.
        
        Args:
            url: URL string to encode
            
        Returns:
            Encoded URL
        """
        return urllib.parse.quote(url)
    
    @staticmethod
    def decode_url(url: str) -> str:
        """
        URL decode string.
        
        Args:
            url: URL string to decode
            
        Returns:
            Decoded URL
        """
        return urllib.parse.unquote(url)
    
    @staticmethod
    def parse_query_string(query: str) -> Dict[str, str]:
        """
        Parse query string into dictionary.
        
        Args:
            query: Query string
            
        Returns:
            Dictionary of parameters
        """
        return dict(urllib.parse.parse_qsl(query))
    
    @staticmethod
    def build_query_string(params: Dict[str, str]) -> str:
        """
        Build query string from dictionary.
        
        Args:
            params: Parameter dictionary
            
        Returns:
            Query string
        """
        return urllib.parse.urlencode(params)


class SocketUtils:
    """Socket operation utilities."""
    
    @staticmethod
    def check_port_open(host: str, port: int, timeout: float = 2.0) -> bool:
        """
        Check if port is open on host.
        
        Args:
            host: Host address
            port: Port number
            timeout: Connection timeout
            
        Returns:
            True if port is open
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    @staticmethod
    def get_local_ip() -> Optional[str]:
        """
        Get local IP address.
        
        Returns:
            Local IP address or None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except:
            return None
    
    @staticmethod
    def get_hostname() -> str:
        """
        Get system hostname.
        
        Returns:
            Hostname
        """
        return socket.gethostname()
    
    @staticmethod
    def resolve_hostname(hostname: str) -> Optional[str]:
        """
        Resolve hostname to IP address.
        
        Args:
            hostname: Hostname to resolve
            
        Returns:
            IP address or None
        """
        try:
            return socket.gethostbyname(hostname)
        except:
            return None
    
    @staticmethod
    def reverse_lookup(ip: str) -> Optional[str]:
        """
        Reverse DNS lookup.
        
        Args:
            ip: IP address
            
        Returns:
            Hostname or None
        """
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None


class NetworkUtils:
    """General network utilities."""
    
    @staticmethod
    def ping_host(host: str, timeout: float = 2.0) -> bool:
        """
        Ping host (simplified - uses socket connection).
        
        Args:
            host: Host to ping
            timeout: Timeout in seconds
            
        Returns:
            True if host is reachable
        """
        return SocketUtils.check_port_open(host, 80, timeout)
    
    @staticmethod
    def download_file(url: str, destination: str) -> bool:
        """
        Download file from URL.
        
        Args:
            url: URL to download from
            destination: Local file path
            
        Returns:
            True if successful
        """
        try:
            urllib.request.urlretrieve(url, destination)
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            return False
    
    @staticmethod
    def get_public_ip() -> Optional[str]:
        """
        Get public IP address using external service.
        
        Returns:
            Public IP or None
        """
        try:
            with urllib.request.urlopen('https://api.ipify.org') as response:
                return response.read().decode('utf-8')
        except:
            return None


class WebScraper:
    """Simple web scraping utilities."""
    
    @staticmethod
    def fetch_page(url: str) -> Optional[str]:
        """
        Fetch web page content.
        
        Args:
            url: URL to fetch
            
        Returns:
            Page content or None
        """
        try:
            with urllib.request.urlopen(url) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"Failed to fetch page: {e}")
            return None
    
    @staticmethod
    def extract_links(html: str) -> list:
        """
        Extract all links from HTML.
        
        Args:
            html: HTML content
            
        Returns:
            List of URLs
        """
        import re
        pattern = r'href=[\'"](https?://[^\'" >]+)'
        return re.findall(pattern, html)
    
    @staticmethod
    def extract_emails(text: str) -> list:
        """
        Extract email addresses from text.
        
        Args:
            text: Text to search
            
        Returns:
            List of email addresses
        """
        import re
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(pattern, text)


def main() -> None:
    """Demonstrate networking utilities."""
    
    print("=== Networking Utilities Demo ===")
    
    # URL parsing
    print("\n--- URL Parsing ---")
    url = "https://example.com/path?param1=value1&param2=value2#fragment"
    parsed = URLUtils.parse_url(url)
    print(f"URL: {url}")
    print(f"Parsed: {parsed}")
    
    # URL building
    print("\n--- URL Building ---")
    base = "https://api.example.com"
    path = "/users"
    params = {"page": "1", "limit": "10"}
    built_url = URLUtils.build_url(base, path, params)
    print(f"Built URL: {built_url}")
    
    # Query string parsing
    print("\n--- Query String ---")
    query = "name=John&age=30&city=NYC"
    parsed_query = URLUtils.parse_query_string(query)
    print(f"Query: {query}")
    print(f"Parsed: {parsed_query}")
    
    # Socket utilities
    print("\n--- Socket Utilities ---")
    print(f"Hostname: {SocketUtils.get_hostname()}")
    print(f"Local IP: {SocketUtils.get_local_ip()}")
    
    google_ip = SocketUtils.resolve_hostname("google.com")
    print(f"Google IP: {google_ip}")
    
    # Port check
    print("\n--- Port Check ---")
    print(f"Port 80 on google.com: {SocketUtils.check_port_open('google.com', 80)}")
    print(f"Port 443 on google.com: {SocketUtils.check_port_open('google.com', 443)}")
    
    # URL encoding/decoding
    print("\n--- URL Encoding ---")
    original = "Hello World!"
    encoded = URLUtils.encode_url(original)
    decoded = URLUtils.decode_url(encoded)
    print(f"Original: {original}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")


if __name__ == "__main__":
    main()
