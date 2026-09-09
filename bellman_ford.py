"""
Bellman-Ford Algorithm - Shortest path with negative weight handling.
Features: Negative edge support, cycle detection, and path reconstruction.
"""

from typing import List, Dict, Optional, TypeVar, Generic

T = TypeVar('T')


class BellmanFord:
    """Bellman-Ford shortest path algorithm implementation."""
    
    def __init__(self, directed: bool = False) -> None:
        """
        Initialize weighted graph.
        
        Args:
            directed: Whether graph is directed
        """
        self.directed = directed
        self.vertices: Set[T] = set()
        self.edges: List[tuple] = []
    
    def add_edge(self, u: T, v: T, weight: float) -> None:
        """
        Add weighted edge to graph.
        
        Args:
            u: First vertex
            v: Second vertex
            weight: Edge weight (can be negative)
        """
        self.vertices.add(u)
        self.vertices.add(v)
        self.edges.append((u, v, weight))
        
        if not self.directed:
            self.edges.append((v, u, weight))
    
    def shortest_path(self, start: T, end: T) -> Optional[tuple]:
        """
        Find shortest path using Bellman-Ford algorithm.
        
        Args:
            start: Starting vertex
            end: Target vertex
            
        Returns:
            Tuple of (distance, path) or None if no path/negative cycle
        """
        if start not in self.vertices or end not in self.vertices:
            return None
        
        # Initialize distances
        distances: Dict[T, float] = {vertex: float('inf') for vertex in self.vertices}
        distances[start] = 0
        parent: Dict[T, Optional[T]] = {vertex: None for vertex in self.vertices}
        
        # Relax edges |V| - 1 times
        for _ in range(len(self.vertices) - 1):
            for u, v, w in self.edges:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    parent[v] = u
        
        # Check for negative cycles
        for u, v, w in self.edges:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                return None  # Negative cycle detected
        
        # Check if end is reachable
        if distances[end] == float('inf'):
            return None
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent[current]
        
        return (distances[end], path[::-1])
    
    def shortest_distance(self, start: T, end: T) -> Optional[float]:
        """
        Find shortest distance without path reconstruction.
        
        Args:
            start: Starting vertex
            end: Target vertex
            
        Returns:
            Shortest distance or None if no path/negative cycle
        """
        result = self.shortest_path(start, end)
        return result[0] if result else None
    
    def all_shortest_paths(self, start: T) -> Optional[Dict[T, tuple]]:
        """
        Find shortest paths from start to all vertices.
        
        Args:
            start: Starting vertex
            
        Returns:
            Dictionary mapping vertex to (distance, path) or None if negative cycle
        """
        if start not in self.vertices:
            return None
        
        # Initialize distances
        distances: Dict[T, float] = {vertex: float('inf') for vertex in self.vertices}
        distances[start] = 0
        parent: Dict[T, Optional[T]] = {vertex: None for vertex in self.vertices}
        
        # Relax edges |V| - 1 times
        for _ in range(len(self.vertices) - 1):
            for u, v, w in self.edges:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    parent[v] = u
        
        # Check for negative cycles
        for u, v, w in self.edges:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                return None  # Negative cycle detected
        
        # Reconstruct all paths
        result = {}
        for vertex in self.vertices:
            if distances[vertex] != float('inf'):
                path = []
                current = vertex
                while current is not None:
                    path.append(current)
                    current = parent[current]
                result[vertex] = (distances[vertex], path[::-1])
        
        return result
    
    def has_negative_cycle(self) -> bool:
        """
        Check if graph contains a negative cycle.
        
        Returns:
            True if negative cycle exists
        """
        # Use any vertex as source
        if not self.vertices:
            return False
        
        start = next(iter(self.vertices))
        
        # Initialize distances
        distances: Dict[T, float] = {vertex: float('inf') for vertex in self.vertices}
        distances[start] = 0
        
        # Relax edges |V| - 1 times
        for _ in range(len(self.vertices) - 1):
            for u, v, w in self.edges:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
        
        # Check for negative cycles
        for u, v, w in self.edges:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                return True
        
        return False
    
    def find_negative_cycle(self) -> Optional[List[T]]:
        """
        Find a negative cycle in the graph.
        
        Returns:
            List of vertices in the cycle or None if no cycle
        """
        if not self.vertices:
            return None
        
        start = next(iter(self.vertices))
        
        # Initialize distances and parent
        distances: Dict[T, float] = {vertex: float('inf') for vertex in self.vertices}
        parent: Dict[T, Optional[T]] = {vertex: None for vertex in self.vertices}
        distances[start] = 0
        
        # Relax edges |V| times (one extra to detect cycle)
        for i in range(len(self.vertices)):
            updated = False
            for u, v, w in self.edges:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    parent[v] = u
                    updated = True
            
            if not updated:
                break
        
        # If no update in |V|-1 iterations, no negative cycle
        if not updated:
            return None
        
        # Find vertex in negative cycle
        cycle_vertex = None
        for u, v, w in self.edges:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                cycle_vertex = v
                break
        
        if cycle_vertex is None:
            return None
        
        # Reconstruct cycle
        visited: Set[T] = set()
        cycle = []
        current = cycle_vertex
        
        while current not in visited:
            visited.add(current)
            cycle.append(current)
            current = parent[current]
        
        # Extract cycle
        cycle_start = current
        cycle_index = cycle.index(cycle_start)
        return cycle[cycle_index:]


