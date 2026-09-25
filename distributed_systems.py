"""
Distributed Systems Module

This module provides comprehensive distributed systems utilities including:
- Distributed lock management
- Leader election
- Distributed cache coordination
- Consistent hashing
- Service discovery
- Load balancing strategies
- Distributed tracing concepts
- Circuit breaker pattern
- Retry mechanisms
- Health checking

All functions include comprehensive docstrings and type hints.
"""

import time
import hashlib
import random
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
import threading


class ConsistencyLevel(Enum):
    """Consistency levels for distributed operations."""
    STRONG = "strong"
    EVENTUAL = "eventual"
    QUORUM = "quorum"
    READ_YOUR_WRITES = "read_your_writes"


class LoadBalancingStrategy(Enum):
    """Load balancing strategies."""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    RANDOM = "random"
    IP_HASH = "ip_hash"


class ServiceStatus(Enum):
    """Service health status."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


@dataclass
class ServiceInstance:
    """Service instance data structure."""
    instance_id: str
    address: str
    port: int
    status: ServiceStatus
    last_heartbeat: float
    metadata: Optional[Dict] = None
    weight: int = 1
    active_connections: int = 0
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class DistributedLock:
    """Distributed lock implementation."""
    
    def __init__(self, lock_name: str, ttl: int = 30):
        """Initialize distributed lock."""
        self.lock_name = lock_name
        self.ttl = ttl
        self.lock_holder: Optional[str] = None
        self.lock_time: Optional[float] = None
        self.lock = threading.Lock()
    
    def acquire(self, holder: str) -> bool:
        """Acquire lock."""
        with self.lock:
            # Check if lock is expired
            if self.lock_time and time.time() - self.lock_time > self.ttl:
                self.lock_holder = None
                self.lock_time = None
            
            if self.lock_holder is None:
                self.lock_holder = holder
                self.lock_time = time.time()
                return True
            
            return False
    
    def release(self, holder: str) -> bool:
        """Release lock."""
        with self.lock:
            if self.lock_holder == holder:
                self.lock_holder = None
                self.lock_time = None
                return True
            return False
    
    def is_locked(self) -> bool:
        """Check if lock is held."""
        with self.lock:
            if self.lock_time and time.time() - self.lock_time > self.ttl:
                self.lock_holder = None
                self.lock_time = None
            
            return self.lock_holder is not None
    
    def get_holder(self) -> Optional[str]:
        """Get current lock holder."""
        with self.lock:
            return self.lock_holder


class LeaderElection:
    """Leader election implementation."""
    
    def __init__(self, node_id: str, peers: List[str]):
        """Initialize leader election."""
        self.node_id = node_id
        self.peers = peers
        self.leader: Optional[str] = None
        self.term: int = 0
        self.votes_received: int = 0
        self.lock = threading.Lock()
    
    def start_election(self) -> bool:
        """Start leader election."""
        with self.lock:
            self.term += 1
            self.votes_received = 1  # Vote for self
            
            # Simulate requesting votes from peers
            for peer in self.peers:
                if peer != self.node_id:
                    # Simulate peer voting (random for demo)
                    if random.random() > 0.3:
                        self.votes_received += 1
            
            # Check if we won
            majority = (len(self.peers) + 1) // 2 + 1
            
            if self.votes_received >= majority:
                self.leader = self.node_id
                return True
            
            return False
    
    def get_leader(self) -> Optional[str]:
        """Get current leader."""
        with self.lock:
            return self.leader
    
    def is_leader(self) -> bool:
        """Check if this node is leader."""
        with self.lock:
            return self.leader == self.node_id


class ConsistentHashing:
    """Consistent hashing for distributed systems."""
    
    def __init__(self, virtual_nodes: int = 100):
        """Initialize consistent hashing."""
        self.virtual_nodes = virtual_nodes
        self.ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []
    
    def _hash(self, key: str) -> int:
        """Hash key to integer."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node: str) -> None:
        """Add node to hash ring."""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}#{i}"
            hash_value = self._hash(virtual_key)
            self.ring[hash_value] = node
            self.sorted_keys.append(hash_value)
        
        self.sorted_keys.sort()
    
    def remove_node(self, node: str) -> None:
        """Remove node from hash ring."""
        keys_to_remove = []
        
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}#{i}"
            hash_value = self._hash(virtual_key)
            if hash_value in self.ring and self.ring[hash_value] == node:
                keys_to_remove.append(hash_value)
        
        for key in keys_to_remove:
            del self.ring[key]
            self.sorted_keys.remove(key)
    
    def get_node(self, key: str) -> Optional[str]:
        """Get node for key."""
        if not self.sorted_keys:
            return None
        
        hash_value = self._hash(key)
        
        # Find first node with hash >= key hash
        for ring_key in self.sorted_keys:
            if ring_key >= hash_value:
                return self.ring[ring_key]
        
        # Wrap around to first node
        return self.ring[self.sorted_keys[0]]


