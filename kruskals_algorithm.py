"""
Kruskal's Algorithm - Minimum Spanning Tree algorithm.
Features: Union-Find (Disjoint Set), edge sorting, and cycle detection.
"""

from typing import List, Dict, Set, Optional, TypeVar, Generic

T = TypeVar('T')


class UnionFind:
    """Union-Find (Disjoint Set) data structure."""
    
    def __init__(self, elements: List[T]) -> None:
        """
        Initialize Union-Find with elements.
        
        Args:
            elements: List of elements
        """
        self.parent: Dict[T, T] = {e: e for e in elements}
        self.rank: Dict[T, int] = {e: 0 for e in elements}
    
    def find(self, x: T) -> T:
        """
        Find representative of set containing x with path compression.
        
        Args:
            x: Element to find
            
        Returns:
            Representative of the set
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: T, y: T) -> bool:
        """
        Union sets containing x and y with union by rank.
        
        Args:
            x: First element
            y: Second element
            
        Returns:
            True if union was performed, False if already in same set
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True


class KruskalsAlgorithm:
    """Kruskal's MST algorithm implementation."""
    
    def __init__(self, directed: bool = False) -> None:
        """
        Initialize weighted graph.
        
        Args:
            directed: Whether graph is directed (usually False for MST)
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
            weight: Edge weight (must be non-negative)
        """
        if weight < 0:
            raise ValueError("Kruskal's algorithm requires non-negative weights")
        
        self.vertices.add(u)
        self.vertices.add(v)
        self.edges.append((weight, u, v))
        
        if not self.directed:
            self.edges.append((weight, v, u))
    
    def mst(self) -> Optional[tuple]:
        """
        Find Minimum Spanning Tree using Kruskal's algorithm.
        
        Returns:
            Tuple of (total_weight, edges) or None if graph is disconnected
        """
        if not self.vertices:
            return None
        
        # Sort edges by weight
        sorted_edges = sorted(self.edges, key=lambda x: x[0])
        
        # Initialize Union-Find
        uf = UnionFind(list(self.vertices))
        
        mst_edges: List[tuple] = []
        total_weight = 0.0
        
        for weight, u, v in sorted_edges:
            if uf.union(u, v):
                mst_edges.append((u, v, weight))
                total_weight += weight
        
        # Check if all vertices are connected
        # Count unique sets
        unique_roots = len({uf.find(v) for v in self.vertices})
        
        if unique_roots > 1:
            return None
        
        return (total_weight, mst_edges)
    
    def mst_total_weight(self) -> Optional[float]:
        """
        Get total weight of MST without edge list.
        
        Returns:
            Total weight or None if disconnected
        """
        result = self.mst()
        return result[0] if result else None
    
    def mst_edges(self) -> Optional[List[tuple]]:
        """
        Get MST edges without total weight.
        
        Returns:
            List of edges or None if disconnected
        """
        result = self.mst()
        return result[1] if result else None
    
    def is_connected(self) -> bool:
        """
        Check if graph is connected using Union-Find.
        
        Returns:
            True if graph is connected
        """
        if not self.vertices:
            return True
        
        uf = UnionFind(list(self.vertices))
        
        for weight, u, v in self.edges:
            uf.union(u, v)
        
        # Check if all vertices have same root
        first_root = uf.find(next(iter(self.vertices)))
        return all(uf.find(v) == first_root for v in self.vertices)
    
    def get_vertices(self) -> List[T]:
        """Get list of vertices."""
        return list(self.vertices)


def main() -> None:
    """Demonstrate Kruskal's algorithm."""
    
    print("=== Kruskal's Algorithm Demo ===")
    
    # Create graph
    kruskal = KruskalsAlgorithm(directed=False)
    
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
        kruskal.add_edge(u, v, w)
    
    print("Graph edges (with weights):")
    for u, v, w in edges:
        print(f"  {u} --{w}--> {v}")
    
    # Find MST
    print("\n--- Minimum Spanning Tree ---")
    result = kruskal.mst()
    if result:
        total_weight, mst_edges = result
        print(f"Total weight: {total_weight}")
        print("MST edges:")
        for u, v, w in mst_edges:
            print(f"  {u} --{w}--> {v}")
    
    # Check connectivity
    print(f"\n--- Connectivity ---")
    print(f"Is connected: {kruskal.is_connected()}")
    
    # Disconnected graph
    print("\n=== Disconnected Graph ===")
    disconnected = KruskalsAlgorithm(directed=False)
    
    disconnected.add_edge(0, 1, 1)
    disconnected.add_edge(2, 3, 1)
    
    print(f"Is connected: {disconnected.is_connected()}")
    result = disconnected.mst()
    print(f"MST result: {result}")
    
    # String vertices
    print("\n=== Vertices as Strings ===")
    str_kruskal = KruskalsAlgorithm(directed=False)
    
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
        str_kruskal.add_edge(u, v, w)
    
    result = str_kruskal.mst()
    if result:
        total_weight, mst_edges = result
        print(f"Total weight: {total_weight}")
        print("MST edges:")
        for u, v, w in mst_edges:
            print(f"  {u} --{w}--> {v}")
    
    # Union-Find demonstration
    print("\n=== Union-Find Demo ===")
    elements = [1, 2, 3, 4, 5]
    uf = UnionFind(elements)
    
    print(f"Initial parents: {uf.parent}")
    print(f"Initial ranks: {uf.rank}")
    
    uf.union(1, 2)
    uf.union(3, 4)
    uf.union(4, 5)
    
    print(f"\nAfter unions:")
    print(f"Parents: {uf.parent}")
    print(f"Ranks: {uf.rank}")
    
    uf.union(1, 3)
    
    print(f"\nAfter merging sets:")
    print(f"Parents: {uf.parent}")
    print(f"Ranks: {uf.rank}")
    
    print(f"\nFind(1): {uf.find(1)}")
    print(f"Find(5): {uf.find(5)}")
    print(f"Find(2): {uf.find(2)}")


if __name__ == "__main__":
    main()
