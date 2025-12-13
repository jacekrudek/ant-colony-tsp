import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.algorithm.colony import Colony
from src.map.graph import Graph
from src.map.pheromone_matrix import PheromoneMatrix


class TestColony:
    def test_initialization(self):
        """Test Colony initialization with correct number of ants"""
        colony = Colony(5)
        
        assert colony.num_ants == 5
        assert len(colony.ants) == 5
        
        # Check that all ants are Ant instances
        from src.algorithm.ant import Ant
        for ant in colony.ants:
            assert isinstance(ant, Ant)

    def test_initialization_zero_ants(self):
        """Test Colony initialization with zero ants"""
        colony = Colony(0)
        
        assert colony.num_ants == 0
        assert len(colony.ants) == 0

    def test_find_paths_returns_correct_format(self):
        """Test that find_paths returns list of (path, length) tuples"""
        
        graph = Graph(3)
        pheromone_matrix = PheromoneMatrix(3, 0.1)
        colony = Colony(2)  # 2 ants
        
        all_paths = colony.find_paths(graph, pheromone_matrix, alpha=1.0, beta=1.0)
        
        # Should return 2 paths (one for each ant)
        assert len(all_paths) == 2
        
        # Each element should be (path, length) tuple
        for path, length in all_paths:
            assert isinstance(path, list)
            assert isinstance(length, (int, float))
            assert length >= 0.0

    def test_find_paths_updates_graph_best_path(self):
        """Test that find_paths updates graph's best path when better one is found"""
        
        graph = Graph(3)
        pheromone_matrix = PheromoneMatrix(3, 0.1)
        
        # Set initial best path length to very high value
        graph.best_path_length = 3000.0
        graph.best_path = None
        
        colony = Colony(3)  # 3 ants
        all_paths = colony.find_paths(graph, pheromone_matrix, alpha=1.0, beta=1.0)
        
        # Best path should be updated (should be much less than 1000.0)
        assert graph.best_path_length < 3000.0
        assert graph.best_path is not None
        assert isinstance(graph.best_path, list)

    def test_find_paths_stores_last_iteration_paths(self):
        """Test that find_paths stores all paths in graph.last_iteration_paths"""
        from src.map.graph import Graph
        from src.map.pheromone_matrix import PheromoneMatrix
        
        graph = Graph(3)
        pheromone_matrix = PheromoneMatrix(3, 0.1)
        colony = Colony(2)
        
        all_paths = colony.find_paths(graph, pheromone_matrix, alpha=1.0, beta=1.0)
        
        # last_iteration_paths should contain same paths as returned
        assert graph.last_iteration_paths == all_paths
        assert len(graph.last_iteration_paths) == 2

    def test_find_paths_with_single_ant(self):
        """Test find_paths with single ant"""
        from src.map.graph import Graph
        from src.map.pheromone_matrix import PheromoneMatrix
        
        graph = Graph(4)
        pheromone_matrix = PheromoneMatrix(4, 0.1)
        colony = Colony(1)  # Single ant
        
        all_paths = colony.find_paths(graph, pheromone_matrix, alpha=2.0, beta=1.5)
        
        assert len(all_paths) == 1
        path, length = all_paths[0]
        assert len(path) == 5  # 4 vertices + return = 5
        assert path[0] == path[-1]  # Closed tour

    def test_find_paths_improves_best_path_over_iterations(self):
        """Test that multiple ants might find better solutions"""
        from src.map.graph import Graph
        from src.map.pheromone_matrix import PheromoneMatrix
        
        graph = Graph(4)
        pheromone_matrix = PheromoneMatrix(4, 0.1)
        colony = Colony(10)  # More ants = higher chance of good solution
        
        # Run multiple times to see if we get different results
        first_run = colony.find_paths(graph, pheromone_matrix, alpha=1.0, beta=1.0)
        first_best = graph.best_path_length
        
        # Reset and run again
        graph.best_path_length = float('inf')
        second_run = colony.find_paths(graph, pheromone_matrix, alpha=1.0, beta=1.0)
        second_best = graph.best_path_length
        
        # Both should find valid solutions
        assert first_best > 0
        assert second_best > 0
        assert len(first_run) == 10
        assert len(second_run) == 10