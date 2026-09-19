"""
Network Programming Module

This module provides comprehensive network programming utilities including:
- Socket programming
- HTTP server and client
- TCP/UDP communication
- Network protocol implementation
- Network discovery and scanning
- DNS operations
- Network monitoring
- WebSocket implementation
- Network utilities
- Network security basics

All functions include comprehensive docstrings and type hints.
"""

import socket
import threading
import time
import json
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
import struct


class NetworkProtocol(Enum):
    """Network protocol types."""
    TCP = "tcp"
    UDP = "udp"
    HTTP = "http"
    HTTPS = "https"
    WEBSOCKET = "websocket"


class SocketType(Enum):
    """Socket type constants."""
    SOCK_STREAM = socket.SOCK_STREAM
    SOCK_DGRAM = socket.SOCK_DGRAM


@dataclass
class NetworkConfig:
    """Network configuration."""
    host: str
    port: int
    protocol: NetworkProtocol
    buffer_size: int = 4096
    timeout: float = 30.0


@dataclass
class NetworkPacket:
    """Container for network packet."""
    data: bytes
    source: str
    destination: str
    timestamp: float
    sequence: int = 0


class TCPServer:
    """TCP server implementation."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8080,
                 max_connections: int = 5):
        """Initialize TCP server."""
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.server_socket: Optional[socket.socket] = None
        self.running = False
        self.clients: List[socket.socket] = []
        self.client_handlers: Dict[str, Callable] = {}
    
    def start(self) -> bool:
        """Start the TCP server."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.max_connections)
            self.running = True
            
            print(f"Server started on {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to start server: {e}")
            return False
    
    def stop(self) -> None:
        """Stop the TCP server."""
        self.running = False
        
        # Close all client connections
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        
        self.clients.clear()
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
    
    def accept_connection(self) -> Optional[socket.socket]:
        """Accept a new client connection."""
        if not self.running or not self.server_socket:
            return None
        
        try:
            client_socket, address = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Connection from {address}")
            return client_socket
        except socket.timeout:
            return None
        except Exception as e:
            print(f"Error accepting connection: {e}")
            return None
    
    def send_data(self, client: socket.socket, data: Union[str, bytes]) -> bool:
        """Send data to a client."""
        try:
            if isinstance(data, str):
                data = data.encode()
            
            client.sendall(data)
            return True
        except Exception as e:
            print(f"Error sending data: {e}")
            return False
    
    def receive_data(self, client: socket.socket, 
                     buffer_size: int = 4096) -> Optional[bytes]:
        """Receive data from a client."""
        try:
            data = client.recv(buffer_size)
            return data
        except socket.timeout:
            return None
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None
    
    def set_handler(self, event: str, handler: Callable) -> None:
        """Set event handler."""
        self.client_handlers[event] = handler


