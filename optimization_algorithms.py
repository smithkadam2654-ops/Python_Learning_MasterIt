"""
Optimization Algorithms Module

This module provides comprehensive optimization algorithms including:
- Gradient Descent variants
- Genetic Algorithm
- Simulated Annealing
- Particle Swarm Optimization
- Hill Climbing
- Tabu Search
- Ant Colony Optimization
- Constraint handling
- Multi-objective optimization
- Optimization benchmarking

All functions include comprehensive docstrings and type hints.
"""

import random
import math
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum


try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class OptimizationType(Enum):
    """Types of optimization problems."""
    MINIMIZATION = "minimization"
    MAXIMIZATION = "maximization"


class ConstraintType(Enum):
    """Types of constraints."""
    EQUALITY = "equality"
    INEQUALITY = "inequality"
    BOUNDS = "bounds"


@dataclass
class Solution:
    """Solution representation."""
    variables: List[float]
    fitness: float
    generation: int = 0
    is_feasible: bool = True
    constraint_violations: List[str] = None
    
    def __post_init__(self):
        if self.constraint_violations is None:
            self.constraint_violations = []
    
    def copy(self) -> 'Solution':
        """Create copy of solution."""
        return Solution(
            variables=self.variables.copy(),
            fitness=self.fitness,
            generation=self.generation,
            is_feasible=self.is_feasible,
            constraint_violations=self.constraint_violations.copy()
        )


class ObjectiveFunction:
    """Objective function interface."""
    
    def __init__(self, opt_type: OptimizationType = OptimizationType.MINIMIZATION):
        """Initialize objective function."""
        self.opt_type = opt_type
    
    def evaluate(self, variables: List[float]) -> float:
        """Evaluate objective function."""
        raise NotImplementedError
    
    def gradient(self, variables: List[float]) -> List[float]:
        """Calculate gradient."""
        raise NotImplementedError


class SphereFunction(ObjectiveFunction):
    """Sphere function (unimodal, convex)."""
    
    def __init__(self, dimensions: int = 2):
        """Initialize sphere function."""
        super().__init__(OptimizationType.MINIMIZATION)
        self.dimensions = dimensions
    
    def evaluate(self, variables: List[float]) -> float:
        """Evaluate sphere function: sum(x_i^2)."""
        return sum(x ** 2 for x in variables)
    
    def gradient(self, variables: List[float]) -> List[float]:
        """Calculate gradient: 2*x_i."""
        return [2 * x for x in variables]


class RastriginFunction(ObjectiveFunction):
    """Rastrigin function (multimodal, many local minima)."""
    
    def __init__(self, dimensions: int = 2):
        """Initialize Rastrigin function."""
        super().__init__(OptimizationType.MINIMIZATION)
        self.dimensions = dimensions
        self.A = 10.0
    
    def evaluate(self, variables: List[float]) -> float:
        """Evaluate Rastrigin function."""
        n = len(variables)
        result = self.A * n
        
        for x in variables:
            result += x ** 2 - self.A * math.cos(2 * math.pi * x)
        
        return result


class GradientDescent:
    """Gradient descent optimization."""
    
    def __init__(self, learning_rate: float = 0.01, momentum: float = 0.0):
        """Initialize gradient descent."""
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.velocity = None
    
    def optimize(self, objective: ObjectiveFunction, 
                  initial: List[float], max_iterations: int = 1000,
                  tolerance: float = 1e-6) -> Solution:
        """Run gradient descent optimization."""
        variables = initial.copy()
        self.velocity = [0.0] * len(variables)
        
        for iteration in range(max_iterations):
            grad = objective.gradient(variables)
            
            # Update with momentum
            for i in range(len(variables)):
                self.velocity[i] = self.momentum * self.velocity[i] + self.learning_rate * grad[i]
                variables[i] -= self.velocity[i]
            
            # Check convergence
            grad_norm = math.sqrt(sum(g ** 2 for g in grad))
            if grad_norm < tolerance:
                break
        
        fitness = objective.evaluate(variables)
        
        return Solution(
            variables=variables,
            fitness=fitness,
            generation=iteration
        )


