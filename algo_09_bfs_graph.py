from collections import deque

def bfs(graph, start):
    """
    Traverses a graph using Breadth-First Search (BFS).
    """
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        print(vertex, end=" ")
        
        for next_node in graph[vertex] - visited:
            visited.add(next_node)
            queue.append(next_node)

if __name__ == "__main__":
    # Representing a graph using an adjacency list
    graph = {
        'A': {'B', 'C'},
        'B': {'A', 'D', 'E'},
        'C': {'A', 'F'},
        'D': {'B'},
        'E': {'B', 'F'},
        'F': {'C', 'E'}
    }
    
    print("BFS traversal starting from node 'A':")
    bfs(graph, 'A')
    print()