class ServiceDiscovery:
    """Service discovery implementation."""
    
    def __init__(self):
        """Initialize service discovery."""
        self.services: Dict[str, List[ServiceInstance]] = defaultdict(list)
        self.lock = threading.Lock()
    
    def register_service(self, service_name: str, instance: ServiceInstance) -> None:
        """Register service instance."""
        with self.lock:
            # Remove existing instance with same ID
            self.services[service_name] = [
                inst for inst in self.services[service_name]
                if inst.instance_id != instance.instance_id
            ]
            self.services[service_name].append(instance)
    
    def deregister_service(self, service_name: str, instance_id: str) -> bool:
        """Deregister service instance."""
        with self.lock:
            if service_name in self.services:
                original_count = len(self.services[service_name])
                self.services[service_name] = [
                    inst for inst in self.services[service_name]
                    if inst.instance_id != instance_id
                ]
                return len(self.services[service_name]) < original_count
            return False
    
    def get_service_instances(self, service_name: str) -> List[ServiceInstance]:
        """Get all instances of service."""
        with self.lock:
            return self.services.get(service_name, []).copy()
    
    def get_healthy_instances(self, service_name: str) -> List[ServiceInstance]:
        """Get healthy instances of service."""
        with self.lock:
            return [
                inst for inst in self.services.get(service_name, [])
                if inst.status == ServiceStatus.HEALTHY
            ]
    
    def update_heartbeat(self, service_name: str, instance_id: str) -> bool:
        """Update instance heartbeat."""
        with self.lock:
            for inst in self.services.get(service_name, []):
                if inst.instance_id == instance_id:
                    inst.last_heartbeat = time.time()
                    return True
            return False
    
    def check_health(self, service_name: str, timeout: int = 30) -> None:
        """Check health of all instances."""
        with self.lock:
            current_time = time.time()
            
            for inst in self.services.get(service_name, []):
                if current_time - inst.last_heartbeat > timeout:
                    inst.status = ServiceStatus.UNHEALTHY
                else:
                    inst.status = ServiceStatus.HEALTHY


class LoadBalancer:
    """Load balancer implementation."""
    
    def __init__(self, strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN):
        """Initialize load balancer."""
        self.strategy = strategy
        self.current_index = 0
        self.lock = threading.Lock()
    
    def select_instance(self, instances: List[ServiceInstance]) -> Optional[ServiceInstance]:
        """Select instance based on strategy."""
        if not instances:
            return None
        
        healthy_instances = [inst for inst in instances if inst.status == ServiceStatus.HEALTHY]
        
        if not healthy_instances:
            return None
        
        with self.lock:
            if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
                instance = healthy_instances[self.current_index % len(healthy_instances)]
                self.current_index += 1
                return instance
            
            elif self.strategy == LoadBalancingStrategy.RANDOM:
                return random.choice(healthy_instances)
            
            elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
                return min(healthy_instances, key=lambda x: x.active_connections)
            
            elif self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
                # Weighted selection
                total_weight = sum(inst.weight for inst in healthy_instances)
                rand = random.uniform(0, total_weight)
                
                cumulative = 0
                for inst in healthy_instances:
                    cumulative += inst.weight
                    if rand <= cumulative:
                        return inst
                
                return healthy_instances[-1]
            
            elif self.strategy == LoadBalancingStrategy.IP_HASH:
                # Simple hash-based selection
                # In real implementation, would use client IP
                hash_value = hash(str(time.time())) % len(healthy_instances)
                return healthy_instances[hash_value]
        
        return healthy_instances[0]


