"""
A* Search Algorithm - Heuristic-based pathfinding.
Features: Admissible heuristics, path reconstruction, and multiple heuristics.
"""

from typing import List, Dict, Set, Optional, TypeVar, Generic, Callable
import heapq
import math

T = TypeVar('T')


class AStarSearch:
    """A* search algorithm implementation."""
    
    def __init__(self, directed: bool = False) -> None:
        """
        Initialize weighted graph.
        
        Args:
            directed: Whether graph is directed
        """
        self.directed = directed
        self.adj_list: Dict[T, List[tuple]] = {}
        self.heuristic: Dict[T, float] = {}
    
    def add_edge(self, u: T, v: T, weight: float) -> None:
        """
        Add weighted edge to graph.
        
        Args:
            u: First vertex
            v: Second vertex
            weight: Edge weight (must be non-negative)
        """
        if weight < 0:
            raise ValueError("A* requires non-negative weights")
        
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))
    
    def set_heuristic(self, vertex: T, value: float) -> None:
        """
        Set heuristic value for vertex.
        
        Args:
            vertex: Vertex
            value: Heuristic value (estimated distance to goal)
        """
        self.heuristic[vertex] = value
    
    def set_heuristics(self, heuristics: Dict[T, float]) -> None:
        """
        Set heuristic values for multiple vertices.
        
        Args:
            heuristics: Dictionary of vertex to heuristic value
        """
        self.heuristic.update(heuristics)
    
    def search(self, start: T, goal: T) -> Optional[tuple]:
        """
        Find shortest path using A* search.
        
        Args:
            start: Starting vertex
            goal: Goal vertex
            
        Returns:
            Tuple of (cost, path) or None if no path
        """
        if start not in self.adj_list or goal not in self.adj_list:
            return None
        
        # Priority queue: (f_score, g_score, vertex)
        pq = [(self.heuristic.get(start, 0), 0, start)]
        
        g_score: Dict[T, float] = {vertex: float('inf') for vertex in self.adj_list}
        g_score[start] = 0
        
        parent: Dict[T, Optional[T]] = {vertex: None for vertex in self.adj_list}
        visited: Set[T] = set()
        
        while pq:
            f_score, current_g, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == goal:
                # Reconstruct path
                path = []
                node = goal
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return (current_g, path[::-1])
            
            for neighbor, weight in self.adj_list[current]:
                if neighbor in visited:
                    continue
                
                tentative_g = current_g + weight
                
                if tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    parent[neighbor] = current
                    f_score = tentative_g + self.heuristic.get(neighbor, 0)
                    heapq.heappush(pq, (f_score, tentative_g, neighbor))
        
        return None
    
    def search_cost(self, start: T, goal: T) -> Optional[float]:
        """
        Find path cost without reconstruction.
        
        Args:
            start: Starting vertex
            goal: Goal vertex
            
        Returns:
            Path cost or None if no path
        """
        result = self.search(start, goal)
        return result[0] if result else None