def main() -> None:
    """Demonstrate Bellman-Ford algorithm."""
    
    print("=== Bellman-Ford Algorithm Demo ===")
    
    # Create graph with positive weights
    bf = BellmanFord(directed=False)
    
    edges = [
        (0, 1, 4),
        (0, 2, 1),
        (1, 2, 2),
        (1, 3, 5),
        (2, 3, 2),
        (3, 4, 3),
        (4, 5, 1),
        (2, 5, 8)
    ]
    
    for u, v, w in edges:
        bf.add_edge(u, v, w)
    
    print("Graph edges (with weights):")
    for u, v, w in edges:
        print(f"  {u} --{w}--> {v}")
    
    # Shortest path
    print("\n--- Shortest Path ---")
    result = bf.shortest_path(0, 5)
    if result:
        distance, path = result
        print(f"Shortest path 0 -> 5: {path}")
        print(f"Distance: {distance}")
    
    # All shortest paths
    print("\n--- All Shortest Paths from 0 ---")
    all_paths = bf.all_shortest_paths(0)
    if all_paths:
        for vertex, (dist, path) in sorted(all_paths.items()):
            print(f"  0 -> {vertex}: distance={dist}, path={path}")
    
    # Negative cycle detection
    print("\n--- Negative Cycle Detection ---")
    print(f"Has negative cycle: {bf.has_negative_cycle()}")
    
    # Graph with negative weights
    print("\n=== Graph with Negative Weights ===")
    bf_neg = BellmanFord(directed=True)
    
    neg_edges = [
        (0, 1, 5),
        (0, 2, 4),
        (1, 3, 3),
        (2, 1, -6),
        (3, 2, 2)
    ]
    
    for u, v, w in neg_edges:
        bf_neg.add_edge(u, v, w)
    
    print("Graph edges (with negative weights):")
    for u, v, w in neg_edges:
        print(f"  {u} --{w}--> {v}")
    
    result_neg = bf_neg.shortest_path(0, 3)
    if result_neg:
        distance, path = result_neg
        print(f"Shortest path 0 -> 3: {path}")
        print(f"Distance: {distance}")
    else:
        print("No path or negative cycle detected")
    
    print(f"Has negative cycle: {bf_neg.has_negative_cycle()}")
    
    # Graph with negative cycle
    print("\n=== Graph with Negative Cycle ===")
    bf_cycle = BellmanFord(directed=True)
    
    cycle_edges = [
        (0, 1, 1),
        (1, 2, -1),
        (2, 0, -1)
    ]
    
    for u, v, w in cycle_edges:
        bf_cycle.add_edge(u, v, w)
    
    print("Graph edges (negative cycle):")
    for u, v, w in cycle_edges:
        print(f"  {u} --{w}--> {v}")
    
    print(f"Has negative cycle: {bf_cycle.has_negative_cycle()}")
    
    cycle = bf_cycle.find_negative_cycle()
    if cycle:
        print(f"Negative cycle: {cycle}")
    
    # String vertices
    print("\n=== Vertices as Strings ===")
    str_bf = BellmanFord(directed=False)
    
    str_edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2)
    ]
    
    for u, v, w in str_edges:
        str_bf.add_edge(u, v, w)
    
    result = str_bf.shortest_path("A", "E")
    if result:
        distance, path = result
        print(f"Shortest path A -> E: {path}")
        print(f"Distance: {distance}")


if __name__ == "__main__":
    main()
