import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.algorithm.ant import Ant
from src.map.graph import Graph
from src.map.pheromone_matrix import PheromoneMatrix


class TestAnt:
    def test_initialization(self):
        """Test Ant initialization"""
        ant = Ant()
        assert ant is not None

    def test_find_tour_returns_path_and_length(self):
        """Test that find_tour returns a path and length"""
        
        # Create real objects
        graph = Graph(3)  # 3 vertices
        pheromone_matrix = PheromoneMatrix(3, 0.1)
        
        ant = Ant()
        path, length = ant.find_tour(graph, pheromone_matrix, alpha=1.0, beta=1.0)
        
        # Basic checks
        assert isinstance(path, list)
        assert isinstance(length, float)
        assert len(path) > 0
        assert length >= 0.0

    def test_find_tour_visits_all_vertices(self):
        """Test that tour visits all vertices exactly once plus return"""
        
        graph = Graph(4)  # 4 vertices
        pheromone_matrix = PheromoneMatrix(4, 0.1)
        
        ant = Ant()
        path, length = ant.find_tour(graph, pheromone_matrix, alpha=1.0, beta=1.0)
        
        # Should visit 4 vertices + return = 5 elements
        assert len(path) == 5
        # First and last should be same (closed tour)
        assert path[0] == path[-1]
        # Should visit all vertices 0,1,2,3
        unique_vertices = set(path[:-1])
        assert len(unique_vertices) == 4

    def test_find_tour_stores_parameters(self):
        """Test that ant stores the parameters correctly"""
        
        graph = Graph(2)
        pheromone_matrix = PheromoneMatrix(2, 0.1)
        
        ant = Ant()
        ant.find_tour(graph, pheromone_matrix, alpha=2.5, beta=3.0)
        
        assert ant.alpha == 2.5
        assert ant.beta == 3.0
        assert ant.graph is graph
        assert ant.pheromone_matrix is pheromone_matrix

    def test_path_is_valid_tour(self):
        """Test that generated path forms a valid tour"""
        
        graph = Graph(3)
        pheromone_matrix = PheromoneMatrix(3, 0.1)
        
        ant = Ant()
        path, length = ant.find_tour(graph, pheromone_matrix, alpha=1.0, beta=1.0)
        
        # Each vertex in path should be valid
        for vertex in path:
            assert 0 <= vertex < 3
        
        # Should be a closed tour
        assert path[0] == path[-1]
        
        # Length should be positive
        assert length > 0.0