class StochasticGradientDescent:
    """Stochastic gradient descent with mini-batches."""
    
    def __init__(self, learning_rate: float = 0.01, batch_size: int = 32):
        """Initialize SGD."""
        self.learning_rate = learning_rate
        self.batch_size = batch_size
    
    def optimize(self, objective: ObjectiveFunction,
                  data: List[Tuple[List[float], float]],
                  initial: List[float], epochs: int = 100) -> Solution:
        """Run SGD optimization."""
        variables = initial.copy()
        
        for epoch in range(epochs):
            # Shuffle data
            random.shuffle(data)
            
            # Mini-batch updates
            for i in range(0, len(data), self.batch_size):
                batch = data[i:i + self.batch_size]
                
                # Compute gradient approximation
                grad = [0.0] * len(variables)
                
                for x, y in batch:
                    # Approximate gradient (simplified)
                    prediction = sum(v * xv for v, xv in zip(variables, x))
                    error = prediction - y
                    
                    for j in range(len(variables)):
                        grad[j] += error * x[j]
                
                grad = [g / len(batch) for g in grad]
                
                # Update
                for j in range(len(variables)):
                    variables[j] -= self.learning_rate * grad[j]
        
        fitness = objective.evaluate(variables)
        
        return Solution(
            variables=variables,
            fitness=fitness,
            generation=epochs
        )


class GeneticAlgorithm:
    """Genetic algorithm optimization."""
    
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.1,
                 crossover_rate: float = 0.8, elite_size: int = 2):
        """Initialize genetic algorithm."""
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
    
    def initialize_population(self, bounds: List[Tuple[float, float]],
                             population_size: Optional[int] = None) -> List[Solution]:
        """Initialize random population."""
        pop_size = population_size or self.population_size
        population = []
        
        for _ in range(pop_size):
            variables = [random.uniform(low, high) for low, high in bounds]
            population.append(Solution(variables=variables, fitness=0.0))
        
        return population
    
    def evaluate_population(self, population: List[Solution],
                            objective: ObjectiveFunction) -> None:
        """Evaluate fitness of all solutions."""
        for solution in population:
            solution.fitness = objective.evaluate(solution.variables)
    
    def selection(self, population: List[Solution], tournament_size: int = 3) -> Solution:
        """Tournament selection."""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda s: s.fitness)
    
    def crossover(self, parent1: Solution, parent2: Solution) -> Tuple[Solution, Solution]:
        """Crossover two solutions."""
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        # Uniform crossover
        child1_vars = []
        child2_vars = []
        
        for v1, v2 in zip(parent1.variables, parent2.variables):
            if random.random() < 0.5:
                child1_vars.append(v1)
                child2_vars.append(v2)
            else:
                child1_vars.append(v2)
                child2_vars.append(v1)
        
        child1 = Solution(variables=child1_vars, fitness=0.0)
        child2 = Solution(variables=child2_vars, fitness=0.0)
        
        return child1, child2
    
    def mutate(self, solution: Solution, bounds: List[Tuple[float, float]]) -> Solution:
        """Mutate solution."""
        if random.random() > self.mutation_rate:
            return solution.copy()
        
        mutated_vars = solution.variables.copy()
        
        for i in range(len(mutated_vars)):
            if random.random() < 0.1:  # Mutation probability per gene
                low, high = bounds[i]
                mutated_vars[i] = random.uniform(low, high)
        
        return Solution(variables=mutated_vars, fitness=0.0)
    
    def optimize(self, objective: ObjectiveFunction, bounds: List[Tuple[float, float]],
                 max_generations: int = 100) -> Solution:
        """Run genetic algorithm optimization."""
        population = self.initialize_population(bounds)
        self.evaluate_population(population, objective)
        
        best_solution = max(population, key=lambda s: s.fitness)
        
        for generation in range(max_generations):
            # Elitism: keep best solutions
            sorted_pop = sorted(population, key=lambda s: s.fitness, reverse=True)
            new_population = [s.copy() for s in sorted_pop[:self.elite_size]]
            
            # Generate offspring
            while len(new_population) < self.population_size:
                parent1 = self.selection(population)
                parent2 = self.selection(population)
                
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1, bounds)
                child2 = self.mutate(child2, bounds)
                
                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)
            
            population = new_population
            self.evaluate_population(population, objective)
            
            # Track best
            current_best = max(population, key=lambda s: s.fitness)
            if current_best.fitness > best_solution.fitness:
                best_solution = current_best.copy()
        
        return best_solution


