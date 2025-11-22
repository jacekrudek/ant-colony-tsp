from src.algorithm.vertice import Vertice
import random

from src.config import CENTER_WIDTH, SCREEN_HEIGHT


class TSPProblem:
    def __init__(self, num_vertices):
        # Create random vertices within the "game" area
        self.vertices = [
            Vertice(random.randint(0, CENTER_WIDTH - 20), random.randint(0, SCREEN_HEIGHT - 20)) 
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
    
    def rebuild(self):
        """Recompute num_vertices and distance_matrix from current vertices list."""
        self.num_vertices = len(self.vertices)
        self.distance_matrix = self._calculate_distances()