class UDPClient:
    """UDP client implementation."""
    
    def __init__(self, timeout: float = 5.0):
        """Initialize UDP client."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timeout = timeout
    
    def send(self, data: Union[str, bytes], host: str, port: int) -> bool:
        """Send UDP packet."""
        try:
            if isinstance(data, str):
                data = data.encode()
            
            self.socket.sendto(data, (host, port))
            return True
        except Exception as e:
            print(f"Error sending UDP packet: {e}")
            return False
    
    def receive(self, buffer_size: int = 4096) -> Optional[Tuple[bytes, Tuple[str, int]]]:
        """Receive UDP packet."""
        try:
            self.socket.settimeout(self.timeout)
            data, address = self.socket.recvfrom(buffer_size)
            return data, address
        except socket.timeout:
            return None
        except Exception as e:
            print(f"Error receiving UDP packet: {e}")
            return None
    
    def close(self) -> None:
        """Close UDP socket."""
        self.socket.close()


class HTTPServer:
    """Simple HTTP server implementation."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        """Initialize HTTP server."""
        self.host = host
        self.port = port
        self.server_socket: Optional[socket.socket] = None
        self.running = False
        self.routes: Dict[str, Callable] = {}
    
    def add_route(self, path: str, handler: Callable) -> None:
        """Add a route handler."""
        self.routes[path] = handler
    
    def start(self) -> bool:
        """Start the HTTP server."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"HTTP server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    threading.Thread(target=self.handle_client, args=(client_socket,)).start()
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Error accepting connection: {e}")
            
            return True
        except Exception as e:
            print(f"Failed to start HTTP server: {e}")
            return False
    
    def handle_client(self, client: socket.socket) -> None:
        """Handle HTTP client connection."""
        try:
            # Receive HTTP request
            request_data = b""
            while True:
                chunk = client.recv(1024)
                if not chunk:
                    break
                request_data += chunk
                if b"\r\n\r\n" in request_data:
                    break
            
            request = request_data.decode()
            
            # Parse HTTP request
            if request:
                lines = request.split('\r\n')
                if lines:
                    request_line = lines[0]
                    parts = request_line.split(' ')
                    
                    if len(parts) >= 2:
                        method = parts[0]
                        path = parts[1]
                        
                        # Route request
                        response = self.handle_request(method, path, request)
                        
                        # Send response
                        client.sendall(response.encode())
            
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client.close()
    
    def handle_request(self, method: str, path: str, request: str) -> str:
        """Handle HTTP request."""
        # Simple routing
        if path in self.routes:
            return self.routes[path](method, path, request)
        
        # Default response
        return self._build_response(404, "Not Found", {"Content-Type": "text/plain"})
    
    def _build_response(self, status_code: int, body: str, 
                       headers: Dict[str, str] = None) -> str:
        """Build HTTP response."""
        status_messages = {
            200: "OK",
            404: "Not Found",
            500: "Internal Server Error"
        }
        
        response = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}\r\n"
        
        if headers:
            for key, value in headers.items():
                response += f"{key}: {value}\r\n"
        
        response += f"Content-Length: {len(body)}\r\n"
        response += "\r\n"
        response += body
        
        return response
    
    def stop(self) -> None:
        """Stop the HTTP server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()


class HTTPClient:
    """Simple HTTP client implementation."""
    
    def __init__(self, timeout: float = 10.0):
        """Initialize HTTP client."""
        self.timeout = timeout
    
    def get(self, url: str, headers: Dict[str, str] = None) -> Optional[Tuple[int, str, str]]:
        """Send HTTP GET request."""
        return self._request("GET", url, headers=headers)
    
    def post(self, url: str, data: str = "", 
             headers: Dict[str, str] = None) -> Optional[Tuple[int, str, str]]:
        """Send HTTP POST request."""
        return self._request("POST", url, data=data, headers=headers)
    
    def _request(self, method: str, url: str, data: str = "",
               headers: Dict[str, str] = None) -> Optional[Tuple[int, str, str]]:
        """Send HTTP request."""
        try:
            # Parse URL
            from urllib.parse import urlparse
            parsed = urlparse(url)
            
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # Connect
            sock.connect((parsed.hostname, parsed.port or 80))
            
            # Build request
            path = parsed.path or "/"
            if parsed.query:
                path += f"?{parsed.query}"
            
            request = f"{method} {path} HTTP/1.1\r\n"
            request += f"Host: {parsed.hostname}\r\n"
            
            if headers:
                for key, value in headers.items():
                    request += f"{key}: {value}\r\n"
            
            if data:
                request += f"Content-Length: {len(data)}\r\n"
            
            request += "\r\n"
            
            if data:
                request += data
            
            # Send request
            sock.sendall(request.encode())
            
            # Receive response
            response_data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                if b"\r\n\r\n" in response_data:
                    break
            
            response = response_data.decode()
            
            # Parse response
            lines = response.split('\r\n')
            status_line = lines[0]
            status_code = int(status_line.split()[1])
            
            # Get body
            body = response.split('\r\n\r\n', 1)[1] if '\r\n\r\n' in response else ""
            
            sock.close()
            
            return status_code, status_line, body
            
        except Exception as e:
            print(f"HTTP request failed: {e}")
            return None


class NetworkScanner:
    """Network scanning and discovery utilities."""
    
    @staticmethod
    def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
        """Check if a port is open on a host."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    @staticmethod
    def scan_ports(host: str, ports: List[int], 
                    timeout: float = 1.0) -> Dict[int, bool]:
        """Scan multiple ports on a host."""
        results = {}
        
        for port in ports:
            results[port] = NetworkScanner.scan_port(host, port, timeout)
        
        return results
    
    @staticmethod
    def ping_host(host: str, timeout: float = 2.0) -> bool:
        """Ping a host to check connectivity."""
        try:
            # ICMP ping requires raw sockets (needs admin privileges)
            # Fall back to TCP connection check
            return NetworkScanner.scan_port(host, 80, timeout)
        except:
            return False
    
    @staticmethod
    def get_local_ip() -> Optional[str]:
        """Get local IP address."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            local_ip = sock.getsockname()[0]
            sock.close()
            return local_ip
        except:
            return None
    
    @staticmethod
    def get_hostname() -> str:
        """Get system hostname."""
        return socket.gethostname()


class DNSResolver:
    """DNS resolution utilities."""
    
    @staticmethod
    def resolve_hostname(hostname: str) -> Optional[str]:
        """Resolve hostname to IP address."""
        try:
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except:
            return None
    
    @staticmethod
    def reverse_lookup(ip_address: str) -> Optional[str]:
        """Reverse DNS lookup (IP to hostname)."""
        try:
            hostname = socket.gethostbyaddr(ip_address)
            return hostname[0]
        except:
            return None
    
    @staticmethod
    def get_dns_records(hostname: str, record_type: str = "A") -> List[str]:
        """Get DNS records for hostname."""
        # This would use dnspython library for full DNS resolution
        # Simplified implementation
        if record_type == "A":
            ip = DNSResolver.resolve_hostname(hostname)
            return [ip] if ip else []
        return []


class WebSocketServer:
    """Simple WebSocket server implementation."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 9000):
        """Initialize WebSocket server."""
        self.host = host
        self.port = port
        self.server_socket: Optional[socket.socket] = None
        self.running = False
        self.clients: List[socket.socket] = []
    
    def handle_handshake(self, client: socket.socket) -> bool:
        """Handle WebSocket handshake."""
        try:
            # Receive handshake request
            request = client.recv(4096).decode()
            
            if "Upgrade: websocket" in request:
                # Extract Sec-WebSocket-Key
                key = None
                for line in request.split('\r\n'):
                    if line.startswith("Sec-WebSocket-Key:"):
                        key = line.split(":")[1].strip()
                        break
                
                if key:
                    # Generate accept key
                    magic_string = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
                    accept_key = base64.b64encode(
                        hashlib.sha1((key + magic_string).encode()).digest()
                    ).decode()
                    
                    # Build response
                    response = (
                        "HTTP/1.1 101 Switching Protocols\r\n"
                        f"Upgrade: websocket\r\n"
                        f"Connection: Upgrade\r\n"
                        f"Sec-WebSocket-Accept: {accept_key}\r\n"
                        "\r\n"
                    )
                    
                    client.send(response.encode())
                    return True
            
            return False
        except Exception as e:
            print(f"Handshake error: {e}")
            return False
    
    def start(self) -> bool:
        """Start WebSocket server."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"WebSocket server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client, address = self.server_socket.accept()
                    print(f"WebSocket connection from {address}")
                    
                    if self.handle_handshake(client):
                        self.clients.append(client)
                        
                        # Handle WebSocket messages
                        threading.Thread(target=self.handle_client, args=(client,)).start()
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Error accepting connection: {e}")
            
            return True
        except Exception as e:
            print(f"Failed to start WebSocket server: {e}")
            return False
    
    def handle_client(self, client: socket.socket) -> None:
        """Handle WebSocket client messages."""
        try:
            while self.running:
                message = client.recv(4096)
                if not message:
                    break
                
                # Parse WebSocket frame (simplified)
                if len(message) >= 2:
                    opcode = message[0] & 0x0F
                    masked = (message[1] & 0x80) != 0
                    
                    if opcode == 0x8:  # Close frame
                        break
                    elif opcode == 0x1:  # Text frame
                        payload = message[2:] if masked else message[2:]
                        print(f"Received: {payload.decode()}")
                    
                    # Send pong for ping
                    if opcode == 0x9:  # Ping frame
                        pong_frame = bytearray([0x8A])
                        client.send(pong_frame)
                    
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            if client in self.clients:
                self.clients.remove(client)
            client.close()
    
    def broadcast(self, message: str) -> None:
        """Broadcast message to all connected clients."""
        frame = self._build_frame(message)
        
        for client in self.clients:
            try:
                client.send(frame)
            except:
                pass
    
    def _build_frame(self, message: str) -> bytes:
        """Build WebSocket frame."""
        data = message.encode()
        frame = bytearray()
        frame.append(0x81)  # Text frame, final fragment, no masking
        frame.extend(len(data).to_bytes(2, byteorder='big'))
        frame.extend(data)
        return bytes(frame)
    
    def stop(self) -> None:
        """Stop WebSocket server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()