class SimulatedAnnealing:
    """Simulated annealing optimization."""
    
    def __init__(self, initial_temp: float = 100.0, cooling_rate: float = 0.95,
                 min_temp: float = 0.01):
        """Initialize simulated annealing."""
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
    
    def optimize(self, objective: ObjectiveFunction, bounds: List[Tuple[float, float]],
                 max_iterations: int = 1000) -> Solution:
        """Run simulated annealing."""
        # Initialize random solution
        variables = [random.uniform(low, high) for low, high in bounds]
        current_fitness = objective.evaluate(variables)
        
        best_solution = Solution(variables=variables, fitness=current_fitness)
        temperature = self.initial_temp
        
        for iteration in range(max_iterations):
            if temperature < self.min_temp:
                break
            
            # Generate neighbor
            neighbor_vars = variables.copy()
            idx = random.randint(0, len(neighbor_vars) - 1)
            low, high = bounds[idx]
            neighbor_vars[idx] = random.uniform(low, high)
            
            neighbor_fitness = objective.evaluate(neighbor_vars)
            
            # Accept or reject
            delta = neighbor_fitness - current_fitness
            
            if objective.opt_type == OptimizationType.MINIMIZATION:
                delta = -delta  # Convert to minimization
            
            if delta > 0 or random.random() < math.exp(delta / temperature):
                variables = neighbor_vars
                current_fitness = neighbor_fitness
                
                if objective.opt_type == OptimizationType.MINIMIZATION:
                    if current_fitness < best_solution.fitness:
                        best_solution = Solution(variables=variables, fitness=current_fitness, generation=iteration)
                else:
                    if current_fitness > best_solution.fitness:
                        best_solution = Solution(variables=variables, fitness=current_fitness, generation=iteration)
            
            # Cool down
            temperature *= self.cooling_rate
        
        return best_solution


class ParticleSwarmOptimization:
    """Particle Swarm Optimization."""
    
    def __init__(self, swarm_size: int = 30, inertia: float = 0.7,
                 cognitive_coeff: float = 1.5, social_coeff: float = 1.5):
        """Initialize PSO."""
        self.swarm_size = swarm_size
        self.inertia = inertia
        self.cognitive_coeff = cognitive_coeff
        self.social_coeff = social_coeff
    
    def initialize_swarm(self, bounds: List[Tuple[float, float]],
                          swarm_size: Optional[int] = None) -> List[Solution]:
        """Initialize particle swarm."""
        size = swarm_size or self.swarm_size
        swarm = []
        
        for _ in range(size):
            variables = [random.uniform(low, high) for low, high in bounds]
            velocity = [random.uniform(-1, 1) for _ in range(len(variables))]
            personal_best = variables.copy()
            
            particle = Solution(variables=variables, fitness=0.0)
            particle.velocity = velocity
            particle.personal_best = personal_best
            particle.personal_best_fitness = float('inf')
            
            swarm.append(particle)
        
        return swarm
    
    def optimize(self, objective: ObjectiveFunction, bounds: List[Tuple[float, float]],
                 max_iterations: int = 100) -> Solution:
        """Run PSO optimization."""
        swarm = self.initialize_swarm(bounds)
        
        # Initialize global best
        for particle in swarm:
            particle.fitness = objective.evaluate(particle.variables)
            particle.personal_best_fitness = particle.fitness
        
        global_best = min(swarm, key=lambda p: p.fitness)
        global_best_position = global_best.variables.copy()
        
        for iteration in range(max_iterations):
            for particle in swarm:
                # Update velocity
                r1, r2 = random.random(), random.random()
                
                for i in range(len(particle.variables)):
                    cognitive = self.cognitive_coeff * r1 * (particle.personal_best[i] - particle.variables[i])
                    social = self.social_coeff * r2 * (global_best_position[i] - particle.variables[i])
                    
                    particle.velocity[i] = (self.inertia * particle.velocity[i] +
                                           cognitive + social)
                    
                    # Update position
                    particle.variables[i] += particle.velocity[i]
                    
                    # Apply bounds
                    low, high = bounds[i]
                    particle.variables[i] = max(low, min(high, particle.variables[i]))
            
            # Evaluate fitness
            for particle in swarm:
                particle.fitness = objective.evaluate(particle.variables)
                
                # Update personal best
                if particle.fitness < particle.personal_best_fitness:
                    particle.personal_best = particle.variables.copy()
                    particle.personal_best_fitness = particle.fitness
                
                # Update global best
                if particle.fitness < global_best.fitness:
                    global_best = particle.copy()
                    global_best_position = global_best.variables.copy()
        
        return global_best


