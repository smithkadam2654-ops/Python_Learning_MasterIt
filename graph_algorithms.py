"""
Graph Algorithms - Graph operations and algorithms.
Features: Graph representations, BFS, DFS, shortest paths, and MST.
"""

from typing import List, Dict, Set, Optional, TypeVar, Generic
from collections import deque
import heapq

T = TypeVar('T')


class Graph:
    """Graph implementation using adjacency list."""
    
    def __init__(self, directed: bool = False) -> None:
        """
        Initialize graph.
        
        Args:
            directed: Whether graph is directed
        """
        self.directed = directed
        self.adj_list: Dict[T, List[T]] = {}
    
    def add_vertex(self, vertex: T) -> None:
        """
        Add vertex to graph.
        
        Args:
            vertex: Vertex to add
        """
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
    
    def add_edge(self, u: T, v: T) -> None:
        """
        Add edge between vertices.
        
        Args:
            u: First vertex
            v: Second vertex
        """
        self.add_vertex(u)
        self.add_vertex(v)
        
        self.adj_list[u].append(v)
        
        if not self.directed:
            self.adj_list[v].append(u)
    
    def remove_edge(self, u: T, v: T) -> None:
        """
        Remove edge between vertices.
        
        Args:
            u: First vertex
            v: Second vertex
        """
        if u in self.adj_list and v in self.adj_list[u]:
            self.adj_list[u].remove(v)
        
        if not self.directed and v in self.adj_list and u in self.adj_list[v]:
            self.adj_list[v].remove(u)
    
    def remove_vertex(self, vertex: T) -> None:
        """
        Remove vertex from graph.
        
        Args:
            vertex: Vertex to remove
        """
        if vertex in self.adj_list:
            # Remove all edges to this vertex
            for v in self.adj_list:
                if vertex in self.adj_list[v]:
                    self.adj_list[v].remove(vertex)
            
            del self.adj_list[vertex]
    
    def get_vertices(self) -> List[T]:
        """Get all vertices."""
        return list(self.adj_list.keys())
    
    def get_edges(self) -> List[tuple]:
        """Get all edges."""
        edges = []
        
        for u in self.adj_list:
            for v in self.adj_list[u]:
                if not self.directed and u < v:
                    edges.append((u, v))
                elif self.directed:
                    edges.append((u, v))
        
        return edges
    
    def __repr__(self) -> str:
        return f"Graph({self.adj_list})"


class WeightedGraph:
    """Weighted graph implementation."""
    
    def __init__(self, directed: bool = False) -> None:
        """
        Initialize weighted graph.
        
        Args:
            directed: Whether graph is directed
        """
        self.directed = directed
        self.adj_list: Dict[T, List[tuple]] = {}
    
    def add_vertex(self, vertex: T) -> None:
        """Add vertex to graph."""
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
    
    def add_edge(self, u: T, v: T, weight: float) -> None:
        """
        Add weighted edge.
        
        Args:
            u: First vertex
            v: Second vertex
            weight: Edge weight
        """
        self.add_vertex(u)
        self.add_vertex(v)
        
        self.adj_list[u].append((v, weight))
        
        if not self.directed:
            self.adj_list[v].append((u, weight))
    
    def get_vertices(self) -> List[T]:
        """Get all vertices."""
        return list(self.adj_list.keys())