class NetworkMonitor:
    """Network monitoring utilities."""
    
    @staticmethod
    def get_connection_info() -> Dict[str, Any]:
        """Get network connection information."""
        try:
            hostname = socket.gethostname()
            local_ip = NetworkScanner.get_local_ip()
            
            return {
                "hostname": hostname,
                "local_ip": local_ip,
                "timestamp": time.time()
            }
        except Exception as e:
            print(f"Error getting connection info: {e}")
            return {}
    
    @staticmethod
    def measure_latency(host: str, port: int = 80, 
                        packets: int = 4) -> float:
        """Measure network latency to host."""
        latencies = []
        
        for _ in range(packets):
            start_time = time.time()
            
            if NetworkScanner.scan_port(host, port, timeout=2.0):
                latency = (time.time() - start_time) * 1000
                latencies.append(latency)
        
        if latencies:
            return sum(latencies) / len(latencies)
        
        return 0.0


class ProtocolHandler:
    """Custom protocol implementation utilities."""
    
    @staticmethod
    def create_packet(data: bytes, packet_type: int, 
                     sequence: int = 0) -> bytes:
        """Create network packet with header."""
        header = struct.pack("!BBI", packet_type, sequence, len(data))
        return header + data
    
    @staticmethod
    def parse_packet(packet: bytes) -> Tuple[int, int, bytes]:
        """Parse network packet header."""
        if len(packet) < 7:
            return 0, 0, b""
        
        packet_type, sequence, data_length = struct.unpack("!BBI", packet[:7])
        data = packet[7:7+data_length]
        
        return packet_type, sequence, data


