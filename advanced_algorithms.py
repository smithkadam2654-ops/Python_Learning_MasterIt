"""
Advanced Algorithms - Complex algorithm implementations.
Features: Randomized algorithms, approximation algorithms, and advanced techniques.
"""

from typing import List, Optional, Tuple
import random
import math


class AdvancedAlgorithms:
    """Advanced algorithm implementations."""
    
    @staticmethod
    def quickselect(arr: List[int], k: int) -> int:
        """
        Quickselect - find kth smallest element.
        
        Args:
            arr: Array of numbers
            k: kth smallest (1-indexed)
            
        Returns:
            kth smallest element
        """
        if k < 1 or k > len(arr):
            raise ValueError("k out of range")
        
        return AdvancedAlgorithms._quickselect_helper(arr, 0, len(arr) - 1, k - 1)
    
    @staticmethod
    def _quickselect_helper(arr: List[int], left: int, right: int, k: int) -> int:
        """Helper for quickselect."""
        if left == right:
            return arr[left]
        
        pivot_index = AdvancedAlgorithms._partition(arr, left, right)
        
        if k == pivot_index:
            return arr[k]
        elif k < pivot_index:
            return AdvancedAlgorithms._quickselect_helper(arr, left, pivot_index - 1, k)
        else:
            return AdvancedAlgorithms._quickselect_helper(arr, pivot_index + 1, right, k)
    
    @staticmethod
    def _partition(arr: List[int], left: int, right: int) -> int:
        """Partition for quickselect."""
        pivot = arr[right]
        i = left
        
        for j in range(left, right):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        
        arr[i], arr[right] = arr[right], arr[i]
        return i
    
    @staticmethod
    def reservoir_sampling(stream: List[int], k: int) -> List[int]:
        """
        Reservoir sampling - select k random items from stream.
        
        Args:
            stream: Stream of items
            k: Number of items to select
            
        Returns:
            k randomly selected items
        """
        reservoir = stream[:k]
        
        for i in range(k, len(stream)):
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = stream[i]
        
        return reservoir
    
    @staticmethod
    def fisher_yates_shuffle(arr: List[int]) -> List[int]:
        """
        Fisher-Yates shuffle - random permutation.
        
        Args:
            arr: Array to shuffle
            
        Returns:
            Shuffled array
        """
        arr = arr.copy()
        
        for i in range(len(arr) - 1, 0, -1):
            j = random.randint(0, i)
            arr[i], arr[j] = arr[j], arr[i]
        
        return arr
    
    @staticmethod
    def monte_carlo_pi(samples: int = 1000000) -> float:
        """
        Estimate π using Monte Carlo method.
        
        Args:
            samples: Number of samples
            
        Returns:
            Estimated value of π
        """
        inside = 0
        
        for _ in range(samples):
            x = random.random()
            y = random.random()
            
            if x * x + y * y <= 1:
                inside += 1
        
        return 4 * inside / samples
    
    @staticmethod
    def miller_rabin_primality(n: int, k: int = 5) -> bool:
        """
        Miller-Rabin primality test (probabilistic).
        
        Args:
            n: Number to test
            k: Number of iterations (accuracy)
            
        Returns:
            True if probably prime, False if definitely composite
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Write n-1 as 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Witness loop
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True
    
    @staticmethod
    def karger_min_cut(graph: List[List[int]]) -> int:
        """
        Karger's algorithm for minimum cut (probabilistic).
        
        Args:
            graph: Adjacency list representation
            
        Returns:
            Minimum cut size
        """
        import random
        
        # Convert to edge list
        edges = []
        for u in range(len(graph)):
            for v in graph[u]:
                if u < v:  # Avoid duplicates
                    edges.append((u, v))
        
        # Contract edges until 2 vertices remain
        while len(graph) > 2:
            # Pick random edge
            edge = random.choice(edges)
            u, v = edge
            
            # Merge v into u
            graph[u].extend(graph[v])
            
            # Update edges
            for w in graph[v]:
                for i in range(len(graph[w])):
                    if graph[w][i] == v:
                        graph[w][i] = u
            
            # Remove self-loops
            graph[u] = [x for x in graph[u] if x != u]
            
            # Remove v
            graph.pop(v)
            
            # Update edges
            edges = [(x, y) for x, y in edges if x != v and y != v]
        
        # Count edges between remaining vertices
        return len(graph[0])
    
    @staticmethod
    def nearest_neighbor(points: List[Tuple[float, float]], query: Tuple[float, float]) -> Tuple[float, Tuple[float, float]]:
        """
        Find nearest neighbor using brute force.
        
        Args:
            points: List of points
            query: Query point
            
        Returns:
            Tuple of (distance, nearest_point)
        """
        min_dist = float('inf')
        nearest = None
        
        for point in points:
            dist = math.sqrt((point[0] - query[0]) ** 2 + (point[1] - query[1]) ** 2)
            if dist < min_dist:
                min_dist = dist
                nearest = point
        
        return (min_dist, nearest)
    
    @staticmethod
    def approximation_vertex_cover(graph: List[List[int]]) -> List[int]:
        """
        Approximate vertex cover (2-approximation).
        
        Args:
            graph: Adjacency list
            
        Returns:
            List of vertices in cover
        """
        cover = set()
        edges = set()
        
        # Get all edges
        for u in range(len(graph)):
            for v in graph[u]:
                if u < v:
                    edges.add((u, v))
        
        while edges:
            # Pick random edge
            u, v = edges.pop()
            
            # Add both vertices to cover
            cover.add(u)
            cover.add(v)
            
            # Remove all edges incident to u or v
            edges = {(x, y) for x, y in edges if x != u and x != v and y != u and y != v}
        
        return list(cover)
    
    @staticmethod
    def approximation_set_cover(universe: set, sets: List[set]) -> List[int]:
        """
        Approximate set cover (greedy approximation).
        
        Args:
            universe: Universe of elements
            sets: List of sets
            
        Returns:
            Indices of selected sets
        """
        uncovered = universe.copy()
        selected = []
        
        while uncovered:
            # Select set covering most uncovered elements
            best_index = 0
            best_cover = set()
            
            for i, s in enumerate(sets):
                covered = uncovered & s
                if len(covered) > len(best_cover):
                    best_cover = covered
                    best_index = i
            
            selected.append(best_index)
            uncovered -= best_cover
        
        return selected
    
    @staticmethod
    def random_partition(arr: List[int]) -> List[int]:
        """
        Random partition of array.
        
        Args:
            arr: Array to partition
            
        Returns:
            Partitioned array
        """
        arr = arr.copy()
        
        # Random pivot
        pivot_index = random.randint(0, len(arr) - 1)
        pivot = arr[pivot_index]
        
        # Partition
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return left + middle + right
    
    @staticmethod
    def bogosort(arr: List[int]) -> List[int]:
        """
        Bogosort - extremely inefficient sorting (for demonstration only).
        
        Args:
            arr: Array to sort
            
        Returns:
            Sorted array
        """
        arr = arr.copy()
        
        def is_sorted(a: List[int]) -> bool:
            return all(a[i] <= a[i + 1] for i in range(len(a) - 1))
        
        while not is_sorted(arr):
            random.shuffle(arr)
        
        return arr
    
    @staticmethod
    def sleep_sort(arr: List[int]) -> List[int]:
        """
        Sleep sort - sorts by sleeping for each value (for demonstration only).
        
        Args:
            arr: Array of positive integers
            
        Returns:
            Sorted array
        """
        import threading
        import time
        
        result = []
        
        def sleep_and_append(val: int) -> None:
            time.sleep(val / 1000.0)  # Scale down for demo
            result.append(val)
        
        threads = []
        for val in arr:
            t = threading.Thread(target=sleep_and_append, args=(val,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        return result


def main() -> None:
    """Demonstrate advanced algorithms."""
    
    print("=== Advanced Algorithms Demo ===")
    
    # Quickselect
    print("\n--- Quickselect ---")
    arr = [3, 2, 1, 5, 6, 4]
    k = 3
    print(f"Array: {arr}, k: {k}")
    print(f"Kth smallest: {AdvancedAlgorithms.quickselect(arr.copy(), k)}")
    
    # Reservoir sampling
    print("\n--- Reservoir Sampling ---")
    stream = list(range(1, 101))
    k = 10
    print(f"Stream: 1-100, k: {k}")
    print(f"Sample: {AdvancedAlgorithms.reservoir_sampling(stream, k)}")
    
    # Fisher-Yates shuffle
    print("\n--- Fisher-Yates Shuffle ---")
    arr = [1, 2, 3, 4, 5]
    print(f"Original: {arr}")
    print(f"Shuffled: {AdvancedAlgorithms.fisher_yates_shuffle(arr)}")
    
    # Monte Carlo π
    print("\n--- Monte Carlo π ---")
    samples = 100000
    pi_estimate = AdvancedAlgorithms.monte_carlo_pi(samples)
    print(f"Samples: {samples}")
    print(f"Estimated π: {pi_estimate}")
    print(f"Actual π: {math.pi}")
    print(f"Error: {abs(pi_estimate - math.pi):.6f}")
    
    # Miller-Rabin primality
    print("\n--- Miller-Rabin Primality ---")
    for n in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        is_prime = AdvancedAlgorithms.miller_rabin_primality(n)
        print(f"{n}: {is_prime}")
    
    # Nearest neighbor
    print("\n--- Nearest Neighbor ---")
    points = [(0, 0), (3, 4), (1, 1), (5, 5), (2, 2)]
    query = (1, 2)
    print(f"Points: {points}")
    print(f"Query: {query}")
    dist, nearest = AdvancedAlgorithms.nearest_neighbor(points, query)
    print(f"Nearest: {nearest}, distance: {dist:.2f}")
    
    # Approximation vertex cover
    print("\n--- Approximation Vertex Cover ---")
    graph = [[1, 2], [0, 2], [0, 1, 3], [2]]
    print(f"Graph: {graph}")
    cover = AdvancedAlgorithms.approximation_vertex_cover(graph)
    print(f"Vertex cover: {cover}")
    
    # Approximation set cover
    print("\n--- Approximation Set Cover ---")
    universe = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    sets = [{1, 2, 3, 4, 5}, {4, 5, 6, 7, 8}, {6, 7, 8, 9, 10}]
    print(f"Universe: {universe}")
    print(f"Sets: {sets}")
    selected = AdvancedAlgorithms.approximation_set_cover(universe, sets)
    print(f"Selected indices: {selected}")
    print(f"Selected sets: {[sets[i] for i in selected]}")
    
    # Random partition
    print("\n--- Random Partition ---")
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"Original: {arr}")
    print(f"Partitioned: {AdvancedAlgorithms.random_partition(arr)}")


if __name__ == "__main__":
    main()
