from src.aco.ant import Ant  

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

        # store last iteration paths for UI
        self.last_iteration_paths = list(all_paths)

        # 2. Evaporate all pheromones 
        for i in self.pheromone_matrix:
            for j in self.pheromone_matrix[i]:
                self.pheromone_matrix[i][j] *= (1.0 - self.evaporation_rate)
                

        # Deposit from all ants proportional to tour quality (1 / length).
        # We scale per-ant deposits by 1/num_ants to keep total deposit magnitude comparable
        # to the single-best strategy and avoid runaway pheromone values.
        per_ant_scale = 1.0 / max(1, self.num_ants)
        for path, length in all_paths:
            if not path or length is None or length <= 0:
                continue
            delta = (1.0 / length) * per_ant_scale
            for k in range(len(path) - 1):
                a = path[k]
                b = path[k + 1]

                # add pheromone (no upper clamp)
                self.pheromone_matrix[a][b] += delta
                self.pheromone_matrix[b][a] += delta

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