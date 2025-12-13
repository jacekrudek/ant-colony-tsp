import pytest
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

if project_root not in sys.path:
    sys.path.insert(0, project_root)


from src.algorithm.aco_engine import AcoEngine

class TestAcoEngine:
    def test_initialization_with_default_graph(self):
        """Test AcoEngine initialization with default graph"""
        engine = AcoEngine(
            alpha=1.5,
            beta=2.0,
            evaporation_rate=0.1,
            num_vertices=10,
            num_ants=20
        )
        
        assert engine.alpha == 1.5
        assert engine.beta == 2.0
        assert engine.evaporation_rate == 0.1
        assert engine.num_ants == 20
        
        # Check that components were created
        assert engine.pheromone_matrix is not None
        assert engine.colony is not None
        assert engine.graph is not None
        assert engine.graph.num_vertices == 10

   
    def test_get_stats_with_paths(self):
        """Test get_stats calculation with valid paths"""
        engine = AcoEngine(
            alpha=1.0,
            beta=1.0,
            evaporation_rate=0.1,
            num_vertices=3,
            num_ants=5
        )
        
        # Mock graph best path length
        engine.graph.best_path_length = 8.0
        
        # Test paths: lengths are 10.0, 12.0, 9.0
        test_paths = [
            ([0, 1, 2], 10.0),
            ([1, 2, 0], 12.0),
            ([2, 0, 1], 9.0)
        ]
        
        stats = engine.get_stats(test_paths)
        
        assert stats["avg_length"] == pytest.approx(10.333, rel=1e-2)  # (10+12+9)/3
        assert stats["min_length"] == 9.0
        assert stats["best_length"] == 8.0
        assert stats["paths_count"] == 3

    def test_get_stats_with_empty_paths(self):
        """Test get_stats with empty paths list"""
        engine = AcoEngine(
            alpha=1.0,
            beta=1.0,
            evaporation_rate=0.1,
            num_vertices=3,
            num_ants=5
        )
        
        engine.graph.best_path_length = 15.5
        
        stats = engine.get_stats([])
        
        assert stats["avg_length"] == 0.0
        assert stats["min_length"] == float('inf')
        assert stats["best_length"] == 15.5
        assert stats["paths_count"] == 0

    def test_get_stats_with_single_path(self):
        """Test get_stats with single path"""
        engine = AcoEngine(
            alpha=1.0,
            beta=1.0,
            evaporation_rate=0.1,
            num_vertices=3,
            num_ants=5
        )
        
        engine.graph.best_path_length = 7.5
        
        single_path = [([0, 1, 2], 11.25)]
        stats = engine.get_stats(single_path)
        
        assert stats["avg_length"] == 11.25
        assert stats["min_length"] == 11.25
        assert stats["best_length"] == 7.5
        assert stats["paths_count"] == 1
    

    def test_parameter_storage(self):
        """Test that all parameters are correctly stored"""
        engine = AcoEngine(
            alpha=2.5,
            beta=1.8,
            evaporation_rate=0.05,
            num_vertices=25,
            num_ants=100
        )
        
        assert engine.alpha == 2.5
        assert engine.beta == 1.8
        assert engine.evaporation_rate == 0.05
        assert engine.num_ants == 100