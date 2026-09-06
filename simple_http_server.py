"""
Simple HTTP Server - Basic HTTP server with custom handlers.
Features: Request handling, routing, and static file serving.
"""

import socket
import threading
from typing import Dict, Callable, Optional
from dataclasses import dataclass
from enum import Enum
import mimetypes
import os


class HTTPMethod(Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


@dataclass
class HTTPRequest:
    """HTTP request."""
    method: HTTPMethod
    path: str
    headers: Dict[str, str]
    body: str = ""
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.method.value} {self.path}"


@dataclass
class HTTPResponse:
    """HTTP response."""
    status_code: int
    status_text: str
    headers: Dict[str, str]
    body: str = ""
    
    def to_bytes(self) -> bytes:
        """Convert response to bytes."""
        status_line = f"HTTP/1.1 {self.status_code} {self.status_text}\r\n"
        headers = "\r\n".join(f"{k}: {v}" for k, v in self.headers.items())
        response = f"{status_line}{headers}\r\n\r\n{self.body}"
        return response.encode('utf-8')


class HTTPServer:
    """Simple HTTP server."""
    
    def __init__(self, host: str = "localhost", port: int = 8080) -> None:
        """
        Initialize HTTP server.
        
        Args:
            host: Host to bind to
            port: Port to listen on
        """
        self.host = host
        self.port = port
        self.routes: Dict[str, Dict[HTTPMethod, Callable]] = {}
        self._running = False
        self._socket: Optional[socket.socket] = None
    
    def add_route(self, path: str, method: HTTPMethod, handler: Callable) -> None:
        """
        Add route handler.
        
        Args:
            path: URL path
            method: HTTP method
            handler: Handler function
        """
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method] = handler
    
    def get(self, path: str) -> Callable:
        """Decorator for GET routes."""
        def decorator(handler: Callable) -> Callable:
            self.add_route(path, HTTPMethod.GET, handler)
            return handler
        return decorator
    
    def post(self, path: str) -> Callable:
        """Decorator for POST routes."""
        def decorator(handler: Callable) -> Callable:
            self.add_route(path, HTTPMethod.POST, handler)
            return handler
        return decorator
    
    def _parse_request(self, request_data: str) -> Optional[HTTPRequest]:
        """Parse HTTP request."""
        lines = request_data.split('\r\n')
        if not lines:
            return None
        
        # Parse request line
        request_line = lines[0].split()
        if len(request_line) < 2:
            return None
        
        method_str, path = request_line[0], request_line[1]
        
        try:
            method = HTTPMethod(method_str)
        except ValueError:
            return None
        
        # Parse headers
        headers = {}
        i = 1
        while i < len(lines) and lines[i]:
            if ':' in lines[i]:
                key, value = lines[i].split(':', 1)
                headers[key.strip()] = value.strip()
            i += 1
        
        # Parse body
        body = '\r\n'.join(lines[i+1:]) if i+1 < len(lines) else ""
        
        return HTTPRequest(method, path, headers, body)
    
    def _handle_client(self, client_socket: socket.socket) -> None:
        """Handle client connection."""
        try:
            request_data = client_socket.recv(4096).decode('utf-8')
            if not request_data:
                return
            
            request = self._parse_request(request_data)
            if not request:
                response = HTTPResponse(400, "Bad Request", {}, "Bad Request")
                client_socket.send(response.to_bytes())
                return
            
            # Find handler
            handler = None
            if request.path in self.routes:
                handler = self.routes[request.path].get(request.method)
            
            if handler:
                response = handler(request)
            else:
                response = HTTPResponse(404, "Not Found", {}, "Not Found")
            
            client_socket.send(response.to_bytes())
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
    
    def serve_static(self, directory: str, url_prefix: str = "/static") -> None:
        """
        Serve static files from directory.
        
        Args:
            directory: Directory to serve
            url_prefix: URL prefix for static files
        """
        @self.get(f"{url_prefix}/*")
        def static_handler(request: HTTPRequest) -> HTTPResponse:
            file_path = request.path[len(url_prefix):].lstrip('/')
            full_path = os.path.join(directory, file_path)
            
            if not os.path.exists(full_path) or not os.path.isfile(full_path):
                return HTTPResponse(404, "Not Found", {}, "File not found")
            
            mime_type, _ = mimetypes.guess_type(full_path)
            mime_type = mime_type or "application/octet-stream"
            
            with open(full_path, 'rb') as f:
                content = f.read()
            
            headers = {"Content-Type": mime_type}
            return HTTPResponse(200, "OK", headers, content.decode('utf-8', errors='ignore'))
    
    def start(self) -> None:
        """Start the server."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self.host, self.port))
        self._socket.listen(5)
        self._running = True
        
        print(f"Server running on http://{self.host}:{self.port}")
        
        while self._running:
            try:
                client_socket, address = self._socket.accept()
                print(f"Connection from {address}")
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,)
                )
                client_thread.daemon = True
                client_thread.start()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Server error: {e}")
    
    def stop(self) -> None:
        """Stop the server."""
        self._running = False
        if self._socket:
            self._socket.close()


def main() -> None:
    """Demonstrate HTTP server."""
    
    print("=== Simple HTTP Server Demo ===")
    print("Note: This is a demonstration. The server won't actually start.")
    print("In production, you would call server.start()")
    
    # Create server
    server = HTTPServer("localhost", 8080)
    
    # Add routes
    @server.get("/")
    def home(request: HTTPRequest) -> HTTPResponse:
        """Home page handler."""
        html = """
        <html>
        <head><title>Home</title></head>
        <body>
            <h1>Welcome to Simple HTTP Server</h1>
            <p>This is a simple HTTP server implementation.</p>
        </body>
        </html>
        """
        headers = {"Content-Type": "text/html"}
        return HTTPResponse(200, "OK", headers, html)
    
    @server.get("/api/data")
    def get_data(request: HTTPRequest) -> HTTPResponse:
        """API data handler."""
        data = {"message": "Hello from API", "status": "success"}
        import json
        headers = {"Content-Type": "application/json"}
        return HTTPResponse(200, "OK", headers, json.dumps(data))
    
    @server.post("/api/submit")
    def submit_form(request: HTTPRequest) -> HTTPResponse:
        """Form submission handler."""
        import json
        headers = {"Content-Type": "application/json"}
        return HTTPResponse(200, "OK", headers, json.dumps({"received": True}))
    
    print("\nRoutes configured:")
    for path, methods in server.routes.items():
        for method in methods:
            print(f"  {method.value} {path}")
    
    print("\nTo start the server, uncomment server.start() in the code")
    print("Then visit http://localhost:8080 in your browser")


if __name__ == "__main__":
    main()
