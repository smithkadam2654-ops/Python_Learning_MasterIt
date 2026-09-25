"""
Cybersecurity Advanced Module

This module provides comprehensive cybersecurity utilities including:
- Network scanning and reconnaissance
- Port scanning concepts
- Vulnerability assessment
- Intrusion detection concepts
- Firewall rule management
- Encryption and decryption
- Hash calculation and verification
- Password security analysis
- Certificate management concepts
- Security audit utilities

Note: This module uses cryptography libraries for advanced features.
Install with: pip install cryptography requests

All functions include comprehensive docstrings and type hints.
"""

import hashlib
import hmac
import base64
import re
import socket
import ssl
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class VulnerabilitySeverity(Enum):
    """Vulnerability severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class PortStatus(Enum):
    """Port scan status."""
    OPEN = "open"
    CLOSED = "closed"
    FILTERED = "filtered"
    TIMEOUT = "timeout"


@dataclass
class Vulnerability:
    """Vulnerability data structure."""
    cve_id: str
    name: str
    description: str
    severity: VulnerabilitySeverity
    affected_components: List[str]
    cvss_score: float
    fix_available: bool
    discovered_date: datetime


@dataclass
class PortScanResult:
    """Port scan result."""
    port: int
    status: PortStatus
    service: Optional[str] = None
    banner: Optional[str] = None
    response_time: float = 0.0


@dataclass
class SecurityEvent:
    """Security event data structure."""
    event_id: str
    event_type: str
    severity: str
    source_ip: str
    destination_ip: str
    timestamp: datetime
    details: Dict[str, Any]


class NetworkScanner:
    """Network scanning utilities."""
    
    @staticmethod
    def check_port(host: str, port: int, timeout: int = 5) -> PortScanResult:
        """Check if port is open on host."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            start_time = datetime.now()
            result = sock.connect_ex((host, port))
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds()
            sock.close()
            
            if result == 0:
                return PortScanResult(
                    port=port,
                    status=PortStatus.OPEN,
                    response_time=response_time
                )
            else:
                return PortScanResult(
                    port=port,
                    status=PortStatus.CLOSED,
                    response_time=response_time
                )
        except socket.timeout:
            return PortScanResult(port=port, status=PortStatus.TIMEOUT)
        except socket.error:
            return PortScanResult(port=port, status=PortStatus.FILTERED)
    
    @staticmethod
    def scan_ports(host: str, ports: List[int], timeout: int = 2) -> List[PortScanResult]:
        """Scan multiple ports on host."""
        results = []
        
        for port in ports:
            result = NetworkScanner.check_port(host, port, timeout)
            results.append(result)
        
        return results
    
    @staticmethod
    def get_service_banner(host: str, port: int) -> Optional[str]:
        """Get service banner from port."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            return banner.strip()
        except:
            return None
    
    @staticmethod
    def ping_host(host: str, timeout: int = 5) -> bool:
        """Ping host to check connectivity."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, 80))  # Try HTTP port
            sock.close()
            return result == 0
        except:
            return False