class HillClimbing:
    """Hill climbing optimization."""
    
    def __init__(self, step_size: float = 0.1):
        """Initialize hill climbing."""
        self.step_size = step_size
    
    def optimize(self, objective: ObjectiveFunction, bounds: List[Tuple[float, float]],
                 max_iterations: int = 1000) -> Solution:
        """Run hill climbing."""
        # Initialize random solution
        variables = [random.uniform(low, high) for low, high in bounds]
        current_fitness = objective.evaluate(variables)
        
        best_solution = Solution(variables=variables, fitness=current_fitness)
        
        for iteration in range(max_iterations):
            improved = False
            
            # Try moves in each dimension
            for i in range(len(variables)):
                # Try positive move
                original = variables[i]
                variables[i] = min(bounds[i][1], variables[i] + self.step_size)
                fitness = objective.evaluate(variables)
                
                if fitness < current_fitness:
                    current_fitness = fitness
                    improved = True
                else:
                    # Try negative move
                    variables[i] = max(bounds[i][0], variables[i] - 2 * self.step_size)
                    variables[i] = max(bounds[i][0], variables[i])  # Clamp
                    
                    fitness = objective.evaluate(variables)
                    
                    if fitness < current_fitness:
                        current_fitness = fitness
                        improved = True
                    else:
                        variables[i] = original  # Revert
                
                if improved:
                    if current_fitness < best_solution.fitness:
                        best_solution = Solution(variables=variables.copy(), fitness=current_fitness, generation=iteration)
                    break  # Move to next dimension if improved
        
        return best_solution


