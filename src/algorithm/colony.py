from src.algorithm.ant import Ant  

class Colony:
    def __init__(self, num_ants):

        self.num_ants = num_ants
        self.ants = [Ant() for _ in range(num_ants)]

    def find_paths(self, graph, pheromone_matrix, alpha, beta):
        all_paths = []
        for ant in self.ants:
            path, length = ant.find_tour(graph, pheromone_matrix, alpha, beta)
            all_paths.append((path, length))

            # Update best path if this ant found a better one
            if length < graph.best_path_length:
                graph.best_path_length = length
                graph.best_path = path

        graph.last_iteration_paths = list(all_paths)
        

        return all_paths
