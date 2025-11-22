import random

from src.map.vertice import Vertice
from src.config import CENTER_WIDTH, SCREEN_HEIGHT


class Graph:
    def __init__(self, num_vertices):
        self.best_path = None
        self.best_path_length = float('inf')

        self.last_iteration_paths = []

        self.num_vertices = num_vertices

        self.vertices = [
            Vertice(random.randint(0, CENTER_WIDTH - 20), random.randint(0, SCREEN_HEIGHT - 20))
            for _ in range(num_vertices)
        ]

        self.distance_matrix = []
        self.calculate_distances()
        

    def calculate_distances(self):
        matrix = {}

        for i, vertice_a in enumerate(self.vertices):
            matrix[i] = {}

            for j, vertice_b in enumerate(self.vertices):
                if i == j:
                    matrix[i][j] = 0.0
                else:
                    matrix[i][j] = vertice_a.distance_to(vertice_b)

        self.distance_matrix = matrix
    
    def get_edge_grade(self, i, j):
        d = self.distance_matrix[i][j]

        if d <= 0:
            return 0.0
        
        return 1 / d
    
    def rebuild(self):
        self.calculate_distances()
        self.last_iteration_paths = []
        self.best_path = None
        self.best_path_length = float('inf')