"""
Optimization Algorithms - Mathematical optimization techniques.
Features: Linear programming, gradient descent, and optimization problems.
"""

from typing import List, Tuple, Optional
import math


class OptimizationAlgorithms:
    """Optimization algorithm implementations."""
    
    @staticmethod
    def gradient_descent(f, df, x0: float, learning_rate: float = 0.01, 
                        max_iter: int = 1000, tolerance: float = 1e-6) -> Tuple[float, List[float]]:
        """
        Gradient descent for function minimization.
        
        Args:
            f: Function to minimize
            df: Derivative of function
            x0: Initial guess
            learning_rate: Step size
            max_iter: Maximum iterations
            tolerance: Convergence tolerance
            
        Returns:
            Tuple of (minimum, history of values)
        """
        x = x0
        history = [x]
        
        for _ in range(max_iter):
            gradient = df(x)
            x_new = x - learning_rate * gradient
            history.append(x_new)
            
            if abs(x_new - x) < tolerance:
                break
            
            x = x_new
        
        return (x, history)
    
    @staticmethod
    def gradient_descent_multivariable(f, grad_f, x0: List[float], 
                                       learning_rate: float = 0.01,
                                       max_iter: int = 1000, 
                                       tolerance: float = 1e-6) -> Tuple[List[float], List[List[float]]]:
        """
        Gradient descent for multivariable function minimization.
        
        Args:
            f: Function to minimize
            grad_f: Gradient of function
            x0: Initial guess (list)
            learning_rate: Step size
            max_iter: Maximum iterations
            tolerance: Convergence tolerance
            
        Returns:
            Tuple of (minimum point, history of points)
        """
        x = x0.copy()
        history = [x.copy()]
        
        for _ in range(max_iter):
            gradient = grad_f(x)
            x_new = [x[i] - learning_rate * gradient[i] for i in range(len(x))]
            history.append(x_new.copy())
            
            # Check convergence
            diff = sum(abs(x_new[i] - x[i]) for i in range(len(x)))
            if diff < tolerance:
                break
            
            x = x_new
        
        return (x, history)
    
    @staticmethod
    def newton_method(f, df, d2f, x0: float, max_iter: int = 100, 
                     tolerance: float = 1e-6) -> Tuple[float, List[float]]:
        """
        Newton's method for finding roots.
        
        Args:
            f: Function
            df: First derivative
            d2f: Second derivative
            x0: Initial guess
            max_iter: Maximum iterations
            tolerance: Convergence tolerance
            
        Returns:
            Tuple of (root, history of values)
        """
        x = x0
        history = [x]
        
        for _ in range(max_iter):
            fx = f(x)
            dfx = df(x)
            
            if abs(dfx) < tolerance:
                break
            
            x_new = x - fx / dfx
            history.append(x_new)
            
            if abs(x_new - x) < tolerance:
                break
            
            x = x_new
        
        return (x, history)
    
    @staticmethod
    def binary_search_min(f, low: float, high: float, 
                          tolerance: float = 1e-6) -> float:
        """
        Binary search for minimum of unimodal function.
        
        Args:
            f: Unimodal function
            low: Lower bound
            high: Upper bound
            tolerance: Convergence tolerance
            
        Returns:
            Approximate minimum
        """
        while high - low > tolerance:
            mid1 = low + (high - low) / 3
            mid2 = high - (high - low) / 3
            
            if f(mid1) < f(mid2):
                high = mid2
            else:
                low = mid1
        
        return (low + high) / 2
    
    @staticmethod
    def golden_section_search(f, low: float, high: float, 
                             tolerance: float = 1e-6) -> float:
        """
        Golden section search for minimum of unimodal function.
        
        Args:
            f: Unimodal function
            low: Lower bound
            high: Upper bound
            tolerance: Convergence tolerance
            
        Returns:
            Approximate minimum
        """
        phi = (1 + math.sqrt(5)) / 2
        resphi = 2 - phi
        
        x1 = low + resphi * (high - low)
        x2 = high - resphi * (high - low)
        
        f1 = f(x1)
        f2 = f(x2)
        
        while abs(high - low) > tolerance:
            if f1 < f2:
                high = x2
                x2 = x1
                f2 = f1
                x1 = low + resphi * (high - low)
                f1 = f(x1)
            else:
                low = x1
                x1 = x2
                f1 = f2
                x2 = high - resphi * (high - low)
                f2 = f(x2)
        
        return (low + high) / 2
    
    @staticmethod
    def simulated_annealing(f, initial_state: float, 
                          temperature: float = 100.0, 
                          cooling_rate: float = 0.95,
                          min_temp: float = 0.01) -> Tuple[float, float]:
        """
        Simulated annealing for global optimization.
        
        Args:
            f: Function to minimize
            initial_state: Initial state
            temperature: Initial temperature
            cooling_rate: Temperature cooling rate
            min_temp: Minimum temperature
            
        Returns:
            Tuple of (best_state, best_value)
        """
        current_state = initial_state
        current_value = f(current_state)
        best_state = current_state
        best_value = current_value
        
        while temperature > min_temp:
            # Generate neighbor
            neighbor = current_state + (random.random() - 0.5) * temperature
            neighbor_value = f(neighbor)
            
            # Accept or reject
            delta = neighbor_value - current_value
            if delta < 0 or math.exp(-delta / temperature) > random.random():
                current_state = neighbor
                current_value = neighbor_value
                
                if current_value < best_value:
                    best_state = current_state
                    best_value = current_value
            
            temperature *= cooling_rate
        
        return (best_state, best_value)
    
    @staticmethod
    def hill_climbing(f, initial_state: float, step_size: float = 0.1,
                     max_iter: int = 1000) -> Tuple[float, float]:
        """
        Hill climbing for local optimization.
        
        Args:
            f: Function to minimize
            initial_state: Initial state
            step_size: Step size for neighbors
            max_iter: Maximum iterations
            
        Returns:
            Tuple of (best_state, best_value)
        """
        current_state = initial_state
        current_value = f(current_state)
        
        for _ in range(max_iter):
            # Generate neighbors
            neighbors = [
                current_state - step_size,
                current_state + step_size
            ]
            
            # Find best neighbor
            best_neighbor = None
            best_neighbor_value = current_value
            
            for neighbor in neighbors:
                neighbor_value = f(neighbor)
                if neighbor_value < best_neighbor_value:
                    best_neighbor = neighbor
                    best_neighbor_value = neighbor_value
            
            # Move if improvement found
            if best_neighbor is not None and best_neighbor_value < current_value:
                current_state = best_neighbor
                current_value = best_neighbor_value
            else:
                break
        
        return (current_state, current_value)
    
    @staticmethod
    def linear_programming_simplex(c: List[float], A: List[List[float]], 
                                    b: List[float]) -> Optional[float]:
        """
        Simple linear programming (simplified for demonstration).
        
        Args:
            c: Objective function coefficients (maximize)
            A: Constraint matrix
            b: Constraint bounds
            
        Returns:
            Maximum value or None
        """
        # This is a simplified version - real simplex is more complex
        # For demonstration, we'll use a basic approach
        
        # Check if problem is feasible
        n_vars = len(c)
        n_constraints = len(b)
        
        # Simple check: find feasible solution
        # This is not a complete simplex implementation
        # Real implementation requires tableau method
        
        # For demo, return None (indicating need for full implementation)
        return None
    
    @staticmethod
    def knapsack_greedy(values: List[int], weights: List[int], 
                       capacity: int) -> Tuple[int, List[int]]:
        """
        Greedy approximation for 0/1 knapsack.
        
        Args:
            values: Item values
            weights: Item weights
            capacity: Knapsack capacity
            
        Returns:
            Tuple of (total_value, selected_indices)
        """
        # Calculate value-to-weight ratios
        items = [(i, values[i] / weights[i]) for i in range(len(values))]
        items.sort(key=lambda x: x[1], reverse=True)
        
        total_value = 0
        total_weight = 0
        selected = []
        
        for idx, ratio in items:
            if total_weight + weights[idx] <= capacity:
                selected.append(idx)
                total_value += values[idx]
                total_weight += weights[idx]
        
        return (total_value, selected)
    
    @staticmethod
    def traveling_salesman_nearest(distances: List[List[int]]) -> Tuple[int, List[int]]:
        """
        Nearest neighbor heuristic for TSP.
        
        Args:
            distances: Distance matrix
            
        Returns:
            Tuple of (total_distance, tour)
        """
        n = len(distances)
        unvisited = set(range(1, n))
        tour = [0]
        total_distance = 0
        current = 0
        
        while unvisited:
            # Find nearest unvisited city
            nearest = min(unvisited, key=lambda x: distances[current][x])
            total_distance += distances[current][nearest]
            tour.append(nearest)
            unvisited.remove(nearest)
            current = nearest
        
        # Return to start
        total_distance += distances[current][0]
        tour.append(0)
        
        return (total_distance, tour)


