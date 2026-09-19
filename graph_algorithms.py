"""
Graph Algorithms Module

This module provides comprehensive graph algorithms and data structures including:
- Graph data structures (adjacency list, adjacency matrix)
- Graph traversal algorithms (BFS, DFS)
- Shortest path algorithms (Dijkstra, Bellman-Ford, Floyd-Warshall)
- Minimum spanning tree (Prim's, Kruskal's)
- Topological sorting
- Graph connectivity components
- Maximum flow algorithms
- Bipartite graph detection
- Graph coloring
- Network flow and matching

All functions include comprehensive docstrings and type hints.
"""

from typing import Any, Dict, List, Optional, Tuple, Set, Union
from dataclasses import dataclass
from enum import Enum
import heapq
import math


class GraphType(Enum):
    """Types of graphs."""
    DIRECTED = "directed"
    UNDIRECTED = "undirected"
    WEIGHTED = "weighted"
    UNWEIGHTED = "unweighted"


@dataclass
class Edge:
    """Represents an edge in a graph."""
    source: str
    destination: str
    weight: float = 1.0
    
    def __hash__(self):
        return hash((self.source, self.destination))
    
    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return self.source == other.source and self.destination == other.destination


@dataclass
class GraphNode:
    """Represents a node in a graph."""
    id: str
    data: Any = None
    visited: bool = False
    distance: float = float('inf')
    parent: Optional[str] = None


class Graph:
    """Graph data structure implementation."""
    
    def __init__(self, graph_type: GraphType = GraphType.UNDIRECTED):
        """Initialize graph."""
        self.graph_type = graph_type
        self.nodes: Dict[str, GraphNode] = {}
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = {}
        self.adjacency_matrix: Dict[str, Dict[str, float]] = {}
    
    def add_node(self, node_id: str, data: Any = None) -> None:
        """Add a node to the graph."""
        if node_id not in self.nodes:
            self.nodes[node_id] = GraphNode(node_id, data)
            self.adjacency_list[node_id] = []
            self.adjacency_matrix[node_id] = {}
    
    def add_edge(self, source: str, destination: str, weight: float = 1.0) -> None:
        """Add an edge to the graph."""
        if source not in self.nodes:
            self.add_node(source)
        if destination not in self.nodes:
            self.add_node(destination)
        
        # Add to adjacency list
        self.adjacency_list[source].append((destination, weight))
        
        # Add to adjacency matrix
        self.adjacency_matrix[source][destination] = weight
        
        # For undirected graphs, add reverse edge
        if self.graph_type == GraphType.UNDIRECTED:
            self.adjacency_list[destination].append((source, weight))
            self.adjacency_matrix[destination][source] = weight
    
    def remove_node(self, node_id: str) -> bool:
        """Remove a node from the graph."""
        if node_id not in self.nodes:
            return False
        
        # Remove from adjacency list
        if node_id in self.adjacency_list:
            del self.adjacency_list[node_id]
        
        # Remove from other nodes' adjacency lists
        for node in self.adjacency_list:
            self.adjacency_list[node] = [(n, w) for n, w in self.adjacency_list[node] if n != node_id]
        
        # Remove from adjacency matrix
        if node_id in self.adjacency_matrix:
            del self.adjacency_matrix[node_id]
        
        for node in self.adjacency_matrix:
            if node_id in self.adjacency_matrix[node]:
                del self.adjacency_matrix[node][node_id]
        
        # Remove from nodes
        del self.nodes[node_id]
        
        return True
    
    def remove_edge(self, source: str, destination: str) -> bool:
        """Remove an edge from the graph."""
        if source not in self.adjacency_list or destination not in self.adjacency_list:
            return False
        
        # Remove from adjacency list
        self.adjacency_list[source] = [(n, w) for n, w in self.adjacency_list[source] if n != destination]
        
        # Remove from adjacency matrix
        if destination in self.adjacency_matrix[source]:
            del self.adjacency_matrix[source][destination]
        
        # For undirected graphs, remove reverse edge
        if self.graph_type == GraphType.UNDIRECTED:
            self.adjacency_list[destination] = [(n, w) for n, w in self.adjacency_list[destination] if n != source]
            if source in self.adjacency_matrix[destination]:
                del self.adjacency_matrix[destination][source]
        
        return True
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """Get neighbors of a node."""
        if node_id not in self.adjacency_list:
            return []
        return [neighbor for neighbor, _ in self.adjacency_list[node_id]]
    
    def get_edge_weight(self, source: str, destination: str) -> Optional[float]:
        """Get weight of an edge."""
        if source in self.adjacency_matrix and destination in self.adjacency_matrix[source]:
            return self.adjacency_matrix[source][destination]
        return None
    
    def get_node_count(self) -> int:
        """Get number of nodes."""
        return len(self.nodes)
    
    def get_edge_count(self) -> int:
        """Get number of edges."""
        count = sum(len(neighbors) for neighbors in self.adjacency_list.values())
        return count // 2 if self.graph_type == GraphType.UNDIRECTED else count
    
    def clear(self) -> None:
        """Clear the graph."""
        self.nodes.clear()
        self.adjacency_list.clear()
        self.adjacency_matrix.clear()


