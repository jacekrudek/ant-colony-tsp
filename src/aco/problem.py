from src.aco.vertice import Vertice
import random

class TSPProblem:
    def __init__(self, num_vertices, width, height):
        # Create random vertices within the "game" area
        self.vertices = [
            Vertice(random.randint(0, width), random.randint(0, height)) 
            for _ in range(num_vertices)
        ]
        self.num_vertices = num_vertices
        self.distance_matrix = self._calculate_distances()

    def _calculate_distances(self):
        matrix = {}
        for i, vertice_a in enumerate(self.vertices):
            matrix[i] = {}
            for j, vertice_b in enumerate(self.vertices):
                if i == j:
                    matrix[i][j] = 0.0
                else:
                    matrix[i][j] = vertice_a.distance_to(vertice_b)
        return matrix