class TabuSearch:
    """Tabu search optimization."""
    
    def __init__(self, tabu_list_size: int = 10, tabu_tenure: int = 5):
        """Initialize tabu search."""
        self.tabu_list_size = tabu_list_size
        self.tabu_tenure = tabu_tenure
        self.tabu_list: List[List[float]] = []
        self.tabu_tenure_list: List[int] = []
    
    def _is_tabu(self, solution: List[float]) -> bool:
        """Check if solution is in tabu list."""
        return solution in self.tabu_list
    
    def _add_to_tabu(self, solution: List[float]) -> None:
        """Add solution to tabu list."""
        if solution not in self.tabu_list:
            self.tabu_list.append(solution)
            self.tabu_tenure_list.append(self.tabu_tenure)
        
        # Manage tabu list size
        if len(self.tabu_list) > self.tabu_list_size:
            self.tabu_list.pop(0)
            self.tabu_tenure_list.pop(0)
    
    def _decrement_tenure(self) -> None:
        """Decrement tenure of all tabu solutions."""
        self.tabu_tenure_list = [t - 1 for t in self.tabu_tenure_list]
        
        # Remove expired
        while self.tabu_tenure_list and self.tabu_tenure_list[0] < 0:
            self.tabu_list.pop(0)
            self.tabu_tenure_list.pop(0)
    
    def optimize(self, objective: ObjectiveFunction, bounds: List[Tuple[float, float]],
                 max_iterations: int = 100) -> Solution:
        """Run tabu search."""
        # Initialize random solution
        variables = [random.uniform(low, high) for low, high in bounds]
        current_fitness = objective.evaluate(variables)
        
        best_solution = Solution(variables=variables, fitness=current_fitness)
        
        for iteration in range(max_iterations):
            self._decrement_tenure()
            
            # Generate neighbors
            neighbors = []
            
            for i in range(len(variables)):
                for delta in [-0.1, 0.1]:
                    neighbor = variables.copy()
                    neighbor[i] = max(bounds[i][0], min(bounds[i][1], neighbor[i] + delta))
                    neighbors.append(neighbor)
            
            # Find best non-tabu neighbor
            best_neighbor = None
            best_neighbor_fitness = float('inf')
            
            for neighbor in neighbors:
                if not self._is_tabu(neighbor):
                    fitness = objective.evaluate(neighbor)
                    if fitness < best_neighbor_fitness:
                        best_neighbor = neighbor
                        best_neighbor_fitness = fitness
            
            if best_neighbor and best_neighbor_fitness < current_fitness:
                variables = best_neighbor
                current_fitness = best_neighbor_fitness
                self._add_to_tabu(variables)
                
                if current_fitness < best_solution.fitness:
                    best_solution = Solution(variables=variables.copy(), fitness=current_fitness, generation=iteration)
        
        return best_solution


class AntColonyOptimization:
    """Ant Colony Optimization for discrete problems."""
    
    def __init__(self, num_ants: int = 20, alpha: float = 1.0, beta: float = 2.0,
                 evaporation_rate: float = 0.1, q0: float = 1.0):
        """Initialize ACO."""
        self.num_ants = num_ants
        self.alpha = alpha  # Pheromone importance
        self.beta = beta    # Heuristic importance
        self.evaporation_rate = evaporation_rate
        self.q0 = q0
    
    def optimize(self, objective: Callable[[List[int]], float],
                 num_solutions: int, max_iterations: int = 100) -> Solution:
        """Run ACO optimization (simplified for TSP-like problems)."""
        # Initialize pheromone trails
        pheromone = {}
        
        # Generate initial solutions
        solutions = []
        for _ in range(self.num_ants):
            solution = random.sample(range(num_solutions), num_solutions)
            fitness = objective(solution)
            solutions.append((solution, fitness))
            
            # Initialize pheromone
            for i in range(len(solution)):
                edge = (solution[i], solution[(i + 1) % len(solution)])
                pheromone[edge] = self.q0
        
        best_solution = min(solutions, key=lambda x: x[1])
        
        for iteration in range(max_iterations):
            # Evaporate pheromone
            for edge in pheromone:
                pheromone[edge] *= (1 - self.evaporation_rate)
            
            # New solutions
            new_solutions = []
            
            for _ in range(self.num_ants):
                solution = []
                available = list(range(num_solutions))
                current = available.pop(random.randint(0, len(available)))
                solution.append(current)
                
                while available:
                    # Choose next city based on pheromone and heuristic
                    next_city = self._choose_next_city(solution, available, pheromone)
                    solution.append(next_city)
                    available.remove(next_city)
                
                fitness = objective(solution)
                new_solutions.append((solution, fitness))
                
                # Update pheromone
                for i in range(len(solution)):
                    edge = (solution[i], solution[(i + 1) % len(solution)])
                    pheromone[edge] = pheromone.get(edge, 0) + 1.0 / fitness
            
            # Update best solution
            current_best = min(new_solutions, key=lambda x: x[1])
            if current_best[1] < best_solution[1]:
                best_solution = current_best
        
        return Solution(variables=best_solution[0], fitness=best_solution[1])