class GraphTraversal:
    """Graph traversal algorithms."""
    
    @staticmethod
    def bfs(graph: Graph, start_node: str) -> List[str]:
        """Breadth-First Search traversal."""
        if start_node not in graph.nodes:
            return []
        
        visited = set()
        queue = [start_node]
        result = []
        
        while queue:
            node = queue.pop(0)
            
            if node not in visited:
                visited.add(node)
                result.append(node)
                
                # Add unvisited neighbors
                for neighbor, _ in graph.adjacency_list[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return result
    
    @staticmethod
    def dfs(graph: Graph, start_node: str) -> List[str]:
        """Depth-First Search traversal (iterative)."""
        if start_node not in graph.nodes:
            return []
        
        visited = set()
        stack = [start_node]
        result = []
        
        while stack:
            node = stack.pop()
            
            if node not in visited:
                visited.add(node)
                result.append(node)
                
                # Add unvisited neighbors (reverse for DFS order)
                neighbors = [neighbor for neighbor, _ in graph.adjacency_list[node]]
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    @staticmethod
    def dfs_recursive(graph: Graph, node: str, visited: Set[str] = None,
                     result: List[str] = None) -> List[str]:
        """Depth-First Search traversal (recursive)."""
        if visited is None:
            visited = set()
        if result is None:
            result = []
        
        if node not in graph.nodes:
            return result
        
        visited.add(node)
        result.append(node)
        
        for neighbor, _ in graph.adjacency_list[node]:
            if neighbor not in visited:
                GraphTraversal.dfs_recursive(graph, neighbor, visited, result)
        
        return result


class ShortestPath:
    """Shortest path algorithms."""
    
    @staticmethod
    def dijkstra(graph: Graph, start_node: str) -> Dict[str, float]:
        """Dijkstra's algorithm for shortest paths."""
        if start_node not in graph.nodes:
            return {}
        
        # Initialize distances
        distances = {node: float('inf') for node in graph.nodes}
        distances[start_node] = 0
        
        # Priority queue: (distance, node)
        pq = [(0, start_node)]
        visited = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            # Check all neighbors
            for neighbor, weight in graph.adjacency_list[current_node]:
                if neighbor in visited:
                    continue
                
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        
        return distances
    
    @staticmethod
    def dijkstra_path(graph: Graph, start_node: str, end_node: str) -> Tuple[float, List[str]]:
        """Dijkstra's algorithm with path reconstruction."""
        if start_node not in graph.nodes or end_node not in graph.nodes:
            return float('inf'), []
        
        # Initialize distances and predecessors
        distances = {node: float('inf') for node in graph.nodes}
        predecessors = {node: None for node in graph.nodes}
        distances[start_node] = 0
        
        # Priority queue
        pq = [(0, start_node)]
        visited = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if current_node == end_node:
                break
            
            # Check all neighbors
            for neighbor, weight in graph.adjacency_list[current_node]:
                if neighbor in visited:
                    continue
                
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
        
        # Reconstruct path
        if distances[end_node] == float('inf'):
            return float('inf'), []
        
        path = []
        current = end_node
        while current is not None:
            path.append(current)
            current = predecessors[current]
        
        path.reverse()
        
        return distances[end_node], path
    
    @staticmethod
    def bellman_ford(graph: Graph, start_node: str) -> Dict[str, float]:
        """Bellman-Ford algorithm (handles negative weights)."""
        if start_node not in graph.nodes:
            return {}
        
        # Initialize distances
        distances = {node: float('inf') for node in graph.nodes}
        distances[start_node] = 0
        
        # Relax edges V-1 times
        for _ in range(len(graph.nodes) - 1):
            for source in graph.adjacency_list:
                for destination, weight in graph.adjacency_list[source]:
                    if distances[source] != float('inf'):
                        if distances[source] + weight < distances[destination]:
                            distances[destination] = distances[source] + weight
        
        # Check for negative cycles
        for source in graph.adjacency_list:
            for destination, weight in graph.adjacency_list[source]:
                if distances[source] != float('inf'):
                    if distances[source] + weight < distances[destination]:
                        raise ValueError("Graph contains negative cycle")
        
        return distances
    
    @staticmethod
    def floyd_warshall(graph: Graph) -> Dict[str, Dict[str, float]]:
        """Floyd-Warshall algorithm (all pairs shortest paths)."""
        # Initialize distance matrix
        nodes = list(graph.nodes.keys())
        distances = {node: {n: float('inf') for n in nodes} for node in nodes}
        
        for node in nodes:
            distances[node][node] = 0
        
        for source in graph.adjacency_list:
            for destination, weight in graph.adjacency_list[source]:
                distances[source][destination] = weight
        
        # Floyd-Warshall algorithm
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if distances[i][k] + distances[k][j] < distances[i][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]
        
        return distances


class MinimumSpanningTree:
    """Minimum Spanning Tree algorithms."""
    
    @staticmethod
    def prim(graph: Graph, start_node: str) -> Tuple[float, List[Edge]]:
        """Prim's algorithm for MST."""
        if start_node not in graph.nodes:
            return 0.0, []
        
        visited = set()
        mst_edges = []
        total_weight = 0.0
        
        # Priority queue: (weight, source, destination)
        pq = [(0, None, start_node)]
        
        while pq and len(visited) < len(graph.nodes):
            weight, source, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if source is not None:
                mst_edges.append(Edge(source, current, weight))
                total_weight += weight
            
            # Add all edges from current node
            for neighbor, edge_weight in graph.adjacency_list[current]:
                if neighbor not in visited:
                    heapq.heappush(pq, (edge_weight, current, neighbor))
        
        return total_weight, mst_edges
    
    @staticmethod
    def kruskal(graph: Graph) -> Tuple[float, List[Edge]]:
        """Kruskal's algorithm for MST."""
        # Get all edges
        edges = []
        for source in graph.adjacency_list:
            for destination, weight in graph.adjacency_list[source]:
                # For undirected graphs, add edge only once
                if graph.graph_type == GraphType.UNDIRECTED:
                    if source < destination:
                        edges.append((weight, source, destination))
                else:
                    edges.append((weight, source, destination))
        
        # Sort edges by weight
        edges.sort()
        
        # Union-Find data structure
        parent = {node: node for node in graph.nodes}
        
        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]
        
        def union(node1, node2):
            root1 = find(node1)
            root2 = find(node2)
            if root1 != root2:
                parent[root1] = root2
                return True
            return False
        
        mst_edges = []
        total_weight = 0.0
        
        for weight, source, destination in edges:
            if union(source, destination):
                mst_edges.append(Edge(source, destination, weight))
                total_weight += weight
        
        return total_weight, mst_edges


