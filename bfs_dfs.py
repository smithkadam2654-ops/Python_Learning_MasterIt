"""
BFS and DFS - Graph traversal algorithms.
Features: Breadth-first search, depth-first search, and various applications.
"""

from typing import List, Dict, Set, Optional, TypeVar, Generic
from collections import deque

T = TypeVar('T')


class GraphTraversal:
    """Graph traversal implementation using adjacency list."""
    
    def __init__(self, directed: bool = False) -> None:
        """
        Initialize graph.
        
        Args:
            directed: Whether graph is directed
        """
        self.directed = directed
        self.adj_list: Dict[T, List[T]] = {}
    
    def add_edge(self, u: T, v: T) -> None:
        """
        Add edge to graph.
        
        Args:
            u: First vertex
            v: Second vertex
        """
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        
        self.adj_list[u].append(v)
        if not self.directed:
            self.adj_list[v].append(u)
    
    def bfs(self, start: T) -> List[T]:
        """
        Breadth-first search traversal.
        
        Args:
            start: Starting vertex
            
        Returns:
            BFS traversal order
        """
        if start not in self.adj_list:
            return []
        
        visited: Set[T] = set()
        result: List[T] = []
        queue = deque([start])
        visited.add(start)
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor in self.adj_list[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def bfs_shortest_path(self, start: T, end: T) -> Optional[List[T]]:
        """
        Find shortest path using BFS.
        
        Args:
            start: Starting vertex
            end: Target vertex
            
        Returns:
            Shortest path or None if no path exists
        """
        if start not in self.adj_list or end not in self.adj_list:
            return None
        
        visited: Set[T] = set()
        parent: Dict[T, Optional[T]] = {}
        queue = deque([start])
        visited.add(start)
        parent[start] = None
        
        while queue:
            vertex = queue.popleft()
            
            if vertex == end:
                # Reconstruct path
                path = []
                current = end
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]
            
            for neighbor in self.adj_list[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        
        return None
    
    def bfs_distance(self, start: T, end: T) -> Optional[int]:
        """
        Find distance between two vertices using BFS.
        
        Args:
            start: Starting vertex
            end: Target vertex
            
        Returns:
            Distance or None if no path exists
        """
        path = self.bfs_shortest_path(start, end)
        return len(path) - 1 if path else None
    
    def dfs(self, start: T) -> List[T]:
        """
        Depth-first search traversal (iterative).
        
        Args:
            start: Starting vertex
            
        Returns:
            DFS traversal order
        """
        if start not in self.adj_list:
            return []
        
        visited: Set[T] = set()
        result: List[T] = []
        stack = [start]
        
        while stack:
            vertex = stack.pop()
            
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                
                # Add neighbors in reverse order for consistent traversal
                for neighbor in reversed(self.adj_list[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    def dfs_recursive(self, start: T) -> List[T]:
        """
        Depth-first search traversal (recursive).
        
        Args:
            start: Starting vertex
            
        Returns:
            DFS traversal order
        """
        if start not in self.adj_list:
            return []
        
        visited: Set[T] = set()
        result: List[T] = []
        
        self._dfs_recursive_helper(start, visited, result)
        return result
    
    def _dfs_recursive_helper(self, vertex: T, visited: Set[T], result: List[T]) -> None:
        """Recursive DFS helper."""
        visited.add(vertex)
        result.append(vertex)
        
        for neighbor in self.adj_list[vertex]:
            if neighbor not in visited:
                self._dfs_recursive_helper(neighbor, visited, result)
    
    def dfs_all_components(self) -> List[List[T]]:
        """
        DFS traversal of all connected components.
        
        Returns:
            List of components, each as a traversal order
        """
        visited: Set[T] = set()
        components = []
        
        for vertex in self.adj_list:
            if vertex not in visited:
                component = []
                self._dfs_recursive_helper(vertex, visited, component)
                components.append(component)
        
        return components
    
    def count_components(self) -> int:
        """
        Count number of connected components.
        
        Returns:
            Number of components
        """
        return len(self.dfs_all_components())
    
    def is_connected(self) -> bool:
        """
        Check if graph is connected.
        
        Returns:
            True if graph is connected
        """
        if not self.adj_list:
            return True
        
        components = self.dfs_all_components()
        return len(components) == 1
    
    def detect_cycle(self) -> bool:
        """
        Detect cycle in graph using DFS.
        
        Returns:
            True if cycle exists
        """
        visited: Set[T] = set()
        rec_stack: Set[T] = set()
        
        for vertex in self.adj_list:
            if vertex not in visited:
                if self._detect_cycle_helper(vertex, visited, rec_stack):
                    return True
        
        return False
    
    def _detect_cycle_helper(self, vertex: T, visited: Set[T], 
                            rec_stack: Set[T]) -> bool:
        """Helper for cycle detection."""
        visited.add(vertex)
        rec_stack.add(vertex)
        
        for neighbor in self.adj_list[vertex]:
            if neighbor not in visited:
                if self._detect_cycle_helper(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(vertex)
        return False
    
    def topological_sort(self) -> Optional[List[T]]:
        """
        Topological sort using DFS (for DAGs).
        
        Returns:
            Topological order or None if cycle detected
        """
        if self.detect_cycle():
            return None
        
        visited: Set[T] = set()
        result: List[T] = []
        
        for vertex in self.adj_list:
            if vertex not in visited:
                self._topological_helper(vertex, visited, result)
        
        return result[::-1]
    
    def _topological_helper(self, vertex: T, visited: Set[T], result: List[T]) -> None:
        """Helper for topological sort."""
        visited.add(vertex)
        
        for neighbor in self.adj_list[vertex]:
            if neighbor not in visited:
                self._topological_helper(neighbor, visited, result)
        
        result.append(vertex)


def main() -> None:
    """Demonstrate BFS and DFS."""
    
    print("=== BFS and DFS Demo ===")
    
    # Create graph
    graph = GraphTraversal(directed=False)
    edges = [(0, 1), (0, 2), (1, 2), (2, 0), (3, 3), (4, 5), (5, 6)]
    for u, v in edges:
        graph.add_edge(u, v)
    
    print("Graph edges:", edges)
    
    # BFS
    print("\n--- BFS ---")
    bfs_order = graph.bfs(0)
    print(f"BFS from 0: {bfs_order}")
    
    bfs_order_2 = graph.bfs(4)
    print(f"BFS from 4: {bfs_order_2}")
    
    # DFS
    print("\n--- DFS ---")
    dfs_order = graph.dfs(0)
    print(f"DFS (iterative) from 0: {dfs_order}")
    
    dfs_recursive = graph.dfs_recursive(0)
    print(f"DFS (recursive) from 0: {dfs_recursive}")
    
    # Shortest path
    print("\n--- Shortest Path ---")
    path = graph.bfs_shortest_path(0, 2)
    print(f"Shortest path 0 -> 2: {path}")
    
    distance = graph.bfs_distance(0, 2)
    print(f"Distance 0 -> 2: {distance}")
    
    # Connected components
    print("\n--- Connected Components ---")
    components = graph.dfs_all_components()
    print(f"Components: {components}")
    print(f"Number of components: {graph.count_components()}")
    print(f"Is connected: {graph.is_connected()}")
    
    # Cycle detection
    print("\n--- Cycle Detection ---")
    print(f"Has cycle: {graph.detect_cycle()}")
    
    # Topological sort (directed graph)
    print("\n--- Topological Sort ---")
    dag = GraphTraversal(directed=True)
    dag_edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    for u, v in dag_edges:
        dag.add_edge(u, v)
    
    topo_order = dag.topological_sort()
    print(f"Topological order: {topo_order}")
    
    # String graph
    print("\n=== String Graph ===")
    str_graph = GraphTraversal(directed=False)
    str_edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
    for u, v in str_edges:
        str_graph.add_edge(u, v)
    
    print(f"BFS from 'A': {str_graph.bfs('A')}")
    print(f"DFS from 'A': {str_graph.dfs('A')}")
    print(f"Shortest path 'A' -> 'D': {str_graph.bfs_shortest_path('A', 'D')}")


if __name__ == "__main__":
    main()
