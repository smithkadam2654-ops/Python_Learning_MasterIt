"""
Graph Data Structure - Graph implementation with BFS, DFS, and shortest path.
Features: Adjacency list, traversal algorithms, and path finding.
"""

from typing import Dict, List, Set, Optional, Tuple
from collections import deque
import heapq


class Graph:
    """Graph implementation using adjacency list."""
    
    def __init__(self, directed: bool = False) -> None:
        """
        Initialize graph.
        
        Args:
            directed: Whether graph is directed
        """
        self.directed = directed
        self.adjacency: Dict[Any, List[Tuple[Any, float]]] = {}
    
    def add_vertex(self, vertex: Any) -> None:
        """
        Add vertex to graph.
        
        Args:
            vertex: Vertex to add
        """
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []
    
    def add_edge(self, vertex1: Any, vertex2: Any, weight: float = 1.0) -> None:
        """
        Add edge between vertices.
        
        Args:
            vertex1: First vertex
            vertex2: Second vertex
            weight: Edge weight
        """
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        
        self.adjacency[vertex1].append((vertex2, weight))
        
        if not self.directed:
            self.adjacency[vertex2].append((vertex1, weight))
    
    def remove_vertex(self, vertex: Any) -> None:
        """
        Remove vertex from graph.
        
        Args:
            vertex: Vertex to remove
        """
        if vertex in self.adjacency:
            # Remove all edges to this vertex
            for v in self.adjacency:
                self.adjacency[v] = [(neighbor, w) for neighbor, w in self.adjacency[v] 
                                     if neighbor != vertex]
            # Remove vertex
            del self.adjacency[vertex]
    
    def remove_edge(self, vertex1: Any, vertex2: Any) -> None:
        """
        Remove edge between vertices.
        
        Args:
            vertex1: First vertex
            vertex2: Second vertex
        """
        if vertex1 in self.adjacency:
            self.adjacency[vertex1] = [(neighbor, w) for neighbor, w in self.adjacency[vertex1]
                                      if neighbor != vertex2]
        
        if not self.directed and vertex2 in self.adjacency:
            self.adjacency[vertex2] = [(neighbor, w) for neighbor, w in self.adjacency[vertex2]
                                      if neighbor != vertex1]
    
    def get_vertices(self) -> List[Any]:
        """Get all vertices."""
        return list(self.adjacency.keys())
    
    def get_edges(self) -> List[Tuple[Any, Any, float]]:
        """Get all edges."""
        edges = []
        for vertex in self.adjacency:
            for neighbor, weight in self.adjacency[vertex]:
                if not self.directed or (vertex, neighbor, weight) not in edges:
                    edges.append((vertex, neighbor, weight))
        return edges
    
    def get_neighbors(self, vertex: Any) -> List[Tuple[Any, float]]:
        """
        Get neighbors of vertex.
        
        Args:
            vertex: Vertex
            
        Returns:
            List of (neighbor, weight) tuples
        """
        return self.adjacency.get(vertex, [])
    
    def has_vertex(self, vertex: Any) -> bool:
        """Check if vertex exists."""
        return vertex in self.adjacency
    
    def has_edge(self, vertex1: Any, vertex2: Any) -> bool:
        """Check if edge exists."""
        if vertex1 not in self.adjacency:
            return False
        return any(neighbor == vertex2 for neighbor, _ in self.adjacency[vertex1])
    
    def bfs(self, start: Any) -> Dict[Any, int]:
        """
        Breadth-first search from start vertex.
        
        Args:
            start: Starting vertex
            
        Returns:
            Dictionary mapping vertex to distance from start
        """
        if start not in self.adjacency:
            return {}
        
        distances = {start: 0}
        queue = deque([start])
        visited = {start}
        
        while queue:
            current = queue.popleft()
            
            for neighbor, _ in self.adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        
        return distances
    
    def dfs(self, start: Any) -> List[Any]:
        """
        Depth-first search from start vertex.
        
        Args:
            start: Starting vertex
            
        Returns:
            List of vertices in DFS order
        """
        if start not in self.adjacency:
            return []
        
        visited = set()
        result = []
        
        def _dfs_recursive(vertex: Any) -> None:
            """Recursive DFS helper."""
            visited.add(vertex)
            result.append(vertex)
            
            for neighbor, _ in self.adjacency[vertex]:
                if neighbor not in visited:
                    _dfs_recursive(neighbor)
        
        _dfs_recursive(start)
        return result
    
    def shortest_path(self, start: Any, end: Any) -> Optional[List[Any]]:
        """
        Find shortest path using BFS (unweighted).
        
        Args:
            start: Starting vertex
            end: Ending vertex
            
        Returns:
            List of vertices in path or None if no path
        """
        if start not in self.adjacency or end not in self.adjacency:
            return None
        
        if start == end:
            return [start]
        
        queue = deque([start])
        visited = {start}
        parent = {start: None}
        
        while queue:
            current = queue.popleft()
            
            if current == end:
                # Reconstruct path
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]
            
            for neighbor, _ in self.adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        return None
    
    def dijkstra(self, start: Any) -> Dict[Any, float]:
        """
        Dijkstra's algorithm for shortest paths (weighted).
        
        Args:
            start: Starting vertex
            
        Returns:
            Dictionary mapping vertex to shortest distance
        """
        if start not in self.adjacency:
            return {}
        
        distances = {vertex: float('inf') for vertex in self.adjacency}
        distances[start] = 0
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for neighbor, weight in self.adjacency[current]:
                if neighbor not in visited:
                    new_dist = current_dist + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor))
        
        return distances
    
    def topological_sort(self) -> Optional[List[Any]]:
        """
        Topological sort (for DAGs).
        
        Returns:
            List of vertices in topological order or None if cycle detected
        """
        # Calculate in-degrees
        in_degree = {vertex: 0 for vertex in self.adjacency}
        for vertex in self.adjacency:
            for neighbor, _ in self.adjacency[vertex]:
                in_degree[neighbor] += 1
        
        # Find vertices with in-degree 0
        queue = deque([vertex for vertex, degree in in_degree.items() if degree == 0])
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor, _ in self.adjacency[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != len(self.adjacency):
            return None  # Cycle detected
        
        return result
    
    def is_connected(self) -> bool:
        """Check if graph is connected."""
        if not self.adjacency:
            return True
        
        start = next(iter(self.adjacency))
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            current = queue.popleft()
            for neighbor, _ in self.adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == len(self.adjacency)
    
    def has_cycle(self) -> bool:
        """Check if graph has cycle."""
        visited = set()
        recursion_stack = set()
        
        def _has_cycle_recursive(vertex: Any) -> bool:
            """Recursive cycle detection."""
            visited.add(vertex)
            recursion_stack.add(vertex)
            
            for neighbor, _ in self.adjacency[vertex]:
                if neighbor not in visited:
                    if _has_cycle_recursive(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True
            
            recursion_stack.remove(vertex)
            return False
        
        for vertex in self.adjacency:
            if vertex not in visited:
                if _has_cycle_recursive(vertex):
                    return True
        
        return False
    
    def __str__(self) -> str:
        """String representation."""
        lines = []
        for vertex in self.adjacency:
            neighbors = ", ".join(f"{neighbor}({weight})" for neighbor, weight in self.adjacency[vertex])
            lines.append(f"{vertex} -> [{neighbors}]")
        return "\n".join(lines)


def main() -> None:
    """Demonstrate graph functionality."""
    
    print("=== Graph Data Structure Demo ===")
    
    # Create undirected graph
    graph = Graph(directed=False)
    
    # Add vertices and edges
    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("B", "C", 1)
    graph.add_edge("B", "D", 5)
    graph.add_edge("C", "D", 8)
    graph.add_edge("C", "E", 10)
    graph.add_edge("D", "E", 2)
    
    print("Graph:")
    print(graph)
    
    print(f"\nVertices: {graph.get_vertices()}")
    print(f"Edges: {graph.get_edges()}")
    
    # BFS
    print(f"\nBFS from A: {graph.bfs('A')}")
    
    # DFS
    print(f"DFS from A: {graph.dfs('A')}")
    
    # Shortest path
    path = graph.shortest_path("A", "E")
    print(f"Shortest path A to E: {path}")
    
    # Dijkstra
    distances = graph.dijkstra("A")
    print(f"\nShortest distances from A:")
    for vertex, dist in distances.items():
        print(f"  {vertex}: {dist}")
    
    # Check connectivity
    print(f"\nIs connected: {graph.is_connected()}")
    
    print("\n=== Directed Graph (DAG) ===")
    
    # Create directed graph
    dag = Graph(directed=True)
    dag.add_edge("A", "B")
    dag.add_edge("A", "C")
    dag.add_edge("B", "D")
    dag.add_edge("C", "D")
    dag.add_edge("D", "E")
    
    print("DAG:")
    print(dag)
    
    # Topological sort
    topo = dag.topological_sort()
    print(f"\nTopological sort: {topo}")
    
    # Check for cycle
    print(f"Has cycle: {dag.has_cycle()}")
    
    # Add cycle
    dag.add_edge("E", "A")
    print(f"\nAfter adding cycle E -> A:")
    print(f"Has cycle: {dag.has_cycle()}")
    print(f"Topological sort: {dag.topological_sort()}")


if __name__ == "__main__":
    main()