class TopologicalSort:
    """Topological sorting algorithms."""
    
    @staticmethod
    def kahn(graph: Graph) -> List[str]:
        """Kahn's algorithm for topological sort."""
        # Calculate in-degrees
        in_degree = {node: 0 for node in graph.nodes}
        
        for source in graph.adjacency_list:
            for destination, _ in graph.adjacency_list[source]:
                in_degree[destination] += 1
        
        # Queue of nodes with in-degree 0
        queue = [node for node, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            
            # Reduce in-degree of neighbors
            for neighbor, _ in graph.adjacency_list[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Check for cycle
        if len(result) != len(graph.nodes):
            raise ValueError("Graph contains cycle")
        
        return result
    
    @staticmethod
    def dfs_topological(graph: Graph) -> List[str]:
        """DFS-based topological sort."""
        visited = set()
        temp_visited = set()
        result = []
        
        def visit(node):
            if node in temp_visited:
                raise ValueError("Graph contains cycle")
            if node in visited:
                return
            
            temp_visited.add(node)
            
            for neighbor, _ in graph.adjacency_list[node]:
                visit(neighbor)
            
            temp_visited.remove(node)
            visited.add(node)
            result.append(node)
        
        for node in graph.nodes:
            if node not in visited:
                visit(node)
        
        result.reverse()
        return result


class GraphConnectivity:
    """Graph connectivity algorithms."""
    
    @staticmethod
    def find_connected_components(graph: Graph) -> List[Set[str]]:
        """Find connected components using BFS."""
        visited = set()
        components = []
        
        for node in graph.nodes:
            if node not in visited:
                # BFS from this node
                component = set()
                queue = [node]
                
                while queue:
                    current = queue.pop(0)
                    
                    if current not in visited:
                        visited.add(current)
                        component.add(current)
                        
                        for neighbor, _ in graph.adjacency_list[current]:
                            if neighbor not in visited:
                                queue.append(neighbor)
                
                components.append(component)
        
        return components
    
    @staticmethod
    def is_connected(graph: Graph) -> bool:
        """Check if graph is connected."""
        if not graph.nodes:
            return True
        
        components = GraphConnectivity.find_connected_components(graph)
        return len(components) == 1
    
    @staticmethod
    def find_strongly_connected_components(graph: Graph) -> List[Set[str]]:
        """Find strongly connected components (Kosaraju's algorithm)."""
        # First pass: DFS to get finishing times
        visited = set()
        finish_order = []
        
        def dfs1(node):
            visited.add(node)
            for neighbor, _ in graph.adjacency_list[node]:
                if neighbor not in visited:
                    dfs1(neighbor)
            finish_order.append(node)
        
        for node in graph.nodes:
            if node not in visited:
                dfs1(node)
        
        # Reverse graph
        reversed_graph = Graph(GraphType.DIRECTED)
        for node in graph.nodes:
            reversed_graph.add_node(node)
        
        for source in graph.adjacency_list:
            for destination, weight in graph.adjacency_list[source]:
                reversed_graph.add_edge(destination, source, weight)
        
        # Second pass: DFS on reversed graph
        visited.clear()
        sccs = []
        
        def dfs2(node, component):
            visited.add(node)
            component.add(node)
            for neighbor, _ in reversed_graph.adjacency_list[node]:
                if neighbor not in visited:
                    dfs2(neighbor, component)
        
        for node in reversed(finish_order):
            if node not in visited:
                component = set()
                dfs2(node, component)
                sccs.append(component)
        
        return sccs


class MaximumFlow:
    """Maximum flow algorithms."""
    
    @staticmethod
    def ford_fulkerson(graph: Graph, source: str, sink: str) -> float:
        """Ford-Fulkerson algorithm for maximum flow."""
        if source not in graph.nodes or sink not in graph.nodes:
            return 0.0
        
        # Create residual graph
        residual = {node: {} for node in graph.nodes}
        
        for src in graph.adjacency_list:
            for dest, weight in graph.adjacency_list[src]:
                residual[src][dest] = weight
                if dest not in residual:
                    residual[dest] = {}
                if src not in residual[dest]:
                    residual[dest][src] = 0
        
        max_flow = 0.0
        
        def bfs_find_path():
            parent = {node: None for node in graph.nodes}
            visited = set()
            queue = [source]
            visited.add(source)
            
            while queue:
                current = queue.pop(0)
                
                for neighbor, capacity in residual[current].items():
                    if neighbor not in visited and capacity > 0:
                        visited.add(neighbor)
                        parent[neighbor] = current
                        queue.append(neighbor)
                        if neighbor == sink:
                            return parent
            
            return None
        
        # Find augmenting paths
        while True:
            parent = bfs_find_path()
            
            if parent is None or parent[sink] is None:
                break
            
            # Find minimum capacity along path
            path_flow = float('inf')
            current = sink
            
            while current != source:
                prev = parent[current]
                path_flow = min(path_flow, residual[prev][current])
                current = prev
            
            # Update residual capacities
            current = sink
            while current != source:
                prev = parent[current]
                residual[prev][current] -= path_flow
                residual[current][prev] += path_flow
                current = prev
            
            max_flow += path_flow
        
        return max_flow


class GraphColoring:
    """Graph coloring algorithms."""
    
    @staticmethod
    def greedy_coloring(graph: Graph) -> Dict[str, int]:
        """Greedy graph coloring algorithm."""
        colors = {}
        used_colors = set()
        
        # Sort nodes by degree (descending)
        nodes_sorted = sorted(graph.nodes.keys(), 
                            key=lambda x: len(graph.adjacency_list[x]), 
                            reverse=True)
        
        for node in nodes_sorted:
            # Get colors of neighbors
            neighbor_colors = set()
            for neighbor, _ in graph.adjacency_list[node]:
                if neighbor in colors:
                    neighbor_colors.add(colors[neighbor])
            
            # Find smallest available color
            color = 0
            while color in neighbor_colors:
                color += 1
            
            colors[node] = color
            used_colors.add(color)
        
        return colors
    
    @staticmethod
    def is_bipartite(graph: Graph) -> bool:
        """Check if graph is bipartite using BFS."""
        if not graph.nodes:
            return True
        
        colors = {}
        
        for start_node in graph.nodes:
            if start_node in colors:
                continue
            
            # BFS coloring
            queue = [start_node]
            colors[start_node] = 0
            
            while queue:
                current = queue.pop(0)
                
                for neighbor, _ in graph.adjacency_list[current]:
                    if neighbor not in colors:
                        colors[neighbor] = 1 - colors[current]
                        queue.append(neighbor)
                    elif colors[neighbor] == colors[current]:
                        return False
        
        return True


class GraphAnalyzer:
    """Graph analysis utilities."""
    
    @staticmethod
    def calculate_degree(graph: Graph, node: str) -> int:
        """Calculate degree of a node."""
        if node not in graph.adjacency_list:
            return 0
        return len(graph.adjacency_list[node])
    
    @staticmethod
    def calculate_degree_centrality(graph: Graph) -> Dict[str, float]:
        """Calculate degree centrality for all nodes."""
        max_degree = max(len(graph.adjacency_list[node]) for node in graph.nodes)
        
        if max_degree == 0:
            return {node: 0.0 for node in graph.nodes}
        
        centrality = {}
        for node in graph.nodes:
            degree = len(graph.adjacency_list[node])
            centrality[node] = degree / max_degree
        
        return centrality
    
    @staticmethod
    def calculate_clustering_coefficient(graph: Graph, node: str) -> float:
        """Calculate clustering coefficient for a node."""
        if node not in graph.adjacency_list:
            return 0.0
        
        neighbors = graph.adjacency_list[node]
        k = len(neighbors)
        
        if k < 2:
            return 0.0
        
        # Count edges between neighbors
        edges_between_neighbors = 0
        neighbor_ids = [neighbor for neighbor, _ in neighbors]
        
        for i in range(len(neighbor_ids)):
            for j in range(i + 1, len(neighbor_ids)):
                node1, node2 = neighbor_ids[i], neighbor_ids[j]
                
                # Check if edge exists
                for neighbor, _ in graph.adjacency_list[node1]:
                    if neighbor == node2:
                        edges_between_neighbors += 1
                        break
        
        possible_edges = k * (k - 1) / 2
        coefficient = edges_between_neighbors / possible_edges if possible_edges > 0 else 0.0
        
        return coefficient
    
    @staticmethod
    def detect_cycle(graph: Graph) -> bool:
        """Detect if graph contains cycle using DFS."""
        visited = set()
        rec_stack = set()
        
        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor, _ in graph.adjacency_list[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph.nodes:
            if node not in visited:
                if dfs(node):
                    return True
        
        return False


def demonstrate_graph_algorithms():
    """Demonstrate graph algorithms functionality."""
    print("=== Graph Algorithms Demonstration ===\n")
    
    # Graph Creation
    print("1. Graph Creation:")
    graph = Graph(GraphType.UNDIRECTED)
    
    graph.add_node("A")
    graph.add_node("B")
    graph.add_node("C")
    graph.add_node("D")
    graph.add_node("E")
    
    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("B", "C", 1)
    graph.add_edge("B", "D", 5)
    graph.add_edge("C", "D", 8)
    graph.add_edge("C", "E", 10)
    graph.add_edge("D", "E", 2)
    
    print(f"   Nodes: {graph.get_node_count()}")
    print(f"   Edges: {graph.get_edge_count()}")
    print(f"   Neighbors of A: {graph.get_neighbors('A')}")
    
    # Graph Traversal
    print("\n2. Graph Traversal:")
    bfs_result = GraphTraversal.bfs(graph, "A")
    print(f"   BFS from A: {bfs_result}")
    
    dfs_result = GraphTraversal.dfs(graph, "A")
    print(f"   DFS from A: {dfs_result}")
    
    # Shortest Path
    print("\n3. Shortest Path:")
    distances = ShortestPath.dijkstra(graph, "A")
    print(f"   Distances from A: {distances}")
    
    shortest_distance, shortest_path = ShortestPath.dijkstra_path(graph, "A", "E")
    print(f"   Shortest path A to E: {shortest_path} (distance: {shortest_distance})")
    
    # Minimum Spanning Tree
    print("\n4. Minimum Spanning Tree:")
    mst_weight, mst_edges = MinimumSpanningTree.prim(graph, "A")
    print(f"   MST weight (Prim's): {mst_weight}")
    print(f"   MST edges: {[(e.source, e.destination) for e in mst_edges]}")
    
    kruskal_weight, kruskal_edges = MinimumSpanningTree.kruskal(graph)
    print(f"   MST weight (Kruskal's): {kruskal_weight}")
    
    # Topological Sort
    print("\n5. Topological Sort:")
    dag = Graph(GraphType.DIRECTED)
    dag.add_node("A")
    dag.add_node("B")
    dag.add_node("C")
    dag.add_node("D")
    dag.add_edge("A", "B")
    dag.add_edge("A", "C")
    dag.add_edge("B", "D")
    dag.add_edge("C", "D")
    
    topo_order = TopologicalSort.kahn(dag)
    print(f"   Topological order: {topo_order}")
    
    # Graph Connectivity
    print("\n6. Graph Connectivity:")
    components = GraphConnectivity.find_connected_components(graph)
    print(f"   Connected components: {len(components)}")
    print(f"   Is connected: {GraphConnectivity.is_connected(graph)}")
    
    # Graph Coloring
    print("\n7. Graph Coloring:")
    colors = GraphColoring.greedy_coloring(graph)
    print(f"   Node colors: {colors}")
    print(f"   Number of colors used: {len(set(colors.values()))}")
    
    is_bipartite = GraphColoring.is_bipartite(graph)
    print(f"   Is bipartite: {is_bipartite}")
    
    # Graph Analysis
    print("\n8. Graph Analysis:")
    degree_centrality = GraphAnalyzer.calculate_degree_centrality(graph)
    print(f"   Degree centrality: {degree_centrality}")
    
    clustering_coeff = GraphAnalyzer.calculate_clustering_coefficient(graph, "A")
    print(f"   Clustering coefficient of A: {clustering_coeff:.3f}")
    
    has_cycle = GraphAnalyzer.detect_cycle(graph)
    print(f"   Has cycle: {has_cycle}")
    
    # Maximum Flow
    print("\n9. Maximum Flow:")
    flow_graph = Graph(GraphType.DIRECTED)
    flow_graph.add_node("S")
    flow_graph.add_node("A")
    flow_graph.add_node("B")
    flow_graph.add_node("T")
    flow_graph.add_edge("S", "A", 10)
    flow_graph.add_edge("S", "B", 10)
    flow_graph.add_edge("A", "B", 2)
    flow_graph.add_edge("A", "T", 8)
    flow_graph.add_edge("B", "T", 9)
    
    max_flow = MaximumFlow.ford_fulkerson(flow_graph, "S", "T")
    print(f"   Maximum flow from S to T: {max_flow}")
    
    # Floyd-Warshall
    print("\n10. All Pairs Shortest Paths:")
    all_distances = ShortestPath.floyd_warshall(graph)
    print(f"   Distance matrix (A to E): {all_distances['A']['E']}")
    
    print("\n=== Demonstration Complete ===")
    print("\nGraph Algorithms Best Practices:")
    print("- Choose appropriate algorithm for your use case")
    print("- Consider graph size and density when selecting algorithms")
    print("- Dijkstra is efficient for sparse graphs")
    print("- Bellman-Ford handles negative weights")
    print("- Floyd-Warshall for all-pairs shortest paths")
    print("- Prim's and Kruskal's for MST in different scenarios")
    print("- Topological sort only works for DAGs")
    print("- Graph coloring is NP-hard (greedy is approximation)")
    print("- Consider memory vs. time trade-offs")
    print("- Use adjacency lists for sparse graphs")
    print("- Use adjacency matrices for dense graphs")


if __name__ == "__main__":
    demonstrate_graph_algorithms()