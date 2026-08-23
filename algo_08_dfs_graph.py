def dfs(graph, start, visited=None):
    """
    Traverses a graph using Depth-First Search (DFS).
    """
    if visited is None:
        visited = set()
        
    visited.add(start)
    print(start, end=" ")
    
    for next_node in graph[start] - visited:
        dfs(graph, next_node, visited)
        
    return visited

if __name__ == "__main__":
    # Representing a graph using an adjacency list (set for faster lookups)
    graph = {
        'A': {'B', 'C'},
        'B': {'A', 'D', 'E'},
        'C': {'A', 'F'},
        'D': {'B'},
        'E': {'B', 'F'},
        'F': {'C', 'E'}
    }
    
    print("DFS traversal starting from node 'A':")
    dfs(graph, 'A')
    print()