class VulnerabilityScanner:
    """Vulnerability assessment utilities."""
    
    @staticmethod
    def check_sql_injection(url: str) -> bool:
        """Simple SQL injection vulnerability check."""
        if not REQUESTS_AVAILABLE:
            return False
        
        test_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "1' OR '1'='1",
            "admin'--"
        ]
        
        for payload in test_payloads:
            try:
                # Simple GET request with payload
                test_url = f"{url}?id={payload}"
                response = requests.get(test_url, timeout=5)
                
                # Check for SQL error patterns
                error_patterns = [
                    "SQL syntax",
                    "mysql_fetch",
                    "ORA-",
                    "PostgreSQL"
                ]
                
                for pattern in error_patterns:
                    if pattern in response.text:
                        return True
            except:
                continue
        
        return False
    
    @staticmethod
    def check_xss(url: str) -> bool:
        """Simple XSS vulnerability check."""
        if not REQUESTS_AVAILABLE:
            return False
        
        test_payload = "<script>alert('XSS')</script>"
        
        try:
            response = requests.get(url, timeout=5)
            
            # Check if payload is reflected in response
            if test_payload in response.text:
                return True
            
            # Try POST with payload
            if '?' in url:
                base_url = url.split('?')[0]
            else:
                base_url = url
            
            response = requests.post(base_url, data={'input': test_payload}, timeout=5)
            
            if test_payload in response.text:
                return True
        except:
            pass
        
        return False
    
    @staticmethod
    def check_directory_traversal(url: str) -> bool:
        """Check for directory traversal vulnerability."""
        if not REQUESTS_AVAILABLE:
            return False
        
        test_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd"
        ]
        
        for path in test_paths:
            try:
                test_url = f"{url}?file={path}"
                response = requests.get(test_url, timeout=5)
                
                # Check for system file patterns
                if "root:" in response.text or "127.0.0.1" in response.text:
                    return True
            except:
                continue
        
        return False
    
    @staticmethod
    def analyze_ssl_tls(hostname: str, port: int = 443) -> Dict:
        """Analyze SSL/TLS configuration (simplified)."""
        try:
            import ssl
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        "protocol": ssock.version(),
                        "cipher": ssock.cipher(),
                        "certificate": {
                            "subject": dict(x[0] for x in cert['subject']),
                            "issuer": dict(x[0] for x in cert['issuer']),
                            "not_before": cert['notBefore'],
                            "not_after": cert['notAfter']
                        }
                    }
        except:
            return {"error": "SSL/TLS analysis failed"}


class PasswordAnalyzer:
    """Password security analysis."""
    
    @staticmethod
    def calculate_entropy(password: str) -> float:
        """Calculate password entropy."""
        if not password:
            return 0.0
        
        charset_size = 0
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            charset_size += 32
        
        if charset_size == 0:
            return 0.0
        
        entropy = len(password) * math.log2(charset_size)
        return entropy
    
    @staticmethod
    def check_password_strength(password: str) -> Dict:
        """Check password strength."""
        strength = {
            "length": len(password),
            "has_lower": any(c.islower() for c in password),
            "has_upper": any(c.isupper() for c in password),
            "has_digit": any(c.isdigit() for c in password),
            "has_special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
            "entropy": PasswordAnalyzer.calculate_entropy(password),
            "score": 0
        }
        
        # Calculate score
        score = 0
        if strength["length"] >= 8:
            score += 1
        if strength["length"] >= 12:
            score += 1
        if strength["has_lower"]:
            score += 1
        if strength["has_upper"]:
            score += 1
        if strength["has_digit"]:
            score += 1
        if strength["has_special"]:
            score += 1
        if strength["entropy"] >= 40:
            score += 1
        if strength["entropy"] >= 60:
            score += 1
        
        strength["score"] = min(score, 5)
        strength["strength"] = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"][strength["score"]]
        
        return strength
    
    @staticmethod
    def check_common_passwords(password: str, common_passwords: List[str]) -> bool:
        """Check if password is in common passwords list."""
        return password.lower() in [p.lower() for p in common_passwords]
    
    @staticmethod
    def generate_password(length: int = 16, include_special: bool = True) -> str:
        """Generate secure random password."""
        import random
        import string
        
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        password = ''.join(random.choice(chars) for _ in range(length))
        return password