class NetworkSecurity:
    """Network security utilities."""
    
    @staticmethod
    def is_local_ip(ip: str) -> bool:
        """Check if IP address is local."""
        local_ranges = [
            "127.",
            "10.",
            "192.168.",
            "172.16.",
            "169.254.",
            "::1"
        ]
        
        return any(ip.startswith(prefix) for prefix in local_ranges)
    
    @staticmethod
    def validate_ip_address(ip: str) -> bool:
        """Validate IP address format."""
        try:
            socket.inet_pton(socket.AF_INET, ip)
            return True
        except:
            return False
    
    @staticmethod
    def is_valid_hostname(hostname: str) -> bool:
        """Validate hostname format."""
        if not hostname or len(hostname) > 253:
            return False
        
        if hostname[-1] == ".":
            return False
        
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-")
        return all(c in allowed for c in hostname)


def demonstrate_network_programming():
    """Demonstrate network programming functionality."""
    print("=== Network Programming Demonstration ===\n")
    
    # Network Scanner
    print("1. Network Scanning:")
    local_ip = NetworkScanner.get_local_ip()
    print(f"   Local IP: {local_ip}")
    
    hostname = NetworkScanner.get_hostname()
    print(f"   Hostname: {hostname}")
    
    # DNS Resolution
    print("\n2. DNS Resolution:")
    google_ip = DNSResolver.resolve_hostname("www.google.com")
    print(f"   www.google.com IP: {google_ip}")
    
    localhost_name = DNSResolver.reverse_lookup("127.0.0.1")
    print(f"   127.0.0.1 hostname: {localhost_name}")
    
    # Port Scanning
    print("\n3. Port Scanning:")
    common_ports = [80, 443, 22, 8080, 9000]
    results = NetworkScanner.scan_ports("localhost", common_ports)
    print(f"   Port scan results: {results}")
    
    # HTTP Client
    print("\n4. HTTP Client:")
    http_client = HTTPClient()
    
    response = http_client.get("http://httpbin.org/get")
    if response:
        status_code, status_line, body = response
        print(f"   Status: {status_code}")
        print(f"   Status line: {status_line}")
        print(f"   Body length: {len(body)}")
    
    # Network Monitoring
    print("\n5. Network Monitoring:")
    conn_info = NetworkMonitor.get_connection_info()
    print(f"   Connection info: {conn_info}")
    
    latency = NetworkMonitor.measure_latency("www.google.com", 80)
    print(f"   Latency to www.google.com: {latency:.2f}ms")
    
    # Protocol Handler
    print("\n6. Protocol Handler:")
    data = b"Hello, Network!"
    packet = ProtocolHandler.create_packet(data, 1, 1)
    print(f"   Created packet size: {len(packet)} bytes")
    
    packet_type, sequence, payload = ProtocolHandler.parse_packet(packet)
    print(f"   Parsed packet: type={packet_type}, seq={sequence}, data={payload}")
    
    # Network Security
    print("\n7. Network Security:")
    print(f"   127.0.0.1 is local: {NetworkSecurity.is_local_ip('127.0.0.1')}")
    print(f"   192.168.1.1 is local: {NetworkSecurity.is_local_ip('192.168.1.1')}")
    print(f"   8.8.8.8 is local: {NetworkSecurity.is_local_ip('8.8.8.8')}")
    print(f"   Valid IP (8.8.8.8): {NetworkSecurity.validate_ip_address('8.8.8.8')}")
    print(f"   Valid hostname: {NetworkSecurity.is_valid_hostname('example.com')}")
    
    # Server Examples
    print("\n8. Server Examples:")
    print("   TCP Server: port scanning, connection handling")
    print("   HTTP Server: request handling, routing")
    print("   WebSocket Server: handshake, real-time communication")
    print("   UDP Client: connectionless messaging")
    
    print("\n=== Demonstration Complete ===")
    print("\nNetwork Programming Best Practices:")
    print("- Always handle network errors gracefully")
    print("- Use appropriate timeouts for network operations")
    "- Implement proper connection cleanup")
    "- Validate and sanitize network input")
    "- Use secure protocols (HTTPS, WSS) when possible")
    print("- Respect rate limits and service terms")
    print("- Monitor network performance and latency")
    print("- Use connection pooling for high-performance applications")


if __name__ == "__main__":
    import base64
    demonstrate_network_programming()