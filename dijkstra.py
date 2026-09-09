"""
Dijkstra's Algorithm - Shortest path algorithm for weighted graphs.
Features: Priority queue optimization, path reconstruction, and multiple targets.
"""

from typing import List, Dict, Set, Optional, TypeVar, Generic
import heapq

T = TypeVar('T')


class Dijkstra:
    """Dijkstra's shortest path algorithm implementation."""
    
    def __init__(self, directed: bool = False) -> None:
        """
        Initialize weighted graph.
        
        Args:
            directed: Whether graph is directed
        """
        self.directed = directed
        self.adj_list: Dict[T, List[tuple]] = {}
    
    def add_edge(self, u: T, v: T, weight: float) -> None:
        """
        Add weighted edge to graph.
        
        Args:
            u: First vertex
            v: Second vertex
            weight: Edge weight (must be non-negative)
        """
        if weight < 0:
            raise ValueError("Dijkstra's algorithm requires non-negative weights")
        
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))
    
    def shortest_path(self, start: T, end: T) -> Optional[tuple]:
        """
        Find shortest path using Dijkstra's algorithm.
        
        Args:
            start: Starting vertex
            end: Target vertex
            
        Returns:
            Tuple of (distance, path) or None if no path exists
        """
        if start not in self.adj_list or end not in self.adj_list:
            return None
        
        # Priority queue: (distance, vertex)
        pq = [(0, start)]
        distances: Dict[T, float] = {vertex: float('inf') for vertex in self.adj_list}
        distances[start] = 0
        parent: Dict[T, Optional[T]] = {vertex: None for vertex in self.adj_list}
        visited: Set[T] = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == end:
                # Reconstruct path
                path = []
                node = end
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return (current_dist, path[::-1])
            
            for neighbor, weight in self.adj_list[current]:
                if neighbor in visited:
                    continue
                
                new_dist = current_dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parent[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return None
    
    def shortest_distance(self, start: T, end: T) -> Optional[float]:
        """
        Find shortest distance without path reconstruction.
        
        Args:
            start: Starting vertex
            end: Target vertex
            
        Returns:
            Shortest distance or None if no path exists
        """
        result = self.shortest_path(start, end)
        return result[0] if result else None
    
    def all_shortest_paths(self, start: T) -> Dict[T, tuple]:
        """
        Find shortest paths from start to all vertices.
        
        Args:
            start: Starting vertex
            
        Returns:
            Dictionary mapping vertex to (distance, path)
        """
        if start not in self.adj_list:
            return {}
        
        pq = [(0, start)]
        distances: Dict[T, float] = {vertex: float('inf') for vertex in self.adj_list}
        distances[start] = 0
        parent: Dict[T, Optional[T]] = {vertex: None for vertex in self.adj_list}
        visited: Set[T] = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for neighbor, weight in self.adj_list[current]:
                if neighbor in visited:
                    continue
                
                new_dist = current_dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parent[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        # Reconstruct all paths
        result = {}
        for vertex in self.adj_list:
            if distances[vertex] != float('inf'):
                path = []
                node = vertex
                while node is not None:
                    path.append(node)
                    node = parent[node]
                result[vertex] = (distances[vertex], path[::-1])
        
        return result
    
    def k_shortest_paths(self, start: T, end: T, k: int) -> List[tuple]:
        """
        Find k shortest paths using Yen's algorithm.
        
        Args:
            start: Starting vertex
            end: Target vertex
            k: Number of paths to find
            
        Returns:
            List of (distance, path) tuples
        """
        # First shortest path
        first_path = self.shortest_path(start, end)
        if not first_path:
            return []
        
        paths = [first_path]
        candidates = []
        
        for i in range(1, k):
            # For each path in shortest paths
            for j in range(len(paths[-1][1]) - 1):
                # Spur node
                spur_node = paths[-1][1][j]
                root_path = paths[-1][1][:j + 1]
                
                # Remove edges from root path
                removed_edges = []
                for path_dist, path in paths:
                    if len(path) > j and root_path == path[:j + 1]:
                        # Remove edge
                        for idx, (neighbor, weight) in enumerate(self.adj_list[path[j]]):
                            if neighbor == path[j + 1]:
                                removed_edges.append((path[j], idx, (neighbor, weight)))
                                self.adj_list[path[j]].pop(idx)
                                break
                
                # Remove vertices from root path (except spur node)
                removed_vertices = []
                for vertex in root_path[:-1]:
                    if vertex in self.adj_list:
                        removed_vertices.append(vertex)
                        del self.adj_list[vertex]
                
                # Find spur path
                spur_path = self.shortest_path(spur_node, end)
                
                # Restore graph
                for vertex in removed_vertices:
                    self.adj_list[vertex] = []
                
                for u, idx, edge in removed_edges:
                    self.adj_list[u].insert(idx, edge)
                
                if spur_path:
                    # Complete path
                    total_path = root_path[:-1] + spur_path[1]
                    total_dist = sum(self._get_edge_weight(total_path[i], total_path[i + 1]) 
                                   for i in range(len(total_path) - 1))
                    
                    # Add to candidates if not duplicate
                    if (total_dist, total_path) not in candidates:
                        candidates.append((total_dist, total_path))
            
            if not candidates:
                break
            
            # Get shortest candidate
            candidates.sort()
            paths.append(candidates.pop(0))
        
        return paths[:k]
    
    def _get_edge_weight(self, u: T, v: T) -> float:
        """Get weight of edge between u and v."""
        for neighbor, weight in self.adj_list[u]:
            if neighbor == v:
                return weight
        return float('inf')


def main() -> None:
    """Demonstrate Dijkstra's algorithm."""
    
    print("=== Dijkstra's Algorithm Demo ===")
    
    # Create graph
    dijkstra = Dijkstra(directed=False)
    
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
        dijkstra.add_edge(u, v, w)
    
    print("Graph edges (with weights):")
    for u, v, w in edges:
        print(f"  {u} --{w}--> {v}")
    
    # Shortest path
    print("\n--- Shortest Path ---")
    result = dijkstra.shortest_path(0, 5)
    if result:
        distance, path = result
        print(f"Shortest path 0 -> 5: {path}")
        print(f"Distance: {distance}")
    
    # Shortest distance
    print("\n--- Shortest Distance ---")
    distance = dijkstra.shortest_distance(0, 3)
    print(f"Distance 0 -> 3: {distance}")
    
    # All shortest paths from source
    print("\n--- All Shortest Paths from 0 ---")
    all_paths = dijkstra.all_shortest_paths(0)
    for vertex, (dist, path) in sorted(all_paths.items()):
        print(f"  0 -> {vertex}: distance={dist}, path={path}")
    
    # K shortest paths
    print("\n--- K Shortest Paths ---")
    k_paths = dijkstra.k_shortest_paths(0, 5, 3)
    for i, (dist, path) in enumerate(k_paths, 1):
        print(f"  Path {i}: {path} (distance={dist})")
    
    # Directed graph
    print("\n=== Directed Graph ===")
    directed_dijkstra = Dijkstra(directed=True)
    
    directed_edges = [
        (0, 1, 5),
        (0, 2, 3),
        (1, 3, 6),
        (2, 1, 2),
        (2, 3, 7),
        (2, 4, 4),
        (3, 4, 2),
        (4, 5, 3)
    ]
    
    for u, v, w in directed_edges:
        directed_dijkstra.add_edge(u, v, w)
    
    result = directed_dijkstra.shortest_path(0, 5)
    if result:
        distance, path = result
        print(f"Shortest path 0 -> 5: {path}")
        print(f"Distance: {distance}")
    
    # String vertices
    print("\n=== Vertices as Strings ===")
    str_dijkstra = Dijkstra(directed=False)
    
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
        str_dijkstra.add_edge(u, v, w)
    
    result = str_dijkstra.shortest_path("A", "E")
    if result:
        distance, path = result
        print(f"Shortest path A -> E: {path}")
        print(f"Distance: {distance}")


if __name__ == "__main__":
    main()
