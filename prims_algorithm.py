"""
Prim's Algorithm - Minimum Spanning Tree algorithm.
Features: Priority queue optimization, total weight calculation, and edge list output.
"""

from typing import List, Dict, Set, Optional, TypeVar, Generic
import heapq

T = TypeVar('T')


class PrimsAlgorithm:
    """Prim's MST algorithm implementation."""
    
    def __init__(self, directed: bool = False) -> None:
        """
        Initialize weighted graph.
        
        Args:
            directed: Whether graph is directed (usually False for MST)
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
            raise ValueError("Prim's algorithm requires non-negative weights")
        
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))
    
    def mst(self, start: Optional[T] = None) -> Optional[tuple]:
        """
        Find Minimum Spanning Tree using Prim's algorithm.
        
        Args:
            start: Starting vertex (optional, uses first vertex if None)
            
        Returns:
            Tuple of (total_weight, edges) or None if graph is disconnected
        """
        if not self.adj_list:
            return None
        
        # Choose starting vertex
        if start is None:
            start = next(iter(self.adj_list))
        
        if start not in self.adj_list:
            return None
        
        # Priority queue: (weight, u, v)
        pq = []
        visited: Set[T] = set()
        mst_edges: List[tuple] = []
        total_weight = 0.0
        
        # Start with first vertex
        visited.add(start)
        
        # Add all edges from start to priority queue
        for neighbor, weight in self.adj_list[start]:
            heapq.heappush(pq, (weight, start, neighbor))
        
        while pq and len(visited) < len(self.adj_list):
            weight, u, v = heapq.heappop(pq)
            
            if v in visited:
                continue
            
            # Add edge to MST
            visited.add(v)
            mst_edges.append((u, v, weight))
            total_weight += weight
            
            # Add all edges from v to priority queue
            for neighbor, edge_weight in self.adj_list[v]:
                if neighbor not in visited:
                    heapq.heappush(pq, (edge_weight, v, neighbor))
        
        # Check if graph is connected
        if len(visited) != len(self.adj_list):
            return None
        
        return (total_weight, mst_edges)
    
    def mst_total_weight(self, start: Optional[T] = None) -> Optional[float]:
        """
        Get total weight of MST without edge list.
        
        Args:
            start: Starting vertex
            
        Returns:
            Total weight or None if disconnected
        """
        result = self.mst(start)
        return result[0] if result else None
    
    def mst_edges(self, start: Optional[T] = None) -> Optional[List[tuple]]:
        """
        Get MST edges without total weight.
        
        Args:
            start: Starting vertex
            
        Returns:
            List of edges or None if disconnected
        """
        result = self.mst(start)
        return result[1] if result else None
    
    def is_connected(self) -> bool:
        """
        Check if graph is connected.
        
        Returns:
            True if graph is connected
        """
        if not self.adj_list:
            return True
        
        start = next(iter(self.adj_list))
        visited: Set[T] = set()
        stack = [start]
        
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                for neighbor, _ in self.adj_list[vertex]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return len(visited) == len(self.adj_list)
    
    def get_vertices(self) -> List[T]:
        """Get list of vertices."""
        return list(self.adj_list.keys())


class LazyPrims(PrimsAlgorithm):
    """Lazy implementation of Prim's algorithm."""
    
    def mst(self, start: Optional[T] = None) -> Optional[tuple]:
        """
        Find MST using lazy Prim's (keeps all edges in queue).
        
        Args:
            start: Starting vertex
            
        Returns:
            Tuple of (total_weight, edges) or None
        """
        if not self.adj_list:
            return None
        
        if start is None:
            start = next(iter(self.adj_list))
        
        if start not in self.adj_list:
            return None
        
        pq = []
        visited: Set[T] = set()
        mst_edges: List[tuple] = []
        total_weight = 0.0
        
        visited.add(start)
        
        for neighbor, weight in self.adj_list[start]:
            heapq.heappush(pq, (weight, start, neighbor))
        
        while pq and len(visited) < len(self.adj_list):
            weight, u, v = heapq.heappop(pq)
            
            if v in visited:
                continue
            
            visited.add(v)
            mst_edges.append((u, v, weight))
            total_weight += weight
            
            for neighbor, edge_weight in self.adj_list[v]:
                if neighbor not in visited:
                    heapq.heappush(pq, (edge_weight, v, neighbor))
        
        if len(visited) != len(self.adj_list):
            return None
        
        return (total_weight, mst_edges)


def main() -> None:
    """Demonstrate Prim's algorithm."""
    
    print("=== Prim's Algorithm Demo ===")
    
    # Create graph
    prim = PrimsAlgorithm(directed=False)
    
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
        prim.add_edge(u, v, w)
    
    print("Graph edges (with weights):")
    for u, v, w in edges:
        print(f"  {u} --{w}--> {v}")
    
    # Find MST
    print("\n--- Minimum Spanning Tree ---")
    result = prim.mst()
    if result:
        total_weight, mst_edges = result
        print(f"Total weight: {total_weight}")
        print("MST edges:")
        for u, v, w in mst_edges:
            print(f"  {u} --{w}--> {v}")
    
    # MST from specific start
    print("\n--- MST from Vertex 1 ---")
    result_1 = prim.mst(start=1)
    if result_1:
        total_weight, mst_edges = result_1
        print(f"Total weight: {total_weight}")
        print("MST edges:")
        for u, v, w in mst_edges:
            print(f"  {u} --{w}--> {v}")
    
    # Check connectivity
    print(f"\n--- Connectivity ---")
    print(f"Is connected: {prim.is_connected()}")
    
    # Lazy Prim's
    print("\n--- Lazy Prim's Algorithm ---")
    lazy_prim = LazyPrims(directed=False)
    
    for u, v, w in edges:
        lazy_prim.add_edge(u, v, w)
    
    lazy_result = lazy_prim.mst()
    if lazy_result:
        total_weight, mst_edges = lazy_result
        print(f"Total weight: {total_weight}")
        print("MST edges:")
        for u, v, w in mst_edges:
            print(f"  {u} --{w}--> {v}")
    
    # Disconnected graph
    print("\n=== Disconnected Graph ===")
    disconnected = PrimsAlgorithm(directed=False)
    
    disconnected.add_edge(0, 1, 1)
    disconnected.add_edge(2, 3, 1)
    
    print(f"Is connected: {disconnected.is_connected()}")
    result = disconnected.mst()
    print(f"MST result: {result}")
    
    # String vertices
    print("\n=== Vertices as Strings ===")
    str_prim = PrimsAlgorithm(directed=False)
    
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
        str_prim.add_edge(u, v, w)
    
    result = str_prim.mst()
    if result:
        total_weight, mst_edges = result
        print(f"Total weight: {total_weight}")
        print("MST edges:")
        for u, v, w in mst_edges:
            print(f"  {u} --{w}--> {v}")


if __name__ == "__main__":
    main()