class EncryptionManager:
    """Encryption and decryption utilities."""
    
    def __init__(self):
        """Initialize encryption manager."""
        self.key: Optional[bytes] = None
        self.fernet: Optional[Fernet] = None
    
    def generate_key(self, password: str, salt: Optional[bytes] = None) -> bytes:
        """Generate encryption key from password."""
        if not CRYPTO_AVAILABLE:
            return hashlib.sha256(password.encode()).digest()
        
        if salt is None:
            salt = b'salt_value'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def set_key(self, key: bytes) -> None:
        """Set encryption key."""
        if CRYPTO_AVAILABLE:
            self.key = key
            self.fernet = Fernet(key)
        else:
            self.key = key
    
    def encrypt(self, data: str) -> bytes:
        """Encrypt data."""
        if CRYPTO_AVAILABLE and self.fernet:
            return self.fernet.encrypt(data.encode())
        else:
            # Fallback using simple XOR
            key_bytes = self.key if self.key else b'default_key'
            data_bytes = data.encode()
            encrypted = bytes(a ^ b for a, b in zip(data_bytes, key_bytes * (len(data_bytes) // len(key_bytes) + 1)))
            return encrypted
    
    def decrypt(self, encrypted_data: bytes) -> str:
        """Decrypt data."""
        if CRYPTO_AVAILABLE and self.fernet:
            return self.fernet.decrypt(encrypted_data).decode()
        else:
            # Fallback using simple XOR
            key_bytes = self.key if self.key else b'default_key'
            decrypted = bytes(a ^ b for a, b in zip(encrypted_data, key_bytes * (len(encrypted_data) // len(key_bytes) + 1)))
            return decrypted.decode(errors='ignore')
    
    def generate_rsa_keypair(self) -> Tuple[bytes, bytes]:
        """Generate RSA key pair."""
        if not CRYPTO_AVAILABLE:
            return b"", b""
        
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        public_key = private_key.public_key()
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem


class HashCalculator:
    """Hash calculation and verification."""
    
    @staticmethod
    def calculate_hash(data: str, algorithm: str = "sha256") -> str:
        """Calculate hash of data."""
        algorithm = algorithm.lower()
        
        if algorithm == "md5":
            return hashlib.md5(data.encode()).hexdigest()
        elif algorithm == "sha1":
            return hashlib.sha1(data.encode()).hexdigest()
        elif algorithm == "sha256":
            return hashlib.sha256(data.encode()).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(data.encode()).hexdigest()
        else:
            return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
        """Calculate hash of file."""
        algorithm = algorithm.lower()
        
        if algorithm == "md5":
            hash_func = hashlib.md5()
        elif algorithm == "sha1":
            hash_func = hashlib.sha1()
        elif algorithm == "sha256":
            hash_func = hashlib.sha256()
        elif algorithm == "sha512":
            hash_func = hashlib.sha512()
        else:
            hash_func = hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
        except:
            return ""
    
    @staticmethod
    def verify_hash(data: str, hash_value: str, algorithm: str = "sha256") -> bool:
        """Verify hash of data."""
        calculated = HashCalculator.calculate_hash(data, algorithm)
        return calculated.lower() == hash_value.lower()
    
    @staticmethod
    def calculate_hmac(data: str, key: str, algorithm: str = "sha256") -> str:
        """Calculate HMAC."""
        algorithm = algorithm.lower()
        
        if algorithm == "md5":
            return hmac.new(key.encode(), data.encode(), hashlib.md5).hexdigest()
        elif algorithm == "sha1":
            return hmac.new(key.encode(), data.encode(), hashlib.sha1).hexdigest()
        elif algorithm == "sha256":
            return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()
        elif algorithm == "sha512":
            return hmac.new(key.encode(), data.encode(), hashlib.sha512).hexdigest()
        else:
            return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()


class FirewallRuleManager:
    """Firewall rule management."""
    
    def __init__(self):
        """Initialize firewall rule manager."""
        self.rules: List[Dict] = []
    
    def add_rule(self, source: str, destination: str, port: str, 
                 action: str, protocol: str = "tcp") -> None:
        """Add firewall rule."""
        rule = {
            "source": source,
            "destination": destination,
            "port": port,
            "protocol": protocol,
            "action": action,
            "enabled": True
        }
        self.rules.append(rule)
    
    def remove_rule(self, index: int) -> bool:
        """Remove firewall rule."""
        if 0 <= index < len(self.rules):
            self.rules.pop(index)
            return True
        return False
    
    def check_packet(self, source: str, destination: str, port: int,
                    protocol: str = "tcp") -> str:
        """Check if packet is allowed by rules."""
        for rule in self.rules:
            if not rule["enabled"]:
                continue
            
            # Simple matching (in real implementation, would use subnet matching)
            if (rule["source"] == source or rule["source"] == "any") and \
               (rule["destination"] == destination or rule["destination"] == "any") and \
               (rule["port"] == str(port) or rule["port"] == "any") and \
               (rule["protocol"] == protocol):
                return rule["action"]
        
        return "deny"  # Default deny
    
    def enable_rule(self, index: int) -> bool:
        """Enable firewall rule."""
        if 0 <= index < len(self.rules):
            self.rules[index]["enabled"] = True
            return True
        return False
    
    def disable_rule(self, index: int) -> bool:
        """Disable firewall rule."""
        if 0 <= index < len(self.rules):
            self.rules[index]["enabled"] = False
            return True
        return False


class IntrusionDetection:
    """Intrusion detection concepts."""
    
    @staticmethod
    def detect_port_scan(ip: str, connection_attempts: List[Tuple[str, int]]) -> bool:
        """Detect port scanning activity."""
        # Check for multiple connection attempts to different ports
        ports = set(port for _, port in connection_attempts)
        
        if len(ports) > 10:  # Threshold for port scan
            return True
        
        return False
    
    @staticmethod
    def detect_brute_force(ip: str, failed_attempts: int, 
                          time_window: int = 60) -> bool:
        """Detect brute force attack."""
        # Simplified: check if failed attempts exceed threshold
        threshold = 5  # 5 failed attempts per minute
        
        if failed_attempts > threshold:
            return True
        
        return False
    
    @staticmethod
    def detect_ddos(ip: str, request_count: int, 
                    time_window: int = 60) -> bool:
        """Detect DDoS attack."""
        # Check if request count exceeds threshold
        threshold = 100  # 100 requests per minute
        
        if request_count > threshold:
            return True
        
        return False


class SecurityAuditor:
    """Security audit utilities."""
    
    @staticmethod
    def audit_password_policy(passwords: List[str]) -> Dict:
        """Audit password policy compliance."""
        results = {
            "total": len(passwords),
            "weak": 0,
            "fair": 0,
            "good": 0,
            "strong": 0,
            "very_strong": 0,
            "violations": []
        }
        
        for password in passwords:
            strength = PasswordAnalyzer.check_password_strength(password)
            results[strength["strength"].lower().replace(" ", "_")] += 1
            
            if strength["score"] < 3:
                results["violations"].append({
                    "password": "*" * len(password),
                    "issues": [k for k, v in strength.items() if not v and k not in ["length", "score", "strength", "entropy"]]
                })
        
        return results
    
    @staticmethod
    def audit_file_permissions(file_path: str) -> Dict:
        """Audit file permissions (simplified)."""
        try:
            import os
            import stat
            
            file_stat = os.stat(file_path)
            mode = file_stat.st_mode
            
            return {
                "file": file_path,
                "mode": oct(mode),
                "readable": os.access(file_path, os.R_OK),
                "writable": os.access(file_path, os.W_OK),
                "executable": os.access(file_path, os.X_OK)
            }
        except:
            return {"error": "Unable to audit file permissions"}
    
    @staticmethod
    def audit_open_ports(host: str, allowed_ports: List[int]) -> Dict:
        """Audit open ports against allowed list."""
        common_ports = [21, 22, 23, 25, 53, 80, 443, 3306, 5432, 6379]
        scan_results = NetworkScanner.scan_ports(host, common_ports)
        
        open_ports = [r.port for r in scan_results if r.status == PortStatus.OPEN]
        unauthorized_ports = [p for p in open_ports if p not in allowed_ports]
        
        return {
            "host": host,
            "open_ports": open_ports,
            "unauthorized_ports": unauthorized_ports,
            "compliant": len(unauthorized_ports) == 0
        }


def demonstrate_cybersecurity_advanced():
    """Demonstrate cybersecurity functionality."""
    print("=== Cybersecurity Advanced Demonstration ===\n")
    
    # Network Scanning
    print("1. Network Scanning:")
    # Scan localhost common ports
    common_ports = [22, 80, 443, 3306, 5432]
    scan_results = NetworkScanner.scan_ports("127.0.0.1", common_ports)
    
    print(f"   Port scan results:")
    for result in scan_results:
        print(f"   Port {result.port}: {result.status.value}")
    
    # Vulnerability Scanning
    print("\n2. Vulnerability Scanning:")
    test_url = "http://example.com"
    
    sql_injection = VulnerabilityScanner.check_sql_injection(test_url)
    xss = VulnerabilityScanner.check_xss(test_url)
    dir_traversal = VulnerabilityScanner.check_directory_traversal(test_url)
    
    print(f"   SQL Injection vulnerable: {sql_injection}")
    print(f"   XSS vulnerable: {xss}")
    print(f"   Directory Traversal vulnerable: {dir_traversal}")
    
    # Password Analysis
    print("\n3. Password Analysis:")
    test_passwords = ["password", "MyP@ssw0rd!", "Secure123!@#"]
    
    for password in test_passwords:
        strength = PasswordAnalyzer.check_password_strength(password)
        print(f"   '{password}': {strength['strength']} (score: {strength['score']})")
    
    # Generate Password
    print("\n4. Password Generation:")
    generated = PasswordAnalyzer.generate_password(length=16, include_special=True)
    print(f"   Generated password: {generated}")
    
    # Encryption
    print("\n5. Encryption:")
    encryption = EncryptionManager()
    key = encryption.generate_key("my_password")
    encryption.set_key(key)
    
    plaintext = "Secret message"
    encrypted = encryption.encrypt(plaintext)
    decrypted = encryption.decrypt(encrypted)
    
    print(f"   Original: {plaintext}")
    print(f"   Encrypted (first 32 chars): {encrypted[:32]}...")
    print(f"   Decrypted: {decrypted}")
    
    # Hash Calculation
    print("\n6. Hash Calculation:")
    data = "test data"
    
    md5_hash = HashCalculator.calculate_hash(data, "md5")
    sha256_hash = HashCalculator.calculate_hash(data, "sha256")
    
    print(f"   MD5: {md5_hash}")
    print(f"   SHA-256: {sha256_hash}")
    
    # HMAC
    print("\n7. HMAC Calculation:")
    hmac_result = HashCalculator.calculate_hmac(data, "secret_key")
    print(f"   HMAC-SHA256: {hmac_result}")
    
    # Firewall Rules
    print("\n8. Firewall Rule Management:")
    firewall = FirewallRuleManager()
    
    firewall.add_rule("192.168.1.0/24", "10.0.0.1", "80", "allow", "tcp")
    firewall.add_rule("any", "10.0.0.1", "22", "deny", "tcp")
    
    packet_action = firewall.check_packet("192.168.1.100", "10.0.0.1", 80, "tcp")
    print(f"   Packet action: {packet_action}")
    
    # Intrusion Detection
    print("\n9. Intrusion Detection:")
    connection_attempts = [("192.168.1.100", 22), ("192.168.1.100", 23), 
                            ("192.168.1.100", 80), ("192.168.1.100", 443)]
    
    port_scan = IntrusionDetection.detect_port_scan("192.168.1.100", connection_attempts)
    print(f"   Port scan detected: {port_scan}")
    
    brute_force = IntrusionDetection.detect_brute_force("192.168.1.100", 7)
    print(f"   Brute force detected: {brute_force}")
    
    # Security Audit
    print("\n10. Security Audit:")
    audit_passwords = ["weak", "Strong123!", "MyPassword!@#"]
    password_audit = SecurityAuditor.audit_password_policy(audit_passwords)
    
    print(f"   Password audit: {password_audit}")
    
    print("\n=== Demonstration Complete ===")
    print("\nCybersecurity Best Practices:")
    print("- Use strong, unique passwords for all accounts")
    print("- Enable multi-factor authentication where possible")
    print("- Keep systems and software updated")
    print("- Use encryption for sensitive data")
    print("- Implement proper firewall rules")
    print("- Monitor for suspicious activity")
    print("- Regular security audits and penetration testing")
    print("- Use secure communication protocols (HTTPS, SSH)")
    print("- Implement proper access controls")
    print("- Regularly backup critical data")
    print("- Educate users about security best practices")
    print("- Use intrusion detection systems")
    print("- Implement proper logging and monitoring")
    print("- Follow principle of least privilege")
    print("- Use VPN for remote access")
    print("- Segment networks to limit attack surface")


if __name__ == "__main__":
    demonstrate_cybersecurity_advanced()
