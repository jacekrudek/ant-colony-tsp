from src.map.pheromone_matrix import PheromoneMatrix
from src.algorithm.colony import Colony
from src.map.graph import Graph


class AcoEngine:
    def __init__(self, alpha, beta, evaporation_rate, num_vertices, num_ants, graph = None):

        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.num_ants = num_ants

        self.pheromone_matrix = PheromoneMatrix(num_vertices, evaporation_rate)

        self.colony = Colony(num_ants)

        if graph is None:
            self.graph = Graph(num_vertices)
        else:
            self.graph = graph
            self.graph.rebuild()



    def run_iteration(self):
        self.pheromone_matrix.reset_pending()

        all_paths = self.colony.find_paths(self.graph, self.pheromone_matrix, self.alpha, self.beta)

        self.pheromone_matrix.apply_pending()

        self.get_stats(all_paths)

    def get_stats(self, all_paths):
        lengths = [length for (_, length) in all_paths] if all_paths else []
        avg_length = sum(lengths) / len(lengths) if lengths else 0.0
        min_length = min(lengths) if lengths else float('inf')

        return {
            "avg_length": avg_length,
            "min_length": min_length,
            "best_length": self.graph.best_path_length,
            "paths_count": len(lengths)
        }