class GridAStar(AStarSearch):
    """A* search for grid-based pathfinding."""
    
    @staticmethod
    def manhattan_distance(a: tuple, b: tuple) -> float:
        """
        Calculate Manhattan distance between two grid points.
        
        Args:
            a: First point (x, y)
            b: Second point (x, y)
            
        Returns:
            Manhattan distance
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    @staticmethod
    def euclidean_distance(a: tuple, b: tuple) -> float:
        """
        Calculate Euclidean distance between two grid points.
        
        Args:
            a: First point (x, y)
            b: Second point (x, y)
            
        Returns:
            Euclidean distance
        """
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    
    @staticmethod
    def chebyshev_distance(a: tuple, b: tuple) -> float:
        """
        Calculate Chebyshev distance between two grid points.
        
        Args:
            a: First point (x, y)
            b: Second point (x, y)
            
        Returns:
            Chebyshev distance
        """
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
    
    def setup_grid(self, width: int, height: int, obstacles: Set[tuple] = None) -> None:
        """
        Setup grid graph.
        
        Args:
            width: Grid width
            height: Grid height
            obstacles: Set of obstacle coordinates
        """
        obstacles = obstacles or set()
        
        # Create grid vertices
        for x in range(width):
            for y in range(height):
                if (x, y) not in obstacles:
                    self.adj_list[(x, y)] = []
        
        # Add edges (4-directional movement)
        for x in range(width):
            for y in range(height):
                if (x, y) in obstacles:
                    continue
                
                # Check neighbors
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in obstacles:
                        self.add_edge((x, y), (nx, ny), 1)
    
    def search_with_heuristic(self, start: tuple, goal: tuple, 
                            heuristic_func: Callable = None) -> Optional[tuple]:
        """
        Search with custom heuristic function.
        
        Args:
            start: Starting position
            goal: Goal position
            heuristic_func: Heuristic function
            
        Returns:
            Tuple of (cost, path) or None
        """
        if heuristic_func is None:
            heuristic_func = self.manhattan_distance
        
        # Set heuristics for all vertices
        for vertex in self.adj_list:
            self.heuristic[vertex] = heuristic_func(vertex, goal)
        
        return self.search(start, goal)


def main() -> None:
    """Demonstrate A* search."""
    
    print("=== A* Search Demo ===")
    
    # Create graph
    astar = AStarSearch(directed=False)
    
    edges = [
        (0, 1, 1),
        (0, 2, 4),
        (1, 2, 2),
        (1, 3, 5),
        (2, 3, 1),
        (3, 4, 3),
        (4, 5, 2)
    ]
    
    for u, v, w in edges:
        astar.add_edge(u, v, w)
    
    # Set heuristics (estimated distance to goal 5)
    heuristics = {
        0: 7,
        1: 6,
        2: 3,
        3: 2,
        4: 2,
        5: 0
    }
    astar.set_heuristics(heuristics)
    
    print("Graph edges (with weights):")
    for u, v, w in edges:
        print(f"  {u} --{w}--> {v}")
    
    print("\nHeuristics:")
    for vertex, h in sorted(heuristics.items()):
        print(f"  {vertex}: {h}")
    
    # Search
    print("\n--- A* Search ---")
    result = astar.search(0, 5)
    if result:
        cost, path = result
        print(f"Path: {path}")
        print(f"Cost: {cost}")
    
    # Grid pathfinding
    print("\n=== Grid Pathfinding ===")
    grid_astar = GridAStar(directed=False)
    
    # Setup 5x5 grid with obstacles
    obstacles = {(2, 1), (2, 2), (2, 3)}
    grid_astar.setup_grid(5, 5, obstacles)
    
    print(f"Grid: 5x5 with obstacles at {obstacles}")
    
    start = (0, 0)
    goal = (4, 4)
    
    # Manhattan distance
    print("\n--- Manhattan Distance ---")
    result_manhattan = grid_astar.search_with_heuristic(start, goal, 
                                                         GridAStar.manhattan_distance)
    if result_manhattan:
        cost, path = result_manhattan
        print(f"Path: {path}")
        print(f"Cost: {cost}")
    
    # Euclidean distance
    print("\n--- Euclidean Distance ---")
    result_euclidean = grid_astar.search_with_heuristic(start, goal, 
                                                          GridAStar.euclidean_distance)
    if result_euclidean:
        cost, path = result_euclidean
        print(f"Path: {path}")
        print(f"Cost: {cost}")
    
    # Chebyshev distance
    print("\n--- Chebyshev Distance ---")
    result_chebyshev = grid_astar.search_with_heuristic(start, goal, 
                                                          GridAStar.chebyshev_distance)
    if result_chebyshev:
        cost, path = result_chebyshev
        print(f"Path: {path}")
        print(f"Cost: {cost}")
    
    # String vertices
    print("\n=== Vertices as Strings ===")
    str_astar = AStarSearch(directed=False)
    
    str_edges = [
        ("A", "B", 1),
        ("A", "C", 4),
        ("B", "C", 2),
        ("B", "D", 5),
        ("C", "D", 1),
        ("D", "E", 3)
    ]
    
    for u, v, w in str_edges:
        str_astar.add_edge(u, v, w)
    
    str_heuristics = {
        "A": 6,
        "B": 5,
        "C": 2,
        "D": 1,
        "E": 0
    }
    str_astar.set_heuristics(str_heuristics)
    
    result = str_astar.search("A", "E")
    if result:
        cost, path = result
        print(f"Path: {path}")
        print(f"Cost: {cost}")


if __name__ == "__main__":
    main()