class CircuitBreaker:
    """Circuit breaker pattern implementation."""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        """Initialize circuit breaker."""
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "closed"  # closed, open, half-open
        self.lock = threading.Lock()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker."""
        with self.lock:
            if self.state == "open":
                if self.last_failure_time and time.time() - self.last_failure_time > self.timeout:
                    self.state = "half-open"
                else:
                    raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            
            with self.lock:
                if self.state == "half-open":
                    self.state = "closed"
                    self.failure_count = 0
            
            return result
        except Exception as e:
            with self.lock:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "open"
            
            raise e
    
    def get_state(self) -> Dict:
        """Get circuit breaker state."""
        with self.lock:
            return {
                "state": self.state,
                "failure_count": self.failure_count,
                "last_failure_time": self.last_failure_time
            }


class RetryMechanism:
    """Retry mechanism with exponential backoff."""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 30.0):
        """Initialize retry mechanism."""
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry logic."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    time.sleep(delay)
        
        raise last_exception


class DistributedCache:
    """Distributed cache coordination."""
    
    def __init__(self, consistency: ConsistencyLevel = ConsistencyLevel.EVENTUAL):
        """Initialize distributed cache."""
        self.consistency = consistency
        self.local_cache: Dict[str, Tuple[Any, float]] = {}
        self.lock = threading.Lock()
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache."""
        with self.lock:
            expiry = time.time() + ttl
            self.local_cache[key] = (value, expiry)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            if key in self.local_cache:
                value, expiry = self.local_cache[key]
                
                if time.time() < expiry:
                    return value
                else:
                    del self.local_cache[key]
            
            return None
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        with self.lock:
            if key in self.local_cache:
                del self.local_cache[key]
                return True
            return False
    
    def clear_expired(self) -> int:
        """Clear expired entries."""
        with self.lock:
            current_time = time.time()
            expired_keys = [
                key for key, (_, expiry) in self.local_cache.items()
                if current_time >= expiry
            ]
            
            for key in expired_keys:
                del self.local_cache[key]
            
            return len(expired_keys)


class DistributedTracing:
    """Distributed tracing concepts."""
    
    def __init__(self):
        """Initialize distributed tracing."""
        self.spans: List[Dict] = []
        self.current_span: Optional[Dict] = None
        self.lock = threading.Lock()
    
    def start_span(self, operation_name: str, parent_span_id: Optional[str] = None) -> str:
        """Start new trace span."""
        span_id = hashlib.md5(
            f"{operation_name}{time.time()}{random.random()}".encode()
        ).hexdigest()[:16]
        
        span = {
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "operation_name": operation_name,
            "start_time": time.time(),
            "end_time": None,
            "tags": {},
            "logs": []
        }
        
        with self.lock:
            self.spans.append(span)
            self.current_span = span
        
        return span_id
    
    def end_span(self, span_id: str) -> None:
        """End trace span."""
        with self.lock:
            for span in self.spans:
                if span["span_id"] == span_id:
                    span["end_time"] = time.time()
                    span["duration"] = span["end_time"] - span["start_time"]
                    break
    
    def add_tag(self, span_id: str, key: str, value: Any) -> None:
        """Add tag to span."""
        with self.lock:
            for span in self.spans:
                if span["span_id"] == span_id:
                    span["tags"][key] = value
                    break
    
    def add_log(self, span_id: str, message: str) -> None:
        """Add log to span."""
        with self.lock:
            for span in self.spans:
                if span["span_id"] == span_id:
                    span["logs"].append({
                        "timestamp": time.time(),
                        "message": message
                    })
                    break
    
    def get_trace(self, root_span_id: str) -> List[Dict]:
        """Get trace from root span."""
        with self.lock:
            # Build tree structure
            spans_by_id = {span["span_id"]: span for span in self.spans}
            trace = []
            
            def collect_spans(span_id: str):
                if span_id in spans_by_id:
                    span = spans_by_id[span_id]
                    trace.append(span)
                    
                    # Find children
                    for child_span in self.spans:
                        if child_span["parent_span_id"] == span_id:
                            collect_spans(child_span["span_id"])
            
            collect_spans(root_span_id)
            return trace