def main() -> None:
    """Demonstrate optimization algorithms."""
    
    import random
    
    print("=== Optimization Algorithms Demo ===")
    
    # Gradient descent
    print("\n--- Gradient Descent ---")
    f = lambda x: x ** 2 + 4 * x + 4
    df = lambda x: 2 * x + 4
    x0 = 0
    
    minimum, history = OptimizationAlgorithms.gradient_descent(f, df, x0)
    print(f"Function: f(x) = x² + 4x + 4")
    print(f"Initial: x = {x0}")
    print(f"Minimum: x = {minimum:.6f}")
    print(f"f(minimum) = {f(minimum):.6f}")
    
    # Newton's method
    print("\n--- Newton's Method ---")
    f = lambda x: x ** 2 - 2
    df = lambda x: 2 * x
    d2f = lambda x: 2
    x0 = 1
    
    root, history = OptimizationAlgorithms.newton_method(f, df, d2f, x0)
    print(f"Function: f(x) = x² - 2")
    print(f"Initial: x = {x0}")
    print(f"Root: x = {root:.6f}")
    print(f"f(root) = {f(root):.6f}")
    
    # Binary search minimization
    print("\n--- Binary Search Minimization ---")
    f = lambda x: (x - 2) ** 2
    minimum = OptimizationAlgorithms.binary_search_min(f, 0, 4)
    print(f"Function: f(x) = (x-2)²")
    print(f"Minimum: x = {minimum:.6f}")
    print(f"f(minimum) = {f(minimum):.6f}")
    
    # Golden section search
    print("\n--- Golden Section Search ---")
    f = lambda x: (x - 2) ** 2
    minimum = OptimizationAlgorithms.golden_section_search(f, 0, 4)
    print(f"Function: f(x) = (x-2)²")
    print(f"Minimum: x = {minimum:.6f}")
    print(f"f(minimum) = {f(minimum):.6f}")
    
    # Hill climbing
    print("\n--- Hill Climbing ---")
    f = lambda x: (x - 2) ** 2
    x0 = 0
    best_state, best_value = OptimizationAlgorithms.hill_climbing(f, x0)
    print(f"Function: f(x) = (x-2)²")
    print(f"Initial: x = {x0}")
    print(f"Best: x = {best_state:.6f}")
    print(f"f(best) = {best_value:.6f}")
    
    # Knapsack greedy
    print("\n--- Knapsack Greedy ---")
    values = [60, 100, 120]
    weights = [10, 20, 30]
    capacity = 50
    
    total_value, selected = OptimizationAlgorithms.knapsack_greedy(values, weights, capacity)
    print(f"Values: {values}")
    print(f"Weights: {weights}")
    print(f"Capacity: {capacity}")
    print(f"Selected indices: {selected}")
    print(f"Total value: {total_value}")
    
    # TSP nearest neighbor
    print("\n--- TSP Nearest Neighbor ---")
    distances = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    
    total_dist, tour = OptimizationAlgorithms.traveling_salesman_nearest(distances)
    print(f"Distance matrix: {distances}")
    print(f"Tour: {tour}")
    print(f"Total distance: {total_dist}")


if __name__ == "__main__":
    main()
