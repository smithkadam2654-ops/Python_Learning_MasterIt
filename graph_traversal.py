"""
Graph Traversal - BFS and DFS algorithms for graph exploration.
Features: Adjacency list representation, path finding, and cycle detection.
"""

from typing import Dict, List, Set, Optional, Any
from collections import deque
from dataclasses import dataclass


@dataclass
class Graph:
    """Graph implementation using adjacency list."""
    
    def __init__(self, directed: bool = False) -> None:
        """
        Initialize graph.
        
        Args:
            directed: Whether the graph is directed (default: False)
        """
        self.adjacency_list: Dict[Any, List[Any]] = {}
        self.directed = directed
    
    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the graph."""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
    
    def add_edge(self, vertex1: Any, vertex2: Any) -> None:
        """Add an edge between two vertices."""
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        
        self.adjacency_list[vertex1].append(vertex2)
        
        if not self.directed:
            self.adjacency_list[vertex2].append(vertex1)
    
    def get_vertices(self) -> List[Any]:
        """Return all vertices in the graph."""
        return list(self.adjacency_list.keys())
    
    def get_edges(self) -> List[tuple]:
        """Return all edges in the graph."""
        edges = []
        for vertex in self.adjacency_list:
            for neighbor in self.adjacency_list[vertex]:
                if not self.directed:
                    # Avoid duplicates in undirected graph
                    if (neighbor, vertex) not in edges:
                        edges.append((vertex, neighbor))
                else:
                    edges.append((vertex, neighbor))
        return edges
    
    def bfs(self, start: Any) -> List[Any]:
        """
        Breadth-First Search traversal.
        
        Args:
            start: Starting vertex for traversal
            
        Returns:
            List of vertices in BFS order
        """
        if start not in self.adjacency_list:
            raise ValueError("Start vertex not in graph")
        
        visited: Set[Any] = set()
        queue = deque([start])
        result: List[Any] = []
        
        visited.add(start)
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start: Any) -> List[Any]:
        """
        Depth-First Search traversal (iterative).
        
        Args:
            start: Starting vertex for traversal
            
        Returns:
            List of vertices in DFS order
        """
        if start not in self.adjacency_list:
            raise ValueError("Start vertex not in graph")
        
        visited: Set[Any] = set()
        stack = [start]
        result: List[Any] = []
        
        while stack:
            vertex = stack.pop()
            
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                
                # Add neighbors in reverse order for consistent traversal
                for neighbor in reversed(self.adjacency_list[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    def dfs_recursive(self, start: Any, visited: Optional[Set[Any]] = None) -> List[Any]:
        """
        Depth-First Search traversal (recursive).
        
        Args:
            start: Starting vertex for traversal
            visited: Set of visited vertices (for internal use)
            
        Returns:
            List of vertices in DFS order
        """
        if visited is None:
            visited = set()
        
        if start not in self.adjacency_list:
            raise ValueError("Start vertex not in graph")
        
        visited.add(start)
        result = [start]
        
        for neighbor in self.adjacency_list[start]:
            if neighbor not in visited:
                result.extend(self.dfs_recursive(neighbor, visited))
        
        return result
    
    def shortest_path(self, start: Any, end: Any) -> Optional[List[Any]]:
        """
        Find shortest path between two vertices using BFS.
        
        Args:
            start: Starting vertex
            end: Target vertex
            
        Returns:
            List of vertices representing the shortest path, or None if no path exists
        """
        if start not in self.adjacency_list or end not in self.adjacency_list:
            return None
        
        if start == end:
            return [start]
        
        visited: Set[Any] = set()
        queue = deque([(start, [start])])
        visited.add(start)
        
        while queue:
            vertex, path = queue.popleft()
            
            for neighbor in self.adjacency_list[vertex]:
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def has_cycle(self) -> bool:
        """
        Detect if the graph contains a cycle using DFS.
        
        Returns:
            True if cycle exists, False otherwise
        """
        visited: Set[Any] = set()
        
        for vertex in self.adjacency_list:
            if vertex not in visited:
                if self._has_cycle_dfs(vertex, visited, None):
                    return True
        
        return False
    
    def _has_cycle_dfs(self, vertex: Any, visited: Set[Any], parent: Optional[Any]) -> bool:
        """Helper method for cycle detection."""
        visited.add(vertex)
        
        for neighbor in self.adjacency_list[vertex]:
            if neighbor not in visited:
                if self._has_cycle_dfs(neighbor, visited, vertex):
                    return True
            elif neighbor != parent:
                return True
        
        return False
    
    def __str__(self) -> str:
        """String representation of the graph."""
        lines = []
        for vertex, neighbors in self.adjacency_list.items():
            lines.append(f"{vertex}: {neighbors}")
        return "\n".join(lines)


def main() -> None:
    """Demonstrate graph traversal algorithms."""
    
    # Create an undirected graph
    print("=== Undirected Graph ===")
    graph = Graph(directed=False)
    
    # Add edges
    edges = [
        ('A', 'B'), ('A', 'C'), ('B', 'D'),
        ('B', 'E'), ('C', 'F'), ('E', 'F')
    ]
    
    for v1, v2 in edges:
        graph.add_edge(v1, v2)
    
    print(f"Graph:\n{graph}")
    print(f"\nVertices: {graph.get_vertices()}")
    print(f"Edges: {graph.get_edges()}")
    
    # BFS traversal
    print(f"\nBFS from 'A': {graph.bfs('A')}")
    
    # DFS traversal
    print(f"DFS (iterative) from 'A': {graph.dfs('A')}")
    print(f"DFS (recursive) from 'A': {graph.dfs_recursive('A')}")
    
    # Shortest path
    print(f"Shortest path from 'A' to 'F': {graph.shortest_path('A', 'F')}")
    print(f"Shortest path from 'A' to 'D': {graph.shortest_path('A', 'D')}")
    
    # Cycle detection
    print(f"Has cycle: {graph.has_cycle()}")
    
    # Add cycle
    graph.add_edge('D', 'A')
    print(f"After adding edge D-A, has cycle: {graph.has_cycle()}")
    
    # Directed graph example
    print("\n=== Directed Graph ===")
    directed_graph = Graph(directed=True)
    
    directed_edges = [
        (1, 2), (1, 3), (2, 4), (3, 4), (4, 5)
    ]
    
    for v1, v2 in directed_edges:
        directed_graph.add_edge(v1, v2)
    
    print(f"Graph:\n{directed_graph}")
    print(f"BFS from 1: {directed_graph.bfs(1)}")
    print(f"DFS from 1: {directed_graph.dfs(1)}")
    print(f"Shortest path from 1 to 5: {directed_graph.shortest_path(1, 5)}")


if __name__ == "__main__":
    main()