class HealthChecker:
    """Health checking utilities."""
    
    @staticmethod
    def check_http_endpoint(url: str, timeout: int = 5) -> bool:
        """Check HTTP endpoint health."""
        try:
            import requests
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def check_tcp_connection(host: str, port: int, timeout: int = 5) -> bool:
        """Check TCP connection."""
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    @staticmethod
    def check_service_dependencies(dependencies: List[Dict]) -> Dict[str, bool]:
        """Check multiple service dependencies."""
        results = {}
        
        for dep in dependencies:
            dep_type = dep.get("type", "http")
            
            if dep_type == "http":
                results[dep["name"]] = HealthChecker.check_http_endpoint(
                    dep["url"],
                    dep.get("timeout", 5)
                )
            elif dep_type == "tcp":
                results[dep["name"]] = HealthChecker.check_tcp_connection(
                    dep["host"],
                    dep["port"],
                    dep.get("timeout", 5)
                )
        
        return results


def demonstrate_distributed_systems():
    """Demonstrate distributed systems functionality."""
    print("=== Distributed Systems Demonstration ===\n")
    
    # Distributed Lock
    print("1. Distributed Lock:")
    lock = DistributedLock("test_lock", ttl=10)
    
    print(f"   Acquire by node1: {lock.acquire('node1')}")
    print(f"   Is locked: {lock.is_locked()}")
    print(f"   Lock holder: {lock.get_holder()}")
    
    print(f"   Acquire by node2: {lock.acquire('node2')}")
    print(f"   Release by node1: {lock.release('node1')}")
    print(f"   Acquire by node2: {lock.acquire('node2')}")
    
    # Leader Election
    print("\n2. Leader Election:")
    election = LeaderElection("node1", ["node1", "node2", "node3"])
    
    won = election.start_election()
    print(f"   Won election: {won}")
    print(f"   Leader: {election.get_leader()}")
    print(f"   Is leader: {election.is_leader()}")
    
    # Consistent Hashing
    print("\n3. Consistent Hashing:")
    ch = ConsistentHashing(virtual_nodes=5)
    
    ch.add_node("node1")
    ch.add_node("node2")
    ch.add_node("node3")
    
    key1 = "user123"
    key2 = "user456"
    
    node1 = ch.get_node(key1)
    node2 = ch.get_node(key2)
    
    print(f"   Key '{key1}' -> {node1}")
    print(f"   Key '{key2}' -> {node2}")
    
    # Service Discovery
    print("\n4. Service Discovery:")
    discovery = ServiceDiscovery()
    
    instance1 = ServiceInstance(
        instance_id="inst1",
        address="192.168.1.1",
        port=8080,
        status=ServiceStatus.HEALTHY,
        last_heartbeat=time.time()
    )
    
    instance2 = ServiceInstance(
        instance_id="inst2",
        address="192.168.1.2",
        port=8080,
        status=ServiceStatus.HEALTHY,
        last_heartbeat=time.time()
    )
    
    discovery.register_service("user-service", instance1)
    discovery.register_service("user-service", instance2)
    
    instances = discovery.get_service_instances("user-service")
    print(f"   Service instances: {len(instances)}")
    
    healthy = discovery.get_healthy_instances("user-service")
    print(f"   Healthy instances: {len(healthy)}")
    
    # Load Balancing
    print("\n5. Load Balancing:")
    lb = LoadBalancer(LoadBalancingStrategy.ROUND_ROBIN)
    
    selected = lb.select_instance(healthy)
    print(f"   Selected instance: {selected.instance_id if selected else 'None'}")
    
    lb_weighted = LoadBalancer(LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN)
    selected_weighted = lb_weighted.select_instance(healthy)
    print(f"   Weighted selection: {selected_weighted.instance_id if selected_weighted else 'None'}")
    
    # Circuit Breaker
    print("\n6. Circuit Breaker:")
    cb = CircuitBreaker(failure_threshold=2, timeout=5)
    
    def failing_function():
        raise Exception("Simulated failure")
    
    try:
        cb.call(failing_function)
    except:
        pass
    
    try:
        cb.call(failing_function)
    except:
        pass
    
    state = cb.get_state()
    print(f"   Circuit breaker state: {state}")
    
    # Retry Mechanism
    print("\n7. Retry Mechanism:")
    retry = RetryMechanism(max_retries=3, base_delay=0.1)
    
    attempt_count = [0]
    
    def flaky_function():
        attempt_count[0] += 1
        if attempt_count[0] < 3:
            raise Exception("Temporary failure")
        return "Success"
    
    result = retry.execute(flaky_function)
    print(f"   Result: {result}")
    print(f"   Attempts: {attempt_count[0]}")
    
    # Distributed Cache
    print("\n8. Distributed Cache:")
    cache = DistributedCache(ConsistencyLevel.EVENTUAL)
    
    cache.set("key1", "value1", ttl=60)
    cache.set("key2", "value2", ttl=60)
    
    print(f"   Get key1: {cache.get('key1')}")
    print(f"   Get key3: {cache.get('key3')}")
    
    # Distributed Tracing
    print("\n9. Distributed Tracing:")
    tracing = DistributedTracing()
    
    span1 = tracing.start_span("http_request")
    tracing.add_tag(span1, "url", "/api/users")
    tracing.add_log(span1, "Request received")
    
    span2 = tracing.start_span("database_query", parent_span_id=span1)
    tracing.add_tag(span2, "query", "SELECT * FROM users")
    tracing.end_span(span2)
    
    tracing.end_span(span1)
    
    trace = tracing.get_trace(span1)
    print(f"   Trace spans: {len(trace)}")
    
    # Health Checking
    print("\n10. Health Checking:")
    dependencies = [
        {"name": "database", "type": "tcp", "host": "localhost", "port": 5432},
        {"name": "cache", "type": "tcp", "host": "localhost", "port": 6379}
    ]
    
    health_results = HealthChecker.check_service_dependencies(dependencies)
    print(f"   Health results: {health_results}")
    
    print("\n=== Demonstration Complete ===")
    print("\nDistributed Systems Best Practices:")
    print("- Use distributed locks for critical sections")
    print("- Implement proper leader election for consistency")
    print("- Use consistent hashing for data distribution")
    print("- Implement service discovery for dynamic environments")
    print("- Use circuit breakers to prevent cascading failures")
    print("- Implement retry mechanisms with exponential backoff")
    print("- Use distributed caching with appropriate consistency")
    print("- Implement distributed tracing for debugging")
    print("- Use health checks for service monitoring")
    print("- Choose appropriate load balancing strategy")
    print("- Consider network partitions and timeouts")
    print("- Implement proper error handling and fallbacks")
    print("- Use idempotent operations when possible")


if __name__ == "__main__":
    demonstrate_distributed_systems()
