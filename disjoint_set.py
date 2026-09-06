"""
Disjoint Set (Union-Find) - Disjoint set data structure.
Features: Path compression, union by rank, and connected components.
"""

from typing import Dict, List, TypeVar, Generic, Optional

T = TypeVar('T')


class DisjointSet(Generic[T]):
    """Disjoint set (Union-Find) implementation."""
    
    def __init__(self) -> None:
        """Initialize disjoint set."""
        self.parent: Dict[T, T] = {}
        self.rank: Dict[T, int] = {}
        self.size: Dict[T, int] = {}
    
    def make_set(self, element: T) -> None:
        """
        Create a new set containing the element.
        
        Args:
            element: Element to add
        """
        if element not in self.parent:
            self.parent[element] = element
            self.rank[element] = 0
            self.size[element] = 1
    
    def find(self, element: T) -> Optional[T]:
        """
        Find representative of set containing element.
        
        Args:
            element: Element to find
            
        Returns:
            Representative element or None if not found
        """
        if element not in self.parent:
            return None
        
        # Path compression
        if self.parent[element] != element:
            self.parent[element] = self.find(self.parent[element])
        
        return self.parent[element]
    
    def union(self, element1: T, element2: T) -> bool:
        """
        Merge sets containing element1 and element2.
        
        Args:
            element1: First element
            element2: Second element
            
        Returns:
            True if merged, False if already in same set
        """
        root1 = self.find(element1)
        root2 = self.find(element2)
        
        if root1 is None or root2 is None:
            return False
        
        if root1 == root2:
            return False
        
        # Union by rank
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
            self.size[root2] += self.size[root1]
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
            self.size[root1] += self.size[root2]
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1
            self.size[root1] += self.size[root2]
        
        return True
    
    def is_connected(self, element1: T, element2: T) -> bool:
        """
        Check if two elements are in the same set.
        
        Args:
            element1: First element
            element2: Second element
            
        Returns:
            True if connected
        """
        root1 = self.find(element1)
        root2 = self.find(element2)
        
        return root1 is not None and root1 == root2
    
    def get_set_size(self, element: T) -> Optional[int]:
        """
        Get size of set containing element.
        
        Args:
            element: Element
            
        Returns:
            Set size or None if not found
        """
        root = self.find(element)
        if root is None:
            return None
        return self.size.get(root, 0)
    
    def get_components(self) -> Dict[T, List[T]]:
        """
        Get all connected components.
        
        Returns:
            Dictionary mapping root to component members
        """
        components: Dict[T, List[T]] = {}
        
        for element in self.parent:
            root = self.find(element)
            if root is not None:
                if root not in components:
                    components[root] = []
                components[root].append(element)
        
        return components
    
    def count_components(self) -> int:
        """
        Count number of connected components.
        
        Returns:
            Number of components
        """
        roots = set()
        for element in self.parent:
            root = self.find(element)
            if root is not None:
                roots.add(root)
        return len(roots)
    
    def clear(self) -> None:
        """Clear all sets."""
        self.parent.clear()
        self.rank.clear()
        self.size.clear()
    
    def __str__(self) -> str:
        """String representation."""
        components = self.get_components()
        return f"DisjointSet({len(components)} components)"


def main() -> None:
    """Demonstrate disjoint set."""
    
    print("=== Disjoint Set Demo ===")
    
    ds = DisjointSet[int]()
    
    # Make sets
    for i in range(1, 6):
        ds.make_set(i)
    
    print(f"Created sets for: 1, 2, 3, 4, 5")
    print(f"Components: {ds.count_components()}")
    
    # Union operations
    print("\n--- Union Operations ---")
    ds.union(1, 2)
    print(f"Union(1, 2): Connected = {ds.is_connected(1, 2)}")
    
    ds.union(3, 4)
    print(f"Union(3, 4): Connected = {ds.is_connected(3, 4)}")
    
    ds.union(2, 3)
    print(f"Union(2, 3): Connected = {ds.is_connected(1, 4)}")
    
    print(f"\nComponents: {ds.count_components()}")
    
    # Check connections
    print("\n--- Check Connections ---")
    print(f"1 and 4 connected: {ds.is_connected(1, 4)}")
    print(f"1 and 5 connected: {ds.is_connected(1, 5)}")
    
    # Get set sizes
    print("\n--- Set Sizes ---")
    print(f"Size of set containing 1: {ds.get_set_size(1)}")
    print(f"Size of set containing 5: {ds.get_set_size(5)}")
    
    # Get components
    print("\n--- Components ---")
    components = ds.get_components()
    for root, members in components.items():
        print(f"  Root {root}: {members}")
    
    # String disjoint set
    print("\n=== String Disjoint Set ===")
    str_ds = DisjointSet[str]()
    
    cities = ["NYC", "LA", "Chicago", "Houston", "Phoenix"]
    for city in cities:
        str_ds.make_set(city)
    
    str_ds.union("NYC", "LA")
    str_ds.union("Chicago", "Houston")
    
    print(f"NYC and LA connected: {str_ds.is_connected('NYC', 'LA')}")
    print(f"NYC and Chicago connected: {str_ds.is_connected('NYC', 'Chicago')}")
    
    # Graph connectivity
    print("\n=== Graph Connectivity ===")
    
    # Graph edges
    edges = [(0, 1), (1, 2), (3, 4), (4, 5), (5, 6)]
    
    graph_ds = DisjointSet[int]()
    for i in range(7):
        graph_ds.make_set(i)
    
    for u, v in edges:
        graph_ds.union(u, v)
    
    print(f"Graph has {graph_ds.count_components()} components")
    
    print("\nConnected components:")
    for root, members in graph_ds.get_components().items():
        print(f"  {members}")
    
    # Kruskal's MST simulation
    print("\n=== Kruskal's MST Simulation ===")
    
    mst_ds = DisjointSet[str]()
    nodes = ["A", "B", "C", "D", "E"]
    for node in nodes:
        mst_ds.make_set(node)
    
    # Edges with weights
    weighted_edges = [
        ("A", "B", 4),
        ("A", "C", 1),
        ("B", "C", 2),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2)
    ]
    
    # Sort by weight
    weighted_edges.sort(key=lambda x: x[2])
    
    mst_edges = []
    for u, v, weight in weighted_edges:
        if not mst_ds.is_connected(u, v):
            mst_ds.union(u, v)
            mst_edges.append((u, v, weight))
            print(f"Added edge: {u}-{v} (weight={weight})")
    
    print(f"\nMST edges: {mst_edges}")
    print(f"Total weight: {sum(w for _, _, w in mst_edges)}")


if __name__ == "__main__":
    main()
