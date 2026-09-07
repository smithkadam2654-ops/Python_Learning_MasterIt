"""
Topological Sort - Linear ordering of vertices in a DAG.
Features: Kahn's algorithm, DFS-based approach, and cycle detection.
"""

from typing import List, Dict, Set, Optional
from collections import deque, defaultdict


class TopologicalSort:
    """Topological sort implementation."""
    
    @staticmethod
    def sort_kahn(graph: Dict[str, List[str]]) -> Optional[List[str]]:
        """
        Topological sort using Kahn's algorithm (BFS-based).
        
        Args:
            graph: Adjacency list representation of DAG
            
        Returns:
            Topological order or None if cycle detected
        """
        # Calculate in-degrees
        in_degree = {node: 0 for node in graph}
        
        for node in graph:
            for neighbor in graph[node]:
                if neighbor not in in_degree:
                    in_degree[neighbor] = 0
                in_degree[neighbor] += 1
        
        # Initialize queue with nodes having in-degree 0
        queue = deque([node for node, degree in in_degree.items() if degree == 0])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            # Reduce in-degree of neighbors
            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Check for cycle
        if len(result) != len(in_degree):
            return None  # Cycle detected
        
        return result
    
    @staticmethod
    def sort_dfs(graph: Dict[str, List[str]]) -> Optional[List[str]]:
        """
        Topological sort using DFS.
        
        Args:
            graph: Adjacency list representation of DAG
            
        Returns:
            Topological order or None if cycle detected
        """
        visited = set()
        temp_visited = set()  # For cycle detection
        result = []
        
        def dfs(node: str) -> bool:
            """DFS helper that returns False if cycle detected."""
            if node in temp_visited:
                return False  # Cycle detected
            if node in visited:
                return True  # Already processed
            
            temp_visited.add(node)
            
            for neighbor in graph.get(node, []):
                if not dfs(neighbor):
                    return False
            
            temp_visited.remove(node)
            visited.add(node)
            result.append(node)
            
            return True
        
        # Visit all nodes
        for node in graph:
            if node not in visited:
                if not dfs(node):
                    return None  # Cycle detected
        
        return result[::-1]  # Reverse for topological order
    
    @staticmethod
    def has_cycle(graph: Dict[str, List[str]]) -> bool:
        """
        Check if graph has a cycle.
        
        Args:
            graph: Adjacency list representation
            
        Returns:
            True if cycle exists
        """
        visited = set()
        rec_stack = set()
        
        def dfs_cycle(node: str) -> bool:
            """DFS for cycle detection."""
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                if dfs_cycle(node):
                    return True
        
        return False
    
    @staticmethod
    def get_levels(graph: Dict[str, List[str]]) -> Dict[str, int]:
        """
        Get level of each node (longest path from source).
        
        Args:
            graph: Adjacency list representation
            
        Returns:
            Dictionary mapping node to its level
        """
        top_order = TopologicalSort.sort_kahn(graph)
        if top_order is None:
            return {}
        
        levels = {node: 0 for node in top_order}
        
        for node in top_order:
            for neighbor in graph.get(node, []):
                levels[neighbor] = max(levels[neighbor], levels[node] + 1)
        
        return levels


class TaskScheduler:
    """Task scheduler using topological sort."""
    
    def __init__(self) -> None:
        """Initialize task scheduler."""
        self.tasks: Dict[str, List[str]] = {}
    
    def add_task(self, task: str, dependencies: List[str] = None) -> None:
        """
        Add task with dependencies.
        
        Args:
            task: Task name
            dependencies: List of tasks this task depends on
        """
        self.tasks[task] = dependencies or []
    
    def get_execution_order(self) -> Optional[List[str]]:
        """
        Get valid execution order.
        
        Returns:
            Execution order or None if circular dependency
        """
        return TopologicalSort.sort_kahn(self.tasks)
    
    def get_parallel_levels(self) -> Optional[List[List[str]]]:
        """
        Get tasks grouped by parallel execution levels.
        
        Returns:
            List of task groups by level or None if circular dependency
        """
        levels = TopologicalSort.get_levels(self.tasks)
        if not levels:
            return None
        
        # Group by level
        level_groups = defaultdict(list)
        for task, level in levels.items():
            level_groups[level].append(task)
        
        # Sort by level
        max_level = max(level_groups.keys()) if level_groups else 0
        return [level_groups[i] for i in range(max_level + 1)]


