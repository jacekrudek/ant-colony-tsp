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
        self.pheromone_matrix = self._init_pheromones(1.0)
        self.pending_pheromone_matrix = self._init_pheromones(0.0)
        self.ants = [Ant(self) for _ in range(self.num_ants)]

        self.best_path = None
        self.best_path_length = float('inf')

        self.last_iteration_paths = []

    def reset_pending(self):
        n = self.problem.num_vertices
        for i in range(n):
            row = self.pending_pheromone_matrix[i]
            for j in range(n):
                row[j] = 0.0

    def compute_edge_grade(self, i, j):
        d = self.problem.distance_matrix[i][j]
        if d <= 0:
            return 0.0
        return 1 / d
    
    
    
    # Ants call this while walking to accumulate into the pending matrix
    def add_pending_pheromone(self, i, j, delta):
        self.pending_pheromone_matrix[i][j] += delta

    # Apply evaporation and then merge pending -> main, then clear pending
    def apply_pending(self, clamp_min=None, clamp_max=None):
        n = self.problem.num_vertices
        pm = self.pheromone_matrix
        pend = self.pending_pheromone_matrix

        # Evaporate
        evap = (1.0 - self.evaporation_rate)
        for i in range(n):
            for j in range(n):
                pm[i][j] *= evap

        # Merge pending
        for i in range(n):
            for j in range(n):
                pm[i][j] += pend[i][j]
                if clamp_min is not None and pm[i][j] < clamp_min:
                    pm[i][j] = clamp_min
                if clamp_max is not None and pm[i][j] > clamp_max:
                    pm[i][j] = clamp_max
                pend[i][j] = 0.0  # clear pending

    def _init_pheromones(self, init_pheromone_lvl):
        matrix = {}
        n = self.problem.num_vertices
        for i in range(n):
            matrix[i] = {}
            for j in range(n):
                if i != j:
                    matrix[i][j] = init_pheromone_lvl  # Initial pheromone level
                else:
                    matrix[i][j] = 0.0
        return matrix

    def run_iteration(self):
        self.reset_pending()
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

        self.apply_pending()

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