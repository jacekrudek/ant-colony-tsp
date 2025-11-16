# in src/aco/colony.py
import random
from src.aco.ant import Ant # We will create this next

class Colony:
    def __init__(self, problem, num_ants, alpha, beta, evaporation_rate):
        self.problem = problem
        self.num_ants = num_ants
        
        # --- Algorithm Parameters ---
        self.alpha = alpha  # Pheromone importance
        self.beta = beta    # Heuristic (distance) importance
        self.evaporation_rate = evaporation_rate

        # --- State ---
        self.pheromone_matrix = self._init_pheromones()
        self.ants = [Ant(self) for _ in range(self.num_ants)]
        self.best_path = None
        self.best_path_length = float('inf')

        self.last_iteration_paths = []

    def _init_pheromones(self):
        # Initialize pheromones on all edges to a small value
        matrix = {}
        n = self.problem.num_vertices
        for i in range(n):
            matrix[i] = {}
            for j in range(n):
                if i != j:
                    matrix[i][j] = 1.0  # Initial pheromone level
        return matrix

    def run_iteration(self):
        # 1. Let all ants find a path
        all_paths = []
        for ant in self.ants:
            path, length = ant.find_tour()
            all_paths.append((path, length))
            
            # Update best path if this ant found a better one
            if length < self.best_path_length:
                self.best_path_length = length
                self.best_path = path
        
        self.last_iteration_paths = list(all_paths)

        # 2. Evaporate all pheromones
        for i in self.pheromone_matrix:
            for j in self.pheromone_matrix[i]:
                self.pheromone_matrix[i][j] *= (1.0 - self.evaporation_rate)

        # 3. Deposit new pheromones based on ant paths
        for path, length in all_paths:
            pheromone_to_deposit = 1.0 / length
            for i in range(len(path) - 1):
                vertice_a = path[i]
                vertice_b = path[i+1]
                self.pheromone_matrix[vertice_a][vertice_b] += pheromone_to_deposit
                self.pheromone_matrix[vertice_b][vertice_a] += pheromone_to_deposit # For symmetric TSP

        # Compute statistics for this iteration
        lengths = [length for (_, length) in all_paths] if all_paths else []
        avg_length = sum(lengths) / len(lengths) if lengths else 0.0
        min_length = min(lengths) if lengths else float('inf')

        return {
            "avg_length": avg_length,
            "min_length": min_length,
            "best_length": self.best_path_length,
            "paths_count": len(lengths)
        }