class GraphAlgorithms:
    """Graph algorithm implementations."""
    
    @staticmethod
    def bfs(graph: Graph, start: T) -> Dict[T, int]:
        """
        Breadth-first search traversal.
        
        Args:
            graph: Graph to traverse
            start: Starting vertex
            
        Returns:
            Dictionary of vertex to distance from start
        """
        distances = {v: -1 for v in graph.get_vertices()}
        distances[start] = 0
        
        queue = deque([start])
        visited = {start}
        
        while queue:
            vertex = queue.popleft()
            
            for neighbor in graph.adj_list.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    distances[neighbor] = distances[vertex] + 1
                    queue.append(neighbor)
        
        return distances
    
    @staticmethod
    def dfs(graph: Graph, start: T) -> List[T]:
        """
        Depth-first search traversal (iterative).
        
        Args:
            graph: Graph to traverse
            start: Starting vertex
            
        Returns:
            List of vertices in DFS order
        """
        visited = set()
        result = []
        stack = [start]
        
        while stack:
            vertex = stack.pop()
            
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                
                # Add neighbors in reverse order for correct DFS
                for neighbor in reversed(graph.adj_list.get(vertex, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    @staticmethod
    def dfs_recursive(graph: Graph, start: T, visited: Set[T] = None) -> List[T]:
        """
        Depth-first search traversal (recursive).
        
        Args:
            graph: Graph to traverse
            start: Starting vertex
            visited: Set of visited vertices (for recursion)
            
        Returns:
            List of vertices in DFS order
        """
        if visited is None:
            visited = set()
        
        visited.add(start)
        result = [start]
        
        for neighbor in graph.adj_list.get(start, []):
            if neighbor not in visited:
                result.extend(GraphAlgorithms.dfs_recursive(graph, neighbor, visited))
        
        return result
    
    @staticmethod
    def has_path(graph: Graph, start: T, end: T) -> bool:
        """
        Check if path exists between two vertices using BFS.
        
        Args:
            graph: Graph to check
            start: Starting vertex
            end: Target vertex
            
        Returns:
            True if path exists
        """
        distances = GraphAlgorithms.bfs(graph, start)
        return distances.get(end, -1) != -1
    
    @staticmethod
    def shortest_path(graph: Graph, start: T, end: T) -> Optional[List[T]]:
        """
        Find shortest path using BFS.
        
        Args:
            graph: Graph to search
            start: Starting vertex
            end: Target vertex
            
        Returns:
            Path as list or None if no path
        """
        if start == end:
            return [start]
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            vertex, path = queue.popleft()
            
            for neighbor in graph.adj_list.get(vertex, []):
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    @staticmethod
    def is_connected(graph: Graph) -> bool:
        """
        Check if graph is connected.
        
        Args:
            graph: Graph to check
            
        Returns:
            True if connected
        """
        if not graph.get_vertices():
            return True
        
        start = graph.get_vertices()[0]
        distances = GraphAlgorithms.bfs(graph, start)
        
        return all(d != -1 for d in distances.values())
    
    @staticmethod
    def connected_components(graph: Graph) -> List[List[T]]:
        """
        Find connected components.
        
        Args:
            graph: Graph to analyze
            
        Returns:
            List of connected components
        """
        visited = set()
        components = []
        
        for vertex in graph.get_vertices():
            if vertex not in visited:
                component = GraphAlgorithms.dfs(graph, vertex)
                visited.update(component)
                components.append(component)
        
        return components
    
    @staticmethod
    def has_cycle(graph: Graph) -> bool:
        """
        Detect cycle in undirected graph using DFS.
        
        Args:
            graph: Graph to check
            
        Returns:
            True if cycle exists
        """
        visited = set()
        
        def dfs_cycle(vertex: T, parent: T) -> bool:
            visited.add(vertex)
            
            for neighbor in graph.adj_list.get(vertex, []):
                if neighbor not in visited:
                    if dfs_cycle(neighbor, vertex):
                        return True
                elif neighbor != parent:
                    return True
            
            return False
        
        for vertex in graph.get_vertices():
            if vertex not in visited:
                if dfs_cycle(vertex, None):
                    return True
        
        return False
    
    @staticmethod
    def topological_sort(graph: Graph) -> Optional[List[T]]:
        """
        Topological sort using Kahn's algorithm.
        
        Args:
            graph: Directed graph to sort
            
        Returns:
            Topological order or None if cycle exists
        """
        if not graph.directed:
            return None
        
        # Calculate in-degrees
        in_degree = {v: 0 for v in graph.get_vertices()}
        
        for u in graph.adj_list:
            for v in graph.adj_list[u]:
                in_degree[v] += 1
        
        # Initialize queue with vertices of in-degree 0
        queue = deque([v for v, d in in_degree.items() if d == 0])
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor in graph.adj_list.get(vertex, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != len(graph.get_vertices()):
            return None  # Cycle exists
        
        return result
    
    @staticmethod
    def dijkstra(graph: WeightedGraph, start: T) -> Dict[T, float]:
        """
        Dijkstra's shortest path algorithm.
        
        Args:
            graph: Weighted graph
            start: Starting vertex
            
        Returns:
            Dictionary of vertex to shortest distance
        """
        distances = {v: float('inf') for v in graph.get_vertices()}
        distances[start] = 0
        
        # Priority queue: (distance, vertex)
        pq = [(0, start)]
        visited = set()
        
        while pq:
            dist, vertex = heapq.heappop(pq)
            
            if vertex in visited:
                continue
            
            visited.add(vertex)
            
            for neighbor, weight in graph.adj_list.get(vertex, []):
                if neighbor not in visited:
                    new_dist = dist + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor))
        
        return distances
    
    @staticmethod
    def prim_mst(graph: WeightedGraph, start: T = None) -> tuple:
        """
        Prim's algorithm for MST.
        
        Args:
            graph: Weighted graph
            start: Starting vertex (optional)
            
        Returns:
            Tuple of (total_weight, edges)
        """
        if not graph.get_vertices():
            return (0, [])
        
        if start is None:
            start = graph.get_vertices()[0]
        
        visited = {start}
        edges = []
        total_weight = 0
        
        # Priority queue: (weight, u, v)
        pq = []
        
        for neighbor, weight in graph.adj_list.get(start, []):
            heapq.heappush(pq, (weight, start, neighbor))
        
        while pq and len(visited) < len(graph.get_vertices()):
            weight, u, v = heapq.heappop(pq)
            
            if v in visited:
                continue
            
            visited.add(v)
            edges.append((u, v, weight))
            total_weight += weight
            
            for neighbor, w in graph.adj_list.get(v, []):
                if neighbor not in visited:
                    heapq.heappush(pq, (w, v, neighbor))
        
        if len(visited) != len(graph.get_vertices()):
            return (0, [])  # Graph is not connected
        
        return (total_weight, edges)
    
    @staticmethod
    def kruskal_mst(graph: WeightedGraph) -> tuple:
        """
        Kruskal's algorithm for MST using Union-Find.
        
        Args:
            graph: Weighted graph
            
        Returns:
            Tuple of (total_weight, edges)
        """
        vertices = graph.get_vertices()
        if not vertices:
            return (0, [])
        
        # Get all edges
        edges = []
        for u in graph.adj_list:
            for v, weight in graph.adj_list[u]:
                if not graph.directed and u < v:
                    edges.append((weight, u, v))
                elif graph.directed:
                    edges.append((weight, u, v))
        
        # Sort by weight
        edges.sort()
        
        # Union-Find
        parent = {v: v for v in vertices}
        
        def find(v: T) -> T:
            if parent[v] != v:
                parent[v] = find(parent[v])
            return parent[v]
        
        def union(u: T, v: T) -> None:
            root_u = find(u)
            root_v = find(v)
            if root_u != root_v:
                parent[root_u] = root_v
        
        mst_edges = []
        total_weight = 0
        
        for weight, u, v in edges:
            if find(u) != find(v):
                union(u, v)
                mst_edges.append((u, v, weight))
                total_weight += weight
        
        # Check if all vertices are connected
        root = find(vertices[0])
        if any(find(v) != root for v in vertices):
            return (0, [])  # Graph is not connected
        
        return (total_weight, mst_edges)


def main() -> None:
    """Demonstrate graph algorithms."""
    
    print("=== Graph Algorithms Demo ===")
    
    # Create graph
    graph = Graph(directed=False)
    edges = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)]
    
    for u, v in edges:
        graph.add_edge(u, v)
    
    print(f"Graph: {graph}")
    print(f"Vertices: {graph.get_vertices()}")
    print(f"Edges: {graph.get_edges()}")
    
    # BFS
    print("\n--- BFS ---")
    distances = GraphAlgorithms.bfs(graph, 0)
    print(f"Distances from 0: {distances}")
    
    # DFS
    print("\n--- DFS ---")
    dfs_order = GraphAlgorithms.dfs(graph, 0)
    print(f"DFS order from 0: {dfs_order}")
    
    # Path
    print("\n--- Shortest Path ---")
    path = GraphAlgorithms.shortest_path(graph, 0, 4)
    print(f"Path from 0 to 4: {path}")
    
    # Connectivity
    print("\n--- Connectivity ---")
    print(f"Is connected: {GraphAlgorithms.is_connected(graph)}")
    
    # Connected components
    print("\n--- Connected Components ---")
    components = GraphAlgorithms.connected_components(graph)
    print(f"Components: {components}")
    
    # Cycle detection
    print("\n--- Cycle Detection ---")
    print(f"Has cycle: {GraphAlgorithms.has_cycle(graph)}")
    
    # Weighted graph - Dijkstra
    print("\n--- Dijkstra ---")
    wg = WeightedGraph(directed=False)
    weighted_edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (2, 3, 5), (3, 4, 3)]
    
    for u, v, w in weighted_edges:
        wg.add_edge(u, v, w)
    
    distances = GraphAlgorithms.dijkstra(wg, 0)
    print(f"Shortest distances from 0: {distances}")
    
    # MST
    print("\n--- Prim's MST ---")
    total_weight, edges = GraphAlgorithms.prim_mst(wg, 0)
    print(f"Total weight: {total_weight}")
    print(f"MST edges: {edges}")
    
    print("\n--- Kruskal's MST ---")
    total_weight, edges = GraphAlgorithms.kruskal_mst(wg)
    print(f"Total weight: {total_weight}")
    print(f"MST edges: {edges}")
    
    # Topological sort (directed graph)
    print("\n--- Topological Sort ---")
    dag = Graph(directed=True)
    dag_edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
    
    for u, v in dag_edges:
        dag.add_edge(u, v)
    
    topo_order = GraphAlgorithms.topological_sort(dag)
    print(f"Topological order: {topo_order}")


if __name__ == "__main__":
    main()