def main() -> None:
    """Demonstrate topological sort."""
    
    print("=== Topological Sort Demo ===")
    
    # Example DAG (course prerequisites)
    graph = {
        "CS101": [],
        "CS102": ["CS101"],
        "CS201": ["CS102"],
        "CS202": ["CS102"],
        "CS301": ["CS201", "CS202"],
        "CS302": ["CS201"],
        "CS401": ["CS301", "CS302"]
    }
    
    print("Course Prerequisites:")
    for course, prereqs in graph.items():
        print(f"  {course}: {prereqs if prereqs else 'None'}")
    
    # Kahn's algorithm
    print("\n--- Kahn's Algorithm ---")
    kahn_order = TopologicalSort.sort_kahn(graph)
    print(f"Topological order: {kahn_order}")
    
    # DFS-based
    print("\n--- DFS-based ---")
    dfs_order = TopologicalSort.sort_dfs(graph)
    print(f"Topological order: {dfs_order}")
    
    # Levels
    print("\n--- Task Levels ---")
    levels = TopologicalSort.get_levels(graph)
    for task, level in sorted(levels.items(), key=lambda x: x[1]):
        print(f"  Level {level}: {task}")
    
    # Cycle detection
    print("\n--- Cycle Detection ---")
    print(f"Has cycle: {TopologicalSort.has_cycle(graph)}")
    
    # Graph with cycle
    cyclic_graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"]
    }
    print(f"Cyclic graph has cycle: {TopologicalSort.has_cycle(cyclic_graph)}")
    print(f"Topological sort of cyclic: {TopologicalSort.sort_kahn(cyclic_graph)}")
    
    # Task scheduler
    print("\n=== Task Scheduler ===")
    scheduler = TaskScheduler()
    
    scheduler.add_task("A", [])
    scheduler.add_task("B", ["A"])
    scheduler.add_task("C", ["A"])
    scheduler.add_task("D", ["B", "C"])
    scheduler.add_task("E", ["D"])
    
    print("Execution order:")
    order = scheduler.get_execution_order()
    print(f"  {order}")
    
    print("\nParallel execution levels:")
    parallel = scheduler.get_parallel_levels()
    for i, level in enumerate(parallel):
        print(f"  Level {i}: {level}")
    
    # Build order example
    print("\n=== Build Order Example ---")
    build_graph = {
        "main": ["utils", "parser"],
        "utils": ["base"],
        "parser": ["base", "lexer"],
        "lexer": ["base"],
        "base": []
    }
    
    build_order = TopologicalSort.sort_kahn(build_graph)
    print(f"Build order: {build_order}")
    
    # Multiple valid orders
    print("\n--- Multiple Valid Orders ---")
    simple_graph = {
        "A": [],
        "B": [],
        "C": ["A", "B"],
        "D": ["C"]
    }
    
    print(f"Valid order 1: {TopologicalSort.sort_kahn(simple_graph)}")
    print(f"Valid order 2: {TopologicalSort.sort_dfs(simple_graph)}")
    
    # Large DAG performance
    print("\n=== Performance Test ===")
    import time
    
    # Generate large DAG
    n = 1000
    large_graph = {str(i): [] for i in range(n)}
    
    for i in range(n):
        if i > 0:
            # Add edge from random previous node
            import random
            prev = random.randint(0, i - 1)
            large_graph[str(i)].append(str(prev))
    
    start = time.time()
    TopologicalSort.sort_kahn(large_graph)
    kahn_time = (time.time() - start) * 1000
    
    start = time.time()
    TopologicalSort.sort_dfs(large_graph)
    dfs_time = (time.time() - start) * 1000
    
    print(f"Kahn's algorithm: {kahn_time:.2f}ms")
    print(f"DFS-based: {dfs_time:.2f}ms")
    
    # Edge cases
    print("\n--- Edge Cases ---")
    
    # Empty graph
    empty = {}
    print(f"Empty graph: {TopologicalSort.sort_kahn(empty)}")
    
    # Single node
    single = {"A": []}
    print(f"Single node: {TopologicalSort.sort_kahn(single)}")
    
    # Linear chain
    linear = {"A": [], "B": ["A"], "C": ["B"], "D": ["C"]}
    print(f"Linear chain: {TopologicalSort.sort_kahn(linear)}")


if __name__ == "__main__":
    main()
