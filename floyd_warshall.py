"""
Floyd-Warshall Algorithm - All-pairs shortest path algorithm.
Features: Dynamic programming, negative edge support, and path reconstruction.
"""

from typing import List, Dict, Optional, TypeVar, Generic
import math

T = TypeVar('T')


class FloydWarshall:
    """Floyd-Warshall all-pairs shortest path implementation."""
    
    def __init__(self, vertices: List[T]) -> None:
        """
        Initialize graph with vertices.
        
        Args:
            vertices: List of vertices
        """
        self.vertices = vertices
        self.vertex_index = {v: i for i, v in enumerate(vertices)}
        self.dist: List[List[float]] = [[math.inf] * len(vertices) for _ in range(len(vertices))]
        self.next: List[List[Optional[int]]] = [[None] * len(vertices) for _ in range(len(vertices))]
        
        # Initialize diagonal to 0
        for i in range(len(vertices)):
            self.dist[i][i] = 0
            self.next[i][i] = i
    
    def add_edge(self, u: T, v: T, weight: float) -> None:
        """
        Add weighted edge to graph.
        
        Args:
            u: First vertex
            v: Second vertex
            weight: Edge weight
        """
        if u not in self.vertex_index or v not in self.vertex_index:
            raise ValueError("Vertex not found")
        
        i = self.vertex_index[u]
        j = self.vertex_index[v]
        self.dist[i][j] = weight
        self.next[i][j] = j
    
    def compute_shortest_paths(self) -> None:
        """Compute all-pairs shortest paths using Floyd-Warshall."""
        n = len(self.vertices)
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if self.dist[i][k] + self.dist[k][j] < self.dist[i][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        self.next[i][j] = self.next[i][k]
    
    def shortest_path(self, u: T, v: T) -> Optional[tuple]:
        """
        Get shortest path between two vertices.
        
        Args:
            u: Starting vertex
            v: Target vertex
            
        Returns:
            Tuple of (distance, path) or None if no path
        """
        if u not in self.vertex_index or v not in self.vertex_index:
            return None
        
        i = self.vertex_index[u]
        j = self.vertex_index[v]
        
        if self.dist[i][j] == math.inf:
            return None
        
        # Reconstruct path
        path = []
        if self.next[i][j] is None:
            return None
        
        current = i
        while current != j:
            path.append(self.vertices[current])
            current = self.next[i][j] if self.next[i][j] is not None else j
            if current == j:
                path.append(self.vertices[j])
                break
        
        return (self.dist[i][j], path)
    
    def shortest_distance(self, u: T, v: T) -> Optional[float]:
        """
        Get shortest distance between two vertices.
        
        Args:
            u: Starting vertex
            v: Target vertex
            
        Returns:
            Shortest distance or None if no path
        """
        if u not in self.vertex_index or v not in self.vertex_index:
            return None
        
        i = self.vertex_index[u]
        j = self.vertex_index[v]
        
        return None if self.dist[i][j] == math.inf else self.dist[i][j]
    
    def all_pairs_shortest_paths(self) -> Dict[tuple, tuple]:
        """
        Get all-pairs shortest paths.
        
        Returns:
            Dictionary mapping (u, v) to (distance, path)
        """
        result = {}
        
        for u in self.vertices:
            for v in self.vertices:
                path_result = self.shortest_path(u, v)
                if path_result:
                    result[(u, v)] = path_result
        
        return result
    
    def has_negative_cycle(self) -> bool:
        """
        Check if graph has a negative cycle.
        
        Returns:
            True if negative cycle exists
        """
        n = len(self.vertices)
        
        for i in range(n):
            if self.dist[i][i] < 0:
                return True
        
        return False
    
    def get_distance_matrix(self) -> List[List[float]]:
        """
        Get distance matrix.
        
        Returns:
            2D matrix of distances
        """
        return self.dist
    
    def get_transitive_closure(self) -> List[List[bool]]:
        """
        Get transitive closure of graph.
        
        Returns:
            Boolean matrix indicating reachability
        """
        n = len(self.vertices)
        closure = [[False] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                closure[i][j] = self.dist[i][j] != math.inf
        
        return closure


def main() -> None:
    """Demonstrate Floyd-Warshall algorithm."""
    
    print("=== Floyd-Warshall Algorithm Demo ===")
    
    # Create graph
    vertices = [0, 1, 2, 3]
    fw = FloydWarshall(vertices)
    
    edges = [
        (0, 1, 5),
        (0, 3, 10),
        (1, 2, 3),
        (2, 3, 1)
    ]
    
    for u, v, w in edges:
        fw.add_edge(u, v, w)
    
    print("Graph edges (with weights):")
    for u, v, w in edges:
        print(f"  {u} --{w}--> {v}")
    
    # Compute shortest paths
    print("\n--- Computing Shortest Paths ---")
    fw.compute_shortest_paths()
    
    # Shortest path between specific vertices
    print("\n--- Shortest Paths ---")
    test_pairs = [(0, 2), (0, 3), (1, 3), (2, 0)]
    for u, v in test_pairs:
        result = fw.shortest_path(u, v)
        if result:
            distance, path = result
            print(f"{u} -> {v}: distance={distance}, path={path}")
        else:
            print(f"{u} -> {v}: No path")
    
    # All pairs shortest paths
    print("\n--- All Pairs Shortest Paths ---")
    all_paths = fw.all_pairs_shortest_paths()
    for (u, v), (dist, path) in sorted(all_paths.items()):
        print(f"{u} -> {v}: {dist} via {path}")
    
    # Distance matrix
    print("\n--- Distance Matrix ---")
    dist_matrix = fw.get_distance_matrix()
    print("    ", end="")
    for v in vertices:
        print(f"{v:6}", end="")
    print()
    for i, row in enumerate(dist_matrix):
        print(f"{vertices[i]}: ", end="")
        for val in row:
            if val == math.inf:
                print(f"  INF ", end="")
            else:
                print(f"{val:6}", end="")
        print()
    
    # Transitive closure
    print("\n--- Transitive Closure ---")
    closure = fw.get_transitive_closure()
    print("    ", end="")
    for v in vertices:
        print(f"{v:3}", end="")
    print()
    for i, row in enumerate(closure):
        print(f"{vertices[i]}: ", end="")
        for val in row:
            print(f"{int(val):3}", end="")
        print()
    
    # Negative cycle detection
    print("\n--- Negative Cycle Detection ---")
    print(f"Has negative cycle: {fw.has_negative_cycle()}")
    
    # Graph with negative weights
    print("\n=== Graph with Negative Weights ===")
    vertices_neg = [0, 1, 2, 3]
    fw_neg = FloydWarshall(vertices_neg)
    
    neg_edges = [
        (0, 1, 1),
        (1, 2, -1),
        (2, 3, -1),
        (3, 0, -1)
    ]
    
    for u, v, w in neg_edges:
        fw_neg.add_edge(u, v, w)
    
    print("Graph edges (with negative weights):")
    for u, v, w in neg_edges:
        print(f"  {u} --{w}--> {v}")
    
    fw_neg.compute_shortest_paths()
    print(f"Has negative cycle: {fw_neg.has_negative_cycle()}")
    
    # String vertices
    print("\n=== Vertices as Strings ===")
    str_vertices = ["A", "B", "C", "D"]
    str_fw = FloydWarshall(str_vertices)
    
    str_edges = [
        ("A", "B", 3),
        ("A", "C", 8),
        ("B", "C", 4),
        ("B", "D", 2),
        ("C", "D", 1)
    ]
    
    for u, v, w in str_edges:
        str_fw.add_edge(u, v, w)
    
    str_fw.compute_shortest_paths()
    
    result = str_fw.shortest_path("A", "D")
    if result:
        distance, path = result
        print(f"Shortest path A -> D: {path}")
        print(f"Distance: {distance}")


if __name__ == "__main__":
    main()