class ConstraintHandler:
    """Constraint handling utilities."""
    
    @staticmethod
    def penalty_method(solution: Solution, constraints: List[Callable],
                         penalty_factor: float = 1000.0) -> float:
        """Apply penalty for constraint violations."""
        penalty = 0.0
        
        for constraint in constraints:
            violation = constraint(solution.variables)
            if violation > 0:
                penalty += penalty_factor * violation
        
        return solution.fitness + penalty
    
    @staticmethod
    def repair_solution(solution: Solution, bounds: List[Tuple[float, float]]) -> Solution:
        """Repair solution to satisfy bounds."""
        repaired_vars = solution.variables.copy()
        
        for i, (low, high) in enumerate(bounds):
            repaired_vars[i] = max(low, min(high, repaired_vars[i]))
        
        return Solution(variables=repaired_vars, fitness=solution.fitness)


class MultiObjectiveOptimizer:
    """Multi-objective optimization utilities."""
    
    @staticmethod
    def pareto_dominance(solution1: Solution, solution2: Solution) -> bool:
        """Check if solution1 dominates solution2."""
        better_in_all = True
        better_in_at_least_one = False
        
        if solution1.fitness < solution2.fitness:  # Assuming minimization
            better_in_all = False
        elif solution1.fitness > solution2.fitness:
            better_in_at_least_one = True
        
        return better_in_all and better_in_at_least_one
    
    @staticmethod
    def find_pareto_front(solutions: List[Solution]) -> List[Solution]:
        """Find Pareto front from solutions."""
        pareto_front = []
        
        for solution in solutions:
            is_dominated = False
            
            for other in solutions:
                if MultiObjectiveOptimizer.pareto_dominance(other, solution):
                    is_dominated = True
                    break
            
            if not is_dominated:
                pareto_front.append(solution)
        
        return pareto_front


class OptimizationBenchmark:
    """Benchmarking utilities for optimization algorithms."""
    
    @staticmethod
    def compare_algorithms(objective: ObjectiveFunction, bounds: List[Tuple[float, float]],
                            algorithms: Dict[str, Callable]) -> Dict:
        """Compare multiple optimization algorithms."""
        results = {}
        
        for name, algorithm in algorithms:
            start = 0  # Use time module in real implementation
            solution = algorithm(objective, bounds)
            end = 0
            
            results[name] = {
                "fitness": solution.fitness,
                "generations": solution.generation,
                "time": end - start
            }
        
        return results


def demonstrate_optimization():
    """Demonstrate optimization algorithms functionality."""
    print("=== Optimization Algorithms Demonstration ===\n")
    
    # Objective Functions
    print("1. Objective Functions:")
    sphere = SphereFunction(dimensions=2)
    rastrigin = RastriginFunction(dimensions=2)
    
    test_vars = [1.0, 2.0]
    sphere_fitness = sphere.evaluate(test_vars)
    rastrigin_fitness = rastrigin.evaluate(test_vars)
    
    print(f"   Sphere function fitness: {sphere_fitness}")
    print(f"   Rastrigin function fitness: {rastrigin_fitness}")
    
    # Gradient Descent
    print("\n2. Gradient Descent:")
    gd = GradientDescent(learning_rate=0.1)
    gd_result = gd.optimize(sphere, [5.0, 5.0], max_iterations=100)
    
    print(f"   Optimal variables: {[f'{v:.4f}' for v in gd_result.variables]}")
    print(f"   Final fitness: {gd_result.fitness:.6f}")
    print(f"   Generations: {gd_result.generation}")
    
    # Genetic Algorithm
    print("\n3. Genetic Algorithm:")
    ga = GeneticAlgorithm(population_size=50, mutation_rate=0.1)
    bounds = [(-5.12, 5.12), (-5.12, 5.12)]
    
    ga_result = ga.optimize(rastrigin, bounds, max_generations=50)
    print(f"   Optimal variables: {[f'{v:.4f}' for v in ga_result.variables]}")
    print(f"   Final fitness: {ga_result.fitness:.6f}")
    print(f"   Generations: {ga_result.generation}")
    
    # Simulated Annealing
    print("\n4. Simulated Annealing:")
    sa = SimulatedAnnealing(initial_temp=100.0, cooling_rate=0.95)
    sa_result = sa.optimize(sphere, bounds, max_iterations=100)
    
    print(f"   Optimal variables: {[f'{v:.4f}' for v in sa_result.variables]}")
    print(f"   Final fitness: {sa_result.fitness:.6f}")
    print(f"   Generations: {sa_result.generation}")
    
    # Particle Swarm Optimization
    print("\n5. Particle Swarm Optimization:")
    pso = ParticleSwarmOptimization(swarm_size=20)
    pso_result = pso.optimize(sphere, bounds, max_iterations=50)
    
    print(f"   Optimal variables: {[f'{v:.4f}' for v in pso_result.variables]}")
    print(f"   Final fitness: {pso_result.fitness:.6f}")
    print(f"   Generations: {pso_result.generation}")
    
    # Hill Climbing
    print("\n6. Hill Climbing:")
    hc = HillClimbing(step_size=0.1)
    hc_result = hc.optimize(sphere, bounds, max_iterations=100)
    
    print(f"   Optimal variables: {[f'{v:.4f}' for v in hc_result.variables]}")
    print(f"   Final fitness: {hc_result.fitness:.6f}")
    print(f" Generations: {hc_result.generation}")
    
    # Tabu Search
    print("\n7. Tabu Search:")
    ts = TabuSearch(tabu_list_size=10, tabu_tenure=5)
    ts_result = ts.optimize(sphere, bounds, max_iterations=50)
    
    print(f"   Optimal variables: [f'{v:.4f}' for v in ts_result.variables]}")
    print(f"   Final fitness: {ts_result.fitness:.6f}")
    print(f"   Generations: {ts_result.generation}")
    
    # Multi-objective
    print("\n8. Multi-Objective Optimization:")
    solutions = [
        Solution(variables=[1.0, 1.0], fitness=5.0),
        Solution(variables=[2.0, 2.0], fitness=3.0),
        Solution(variables=[1.5, 1.5], fitness=4.0),
        Solution(variables=[0.5, 0.5], fitness=6.0)
    ]
    
    pareto_front = MultiObjectiveOptimizer.find_pareto_front(solutions)
    print(f"   Pareto front size: {len(pareto_front)}")
    print(f"   Pareto front fitnesses: {[s.fitness for s in pareto_front]}")
    
    # Constraint Handling
    print("\n9. Constraint Handling:")
    constrained_solution = Solution(variables=[6.0, 6.0], fitness=25.0)
    bounds = [(-5.0, 5.0), (-5.0, 5.0)]
    
    repaired = ConstraintHandler.repair_solution(constrained_solution, bounds)
    print(f"   Original: {[f'{v:.2f}' for v in constrained_solution.variables]}")
    print(f"   Repaired: {[f'{v:.2f}' for v in repaired.variables]}")
    
    print("\n=== Demonstration Complete ===")
    print("\nOptimization Best Practices:")
    print("- Choose algorithm based on problem characteristics")
    print("- Gradient descent for smooth, convex functions")
    print("- Genetic algorithms for complex, non-differentiable problems")
    print("- Simulated annealing for avoiding local optima")
    print("- PSO for continuous optimization")
    print("- Hill climbing for simple, unimodal problems")
    print("- Tabu search for escaping local optima")
    print("- ACO for discrete combinatorial problems")
    print("- Use appropriate population sizes for evolutionary algorithms")
    print("- Tune hyperparameters for your specific problem")
    print("- Use multiple restarts for stochastic algorithms")
    print("- Consider constraints and penalties")
    print("- Use multi-objective methods for trade-off analysis")


if __name__ == "__main__":
    demonstrate_optimization()
